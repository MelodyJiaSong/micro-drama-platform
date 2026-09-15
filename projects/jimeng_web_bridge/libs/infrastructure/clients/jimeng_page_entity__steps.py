"""Entity page: open it (its own subject request is observed passively) and drive the 新建主体 form (FR-47, FR-49)."""
from __future__ import annotations

import asyncio
import time
from collections.abc import Sequence
from pathlib import Path

from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from libs.infrastructure.clients.jimeng_browser__client import BrowserSession
from libs.infrastructure.clients.jimeng_page__steps import guard, locate, ms, page_url, require
from libs.infrastructure.errors.jimeng_browser__error import PageStepError, StepFailureKind


async def open_entity_page(session: BrowserSession) -> None:
    await session.page.goto(page_url(session, "entity_page"), wait_until="domcontentloaded",
                            timeout=ms(session.timeouts.page_ready_s))
    await require(session, "entity_list", timeout_s=session.timeouts.page_ready_s)


async def submit_entity_form(session: BrowserSession, name: str, description: str, images: Sequence[Path]) -> None:
    await guard(session, "entity_new_form_open")
    action = ms(session.timeouts.action_s)
    await (await require(session, "entity_new_form_open")).click(timeout=action)
    dialog = await require(session, "entity_new_form_dialog")
    for image in images:
        async with session.page.expect_file_chooser(timeout=action) as chooser_info:
            await (await require(session, "entity_new_form_image_add")).click(timeout=action)
        await (await chooser_info.value).set_files(str(image))
    pending = locate(session, "entity_new_form_image_pending")
    deadline = time.monotonic() + session.timeouts.upload_done_s
    await asyncio.sleep(0.05)
    while await pending.count() > 0:
        if time.monotonic() > deadline:
            raise PageStepError(StepFailureKind.UPLOAD_TIMEOUT, "entity_new_form_image_add", "reference images not uploaded")
        await asyncio.sleep(0.1)
    await (await require(session, "entity_new_form_name")).fill(name, timeout=action)
    await (await require(session, "entity_new_form_description")).fill(description, timeout=action)
    await (await require(session, "entity_new_form_save")).click(timeout=action)
    try:
        await dialog.wait_for(state="hidden", timeout=ms(session.timeouts.response_wait_s))
    except PlaywrightTimeoutError as error:
        raise PageStepError(StepFailureKind.ENTITY_FORM_FAILED, "entity_new_form_save", "form did not close") from error
