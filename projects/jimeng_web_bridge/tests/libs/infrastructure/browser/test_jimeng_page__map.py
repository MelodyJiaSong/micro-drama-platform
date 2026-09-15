"""PageMap registry (UT-W-PM-01..07) — static checks plus resolution on the offline fake page."""
from __future__ import annotations

import time
from pathlib import Path

import pytest

from libs.infrastructure.clients.jimeng_browser__client import BrowserSession, JimengBrowserClient
from libs.infrastructure.clients.jimeng_page__map import CANARY_STEPS, DOM_STRATEGIES, JimengPageMap, LocatorStrategy
from libs.infrastructure.clients.jimeng_page__steps import is_visible, locate
from tests.fixtures.fake_jimeng_site.server import FakeJimengSite
from tests.libs.infrastructure.browser.support import fresh_page

PAGE_MAP = JimengPageMap()
REQUIRED_STEPS: tuple[str, ...] = (
    "login_marker",
    *(f"{control}.{role}" for control in ("creation_type", "model", "reference_mode", "ratio", "resolution", "count", "duration")
      for role in ("set", "readback")),
    "upload_input", "upload_done_signal", "upload_rejected",
    "editor", "mention_trigger", "mention_popup", "mention_option_by_name", "mention_node", "editor_clear", "negative_field",
    "composer_region", "estimated_credits_text",
    "generate_button", "parallel_limit_notice", "history_record_by_prompt_prefix",
    "history_response_patterns",
    "record_download_control", "record_details_credits",
    "captcha_or_risk_popup", "login_expired_notice",
    "entity_page", "entity_new_form_open", "entity_new_form_name", "entity_new_form_description", "entity_new_form_save",
)
ALWAYS_ON_DEFAULT_PAGE: tuple[str, ...] = (
    "login_marker", "composer_region", "toolbar", "creation_type.readback", "model.readback", "reference_mode.readback",
    "ratio.readback", "duration.readback", "mention_trigger", "estimated_credits_text", "generate_button", "upload_input",
    "editor", "history_list",
)
BLOCKERS: tuple[str, ...] = ("captcha_or_risk_popup", "login_expired_notice", "login_button", "parallel_limit_notice")


def test_registry_covers_every_required_step() -> None:
    assert set(REQUIRED_STEPS) <= set(PAGE_MAP.steps())


def test_nothing_is_verified_on_the_real_site_yet() -> None:
    assert set(PAGE_MAP.unverified()) == set(PAGE_MAP.steps())


def test_locators_are_semantic_and_parents_exist() -> None:
    for entry in PAGE_MAP.entries():
        if entry.within is not None:
            assert entry.within in PAGE_MAP.steps(), entry.step
        if entry.strategy is LocatorStrategy.CSS:
            assert entry.step == "editor" or entry.read_only, f"{entry.step}: CSS only for the observed editor or read-only structure"
            assert ">>" not in (entry.css or "") and "nth" not in (entry.css or "")
        if entry.strategy is LocatorStrategy.ROLE:
            assert entry.role


def test_canary_steps_are_registered_dom_entries_and_never_click() -> None:
    for step in CANARY_STEPS:
        assert PAGE_MAP.get(step).strategy in DOM_STRATEGIES
    canary_source = (Path(__file__).resolve().parents[4] / "libs/infrastructure/clients/jimeng_page_canary__steps.py").read_text(encoding="utf-8")
    assert ".click(" not in canary_source and "generate_button" not in canary_source


def count_visible(client: JimengBrowserClient, step: str) -> int:
    async def command(session: BrowserSession) -> int:
        locator = locate(session, step)
        return sum([await locator.nth(index).is_visible() for index in range(await locator.count())])

    return client.run(command)


def test_default_page_resolves_each_always_on_entry_exactly_once(browser_client: JimengBrowserClient, fake_jimeng_site: FakeJimengSite) -> None:
    fresh_page(browser_client, fake_jimeng_site)
    assert {step: count_visible(browser_client, step) for step in ALWAYS_ON_DEFAULT_PAGE} == {step: 1 for step in ALWAYS_ON_DEFAULT_PAGE}
    assert {step: count_visible(browser_client, step) for step in BLOCKERS} == {step: 0 for step in BLOCKERS}


@pytest.mark.parametrize(
    ("inject", "seed", "expected_visible"),
    [
        ({"name": "captcha_popup", "now": True}, {}, "captcha_or_risk_popup"),
        ({"name": "login_expired"}, {}, "login_expired_notice"),
        (None, {"external_running": 3}, "parallel_limit_notice"),
    ],
)
def test_blocker_detectors_fire_on_their_variant(
    browser_client: JimengBrowserClient,
    fake_jimeng_site: FakeJimengSite,
    inject: dict[str, object] | None,
    seed: dict[str, object],
    expected_visible: str,
) -> None:
    fresh_page(browser_client, fake_jimeng_site, **seed)
    if inject is not None:
        name = str(inject.pop("name"))
        fake_jimeng_site.inject(name, **inject)
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline and count_visible(browser_client, expected_visible) == 0:
        time.sleep(0.1)
    assert count_visible(browser_client, expected_visible) >= 1
    fake_jimeng_site.reset()


def test_record_scoped_controls_stay_inside_their_record(browser_client: JimengBrowserClient, fake_jimeng_site: FakeJimengSite) -> None:
    fresh_page(browser_client, fake_jimeng_site)
    state = fake_jimeng_site.state
    for index, prefix in enumerate(("shot01 甲", "shot02 乙", "shot03 丙")):
        record = state.new_record(f"{prefix} 情节", [], [], {"model": "即梦 Seedance 2.5", "duration": 22, "ratio": "16:9", "resolution": "720P"})
        record.status, record.progress = "succeeded", 100
    fresh_page_keep_state(browser_client, fake_jimeng_site)

    async def command(session: BrowserSession) -> tuple[int, int, int]:
        records = locate(session, "history_record_by_prompt_prefix")
        deadline = time.monotonic() + 5
        while await records.count() < 3 and time.monotonic() < deadline:
            await session.page.wait_for_timeout(100)
        target = records.filter(has_text="shot02 乙")
        return await records.count(), await target.count(), await locate(session, "record_download_control", root=target.first).count()

    assert browser_client.run(command) == (3, 1, 1)


def fresh_page_keep_state(client: JimengBrowserClient, site: FakeJimengSite) -> None:
    async def reload(session: BrowserSession) -> None:
        await session.page.goto(site.generate_url, wait_until="domcontentloaded")
        await is_visible(locate(session, "history_list"))

    client.run(reload)
