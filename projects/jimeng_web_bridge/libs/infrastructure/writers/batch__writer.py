from __future__ import annotations

import sqlite3
from dataclasses import astuple, fields

from libs.infrastructure.clients.sqlite__client import SqliteClient
from libs.infrastructure.daos.batch__dao import BatchDao

_COLUMNS: tuple[str, ...] = tuple(field.name for field in fields(BatchDao))
_UPSERT: str = (
    f"INSERT INTO batches ({', '.join(_COLUMNS)}) VALUES ({', '.join('?' for _ in _COLUMNS)}) "
    f"ON CONFLICT(batch_id) DO UPDATE SET {', '.join(f'{c}=excluded.{c}' for c in _COLUMNS if c != 'batch_id')}"
)


class BatchWriter:
    def __init__(self, client: SqliteClient) -> None:
        self._client = client

    def save(self, batch: BatchDao) -> None:
        self._client.transaction(lambda conn: conn.execute(_UPSERT, _row(batch)))

    def save_if_token_unused(self, batch: BatchDao, expected_content_digest: str) -> bool:
        """Compare-and-set for single-use confirmation: only the first confirm of an unchanged batch wins."""

        def work(conn: sqlite3.Connection) -> bool:
            cursor = conn.execute(
                "UPDATE batches SET token_used = 1 WHERE batch_id = ? AND token_used = 0 AND content_digest = ?",
                (batch.batch_id, expected_content_digest),
            )
            if cursor.rowcount != 1:
                return False
            conn.execute(_UPSERT, _row(batch))
            return True

        return self._client.transaction(work)


def _row(batch: BatchDao) -> tuple[object, ...]:
    return tuple(int(value) if isinstance(value, bool) else value for value in astuple(batch))
