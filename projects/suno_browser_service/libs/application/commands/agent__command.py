from __future__ import annotations

from pathlib import Path

from projects.suno_browser_service.libs.common.errors import ServiceError
from projects.suno_browser_service.libs.common.generation import GenerationRequest
from projects.suno_browser_service.libs.infrastructure.clients.service__client import ServiceClient


class AgentCommand:
    def __init__(self, client: ServiceClient | None = None) -> None:
        self.client = client or ServiceClient()

    def upload(self, path: str, rights_confirmed: bool = False) -> dict:
        local = Path(path).expanduser().resolve()
        if not local.is_file():
            raise ServiceError("file_not_found", "本机参考文件不存在", 404)
        with local.open("rb") as file:
            return self.client.request("POST", "/v1/assets", files={"file": (local.name, file)}, data={"rights_confirmed": str(rights_confirmed).lower()})

    def create(self, request: GenerationRequest, idempotency_key: str) -> dict:
        return self.client.request("POST", "/v1/jobs", body=request.model_dump(exclude_none=True), key=idempotency_key)

    def resume(self, job_id: str, song_urls: list[str], recollect: bool = False) -> dict:
        return self.client.request("POST", self.client.job_path(job_id) + "/resume", body={"song_urls": song_urls, "recollect": recollect})

    def cancel(self, job_id: str) -> dict:
        return self.client.request("POST", self.client.job_path(job_id) + "/cancel")

    def download(self, job_id: str, directory: str) -> dict:
        return self.client.download(job_id, directory)
