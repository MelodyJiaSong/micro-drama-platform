from __future__ import annotations

import sqlite3
import threading
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import TypeVar

T = TypeVar("T")

SCHEMA_VERSION: int = 2

_SCHEMA: str = """
CREATE TABLE IF NOT EXISTS jobs (
    job_id TEXT PRIMARY KEY,
    batch_id TEXT NOT NULL,
    kind TEXT NOT NULL,
    backend TEXT NOT NULL,
    source_type TEXT NOT NULL,
    source_path TEXT,
    drama_rel TEXT,
    output_slot TEXT NOT NULL,
    state TEXT NOT NULL,
    reason TEXT,
    blocked_on TEXT,
    preparing_step TEXT,
    fingerprint TEXT NOT NULL,
    idempotency_key TEXT,
    attempt INTEGER NOT NULL,
    confirmed INTEGER NOT NULL,
    cancel_requested INTEGER NOT NULL,
    credits_spent INTEGER NOT NULL,
    platform_task_id TEXT,
    credits_estimated_static INTEGER,
    credits_estimated_page INTEGER,
    credits_charged INTEGER,
    frozen_request_json TEXT,
    extra_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_jobs_state ON jobs(state);
CREATE INDEX IF NOT EXISTS ix_jobs_batch ON jobs(batch_id);
CREATE INDEX IF NOT EXISTS ix_jobs_fingerprint ON jobs(fingerprint);
CREATE INDEX IF NOT EXISTS ix_jobs_drama ON jobs(drama_rel);
CREATE INDEX IF NOT EXISTS ix_jobs_updated ON jobs(updated_at);
CREATE TABLE IF NOT EXISTS job_transitions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id TEXT NOT NULL,
    from_state TEXT,
    to_state TEXT NOT NULL,
    reason TEXT,
    at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_transitions_job ON job_transitions(job_id);
CREATE TABLE IF NOT EXISTS batches (
    batch_id TEXT PRIMARY KEY,
    state TEXT NOT NULL,
    idempotency_key TEXT,
    content_digest TEXT NOT NULL,
    estimated_credits INTEGER,
    items_json TEXT NOT NULL,
    token_used INTEGER NOT NULL,
    expires_at TEXT,
    confirmed_at TEXT,
    confirmer TEXT,
    balance_start INTEGER,
    balance_end INTEGER,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS operations (
    operation_id TEXT PRIMARY KEY,
    kind TEXT NOT NULL,
    state TEXT NOT NULL,
    job_id TEXT,
    payload_json TEXT NOT NULL,
    result_json TEXT,
    error_json TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS idempotency (
    key TEXT PRIMARY KEY,
    content_sha256 TEXT NOT NULL,
    response_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS queue_state (
    backend TEXT PRIMARY KEY,
    state TEXT NOT NULL,
    reason TEXT,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS entity_snapshot (
    name TEXT PRIMARY KEY,
    thumbnail_url TEXT,
    modified_at TEXT,
    synced_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""


class SqliteClient:
    """The service's single SQLite handle (WAL, one writer).

    Every read and write goes through one re-entrant lock: volume is one account's jobs, and a
    single serialised connection is the simplest way to keep `BEGIN IMMEDIATE` transactions and
    compare-and-set updates race-free. Async callers wrap calls in `asyncio.to_thread`.
    """

    def __init__(self, db_path: Path) -> None:
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(db_path), check_same_thread=False, isolation_level=None)
        self._conn.row_factory = sqlite3.Row
        self._lock = threading.RLock()
        with self._lock:
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA busy_timeout=5000")
            self._conn.execute("PRAGMA synchronous=NORMAL")
            self._migrate()

    def transaction(self, work: Callable[[sqlite3.Connection], T]) -> T:
        with self._lock:
            self._conn.execute("BEGIN IMMEDIATE")
            try:
                result = work(self._conn)
            except BaseException:
                self._conn.execute("ROLLBACK")
                raise
            self._conn.execute("COMMIT")
            return result

    def query(self, sql: str, params: Sequence[object] = ()) -> list[sqlite3.Row]:
        with self._lock:
            return self._conn.execute(sql, tuple(params)).fetchall()

    def pragma(self, name: str) -> object:
        with self._lock:
            return self._conn.execute(f"PRAGMA {name}").fetchone()[0]

    def close(self) -> None:
        with self._lock:
            self._conn.close()

    def _migrate(self) -> None:
        version = self._conn.execute("PRAGMA user_version").fetchone()[0]
        if version < SCHEMA_VERSION:
            self._conn.executescript(_SCHEMA)
            self._conn.execute(f"PRAGMA user_version={SCHEMA_VERSION}")
