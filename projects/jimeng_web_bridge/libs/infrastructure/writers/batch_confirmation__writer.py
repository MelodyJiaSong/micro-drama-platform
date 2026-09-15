from __future__ import annotations

import sqlite3
from collections.abc import Sequence
from dataclasses import astuple, fields

from libs.infrastructure.clients.sqlite__client import SqliteClient
from libs.infrastructure.daos.batch__dao import BatchDao
from libs.infrastructure.daos.job__dao import JobDao, JobTransitionDao

_BATCH_COLUMNS: tuple[str, ...] = tuple(field.name for field in fields(BatchDao) if field.name != "batch_id")
_CONSUME_TOKEN: str = (
    f"UPDATE batches SET {', '.join(f'{column} = ?' for column in _BATCH_COLUMNS)} "
    "WHERE batch_id = ? AND token_used = 0 AND content_digest = ?"
)
_JOB_COLUMNS: tuple[str, ...] = tuple(field.name for field in fields(JobDao))
_INSERT_JOB: str = f"INSERT INTO jobs ({', '.join(_JOB_COLUMNS)}) VALUES ({', '.join('?' for _ in _JOB_COLUMNS)})"
_INSERT_TRANSITION: str = "INSERT INTO job_transitions (job_id, from_state, to_state, reason, at) VALUES (?, ?, ?, ?, ?)"


class BatchConfirmationWriter:
    """Consumes a batch's single-use token and inserts its jobs in one transaction, so a confirmed batch never exists
    without its jobs. Returns False (and writes nothing) when the token was already used or the stored content differs."""

    def __init__(self, client: SqliteClient) -> None:
        self._client: SqliteClient = client

    def confirm(
        self,
        batch: BatchDao,
        expected_content_digest: str,
        jobs: Sequence[tuple[JobDao, Sequence[JobTransitionDao]]],
    ) -> bool:
        def work(conn: sqlite3.Connection) -> bool:
            values = tuple(_sql(getattr(batch, column)) for column in _BATCH_COLUMNS)
            cursor = conn.execute(_CONSUME_TOKEN, (*values, batch.batch_id, expected_content_digest))
            if cursor.rowcount != 1:
                return False
            for job, transitions in jobs:
                conn.execute(_INSERT_JOB, tuple(_sql(value) for value in astuple(job)))
                conn.executemany(
                    _INSERT_TRANSITION, [(t.job_id, t.from_state, t.to_state, t.reason, t.at) for t in transitions]
                )
            return True

        return self._client.transaction(work)


def _sql(value: object) -> object:
    return int(value) if isinstance(value, bool) else value
