from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BatchDao:
    batch_id: str
    state: str
    idempotency_key: str | None
    content_digest: str
    estimated_credits: int | None
    items_json: str
    token_used: bool
    expires_at: str | None
    confirmed_at: str | None
    confirmer: str | None
    balance_start: int | None
    balance_end: int | None
    created_at: str
    updated_at: str
