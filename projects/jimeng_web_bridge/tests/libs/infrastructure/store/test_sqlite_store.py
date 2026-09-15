from __future__ import annotations

import threading
import time
from dataclasses import replace
from pathlib import Path

import pytest

from libs.infrastructure.clients.sqlite__client import SCHEMA_VERSION, SqliteClient
from libs.infrastructure.daos.batch__dao import BatchDao
from libs.infrastructure.daos.job__dao import JobDao, JobTransitionDao
from libs.infrastructure.daos.operation__dao import OperationDao
from libs.infrastructure.daos.store_record__dao import EntitySnapshotDao, IdempotencyDao, QueueStateDao
from libs.infrastructure.readers.batch__reader import BatchReader
from libs.infrastructure.readers.job__reader import JobReader
from libs.infrastructure.readers.operation__reader import OperationReader
from libs.infrastructure.readers.store_record__reader import EntitySnapshotReader, IdempotencyReader, QueueStateReader
from libs.infrastructure.writers.batch__writer import BatchWriter
from libs.infrastructure.writers.job__writer import JobWriter
from libs.infrastructure.writers.operation__writer import OperationWriter
from libs.infrastructure.writers.store_record__writer import EntitySnapshotWriter, IdempotencyWriter, QueueStateWriter


def _job(job_id: str, state: str = "queued", **overrides: object) -> JobDao:
    base = JobDao(
        job_id=job_id, batch_id="b1", kind="video", backend="web", source_type="shot",
        source_path="ai_videos/huangye_shenghuo/hy3/5_6_分镜与prompt/shots/shot02/shot02.md",
        drama_rel="ai_videos/huangye_shenghuo/hy3", output_slot="ai_videos/huangye_shenghuo/hy3/5_6_分镜与prompt/shots/shot02",
        state=state, reason=None, blocked_on="slot", preparing_step=None, fingerprint=f"fp-{job_id}",
        idempotency_key=None, attempt=1, confirmed=True, cancel_requested=False, credits_spent=False,
        platform_task_id=None, credits_estimated_static=440, credits_estimated_page=None, credits_charged=None,
        frozen_request_json='{"prompt": "shot02"}', extra_json="{}", created_at="2026-09-13T10:00:00Z",
        updated_at="2026-09-13T10:00:00Z",
    )
    return replace(base, **overrides)


@pytest.fixture()
def client(tmp_path: Path) -> SqliteClient:
    db = SqliteClient(tmp_path / "bridge.db")
    yield db
    db.close()


def test_schema_is_wal_and_versioned(client: SqliteClient) -> None:
    assert str(client.pragma("journal_mode")).lower() == "wal"
    assert client.pragma("user_version") == SCHEMA_VERSION


def test_job_roundtrip_with_transitions_survives_reopen(tmp_path: Path) -> None:
    db = SqliteClient(tmp_path / "bridge.db")
    job = _job("j1", state="submitting", confirmed=True, credits_spent=False)
    JobWriter(db).save(job, [JobTransitionDao("j1", "preparing", "submitting", None, "2026-09-13T10:01:00Z")])
    db.close()
    reopened = SqliteClient(tmp_path / "bridge.db")
    reader = JobReader(reopened)
    assert reader.get("j1") == job
    assert [t.to_state for t in reader.transitions("j1")] == ["submitting"]
    reopened.close()


def test_upsert_updates_and_appends_transitions(client: SqliteClient) -> None:
    writer, reader = JobWriter(client), JobReader(client)
    writer.save(_job("j1"), [JobTransitionDao("j1", None, "queued", None, "t0")])
    writer.save(_job("j1", state="generating", platform_task_id="pt-1", updated_at="2026-09-13T10:05:00Z"),
                [JobTransitionDao("j1", "queued", "generating", None, "t1")])
    job = reader.get("j1")
    assert job is not None and job.state == "generating" and job.platform_task_id == "pt-1"
    assert [t.to_state for t in reader.transitions("j1")] == ["queued", "generating"]


def test_list_filters_paginates_and_counts(client: SqliteClient) -> None:
    writer = JobWriter(client)
    writer.save_all([(_job(f"j{i:02d}", state="done" if i % 2 else "queued", updated_at=f"2026-09-13T10:{i:02d}:00Z"), []) for i in range(10)])
    reader = JobReader(client)
    page, total = reader.list(states=["done"], batch_id="b1", drama_rel=None, updated_after=None, limit=2, offset=0)
    assert total == 5 and [j.job_id for j in page] == ["j09", "j07"]
    newer, newer_total = reader.list(states=None, batch_id=None, drama_rel=None, updated_after="2026-09-13T10:07:00Z", limit=50, offset=0)
    assert newer_total == 2 and {j.job_id for j in newer} == {"j08", "j09"}
    assert reader.count_in_states(["queued", "generating"]) == 5


def test_fingerprint_lookup(client: SqliteClient) -> None:
    JobWriter(client).save_all([(_job("a", fingerprint="same"), []), (_job("b", fingerprint="same", attempt=2), [])])
    assert [j.job_id for j in JobReader(client).find_by_fingerprint("same")] == ["a", "b"]


def test_failed_transaction_rolls_back(client: SqliteClient) -> None:
    bad = _job("j1")
    with pytest.raises(Exception):
        JobWriter(client).save(bad, [JobTransitionDao("j1", None, None, None, "t0")])  # type: ignore[arg-type]
    assert JobReader(client).get("j1") is None


def _batch(**overrides: object) -> BatchDao:
    base = BatchDao(batch_id="b1", state="awaiting_confirm", idempotency_key="k1", content_digest="d1",
                    estimated_credits=440, items_json="[]", token_used=False, expires_at="2026-09-13T10:30:00Z",
                    confirmed_at=None, confirmer=None, balance_start=None, balance_end=None,
                    created_at="2026-09-13T10:00:00Z", updated_at="2026-09-13T10:00:00Z")
    return replace(base, **overrides)


def test_confirmation_token_is_single_use_under_concurrency(client: SqliteClient) -> None:
    writer = BatchWriter(client)
    writer.save(_batch())
    confirmed = _batch(state="confirmed", token_used=True, confirmed_at="2026-09-13T10:02:00Z", confirmer="ui_human")
    results: list[bool] = []
    barrier = threading.Barrier(8)

    def attempt() -> None:
        barrier.wait()
        results.append(writer.save_if_token_unused(confirmed, expected_content_digest="d1"))

    threads = [threading.Thread(target=attempt) for _ in range(8)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert results.count(True) == 1
    batch = BatchReader(client).get("b1")
    assert batch is not None and batch.state == "confirmed" and batch.token_used


def test_changed_content_digest_cannot_confirm(client: SqliteClient) -> None:
    writer = BatchWriter(client)
    writer.save(_batch())
    assert not writer.save_if_token_unused(_batch(state="confirmed", token_used=True), expected_content_digest="other")
    assert BatchReader(client).get("b1") == _batch()


def test_confirmed_credits_window_and_idempotency_lookup(client: SqliteClient) -> None:
    writer = BatchWriter(client)
    writer.save(_batch(batch_id="b1", confirmed_at="2026-09-13T01:00:00Z", estimated_credits=440))
    writer.save(_batch(batch_id="b2", idempotency_key="k2", confirmed_at="2026-09-12T23:00:00Z", estimated_credits=100))
    reader = BatchReader(client)
    assert reader.confirmed_credits_between("2026-09-13T00:00:00Z", "2026-09-14T00:00:00Z") == 440
    found = reader.find_by_idempotency_key("k2")
    assert found is not None and found.batch_id == "b2"


def test_operations_roundtrip(client: SqliteClient) -> None:
    op = OperationDao("op1", "canary", "running", None, "{}", None, None, "t0", "t0")
    OperationWriter(client).save(op)
    OperationWriter(client).save(replace(op, state="succeeded", result_json='{"ok": true}', updated_at="t1"))
    reader = OperationReader(client)
    assert reader.get("op1").state == "succeeded"  # type: ignore[union-attr]
    assert reader.in_states(("running",)) == []


def test_idempotency_keeps_first_response(client: SqliteClient) -> None:
    writer = IdempotencyWriter(client)
    first = writer.put_if_absent(IdempotencyDao("k", "c1", '{"batch_id": "b1"}', "2026-09-13T10:00:00Z"))
    second = writer.put_if_absent(IdempotencyDao("k", "c2", '{"batch_id": "b2"}', "2026-09-13T10:01:00Z"))
    assert first == second and second.content_sha256 == "c1"
    assert writer.purge_created_before("2026-09-14T00:00:00Z") == 1
    assert IdempotencyReader(client).get("k") is None


def test_queue_state_and_entity_snapshot(client: SqliteClient) -> None:
    QueueStateWriter(client).set(QueueStateDao("web", "paused", "captcha_or_risk_popup", "t0"))
    QueueStateWriter(client).set(QueueStateDao("web", "running", None, "t1"))
    assert QueueStateReader(client).all() == [QueueStateDao("web", "running", None, "t1")]
    snapshots = EntitySnapshotWriter(client)
    snapshots.replace_all([EntitySnapshotDao("hy3_主角", None, "2026-09-13", "s1"), EntitySnapshotDao("hy1_主角", None, None, "s1")])
    snapshots.replace_all([EntitySnapshotDao("hy3_主角", None, "2026-09-13", "s2")])
    reader = EntitySnapshotReader(client)
    assert [e.name for e in reader.all()] == ["hy3_主角"] and reader.last_synced_at() == "s2"


def test_list_query_is_fast_at_one_thousand_jobs(client: SqliteClient) -> None:
    JobWriter(client).save_all([(_job(f"j{i:04d}", state=("done", "queued", "generating")[i % 3], updated_at=f"2026-09-13T{i % 24:02d}:{i % 60:02d}:00Z"), []) for i in range(1000)])
    reader = JobReader(client)
    started = time.perf_counter()
    for _ in range(20):
        reader.list(states=["generating"], batch_id=None, drama_rel="ai_videos/huangye_shenghuo/hy3", updated_after=None, limit=50, offset=0)
    assert (time.perf_counter() - started) / 20 < 0.5


def test_empty_sync_still_counts_as_synced(client: SqliteClient) -> None:
    reader = EntitySnapshotReader(client)
    assert reader.last_synced_at() is None
    EntitySnapshotWriter(client).replace_all([], synced_at="2026-09-14T01:00:00.000000Z")
    assert reader.all() == [] and reader.last_synced_at() == "2026-09-14T01:00:00.000000Z"


def test_schema_upgrade_from_v1_adds_meta_table(tmp_path: Path) -> None:
    import sqlite3
    db_path = tmp_path / "old.db"
    legacy = sqlite3.connect(str(db_path))
    legacy.execute("CREATE TABLE entity_snapshot (name TEXT PRIMARY KEY, thumbnail_url TEXT, modified_at TEXT, synced_at TEXT NOT NULL)")
    legacy.execute("INSERT INTO entity_snapshot VALUES ('hy3_主角', NULL, NULL, 's-old')")
    legacy.execute("PRAGMA user_version=1")
    legacy.commit()
    legacy.close()
    upgraded = SqliteClient(db_path)
    assert upgraded.pragma("user_version") == SCHEMA_VERSION
    assert EntitySnapshotReader(upgraded).last_synced_at() == "s-old"
    upgraded.close()
