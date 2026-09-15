from __future__ import annotations

from dataclasses import fields

from libs.infrastructure.clients.sqlite__client import SqliteClient
from libs.infrastructure.daos.batch__dao import BatchDao

_COLUMNS: tuple[str, ...] = tuple(field.name for field in fields(BatchDao))


class BatchReader:
    def __init__(self, client: SqliteClient) -> None:
        self._client = client

    def get(self, batch_id: str) -> BatchDao | None:
        rows = self._client.query(f"SELECT {', '.join(_COLUMNS)} FROM batches WHERE batch_id = ?", (batch_id,))
        if not rows:
            return None
        row = rows[0]
        return BatchDao(**{name: bool(row[name]) if name == "token_used" else row[name] for name in _COLUMNS})

    def find_by_idempotency_key(self, key: str) -> BatchDao | None:
        rows = self._client.query("SELECT batch_id FROM batches WHERE idempotency_key = ?", (key,))
        return self.get(rows[0]["batch_id"]) if rows else None

    def confirmed_credits_between(self, start_iso: str, end_iso: str) -> int:
        rows = self._client.query(
            "SELECT COALESCE(SUM(estimated_credits), 0) FROM batches WHERE confirmed_at >= ? AND confirmed_at < ?",
            (start_iso, end_iso),
        )
        return int(rows[0][0])
