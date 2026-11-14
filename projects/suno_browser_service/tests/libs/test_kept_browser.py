"""常驻窗口：本机多次任务共用一个 Chrome 上下文；窗口被关掉后自动重开。用假 Playwright，不启动浏览器。"""

from pathlib import Path

import pytest

from projects.suno_browser_service.libs.common.settings import Settings
from projects.suno_browser_service.libs.infrastructure.clients import browser__client
from projects.suno_browser_service.libs.infrastructure.clients.audit__client import AuditClient
from projects.suno_browser_service.libs.infrastructure.clients.browser__client import BrowserClient


class FakePage:
    def bring_to_front(self) -> None:
        pass


class FakeContext:
    def __init__(self) -> None:
        self.closed = False
        self.handlers = []
        self._pages = [FakePage()]

    @property
    def pages(self):
        if self.closed:
            raise RuntimeError("Target closed")
        return self._pages

    def new_page(self):
        self._pages.append(FakePage())
        return self._pages[-1]

    def on(self, _event, handler) -> None:
        self.handlers.append(handler)

    def close(self) -> None:
        self.closed = True


class FakePlaywright:
    def __init__(self) -> None:
        self.contexts: list[FakeContext] = []
        self.stopped = False
        self.chromium = self

    def launch_persistent_context(self, *_args, **_kwargs):
        self.contexts.append(FakeContext())
        return self.contexts[-1]

    def stop(self) -> None:
        self.stopped = True


@pytest.fixture
def fake(monkeypatch: pytest.MonkeyPatch):
    playwrights: list[FakePlaywright] = []

    class Starter:
        def start(self):
            playwrights.append(FakePlaywright())
            return playwrights[-1]

    monkeypatch.setattr(browser__client, "sync_playwright", lambda: Starter())
    return playwrights


def test_kept_window_is_reused_and_reopened(tmp_path: Path, fake):
    settings = Settings(tmp_path / "data", keep_browser=True, headless=False)
    audit = AuditClient(tmp_path / "ai_videos" / "kept_fixture")
    client = BrowserClient(settings)
    with client.session(audit) as first:
        pass
    with client.session(audit) as second:
        pass
    assert first is second and not first.closed
    assert len(fake) == 1 and len(fake[0].contexts) == 1

    first.closed = True  # 人把窗口关了
    with client.session(audit) as third:
        pass
    assert third is not first and sum(len(item.contexts) for item in fake) == 2

    client.close()
    assert third.closed and all(item.stopped for item in fake)
    log = audit.log.path.read_text(encoding="utf-8")
    assert log.count('"browser_launch"') >= 2 and '"browser_reuse"' in log


def test_keep_browser_defaults_on_from_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("SUNO_BROWSER_KEEP", raising=False)
    assert Settings.from_env().keep_browser
    monkeypatch.setenv("SUNO_BROWSER_KEEP", "0")
    assert not Settings.from_env().keep_browser
