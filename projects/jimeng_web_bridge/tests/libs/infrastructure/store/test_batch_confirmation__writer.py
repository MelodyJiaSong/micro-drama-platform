from __future__ import annotations

import sqlite3
import threading
from collections.abc import Iterator
from dataclasses import replace
from pathlib import Path

import pytest

from libs.infrastructure.clients.sqlite__client import SqliteClient
from libs.infrastructure.daos.batch__dao import BatchDao
from libs.infrastructure.daos.job__dao import JobDao, JobTransitionDao
from libs.infrastructure.readers.batch__reader import BatchReader
from libs.infrastructure.readers.job__reader import JobReader
from libs.infrastructure.writers.batch__writer import BatchWriter
from libs.infrastructure.writers.batch_confirmation__writer import BatchConfirmationWriter
from libs.infrastructure.writers.job__writer import JobWriter

AWAITING = BatchDao(
    batch_id="b1", state="awaiting_confirm", idempotency_key=None, content_digest="d1", estimated_credits=440,
    items_json="{}", token_used=False, expires_at="2026-09-13T10:30:00.000000Z", confirmed_at=None, confirmer=None,
    balance_start=None, balance_end=None, created_at="2026-09-13T10:00:00.000000Z", updated_at="2026-09-13T10:00:00.000000Z",
)
CONFIRMED = replace(
    AWAITING, state="confirmed", token_used=True, confirmed_at="2026-09-13T10:05:00.000000Z", confirmer="ui_human",
    updated_at="2026-09-13T10:05:00.000000Z",
)


def _job(job_id: str) -> tuple[JobDao, list[JobTransitionDao]]:
    job = JobDao(
        job_id=job_id, batch_id="b1", kind="video", backend="web", source_type="shot", source_path="ai_videos/d/shot02.md",
        drama_rel="ai_videos/d", output_slot="ai_videos/d/shots/shot02", state="queued", reason=None, blocked_on="none",
        preparing_step=None, fingerprint="f" * 64, idempotency_key=None, attempt=1, confirmed=True,
        cancel_requested=False, credits_spent=False, platform_task_id=None, credits_estimated_static=440,
        credits_estimated_page=None, credits_charged=None, frozen_request_json="{}", extra_json="{}",
        created_at="2026-09-13T10:05:00.000000Z", updated_at="2026-09-13T10:05:00.000000Z",
    )
    return job, [JobTransitionDao(job_id, None, "queued", "created", "2026-09-13T10:05:00.000000Z")]


@pytest.fixture()
def client(tmp_path: Path) -> Iterator[SqliteClient]:
    db = SqliteClient(tmp_path / "bridge.db")
    BatchWriter(db).save(AWAITING)
    yield db
    db.close()


def _job_ids(client: SqliteClient) -> list[str]:
    return [row["job_id"] for row in client.query("SELECT job_id FROM jobs ORDER BY job_id")]


def test_consumes_the_token_and_inserts_jobs_with_first_transitions(client: SqliteClient) -> None:
    assert BatchConfirmationWriter(client).confirm(CONFIRMED, "d1", [_job("j1"), _job("j2")])

    assert BatchReader(client).get("b1") == CONFIRMED
    assert _job_ids(client) == ["j1", "j2"]
    assert JobReader(client).get("j1") == _job("j1")[0]
    assert [(t.from_state, t.to_state) for t in JobReader(client).transitions("j2")] == [(None, "queued")]


@pytest.mark.parametrize(("digest", "prior_confirm"), [("d1", True), ("other-digest", False)])
def test_used_token_or_changed_content_writes_nothing(client: SqliteClient, digest: str, prior_confirm: bool) -> None:
    writer = BatchConfirmationWriter(client)
    if prior_confirm:
        assert writer.confirm(CONFIRMED, "d1", [_job("j1")])

    assert not writer.confirm(CONFIRMED, digest, [_job("j9")])

    assert "j9" not in _job_ids(client)
    stored = BatchReader(client).get("b1")
    assert stored is not None and stored.token_used is prior_confirm


def test_failed_job_insert_rolls_back_the_token_consumption(client: SqliteClient) -> None:
    JobWriter(client).save(*_job("j1"))

    with pytest.raises(sqlite3.IntegrityError):
        BatchConfirmationWriter(client).confirm(CONFIRMED, "d1", [_job("j0"), _job("j1")])

    assert BatchReader(client).get("b1") == AWAITING
    assert _job_ids(client) == ["j1"]


def test_concurrent_confirms_have_exactly_one_winner(client: SqliteClient) -> None:
    writer = BatchConfirmationWriter(client)
    barrier = threading.Barrier(8)
    results: list[bool] = []
    lock = threading.Lock()

    def attempt(index: int) -> None:
        barrier.wait()
        won = writer.confirm(CONFIRMED, "d1", [_job(f"j{index}")])
        with lock:
            results.append(won)

    threads = [threading.Thread(target=attempt, args=(index,)) for index in range(8)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert sorted(results) == [False] * 7 + [True]
    assert len(_job_ids(client)) == 1
