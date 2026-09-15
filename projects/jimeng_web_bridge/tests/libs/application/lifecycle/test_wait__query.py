from __future__ import annotations

from collections.abc import Callable, Iterator
from pathlib import Path

import pytest

from libs.application.errors.lifecycle__error import InvalidWaitTargetError
from libs.application.mappers.operation__mapper import OperationMapper
from libs.application.queries.wait__query import WaitQuery
from libs.common.enums import JobState, OperationKind, PauseReason
from libs.domain.entities.operation__entity import OperationEntity
from libs.domain.value_objects.global_config__valueobject import GlobalConfig
from libs.infrastructure.clients.sqlite__client import SqliteClient
from libs.infrastructure.readers.job__reader import JobReader
from libs.infrastructure.readers.operation__reader import OperationReader
from libs.infrastructure.writers.operation__writer import OperationWriter
from tests.libs.application.lifecycle.fakes import FakeJobRepository, advance, confirmed_job, video_request
from tests.libs.domain.builders import T0, global_data


class FakeTime:
    def __init__(self) -> None:
        self.now = 0.0
        self.hooks: list[tuple[float, Callable[[], None]]] = []

    def monotonic(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        assert seconds >= 0
        self.now += seconds
        for at, hook in list(self.hooks):
            if self.now >= at:
                self.hooks.remove((at, hook))
                hook()


class Env:
    def __init__(self, tmp_path: Path) -> None:
        self.client = SqliteClient(tmp_path / "bridge.db")
        self.jobs = FakeJobRepository(self.client)
        self.time = FakeTime()
        self.config = global_data()
        self.query = WaitQuery(
            JobReader(self.client), OperationReader(self.client), lambda: GlobalConfig.from_dict(self.config),
            monotonic=self.time.monotonic, sleep=self.time.sleep,
        )

    def job(self, job_id: str, state: JobState, batch_id: str = "batch-1") -> None:
        self.jobs.save(advance(confirmed_job(job_id, video_request(job_id), batch_id=batch_id), state))


@pytest.fixture
def env(tmp_path: Path) -> Iterator[Env]:
    environment = Env(tmp_path)
    yield environment
    environment.client.close()


def test_timeout_is_clamped_to_max_call_s_with_progress_every_interval(env: Env) -> None:
    env.job("job-a", JobState.GENERATING)
    progress: list[tuple[float, float | None, str]] = []
    result = env.query.wait(job_ids=["job-a"], timeout_s=600, on_progress=lambda *args: progress.append(args))
    assert (result.finished, result.timeout_s, result.waited_s, env.time.now) == (False, 85.0, 85.0, 85.0)
    assert [elapsed for elapsed, _, _ in progress] == [0.0, 25.0, 50.0, 75.0]
    assert all(total == 85.0 for _, total, _ in progress) and result.suggested_next == "仍在进行中：再次调用 wait"


def test_cadence_follows_config(env: Env) -> None:
    api = env.config["api"]
    assert isinstance(api, dict)
    api.update({"max_call_s": 40, "progress_interval_s": 10})
    env.job("job-a", JobState.GENERATING)
    seen: list[float] = []
    env.query.wait(job_ids=["job-a"], on_progress=lambda elapsed, total, message: seen.append(elapsed))
    assert seen == [0.0, 10.0, 20.0, 30.0] and env.time.now == 40.0


def test_returns_as_soon_as_the_jobs_settle(env: Env) -> None:
    env.job("job-a", JobState.GENERATING)
    env.time.hooks.append((3.0, lambda: env.jobs.save(_downloaded_then_done(env))))
    result = env.query.wait(job_ids=["job-a"], timeout_s=60)
    assert result.finished and 3.0 <= result.waited_s <= 4.0
    assert result.snapshot.jobs[0].state == "done" and result.suggested_next.startswith("全部完成")


def _downloaded_then_done(env: Env):  # type: ignore[no-untyped-def]
    job = env.jobs.get("job-a")
    assert job is not None
    job.mark_downloading(T0)
    job.mark_done(T0)
    return job


def test_a_job_waiting_for_a_human_is_settled(env: Env) -> None:
    job = advance(confirmed_job("job-a", video_request("job-a")), JobState.PREPARING)
    job.pause(PauseReason.FILL_MISMATCH, T0)
    env.jobs.save(job)
    result = env.query.wait(job_ids=["job-a"], timeout_s=60)
    assert result.finished and env.time.now == 0.0 and "待人工处理" in result.suggested_next


def test_batch_target_counts_every_job(env: Env) -> None:
    env.job("job-a", JobState.DONE)
    env.job("job-b", JobState.QUEUED)
    env.job("other", JobState.QUEUED, batch_id="batch-2")
    result = env.query.wait(batch_id="batch-1", timeout_s=0)
    assert not result.finished and result.snapshot.total_jobs == 2
    assert {(item.state, item.count) for item in result.snapshot.counts} == {("done", 1), ("queued", 1)}


def test_operation_target(env: Env) -> None:
    operation = OperationEntity("op_1", OperationKind.CANARY, T0, "web")
    operation.start(T0)
    writer = OperationWriter(env.client)
    writer.save(OperationMapper.to_dao(operation))

    def finish() -> None:
        operation.succeed({"ok": True}, T0)
        writer.save(OperationMapper.to_dao(operation))

    env.time.hooks.append((2.0, finish))
    result = env.query.wait(operation_id="op_1", timeout_s=30)
    assert result.finished and result.snapshot.operation is not None and result.snapshot.operation.result == {"ok": True}


@pytest.mark.parametrize("kwargs", [{}, {"job_ids": ["a"], "batch_id": "b"}, {"job_ids": []}])
def test_exactly_one_target(env: Env, kwargs: dict[str, object]) -> None:
    with pytest.raises(InvalidWaitTargetError):
        env.query.wait(**kwargs)  # type: ignore[arg-type]


def test_unknown_ids_are_reported_not_waited_on(env: Env) -> None:
    result = env.query.wait(job_ids=["ghost"], timeout_s=30)
    assert result.finished and result.snapshot.missing_job_ids == ("ghost",) and env.time.now == 0.0
