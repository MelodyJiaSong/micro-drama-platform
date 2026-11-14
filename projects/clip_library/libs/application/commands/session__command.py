from typing import Callable

from libs.application.dtos.session__dto import SessionCdto
from libs.common.options import LOGIN_URL
from libs.domain.value_objects.session__valueobject import Session, in_scope
from libs.infrastructure.clients.chrome__client import ChromeClient
from libs.infrastructure.writers.cookie__writer import CookieWriter


class SessionCommand:
    def __init__(self, chrome: ChromeClient, writer: CookieWriter) -> None:
        self._chrome = chrome
        self._writer = writer

    def login(self, notify: Callable[[str], None]) -> SessionCdto:
        notify("已打开独立的 Chrome 窗口：登录 YouTube，看到首页后关闭这个窗口……")
        self._chrome.open_and_wait(LOGIN_URL)
        cookies = [cookie for cookie in self._chrome.read_cookies() if in_scope(cookie.domain)]
        Session(frozenset(cookie.name for cookie in cookies))
        return SessionCdto(str(self._writer.write(cookies)), len(cookies))
