from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest

from libs.application.commands.operation__command import OperationCommand
from libs.application.dtos.operation__dto import OperationRunners
from libs.application.errors.lifecycle__error import InvalidStepOpError, JobNotFoundError, StepNotAllowedError
from libs.application.mappers.operation__mapper import OperationMapper
from libs.application.queries.operation__query import OperationQuery
from libs.application.repositories.operation__repository import SqliteOperationRepository
from libs.common.clock import FrozenClock
from libs.common.enums import BackendKind, JobState, OperationKind, OperationState, PreparingStep
from libs.domain.entities.generation_job__entity import GenerationJobEntity
from libs.domain.entities.operation__entity import OperationEntity
from libs.domain.errors.job__error import UnconfirmedJobError
from libs.domain.value_objects.fingerprint__valueobject import Fingerprint
from libs.infrastructure.clients.sqlite__client import SqliteClient
from libs.infrastructure.readers.operation__reader import OperationReader
from libs.infrastructure.writers.operation__writer import OperationWriter
from tests.libs.application.lifecycle.fakes import (
    FakeJobRepository, InlineExecutor, advance, confirmed_job, image_request, video_request,
)
from tests.libs.domain.builders import T0


class BrokenRunner(Exception):
    error_code = "canary_failed"


class Env:
    def __init__(self, tmp_path: Path) -> None:
        self.client = SqliteClient(tmp_path / "bridge.db")
        self.calls: list[tuple[str, object]] = []
        self.fail_canary = False
        self.executor = InlineExecutor(manual=True)
        self.jobs = FakeJobRepository(self.client)
        self.operations = SqliteOperationRepository(OperationReader(self.client), OperationWriter(self.client))
        self.query = OperationQuery(OperationReader(self.client))
        self.command = OperationCommand(self.operations, self.executor, OperationRunners(
            canary=self._canary,
            resume_queue=lambda backend: self._record("resume_queue", backend, {"queue": "running"}),
            entity_sync=lambda: self._record("entity_sync", None, {"entities": 3}),
            step=lambda job_id, op: self._record("step", (job_id, op), {"reached": op.value}),
            step_submit=lambda job_id: self._record("step_submit", job_id, {"clicked": False}),
        ), FrozenClock(T0), self.jobs)

    def _canary(self, backend: BackendKind) -> dict[str, object]:
        if self.fail_canary:
            raise BrokenRunner("生成按钮找不到")
        return self._record("canary", backend, {"ok": True, "failed_checks": []})

    def _record(self, name: str, arg: object, result: dict[str, object]) -> dict[str, object]:
        self.calls.append((name, arg))
        return result


@pytest.fixture
def env(tmp_path: Path) -> Iterator[Env]:
    environment = Env(tmp_path)
    yield environment
    environment.client.close()


def test_canary_returns_immediately_and_runs_in_the_background(env: Env) -> None:
    started = env.command.start_canary(BackendKind.WEB)
    assert started.state == "pending" and started.kind == "canary" and env.calls == []
    assert env.executor.submitted == [(BackendKind.WEB, f"op:{started.operation_id}")]
    env.executor.run_pending()
    snapshot = env.query.get(started.operation_id)
    assert snapshot is not None and snapshot.state == "succeeded" and snapshot.result == {"failed_checks": [], "ok": True}
    assert env.calls == [("canary", BackendKind.WEB)] and snapshot.started_at is not None and snapshot.finished_at is not None


def test_runner_failure_is_persisted_on_the_operation(env: Env) -> None:
    env.fail_canary = True
    started = env.command.start_canary(BackendKind.WEB)
    env.executor.run_pending()
    snapshot = env.query.get(started.operation_id)
    assert snapshot is not None and (snapshot.state, snapshot.error_code, snapshot.error_message) == ("failed", "canary_failed", "生成按钮找不到")


def test_resume_queue_and_entity_sync_use_their_lanes(env: Env) -> None:
    env.command.start_resume_queue(BackendKind.CLI)
    env.command.start_entity_sync()
    assert [lane for lane, _ in env.executor.submitted] == [BackendKind.CLI, BackendKind.WEB]


def test_step_works_on_unconfirmed_jobs_without_queueing_them(env: Env) -> None:
    request = video_request("shot02")
    env.jobs.save(GenerationJobEntity("raw", "batch-1", BackendKind.WEB, request, Fingerprint.of(request)))
    started = env.command.start_step("raw", "fill")
    env.executor.run_pending()
    snapshot = env.query.get(started.operation_id)
    assert snapshot is not None and (snapshot.job_id, snapshot.step, snapshot.subject_id) == ("raw", "fill", "raw#fill")
    assert env.calls == [("step", ("raw", PreparingStep.FILL))]
    stored = env.jobs.get("raw")
    assert stored is not None and stored.state is JobState.QUEUED and not stored.confirmed


def test_step_validation(env: Env) -> None:
    with pytest.raises(InvalidStepOpError):
        env.command.start_step("raw", "submit")
    with pytest.raises(JobNotFoundError):
        env.command.start_step("missing", "fill")
    env.jobs.save(confirmed_job("cli-a", image_request("c1-1"), BackendKind.CLI))
    with pytest.raises(StepNotAllowedError):
        env.command.start_step("cli-a", "fill")
    env.jobs.save(advance(confirmed_job("gen", video_request("shot03")), JobState.GENERATING))
    with pytest.raises(StepNotAllowedError):
        env.command.start_step("gen", "preview")


def test_step_submit_requires_a_confirmed_queued_job(env: Env) -> None:
    request = video_request("shot04")
    env.jobs.save(GenerationJobEntity("raw", "batch-1", BackendKind.WEB, request, Fingerprint.of(request)))
    with pytest.raises(UnconfirmedJobError):
        env.command.start_step_submit("raw")
    env.jobs.save(confirmed_job("ok", video_request("shot05")))
    assert env.command.start_step_submit("ok").kind == "step_submit"


def test_recover_fails_operations_interrupted_by_restart(env: Env) -> None:
    started = env.command.start_entity_sync()
    assert env.command.recover() == 1
    snapshot = env.query.get(started.operation_id)
    assert snapshot is not None and (snapshot.state, snapshot.error_code) == ("failed", "interrupted_by_restart")
    assert env.operations.list_unfinished() == []


def test_mapper_round_trip() -> None:
    operation = OperationEntity("op_1", OperationKind.STEP, T0, OperationMapper.step_subject("job-1", "upload"))
    operation.start(T0)
    operation.succeed({"reached": "upload", "screens": ["a.jpg"]}, T0)
    loaded = OperationMapper.to_entity(OperationMapper.to_dao(operation))
    assert (loaded.kind, loaded.state, loaded.subject_id, dict(loaded.result or {})) == (
        OperationKind.STEP, OperationState.SUCCEEDED, "job-1#upload", {"reached": "upload", "screens": ["a.jpg"]},
    )
    assert loaded.started_at == T0 and loaded.finished_at == T0 and OperationMapper.to_dao(operation).job_id == "job-1"
