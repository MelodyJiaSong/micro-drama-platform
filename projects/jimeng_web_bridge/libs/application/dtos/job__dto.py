from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from libs.domain.repositories.generation_backend__repository import PrepareResult, SubmitOutcome

CREDITS_NOT_REFUNDED: str = "积分不会退还"


@dataclass(frozen=True)
class TransitionQdto:
    from_state: str | None
    to_state: str
    reason: str | None
    at: str


@dataclass(frozen=True)
class JobSummaryQdto:
    job_id: str
    batch_id: str
    kind: str
    backend: str
    source_type: str
    source_path: str | None
    drama_rel: str | None
    output_slot: str
    state: str
    reason: str | None
    blocked_on: str | None
    preparing_step: str | None
    attempt: int
    confirmed: bool
    cancel_requested: bool
    credits_spent: bool
    platform_task_id: str | None
    credits_estimated_static: int | None
    credits_estimated_page: int | None
    credits_charged: int | None
    created_at: str
    updated_at: str


@dataclass(frozen=True)
class JobPageQdto:
    items: tuple[JobSummaryQdto, ...]
    total: int
    page: int
    page_size: int
    cursor: str | None


@dataclass(frozen=True)
class JobRuntimeQdto:
    screenshots: tuple[str, ...]
    outputs: tuple[str, ...]
    progress_pct: int | None
    last_error: str | None
    sidecar_missing: bool


@dataclass(frozen=True)
class AllowedActionQdto:
    action: str
    ui_only: bool


@dataclass(frozen=True)
class JobDetailQdto:
    job: JobSummaryQdto
    transitions: tuple[TransitionQdto, ...]
    pause_reason: str | None
    pause_tier: str | None
    resume_allowance: str | None
    allowed_actions: tuple[AllowedActionQdto, ...]
    runtime: JobRuntimeQdto
    credits_not_refundable: bool


@dataclass(frozen=True)
class JobStateCdto:
    job_id: str
    state: str
    reason: str | None
    attempt: int
    cancel_requested: bool
    credits_spent: bool
    platform_task_id: str | None
    message: str | None


@dataclass(frozen=True)
class QueueStateCdto:
    backend: str
    state: str
    reason: str | None
    updated_at: str


@dataclass(frozen=True)
class RecoveredJobCdto:
    job_id: str
    from_state: str
    to_state: str
    reason: str | None


@dataclass(frozen=True)
class RecoveryCdto:
    recovered: tuple[RecoveredJobCdto, ...]
    resumed_polling: tuple[str, ...]
    resumed_downloads: tuple[str, ...]
    pruned_previews: int


@dataclass(frozen=True)
class TickCdto:
    applied: int
    dispatched: tuple[str, ...]
    paused_jobs: tuple[str, ...]
    failed_jobs: tuple[str, ...]
    done_jobs: tuple[str, ...]
    paused_queues: tuple[str, ...]
    remote_rendering: int


@dataclass(frozen=True)
class StepWorkCdto:
    prepare: PrepareResult | None
    changed_references: tuple[str, ...]


@dataclass(frozen=True)
class SubmitWorkCdto:
    """Result of the verify → persist `submitting` → submit work item.

    `pre_click` is a backend's not-clicked answer before `submitting` was persisted; `submitted` tells whether
    `submitting` was persisted and `backend.submit` was called.
    """

    changed_references: tuple[str, ...]
    prepare: PrepareResult | None
    pre_click: SubmitOutcome | None
    submitted: bool
    outcome: SubmitOutcome | None
    aborted_reason: str | None


@dataclass(frozen=True)
class DownloadPlanCdto:
    target_dir_rel: str
    name_template: str
    name_fields: dict[str, str]
    default_extension: str | None
    count: int
    duration_s: float | None
    ratio: str | None
    duration_tolerance_s: float
    timezone: str
    downloading_at: datetime | None
    sidecar: dict[str, object]


@dataclass(frozen=True)
class DownloadWorkCdto:
    skipped: bool
    outputs: tuple[str, ...]
    sidecars: tuple[str, ...]
    credits_charged: int | None
    sidecar_missing: bool
    note: str | None
