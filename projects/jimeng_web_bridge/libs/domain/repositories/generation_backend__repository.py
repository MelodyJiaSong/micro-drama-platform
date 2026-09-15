from dataclasses import dataclass
from typing import Protocol

from libs.common.enums import BackendKind, PauseReason, PreparingStep, RemoteStatus
from libs.domain.value_objects.frozen_request__valueobject import FrozenRequest


@dataclass(frozen=True)
class BackendHealth:
    ok: bool
    failed_checks: tuple[str, ...]
    version: str | None
    pause_reason: PauseReason | None = None


@dataclass(frozen=True)
class PrepareResult:
    reached_step: PreparingStep
    page_estimated_credits: int | None
    screenshot_names: tuple[str, ...]
    pause_reason: PauseReason | None = None
    message: str | None = None


@dataclass(frozen=True)
class SubmitOutcome:
    platform_task_id: str | None
    rejection: PauseReason | None = None
    message: str | None = None

    @property
    def accepted(self) -> bool:
        return self.platform_task_id is not None


@dataclass(frozen=True)
class PollResult:
    status: RemoteStatus
    progress_pct: int | None
    failure: PauseReason | None = None
    message: str | None = None


@dataclass(frozen=True)
class DownloadedFile:
    temp_path: str
    size: int
    sha256: str
    credits_charged: int | None = None


class GenerationBackend(Protocol):
    @property
    def kind(self) -> BackendKind: ...

    def health(self) -> BackendHealth: ...

    def prepare(self, job_id: str, request: FrozenRequest, until: PreparingStep) -> PrepareResult: ...

    def submit(self, job_id: str, request: FrozenRequest) -> SubmitOutcome: ...

    def poll(self, platform_task_id: str) -> PollResult: ...

    def download(self, job_id: str, platform_task_id: str) -> DownloadedFile: ...
