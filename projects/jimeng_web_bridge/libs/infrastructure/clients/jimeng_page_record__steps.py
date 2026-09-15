"""History-view reload (a navigation, never a forged request), result download via the card's own 下载 icon,
and the 详细信息 credits read (FR-34, FR-35)."""
from __future__ import annotations

import asyncio
import time
from pathlib import Path

from playwright.async_api import Error as PlaywrightError
from playwright.async_api import Locator
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from libs.infrastructure.clients.jimeng_browser__client import BrowserSession
from libs.infrastructure.clients.jimeng_page__map import DETAILS_CREDITS
from libs.infrastructure.clients.jimeng_page__steps import (
    ensure_generate_page,
    guard,
    locate,
    ms,
    on_page,
    require,
)
from libs.infrastructure.daos.jimeng_page__dao import DownloadCaptureDao
from libs.infrastructure.errors.jimeng_browser__error import PageStepError, StepFailureKind

HOVER_ATTEMPTS: int = 3
DETAILS_WAIT_S: float = 2.0


async def reload_history_view(session: BrowserSession) -> None:
    if on_page(session, "generate_page"):
        await session.page.reload(wait_until="domcontentloaded", timeout=ms(session.timeouts.page_ready_s))
    else:
        await ensure_generate_page(session)


async def download_record(session: BrowserSession, prompt_prefix: str, target: Path) -> DownloadCaptureDao:
    await ensure_generate_page(session)
    await guard(session, "record_download_control")
    record = await _finished_record(session, prompt_prefix)
    target.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(HOVER_ATTEMPTS):
        try:
            await record.scroll_into_view_if_needed(timeout=ms(session.timeouts.action_s))
            await locate(session, "record_media", root=record).first.hover(timeout=ms(session.timeouts.action_s))
            control = locate(session, "record_download_control", root=record).first
            async with session.page.expect_download(timeout=ms(session.timeouts.download_s)) as download_info:
                await control.click(timeout=ms(2))
            break
        except PlaywrightTimeoutError as error:
            if attempt == HOVER_ATTEMPTS - 1:
                raise PageStepError(StepFailureKind.DOWNLOAD_FAILED, "record_download_control", "download did not start") from error
    download = await download_info.value
    failure = await download.failure()
    if failure is not None:
        raise PageStepError(StepFailureKind.DOWNLOAD_FAILED, "download", failure)
    await download.save_as(str(target))
    credits = await read_record_credits(session, record)
    return DownloadCaptureDao(path=target, suggested_filename=download.suggested_filename, credits_charged=credits)


async def read_record_credits(session: BrowserSession, record: Locator) -> int | None:
    trigger = locate(session, "record_details_trigger", root=record)
    if await trigger.count() == 0:
        return None
    try:
        await trigger.first.hover(timeout=ms(session.timeouts.action_s))
        tip = locate(session, "record_details_credits").first
        await tip.wait_for(state="visible", timeout=ms(DETAILS_WAIT_S))
        match = DETAILS_CREDITS.search(await tip.inner_text())
        await locate(session, "composer_region").first.hover(timeout=ms(session.timeouts.action_s))
    except PlaywrightError:
        return None
    return int(match.group(1)) if match else None


async def _finished_record(session: BrowserSession, prompt_prefix: str) -> Locator:
    records = locate(session, "history_record_by_prompt_prefix").filter(has_text=prompt_prefix)
    await require(session, "history_list", timeout_s=session.timeouts.page_ready_s)
    deadline = time.monotonic() + session.timeouts.response_wait_s
    while True:
        count = await records.count()
        if count and await locate(session, "record_media", root=records.last).count():
            return records.last
        if time.monotonic() > deadline:
            detail = "no record with this prompt prefix" if count == 0 else "record has no finished video"
            raise PageStepError(StepFailureKind.RECORD_NOT_FOUND, "history_record_by_prompt_prefix", detail)
        await asyncio.sleep(0.2)
