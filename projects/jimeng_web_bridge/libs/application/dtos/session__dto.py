from __future__ import annotations

from dataclasses import dataclass

from libs.application.dtos.job__dto import QueueStateCdto


@dataclass(frozen=True)
class HealthQdto:
    ok: bool


@dataclass(frozen=True)
class CanaryCheckQdto:
    name: str
    ok: bool
    detail: str | None


@dataclass(frozen=True)
class WebSessionQdto:
    """Last known web session facts; `login_state`: logged_in | logged_out | unknown. Never probes inside a request."""

    login_state: str
    browser_open: bool
    web_version: str | None
    checked_at: str | None
    canary_operation_id: str | None
    canary_state: str | None
    canary_ok: bool | None
    canary_checks: tuple[CanaryCheckQdto, ...]


@dataclass(frozen=True)
class CliSessionQdto:
    configured: bool
    logged_in: bool | None
    version: str | None
    min_version: str
    version_ok: bool | None
    credit_balance: int | None
    checked_at: str | None
    error: str | None


@dataclass(frozen=True)
class SessionStatusQdto:
    web: WebSessionQdto
    cli: CliSessionQdto
    queues: tuple[QueueStateCdto, ...]
    today_confirmed_credits: int
    test_mode: bool


@dataclass(frozen=True)
class BrowserOpenCdto:
    accepted: bool
    message: str | None
