from __future__ import annotations

import hashlib
import json
from datetime import timedelta
from pathlib import Path

import pytest

from libs.common.enums import BackendKind, BlockedOn, JobState, PauseReason, PreparingStep, ResumeVia
from libs.domain.errors.job__error import AdjudicationRequiredError, EstimateApprovalMismatchError
from libs.domain.repositories.generation_backend__repository import BackendHealth, PrepareResult, SubmitOutcome
from libs.infrastructure.readers.job__reader import JobReader
from tests.libs.application.lifecycle.fakes import (
    CARD_REL, SHOTS_REL, FakeWebBackend, Harness, PrepareResultWithNegative, advance, confirmed_job, image_request,
    make_harness, reference_file, video_request,
)

W, C = BackendKind.WEB, BackendKind.CLI
S = JobState
SIDECAR_KEYS = [
    "job_id", "batch_id", "attempt", "backend", "source", "prompt_sha256", "negative_prompt_sha256",
    "negative_prompt_sent", "references", "params", "platform_task_id", "credits_estimated", "credits_charged",
    "confirmed_at", "confirmer", "submitted_at", "finished_at", "durations", "web_version", "browser_version", "output",
]


@pytest.fixture
def h(tmp_path: Path) -> Harness:
    harness = make_harness(tmp_path)
    yield harness
    harness.client.close()


def web(h: Harness, job_id: str, **request: object) -> None:
    h.add(confirmed_job(job_id, video_request(job_id, **request)))  # type: ignore[arg-type]


def test_web_job_runs_to_done_with_render_and_whitelisted_sidecar(h: Harness) -> None:
    h.add(confirmed_job("job-a", video_request("shot02")))
    h.run_until(lambda: h.state("job-a") is S.DONE, limit=80)
    prepares = [call for call in h.web.calls if call[0] == "prepare"]
    assert prepares == [("prepare", f"job-a:{step}") for step in ("set_params", "upload", "fill", "preview", "verify")]
    assert h.web.submit_states == [S.SUBMITTING]
    outputs = h.runtime("job-a")["outputs"]
    assert isinstance(outputs, list) and len(outputs) == 1
    assert outputs[0].startswith(f"{SHOTS_REL}/shot02/renders/shot02_20260913-18") and outputs[0].endswith(".mp4")
    sidecar = json.loads(h.abs(outputs[0] + ".jimeng.json").read_text(encoding="utf-8"))
    assert list(sidecar) == SIDECAR_KEYS
    assert sidecar["credits_estimated"] == {"static": 440, "page": 440} and sidecar["credits_charged"] == 440
    assert sidecar["confirmer"] == "ui_human" and sidecar["negative_prompt_sha256"] is None and sidecar["negative_prompt_sent"] is False
    assert sidecar["web_version"] == "web-1.0" and sidecar["platform_task_id"] == "task-job-a-1"
    assert set(sidecar["durations"]) == {"prepare_s", "queue_wait_s", "render_s", "download_s"}
    dao = JobReader(h.client).get("job-a")
    assert dao is not None and dao.credits_charged == 440
    assert [toast["title"] for toast in h.toasts()] == ["批次已全部结束"]


def test_remote_rendering_never_exceeds_cap_and_submits_are_spaced_across_backends(h: Harness) -> None:
    h.web.polls_to_finish = h.cli.polls_to_finish = 8
    ids = [f"web-{i}" for i in range(5)] + [f"cli-{i}" for i in range(3)]
    for index in range(5):
        web(h, f"web-{index}")
    for index in range(3):
        h.add(confirmed_job(f"cli-{index}", image_request(f"c1-{index + 1}"), C))
    peak: list[int] = []

    def check() -> None:
        peak.append(h.remote_count())
        assert h.remote_count() <= 3
        assert len(h.web.active_tasks) + len(h.cli.active_tasks) <= 3

    h.run(900, check=check)
    assert all(h.state(job_id) is S.DONE for job_id in ids)
    assert max(peak) == 3
    submits = sorted(h.web.submit_times + h.cli.submit_times)
    assert len(submits) == 8
    assert all((later - earlier).total_seconds() >= 15 for earlier, later in zip(submits, submits[1:]))


def test_min_interval_comes_from_config(h: Harness) -> None:
    h.set_config("pacing", "min_submit_interval_s", 40)
    web(h, "web-a")
    h.add(confirmed_job("cli-a", image_request("c1-1"), C))
    h.run_until(lambda: h.state("web-a") is S.DONE and h.state("cli-a") is S.DONE, limit=300)
    first, second = sorted(h.web.submit_times + h.cli.submit_times)
    assert (second - first).total_seconds() >= 40


def test_web_queue_pause_blocks_only_web_jobs(h: Harness) -> None:
    h.pause_queue(W, "captcha_or_risk_popup")
    web(h, "web-a")
    h.add(confirmed_job("cli-a", image_request("c1-1"), C))
    h.run_until(lambda: h.state("cli-a") is S.DONE, limit=100)
    assert h.web.count("prepare") == 0 and h.web.count("submit") == 0
    parked = h.job("web-a")
    assert parked.state is S.QUEUED and parked.blocked_on is BlockedOn.QUEUE_PAUSED


def test_preparation_waits_for_a_slot(h: Harness) -> None:
    h.set_config("concurrency", "max_remote_rendering", 1)
    h.web.polls_to_finish = 20
    web(h, "job-a")
    web(h, "job-b")
    h.run_until(lambda: h.state("job-a") is S.GENERATING, limit=40)
    h.run(60)
    assert ("prepare", "job-b:set_params") not in h.web.calls
    assert h.job("job-b").blocked_on is BlockedOn.SLOT
    h.run_until(lambda: h.state("job-b") is S.DONE, limit=400)
    b_prepared = h.web.calls.index(("prepare", "job-b:set_params"))
    assert h.web.calls.index(("download", "job-a")) < b_prepared or h.state("job-a") is S.DONE


def test_recover_after_crash_never_resubmits_and_resumes_observation(h: Harness) -> None:
    for job_id, slot, state in (("sub", "shot01", S.SUBMITTING), ("gen", "shot02", S.GENERATING),
                                ("prep", "shot03", S.PREPARING), ("dl", "shot04", S.DOWNLOADING)):
        h.add(advance(confirmed_job(job_id, video_request(slot)), state))
    recovered_at = h.clock.now()
    recovery = h.scheduler.recover(recovered_at)
    assert {(item.job_id, item.to_state, item.reason) for item in recovery.recovered} == {
        ("sub", "paused_needs_human", "restart_during_submit"), ("prep", "queued", None),
    }
    assert recovery.resumed_polling == ("gen",) and recovery.resumed_downloads == ("dl",)
    h.run_until(lambda: all(h.state(j) is S.DONE for j in ("gen", "dl", "prep")), limit=200)
    assert [call for call in h.web.calls if call[0] == "submit"] == [("submit", "prep")]
    assert h.state("sub") is S.PAUSED_NEEDS_HUMAN and h.job("sub").requires_adjudication
    assert (h.web.submit_times[0] - recovered_at).total_seconds() >= 15
    assert "作业待人工处理" in [toast["title"] for toast in h.toasts()]


def test_submit_exception_is_never_retried(h: Harness) -> None:
    web(h, "job-a")
    h.web.submit_script["job-a"] = [RuntimeError("page crashed mid-click")]
    h.run_until(lambda: h.state("job-a") is S.PAUSED_NEEDS_HUMAN, limit=40)
    h.run(60)
    job = h.job("job-a")
    assert h.web.count("submit") == 1
    assert job.pause_reason is PauseReason.SUBMIT_UNCONFIRMED and job.requires_adjudication


def test_post_click_rejection_pauses_submit_rejected_with_exactly_one_click(h: Harness) -> None:
    web(h, "job-a")
    web(h, "job-b")
    h.web.submit_script["job-a"] = [SubmitOutcome(None, PauseReason.SUBMIT_REJECTED, "并行任务已达上限")]
    h.run_until(lambda: h.state("job-b") is S.DONE, limit=200)
    assert h.job("job-a").pause_reason is PauseReason.SUBMIT_REJECTED
    assert [call for call in h.web.calls if call == ("submit", "job-a")] == [("submit", "job-a")]


def test_no_task_id_and_no_rejection_is_submit_unconfirmed(h: Harness) -> None:
    web(h, "job-a")
    h.web.submit_script["job-a"] = [SubmitOutcome(None, None, "未截获提交响应")]
    h.run_until(lambda: h.state("job-a") is S.PAUSED_NEEDS_HUMAN, limit=40)
    assert h.job("job-a").pause_reason is PauseReason.SUBMIT_UNCONFIRMED


def test_backend_that_proves_no_click_pauses_submit_rejected(h: Harness) -> None:
    web(h, "job-a")
    h.web.submit_script["job-a"] = [SubmitOutcome(None, None, "not_now:concurrency_limit_pre_click")]
    h.run_until(lambda: h.state("job-a") is S.PAUSED_NEEDS_HUMAN, limit=40)
    assert h.job("job-a").pause_reason is PauseReason.SUBMIT_REJECTED and not h.job("job-a").credits_spent


def test_page_estimate_over_tolerance_pauses_and_ui_approval_is_bound_to_the_amount(h: Harness) -> None:
    web(h, "job-a")
    h.web.page_estimate = 600
    h.run_until(lambda: h.state("job-a") is S.PAUSED_NEEDS_HUMAN, limit=40)
    job = h.job("job-a")
    assert job.pause_reason is PauseReason.ESTIMATE_EXCEEDS_CONFIRMED and job.page_estimated_credits == 600
    assert h.web.count("submit") == 0 and ("prepare", "job-a:verify") not in h.web.calls
    with pytest.raises(EstimateApprovalMismatchError):
        h.job_command.approve_estimate("job-a", 599)
    assert h.job_command.approve_estimate("job-a", 600).state == "queued"
    h.run_until(lambda: h.state("job-a") is S.DONE, limit=120)
    assert h.web.count("submit") == 1


def test_missing_static_estimate_pauses_the_first_job(h: Harness) -> None:
    h.add(confirmed_job("job-a", video_request("shot02"), credits=None))
    h.run_until(lambda: h.state("job-a") is S.PAUSED_NEEDS_HUMAN, limit=40)
    assert h.job("job-a").pause_reason is PauseReason.ESTIMATE_EXCEEDS_CONFIRMED


def test_reference_changed_after_confirmation_pauses_before_upload(h: Harness) -> None:
    ref = reference_file(h, "bg11-1", b"original bytes")
    h.add(confirmed_job("job-a", video_request("shot02", refs=(ref,))))
    assert ref.resolved_path is not None
    h.abs(ref.resolved_path).write_bytes(b"edited after confirmation")
    h.run_until(lambda: h.state("job-a") is S.PAUSED_NEEDS_HUMAN, limit=40)
    assert h.job("job-a").pause_reason is PauseReason.INPUTS_CHANGED
    assert ("prepare", "job-a:upload") not in h.web.calls
    assert "bg11-1" in str(h.runtime("job-a")["last_error"])


def test_generating_past_wait_timeout_pauses(h: Harness) -> None:
    h.set_config("wait", "timeout_h", 1)
    h.web.polls_to_finish = 10**6
    web(h, "job-a")
    h.run_until(lambda: h.state("job-a") is S.GENERATING, limit=40)
    h.tick(3601)
    h.run_until(lambda: h.state("job-a") is S.PAUSED_NEEDS_HUMAN, limit=5)
    assert h.job("job-a").pause_reason is PauseReason.WAIT_TIMEOUT


def test_download_retries_then_download_failed_then_api_resume_finishes(h: Harness) -> None:
    web(h, "job-a")
    h.web.download_script["job-a"] = [RuntimeError("download control missing") for _ in range(4)]
    h.run_until(lambda: h.state("job-a") is S.PAUSED_NEEDS_HUMAN, limit=80)
    assert h.web.count("download") == 4 and h.job("job-a").pause_reason is PauseReason.DOWNLOAD_FAILED
    renders = h.abs(f"{SHOTS_REL}/job-a/renders")
    assert not renders.exists() or not any(renders.iterdir())
    h.job_command.resume("job-a", ResumeVia.API)
    h.run_until(lambda: h.state("job-a") is S.DONE, limit=40)
    assert h.web.count("download") == 5


def test_queue_tier_reason_from_backend_pauses_that_queue_toasts_and_yields(h: Harness) -> None:
    web(h, "web-a")
    h.add(confirmed_job("cli-a", image_request("c1-1"), C))
    captcha = PrepareResult(PreparingStep.SET_PARAMS, None, (), PauseReason.CAPTCHA_OR_RISK_POPUP, "出现验证码")
    h.web.prepare_script[("web-a", PreparingStep.SET_PARAMS)] = [captcha]
    h.run_until(lambda: h.queue(W) == ("paused", "captcha_or_risk_popup"), limit=20)
    parked = h.job("web-a")
    assert parked.state is S.QUEUED and parked.blocked_on is BlockedOn.QUEUE_PAUSED
    assert any(toast["title"] == "队列已暂停" and "web" in toast["body"] for toast in h.toasts())
    h.run_until(lambda: h.state("cli-a") is S.DONE, limit=100)
    assert h.queue(C) == ("running", None) and h.web.count("submit") == 0
    h.job_command.mark_queue_running(W)
    h.run_until(lambda: h.state("web-a") is S.DONE, limit=100)


def test_job_level_moderation_reject_fails_only_that_job(h: Harness) -> None:
    web(h, "job-a")
    web(h, "job-b")
    h.web.submit_script["job-a"] = [SubmitOutcome(None, PauseReason.MODERATION_REJECT, "内容违规")]
    h.run_until(lambda: h.state("job-b") is S.DONE, limit=200)
    failed = h.job("job-a")
    assert failed.state is S.FAILED and failed.failure_reason is PauseReason.MODERATION_REJECT
    assert h.queue(W) == ("running", None)


def test_cancel_during_preparing_takes_effect_at_the_next_checkpoint(tmp_path: Path) -> None:
    h = make_harness(tmp_path, manual=True)
    web(h, "job-a")
    for _ in range(10):
        h.tick()
        if h.state("job-a") is S.PREPARING:
            break
        h.executor.run_pending()
    cancelled = h.job_command.cancel("job-a")
    assert cancelled.state == "cancelled" and not cancelled.credits_spent
    for _ in range(5):
        h.executor.run_pending()
        h.tick()
    assert [call for call in h.web.calls if call[0] == "prepare"] == [("prepare", "job-a:set_params")]
    h.client.close()


def test_cancel_while_submitting_waits_for_the_click_result(h: Harness) -> None:
    web(h, "job-a")
    replies: list[object] = []
    h.web.on_submit = lambda job_id: replies.append(h.job_command.cancel(job_id))
    h.run_until(lambda: h.state("job-a") is S.CANCELLED, limit=40)
    reply = replies[0]
    assert getattr(reply, "state") == "submitting" and getattr(reply, "cancel_requested") is True
    assert "积分不会退还" in str(getattr(reply, "message"))
    assert h.job("job-a").credits_spent and h.web.count("poll") == 0


def test_cancel_intent_with_a_rejected_click_cancels_without_spend(h: Harness) -> None:
    web(h, "job-a")
    h.web.on_submit = lambda job_id: h.job_command.cancel(job_id) and None
    h.web.submit_script["job-a"] = [SubmitOutcome(None, PauseReason.SUBMIT_REJECTED, "平台拒绝")]
    h.run_until(lambda: h.state("job-a") is S.CANCELLED, limit=40)
    assert not h.job("job-a").credits_spent


def test_cancel_generating_stops_polling(h: Harness) -> None:
    h.web.polls_to_finish = 10**6
    web(h, "job-a")
    h.run_until(lambda: h.state("job-a") is S.GENERATING, limit=40)
    h.run(12)
    polls = h.web.count("poll")
    reply = h.job_command.cancel("job-a")
    assert reply.credits_spent and "积分不会退还" in str(reply.message)
    h.run(30)
    assert h.web.count("poll") == polls


def test_step_exception_retries_per_config_then_step_failed(h: Harness) -> None:
    h.set_config("retries", "upload", 2)
    web(h, "job-a")
    h.web.prepare_script[("job-a", PreparingStep.UPLOAD)] = [RuntimeError("file chooser detached") for _ in range(3)]
    h.run_until(lambda: h.state("job-a") is S.PAUSED_NEEDS_HUMAN, limit=40)
    assert h.web.calls.count(("prepare", "job-a:upload")) == 3
    assert h.job("job-a").pause_reason is PauseReason.STEP_FAILED


def test_cli_multi_image_job_uses_download_all_and_numbered_candidates(h: Harness) -> None:
    h.add(confirmed_job("cli-a", image_request("c1-1", count=2), C))
    h.run_until(lambda: h.state("cli-a") is S.DONE, limit=60)
    outputs = h.runtime("cli-a")["outputs"]
    assert isinstance(outputs, list) and [Path(p).name[-6:] for p in outputs] == ["_1.png", "_2.png"]
    assert all(p.startswith(f"{CARD_REL}/_candidates/c1-1/20260913-") for p in outputs)
    assert ("download_all", "cli-a") in h.cli.calls and h.cli.count("download") == 0
    assert [call for call in h.cli.calls if call[0] == "prepare"] == [("prepare", "cli-a:verify")]
    dao = JobReader(h.client).get("cli-a")
    assert dao is not None and dao.credits_charged == 4


def test_cli_error_while_submitting_requires_ui_adjudication(h: Harness) -> None:
    h.add(confirmed_job("cli-a", image_request("c1-1"), C))
    h.cli.submit_script["cli-a"] = [SubmitOutcome(None, PauseReason.CLI_ERROR, "exit 1")]
    h.run_until(lambda: h.state("cli-a") is S.PAUSED_NEEDS_HUMAN, limit=40)
    assert h.job("cli-a").pause_reason is PauseReason.CLI_ERROR and h.job("cli-a").requires_adjudication
    with pytest.raises(AdjudicationRequiredError):
        h.job_command.resume("cli-a", ResumeVia.API)


def test_pre_click_not_now_holds_without_clicking_then_submits_once(tmp_path: Path) -> None:
    h = make_harness(tmp_path, pre_click=True)
    web(h, "job-a")
    assert isinstance(h.web, FakeWebBackend)
    h.web.pre_click_script = [SubmitOutcome(None, None, "not_now:concurrency_limit_pre_click"), None]
    h.run_until(lambda: h.state("job-a") is S.DONE, limit=80)
    assert h.web.count("check_before_submit") == 2 and h.web.count("submit") == 1
    assert ("prepare", "job-a:verify") not in h.web.calls
    h.client.close()


def test_failed_health_pauses_the_queue_and_toasts(h: Harness) -> None:
    h.web.health_script = [BackendHealth(False, ("login",), None, PauseReason.LOGIN_EXPIRED)]
    web(h, "job-a")
    h.run(5)
    assert h.queue(W) == ("paused", "login_expired") and h.web.count("prepare") == 0
    assert any(toast["title"] == "队列已暂停" for toast in h.toasts())


def test_sidecar_carries_frozen_negative_prompt_and_reported_sent_flag(h: Harness) -> None:
    web(h, "job-a", negative="低质量，模糊")
    h.web.prepare_script[("job-a", PreparingStep.FILL)] = [
        PrepareResultWithNegative(reached_step=PreparingStep.FILL, page_estimated_credits=None, screenshot_names=(), negative_prompt_sent=True)
    ]
    h.run_until(lambda: h.state("job-a") is S.DONE, limit=80)
    outputs = h.runtime("job-a")["outputs"]
    assert isinstance(outputs, list)
    sidecar = json.loads(h.abs(outputs[0] + ".jimeng.json").read_text(encoding="utf-8"))
    assert sidecar["negative_prompt_sha256"] == hashlib.sha256("低质量，模糊".encode()).hexdigest()
    assert sidecar["negative_prompt_sent"] is True


def test_duration_mismatch_counts_as_download_failure(h: Harness) -> None:
    h.prober.duration_s = 4.0
    h.set_config("retries", "download", 1)
    web(h, "job-a")
    h.run_until(lambda: h.state("job-a") is S.PAUSED_NEEDS_HUMAN, limit=60)
    assert h.job("job-a").pause_reason is PauseReason.DOWNLOAD_FAILED and h.web.count("download") == 2
    assert "时长" in str(h.runtime("job-a")["last_error"])


def test_unconfirmed_jobs_are_never_prepared(h: Harness) -> None:
    from libs.domain.entities.generation_job__entity import GenerationJobEntity
    from libs.domain.value_objects.fingerprint__valueobject import Fingerprint

    request = video_request("shot09")
    h.add(GenerationJobEntity("raw", "batch-9", W, request, Fingerprint.of(request)))
    h.run(30)
    assert h.web.count("prepare") == 0 and h.web.count("submit") == 0 and h.state("raw") is S.QUEUED


def test_tick_reports_dispatched_work(h: Harness) -> None:
    first = h.tick()
    assert set(first.dispatched) == {"health:web", "health:cli"}
    web(h, "job-a")
    second = h.tick()
    assert second.applied == 2 and "job:job-a:step:set_params" in second.dispatched
    h.clock.advance(timedelta(seconds=1))
