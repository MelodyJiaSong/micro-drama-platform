"""Shared harness for browser tests against the offline fake 即梦 site (never the real site)."""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from libs.infrastructure.clients.jimeng_browser__client import BrowserSession, JimengBrowserClient
from libs.infrastructure.clients.jimeng_page__map import JimengPageMap
from libs.infrastructure.clients.jimeng_page__steps import wait_composer_ready
from libs.infrastructure.daos.jimeng_page__dao import BrowserSettingsDao, StepTimeoutsDao
from libs.infrastructure.readers.jimeng_history__reader import RESPONSE_PATTERNS
from tests.fixtures.fake_jimeng_site.server import FakeJimengSite

CHROMIUM_ENV: str = "JWB_TEST_CHROMIUM"
FAST_TIMEOUTS: StepTimeoutsDao = StepTimeoutsDao(
    action_s=5.0,
    readback_s=1.0,
    page_ready_s=15.0,
    upload_done_s=8.0,
    mention_popup_s=3.0,
    submit_response_s=4.0,
    history_fallback_s=3.0,
    download_s=30.0,
    response_wait_s=8.0,
)
FAST_POLL_MS: int = 250


def chromium_executable() -> Path | None:
    """None = Playwright's own bundled build is installed. Otherwise the newest local headless shell.

    Needed because the pinned Playwright may expect a browser revision that could not be downloaded here.
    """
    override = os.environ.get(CHROMIUM_ENV)
    if override:
        return Path(override)
    import playwright

    package = Path(playwright.__file__).resolve().parent / "driver" / "package" / "browsers.json"
    root = Path(os.environ.get("PLAYWRIGHT_BROWSERS_PATH") or Path(os.environ.get("LOCALAPPDATA", "")) / "ms-playwright")
    revision = next(
        (b["revision"] for b in json.loads(package.read_text(encoding="utf-8"))["browsers"] if b["name"] == "chromium-headless-shell"),
        None,
    )
    if revision is not None and (root / f"chromium_headless_shell-{revision}").is_dir():
        return None
    shells = sorted(root.glob("chromium_headless_shell-*/chrome-headless-shell-*/chrome-headless-shell*"), key=lambda p: p.parts[-3])
    executables = [path for path in shells if path.suffix in (".exe", "")]
    if not executables:
        pytest.skip("no Playwright chromium available (run `.venv/Scripts/python.exe -m playwright install chromium`)")
    return executables[-1]


def browser_settings(profile_dir: Path, start_url: str) -> BrowserSettingsDao:
    return BrowserSettingsDao(
        channel="chromium",
        profile_dir=profile_dir,
        start_url=start_url,
        headless=True,
        test_mode=True,
        launch_timeout_s=60.0,
        command_timeout_s=120.0,
        executable_path=chromium_executable(),
    )


def start_client(site: FakeJimengSite, profile_dir: Path) -> JimengBrowserClient:
    client = JimengBrowserClient(browser_settings(profile_dir, site.generate_url), JimengPageMap(), FAST_TIMEOUTS, RESPONSE_PATTERNS)
    client.start()
    return client


def fresh_page(client: JimengBrowserClient, site: FakeJimengSite, **seed: object) -> None:
    """Resets the fake site and reloads the work page so every test starts from the same page state."""
    site.reset()
    site.state.seed(poll_ms=FAST_POLL_MS, **seed)  # type: ignore[arg-type]
    if client.is_lost:
        client.restart()

    async def reload(session: BrowserSession) -> None:
        await session.page.goto(site.generate_url, wait_until="domcontentloaded")
        await wait_composer_ready(session)

    client.run(reload)
