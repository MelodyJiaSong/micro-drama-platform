from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

from libs.common.enums import BackendKind, JobState, PauseReason, PauseTier, ResumeAllowance

S = JobState


@dataclass(frozen=True)
class PauseRule:
    reason: PauseReason
    tier: PauseTier
    target_state: JobState | None
    from_states: frozenset[JobState]
    resume: ResumeAllowance
    resume_before_submit: JobState | None = None
    resume_after_submit: JobState | None = None
    backend: BackendKind | None = None

    @property
    def is_failure(self) -> bool:
        return self.target_state is JobState.FAILED

    def resume_target(self, submitted: bool) -> JobState | None:
        return self.resume_after_submit if submitted else self.resume_before_submit

    def applies_to(self, backend: BackendKind) -> bool:
        return self.backend is None or self.backend is backend


def _failed(reason: PauseReason, *from_states: JobState) -> PauseRule:
    return PauseRule(reason, PauseTier.JOB, S.FAILED, frozenset(from_states), ResumeAllowance.NEVER)


def _paused(
    reason: PauseReason,
    from_states: tuple[JobState, ...],
    resume: ResumeAllowance,
    before: JobState | None = None,
    after: JobState | None = None,
    backend: BackendKind | None = None,
) -> PauseRule:
    return PauseRule(
        reason, PauseTier.JOB, S.PAUSED_NEEDS_HUMAN, frozenset(from_states), resume,
        before, after if after is not None else before, backend,
    )


def _queue(reason: PauseReason, backend: BackendKind) -> PauseRule:
    return PauseRule(reason, PauseTier.QUEUE, None, frozenset({S.PREPARING}), ResumeAllowance.API, backend=backend)


R = PauseReason
_API, _UI, _NEVER = ResumeAllowance.API, ResumeAllowance.UI_ONLY, ResumeAllowance.NEVER
_SUBMIT: tuple[JobState, ...] = (S.SUBMITTING,)

PAUSE_RULES: Mapping[PauseReason, PauseRule] = MappingProxyType({
    rule.reason: rule
    for rule in (
        _failed(R.MODERATION_REJECT, S.SUBMITTING, S.GENERATING),
        _failed(R.REAL_FACE_REJECTED, S.PREPARING, S.SUBMITTING, S.GENERATING),
        _failed(R.UPLOAD_REJECTED, S.PREPARING),
        _paused(R.FILL_MISMATCH, (S.PREPARING,), _API, S.QUEUED),
        _paused(R.STEP_FAILED, (S.PREPARING,), _API, S.QUEUED),
        _paused(R.INPUTS_CHANGED, (S.PREPARING,), _NEVER),
        _paused(R.WAIT_TIMEOUT, (S.GENERATING,), _API, S.GENERATING),
        _paused(R.DOWNLOAD_FAILED, (S.DOWNLOADING,), _API, S.DOWNLOADING),
        _paused(R.RESTART_DURING_SUBMIT, _SUBMIT, _UI),
        _paused(R.SUBMIT_REJECTED, _SUBMIT, _UI),
        _paused(R.SUBMIT_UNCONFIRMED, _SUBMIT, _UI),
        _paused(R.ESTIMATE_EXCEEDS_CONFIRMED, (S.PREPARING,), _UI, S.QUEUED),
        _paused(
            R.CLI_ERROR, (S.PREPARING, S.SUBMITTING, S.GENERATING, S.DOWNLOADING), _API, S.QUEUED, S.GENERATING,
            BackendKind.CLI,
        ),
        _queue(R.LOGIN_EXPIRED, BackendKind.WEB),
        _queue(R.CAPTCHA_OR_RISK_POPUP, BackendKind.WEB),
        _queue(R.INSUFFICIENT_CREDIT, BackendKind.WEB),
        _queue(R.PAGE_CONTRACT_BROKEN, BackendKind.WEB),
        _queue(R.BROWSER_LOST, BackendKind.WEB),
        _queue(R.CLI_LOGIN_REQUIRED, BackendKind.CLI),
        _queue(R.COMPLIANCE_CONFIRMATION_REQUIRED, BackendKind.CLI),
    )
})

ADJUDICATED_REASONS: frozenset[PauseReason] = frozenset(
    {R.RESTART_DURING_SUBMIT, R.SUBMIT_REJECTED, R.SUBMIT_UNCONFIRMED}
)


class PauseReasonPolicy:
    @staticmethod
    def rule(reason: PauseReason) -> PauseRule:
        return PAUSE_RULES[reason]

    @staticmethod
    def requires_adjudication(reason: PauseReason, paused_from: JobState | None, has_platform_task_id: bool) -> bool:
        return reason in ADJUDICATED_REASONS or (paused_from is S.SUBMITTING and not has_platform_task_id)

    @staticmethod
    def queue_reasons(backend: BackendKind) -> frozenset[PauseReason]:
        return frozenset(r.reason for r in PAUSE_RULES.values() if r.tier is PauseTier.QUEUE and r.backend is backend)

    @staticmethod
    def job_reasons() -> frozenset[PauseReason]:
        return frozenset(r.reason for r in PAUSE_RULES.values() if r.tier is PauseTier.JOB)
