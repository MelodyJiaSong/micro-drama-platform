from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class JobDao:
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
    fingerprint: str
    idempotency_key: str | None
    attempt: int
    confirmed: bool
    cancel_requested: bool
    credits_spent: bool
    platform_task_id: str | None
    credits_estimated_static: int | None
    credits_estimated_page: int | None
    credits_charged: int | None
    frozen_request_json: str | None
    extra_json: str
    created_at: str
    updated_at: str


@dataclass(frozen=True)
class JobTransitionDao:
    job_id: str
    from_state: str | None
    to_state: str
    reason: str | None
    at: str
