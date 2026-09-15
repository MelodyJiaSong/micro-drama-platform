from __future__ import annotations

from dataclasses import astuple, fields

from libs.infrastructure.clients.sqlite__client import SqliteClient
from libs.infrastructure.daos.operation__dao import OperationDao

_COLUMNS: tuple[str, ...] = tuple(field.name for field in fields(OperationDao))
_UPSERT: str = (
    f"INSERT INTO operations ({', '.join(_COLUMNS)}) VALUES ({', '.join('?' for _ in _COLUMNS)}) "
    f"ON CONFLICT(operation_id) DO UPDATE SET {', '.join(f'{c}=excluded.{c}' for c in _COLUMNS if c != 'operation_id')}"
)


class OperationWriter:
    def __init__(self, client: SqliteClient) -> None:
        self._client = client

    def save(self, operation: OperationDao) -> None:
        self._client.transaction(lambda conn: conn.execute(_UPSERT, astuple(operation)))
