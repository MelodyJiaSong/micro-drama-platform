from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class InsertionStrategy(StrEnum):
    INSERT_TEXT = "insert_text"
    TYPE = "type"
    EXEC_COMMAND = "exec_command"


class NewlineMode(StrEnum):
    INSERT_TEXT = "insert_text"
    SHIFT_ENTER = "shift_enter"


@dataclass(frozen=True)
class BrowserSettingsDao:
    channel: str
    profile_dir: Path
    start_url: str
    headless: bool
    test_mode: bool
    viewport_width: int = 1366
    viewport_height: int = 900
    launch_timeout_s: float = 60.0
    command_timeout_s: float = 240.0
    executable_path: Path | None = None


@dataclass(frozen=True)
class StepTimeoutsDao:
    action_s: float = 10.0
    readback_s: float = 3.0
    page_ready_s: float = 20.0
    upload_done_s: float = 60.0
    mention_popup_s: float = 5.0
    submit_response_s: float = 20.0
    history_fallback_s: float = 10.0
    download_s: float = 180.0
    response_wait_s: float = 15.0
    insertion: InsertionStrategy = InsertionStrategy.INSERT_TEXT
    newline: NewlineMode = NewlineMode.INSERT_TEXT


@dataclass(frozen=True)
class BrowserInfoDao:
    browser_version: str
    start_url: str


@dataclass(frozen=True)
class ObservedResponseDao:
    seq: int
    key: str
    url: str
    status: int
    body: bytes | None
    error: str | None
    observed_at: float


@dataclass(frozen=True)
class ComposerParamsDao:
    creation_type: str
    model: str
    reference_mode: str
    ratio: str
    resolution: str
    count: int
    duration_s: int | None


@dataclass(frozen=True)
class ParamsReadbackDao:
    creation_type: str | None
    model: str | None
    reference_mode: str | None
    ratio: str | None
    resolution: str | None
    count: int | None
    duration_s: int | None


@dataclass(frozen=True)
class MentionMarkerDao:
    name: str
    label: str
    mention: str


@dataclass(frozen=True)
class FillSegmentDao:
    """Either literal text (`mention is None`) or one mention chip to pick by name."""

    text: str
    mention: str | None = None


@dataclass(frozen=True)
class EditorSnapshotDao:
    text: str
    mentions: tuple[str, ...]


@dataclass(frozen=True)
class UploadItemDao:
    name: str
    path: Path


@dataclass(frozen=True)
class PreviewCaptureDao:
    page_png: bytes
    composer_png: bytes
    estimate_text: str | None
    estimated_credits: int | None


@dataclass(frozen=True)
class PreClickStateDao:
    parallel_notice: bool
    inflight: int | None
    inflight_limit: int | None
    send_enabled: bool


@dataclass(frozen=True)
class SubmitCaptureDao:
    """`clicked` is True as soon as the generate click was dispatched, whatever happened afterwards."""

    clicked: bool
    task_id: str | None
    via: str
    rejection_text: str | None
    login_error: bool
    blocker: str | None


@dataclass(frozen=True)
class DownloadCaptureDao:
    path: Path
    suggested_filename: str
    credits_charged: int | None


@dataclass(frozen=True)
class CanaryCheckDao:
    name: str
    ok: bool
    detail: str


@dataclass(frozen=True)
class CanaryReportDao:
    checks: tuple[CanaryCheckDao, ...]
    blocker: str | None

    @property
    def failed(self) -> tuple[str, ...]:
        return tuple(check.name for check in self.checks if not check.ok)
