from __future__ import annotations

import sqlite3
from collections.abc import Sequence
from dataclasses import fields

from libs.infrastructure.clients.sqlite__client import SqliteClient
from libs.infrastructure.daos.job__dao import JobDao, JobTransitionDao

_BOOL_COLUMNS: frozenset[str] = frozenset({"confirmed", "cancel_requested", "credits_spent"})
_COLUMNS: tuple[str, ...] = tuple(field.name for field in fields(JobDao))


class JobReader:
    def __init__(self, client: SqliteClient) -> None:
        self._client = client

    def get(self, job_id: str) -> JobDao | None:
        rows = self._client.query(f"SELECT {', '.join(_COLUMNS)} FROM jobs WHERE job_id = ?", (job_id,))
        return _job(rows[0]) if rows else None

    def list(
        self,
        states: Sequence[str] | None,
        batch_id: str | None,
        drama_rel: str | None,
        updated_after: str | None,
        limit: int,
        offset: int,
    ) -> tuple[list[JobDao], int]:
        clauses: list[str] = []
        params: list[object] = []
        if states:
            clauses.append(f"state IN ({', '.join('?' for _ in states)})")
            params.extend(states)
        for column, value in (("batch_id", batch_id), ("drama_rel", drama_rel)):
            if value is not None:
                clauses.append(f"{column} = ?")
                params.append(value)
        if updated_after is not None:
            clauses.append("updated_at > ?")
            params.append(updated_after)
        where = f" WHERE {' AND '.join(clauses)}" if clauses else ""
        total = int(self._client.query(f"SELECT COUNT(*) FROM jobs{where}", params)[0][0])
        rows = self._client.query(
            f"SELECT {', '.join(_COLUMNS)} FROM jobs{where} ORDER BY updated_at DESC, job_id LIMIT ? OFFSET ?",
            [*params, limit, offset],
        )
        return [_job(row) for row in rows], total

    def find_by_fingerprint(self, fingerprint: str) -> list[JobDao]:
        rows = self._client.query(
            f"SELECT {', '.join(_COLUMNS)} FROM jobs WHERE fingerprint = ? ORDER BY created_at", (fingerprint,)
        )
        return [_job(row) for row in rows]

    def count_in_states(self, states: Sequence[str]) -> int:
        if not states:
            return 0
        return int(
            self._client.query(f"SELECT COUNT(*) FROM jobs WHERE state IN ({', '.join('?' for _ in states)})", states)[0][0]
        )

    def transitions(self, job_id: str) -> list[JobTransitionDao]:
        rows = self._client.query(
            "SELECT job_id, from_state, to_state, reason, at FROM job_transitions WHERE job_id = ? ORDER BY id", (job_id,)
        )
        return [JobTransitionDao(row["job_id"], row["from_state"], row["to_state"], row["reason"], row["at"]) for row in rows]


def _job(row: sqlite3.Row) -> JobDao:
    return JobDao(**{name: bool(row[name]) if name in _BOOL_COLUMNS else row[name] for name in _COLUMNS})
