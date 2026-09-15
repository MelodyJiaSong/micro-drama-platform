from dataclasses import dataclass
from datetime import datetime

from libs.common.enums import (
    PREPARING_STEPS_BY_BACKEND, BackendKind, BlockedOn, Confirmer, JobState, PauseReason, PauseTier, PreparingStep,
)
from libs.domain.value_objects.batch_confirmation__valueobject import BatchConfirmation
from libs.domain.value_objects.batch_item__valueobject import BatchItem
from libs.domain.value_objects.fingerprint__valueobject import Fingerprint
from libs.domain.value_objects.frozen_request__valueobject import FrozenRequest
from libs.domain.value_objects.generation_request__valueobject import GenerationRequest
from libs.domain.value_objects.pause_reason__valueobject import PauseReasonPolicy, PauseRule

S, R = JobState, PauseReason
NEEDS_CONFIRMATION: frozenset[JobState] = frozenset(
    {S.PREPARING, S.SUBMITTING, S.GENERATING, S.DOWNLOADING, S.DONE, S.PAUSED_NEEDS_HUMAN, S.FAILED}
)
NEEDS_TASK_ID: frozenset[JobState] = frozenset({S.GENERATING, S.DOWNLOADING, S.DONE})
CANCEL_INTENT_STATES: frozenset[JobState] = frozenset({S.SUBMITTING, S.PAUSED_NEEDS_HUMAN, S.CANCELLED, S.FAILED})


@dataclass(frozen=True)
class TransitionRecord:
    from_state: JobState
    to_state: JobState
    at: datetime
    reason: str | None


@dataclass(frozen=True)
class JobSnapshot:
    job_id: str
    batch_id: str
    backend: BackendKind
    request: GenerationRequest
    fingerprint: Fingerprint
    attempt: int = 1
    state: JobState = S.QUEUED
    blocked_on: BlockedOn = BlockedOn.NONE
    current_step: PreparingStep | None = None
    pause_reason: PauseReason | None = None
    paused_from: JobState | None = None
    failure_reason: PauseReason | None = None
    confirmation: BatchConfirmation | None = None
    frozen_request: FrozenRequest | None = None
    platform_task_id: str | None = None
    cancel_requested: bool = False
    credits_spent: bool = False
    page_estimated_credits: int | None = None
    approved_credits: int | None = None
    transitions: tuple[TransitionRecord, ...] = ()

    @property
    def confirmed(self) -> bool:
        return self.confirmation is not None and self.frozen_request is not None

    @property
    def submitted(self) -> bool:
        return self.platform_task_id is not None

    @property
    def preparing_steps(self) -> tuple[PreparingStep, ...]:
        return PREPARING_STEPS_BY_BACKEND[self.backend]

    def exceeds_estimate_baseline(self, credits: int) -> bool | None:
        if self.frozen_request is None:
            return None
        baseline: int | None = (
            self.approved_credits if self.approved_credits is not None else self.frozen_request.credits_estimated
        )
        if baseline is None:
            return None
        return credits * 100 > baseline * (100 + self.frozen_request.estimate_tolerance_pct)

    def problem(self) -> str | None:
        state: JobState = self.state
        if self.attempt < 1:
            return "attempt 必须 ≥ 1"
        if self.fingerprint != Fingerprint.of(self.request):
            return "fingerprint 与请求内容不一致"
        if (self.confirmation is None) != (self.frozen_request is None):
            return "确认凭据与冻结请求必须同时存在"
        if self.confirmation is not None and self.frozen_request is not None:
            mismatch: str | None = binding_mismatch(self, self.confirmation, self.frozen_request)
            if mismatch is not None:
                return mismatch
        if state in NEEDS_CONFIRMATION and not self.confirmed:
            return f"{state} 的作业必须已确认并带冻结请求"
        pause_problem: str | None = self._pause_problem()
        if pause_problem is not None:
            return pause_problem
        if (state is S.FAILED) != (self.failure_reason is not None):
            return "failed 与 failure_reason 必须同时存在"
        if (state in NEEDS_TASK_ID or self.paused_from in (S.GENERATING, S.DOWNLOADING)) and not self.platform_task_id:
            return f"{state} 的作业必须带平台任务标识"
        if (self.current_step is not None) != (state is S.PREPARING):
            return "只有 preparing 的作业带子步骤"
        if self.current_step is not None and self.current_step not in self.preparing_steps:
            return f"{self.backend} 作业没有子步骤 {self.current_step}"
        if self.blocked_on is not BlockedOn.NONE and state is not S.QUEUED:
            return "只有 queued 的作业带 blocked_on"
        if self.cancel_requested and state not in CANCEL_INTENT_STATES:
            return f"{state} 的作业不能带 cancel_requested"
        if any(value is not None and value < 0 for value in (self.page_estimated_credits, self.approved_credits)):
            return "预计积分与批准额不能为负"
        return None

    def _pause_problem(self) -> str | None:
        if (self.state is S.PAUSED_NEEDS_HUMAN) != (self.pause_reason is not None):
            return "paused_needs_human 与 pause_reason 必须同时存在"
        if self.pause_reason is None:
            return None if self.paused_from is None else "非暂停作业不能带 paused_from"
        rule: PauseRule = PauseReasonPolicy.rule(self.pause_reason)
        if rule.tier is not PauseTier.JOB or rule.target_state is not S.PAUSED_NEEDS_HUMAN:
            return f"{self.pause_reason} 不是作业级暂停原因"
        if self.paused_from not in rule.from_states or not rule.applies_to(self.backend):
            return f"{self.pause_reason} 不能从 {self.paused_from} / {self.backend} 进入"
        if self.pause_reason is R.ESTIMATE_EXCEEDS_CONFIRMED and self.page_estimated_credits is None:
            return "积分超出暂停必须带页面预计积分"
        return None


def binding_mismatch(snapshot: JobSnapshot, confirmation: BatchConfirmation, frozen: FrozenRequest) -> str | None:
    if confirmation.batch_id != snapshot.batch_id:
        return "确认凭据不属于本作业的批次"
    if confirmation.confirmer is not Confirmer.UI_HUMAN:
        return "只有 UI 里的人可以确认"
    if frozen.request.kind is not snapshot.request.kind:
        return "冻结请求的类型与作业不一致"
    if frozen.backend is not snapshot.backend:
        return "冻结请求的通道与作业不一致"
    if frozen.fingerprint != snapshot.fingerprint or Fingerprint.of(frozen.request) != snapshot.fingerprint:
        return "冻结请求与预检时的内容不一致"
    return None


def item_mismatch(snapshot: JobSnapshot, frozen: FrozenRequest, item: BatchItem) -> str | None:
    if item.fingerprint != snapshot.fingerprint:
        return "已确认的批次条目与作业内容不一致"
    if item.precheck.has_errors:
        return "含 error 的批次条目不能确认"
    if item.precheck.existing_job_id is not None:
        return f"该条目命中已有作业 {item.precheck.existing_job_id}，应返回已有作业而不是确认新作业"
    if frozen.credits_estimated != item.precheck.estimate.credits:
        return f"冻结请求的预计积分 {frozen.credits_estimated} 与已确认条目的 {item.precheck.estimate.credits} 不一致"
    return None
