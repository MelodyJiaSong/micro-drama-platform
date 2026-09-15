from collections.abc import Callable
from dataclasses import replace
from typing import Any

import pytest

from libs.common.enums import (
    Adjudication, BackendKind, BlockedOn, CheckSeverity, JobState, PauseReason, PrecheckCheck, PreparingStep, ResumeVia,
)
from libs.domain.entities.generation_job__entity import GenerationJobEntity
from libs.domain.errors.job__error import (
    AdjudicationRequiredError, ConfirmationMismatchError, EstimateApprovalMismatchError, EstimateNotApprovedError,
    EstimateNotRecordedError, InvalidJobReasonError, JobAlreadyTerminalError, JobError, JobInvariantError,
    MissingPlatformTaskIdError, ResumeNotAllowedError, StepOrderError, UiOnlyActionError, UnconfirmedJobError,
)
from libs.domain.value_objects.batch_item__valueobject import BatchItem
from libs.domain.value_objects.fingerprint__valueobject import Fingerprint
from libs.domain.value_objects.frozen_request__valueobject import FrozenRequest
from libs.domain.value_objects.generation_request__valueobject import GenerationRequest
from libs.domain.value_objects.precheck_result__valueobject import PrecheckItem, PrecheckResult
from libs.domain.value_objects.price_estimate__valueobject import PriceEstimate
from tests.libs.domain.builders import (
    PAGE_OVER_ESTIMATE, STATIC_CREDITS, T0, TOLERANCE_PCT, confirmed_item, entity_create_request, image_request,
    job_in, new_job, prepared_to_last_step, proof, rehydrate, video_request,
)

S, R = JobState, PauseReason
P, WEB, CLI = S.PAUSED_NEEDS_HUMAN, BackendKind.WEB, BackendKind.CLI

ROWS: dict[str, Callable[[], GenerationJobEntity]] = {
    "queued": lambda: job_in(S.QUEUED),
    "preparing": lambda: job_in(S.PREPARING),
    "submitting": lambda: job_in(S.SUBMITTING),
    "generating": lambda: job_in(S.GENERATING),
    "downloading": lambda: job_in(S.DOWNLOADING),
    "done": lambda: job_in(S.DONE),
    "failed": lambda: job_in(S.FAILED),
    "cancelled": lambda: job_in(S.CANCELLED),
    "p:fill_mismatch": lambda: job_in(P, R.FILL_MISMATCH),
    "p:step_failed": lambda: job_in(P, R.STEP_FAILED),
    "p:inputs_changed": lambda: job_in(P, R.INPUTS_CHANGED),
    "p:wait_timeout": lambda: job_in(P, R.WAIT_TIMEOUT),
    "p:download_failed": lambda: job_in(P, R.DOWNLOAD_FAILED),
    "p:restart_during_submit": lambda: job_in(P, R.RESTART_DURING_SUBMIT),
    "p:submit_rejected": lambda: job_in(P, R.SUBMIT_REJECTED),
    "p:submit_unconfirmed": lambda: job_in(P, R.SUBMIT_UNCONFIRMED),
    "p:estimate_exceeds_confirmed": lambda: job_in(P, R.ESTIMATE_EXCEEDS_CONFIRMED),
    "cli:preparing": lambda: job_in(S.PREPARING, backend=CLI),
    "cli:p:cli_error@preparing": lambda: job_in(P, R.CLI_ERROR, S.PREPARING, CLI),
    "cli:p:cli_error@submitting": lambda: job_in(P, R.CLI_ERROR, S.SUBMITTING, CLI),
    "cli:p:cli_error@generating": lambda: job_in(P, R.CLI_ERROR, S.GENERATING, CLI),
    "cli:p:cli_error@downloading": lambda: job_in(P, R.CLI_ERROR, S.DOWNLOADING, CLI),
}
WEB_ROWS = {k for k in ROWS if not k.startswith("cli:")}
CLI_ROWS = set(ROWS) - WEB_ROWS
ADJUDICATE_ROWS = {"p:restart_during_submit", "p:submit_rejected", "p:submit_unconfirmed", "cli:p:cli_error@submitting"}
RESUMABLE_ROWS = {"p:fill_mismatch", "p:step_failed", "p:wait_timeout", "p:download_failed",
                  "cli:p:cli_error@preparing", "cli:p:cli_error@generating", "cli:p:cli_error@downloading"}
CANCELLABLE_ROWS = {"queued", "preparing", "submitting", "generating", "downloading", "cli:preparing",
                    "p:inputs_changed", "p:estimate_exceeds_confirmed"} | RESUMABLE_ROWS

Command = Callable[[GenerationJobEntity], Any]
COMMANDS: dict[str, tuple[Command, set[str]]] = {
    "start_preparing": (lambda j: j.start_preparing(T0), {"queued"}),
    "set_blocked_on": (lambda j: j.set_blocked_on(BlockedOn.SLOT), {"queued"}),
    "mark_submitting": (lambda j: j.mark_submitting(T0), {"cli:preparing"}),
    "mark_generating": (lambda j: j.mark_generating("task-9", T0), {"submitting"}),
    "abort_submit": (lambda j: j.abort_submit(T0), set()),
    "mark_downloading": (lambda j: j.mark_downloading(T0), {"generating"}),
    "mark_done": (lambda j: j.mark_done(T0), {"downloading"}),
    "pause_fill_mismatch": (lambda j: j.pause(R.FILL_MISMATCH, T0), {"preparing", "cli:preparing"}),
    "pause_estimate_without_page": (lambda j: j.pause(R.ESTIMATE_EXCEEDS_CONFIRMED, T0), set()),
    "record_page_estimate": (lambda j: j.record_page_estimate(PAGE_OVER_ESTIMATE, False, T0), {"preparing", "cli:preparing"}),
    "pause_wait_timeout": (lambda j: j.pause(R.WAIT_TIMEOUT, T0), {"generating"}),
    "pause_download_failed": (lambda j: j.pause(R.DOWNLOAD_FAILED, T0), {"downloading"}),
    "pause_restart_during_submit": (lambda j: j.pause(R.RESTART_DURING_SUBMIT, T0), {"submitting"}),
    "pause_submit_rejected": (lambda j: j.pause(R.SUBMIT_REJECTED, T0), {"submitting"}),
    "pause_cli_error": (lambda j: j.pause(R.CLI_ERROR, T0), {"cli:preparing"}),
    "fail_moderation": (lambda j: j.fail(R.MODERATION_REJECT, T0), {"submitting", "generating"}),
    "fail_upload_rejected": (lambda j: j.fail(R.UPLOAD_REJECTED, T0), {"preparing", "cli:preparing"}),
    "yield_web_queue_pause": (lambda j: j.yield_to_queue_pause(R.CAPTCHA_OR_RISK_POPUP, T0), {"preparing"} | CLI_ROWS),
    "yield_cli_queue_pause": (lambda j: j.yield_to_queue_pause(R.CLI_LOGIN_REQUIRED, T0), {"cli:preparing"} | WEB_ROWS),
    "cancel": (lambda j: j.cancel(T0), CANCELLABLE_ROWS),
    "resume_api": (lambda j: j.resume(ResumeVia.API, T0), RESUMABLE_ROWS),
    "resume_ui": (lambda j: j.resume(ResumeVia.UI, T0), RESUMABLE_ROWS),
    "adjudicate_link_ui": (lambda j: j.adjudicate(Adjudication.LINK_EXISTING, ResumeVia.UI, T0, "hist-1"), ADJUDICATE_ROWS),
    "adjudicate_not_submitted_ui": (lambda j: j.adjudicate(Adjudication.CONFIRM_NOT_SUBMITTED, ResumeVia.UI, T0), ADJUDICATE_ROWS),
    "adjudicate_cancel_ui": (lambda j: j.adjudicate(Adjudication.CANCEL, ResumeVia.UI, T0), ADJUDICATE_ROWS),
    "adjudicate_cancel_api": (lambda j: j.adjudicate(Adjudication.CANCEL, ResumeVia.API, T0), set()),
    "approve_estimate_ui": (lambda j: j.approve_estimate(j.page_estimated_credits or 0, ResumeVia.UI, T0), {"p:estimate_exceeds_confirmed"}),
    "approve_estimate_api": (lambda j: j.approve_estimate(j.page_estimated_credits or 0, ResumeVia.API, T0), set()),
    "recover_after_restart": (lambda j: j.recover_after_restart(T0), set(ROWS)),
}


@pytest.mark.parametrize("row", list(ROWS))
@pytest.mark.parametrize("command", list(COMMANDS))
def test_transition_matrix(row: str, command: str) -> None:
    job = ROWS[row]()
    run, allowed = COMMANDS[command]
    before = (job.state, len(job.transitions), job.pause_reason, job.attempt)
    if row in allowed:
        run(job)
        rehydrate(job)
        return
    with pytest.raises(JobError):
        run(job)
    assert (job.state, len(job.transitions), job.pause_reason, job.attempt) == before


@pytest.mark.parametrize("row", list(ROWS))
def test_every_reachable_job_rehydrates(row: str) -> None:
    job = ROWS[row]()
    loaded = rehydrate(job)
    assert (loaded.state, loaded.pause_reason, loaded.paused_from, loaded.transitions) == (
        job.state, job.pause_reason, job.paused_from, job.transitions,
    )


RESUME_TARGETS = {
    "p:fill_mismatch": S.QUEUED, "p:step_failed": S.QUEUED, "p:wait_timeout": S.GENERATING,
    "p:download_failed": S.DOWNLOADING, "cli:p:cli_error@preparing": S.QUEUED,
    "cli:p:cli_error@generating": S.GENERATING, "cli:p:cli_error@downloading": S.GENERATING,
}


@pytest.mark.parametrize(("row", "target"), RESUME_TARGETS.items())
def test_resume_targets(row: str, target: JobState) -> None:
    job = ROWS[row]()
    job.resume(ResumeVia.API, T0)
    assert job.state is target and job.pause_reason is None and job.transitions[-1].reason == "resumed_via_api"


@pytest.mark.parametrize(("row", "error"), [("p:inputs_changed", ResumeNotAllowedError), ("p:estimate_exceeds_confirmed", AdjudicationRequiredError)]
                         + [(r, AdjudicationRequiredError) for r in sorted(ADJUDICATE_ROWS)])
@pytest.mark.parametrize("via", list(ResumeVia))
def test_resume_refusals(row: str, error: type[JobError], via: ResumeVia) -> None:
    with pytest.raises(error):
        ROWS[row]().resume(via, T0)


def test_happy_path_log() -> None:
    job = job_in(S.DONE)
    assert [(t.from_state, t.to_state) for t in job.transitions] == [
        (S.QUEUED, S.PREPARING), (S.PREPARING, S.SUBMITTING), (S.SUBMITTING, S.GENERATING),
        (S.GENERATING, S.DOWNLOADING), (S.DOWNLOADING, S.DONE),
    ]
    assert all(t.at == T0 and t.reason is None for t in job.transitions)


# U1-UT-01 — submit-unknown safety for cli_error and any submitting-origin pause
def test_cli_error_from_submitting_requires_ui_adjudication() -> None:
    job = ROWS["cli:p:cli_error@submitting"]()
    assert job.requires_adjudication
    with pytest.raises(AdjudicationRequiredError):
        job.resume(ResumeVia.API, T0)
    with pytest.raises(AdjudicationRequiredError):
        job.cancel(T0)
    with pytest.raises(UiOnlyActionError):
        job.adjudicate(Adjudication.CONFIRM_NOT_SUBMITTED, ResumeVia.API, T0)
    job.adjudicate(Adjudication.CONFIRM_NOT_SUBMITTED, ResumeVia.UI, T0)
    assert job.state is S.QUEUED and job.attempt == 2


def test_cli_error_submitting_adjudicate_cancel_assumes_spent() -> None:
    job = ROWS["cli:p:cli_error@submitting"]()
    job.adjudicate(Adjudication.CANCEL, ResumeVia.UI, T0)
    assert job.state is S.CANCELLED and job.credits_spent


def test_web_job_cannot_pause_with_cli_error() -> None:
    with pytest.raises(InvalidJobReasonError):
        job_in(S.SUBMITTING).pause(R.CLI_ERROR, T0)


# U1-UT-02 — frozen request bound to the job for every kind
@pytest.mark.parametrize(
    "frozen_factory",
    [
        lambda: FrozenRequest.freeze(image_request(), WEB, "d", STATIC_CREDITS, TOLERANCE_PCT),
        lambda: FrozenRequest.freeze(video_request(), CLI, "d", STATIC_CREDITS, TOLERANCE_PCT),
        lambda: FrozenRequest.freeze(video_request(prompt="改过"), WEB, "d", STATIC_CREDITS, TOLERANCE_PCT),
        lambda: FrozenRequest.freeze(video_request(duration=30), WEB, "d", STATIC_CREDITS, TOLERANCE_PCT),
    ],
    ids=["kind", "backend", "prompt", "params"],
)
def test_confirm_rejects_mismatched_frozen_request(frozen_factory: Callable[[], FrozenRequest]) -> None:
    job = new_job(confirmed=False)
    with pytest.raises(ConfirmationMismatchError):
        job.confirm(proof(), frozen_factory(), confirmed_item(job.request))
    assert not job.confirmed


@pytest.mark.parametrize(
    "frozen_request",
    [entity_create_request(prompt="确认页改过的描述"), entity_create_request(name="hy3_别人"), video_request()],
    ids=["edited_description", "entity_name", "video"],
)
def test_entity_create_confirm_is_bound(frozen_request: Any) -> None:
    job = new_job(entity_create_request(), confirmed=False)
    item = confirmed_item(job.request, 0)
    with pytest.raises(ConfirmationMismatchError):
        job.confirm(proof(), FrozenRequest.freeze(frozen_request, WEB, "d", 0, TOLERANCE_PCT), item)
    job.confirm(proof(), FrozenRequest.from_item(item, WEB, "d", TOLERANCE_PCT), item)
    assert job.confirmed


def test_confirm_rejects_other_batch_and_forged_confirmer() -> None:
    job = new_job(confirmed=False)
    item = confirmed_item(job.request)
    frozen = FrozenRequest.from_item(item, WEB, "d", TOLERANCE_PCT)
    with pytest.raises(ConfirmationMismatchError):
        job.confirm(proof("batch-other"), frozen, item)
    forged = proof()
    object.__setattr__(forged, "confirmer", "mcp")
    with pytest.raises(ConfirmationMismatchError):
        job.confirm(forged, frozen, item)


# U1-UT-03 — cancel intent persists
def test_cancel_intent_survives_restart_and_blocks_requeue() -> None:
    job = job_in(S.SUBMITTING)
    job.cancel(T0)
    assert job.recover_after_restart(T0) and job.cancel_requested and job.state is P
    assert rehydrate(job).cancel_requested
    job.adjudicate(Adjudication.CONFIRM_NOT_SUBMITTED, ResumeVia.UI, T0)
    assert job.state is S.CANCELLED and not job.credits_spent and job.attempt == 1


def test_cancel_intent_with_submit_rejected_cancels_without_spend() -> None:
    job = job_in(S.SUBMITTING)
    job.cancel(T0)
    job.pause(R.SUBMIT_REJECTED, T0)
    assert job.state is S.CANCELLED and not job.credits_spent and job.pause_reason is None


def test_cancel_intent_with_link_existing_cancels_with_spend() -> None:
    job = job_in(S.SUBMITTING)
    job.cancel(T0)
    job.pause(R.SUBMIT_UNCONFIRMED, T0)
    with pytest.raises(AdjudicationRequiredError):
        job.cancel(T0)
    job.adjudicate(Adjudication.LINK_EXISTING, ResumeVia.UI, T0, "hist-7")
    assert job.state is S.CANCELLED and job.credits_spent and job.platform_task_id == "hist-7"


def test_cancel_during_submitting_click_outcomes() -> None:
    clicked = job_in(S.SUBMITTING)
    clicked.cancel(T0)
    clicked.mark_generating("task-7", T0)
    assert clicked.state is S.CANCELLED and clicked.credits_spent
    not_clicked = job_in(S.SUBMITTING)
    not_clicked.cancel(T0)
    not_clicked.abort_submit(T0)
    assert not_clicked.state is S.CANCELLED and not not_clicked.credits_spent


@pytest.mark.parametrize(("row", "spent"), [("queued", False), ("preparing", False), ("generating", True), ("downloading", True), ("p:wait_timeout", True), ("p:fill_mismatch", False)])
def test_cancel_credit_semantics(row: str, spent: bool) -> None:
    job = ROWS[row]()
    job.cancel(T0)
    assert job.state is S.CANCELLED and job.credits_spent is spent


@pytest.mark.parametrize(("row", "spent"), [("p:restart_during_submit", True), ("p:submit_unconfirmed", True), ("p:submit_rejected", False)])
def test_adjudicate_cancel(row: str, spent: bool) -> None:
    job = ROWS[row]()
    job.adjudicate(Adjudication.CANCEL, ResumeVia.UI, T0)
    assert job.state is S.CANCELLED and job.credits_spent is spent


def test_adjudicate_link_requires_task_id() -> None:
    with pytest.raises(MissingPlatformTaskIdError):
        ROWS["p:restart_during_submit"]().adjudicate(Adjudication.LINK_EXISTING, ResumeVia.UI, T0)


# U1-UT-05 — estimate approval bound to an amount
def test_page_estimate_tolerance_boundary() -> None:
    within = job_in(S.PREPARING)
    assert not within.record_page_estimate(528, False, T0) and within.state is S.PREPARING
    over = job_in(S.PREPARING)
    assert over.record_page_estimate(529, False, T0) and over.pause_reason is R.ESTIMATE_EXCEEDS_CONFIRMED
    assert over.page_estimated_credits == 529


def test_approval_is_bound_to_amount_and_ui_only() -> None:
    job = ROWS["p:estimate_exceeds_confirmed"]()
    with pytest.raises(UiOnlyActionError):
        job.approve_estimate(PAGE_OVER_ESTIMATE, ResumeVia.API, T0)
    with pytest.raises(EstimateApprovalMismatchError):
        job.approve_estimate(PAGE_OVER_ESTIMATE - 1, ResumeVia.UI, T0)
    job.approve_estimate(PAGE_OVER_ESTIMATE, ResumeVia.UI, T0)
    assert job.state is S.QUEUED and job.approved_credits == PAGE_OVER_ESTIMATE and job.estimate_approved
    job.start_preparing(T0)
    assert not job.record_page_estimate(720, False, T0)
    assert job.record_page_estimate(721, False, T0) and job.state is P


def test_other_pause_clears_approval() -> None:
    job = ROWS["p:estimate_exceeds_confirmed"]()
    job.approve_estimate(PAGE_OVER_ESTIMATE, ResumeVia.UI, T0)
    job.start_preparing(T0)
    job.pause(R.FILL_MISMATCH, T0)
    assert job.approved_credits is None
    job.resume(ResumeVia.API, T0)
    job.start_preparing(T0)
    assert job.record_page_estimate(PAGE_OVER_ESTIMATE, False, T0)


def test_unestimated_first_job_pauses() -> None:
    first = new_job(credits=None)
    first.start_preparing(T0)
    assert first.record_page_estimate(100, True, T0)
    later = new_job(credits=None)
    later.start_preparing(T0)
    assert not later.record_page_estimate(100, False, T0)


def test_confirm_not_submitted_clears_estimate_state() -> None:
    job = ROWS["p:estimate_exceeds_confirmed"]()
    job.approve_estimate(PAGE_OVER_ESTIMATE, ResumeVia.UI, T0)
    prepared_to_last_step(job).mark_submitting(T0)
    job.recover_after_restart(T0)
    job.adjudicate(Adjudication.CONFIRM_NOT_SUBMITTED, ResumeVia.UI, T0)
    assert job.page_estimated_credits is None and job.approved_credits is None


def test_negative_page_estimate_rejected() -> None:
    with pytest.raises(JobInvariantError):
        job_in(S.PREPARING).record_page_estimate(-1, False, T0)


# U1-UT-12 — mark_submitting re-checks the estimate gate itself
def _at_last_step(job: GenerationJobEntity) -> GenerationJobEntity:
    return prepared_to_last_step(job, page_credits=None)


def test_web_submit_requires_estimate_from_current_preparation() -> None:
    job = _at_last_step(new_job())
    before = job.snapshot()
    with pytest.raises(EstimateNotRecordedError):
        job.mark_submitting(T0)
    assert job.snapshot() == before
    job.record_page_estimate(STATIC_CREDITS, False, T0)
    job.mark_submitting(T0)
    assert job.state is S.SUBMITTING


def test_cleared_approval_with_old_estimate_cannot_submit_without_fresh_estimate() -> None:
    job = new_job()
    job.start_preparing(T0)
    assert job.record_page_estimate(900, False, T0)
    job.approve_estimate(900, ResumeVia.UI, T0)
    job.start_preparing(T0)
    job.pause(R.FILL_MISMATCH, T0)
    assert job.approved_credits is None
    job.resume(ResumeVia.API, T0)
    _at_last_step(job)
    with pytest.raises(EstimateNotRecordedError):
        job.mark_submitting(T0)
    stale = GenerationJobEntity.from_snapshot(replace(job.snapshot(), page_estimated_credits=900))
    with pytest.raises(EstimateNotApprovedError):
        stale.mark_submitting(T0)
    assert stale.state is S.PREPARING
    assert job.record_page_estimate(900, False, T0) and job.pause_reason is R.ESTIMATE_EXCEEDS_CONFIRMED


@pytest.mark.parametrize(
    ("page", "approved", "allowed"),
    [(528, None, True), (529, None, False), (900, None, False), (900, 900, True), (1080, 900, True), (1081, 900, False)],
)
def test_submit_refuses_recorded_estimate_over_baseline(page: int, approved: int | None, allowed: bool) -> None:
    saved = _at_last_step(new_job()).snapshot()
    job = GenerationJobEntity.from_snapshot(replace(saved, page_estimated_credits=page, approved_credits=approved))
    before = job.snapshot()
    if allowed:
        job.mark_submitting(T0)
        assert job.state is S.SUBMITTING
        return
    with pytest.raises(EstimateNotApprovedError):
        job.mark_submitting(T0)
    assert job.snapshot() == before


def test_start_preparing_clears_estimate_but_keeps_approval() -> None:
    job = job_in(P, R.ESTIMATE_EXCEEDS_CONFIRMED)
    job.approve_estimate(PAGE_OVER_ESTIMATE, ResumeVia.UI, T0)
    job.start_preparing(T0)
    assert job.page_estimated_credits is None and job.approved_credits == PAGE_OVER_ESTIMATE


def test_cli_entity_and_unestimated_jobs_submit_paths() -> None:
    cli = new_job(backend=CLI)
    cli.start_preparing(T0)
    cli.mark_submitting(T0)
    entity = _at_last_step(new_job(entity_create_request(), credits=0))
    entity.mark_submitting(T0)
    unestimated = _at_last_step(new_job(credits=None))
    unestimated.record_page_estimate(5000, False, T0)
    unestimated.mark_submitting(T0)
    assert cli.state is entity.state is unestimated.state is S.SUBMITTING


# U1-UT-13 — the per-job credit baseline is bound to the confirmed batch item
def _error_item(request: GenerationRequest) -> BatchItem:
    error = PrecheckItem(PrecheckCheck.PARAMS, CheckSeverity.ERROR, "duration_out_of_range", "x")
    return BatchItem.of(0, request, PrecheckResult((error,), PriceEstimate(STATIC_CREDITS)))


def _dedupe_item(request: GenerationRequest) -> BatchItem:
    return BatchItem.of(0, request, PrecheckResult((), PriceEstimate(STATIC_CREDITS), existing_job_id="job-0"))


@pytest.mark.parametrize(
    ("item_factory", "frozen_credits"),
    [
        (lambda r: confirmed_item(r, STATIC_CREDITS), 99_999),
        (lambda r: confirmed_item(r, STATIC_CREDITS), None),
        (lambda r: confirmed_item(r, None), STATIC_CREDITS),
        (lambda r: confirmed_item(video_request(duration=10), STATIC_CREDITS), STATIC_CREDITS),
        (_error_item, STATIC_CREDITS),
        (_dedupe_item, STATIC_CREDITS),
    ],
    ids=["inflated", "dropped", "invented", "other_item", "error_item", "dedupe_item"],
)
def test_confirm_binds_frozen_estimate_to_confirmed_item(
    item_factory: Callable[[GenerationRequest], BatchItem], frozen_credits: int | None
) -> None:
    job = new_job(confirmed=False)
    frozen = FrozenRequest.freeze(job.request, WEB, "d", frozen_credits, TOLERANCE_PCT)
    with pytest.raises(ConfirmationMismatchError):
        job.confirm(proof(), frozen, item_factory(job.request))
    assert not job.confirmed


def test_confirmed_item_estimate_drives_the_gate() -> None:
    job = new_job(confirmed=False)
    item = confirmed_item(job.request, STATIC_CREDITS)
    job.confirm(proof(), FrozenRequest.from_item(item, WEB, "d", TOLERANCE_PCT), item)
    job.start_preparing(T0)
    assert job.frozen_request is not None and job.frozen_request.credits_estimated == STATIC_CREDITS
    assert job.record_page_estimate(5000, False, T0)


# U1-UT-14 — snapshot round trip; commits are atomic
def test_snapshot_round_trip_and_invalid_snapshot_rejected() -> None:
    job = job_in(P, R.ESTIMATE_EXCEEDS_CONFIRMED)
    assert GenerationJobEntity.from_snapshot(job.snapshot()).snapshot() == job.snapshot()
    assert rehydrate(job).snapshot() == job.snapshot()
    with pytest.raises(JobInvariantError):
        GenerationJobEntity.from_snapshot(replace(job.snapshot(), page_estimated_credits=None))


# FR-16 — unconfirmed jobs never reach preparing / submitting through any path
HUMAN_PATHS: list[Command] = [
    lambda j: j.start_preparing(T0),
    lambda j: j.mark_submitting(T0),
    lambda j: j.resume(ResumeVia.API, T0),
    lambda j: j.resume(ResumeVia.UI, T0),
    lambda j: j.adjudicate(Adjudication.LINK_EXISTING, ResumeVia.UI, T0, "x"),
    lambda j: j.adjudicate(Adjudication.CONFIRM_NOT_SUBMITTED, ResumeVia.UI, T0),
    lambda j: j.approve_estimate(0, ResumeVia.UI, T0),
    lambda j: j.recover_after_restart(T0),
    lambda j: j.record_page_estimate(1, True, T0),
    lambda j: j.yield_to_queue_pause(R.CAPTCHA_OR_RISK_POPUP, T0),
]


@pytest.mark.parametrize("backend", [WEB, CLI])
@pytest.mark.parametrize("path", range(len(HUMAN_PATHS)))
def test_fr16_unconfirmed_job_never_prepares_or_submits(path: int, backend: BackendKind) -> None:
    job = new_job(confirmed=False, backend=backend)
    for index in [path, *range(len(HUMAN_PATHS))]:
        try:
            HUMAN_PATHS[index](job)
        except JobError:
            pass
    assert job.state is S.QUEUED
    assert all(t.to_state not in (S.PREPARING, S.SUBMITTING) for t in job.transitions)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"state": S.PREPARING, "current_step": PreparingStep.SET_PARAMS},
        {"state": S.SUBMITTING},
        {"state": S.GENERATING, "platform_task_id": "t"},
        {"state": S.DOWNLOADING, "platform_task_id": "t"},
        {"state": S.DONE, "platform_task_id": "t"},
        {"state": P, "pause_reason": R.FILL_MISMATCH, "paused_from": S.PREPARING},
        {"state": P, "pause_reason": R.WAIT_TIMEOUT, "paused_from": S.GENERATING, "platform_task_id": "t"},
        {"state": S.FAILED, "failure_reason": R.UPLOAD_REJECTED},
    ],
)
def test_fr16_unconfirmed_active_jobs_cannot_be_loaded(kwargs: dict[str, Any]) -> None:
    request = video_request()
    with pytest.raises(JobInvariantError):
        GenerationJobEntity("j", "batch-1", WEB, request, Fingerprint.of(request), **kwargs)


# U1-UT-07 — invariants on load
@pytest.mark.parametrize(
    "changes",
    [
        {"state": P, "pause_reason": R.WAIT_TIMEOUT, "paused_from": S.GENERATING},
        {"state": P, "pause_reason": R.CLI_ERROR, "paused_from": S.PREPARING},
        {"state": P, "pause_reason": R.FILL_MISMATCH, "paused_from": S.GENERATING, "platform_task_id": "t"},
        {"state": P, "pause_reason": R.ESTIMATE_EXCEEDS_CONFIRMED, "paused_from": S.PREPARING},
        {"state": S.QUEUED, "paused_from": S.PREPARING},
        {"state": S.QUEUED, "current_step": PreparingStep.FILL},
        {"state": S.GENERATING, "platform_task_id": "t", "blocked_on": BlockedOn.SLOT},
        {"state": S.QUEUED, "cancel_requested": True},
        {"state": S.QUEUED, "page_estimated_credits": -1},
        {"state": S.DONE},
    ],
)
def test_inconsistent_saved_jobs_rejected(changes: dict[str, Any]) -> None:
    base = job_in(S.QUEUED)
    with pytest.raises(JobInvariantError):
        GenerationJobEntity(
            "j", "batch-1", WEB, base.request, base.fingerprint,
            confirmation=base.confirmation, frozen_request=base.frozen_request, **changes,
        )


# U1-UT-08 — queue pauses only affect their backend
def test_yield_to_queue_pause_ignores_other_backend() -> None:
    cli_job = job_in(S.PREPARING, backend=CLI)
    assert not cli_job.yield_to_queue_pause(R.CAPTCHA_OR_RISK_POPUP, T0) and cli_job.state is S.PREPARING
    web_job = job_in(S.PREPARING)
    assert not web_job.yield_to_queue_pause(R.CLI_LOGIN_REQUIRED, T0) and web_job.state is S.PREPARING
    assert web_job.yield_to_queue_pause(R.LOGIN_EXPIRED, T0)
    assert web_job.state is S.QUEUED and web_job.blocked_on is BlockedOn.QUEUE_PAUSED


# U1-UT-09 — state is guarded
@pytest.mark.parametrize("attribute", ["state", "confirmation", "frozen_request", "platform_task_id", "pause_reason", "approved_credits"])
def test_guarded_attributes_are_read_only(attribute: str) -> None:
    job = job_in(S.QUEUED)
    with pytest.raises(AttributeError):
        setattr(job, attribute, None)
    with pytest.raises(AttributeError):
        job.transitions.append(None)  # type: ignore[attr-defined]


# U1-BDD-07 — CLI prepare has only the final verify step
def test_cli_prepare_steps() -> None:
    job = new_job(backend=CLI)
    job.start_preparing(T0)
    assert job.preparing_steps == (PreparingStep.VERIFY,) and job.current_step is PreparingStep.VERIFY
    with pytest.raises(StepOrderError):
        job.advance_step(PreparingStep.UPLOAD)
    job.mark_submitting(T0)
    assert job.state is S.SUBMITTING


def test_web_step_order_enforced() -> None:
    job = job_in(S.PREPARING)
    with pytest.raises(StepOrderError):
        job.advance_step(PreparingStep.FILL)
    with pytest.raises(StepOrderError):
        job.mark_submitting(T0)
    job.advance_step(PreparingStep.UPLOAD)
    assert job.current_step is PreparingStep.UPLOAD


def test_unconfirmed_start_preparing_error_type() -> None:
    with pytest.raises(UnconfirmedJobError):
        new_job(confirmed=False).start_preparing(T0)


def test_mark_generating_requires_task_id() -> None:
    with pytest.raises(MissingPlatformTaskIdError):
        job_in(S.SUBMITTING).mark_generating("", T0)


@pytest.mark.parametrize("state", [S.DONE, S.FAILED, S.CANCELLED])
def test_cancel_terminal_rejected(state: JobState) -> None:
    with pytest.raises(JobAlreadyTerminalError):
        job_in(state).cancel(T0)


def test_fail_after_submission_marks_credits_spent() -> None:
    job = job_in(S.GENERATING)
    job.fail(R.MODERATION_REJECT, T0)
    assert job.failure_reason is R.MODERATION_REJECT and job.credits_spent
    assert job.transitions[-1].reason == "moderation_reject"


def test_recover_after_restart() -> None:
    submitting = job_in(S.SUBMITTING)
    assert submitting.recover_after_restart(T0) and submitting.pause_reason is R.RESTART_DURING_SUBMIT
    for row in ("generating", "downloading", "queued", "done", "p:wait_timeout"):
        job = ROWS[row]()
        before = job.state
        assert not job.recover_after_restart(T0) and job.state is before
    preparing = job_in(S.PREPARING)
    assert preparing.recover_after_restart(T0) and preparing.state is S.QUEUED
