import pytest

from libs.common.enums import BackendKind, JobState, PauseReason, PauseTier, ResumeAllowance
from libs.domain.value_objects.pause_reason__valueobject import ADJUDICATED_REASONS, PAUSE_RULES, PauseReasonPolicy, PauseRule

R, S = PauseReason, JobState

QUEUE_WEB = {R.LOGIN_EXPIRED, R.CAPTCHA_OR_RISK_POPUP, R.INSUFFICIENT_CREDIT, R.PAGE_CONTRACT_BROKEN, R.BROWSER_LOST}
QUEUE_CLI = {R.CLI_LOGIN_REQUIRED, R.COMPLIANCE_CONFIRMATION_REQUIRED}

FR17_TABLE: list[tuple[PauseReason, JobState, ResumeAllowance, JobState | None, JobState | None, BackendKind | None]] = [
    (R.MODERATION_REJECT, S.FAILED, ResumeAllowance.NEVER, None, None, None),
    (R.REAL_FACE_REJECTED, S.FAILED, ResumeAllowance.NEVER, None, None, None),
    (R.UPLOAD_REJECTED, S.FAILED, ResumeAllowance.NEVER, None, None, None),
    (R.FILL_MISMATCH, S.PAUSED_NEEDS_HUMAN, ResumeAllowance.API, S.QUEUED, S.QUEUED, None),
    (R.STEP_FAILED, S.PAUSED_NEEDS_HUMAN, ResumeAllowance.API, S.QUEUED, S.QUEUED, None),
    (R.INPUTS_CHANGED, S.PAUSED_NEEDS_HUMAN, ResumeAllowance.NEVER, None, None, None),
    (R.WAIT_TIMEOUT, S.PAUSED_NEEDS_HUMAN, ResumeAllowance.API, S.GENERATING, S.GENERATING, None),
    (R.DOWNLOAD_FAILED, S.PAUSED_NEEDS_HUMAN, ResumeAllowance.API, S.DOWNLOADING, S.DOWNLOADING, None),
    (R.RESTART_DURING_SUBMIT, S.PAUSED_NEEDS_HUMAN, ResumeAllowance.UI_ONLY, None, None, None),
    (R.SUBMIT_REJECTED, S.PAUSED_NEEDS_HUMAN, ResumeAllowance.UI_ONLY, None, None, None),
    (R.SUBMIT_UNCONFIRMED, S.PAUSED_NEEDS_HUMAN, ResumeAllowance.UI_ONLY, None, None, None),
    (R.ESTIMATE_EXCEEDS_CONFIRMED, S.PAUSED_NEEDS_HUMAN, ResumeAllowance.UI_ONLY, S.QUEUED, S.QUEUED, None),
    (R.CLI_ERROR, S.PAUSED_NEEDS_HUMAN, ResumeAllowance.API, S.QUEUED, S.GENERATING, BackendKind.CLI),
]


def test_every_reason_classified_exactly_once() -> None:
    assert set(PAUSE_RULES) == set(PauseReason)
    assert all(rule.reason is reason for reason, rule in PAUSE_RULES.items())


@pytest.mark.parametrize(("reason", "target", "resume", "before", "after", "backend"), FR17_TABLE)
def test_job_tier_table(
    reason: PauseReason, target: JobState, resume: ResumeAllowance, before: JobState | None, after: JobState | None,
    backend: BackendKind | None,
) -> None:
    rule = PauseReasonPolicy.rule(reason)
    assert rule.tier is PauseTier.JOB and rule.backend is backend
    assert rule.target_state is target and rule.resume is resume
    assert rule.resume_target(submitted=False) is before and rule.resume_target(submitted=True) is after
    assert rule.from_states


@pytest.mark.parametrize("reason", sorted(QUEUE_WEB | QUEUE_CLI))
def test_queue_tier(reason: PauseReason) -> None:
    rule = PauseReasonPolicy.rule(reason)
    assert rule.tier is PauseTier.QUEUE and rule.target_state is None
    assert rule.backend is (BackendKind.WEB if reason in QUEUE_WEB else BackendKind.CLI)


def test_queue_reasons_by_backend() -> None:
    assert PauseReasonPolicy.queue_reasons(BackendKind.WEB) == QUEUE_WEB
    assert PauseReasonPolicy.queue_reasons(BackendKind.CLI) == QUEUE_CLI
    assert PauseReasonPolicy.job_reasons() == {row[0] for row in FR17_TABLE}


def test_cli_error_applies_only_to_cli() -> None:
    rule = PauseReasonPolicy.rule(R.CLI_ERROR)
    assert rule.applies_to(BackendKind.CLI) and not rule.applies_to(BackendKind.WEB)
    assert PauseReasonPolicy.rule(R.FILL_MISMATCH).applies_to(BackendKind.WEB)


ADJUDICATION: list[tuple[PauseReason, JobState, bool, bool]] = [
    (R.RESTART_DURING_SUBMIT, S.SUBMITTING, False, True),
    (R.SUBMIT_REJECTED, S.SUBMITTING, False, True),
    (R.SUBMIT_UNCONFIRMED, S.SUBMITTING, False, True),
    (R.CLI_ERROR, S.SUBMITTING, False, True),
    (R.CLI_ERROR, S.SUBMITTING, True, False),
    (R.CLI_ERROR, S.PREPARING, False, False),
    (R.CLI_ERROR, S.GENERATING, True, False),
    (R.CLI_ERROR, S.DOWNLOADING, True, False),
    (R.FILL_MISMATCH, S.PREPARING, False, False),
    (R.WAIT_TIMEOUT, S.GENERATING, True, False),
]


@pytest.mark.parametrize(("reason", "paused_from", "has_task_id", "expected"), ADJUDICATION)
def test_requires_adjudication(reason: PauseReason, paused_from: JobState, has_task_id: bool, expected: bool) -> None:
    assert PauseReasonPolicy.requires_adjudication(reason, paused_from, has_task_id) is expected


def test_adjudicated_reasons_are_ui_only() -> None:
    assert ADJUDICATED_REASONS == {R.RESTART_DURING_SUBMIT, R.SUBMIT_REJECTED, R.SUBMIT_UNCONFIRMED}
    assert all(PauseReasonPolicy.rule(r).resume is ResumeAllowance.UI_ONLY for r in ADJUDICATED_REASONS)


def test_policy_table_is_immutable() -> None:
    with pytest.raises(TypeError):
        PAUSE_RULES[R.INPUTS_CHANGED] = PAUSE_RULES[R.FILL_MISMATCH]  # type: ignore[index]
    with pytest.raises(AttributeError):
        PAUSE_RULES[R.CLI_ERROR].resume = ResumeAllowance.API  # type: ignore[misc]
    assert isinstance(PAUSE_RULES[R.CLI_ERROR], PauseRule)
