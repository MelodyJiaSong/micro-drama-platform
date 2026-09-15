from __future__ import annotations

import time
from collections import Counter
from collections.abc import Callable, Sequence

from libs.application.dtos.operation__dto import OperationQdto
from libs.application.dtos.wait__dto import StateCountQdto, WaitJobQdto, WaitQdto, WaitSnapshotQdto
from libs.application.errors.lifecycle__error import InvalidWaitTargetError
from libs.application.mappers.operation__mapper import OperationMapper
from libs.application.queries.job__query import runtime_facts
from libs.common.enums import TERMINAL_JOB_STATES, BlockedOn, JobState, OperationState
from libs.domain.value_objects.global_config__valueobject import GlobalConfig
from libs.infrastructure.daos.job__dao import JobDao
from libs.infrastructure.readers.job__reader import JobReader
from libs.infrastructure.readers.operation__reader import OperationReader

BATCH_SCAN_LIMIT: int = 10_000
_SETTLED: frozenset[str] = frozenset({*(s.value for s in TERMINAL_JOB_STATES), JobState.PAUSED_NEEDS_HUMAN.value})
_FINISHED_OPERATION: frozenset[str] = frozenset({OperationState.SUCCEEDED.value, OperationState.FAILED.value})
_EPSILON: float = 1e-6

ProgressCallback = Callable[[float, float | None, str], None]


class WaitQuery:
    """Bounded wait on jobs, a batch or an operation (FR-52, §5.10 `/api/wait`).

    Never blocks longer than `api.max_call_s`; emits progress at the start and then exactly every
    `api.progress_interval_s`; re-reads the store about once per second. A job waiting for a human counts as settled,
    because waiting longer cannot move it.
    """

    def __init__(
        self,
        job_reader: JobReader,
        operation_reader: OperationReader,
        global_config_provider: Callable[[], GlobalConfig],
        monotonic: Callable[[], float] = time.monotonic,
        sleep: Callable[[float], None] = time.sleep,
        poll_interval_s: float = 1.0,
    ) -> None:
        self._jobs = job_reader
        self._operations = operation_reader
        self._global_config_provider = global_config_provider
        self._monotonic = monotonic
        self._sleep = sleep
        self._poll_interval_s = poll_interval_s

    def wait(
        self,
        job_ids: Sequence[str] | None = None,
        batch_id: str | None = None,
        operation_id: str | None = None,
        timeout_s: float | None = None,
        on_progress: ProgressCallback | None = None,
    ) -> WaitQdto:
        api = self._global_config_provider().api
        if sum(1 for target in (job_ids, batch_id, operation_id) if target) != 1:
            raise InvalidWaitTargetError("job_ids、batch_id、operation_id 必须恰好给一个")
        if job_ids and len(job_ids) > api.page_size_max:
            raise InvalidWaitTargetError(f"job_ids 最多 {api.page_size_max} 个")
        limit = float(api.max_call_s) if timeout_s is None else max(0.0, min(float(timeout_s), float(api.max_call_s)))
        interval = float(api.progress_interval_s)
        started = self._monotonic()
        next_progress = 0.0
        while True:
            snapshot, finished = self._snapshot(job_ids, batch_id, operation_id, api.page_size_max)
            elapsed = self._monotonic() - started
            if on_progress is not None and not finished and elapsed + _EPSILON >= next_progress and elapsed < limit:
                on_progress(round(elapsed, 3), limit, _progress_message(snapshot))
                next_progress += interval
            if finished or elapsed + _EPSILON >= limit:
                waited = round(min(elapsed, limit), 3)
                return WaitQdto(snapshot, finished, _suggest(snapshot, finished), waited, limit)
            pause = min(self._poll_interval_s, limit - elapsed)
            if on_progress is not None:
                pause = min(pause, max(next_progress - elapsed, 0.0))
            self._sleep(max(pause, 0.0))

    def _snapshot(
        self, job_ids: Sequence[str] | None, batch_id: str | None, operation_id: str | None, max_items: int
    ) -> tuple[WaitSnapshotQdto, bool]:
        if operation_id:
            dao = self._operations.get(operation_id)
            operation: OperationQdto | None = None if dao is None else OperationMapper.to_qdto(dao)
            missing = () if operation is not None else (operation_id,)
            finished = operation is None or operation.state in _FINISHED_OPERATION
            return WaitSnapshotQdto((), (), 0, missing, operation), finished
        if job_ids:
            found = {job_id: self._jobs.get(job_id) for job_id in dict.fromkeys(job_ids)}
            rows = [row for row in found.values() if row is not None]
            missing = tuple(job_id for job_id, row in found.items() if row is None)
        else:
            rows, _ = self._jobs.list(None, batch_id, None, None, BATCH_SCAN_LIMIT, 0)
            missing = ()
        counts = Counter(row.state for row in rows)
        snapshot = WaitSnapshotQdto(
            jobs=tuple(_wait_job(row) for row in rows[:max_items]),
            counts=tuple(StateCountQdto(state, count) for state, count in sorted(counts.items())),
            total_jobs=len(rows),
            missing_job_ids=missing,
            operation=None,
        )
        return snapshot, all(row.state in _SETTLED for row in rows)


def _wait_job(dao: JobDao) -> WaitJobQdto:
    return WaitJobQdto(
        job_id=dao.job_id, state=dao.state, reason=dao.reason, blocked_on=dao.blocked_on,
        preparing_step=dao.preparing_step, platform_task_id=dao.platform_task_id,
        progress_pct=runtime_facts(dao.extra_json).progress_pct, updated_at=dao.updated_at,
    )


def _count(snapshot: WaitSnapshotQdto, *states: JobState) -> int:
    wanted = {state.value for state in states}
    return sum(item.count for item in snapshot.counts if item.state in wanted)


def _progress_message(snapshot: WaitSnapshotQdto) -> str:
    if snapshot.operation is not None:
        return f"operation {snapshot.operation.kind}：{snapshot.operation.state}"
    settled = sum(item.count for item in snapshot.counts if item.state in _SETTLED)
    return f"{settled}/{snapshot.total_jobs} 个作业已结束或待人工处理"


def _suggest(snapshot: WaitSnapshotQdto, finished: bool) -> str:
    if snapshot.operation is not None or (snapshot.missing_job_ids and snapshot.total_jobs == 0 and not snapshot.jobs):
        if snapshot.operation is None:
            return "目标不存在：检查 id 是否正确"
        if finished:
            return "operation 已结束：查看 result 或 error_code"
        return "operation 仍在进行：再次调用 wait（同一 operation_id）"
    paused = [job.job_id for job in snapshot.jobs if job.state == JobState.PAUSED_NEEDS_HUMAN.value]
    if paused:
        return f"有 {len(paused)} 个作业待人工处理（{', '.join(paused[:5])}）：可自动恢复的原因可调用 resume，其余请在 UI 队列看板处理"
    if finished:
        unfinished = _count(snapshot, JobState.FAILED, JobState.CANCELLED)
        if unfinished:
            return f"已全部结束，其中 {unfinished} 个失败或取消：用 list_jobs 查看原因"
        return "全部完成：产物在 renders/ 或 _candidates/，积分与耗时见 GET /api/history"
    if any(job.blocked_on == BlockedOn.QUEUE_PAUSED.value for job in snapshot.jobs):
        return "队列已暂停：在浏览器处理完后，于 UI 点「恢复队列」或调用 resume（queue）"
    return "仍在进行中：再次调用 wait"
