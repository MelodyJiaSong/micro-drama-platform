from __future__ import annotations

import logging
import threading
from collections.abc import Callable
from typing import Protocol

from libs.application.dtos.session__dto import BrowserOpenCdto

_LOG = logging.getLogger(__name__)


class BrowserWindow(Protocol):
    @property
    def is_started(self) -> bool: ...

    @property
    def is_lost(self) -> bool: ...

    def start(self) -> object: ...

    def restart(self) -> object: ...


class SessionCommand:
    """「打开浏览器窗口」: launches the dedicated profile in the background so the user can scan the QR code.

    It only launches (the actor lands on `browser.start_url`); it never navigates to a generate action or clicks.
    """

    def __init__(self, browser_provider: Callable[[], BrowserWindow]) -> None:
        self._browser_provider = browser_provider

    def open_browser(self) -> BrowserOpenCdto:
        browser = self._browser_provider()
        if browser.is_started and not browser.is_lost:
            return BrowserOpenCdto(accepted=False, message="浏览器窗口已经打开")
        if not _LAUNCHING.acquire(blocking=False):
            return BrowserOpenCdto(accepted=False, message="浏览器窗口正在启动")
        threading.Thread(target=_launch, args=(browser,), name="jwb-browser-open", daemon=True).start()
        return BrowserOpenCdto(accepted=True, message="正在打开浏览器窗口；如需登录请在窗口里扫码")


_LAUNCHING = threading.Lock()


def _launch(browser: BrowserWindow) -> None:
    try:
        if browser.is_lost:
            browser.restart()
        else:
            browser.start()
    except Exception:  # background best effort: the session page shows the resulting state
        _LOG.exception("opening the browser window failed")
    finally:
        _LAUNCHING.release()
