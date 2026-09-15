from __future__ import annotations

from collections.abc import Callable, Mapping

from libs.application.dtos.operation__dto import OperationCdto, OperationRunners
from libs.application.errors.lifecycle__error import InvalidStepOpError, JobNotFoundError, StepNotAllowedError
from libs.application.executors.backend__executor import BackendExecutor
from libs.application.mappers.operation__mapper import OperationMapper
from libs.common.clock import Clock
from libs.common.enums import BackendKind, JobState, OperationKind, PreparingStep
from libs.common.ids import new_id
from libs.domain.entities.generation_job__entity import GenerationJobEntity
from libs.domain.entities.operation__entity import OperationEntity
from libs.domain.errors.job__error import UnconfirmedJobError
from libs.domain.repositories.job__repository import JobRepository
from libs.domain.repositories.operation__repository import OperationRepository

STEP_OPS: tuple[PreparingStep, ...] = (
    PreparingStep.SET_PARAMS, PreparingStep.UPLOAD, PreparingStep.FILL, PreparingStep.PREVIEW,
)
INTERRUPTED_ERROR_CODE: str = "interrupted_by_restart"
_STEPPABLE_STATES: frozenset[JobState] = frozenset({JobState.QUEUED, JobState.PAUSED_NEEDS_HUMAN})
_MESSAGE_LIMIT: int = 500


class OperationCommand:
    """Starts long-running work as background operations and returns at once (spec v2 §4, FR-23, FR-27, F7)."""

    def __init__(
        self,
        operations: OperationRepository,
        executor: BackendExecutor,
        runners: OperationRunners,
        clock: Clock,
        jobs: JobRepository,
    ) -> None:
        self._operations = operations
        self._executor = executor
        self._runners = runners
        self._clock = clock
        self._jobs = jobs

    def start_canary(self, backend: BackendKind) -> OperationCdto:
        return self._start(OperationKind.CANARY, backend, backend.value, lambda: self._runners.canary(backend))

    def start_resume_queue(self, backend: BackendKind) -> OperationCdto:
        return self._start(OperationKind.RESUME_QUEUE, backend, backend.value, lambda: self._runners.resume_queue(backend))

    def start_entity_sync(self) -> OperationCdto:
        return self._start(OperationKind.ENTITY_SYNC, BackendKind.WEB, None, self._runners.entity_sync)

    def start_step(self, job_id: str, op: str) -> OperationCdto:
        step = _step_op(op)
        job = self._job(job_id)
        if job.state not in _STEPPABLE_STATES:
            raise StepNotAllowedError(f"作业处于 {job.state}，分步调试只用于排队中或待人工处理的作业")
        if step not in job.preparing_steps:
            raise StepNotAllowedError(f"{job.backend} 作业没有子步骤 {step}")
        subject = OperationMapper.step_subject(job_id, step.value)
        return self._start(OperationKind.STEP, job.backend, subject, lambda: self._runners.step(job_id, step))

    def start_step_submit(self, job_id: str) -> OperationCdto:
        job = self._job(job_id)
        if not job.confirmed:
            raise UnconfirmedJobError("未经确认的作业不能提交：请先在 UI 确认批次")
        if job.state is not JobState.QUEUED:
            raise StepNotAllowedError(f"作业处于 {job.state}，只有排队中的已确认作业可以分步提交")
        return self._start(OperationKind.STEP_SUBMIT, job.backend, job_id, lambda: self._runners.step_submit(job_id))

    def recover(self) -> int:
        now = self._clock.now()
        interrupted = self._operations.list_unfinished()
        for operation in interrupted:
            operation.fail(INTERRUPTED_ERROR_CODE, "服务重启时该操作尚未结束", now)
            self._operations.save(operation)
        return len(interrupted)

    def _start(
        self, kind: OperationKind, lane: BackendKind, subject: str | None, body: Callable[[], Mapping[str, object]]
    ) -> OperationCdto:
        now = self._clock.now()
        operation = OperationEntity(new_id("op", now), kind, now, subject)
        self._operations.save(operation)
        self._executor.submit(lane, f"op:{operation.operation_id}", lambda: self._run(operation.operation_id, body))
        return OperationMapper.to_cdto(operation)

    def _run(self, operation_id: str, body: Callable[[], Mapping[str, object]]) -> dict[str, object]:
        operation = self._operations.get(operation_id)
        if operation is None:
            return {}
        operation.start(self._clock.now())
        self._operations.save(operation)
        try:
            result = dict(body())
        except Exception as error:  # background boundary: the failure is persisted on the operation, not lost in a thread
            code = getattr(error, "error_code", None)
            message = getattr(error, "message", None) or str(error) or type(error).__name__
            operation.fail(code if isinstance(code, str) else "operation_failed", str(message)[:_MESSAGE_LIMIT], self._clock.now())
            self._operations.save(operation)
            return {}
        operation.succeed(result, self._clock.now())
        self._operations.save(operation)
        return result

    def _job(self, job_id: str) -> GenerationJobEntity:
        job = self._jobs.get(job_id)
        if job is None:
            raise JobNotFoundError(f"作业 {job_id} 不存在")
        return job


def _step_op(op: str) -> PreparingStep:
    for step in STEP_OPS:
        if op == step.value:
            return step
    raise InvalidStepOpError(f"op 必须是 {' | '.join(s.value for s in STEP_OPS)}，收到 {op!r}", hint="提交只能在 UI 里进行")
