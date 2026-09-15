"""BrowserActor: one persistent Playwright context on a dedicated asyncio loop thread (FR-25, FR-34, FR-37).

UI commands run strictly one at a time. Callers on other threads submit an async command and block on
its result, so the service's own event loop never touches Playwright. Observation is passive only: a
context-level `response` listener copies the bodies of configured URL patterns into bounded buffers the
moment they arrive. Nothing here intercepts, modifies or issues requests on the page's behalf.
"""
from __future__ import annotations

import asyncio
import concurrent.futures
import re
import sys
import threading
import time
from collections import deque
from collections.abc import Awaitable, Callable, Coroutine, Mapping
from pathlib import Path
from typing import Any, TypeVar
from urllib.parse import parse_qs, urlsplit

from playwright.async_api import BrowserContext, Frame, Page, Playwright, Response, async_playwright
from playwright.async_api import Error as PlaywrightError
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from libs.infrastructure.clients.jimeng_page__map import JimengPageMap
from libs.infrastructure.daos.jimeng_page__dao import (
    BrowserInfoDao,
    BrowserSettingsDao,
    ObservedResponseDao,
    StepTimeoutsDao,
)
from libs.infrastructure.errors.jimeng_browser__error import (
    BrowserCommandTimeoutError,
    BrowserLaunchError,
    BrowserLostError,
    BrowserNotStartedError,
    LaunchFailureKind,
    PageStepError,
    StepFailureKind,
)

T = TypeVar("T")
REAL_SITE_PREFIX: str = "https://jimeng.jianying.com/"
LOCAL_HOSTS: frozenset[str] = frozenset({"127.0.0.1", "localhost"})
_CLOSED_MARKERS: tuple[str, ...] = ("has been closed", "Target closed", "Browser closed", "browser has disconnected")
_CHROME_VERSION = re.compile(r"(?:HeadlessChrome|Chrome)/([\d.]+)")


class BrowserSession:
    """What a step sees: the single work page, the registry, timeouts and the observation buffers."""

    def __init__(self, client: JimengBrowserClient, context: BrowserContext, page: Page) -> None:
        self._client = client
        self.context = context
        self.page = page

    @property
    def page_map(self) -> JimengPageMap:
        return self._client.page_map

    @property
    def timeouts(self) -> StepTimeoutsDao:
        return self._client.timeouts

    @property
    def settings(self) -> BrowserSettingsDao:
        return self._client.settings

    def observations(self, key: str, after_seq: int = 0) -> tuple[ObservedResponseDao, ...]:
        return self._client.observations(key, after_seq)

    def latest_seq(self) -> int:
        return self._client.latest_seq()


class JimengBrowserClient:
    def __init__(
        self,
        settings: BrowserSettingsDao,
        page_map: JimengPageMap,
        timeouts: StepTimeoutsDao,
        observe: Mapping[str, str],
        buffer_size: int = 256,
    ) -> None:
        self.settings = settings
        self.page_map = page_map
        self.timeouts = timeouts
        self._patterns: dict[str, re.Pattern[str]] = {key: re.compile(value) for key, value in observe.items()}
        self._buffers: dict[str, deque[ObservedResponseDao]] = {key: deque(maxlen=buffer_size) for key in observe}
        self._buffer_lock = threading.Lock()
        self._exclusive = threading.RLock()
        self._seq = 0
        self._loop: asyncio.AbstractEventLoop | None = None
        self._thread: threading.Thread | None = None
        self._playwright: Playwright | None = None
        self._context: BrowserContext | None = None
        self._session: BrowserSession | None = None
        self._command_lock: asyncio.Lock | None = None
        self._lost_reason: str | None = None
        self._epoch = 0
        self._browser_version = ""
        self._web_version: str | None = None
        self._body_failures = 0

    @property
    def is_started(self) -> bool:
        return self._session is not None

    @property
    def is_lost(self) -> bool:
        return self._lost_reason is not None

    @property
    def lost_reason(self) -> str | None:
        return self._lost_reason

    @property
    def navigation_epoch(self) -> int:
        return self._epoch

    @property
    def browser_version(self) -> str:
        return self._browser_version

    @property
    def web_version(self) -> str | None:
        return self._web_version

    @property
    def body_failures(self) -> int:
        return self._body_failures

    def exclusive(self) -> threading.RLock:
        """Hold across several `run` calls that must not be interleaved with other callers' commands."""
        return self._exclusive

    def start(self) -> BrowserInfoDao:
        check_start_url(self.settings)
        with self._exclusive:
            self._ensure_loop()
            return self._call(self._launch(), self.settings.launch_timeout_s + 30)

    def restart(self) -> BrowserInfoDao:
        check_start_url(self.settings)
        with self._exclusive:
            self._ensure_loop()
            return self._call(self._relaunch(), self.settings.launch_timeout_s + 60)

    def close(self) -> None:
        with self._exclusive:
            loop, thread = self._loop, self._thread
            if loop is None or thread is None:
                return
            try:
                self._call(self._shutdown(), 30)
            except (BrowserCommandTimeoutError, PlaywrightError):
                pass
            loop.call_soon_threadsafe(loop.stop)
            thread.join(timeout=10)
            loop.close()
            self._loop, self._thread, self._session = None, None, None

    def run(self, command: Callable[[BrowserSession], Awaitable[T]], timeout_s: float | None = None) -> T:
        with self._exclusive:
            if self._loop is None or self._session is None:
                raise BrowserNotStartedError("browser actor not started")
            if self._lost_reason is not None:
                raise BrowserLostError(self._lost_reason)
            return self._call(self._serial(command), timeout_s or self.settings.command_timeout_s)

    def observations(self, key: str, after_seq: int = 0) -> tuple[ObservedResponseDao, ...]:
        with self._buffer_lock:
            return tuple(item for item in self._buffers.get(key, ()) if item.seq > after_seq)

    def latest_seq(self) -> int:
        with self._buffer_lock:
            return self._seq

    def _ensure_loop(self) -> None:
        if self._loop is not None:
            return
        loop: asyncio.AbstractEventLoop = asyncio.ProactorEventLoop() if sys.platform == "win32" else asyncio.new_event_loop()
        thread = threading.Thread(target=loop.run_forever, name="jimeng-browser-actor", daemon=True)
        thread.start()
        self._loop, self._thread = loop, thread

    def _call(self, coroutine: Coroutine[Any, Any, T], timeout_s: float) -> T:
        assert self._loop is not None
        future = asyncio.run_coroutine_threadsafe(coroutine, self._loop)
        try:
            return future.result(timeout_s)
        except concurrent.futures.TimeoutError as error:
            raise BrowserCommandTimeoutError(f"browser command exceeded {timeout_s:.0f}s") from error

    async def _serial(self, command: Callable[[BrowserSession], Awaitable[T]]) -> T:
        assert self._command_lock is not None and self._session is not None
        async with self._command_lock:
            if self._lost_reason is not None:
                raise BrowserLostError(self._lost_reason)
            try:
                return await command(self._session)
            except PlaywrightError as error:
                if self._lost_reason is not None or _is_closed(error):
                    self._mark_lost(self._lost_reason or "target_closed")
                    raise BrowserLostError(self._lost_reason or "target_closed") from error
                raise PageStepError(StepFailureKind.PAGE_ERROR, "page", str(error).splitlines()[0][:300]) from error

    async def _launch(self) -> BrowserInfoDao:
        settings = self.settings
        if self._playwright is None:
            self._playwright = await async_playwright().start()
        settings.profile_dir.mkdir(parents=True, exist_ok=True)
        options: dict[str, Any] = {
            "headless": settings.headless,
            "viewport": {"width": settings.viewport_width, "height": settings.viewport_height},
            "accept_downloads": True,
            "timeout": settings.launch_timeout_s * 1000,
        }
        if settings.executable_path is not None:
            options["executable_path"] = str(settings.executable_path)
        elif settings.channel != "chromium":
            options["channel"] = settings.channel
        try:
            context = await self._playwright.chromium.launch_persistent_context(str(settings.profile_dir), **options)
        except PlaywrightTimeoutError as error:
            raise BrowserLaunchError(LaunchFailureKind.LAUNCH_TIMEOUT, str(error)[:300]) from error
        except PlaywrightError as error:
            raise BrowserLaunchError(classify_launch_error(str(error)), str(error)[:300]) from error
        self._context = context
        self._command_lock = asyncio.Lock()
        self._lost_reason = None
        context.on("close", lambda _context: self._mark_lost("context_closed"))
        context.on("response", self._on_response)
        page = context.pages[0] if context.pages else await context.new_page()
        page.on("close", lambda _page: self._mark_lost("page_closed"))
        page.on("crash", lambda _page: self._mark_lost("page_crashed"))
        page.on("domcontentloaded", lambda _page: self._bump_epoch())
        page.on("framenavigated", lambda frame: self._on_navigated(page, frame))
        self._browser_version = await _browser_version(context, page)
        await page.goto(settings.start_url, wait_until="domcontentloaded", timeout=self.timeouts.page_ready_s * 1000)
        self._session = BrowserSession(self, context, page)
        return BrowserInfoDao(browser_version=self._browser_version, start_url=settings.start_url)

    async def _relaunch(self) -> BrowserInfoDao:
        await self._close_context()
        return await self._launch()

    async def _shutdown(self) -> None:
        await self._close_context()
        if self._playwright is not None:
            await self._playwright.stop()
            self._playwright = None

    async def _close_context(self) -> None:
        context, self._context, self._session = self._context, None, None
        if context is None:
            return
        try:
            await context.close()
        except PlaywrightError:
            pass

    def _mark_lost(self, reason: str) -> None:
        if self._lost_reason is None:
            self._lost_reason = reason
        self._bump_epoch()

    def _bump_epoch(self) -> None:
        self._epoch += 1

    def _on_navigated(self, page: Page, frame: Frame) -> None:
        if frame is not page.main_frame or not self.settings.test_mode:
            return
        host = urlsplit(frame.url).hostname
        if host is not None and host not in LOCAL_HOSTS:
            self._mark_lost(f"left_test_origin:{host}")
            if self._context is not None:
                asyncio.get_running_loop().create_task(self._close_context())

    def _on_response(self, response: Response) -> None:
        url = response.url
        version = parse_qs(urlsplit(url).query).get("web_version")
        if version:
            self._web_version = version[0]
        for key, pattern in self._patterns.items():
            if pattern.search(url):
                asyncio.get_running_loop().create_task(self._read_body(key, response))
                return

    async def _read_body(self, key: str, response: Response) -> None:
        body: bytes | None = None
        error: str | None = None
        try:
            body = await response.body()
        except PlaywrightError as failure:
            error = str(failure).splitlines()[0][:200]
            self._body_failures += 1
        with self._buffer_lock:
            self._seq += 1
            self._buffers[key].append(
                ObservedResponseDao(self._seq, key, response.url, response.status, body, error, time.monotonic())
            )


def check_start_url(settings: BrowserSettingsDao) -> None:
    parts = urlsplit(settings.start_url)
    if settings.test_mode:
        if parts.scheme not in ("http", "https") or parts.hostname not in LOCAL_HOSTS:
            raise BrowserLaunchError(LaunchFailureKind.UNSAFE_START_URL, "test mode requires a localhost start_url")
        if settings.channel != "chromium":
            raise BrowserLaunchError(LaunchFailureKind.UNSAFE_START_URL, "test mode requires the bundled chromium")
        return
    if not settings.start_url.startswith(REAL_SITE_PREFIX):
        raise BrowserLaunchError(LaunchFailureKind.UNSAFE_START_URL, f"start_url must start with {REAL_SITE_PREFIX}")


def classify_launch_error(message: str) -> LaunchFailureKind:
    lowered = message.lower()
    if "processsingleton" in lowered or "already in use" in lowered or "profile" in lowered and "in use" in lowered:
        return LaunchFailureKind.PROFILE_IN_USE
    if "executable doesn't exist" in lowered or "is not found" in lowered or "not found at" in lowered:
        return LaunchFailureKind.BROWSER_MISSING
    if "timeout" in lowered:
        return LaunchFailureKind.LAUNCH_TIMEOUT
    return LaunchFailureKind.LAUNCH_FAILED


def _is_closed(error: PlaywrightError) -> bool:
    return type(error).__name__ == "TargetClosedError" or any(marker in str(error) for marker in _CLOSED_MARKERS)


async def _browser_version(context: BrowserContext, page: Page) -> str:
    if context.browser is not None and context.browser.version:
        return context.browser.version
    match = _CHROME_VERSION.search(await page.evaluate("() => navigator.userAgent"))
    return match.group(1) if match else ""


def default_profile_dir(data_dir: Path) -> Path:
    return data_dir / "chrome_profile"
