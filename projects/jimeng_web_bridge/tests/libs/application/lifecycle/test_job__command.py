from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest

from libs.application.commands.job__command import JobCommand
from libs.application.errors.lifecycle__error import InvalidQueueReasonError, JobNotFoundError
from libs.common.clock import FrozenClock
from libs.common.enums import Adjudication, BackendKind, JobState, PauseReason, ResumeVia
from libs.domain.errors.job__error import (
    AdjudicationRequiredError, EstimateApprovalMismatchError, JobAlreadyTerminalError, ResumeNotAllowedError,
)
from libs.infrastructure.clients.sqlite__client import SqliteClient
from libs.infrastructure.readers.store_record__reader import QueueStateReader
from libs.infrastructure.writers.store_record__writer import QueueStateWriter
from tests.libs.application.lifecycle.fakes import FakeJobRepository
from tests.libs.domain.builders import PAGE_OVER_ESTIMATE, T0, job_in

S, R = JobState, PauseReason


class Env:
    def __init__(self, tmp_path: Path) -> None:
        self.client = SqliteClient(tmp_path / "bridge.db")
        self.jobs = FakeJobRepository(self.client)
        self.queues = QueueStateReader(self.client)
        self.command = JobCommand(self.jobs, (self.queues, QueueStateWriter(self.client)), FrozenClock(T0))

    def put(self, state: JobState, reason: PauseReason | None = None, origin: JobState | None = None,
            backend: BackendKind = BackendKind.WEB) -> str:
        self.jobs.save(job_in(state, reason, origin, backend))
        return "job-1"


@pytest.fixture
def env(tmp_path: Path) -> Iterator[Env]:
    environment = Env(tmp_path)
    yield environment
    environment.client.close()


@pytest.mark.parametrize("state", [S.QUEUED, S.PREPARING])
def test_cancel_before_submit_spends_nothing(env: Env, state: JobState) -> None:
    reply = env.command.cancel(env.put(state))
    assert reply.state == "cancelled" and not reply.credits_spent and reply.message == "已取消，未花费积分"


@pytest.mark.parametrize("state", [S.GENERATING, S.DOWNLOADING])
def test_cancel_after_submit_says_credits_are_not_refunded(env: Env, state: JobState) -> None:
    reply = env.command.cancel(env.put(state))
    assert reply.state == "cancelled" and reply.credits_spent and "积分不会退还" in (reply.message or "")


def test_cancel_during_submitting_records_intent_only(env: Env) -> None:
    reply = env.command.cancel(env.put(S.SUBMITTING))
    stored = env.jobs.get("job-1")
    assert reply.state == "submitting" and reply.cancel_requested
    assert stored is not None and stored.cancel_requested and stored.state is S.SUBMITTING


def test_cancel_terminal_and_unknown_jobs(env: Env) -> None:
    with pytest.raises(JobNotFoundError):
        env.command.cancel("nope")
    with pytest.raises(JobAlreadyTerminalError):
        env.command.cancel(env.put(S.DONE))


@pytest.mark.parametrize("reason", [R.SUBMIT_REJECTED, R.SUBMIT_UNCONFIRMED, R.RESTART_DURING_SUBMIT])
def test_unknown_submit_outcomes_are_ui_adjudication_only(env: Env, reason: PauseReason) -> None:
    job_id = env.put(S.PAUSED_NEEDS_HUMAN, reason)
    for action in (lambda: env.command.cancel(job_id), lambda: env.command.resume(job_id, ResumeVia.API),
                   lambda: env.command.resume(job_id, ResumeVia.UI)):
        with pytest.raises(AdjudicationRequiredError):
            action()


@pytest.mark.parametrize(("reason", "target"), [(R.FILL_MISMATCH, "queued"), (R.STEP_FAILED, "queued"), (R.WAIT_TIMEOUT, "generating"), (R.DOWNLOAD_FAILED, "downloading")])
def test_api_resume_for_resumable_reasons(env: Env, reason: PauseReason, target: str) -> None:
    assert env.command.resume(env.put(S.PAUSED_NEEDS_HUMAN, reason), ResumeVia.API).state == target


def test_inputs_changed_cannot_be_resumed(env: Env) -> None:
    with pytest.raises(ResumeNotAllowedError):
        env.command.resume(env.put(S.PAUSED_NEEDS_HUMAN, R.INPUTS_CHANGED), ResumeVia.API)


def test_cli_error_while_submitting_requires_adjudication(env: Env) -> None:
    job_id = env.put(S.PAUSED_NEEDS_HUMAN, R.CLI_ERROR, S.SUBMITTING, BackendKind.CLI)
    with pytest.raises(AdjudicationRequiredError):
        env.command.resume(job_id, ResumeVia.API)
    assert env.command.adjudicate(job_id, Adjudication.CONFIRM_NOT_SUBMITTED, None).state == "queued"


def test_adjudication_paths(env: Env) -> None:
    linked = env.command.adjudicate(env.put(S.PAUSED_NEEDS_HUMAN, R.SUBMIT_UNCONFIRMED), Adjudication.LINK_EXISTING, "task-9")
    assert linked.state == "generating" and linked.platform_task_id == "task-9"
    retried = env.command.adjudicate(env.put(S.PAUSED_NEEDS_HUMAN, R.RESTART_DURING_SUBMIT), Adjudication.CONFIRM_NOT_SUBMITTED, None)
    assert retried.state == "queued" and retried.attempt == 2
    cancelled = env.command.adjudicate(env.put(S.PAUSED_NEEDS_HUMAN, R.SUBMIT_UNCONFIRMED), Adjudication.CANCEL, None)
    assert cancelled.state == "cancelled" and "积分不会退还" in (cancelled.message or "")


def test_estimate_approval_binds_to_the_page_amount(env: Env) -> None:
    job_id = env.put(S.PAUSED_NEEDS_HUMAN, R.ESTIMATE_EXCEEDS_CONFIRMED)
    with pytest.raises(EstimateApprovalMismatchError):
        env.command.approve_estimate(job_id, PAGE_OVER_ESTIMATE + 1)
    reply = env.command.approve_estimate(job_id, PAGE_OVER_ESTIMATE)
    stored = env.jobs.get(job_id)
    assert reply.state == "queued" and stored is not None and stored.approved_credits == PAGE_OVER_ESTIMATE


def test_queue_pause_and_running(env: Env) -> None:
    with pytest.raises(InvalidQueueReasonError):
        env.command.pause_queue(BackendKind.WEB, R.CLI_LOGIN_REQUIRED)
    with pytest.raises(InvalidQueueReasonError):
        env.command.pause_queue(BackendKind.WEB, R.FILL_MISMATCH)
    manual = env.command.pause_queue(BackendKind.WEB, None)
    captcha = env.command.pause_queue(BackendKind.WEB, R.CAPTCHA_OR_RISK_POPUP)
    assert (manual.state, manual.reason, captcha.reason) == ("paused", "manual", "captcha_or_risk_popup")
    running = env.command.mark_queue_running(BackendKind.WEB)
    assert (running.state, running.reason) == ("running", None)
    assert [(row.backend, row.state) for row in env.queues.all()] == [("web", "running")]
