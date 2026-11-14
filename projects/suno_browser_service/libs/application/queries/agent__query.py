from __future__ import annotations

from projects.suno_browser_service.libs.common.generation import GenerationRequest
from projects.suno_browser_service.libs.infrastructure.clients.service__client import ServiceClient


class AgentQuery:
    def __init__(self, client: ServiceClient | None = None) -> None:
        self.client = client or ServiceClient()

    def capabilities(self) -> dict:
        return self.client.request("GET", "/v1/capabilities")

    def plan(self, request: GenerationRequest) -> dict:
        return self.client.request("POST", "/v1/plan", body=request.model_dump(exclude_none=True))

    def get(self, job_id: str) -> dict:
        return self.client.request("GET", self.client.job_path(job_id))

    def list(self) -> list:
        return self.client.request("GET", "/v1/jobs")

    def wait(self, job_id: str, seconds: int = 45) -> dict:
        return self.client.wait(job_id, seconds)
