from dataclasses import dataclass

from libs.common.enums import BackendKind


@dataclass(frozen=True)
class ServerSection:
    port: int


@dataclass(frozen=True)
class RoutingSection:
    video: BackendKind

    @property
    def image(self) -> BackendKind:
        return BackendKind.CLI


@dataclass(frozen=True)
class ConcurrencySection:
    max_remote_rendering: int


@dataclass(frozen=True)
class PacingSection:
    min_submit_interval_s: float


@dataclass(frozen=True)
class WaitSection:
    timeout_h: int


@dataclass(frozen=True)
class RetriesSection:
    set_params: int
    upload: int
    download: int
    fill: int


@dataclass(frozen=True)
class ConfirmSection:
    token_ttl_min: int


@dataclass(frozen=True)
class IdempotencySection:
    retention_h: int


@dataclass(frozen=True)
class StatusSection:
    parse_failure_threshold: int


@dataclass(frozen=True)
class EntitiesSection:
    snapshot_stale_h: int


@dataclass(frozen=True)
class DownloadSection:
    duration_tolerance_s: float


@dataclass(frozen=True)
class ApiSection:
    max_call_s: int
    progress_interval_s: int
    page_size_default: int
    page_size_max: int
    max_body_bytes: int
    max_batch_items: int


@dataclass(frozen=True)
class McpSection:
    thumbnail_max_px: int


@dataclass(frozen=True)
class UiSection:
    reference_thumb_max_px: int


@dataclass(frozen=True)
class ArtifactsSection:
    preview_max_bytes: int
    preview_retention_days: int


@dataclass(frozen=True)
class TimeSection:
    timezone: str


@dataclass(frozen=True)
class BrowserSection:
    channel: str
    profile_dir: str
    start_url: str


@dataclass(frozen=True)
class CanarySection:
    interval_min: int


@dataclass(frozen=True)
class CliSection:
    path: str
    min_version: str


@dataclass(frozen=True)
class NotificationsSection:
    toast: bool
