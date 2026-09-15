from __future__ import annotations

from dataclasses import fields

from libs.infrastructure.clients.sqlite__client import SqliteClient
from libs.infrastructure.daos.operation__dao import OperationDao

_COLUMNS: tuple[str, ...] = tuple(field.name for field in fields(OperationDao))


class OperationReader:
    def __init__(self, client: SqliteClient) -> None:
        self._client = client

    def get(self, operation_id: str) -> OperationDao | None:
        rows = self._client.query(f"SELECT {', '.join(_COLUMNS)} FROM operations WHERE operation_id = ?", (operation_id,))
        return OperationDao(**{name: rows[0][name] for name in _COLUMNS}) if rows else None

    def in_states(self, states: tuple[str, ...]) -> list[OperationDao]:
        rows = self._client.query(
            f"SELECT {', '.join(_COLUMNS)} FROM operations WHERE state IN ({', '.join('?' for _ in states)}) ORDER BY created_at",
            states,
        )
        return [OperationDao(**{name: row[name] for name in _COLUMNS}) for row in rows]

    def latest(self, kind: str, subject_id: str | None) -> OperationDao | None:
        rows = self._client.query(
            f"SELECT {', '.join(_COLUMNS)} FROM operations WHERE kind = ? AND json_extract(payload_json, '$.subject_id') IS ? "
            "ORDER BY created_at DESC, operation_id DESC LIMIT 1",
            (kind, subject_id),
        )
        return OperationDao(**{name: rows[0][name] for name in _COLUMNS}) if rows else None
