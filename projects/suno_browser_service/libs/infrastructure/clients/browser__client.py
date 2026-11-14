import os
import time
from contextlib import contextmanager
from collections.abc import Callable, Iterator
from pathlib import Path
from urllib.parse import urlsplit

from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from projects.suno_browser_service.libs.common.errors import ServiceError
from projects.suno_browser_service.libs.common.settings import Settings
from projects.suno_browser_service.libs.infrastructure.clients.audit__client import AuditClient
from projects.suno_browser_service.libs.infrastructure.clients.manual_browser__client import close_hung_tabs, window_open


class BrowserClient:
    """Opens the Suno browser. With settings.attached the service works in the window a person keeps
    open (open-window.ps1); with settings.keep_browser its own launched window stays open across jobs.

    Playwright's sync API is bound to one thread: a kept or attached window must only be used and
    closed from the worker thread that opened it.
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._playwright: Playwright | None = None
        self._context: BrowserContext | None = None
        self._browser: Browser | None = None
        self._page: Page | None = None

    @contextmanager
    def session(self, audit: AuditClient, *, headed: bool = False) -> Iterator[BrowserContext]:
        config = self.settings
        if config.attached and not headed:
            yield self._attached(audit)
            return
        if config.keep_browser and not config.endpoint and not headed:
            yield self._kept(audit)
            return
        state = config.data_dir / "storage-state.json"
        with sync_playwright() as playwright:
            browser = None
            try:
                if config.endpoint:
                    if headed:
                        raise ServiceError("remote_login", "先通过 Browserless 的交互会话登录，再配置 storage-state.json")
                    browser = audit.call("browser_connect", {"host": urlsplit(config.endpoint).hostname, "transport": "playwright"},
                                         lambda: playwright.chromium.connect(config.endpoint))
                    context = audit.call("browser_context", {"storage_state": "local file" if state.exists() else "none"},
                                         lambda: browser.new_context(accept_downloads=True, storage_state=str(state) if state.exists() else None))
                else:
                    context = audit.call("browser_launch", {"channel": config.channel, "headless": config.headless and not headed},
                                         lambda: self._launch(playwright, config.headless and not headed))
            except ServiceError:
                raise
            except Exception as exc:
                raise ServiceError("browser_unavailable", "浏览器启动或连接失败；检查 Chrome / Playwright 安装与 SUNO_BROWSER_WS") from None
            try:
                yield context
            finally:
                context.close()
                if browser is not None:
                    browser.close()

    def _launch(self, playwright: Playwright, headless: bool) -> BrowserContext:
        return playwright.chromium.launch_persistent_context(
            str(self.settings.profile_dir), channel=self.settings.channel or None,
            headless=headless, accept_downloads=True, viewport={"width": 1440, "height": 1000})

    def page(self, context: BrowserContext) -> Page:
        """The tab a job works in. Attached: the service's own tab, so the person's other tabs are left alone."""
        if not self.settings.attached:
            return context.pages[0] if context.pages else context.new_page()
        page = self._page
        if page is None or page.is_closed() or page.context is not context:
            page = self._page = context.new_page()
            # Without a handler Playwright dismisses dialogs, and a dismissed "Leave site?" keeps the tab where it is:
            # every later navigation of this tab then timed out (2026-11-03, 14 jobs). Only the service uses this tab.
            page.on("dialog", lambda dialog: dialog.accept() if dialog.type == "beforeunload" else dialog.dismiss())
        return page

    def renew_page(self, context: BrowserContext) -> Page:
        """Replace a work tab that stopped responding with a new one (attached mode only)."""
        old, self._page = self._page, None
        if old is not None:
            try:
                old.close(run_before_unload=False)
            except Exception:
                pass
        return self.page(context)

    def capture_download(self, page: Page, click: Callable[[], None], dest: Path, timeout_ms: int) -> None:
        """Attached window: Playwright's download object comes back empty and Chrome would save into the person's
        Downloads folder, so for this one download Chrome saves into a private staging folder and the file is moved
        to dest. The window's own download setting is restored afterwards."""
        if self._browser is None:
            raise ServiceError("window_not_open", "常驻窗口连接已断开；恢复任务重试下载")
        staging = self.settings.data_dir / "downloads"
        staging.mkdir(parents=True, exist_ok=True)
        session = self._browser.new_browser_cdp_session()
        state: dict = {}
        session.on("Browser.downloadWillBegin", lambda event: state.setdefault("guid", event["guid"]))
        session.on("Browser.downloadProgress", lambda event: state.update(guid=event["guid"], done=event["state"])
                   if event["state"] in {"completed", "canceled"} and event["guid"] == state.get("guid", event["guid"]) else None)
        session.send("Browser.setDownloadBehavior", {"behavior": "allowAndName", "downloadPath": str(staging), "eventsEnabled": True})
        try:
            click()
            deadline = time.monotonic() + timeout_ms / 1000
            while "done" not in state and time.monotonic() < deadline:
                page.wait_for_timeout(500)  # also lets Playwright deliver the CDP events
            if state.get("done") != "completed":
                raise ServiceError("download_failed", "官方下载没有完成；可恢复补收")
            os.replace(staging / state["guid"], dest)
        finally:
            try:
                session.send("Browser.setDownloadBehavior", {"behavior": "default"})
                session.detach()
            except Exception:
                pass

    def _attached(self, audit: AuditClient) -> BrowserContext:
        if self._browser is not None:
            try:
                if self._browser.is_connected() and self._browser.contexts:
                    return self._browser.contexts[0]
            except Exception:
                pass
            self.close()
        if not window_open(self.settings):
            raise ServiceError("window_not_open", "常驻 Suno 窗口没有打开；运行 open-window.ps1 打开后恢复任务")
        try:
            if self._playwright is None:
                self._playwright = sync_playwright().start()
            playwright = self._playwright

            def attach() -> Browser:
                return audit.call("browser_attach", {"cdp": f"127.0.0.1:{self.settings.window_port}", "window": "kept open by person"},
                                  lambda: playwright.chromium.connect_over_cdp(self.settings.cdp_url, timeout=15000))
            try:
                self._browser = attach()
            except Exception:
                # The window answers but the connect timed out: a hung tab blocks it. Close hung tabs, try once more.
                if not window_open(self.settings):
                    raise
                result = audit.call("close_hung_tabs", {"window": f"127.0.0.1:{self.settings.window_port}"},
                                    lambda: close_hung_tabs(self.settings))
                if not result["closed"]:
                    raise
                self._browser = attach()
            if not self._browser.contexts:
                raise ServiceError("window_not_open", "常驻窗口没有可用的浏览器上下文；关掉后重新运行 open-window.ps1")
            return self._browser.contexts[0]
        except ServiceError:
            self.close()
            raise
        except Exception:
            self.close()
            raise ServiceError("window_not_open", "连接常驻 Suno 窗口失败；关掉后重新运行 open-window.ps1") from None

    def _kept(self, audit: AuditClient) -> BrowserContext:
        if self._context is not None:
            try:
                # Fails once the person closed the window; then a new one is opened below.
                page = self._context.pages[0] if self._context.pages else self._context.new_page()
                audit.call("browser_reuse", {"channel": self.settings.channel, "open_pages": len(self._context.pages)},
                           lambda: page.bring_to_front())
                return self._context
            except ServiceError:
                raise
            except Exception:
                self.close()
        try:
            if self._playwright is None:
                self._playwright = sync_playwright().start()
            playwright = self._playwright
            self._context = audit.call("browser_launch", {"channel": self.settings.channel, "headless": self.settings.headless, "kept": True},
                                       lambda: self._launch(playwright, self.settings.headless))
        except ServiceError:
            self.close()
            raise
        except Exception:
            self.close()
            raise ServiceError("browser_unavailable", "浏览器启动失败；检查 Chrome / Playwright 安装") from None
        self._context.on("close", lambda _context: setattr(self, "_context", None))
        return self._context

    def close(self) -> None:
        # Attached: only the connection is dropped (stopping Playwright); the person's window stays open.
        context, playwright = self._context, self._playwright
        self._context = self._playwright = self._browser = self._page = None
        for action in (context.close if context else None, playwright.stop if playwright else None):
            if action is None:
                continue
            try:
                action()
            except Exception:
                pass
