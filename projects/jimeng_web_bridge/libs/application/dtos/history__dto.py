from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DurationsQdto:
    queue_wait_s: float | None
    prepare_s: float | None
    render_s: float | None
    download_s: float | None


@dataclass(frozen=True)
class HistoryItemQdto:
    job_id: str
    batch_id: str
    kind: str
    backend: str
    state: str
    reason: str | None
    drama_rel: str | None
    shot: str | None
    subject: str | None
    block_key: str | None
    source_path: str | None
    output_slot: str
    attempt: int
    credits_estimated_static: int | None
    credits_estimated_page: int | None
    credits_charged: int | None
    created_at: str
    finished_at: str | None
    durations: DurationsQdto
    outputs: tuple[str, ...]
    candidates: tuple[str, ...]


@dataclass(frozen=True)
class BatchBalanceQdto:
    batch_id: str
    balance_start: int | None
    balance_end: int | None


@dataclass(frozen=True)
class HistoryPageQdto:
    items: tuple[HistoryItemQdto, ...]
    total: int
    page: int
    page_size: int
    batches: tuple[BatchBalanceQdto, ...]


@dataclass(frozen=True)
class DailyTotalQdto:
    date: str
    jobs: int
    jobs_done: int
    jobs_failed: int
    credits_estimated_static: int
    credits_estimated_page: int
    credits_charged: int


@dataclass(frozen=True)
class DailyTotalsQdto:
    timezone: str
    days: tuple[DailyTotalQdto, ...]
