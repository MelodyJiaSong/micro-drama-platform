from __future__ import annotations

from libs.infrastructure.clients.sqlite__client import SqliteClient
from libs.infrastructure.daos.store_record__dao import EntitySnapshotDao, IdempotencyDao, QueueStateDao


class IdempotencyReader:
    def __init__(self, client: SqliteClient) -> None:
        self._client = client

    def get(self, key: str) -> IdempotencyDao | None:
        rows = self._client.query(
            "SELECT key, content_sha256, response_json, created_at FROM idempotency WHERE key = ?", (key,)
        )
        return IdempotencyDao(rows[0]["key"], rows[0]["content_sha256"], rows[0]["response_json"], rows[0]["created_at"]) if rows else None


class QueueStateReader:
    def __init__(self, client: SqliteClient) -> None:
        self._client = client

    def all(self) -> list[QueueStateDao]:
        rows = self._client.query("SELECT backend, state, reason, updated_at FROM queue_state ORDER BY backend")
        return [QueueStateDao(r["backend"], r["state"], r["reason"], r["updated_at"]) for r in rows]


class EntitySnapshotReader:
    def __init__(self, client: SqliteClient) -> None:
        self._client = client

    def all(self) -> list[EntitySnapshotDao]:
        rows = self._client.query("SELECT name, thumbnail_url, modified_at, synced_at FROM entity_snapshot ORDER BY name")
        return [EntitySnapshotDao(r["name"], r["thumbnail_url"], r["modified_at"], r["synced_at"]) for r in rows]

    def last_synced_at(self) -> str | None:
        rows = self._client.query("SELECT value FROM meta WHERE key = 'entity_snapshot_synced_at'")
        if rows:
            return str(rows[0]["value"])
        legacy = self._client.query("SELECT MAX(synced_at) FROM entity_snapshot")
        return legacy[0][0] if legacy else None
