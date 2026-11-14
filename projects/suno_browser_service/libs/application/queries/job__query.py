import re
from pathlib import Path

from projects.suno_browser_service.libs.application.dtos.job__dto import JobQdto
from projects.suno_browser_service.libs.application.mappers.job__mapper import JobMapper
from projects.suno_browser_service.libs.common.errors import ServiceError
from projects.suno_browser_service.libs.common.settings import Settings
from projects.suno_browser_service.libs.infrastructure.clients.database__client import DatabaseClient
from projects.suno_browser_service.libs.infrastructure.readers.job__reader import JobReader


class JobQuery:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.reader = JobReader(DatabaseClient(settings.data_dir / "jobs.sqlite3"))

    def get(self, job_id: str) -> JobQdto:
        job = self.reader.get(job_id)
        if not job:
            raise ServiceError("not_found", "任务不存在", 404)
        return JobMapper.dto(job)

    def list(self) -> list[JobQdto]:
        return [JobMapper.dto(job) for job in self.reader.list()]

    def file(self, job_id: str, name: str) -> Path:
        job = self.get(job_id)
        if not re.fullmatch(r"[0-9a-f]{32}", job_id) or not re.fullmatch(r"[0-9a-f-]{36}\.(mp3|wav)", name):
            raise ServiceError("not_found", "文件不存在", 404)
        if name not in {item["name"] for item in job.files}:
            raise ServiceError("not_found", "文件不存在", 404)
        root = self.settings.data_dir.resolve() / "outputs" / job_id
        path = (root / name).resolve()
        if path.parent != root or not path.is_file():
            raise ServiceError("not_found", "文件不存在", 404)
        return path
