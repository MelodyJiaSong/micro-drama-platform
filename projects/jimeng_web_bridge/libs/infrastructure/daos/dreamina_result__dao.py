from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DreaminaVersionDao:
    version: str
    commit: str | None
    build_time: str | None


@dataclass(frozen=True)
class DreaminaCreditDao:
    total_credit: int
    vip_level: str | None


@dataclass(frozen=True)
class DreaminaSubmitDao:
    submit_id: str
    gen_status: str | None
    raw: dict[str, object]


@dataclass(frozen=True)
class DreaminaTaskDao:
    submit_id: str
    gen_task_type: str | None
    gen_status: str | None
    fail_reason: str | None
    credit_count: int | None
    image_count: int
    video_count: int


@dataclass(frozen=True)
class DreaminaResultDao:
    submit_id: str
    gen_status: str | None
    fail_reason: str | None
    downloaded_files: tuple[Path, ...]
    raw: dict[str, object]
