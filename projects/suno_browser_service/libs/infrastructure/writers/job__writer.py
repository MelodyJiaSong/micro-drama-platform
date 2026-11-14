import json
import sqlite3

from projects.suno_browser_service.libs.common.errors import ServiceError
from projects.suno_browser_service.libs.infrastructure.clients.database__client import DatabaseClient
from projects.suno_browser_service.libs.infrastructure.daos.job__dao import JobDao


class JobWriter:
    def __init__(self, db: DatabaseClient) -> None:
        self.db = db

    def insert(self, job: JobDao) -> bool:
        try:
            with self.db.connect() as conn:
                conn.execute("INSERT INTO jobs(id,key,fingerprint,status,payload) VALUES(?,?,?,?,?)",
                             (job.id, job.key, job.fingerprint, job.status, json.dumps(job.payload, ensure_ascii=False)))
            return True
        except sqlite3.IntegrityError:
            return False

    def save(self, job: JobDao) -> None:
        with self.db.connect() as conn:
            updated = conn.execute("UPDATE jobs SET status=?,payload=?,version=version+1 WHERE id=? AND version=?",
                                   (job.status, json.dumps(job.payload, ensure_ascii=False), job.id, job.version))
            if updated.rowcount != 1:
                raise ServiceError("job_changed", "任务已被另一操作更新，请重新读取")
