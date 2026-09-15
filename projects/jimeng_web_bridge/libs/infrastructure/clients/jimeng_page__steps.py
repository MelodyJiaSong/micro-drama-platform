"""Shared locator resolution, blocker detection and page guards used by every `jimeng_page_*__steps` module."""
from __future__ import annotations

import asyncio
import re
import time
from urllib.parse import urlsplit, urlunsplit

from playwright.async_api import Error as PlaywrightError
from playwright.async_api import Locator, Page
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from libs.infrastructure.clients.jimeng_browser__client import BrowserSession
from libs.infrastructure.clients.jimeng_page__map import SKELETON_CREATION_TYPE, LocatorStrategy
from libs.infrastructure.errors.jimeng_browser__error import PageStepError, StepFailureKind

BLOCKERS: tuple[tuple[str, StepFailureKind], ...] = (
    ("captcha_or_risk_popup", StepFailureKind.CAPTCHA_OR_RISK),
    ("login_expired_notice", StepFailureKind.LOGIN_REQUIRED),
    ("login_button", StepFailureKind.LOGIN_REQUIRED),
    ("insufficient_credit_notice", StepFailureKind.INSUFFICIENT_CREDIT),
)
_NAMED_BY_TEXT: frozenset[str] = frozenset({"option", "listitem"})


def ms(seconds: float) -> float:
    return seconds * 1000


def locate(session: BrowserSession, step: str, root: Locator | None = None) -> Locator:
    entry = session.page_map.get(step)
    base: Page | Locator
    if root is not None:
        base = root
    elif entry.within is not None:
        base = locate(session, entry.within)
    else:
        base = session.page
    if entry.strategy is LocatorStrategy.ROLE:
        role = entry.role or ""
        if entry.pattern is not None:
            locator = base.get_by_role(role, name=re.compile(entry.pattern))  # type: ignore[arg-type]
        elif entry.name is not None:
            locator = base.get_by_role(role, name=entry.name, exact=True)  # type: ignore[arg-type]
        else:
            locator = base.get_by_role(role)  # type: ignore[arg-type]
    elif entry.strategy is LocatorStrategy.TEXT:
        locator = base.get_by_text(re.compile(entry.pattern)) if entry.pattern else base.get_by_text(entry.name or "", exact=True)
    elif entry.strategy is LocatorStrategy.LABEL:
        locator = base.get_by_label(entry.name or "", exact=True)
    elif entry.strategy is LocatorStrategy.TITLE:
        locator = base.get_by_title(entry.name or "", exact=True)
    elif entry.strategy is LocatorStrategy.CSS:
        locator = base.locator(entry.css or "").locator("visible=true")
    else:
        raise ValueError(f"{step} is not a DOM locator ({entry.strategy})")
    if entry.has_text is not None:
        locator = locator.filter(has_text=re.compile(entry.has_text))
    return locator


def named(session: BrowserSession, step: str, name: str, root: Locator | None = None) -> Locator:
    """The `step` element whose name is exactly `name` (exact child text for options and list items)."""
    entry = session.page_map.get(step)
    if entry.strategy is LocatorStrategy.ROLE and entry.role not in _NAMED_BY_TEXT:
        base: Page | Locator = root if root is not None else (
            locate(session, entry.within) if entry.within is not None else session.page
        )
        return base.get_by_role(entry.role or "", name=name, exact=True)  # type: ignore[arg-type]
    return locate(session, step, root).filter(has=session.page.get_by_text(name, exact=True))


async def is_visible(locator: Locator) -> bool:
    try:
        return await locator.first.is_visible()
    except PlaywrightError:
        return False


async def require(
    session: BrowserSession,
    step: str,
    root: Locator | None = None,
    timeout_s: float | None = None,
    locator: Locator | None = None,
) -> Locator:
    target = (locator if locator is not None else locate(session, step, root)).first
    try:
        await target.wait_for(state="visible", timeout=ms(timeout_s or session.timeouts.action_s))
    except PlaywrightTimeoutError as error:
        raise PageStepError(StepFailureKind.SELECTOR_MISSING, step, "not visible") from error
    return target


async def press_keys(session: BrowserSession, step: str) -> None:
    for key in session.page_map.get(step).keys:
        await session.page.keyboard.press(key)


async def detect_blocker(session: BrowserSession) -> StepFailureKind | None:
    for step, kind in BLOCKERS:
        if await is_visible(locate(session, step)):
            return kind
    return None


async def guard(session: BrowserSession, step: str) -> None:
    kind = await detect_blocker(session)
    if kind is not None:
        raise PageStepError(kind, step, "blocking page UI is showing")


def page_url(session: BrowserSession, path_step: str) -> str:
    parts = urlsplit(session.settings.start_url)
    return urlunsplit((parts.scheme, parts.netloc, session.page_map.get(path_step).name or "/", "", ""))


def on_page(session: BrowserSession, path_step: str) -> bool:
    return urlsplit(session.page.url).path == session.page_map.get(path_step).name


async def ensure_generate_page(session: BrowserSession) -> None:
    if not on_page(session, "generate_page"):
        await session.page.goto(session.settings.start_url, wait_until="domcontentloaded", timeout=ms(session.timeouts.page_ready_s))


async def wait_composer_ready(session: BrowserSession) -> None:
    await ensure_generate_page(session)
    await require(session, "editor", timeout_s=session.timeouts.page_ready_s)
    button = await require(session, "creation_type.readback", timeout_s=session.timeouts.page_ready_s)
    deadline = time.monotonic() + session.timeouts.readback_s
    while (await button.inner_text()).strip() == SKELETON_CREATION_TYPE and time.monotonic() < deadline:
        await asyncio.sleep(0.1)


def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace(chr(0x200B), "")).strip()
