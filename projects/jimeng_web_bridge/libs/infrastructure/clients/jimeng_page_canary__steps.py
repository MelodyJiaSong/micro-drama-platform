"""Read-only canary (FR-27): login marker, every composer control, editor, upload entry, generate button,
estimate text, and a recently observed status response that parses. Never clicks anything."""
from __future__ import annotations

import asyncio
import time

from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from libs.infrastructure.clients.jimeng_browser__client import BrowserSession
from libs.infrastructure.clients.jimeng_page__map import CANARY_STEPS
from libs.infrastructure.clients.jimeng_page__steps import detect_blocker, ensure_generate_page, is_visible, locate, require
from libs.infrastructure.daos.jimeng_history__dao import ParseOutcome
from libs.infrastructure.daos.jimeng_page__dao import CanaryCheckDao, CanaryReportDao
from libs.infrastructure.errors.jimeng_browser__error import PageStepError
from libs.infrastructure.readers.jimeng_history__reader import STATUS_KEYS, JimengHistoryReader

STATUS_CHECK: str = "status_response"


async def run_canary(session: BrowserSession, reader: JimengHistoryReader, status_fresh_s: float) -> CanaryReportDao:
    await ensure_generate_page(session)
    try:
        await require(session, "composer_region", timeout_s=session.timeouts.page_ready_s)
        await locate(session, "editor").first.wait_for(state="visible", timeout=session.timeouts.readback_s * 1000)
    except (PageStepError, PlaywrightTimeoutError):
        pass
    blocker = await detect_blocker(session)
    checks = [
        CanaryCheckDao(step, ok, "" if ok else "not visible")
        for step, ok in [(step, await is_visible(locate(session, step))) for step in CANARY_STEPS]
    ]
    checks.append(await _status_check(session, reader, status_fresh_s))
    return CanaryReportDao(checks=tuple(checks), blocker=None if blocker is None else blocker.value)


async def _status_check(session: BrowserSession, reader: JimengHistoryReader, fresh_s: float) -> CanaryCheckDao:
    deadline = time.monotonic() + fresh_s
    while True:
        latest = max(
            (item for key in STATUS_KEYS for item in session.observations(key)),
            key=lambda item: item.seq,
            default=None,
        )
        if latest is not None and time.monotonic() - latest.observed_at <= fresh_s:
            outcome = reader.status_body(latest.key, latest.body).outcome
            return CanaryCheckDao(STATUS_CHECK, outcome is ParseOutcome.OK, f"{latest.key}: {outcome.value}")
        if time.monotonic() > deadline:
            return CanaryCheckDao(STATUS_CHECK, False, "no status response observed recently")
        await asyncio.sleep(0.2)
