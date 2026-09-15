from __future__ import annotations

import sqlite3
from collections.abc import Sequence
from dataclasses import astuple, fields

from libs.infrastructure.clients.sqlite__client import SqliteClient
from libs.infrastructure.daos.job__dao import JobDao, JobTransitionDao

_COLUMNS: tuple[str, ...] = tuple(field.name for field in fields(JobDao))
_UPSERT: str = (
    f"INSERT INTO jobs ({', '.join(_COLUMNS)}) VALUES ({', '.join('?' for _ in _COLUMNS)}) "
    f"ON CONFLICT(job_id) DO UPDATE SET {', '.join(f'{c}=excluded.{c}' for c in _COLUMNS if c != 'job_id')}"
)
_TRANSITION: str = "INSERT INTO job_transitions (job_id, from_state, to_state, reason, at) VALUES (?, ?, ?, ?, ?)"


class JobWriter:
    def __init__(self, client: SqliteClient) -> None:
        self._client = client

    def save(self, job: JobDao, new_transitions: Sequence[JobTransitionDao]) -> None:
        self.save_all([(job, new_transitions)])

    def save_all(self, items: Sequence[tuple[JobDao, Sequence[JobTransitionDao]]]) -> None:
        def work(conn: sqlite3.Connection) -> None:
            for job, transitions in items:
                conn.execute(_UPSERT, _row(job))
                conn.executemany(
                    _TRANSITION, [(t.job_id, t.from_state, t.to_state, t.reason, t.at) for t in transitions]
                )

        self._client.transaction(work)


def _row(job: JobDao) -> tuple[object, ...]:
    return tuple(int(value) if isinstance(value, bool) else value for value in astuple(job))
