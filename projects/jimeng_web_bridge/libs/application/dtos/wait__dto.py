from __future__ import annotations

from dataclasses import dataclass

from libs.application.dtos.operation__dto import OperationQdto


@dataclass(frozen=True)
class WaitJobQdto:
    job_id: str
    state: str
    reason: str | None
    blocked_on: str | None
    preparing_step: str | None
    platform_task_id: str | None
    progress_pct: int | None
    updated_at: str


@dataclass(frozen=True)
class StateCountQdto:
    state: str
    count: int


@dataclass(frozen=True)
class WaitSnapshotQdto:
    jobs: tuple[WaitJobQdto, ...]
    counts: tuple[StateCountQdto, ...]
    total_jobs: int
    missing_job_ids: tuple[str, ...]
    operation: OperationQdto | None


@dataclass(frozen=True)
class WaitQdto:
    snapshot: WaitSnapshotQdto
    finished: bool
    suggested_next: str
    waited_s: float
    timeout_s: float
