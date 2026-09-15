from __future__ import annotations

import sqlite3
from collections.abc import Sequence

from libs.infrastructure.clients.sqlite__client import SqliteClient
from libs.infrastructure.daos.store_record__dao import EntitySnapshotDao, IdempotencyDao, QueueStateDao


class IdempotencyWriter:
    def __init__(self, client: SqliteClient) -> None:
        self._client = client

    def put_if_absent(self, record: IdempotencyDao) -> IdempotencyDao:
        """Stores the first response for a key; a later call with the same key gets the original back."""

        def work(conn: sqlite3.Connection) -> IdempotencyDao:
            conn.execute(
                "INSERT OR IGNORE INTO idempotency (key, content_sha256, response_json, created_at) VALUES (?, ?, ?, ?)",
                (record.key, record.content_sha256, record.response_json, record.created_at),
            )
            row = conn.execute(
                "SELECT key, content_sha256, response_json, created_at FROM idempotency WHERE key = ?", (record.key,)
            ).fetchone()
            return IdempotencyDao(row["key"], row["content_sha256"], row["response_json"], row["created_at"])

        return self._client.transaction(work)

    def purge_created_before(self, cutoff_iso: str) -> int:
        return self._client.transaction(
            lambda conn: conn.execute("DELETE FROM idempotency WHERE created_at < ?", (cutoff_iso,)).rowcount
        )


class QueueStateWriter:
    def __init__(self, client: SqliteClient) -> None:
        self._client = client

    def set(self, record: QueueStateDao) -> None:
        self._client.transaction(
            lambda conn: conn.execute(
                "INSERT INTO queue_state (backend, state, reason, updated_at) VALUES (?, ?, ?, ?) "
                "ON CONFLICT(backend) DO UPDATE SET state=excluded.state, reason=excluded.reason, updated_at=excluded.updated_at",
                (record.backend, record.state, record.reason, record.updated_at),
            )
        )


class EntitySnapshotWriter:
    def __init__(self, client: SqliteClient) -> None:
        self._client = client

    def replace_all(self, records: Sequence[EntitySnapshotDao], synced_at: str | None = None) -> None:
        """Replace the snapshot; `synced_at` records that a sync happened even when it found no entities."""

        def work(conn: sqlite3.Connection) -> None:
            conn.execute("DELETE FROM entity_snapshot")
            conn.executemany(
                "INSERT INTO entity_snapshot (name, thumbnail_url, modified_at, synced_at) VALUES (?, ?, ?, ?)",
                [(r.name, r.thumbnail_url, r.modified_at, r.synced_at) for r in records],
            )
            stamp = synced_at if synced_at is not None else max((r.synced_at for r in records), default=None)
            if stamp is not None:
                conn.execute(
                    "INSERT INTO meta (key, value) VALUES ('entity_snapshot_synced_at', ?) "
                    "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                    (stamp,),
                )

        self._client.transaction(work)
