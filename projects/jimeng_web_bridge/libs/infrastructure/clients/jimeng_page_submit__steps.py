"""Preview capture, pre-click state, and the single generate click with passive submit capture (FR-32, FR-33)."""
from __future__ import annotations

import asyncio
import time

from playwright.async_api import Error as PlaywrightError

from libs.infrastructure.clients.jimeng_browser__client import BrowserSession
from libs.infrastructure.clients.jimeng_page__map import CREDITS_NUMBER, INFLIGHT_TEXT
from libs.infrastructure.clients.jimeng_page__steps import (
    detect_blocker,
    is_visible,
    locate,
    ms,
    normalize_spaces,
    require,
)
from libs.infrastructure.daos.jimeng_history__dao import ParseOutcome
from libs.infrastructure.daos.jimeng_page__dao import PreClickStateDao, PreviewCaptureDao, SubmitCaptureDao
from libs.infrastructure.readers.jimeng_history__reader import STATUS_KEYS, SUBMIT, JimengHistoryReader

REJECTION_STEPS: tuple[str, ...] = ("parallel_limit_toast", "insufficient_credit_notice", "moderation_notice", "real_face_notice")
BODY_GRACE_S: float = 1.5
CLOCK_SKEW_S: float = 120.0
PRICE_PIECES_JS: str = """(root) => Array.from(root.querySelectorAll('*'))
  .filter((node) => node.children.length === 0)
  .filter((node) => !['S', 'DEL', 'STRIKE'].includes(node.tagName)
    && !getComputedStyle(node).textDecorationLine.includes('line-through'))
  .map((node) => (node.textContent || '').trim())
  .filter((text) => text.length > 0)"""


async def capture_preview(session: BrowserSession) -> PreviewCaptureDao:
    page_png = await session.page.screenshot(type="png", full_page=True)
    region = await require(session, "composer_region")
    composer_png = await region.screenshot(type="png")
    credits = locate(session, "estimated_credits_text")
    if await credits.count() == 0:
        return PreviewCaptureDao(page_png, composer_png, None, None)
    text = (await credits.first.inner_text()).strip()
    pieces = [str(piece) for piece in await credits.first.evaluate(PRICE_PIECES_JS)] or [text]
    current = next((match for match in (CREDITS_NUMBER.search(piece) for piece in pieces) if match), None)
    return PreviewCaptureDao(page_png, composer_png, text, int(current.group(1).replace(",", "")) if current else None)


async def pre_click_state(session: BrowserSession) -> PreClickStateDao:
    badge = locate(session, "inflight_badge")
    inflight = INFLIGHT_TEXT.search(await badge.first.inner_text()) if await is_visible(badge) else None
    button = locate(session, "generate_button")
    enabled = await button.count() > 0 and await button.first.is_enabled()
    return PreClickStateDao(
        parallel_notice=await is_visible(locate(session, "parallel_limit_notice")),
        inflight=int(inflight.group(1)) if inflight else None,
        inflight_limit=int(inflight.group(2)) if inflight else None,
        send_enabled=enabled,
    )


async def click_generate(session: BrowserSession, prompt_prefix: str, reader: JimengHistoryReader) -> SubmitCaptureDao:
    """Clicks generate exactly once. Everything after the dispatch is observation only — no second click."""
    button = await require(session, "generate_button")
    seq_before = session.latest_seq()
    known = _known_record_ids(session, reader)
    toasts_before = {step: await locate(session, step).count() for step in REJECTION_STEPS}
    clicked_at = time.time()
    try:
        await button.click(timeout=ms(session.timeouts.action_s))
    except PlaywrightError as error:
        return SubmitCaptureDao(True, None, "click_error", str(error).splitlines()[0][:200], False, None)
    deadline = time.monotonic() + session.timeouts.submit_response_s
    while time.monotonic() < deadline:
        captured = _from_submit_bodies(session, reader, seq_before)
        if captured is not None:
            return captured
        toast = await _new_toast(session, toasts_before)
        blocker = None if toast is not None else await detect_blocker(session)
        if toast is not None or blocker is not None:
            await asyncio.sleep(BODY_GRACE_S)
            settled = _from_submit_bodies(session, reader, seq_before)
            if settled is not None:
                return settled
            toast = toast or await _new_toast(session, toasts_before)
            if toast is not None:
                return SubmitCaptureDao(True, None, "toast", toast, False, None)
            return SubmitCaptureDao(True, None, "blocker", None, False, None if blocker is None else blocker.value)
        await asyncio.sleep(0.1)
    fallback_deadline = time.monotonic() + session.timeouts.history_fallback_s
    while time.monotonic() < fallback_deadline:
        record_id = _record_from_history(session, reader, seq_before, known, prompt_prefix, clicked_at)
        if record_id is not None:
            return SubmitCaptureDao(True, record_id, "history", None, False, None)
        await asyncio.sleep(0.2)
    return SubmitCaptureDao(True, None, "none", None, False, None)


def _from_submit_bodies(session: BrowserSession, reader: JimengHistoryReader, after: int) -> SubmitCaptureDao | None:
    for observed in session.observations(SUBMIT, after):
        parsed = reader.submit_body(observed.body)
        if parsed.outcome is ParseOutcome.OK:
            return SubmitCaptureDao(True, parsed.task_id, "response", None, False, None)
        if parsed.outcome is ParseOutcome.LOGIN_ERROR:
            return SubmitCaptureDao(True, None, "response", parsed.errmsg, True, None)
        if parsed.outcome is ParseOutcome.ERROR_ENVELOPE:
            return SubmitCaptureDao(True, None, "response", parsed.errmsg, False, None)
    return None


async def _new_toast(session: BrowserSession, before: dict[str, int]) -> str | None:
    for step, count in before.items():
        locator = locate(session, step)
        if await locator.count() > count:
            return (await locator.last.inner_text()).strip()
    return None


def _known_record_ids(session: BrowserSession, reader: JimengHistoryReader) -> set[str]:
    known: set[str] = set()
    for key in STATUS_KEYS:
        for observed in session.observations(key):
            known.update(record.record_id for record in reader.status_body(key, observed.body).records)
    return known


def _record_from_history(
    session: BrowserSession,
    reader: JimengHistoryReader,
    after: int,
    known: set[str],
    prefix: str,
    clicked_at: float,
) -> str | None:
    wanted = normalize_spaces(prefix)
    best: tuple[float, str] | None = None
    for key in STATUS_KEYS:
        for observed in session.observations(key, after):
            for record in reader.status_body(key, observed.body).records:
                if record.record_id in known or record.prompt_text is None:
                    continue
                if not normalize_spaces(record.prompt_text).startswith(wanted):
                    continue
                created = record.created_time if record.created_time is not None else clicked_at
                if created < clicked_at - CLOCK_SKEW_S:
                    continue
                if best is None or created > best[0]:
                    best = (created, record.record_id)
    return None if best is None else best[1]
