from __future__ import annotations

from libs.application.dtos.job__dto import CREDITS_NOT_REFUNDED, JobStateCdto, QueueStateCdto
from libs.application.errors.lifecycle__error import InvalidQueueReasonError, JobNotFoundError
from libs.application.executors.backend__executor import JOB_MUTATION_LOCK
from libs.common.clock import Clock, iso
from libs.common.enums import Adjudication, BackendKind, JobState, PauseReason, PauseTier, QueueState, ResumeVia
from libs.domain.entities.generation_job__entity import GenerationJobEntity
from libs.domain.repositories.job__repository import JobRepository
from libs.domain.value_objects.pause_reason__valueobject import PauseReasonPolicy
from libs.infrastructure.daos.store_record__dao import QueueStateDao
from libs.infrastructure.readers.store_record__reader import QueueStateReader
from libs.infrastructure.writers.store_record__writer import QueueStateWriter

MANUAL_PAUSE_REASON: str = "manual"


class JobCommand:
    """Human / client actions on one job or one backend queue (FR-19, FR-21..FR-23).

    Domain errors pass through unchanged so routes can map them: `UiOnlyActionError` / `AdjudicationRequiredError`
    → 403, `IllegalJobTransitionError` / `ResumeNotAllowedError` → 409, `EstimateApprovalMismatchError` → 422.
    """

    def __init__(self, jobs: JobRepository, queue_states: tuple[QueueStateReader, QueueStateWriter], clock: Clock) -> None:
        self._jobs = jobs
        self._queue_reader, self._queue_writer = queue_states
        self._clock = clock

    def cancel(self, job_id: str) -> JobStateCdto:
        with JOB_MUTATION_LOCK:
            job = self._load(job_id)
            job.cancel(self._clock.now())
            self._jobs.save(job)
        return _state(job, _cancel_message(job))

    def resume(self, job_id: str, via: ResumeVia) -> JobStateCdto:
        with JOB_MUTATION_LOCK:
            job = self._load(job_id)
            job.resume(via, self._clock.now())
            self._jobs.save(job)
        return _state(job, None)

    def adjudicate(self, job_id: str, choice: Adjudication, platform_task_id: str | None) -> JobStateCdto:
        with JOB_MUTATION_LOCK:
            job = self._load(job_id)
            job.adjudicate(choice, ResumeVia.UI, self._clock.now(), platform_task_id)
            self._jobs.save(job)
        return _state(job, _cancel_message(job) if job.state is JobState.CANCELLED else None)

    def approve_estimate(self, job_id: str, approved_credits: int) -> JobStateCdto:
        with JOB_MUTATION_LOCK:
            job = self._load(job_id)
            job.approve_estimate(approved_credits, ResumeVia.UI, self._clock.now())
            self._jobs.save(job)
        return _state(job, f"已批准按 {approved_credits} 积分提交；再次准备时超出此数（含容差）会重新暂停")

    def pause_queue(self, backend: BackendKind, reason: PauseReason | None) -> QueueStateCdto:
        if reason is not None:
            rule = PauseReasonPolicy.rule(reason)
            if rule.tier is not PauseTier.QUEUE or not rule.applies_to(backend):
                raise InvalidQueueReasonError(f"{reason} 不是 {backend} 队列的暂停原因")
        return self._set(backend, QueueState.PAUSED, MANUAL_PAUSE_REASON if reason is None else reason.value)

    def mark_queue_running(self, backend: BackendKind) -> QueueStateCdto:
        return self._set(backend, QueueState.RUNNING, None)

    def _set(self, backend: BackendKind, state: QueueState, reason: str | None) -> QueueStateCdto:
        record = QueueStateDao(backend.value, state.value, reason, iso(self._clock.now()))
        self._queue_writer.set(record)
        return QueueStateCdto(record.backend, record.state, record.reason, record.updated_at)

    def _load(self, job_id: str) -> GenerationJobEntity:
        job = self._jobs.get(job_id)
        if job is None:
            raise JobNotFoundError(f"作业 {job_id} 不存在")
        return job


def _state(job: GenerationJobEntity, message: str | None) -> JobStateCdto:
    reason = job.pause_reason or job.failure_reason
    return JobStateCdto(
        job_id=job.job_id,
        state=job.state.value,
        reason=None if reason is None else reason.value,
        attempt=job.attempt,
        cancel_requested=job.cancel_requested,
        credits_spent=job.credits_spent,
        platform_task_id=job.platform_task_id,
        message=message,
    )


def _cancel_message(job: GenerationJobEntity) -> str:
    if job.state is JobState.SUBMITTING:
        return f"已记录取消请求：等本次点击的结果；如果已经提交，{CREDITS_NOT_REFUNDED}"
    if job.credits_spent:
        return f"已取消；该作业已经提交，{CREDITS_NOT_REFUNDED}"
    return "已取消，未花费积分"
