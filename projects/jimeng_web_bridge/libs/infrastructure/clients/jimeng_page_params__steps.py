"""Composer reset and parameter setting with read-back (FR-29)."""
from __future__ import annotations

import asyncio
import time

from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from libs.infrastructure.clients.jimeng_browser__client import BrowserSession
from libs.infrastructure.clients.jimeng_page__map import DURATION_READBACK, RATIO_READBACK
from libs.infrastructure.clients.jimeng_page__steps import (
    guard,
    is_visible,
    locate,
    ms,
    named,
    press_keys,
    require,
    wait_composer_ready,
)
from libs.infrastructure.clients.jimeng_page_fill__steps import clear_editor
from libs.infrastructure.daos.jimeng_page__dao import ComposerParamsDao, ParamsReadbackDao
from libs.infrastructure.errors.jimeng_browser__error import PageStepError, StepFailureKind

MAX_TILES_REMOVED: int = 60


async def reset_composer(session: BrowserSession) -> None:
    await wait_composer_ready(session)
    await guard(session, "composer_region")
    await press_keys(session, "popover_close")
    tiles = locate(session, "upload_tile")
    for _ in range(MAX_TILES_REMOVED):
        if await tiles.count() == 0:
            break
        await locate(session, "upload_tile_remove", root=tiles.first).first.click(timeout=ms(session.timeouts.action_s))
    await clear_editor(session)
    negative = locate(session, "negative_field")
    if await is_visible(negative):
        await negative.first.fill("")


async def set_params(session: BrowserSession, params: ComposerParamsDao) -> ParamsReadbackDao:
    """Sets every control, then returns what the page displays; the caller compares with `params_diff`."""
    await wait_composer_ready(session)
    await guard(session, "creation_type.open")
    await _choose(session, "creation_type", params.creation_type)
    await _choose(session, "model", params.model)
    await _choose(session, "reference_mode", params.reference_mode)
    await _open(session, "ratio")
    for control, value in (("ratio", params.ratio), ("resolution", params.resolution), ("count", str(params.count))):
        await _click(session, f"{control}.set", named(session, f"{control}.set", value))
    await press_keys(session, "popover_close")
    if params.duration_s is not None:
        await _open(session, "duration")
        spin = await require(session, "duration.set")
        await spin.fill(str(params.duration_s), timeout=ms(session.timeouts.action_s))
        await press_keys(session, "popover_close")
    return await wait_readback(session, params)


async def wait_readback(session: BrowserSession, params: ComposerParamsDao) -> ParamsReadbackDao:
    deadline = time.monotonic() + session.timeouts.readback_s
    while True:
        readback = await read_params(session)
        if not params_diff(params, readback) or time.monotonic() > deadline:
            return readback
        await asyncio.sleep(0.1)


async def read_params(session: BrowserSession) -> ParamsReadbackDao:
    ratio_text = await _text(session, "ratio.readback") or ""
    ratio = RATIO_READBACK.search(ratio_text)
    duration = DURATION_READBACK.search(await _text(session, "duration.readback") or "")
    return ParamsReadbackDao(
        creation_type=await _text(session, "creation_type.readback"),
        model=await _text(session, "model.readback"),
        reference_mode=await _text(session, "reference_mode.readback"),
        ratio=ratio.group(1) if ratio else None,
        resolution=ratio.group(2) if ratio else None,
        count=int(ratio.group(3)) if ratio else None,
        duration_s=int(duration.group(1)) if duration else None,
    )


def params_diff(expected: ComposerParamsDao, actual: ParamsReadbackDao) -> tuple[str, ...]:
    pairs: list[tuple[str, object, object]] = [
        ("创作类型", expected.creation_type, actual.creation_type),
        ("模型", expected.model, actual.model),
        ("参考模式", expected.reference_mode, actual.reference_mode),
        ("比例", expected.ratio, actual.ratio),
        ("分辨率", expected.resolution, actual.resolution),
        ("数量", expected.count, actual.count),
    ]
    if expected.duration_s is not None:
        pairs.append(("时长", expected.duration_s, actual.duration_s))
    return tuple(f"{label}：期望 {want!r}，页面显示 {got!r}" for label, want, got in pairs if want != got)


async def _open(session: BrowserSession, control: str) -> None:
    await guard(session, f"{control}.open")
    opener = await require(session, f"{control}.open")
    await opener.click(timeout=ms(session.timeouts.action_s))
    await require(session, f"{control}.menu")


async def _choose(session: BrowserSession, control: str, value: str) -> None:
    await _open(session, control)
    await _click(session, f"{control}.set", named(session, f"{control}.set", value))


async def _click(session: BrowserSession, step: str, target: object) -> None:
    locator = getattr(target, "first")
    try:
        await locator.click(timeout=ms(session.timeouts.action_s))
    except PlaywrightTimeoutError as error:
        await press_keys(session, "popover_close")
        raise PageStepError(StepFailureKind.SELECTOR_MISSING, step, "option not found or not clickable") from error


async def _text(session: BrowserSession, step: str) -> str | None:
    try:
        return (await locate(session, step).first.inner_text(timeout=ms(session.timeouts.readback_s))).strip()
    except PlaywrightTimeoutError:
        return None
