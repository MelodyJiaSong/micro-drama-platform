import json

from projects.suno_browser_service.libs.infrastructure.clients.database__client import DatabaseClient
from projects.suno_browser_service.libs.infrastructure.daos.job__dao import JobDao


class JobReader:
    def __init__(self, db: DatabaseClient) -> None:
        self.db = db

    def get(self, job_id: str) -> JobDao | None:
        with self.db.connect() as conn:
            row = conn.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
        return self._decode(row) if row else None

    def by_key(self, key: str) -> JobDao | None:
        with self.db.connect() as conn:
            row = conn.execute("SELECT * FROM jobs WHERE key=?", (key,)).fetchone()
        return self._decode(row) if row else None

    def list(self, status: str | None = None) -> list[JobDao]:
        with self.db.connect() as conn:
            rows = conn.execute("SELECT * FROM jobs WHERE status=? ORDER BY rowid" if status else
                                "SELECT * FROM jobs ORDER BY rowid DESC LIMIT 100", (status,) if status else ()).fetchall()
        return [self._decode(row) for row in rows]

    @staticmethod
    def _decode(row: dict) -> JobDao:
        return JobDao(row["id"], row["key"], row["fingerprint"], row["status"], json.loads(row["payload"]), row["version"])
