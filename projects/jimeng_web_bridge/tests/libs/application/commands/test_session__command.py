from __future__ import annotations

import threading
import time
from collections.abc import Iterator

import pytest

from libs.application.commands import session__command
from libs.application.commands.session__command import SessionCommand


@pytest.fixture(autouse=True)
def launch_lock_released() -> Iterator[None]:
    yield
    deadline = time.monotonic() + 5
    while session__command._LAUNCHING.locked() and time.monotonic() < deadline:
        time.sleep(0.01)
    assert not session__command._LAUNCHING.locked()


class FakeBrowser:
    def __init__(self, started: bool = False, lost: bool = False) -> None:
        self.started = started
        self.lost = lost
        self.calls: list[str] = []
        self.release = threading.Event()
        self.done = threading.Event()

    @property
    def is_started(self) -> bool:
        return self.started

    @property
    def is_lost(self) -> bool:
        return self.lost

    def start(self) -> object:
        self.calls.append("start")
        self.release.wait(5)
        self.started = True
        self.done.set()
        return None

    def restart(self) -> object:
        self.calls.append("restart")
        self.lost = False
        self.done.set()
        return None


def test_open_launches_once_in_background() -> None:
    browser = FakeBrowser()
    command = SessionCommand(lambda: browser)
    first = command.open_browser()
    second = command.open_browser()
    assert first.accepted and not second.accepted and second.message == "浏览器窗口正在启动"
    browser.release.set()
    assert browser.done.wait(5)
    assert browser.calls == ["start"]


def test_already_open_is_not_relaunched() -> None:
    browser = FakeBrowser(started=True)
    result = SessionCommand(lambda: browser).open_browser()
    assert not result.accepted and browser.calls == []


def test_lost_browser_is_restarted() -> None:
    browser = FakeBrowser(started=True, lost=True)
    assert SessionCommand(lambda: browser).open_browser().accepted
    assert browser.done.wait(5) and browser.calls == ["restart"]
