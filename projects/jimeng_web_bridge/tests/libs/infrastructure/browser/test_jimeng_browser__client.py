from __future__ import annotations

import threading
import time
from pathlib import Path

import pytest

from libs.infrastructure.clients.jimeng_browser__client import (
    BrowserSession,
    JimengBrowserClient,
    check_start_url,
    classify_launch_error,
)
from libs.infrastructure.clients.jimeng_page__map import JimengPageMap
from libs.infrastructure.daos.jimeng_page__dao import BrowserSettingsDao
from libs.infrastructure.errors.jimeng_browser__error import (
    BrowserLaunchError,
    BrowserLostError,
    BrowserNotStartedError,
    LaunchFailureKind,
)
from libs.infrastructure.readers.jimeng_history__reader import HISTORY_BY_IDS, HISTORY_QUEUE_INFO, RESPONSE_PATTERNS
from tests.fixtures.fake_jimeng_site.server import FakeJimengSite
from tests.libs.infrastructure.browser.support import FAST_TIMEOUTS, fresh_page, start_client


def settings(start_url: str, test_mode: bool, channel: str = "chromium") -> BrowserSettingsDao:
    return BrowserSettingsDao(channel=channel, profile_dir=Path("unused"), start_url=start_url, headless=True, test_mode=test_mode)


@pytest.mark.parametrize(
    ("start_url", "test_mode", "channel"),
    [
        ("https://jimeng.jianying.com/ai-tool/generate?type=video", True, "chromium"),
        ("http://example.com/ai-tool/generate", True, "chromium"),
        ("http://127.0.0.1:9/ai-tool/generate", True, "chrome"),
        ("http://127.0.0.1:9/ai-tool/generate", False, "chrome"),
        ("https://jimeng.jianying.com.evil.example/", False, "chrome"),
    ],
)
def test_unsafe_start_urls_are_refused_before_launch(start_url: str, test_mode: bool, channel: str) -> None:
    with pytest.raises(BrowserLaunchError) as caught:
        check_start_url(settings(start_url, test_mode, channel))
    assert caught.value.kind is LaunchFailureKind.UNSAFE_START_URL


def test_safe_start_urls_pass() -> None:
    check_start_url(settings("http://127.0.0.1:9/ai-tool/generate?type=video", True))
    check_start_url(settings("https://jimeng.jianying.com/ai-tool/generate?type=video", False, "chrome"))


@pytest.mark.parametrize(
    ("message", "kind"),
    [
        ("Failed to create a ProcessSingleton for your profile directory", LaunchFailureKind.PROFILE_IN_USE),
        ("Executable doesn't exist at C:\\x\\chrome.exe", LaunchFailureKind.BROWSER_MISSING),
        ("Chromium distribution 'chrome' is not found at C:\\Program Files", LaunchFailureKind.BROWSER_MISSING),
        ("Timeout 60000ms exceeded", LaunchFailureKind.LAUNCH_TIMEOUT),
        ("something else", LaunchFailureKind.LAUNCH_FAILED),
    ],
)
def test_launch_failures_are_classified(message: str, kind: LaunchFailureKind) -> None:
    assert classify_launch_error(message) is kind


def test_run_before_start_is_refused(tmp_path: Path) -> None:
    client = JimengBrowserClient(settings("http://127.0.0.1:9/", True), JimengPageMap(), FAST_TIMEOUTS, RESPONSE_PATTERNS)
    with pytest.raises(BrowserNotStartedError):
        client.run(lambda session: session.page.title())


def test_passive_listener_buffers_status_bodies(browser_client: JimengBrowserClient, fake_jimeng_site: FakeJimengSite) -> None:
    fresh_page(browser_client, fake_jimeng_site)
    after = browser_client.latest_seq()
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline and not browser_client.observations(HISTORY_QUEUE_INFO, after):
        time.sleep(0.1)
    observed = browser_client.observations(HISTORY_QUEUE_INFO, after)
    assert observed and observed[-1].body is not None and observed[-1].status == 200
    assert browser_client.observations(HISTORY_BY_IDS, after)
    assert browser_client.web_version == "7.5.0-fake"
    assert browser_client.browser_version
    assert browser_client.body_failures == 0


def test_reload_bumps_navigation_epoch(browser_client: JimengBrowserClient, fake_jimeng_site: FakeJimengSite) -> None:
    before = browser_client.navigation_epoch
    fresh_page(browser_client, fake_jimeng_site)
    assert browser_client.navigation_epoch > before


def test_commands_never_overlap(browser_client: JimengBrowserClient) -> None:
    spans: list[tuple[float, float]] = []

    async def command(session: BrowserSession) -> None:
        started = time.monotonic()
        await session.page.wait_for_timeout(150)
        spans.append((started, time.monotonic()))

    threads = [threading.Thread(target=browser_client.run, args=(command,)) for _ in range(4)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=30)
    spans.sort()
    assert len(spans) == 4
    assert all(earlier[1] <= later[0] for earlier, later in zip(spans, spans[1:]))


def test_page_close_marks_lost_and_restart_recovers(fake_jimeng_site: FakeJimengSite, tmp_path: Path) -> None:
    client = start_client(fake_jimeng_site, tmp_path / "profile")
    try:
        client.run(lambda session: session.page.close())
        assert client.is_lost and client.lost_reason == "page_closed"
        with pytest.raises(BrowserLostError):
            client.run(lambda session: session.page.title())
        client.restart()
        assert not client.is_lost
        assert client.run(lambda session: session.page.title())
    finally:
        client.close()
