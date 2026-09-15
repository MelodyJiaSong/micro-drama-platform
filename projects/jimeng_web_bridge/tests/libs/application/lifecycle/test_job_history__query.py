from __future__ import annotations

import json
from collections.abc import Iterator
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

import pytest

from libs.application.errors.lifecycle__error import InvalidQueryFilterError
from libs.application.queries.history__query import HistoryQuery
from libs.application.queries.job__query import JobQuery
from libs.common.clock import FrozenClock
from libs.common.enums import JobState, PauseReason
from libs.domain.value_objects.global_config__valueobject import GlobalConfig
from libs.infrastructure.clients.sqlite__client import SqliteClient
from libs.infrastructure.daos.batch__dao import BatchDao
from libs.infrastructure.daos.job__dao import JobDao, JobTransitionDao
from libs.infrastructure.readers.batch__reader import BatchReader
from libs.infrastructure.readers.job__reader import JobReader
from libs.infrastructure.writers.batch__writer import BatchWriter
from libs.infrastructure.writers.job__writer import JobWriter
from tests.libs.application.lifecycle.fakes import (
    CARD_REL, DRAMA_REL, SHOTS_REL, FakeJobRepository, advance, confirmed_job, video_request,
)
from tests.libs.domain.builders import T0, global_data

S, R = JobState, PauseReason


class Env:
    def __init__(self, tmp_path: Path) -> None:
        self.client = SqliteClient(tmp_path / "bridge.db")
        self.jobs = FakeJobRepository(self.client)
        self.config = global_data()
        provider = lambda: GlobalConfig.from_dict(self.config)  # noqa: E731
        self.job_query = JobQuery(JobReader(self.client), provider)
        self.clock = FrozenClock(datetime(2026, 9, 14, 3, 0, tzinfo=timezone.utc))
        self.history = HistoryQuery(JobReader(self.client), BatchReader(self.client), provider, self.clock)

    def row(self, job_id: str, created_at: str, state: str = "done", slot: str | None = None, source_type: str = "shot",
            static: int | None = 440, charged: int | None = 440, outputs: list[str] | None = None,
            transitions: list[tuple[str, str]] | None = None) -> None:
        dao = JobDao(
            job_id=job_id, batch_id="batch-1", kind="video" if source_type == "shot" else "image", backend="web",
            source_type=source_type, source_path=None, drama_rel=DRAMA_REL,
            output_slot=slot or f"{SHOTS_REL}/{job_id}", state=state, reason=None, blocked_on="none", preparing_step=None,
            fingerprint=f"fp-{job_id}", idempotency_key=None, attempt=1, confirmed=True, cancel_requested=False,
            credits_spent=state == "done", platform_task_id="task", credits_estimated_static=static,
            credits_estimated_page=None, credits_charged=charged, frozen_request_json="{}",
            extra_json=json.dumps({"runtime": {"outputs": outputs or []}}), created_at=created_at, updated_at=created_at,
        )
        moves = [JobTransitionDao(job_id, None if i == 0 else transitions[i - 1][0], to, None, at)
                 for i, (to, at) in enumerate(transitions or [])]
        JobWriter(self.client).save(dao, moves)


@pytest.fixture
def env(tmp_path: Path) -> Iterator[Env]:
    environment = Env(tmp_path)
    yield environment
    environment.client.close()


def test_list_pages_without_transitions_and_clamps_page_size(env: Env) -> None:
    for index in range(3):
        env.jobs.save(confirmed_job(f"job-{index}", video_request(f"shot0{index}")))
    page = env.job_query.list(page_size=2)
    assert (len(page.items), page.total, page.page_size) == (2, 3, 2) and not hasattr(page.items[0], "transitions")
    assert env.job_query.list(page_size=10_000).page_size == 200 and env.job_query.list().page_size == 50
    assert env.job_query.list(states=["done"]).total == 0 and page.cursor is not None
    with pytest.raises(InvalidQueryFilterError):
        env.job_query.list(states=["bogus"])


def test_detail_lists_transitions_reason_and_ui_only_actions(env: Env) -> None:
    submitted = advance(confirmed_job("rej", video_request("shot01")), S.SUBMITTING)
    submitted.pause(R.SUBMIT_REJECTED, T0)
    env.jobs.save(submitted)
    detail = env.job_query.get("rej")
    assert detail is not None and detail.pause_reason == "submit_rejected" and detail.resume_allowance == "ui_only"
    assert [(a.action, a.ui_only) for a in detail.allowed_actions] == [("adjudicate", True)]
    assert [t.to_state for t in detail.transitions] == ["preparing", "submitting", "paused_needs_human"]
    assert env.job_query.get("missing") is None


def test_actions_for_resumable_estimate_and_queued_jobs(env: Env) -> None:
    fill = advance(confirmed_job("fill", video_request("shot02")), S.PREPARING)
    fill.pause(R.FILL_MISMATCH, T0)
    estimate = advance(confirmed_job("est", video_request("shot03")), S.PREPARING)
    estimate.record_page_estimate(900, False, T0)
    for job in (fill, estimate, confirmed_job("queued", video_request("shot04"))):
        env.jobs.save(job)
    actions = {job_id: [(a.action, a.ui_only) for a in env.job_query.get(job_id).allowed_actions]  # type: ignore[union-attr]
               for job_id in ("fill", "est", "queued")}
    assert actions == {
        "fill": [("resume", False), ("cancel", False)],
        "est": [("approve_estimate", True), ("cancel", False)],
        "queued": [("cancel", False), ("steps", False), ("step_submit", True)],
    }


def test_detail_exposes_runtime_facts_and_refund_warning(env: Env) -> None:
    env.jobs.save(advance(confirmed_job("gen", video_request("shot05")), S.GENERATING))
    reader, writer = JobReader(env.client), JobWriter(env.client)
    dao = reader.get("gen")
    assert dao is not None
    facts = {"runtime": {"screenshots": ["preview_page.jpg"], "progress_pct": 40, "last_error": None}}
    writer.save(replace(dao, extra_json=json.dumps(facts)), [])
    detail = env.job_query.get("gen")
    assert detail is not None and detail.runtime.screenshots == ("preview_page.jpg",) and detail.runtime.progress_pct == 40
    assert detail.credits_not_refundable


def test_history_filters_by_shot_subject_and_local_date(env: Env) -> None:
    env.row("shot02", "2026-09-13T15:59:59.000000Z")
    env.row("shot03", "2026-09-13T16:00:00.000000Z")
    candidate = f"{CARD_REL}/_candidates/c1-1/20260913-181500.png"
    env.row("img", "2026-09-13T12:00:00.000000Z", slot=f"{CARD_REL}#c1-1", source_type="asset_image", outputs=[candidate])
    assert [item.job_id for item in env.history.list(shot="shot02").items] == ["shot02"]
    by_subject = env.history.list(subject="c1_砌炉的老人")
    assert [item.job_id for item in by_subject.items] == ["img"] and by_subject.items[0].candidates == (candidate,)
    assert [item.job_id for item in env.history.list(subject="c1-1").items] == ["img"]
    same_day = env.history.list(date_from="2026-09-13", date_to="2026-09-13")
    assert {item.job_id for item in same_day.items} == {"shot02", "img"}
    with pytest.raises(InvalidQueryFilterError):
        env.history.list(date_from="13/09/2026")


def test_history_durations_and_batch_balance(env: Env) -> None:
    env.row("shot02", "2026-09-13T10:00:00.000000Z", transitions=[
        ("preparing", "2026-09-13T10:01:00.000000Z"), ("submitting", "2026-09-13T10:03:00.000000Z"),
        ("generating", "2026-09-13T10:03:01.000000Z"), ("downloading", "2026-09-13T10:10:01.000000Z"),
        ("done", "2026-09-13T10:10:31.000000Z"),
    ])
    BatchWriter(env.client).save(BatchDao("batch-1", "confirmed", None, "d", 440, "[]", True, None, None, None, 5000, 4560, "t", "t"))
    page = env.history.list()
    item = page.items[0]
    assert (item.durations.queue_wait_s, item.durations.prepare_s, item.durations.render_s, item.durations.download_s) == (60.0, 120.0, 420.0, 30.0)
    assert item.finished_at == "2026-09-13T10:10:31.000000Z"
    assert [(b.batch_id, b.balance_start, b.balance_end) for b in page.batches] == [("batch-1", 5000, 4560)]


def test_daily_totals_cut_days_in_the_configured_timezone(env: Env) -> None:
    env.row("late", "2026-09-13T15:59:59.000000Z", static=100, charged=90)
    env.row("midnight", "2026-09-13T16:00:00.000000Z", state="failed", static=200, charged=None)
    totals = env.history.daily_totals(days=2)
    assert totals.timezone == "Asia/Shanghai"
    assert [(d.date, d.jobs, d.jobs_done, d.jobs_failed, d.credits_estimated_static, d.credits_charged) for d in totals.days] == [
        ("2026-09-13", 1, 1, 0, 100, 90), ("2026-09-14", 1, 0, 1, 200, 0),
    ]
    utc = env.history.daily_totals(days=2, timezone="UTC")
    assert [d.jobs for d in utc.days] == [2, 0]
