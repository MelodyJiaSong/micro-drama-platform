from collections.abc import Sequence
from dataclasses import replace
from datetime import datetime

from libs.common.enums import (
    TERMINAL_JOB_STATES, Adjudication, BackendKind, BlockedOn, GenerationKind, JobState, PauseReason, PauseTier,
    PreparingStep, ResumeAllowance, ResumeVia,
)
from libs.domain.errors.job__error import (
    AdjudicationRequiredError, ConfirmationMismatchError, EstimateApprovalMismatchError, EstimateNotApprovedError,
    EstimateNotRecordedError, IllegalJobTransitionError, InvalidJobReasonError, JobAlreadyTerminalError,
    JobInvariantError, MissingPlatformTaskIdError, ResumeNotAllowedError, StepOrderError, UiOnlyActionError,
    UnconfirmedJobError,
)
from libs.domain.value_objects.batch_confirmation__valueobject import BatchConfirmation
from libs.domain.value_objects.batch_item__valueobject import BatchItem
from libs.domain.value_objects.fingerprint__valueobject import Fingerprint
from libs.domain.value_objects.frozen_request__valueobject import FrozenRequest
from libs.domain.value_objects.generation_request__valueobject import GenerationRequest
from libs.domain.value_objects.job_snapshot__valueobject import JobSnapshot, TransitionRecord, binding_mismatch, item_mismatch
from libs.domain.value_objects.pause_reason__valueobject import PauseReasonPolicy, PauseRule

__all__ = ["GenerationJobEntity", "TransitionRecord"]

S = JobState
R = PauseReason


class GenerationJobEntity:
    def __init__(
        self,
        job_id: str,
        batch_id: str,
        backend: BackendKind,
        request: GenerationRequest,
        fingerprint: Fingerprint,
        *,
        attempt: int = 1,
        state: JobState = S.QUEUED,
        blocked_on: BlockedOn = BlockedOn.NONE,
        current_step: PreparingStep | None = None,
        pause_reason: PauseReason | None = None,
        paused_from: JobState | None = None,
        failure_reason: PauseReason | None = None,
        confirmation: BatchConfirmation | None = None,
        frozen_request: FrozenRequest | None = None,
        platform_task_id: str | None = None,
        cancel_requested: bool = False,
        credits_spent: bool = False,
        page_estimated_credits: int | None = None,
        approved_credits: int | None = None,
        transitions: Sequence[TransitionRecord] = (),
    ) -> None:
        self._s: JobSnapshot = _validated(JobSnapshot(
            job_id, batch_id, backend, request, fingerprint, attempt=attempt, state=state, blocked_on=blocked_on,
            current_step=current_step, pause_reason=pause_reason, paused_from=paused_from,
            failure_reason=failure_reason, confirmation=confirmation, frozen_request=frozen_request,
            platform_task_id=platform_task_id, cancel_requested=cancel_requested, credits_spent=credits_spent,
            page_estimated_credits=page_estimated_credits, approved_credits=approved_credits,
            transitions=tuple(transitions),
        ))

    @classmethod
    def from_snapshot(cls, snapshot: JobSnapshot) -> "GenerationJobEntity":
        job: GenerationJobEntity = object.__new__(cls)
        job._s = _validated(snapshot)
        return job

    def snapshot(self) -> JobSnapshot:
        return self._s

    @property
    def job_id(self) -> str:
        return self._s.job_id

    @property
    def batch_id(self) -> str:
        return self._s.batch_id

    @property
    def backend(self) -> BackendKind:
        return self._s.backend

    @property
    def request(self) -> GenerationRequest:
        return self._s.request

    @property
    def fingerprint(self) -> Fingerprint:
        return self._s.fingerprint

    @property
    def attempt(self) -> int:
        return self._s.attempt

    @property
    def state(self) -> JobState:
        return self._s.state

    @property
    def blocked_on(self) -> BlockedOn:
        return self._s.blocked_on

    @property
    def current_step(self) -> PreparingStep | None:
        return self._s.current_step

    @property
    def pause_reason(self) -> PauseReason | None:
        return self._s.pause_reason

    @property
    def paused_from(self) -> JobState | None:
        return self._s.paused_from

    @property
    def failure_reason(self) -> PauseReason | None:
        return self._s.failure_reason

    @property
    def confirmation(self) -> BatchConfirmation | None:
        return self._s.confirmation

    @property
    def frozen_request(self) -> FrozenRequest | None:
        return self._s.frozen_request

    @property
    def platform_task_id(self) -> str | None:
        return self._s.platform_task_id

    @property
    def cancel_requested(self) -> bool:
        return self._s.cancel_requested

    @property
    def credits_spent(self) -> bool:
        return self._s.credits_spent

    @property
    def page_estimated_credits(self) -> int | None:
        return self._s.page_estimated_credits

    @property
    def approved_credits(self) -> int | None:
        return self._s.approved_credits

    @property
    def transitions(self) -> tuple[TransitionRecord, ...]:
        return self._s.transitions

    @property
    def confirmed(self) -> bool:
        return self._s.confirmed

    @property
    def submitted(self) -> bool:
        return self._s.submitted

    @property
    def is_terminal(self) -> bool:
        return self._s.state in TERMINAL_JOB_STATES

    @property
    def estimate_approved(self) -> bool:
        return self._s.approved_credits is not None

    @property
    def preparing_steps(self) -> tuple[PreparingStep, ...]:
        return self._s.preparing_steps

    @property
    def requires_adjudication(self) -> bool:
        s = self._s
        return (
            s.state is S.PAUSED_NEEDS_HUMAN
            and s.pause_reason is not None
            and PauseReasonPolicy.requires_adjudication(s.pause_reason, s.paused_from, s.submitted)
        )

    def confirm(self, confirmation: BatchConfirmation, frozen: FrozenRequest, item: BatchItem) -> None:
        s = self._require(S.QUEUED, command="confirm")
        if s.confirmation is not None:
            raise ConfirmationMismatchError("作业已经确认过")
        mismatch: str | None = binding_mismatch(s, confirmation, frozen) or item_mismatch(s, frozen, item)
        if mismatch is not None:
            raise ConfirmationMismatchError(mismatch)
        self._commit(replace(s, confirmation=confirmation, frozen_request=frozen))

    def set_blocked_on(self, blocked_on: BlockedOn) -> None:
        self._commit(replace(self._require(S.QUEUED, command="set_blocked_on"), blocked_on=blocked_on))

    def start_preparing(self, at: datetime) -> None:
        s = self._require(S.QUEUED, command="start_preparing")
        self._require_confirmed()
        fresh = replace(s, blocked_on=BlockedOn.NONE, current_step=s.preparing_steps[0], page_estimated_credits=None)
        self._move(fresh, S.PREPARING, at, None)

    def advance_step(self, step: PreparingStep) -> None:
        s = self._require(S.PREPARING, command="advance_step")
        steps: tuple[PreparingStep, ...] = s.preparing_steps
        current: int = steps.index(s.current_step) if s.current_step in steps else -1
        if step not in steps or steps.index(step) != current + 1:
            raise StepOrderError(f"{s.backend} 作业当前子步骤 {s.current_step}，不能跳到 {step}")
        self._commit(replace(s, current_step=step))

    def record_page_estimate(self, credits: int, pause_if_unestimated: bool, at: datetime) -> bool:
        s = self._require(S.PREPARING, command="record_page_estimate")
        if credits < 0:
            raise JobInvariantError("页面预计积分不能为负")
        self._commit(replace(s, page_estimated_credits=credits))
        over: bool | None = self._s.exceeds_estimate_baseline(credits)
        exceeds: bool = pause_if_unestimated if over is None else over
        if exceeds:
            self.pause(R.ESTIMATE_EXCEEDS_CONFIRMED, at)
        return exceeds

    def mark_submitting(self, at: datetime) -> None:
        s = self._require(S.PREPARING, command="mark_submitting")
        self._require_confirmed()
        if s.current_step is not s.preparing_steps[-1]:
            raise StepOrderError(f"{s.preparing_steps[-1]} 之前不能进入 submitting")
        if s.backend is BackendKind.WEB and s.request.kind is not GenerationKind.ENTITY:
            if s.page_estimated_credits is None:
                raise EstimateNotRecordedError("本次准备还没有读取页面预计积分，不能提交")
            if s.exceeds_estimate_baseline(s.page_estimated_credits) is True:
                raise EstimateNotApprovedError(
                    f"页面预计积分 {s.page_estimated_credits} 超出已确认额度且未经 UI 批准，不能提交"
                )
        self._move(replace(s, current_step=None), S.SUBMITTING, at, None)

    def mark_generating(self, platform_task_id: str, at: datetime) -> None:
        s = self._require(S.SUBMITTING, command="mark_generating")
        if not platform_task_id:
            raise MissingPlatformTaskIdError("进入 generating 必须带平台任务标识")
        linked = replace(s, platform_task_id=platform_task_id)
        if s.cancel_requested:
            self._finish_cancel(linked, True, at, "cancel_requested")
            return
        self._move(linked, S.GENERATING, at, None)

    def abort_submit(self, at: datetime) -> None:
        s = self._require(S.SUBMITTING, command="abort_submit")
        if not s.cancel_requested:
            raise IllegalJobTransitionError(s.state, "abort_submit（未请求取消）")
        self._finish_cancel(s, False, at, "cancel_requested")

    def mark_downloading(self, at: datetime) -> None:
        self._move(self._require(S.GENERATING, command="mark_downloading"), S.DOWNLOADING, at, None)

    def mark_done(self, at: datetime) -> None:
        self._move(self._require(S.DOWNLOADING, command="mark_done"), S.DONE, at, None)

    def pause(self, reason: PauseReason, at: datetime) -> None:
        rule: PauseRule = PauseReasonPolicy.rule(reason)
        if rule.tier is not PauseTier.JOB or rule.target_state is not S.PAUSED_NEEDS_HUMAN:
            raise InvalidJobReasonError(reason, f"{reason} 不会让作业进入待人工处理")
        if not rule.applies_to(self._s.backend):
            raise InvalidJobReasonError(reason, f"{reason} 只适用于 {rule.backend} 作业")
        s = self._require(*rule.from_states, command=f"pause({reason})")
        if reason is R.ESTIMATE_EXCEEDS_CONFIRMED and s.page_estimated_credits is None:
            raise InvalidJobReasonError(reason, "暂停前必须先记录页面预计积分")
        if reason is R.SUBMIT_REJECTED and s.cancel_requested:
            self._finish_cancel(s, False, at, "cancel_requested")
            return
        approved: int | None = s.approved_credits if reason is R.ESTIMATE_EXCEEDS_CONFIRMED else None
        paused = replace(
            s, paused_from=s.state, pause_reason=reason, current_step=None, blocked_on=BlockedOn.NONE,
            approved_credits=approved,
        )
        self._move(paused, S.PAUSED_NEEDS_HUMAN, at, reason.value)

    def fail(self, reason: PauseReason, at: datetime) -> None:
        rule: PauseRule = PauseReasonPolicy.rule(reason)
        if not rule.is_failure:
            raise InvalidJobReasonError(reason, f"{reason} 不是作业失败原因")
        s = self._require(*rule.from_states, command=f"fail({reason})")
        failed = replace(s, failure_reason=reason, credits_spent=s.submitted, current_step=None)
        self._move(failed, S.FAILED, at, reason.value)

    def yield_to_queue_pause(self, reason: PauseReason, at: datetime) -> bool:
        rule: PauseRule = PauseReasonPolicy.rule(reason)
        if rule.tier is not PauseTier.QUEUE:
            raise InvalidJobReasonError(reason, f"{reason} 不是队列级暂停原因")
        if not rule.applies_to(self._s.backend):
            return False
        s = self._require(S.PREPARING, command=f"yield_to_queue_pause({reason})")
        self._move(replace(s, current_step=None, blocked_on=BlockedOn.QUEUE_PAUSED), S.QUEUED, at, reason.value)
        return True

    def cancel(self, at: datetime) -> None:
        s = self._s
        if s.state in TERMINAL_JOB_STATES:
            raise JobAlreadyTerminalError(s.state, "cancel")
        if s.state is S.SUBMITTING:
            self._commit(replace(s, cancel_requested=True))
            return
        if s.state is S.PAUSED_NEEDS_HUMAN:
            if self.requires_adjudication:
                raise AdjudicationRequiredError(f"{s.pause_reason} 提交结果不明，只能在 UI 裁决（含取消）")
            spent: bool = s.submitted
        else:
            spent = s.state in (S.GENERATING, S.DOWNLOADING)
        self._finish_cancel(s, spent, at, "cancelled")

    def resume(self, via: ResumeVia, at: datetime) -> None:
        s = self._require(S.PAUSED_NEEDS_HUMAN, command="resume")
        rule: PauseRule = PauseReasonPolicy.rule(_reason(s))
        if rule.resume is ResumeAllowance.NEVER:
            raise ResumeNotAllowedError(f"{rule.reason} 不能恢复，只能重新预检")
        if rule.resume is ResumeAllowance.UI_ONLY or self.requires_adjudication:
            raise AdjudicationRequiredError(f"{rule.reason} 只能在 UI 裁决或批准")
        target: JobState | None = rule.resume_target(s.submitted)
        if target is None:
            raise ResumeNotAllowedError(f"{rule.reason} 没有恢复目标")
        self._move(_cleared(s), target, at, f"resumed_via_{via.value}")

    def adjudicate(self, choice: Adjudication, via: ResumeVia, at: datetime, platform_task_id: str | None = None) -> None:
        s = self._require(S.PAUSED_NEEDS_HUMAN, command="adjudicate")
        reason: PauseReason = _reason(s)
        if not self.requires_adjudication:
            raise InvalidJobReasonError(reason, f"{reason} 不需要裁决")
        if via is not ResumeVia.UI:
            raise UiOnlyActionError("提交结果不明的作业只能在 UI 裁决")
        label: str = f"adjudicated:{choice.value}"
        if choice is Adjudication.LINK_EXISTING:
            if not platform_task_id:
                raise MissingPlatformTaskIdError("「这就是它」必须指定平台任务标识")
            linked = replace(s, platform_task_id=platform_task_id)
            if s.cancel_requested:
                self._finish_cancel(linked, True, at, label)
            else:
                self._move(_cleared(linked), S.GENERATING, at, label)
        elif choice is Adjudication.CONFIRM_NOT_SUBMITTED:
            if s.cancel_requested:
                self._finish_cancel(s, False, at, label)
            else:
                retry = replace(_cleared(s), attempt=s.attempt + 1, page_estimated_credits=None, approved_credits=None)
                self._move(retry, S.QUEUED, at, label)
        else:
            self._finish_cancel(s, reason is not R.SUBMIT_REJECTED, at, label)

    def approve_estimate(self, approved_credits: int, via: ResumeVia, at: datetime) -> None:
        s = self._require(S.PAUSED_NEEDS_HUMAN, command="approve_estimate")
        reason: PauseReason = _reason(s)
        if reason is not R.ESTIMATE_EXCEEDS_CONFIRMED:
            raise InvalidJobReasonError(reason, f"{reason} 不是积分超出待批准")
        if via is not ResumeVia.UI:
            raise UiOnlyActionError("积分超出只能在 UI 批准")
        if approved_credits != s.page_estimated_credits:
            raise EstimateApprovalMismatchError(
                f"批准额 {approved_credits} 与作业记录的页面预计积分 {s.page_estimated_credits} 不一致"
            )
        self._move(replace(_cleared(s), approved_credits=approved_credits), S.QUEUED, at, "estimate_approved")

    def recover_after_restart(self, at: datetime) -> bool:
        s = self._s
        if s.state is S.SUBMITTING:
            self.pause(R.RESTART_DURING_SUBMIT, at)
            return True
        if s.state is S.PREPARING:
            self._move(replace(s, current_step=None), S.QUEUED, at, "restart_during_prepare")
            return True
        return False

    def _require(self, *states: JobState, command: str) -> JobSnapshot:
        s = self._s
        if s.state not in states:
            if s.state in TERMINAL_JOB_STATES:
                raise JobAlreadyTerminalError(s.state, command)
            raise IllegalJobTransitionError(s.state, command)
        return s

    def _require_confirmed(self) -> None:
        if not self._s.confirmed:
            raise UnconfirmedJobError("未经确认的作业不能进入 preparing / submitting")

    def _finish_cancel(self, snapshot: JobSnapshot, credits_spent: bool, at: datetime, reason: str) -> None:
        cancelled = replace(_cleared(snapshot), credits_spent=credits_spent, current_step=None)
        self._move(cancelled, S.CANCELLED, at, reason)

    def _move(self, snapshot: JobSnapshot, to_state: JobState, at: datetime, reason: str | None) -> None:
        record = TransitionRecord(self._s.state, to_state, at, reason)
        self._commit(replace(snapshot, state=to_state, transitions=self._s.transitions + (record,)))

    def _commit(self, snapshot: JobSnapshot) -> None:
        self._s = _validated(snapshot)


def _validated(snapshot: JobSnapshot) -> JobSnapshot:
    problem: str | None = snapshot.problem()
    if problem is not None:
        raise JobInvariantError(problem)
    return snapshot


def _cleared(snapshot: JobSnapshot) -> JobSnapshot:
    return replace(snapshot, pause_reason=None, paused_from=None, blocked_on=BlockedOn.NONE)


def _reason(snapshot: JobSnapshot) -> PauseReason:
    if snapshot.pause_reason is None:
        raise JobInvariantError("待人工处理的作业缺少原因")
    return snapshot.pause_reason
