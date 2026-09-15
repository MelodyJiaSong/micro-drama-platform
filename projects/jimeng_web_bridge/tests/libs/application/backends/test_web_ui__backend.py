"""WebUiBackend + WebEntityGateway end to end on the offline fake 即梦 site (never the real site)."""
from __future__ import annotations

import asyncio
import hashlib
import shutil
import threading
import time
from collections.abc import Callable, Iterator
from pathlib import Path

import pytest

from libs.application.backends.web_entity__gateway import WebEntityGateway
from libs.application.backends.web_ui__backend import (
    CONCURRENCY_LIMIT_PRE_CLICK,
    NEGATIVE_ENTERED,
    NEGATIVE_OMITTED,
    NOT_NOW_PREFIX,
    POST_CLICK_REJECTIONS,
    WebUiBackend,
)
from libs.common.enums import BackendKind, GenerationKind, PauseReason, PreparingStep, RefKind, RemoteStatus, SourceType
from libs.common.paths import RepoSandbox
from libs.domain.repositories.generation_backend__repository import PollResult
from libs.domain.value_objects.frozen_request__valueobject import FrozenRequest
from libs.domain.value_objects.generation_params__valueobject import GenerationParams
from libs.domain.value_objects.generation_request__valueobject import GenerationRequest, RequestSource
from libs.domain.value_objects.global_config__valueobject import GlobalConfig
from libs.domain.value_objects.reference_item__valueobject import ReferenceItem
from libs.infrastructure.clients.jimeng_browser__client import BrowserSession, JimengBrowserClient
from libs.infrastructure.errors.jimeng_browser__error import WebBackendError
from libs.infrastructure.readers.shot_prompt__reader import ShotPromptReader
from libs.infrastructure.writers.artifact__writer import ArtifactWriter
from tests.fixtures.fake_jimeng_site.media import make_png
from tests.fixtures.fake_jimeng_site.server import FakeJimengSite, fake_jimeng_site  # noqa: F401
from tests.libs.domain.builders import global_data
from tests.libs.infrastructure.browser.support import fresh_page, start_client

HY3 = "ai_videos/huangye_shenghuo/hy3"
SHOT_DIR = f"{HY3}/5_6_分镜与prompt/shots/shot02"
ASSETS: dict[str, tuple[str, str, tuple[int, int, int]]] = {
    "bg11-1": ("场景参考图", f"{HY3}/2_世界观人设/scenes/caoya/bg11_崖脚洼地/bg11-1.png", (90, 110, 140)),
    "p2-1": ("随身装备锚点", f"{HY3}/2_世界观人设/props/p2_随身装备/p2-1.png", (80, 100, 60)),
    "p3-1": ("抹泥板锚点", f"{HY3}/2_世界观人设/props/p3_抹泥板与黏土壁炉/p3-1.png", (150, 130, 90)),
}
CHARACTER_CARD = f"{HY3}/2_世界观人设/characters/c1_砌炉的老人/c1-1.png"
SHORT_PROMPT = (
    "shot02\n参考: `bg11-1(场景参考图)=>@`，`砌炉的老人(Seedance 人物 entity)=>@`，`p2-1(随身装备锚点)=>@`，"
    "`p3-1(抹泥板锚点)=>@`\n情节: 他走到沟边蹲下，食指抹过湿土。\n时长: 22秒"
)
MENTIONS = ["bg11-1", "hy3_主角", "p2-1", "p3-1"]
REAL_SHOT02 = Path(__file__).resolve().parents[3] / "fixtures" / "real_shots" / "hy3__shot02.md"


@pytest.fixture(scope="module")
def repo(tmp_path_factory: pytest.TempPathFactory) -> Path:
    root = tmp_path_factory.mktemp("repo")
    for _label, rel, color in ASSETS.values():
        make_png(root / rel, color)
    make_png(root / CHARACTER_CARD, (200, 180, 160))
    (root / SHOT_DIR).mkdir(parents=True, exist_ok=True)
    shutil.copyfile(REAL_SHOT02, root / SHOT_DIR / "shot02.md")
    return root


@pytest.fixture(scope="module")
def client(fake_jimeng_site: FakeJimengSite, tmp_path_factory: pytest.TempPathFactory) -> Iterator[JimengBrowserClient]:  # noqa: F811
    browser = start_client(fake_jimeng_site, tmp_path_factory.mktemp("backend_profile"))
    yield browser
    browser.close()


def make_backend(client: JimengBrowserClient, site: FakeJimengSite, repo: Path, tmp_path: Path, **retries: int) -> WebUiBackend:
    fresh_page(client, site)
    data = global_data()
    data["retries"].update(retries)  # type: ignore[union-attr]
    return WebUiBackend(
        client, ArtifactWriter(tmp_path / "artifacts"), GlobalConfig.from_dict(data), repo, tmp_path / "tmp",
        poll_stale_s=2.0, poll_wait_s=4.0, status_fresh_s=3.0,
    )


@pytest.fixture
def backend(client: JimengBrowserClient, fake_jimeng_site: FakeJimengSite, repo: Path, tmp_path: Path) -> WebUiBackend:  # noqa: F811
    return make_backend(client, fake_jimeng_site, repo, tmp_path)


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frozen(repo: Path, prompt: str = SHORT_PROMPT, negative: str | None = None) -> FrozenRequest:
    def image(name: str) -> ReferenceItem:
        label, rel, _color = ASSETS[name]
        return ReferenceItem(name=name, label=label, kind=RefKind.IMAGE, resolved_path=rel, sha256=sha256_of(repo / rel))

    references = (
        image("bg11-1"),
        ReferenceItem(name="砌炉的老人", label="Seedance 人物 entity", kind=RefKind.ENTITY, entity_name="hy3_主角"),
        image("p2-1"),
        image("p3-1"),
    )
    request = GenerationRequest(
        kind=GenerationKind.VIDEO,
        prompt=prompt,
        negative_prompt=negative,
        references=references,
        params=GenerationParams(model="seedance2.5", ratio="16:9", resolution="720p", count=1, duration_s=22),
        output_slot=SHOT_DIR,
        source=RequestSource(type=SourceType.SHOT, path=f"{SHOT_DIR}/shot02.md"),
    )
    return FrozenRequest.freeze(request, BackendKind.WEB, "config-digest-test", 440, 20)


def poll_until(backend: WebUiBackend, task_id: str, done: Callable[[PollResult], bool], timeout_s: float = 20.0) -> PollResult:
    deadline = time.monotonic() + timeout_s
    while True:
        result = backend.poll(task_id)
        if done(result) or time.monotonic() > deadline:
            return result
        time.sleep(0.3)


def prepared_and_submitted(backend: WebUiBackend, repo: Path, job_id: str) -> str:
    request = frozen(repo)
    prepared = backend.prepare(job_id, request, PreparingStep.VERIFY)
    assert prepared.pause_reason is None, prepared.message
    outcome = backend.submit(job_id, request)
    assert outcome.platform_task_id is not None, outcome
    return outcome.platform_task_id


def test_golden_path_hy3_shot02(backend: WebUiBackend, fake_jimeng_site: FakeJimengSite, repo: Path, tmp_path: Path) -> None:  # noqa: F811
    site = fake_jimeng_site
    shot = ShotPromptReader(RepoSandbox(repo)).parse_bytes(REAL_SHOT02.read_bytes(), f"{SHOT_DIR}/shot02.md")
    assert shot.negative_prompt
    request = frozen(repo, prompt=shot.prompt, negative=shot.negative_prompt)

    prepared = backend.prepare("job_golden", request, PreparingStep.VERIFY)
    assert prepared.pause_reason is None, prepared.message
    assert prepared.reached_step is PreparingStep.VERIFY
    assert prepared.page_estimated_credits == 440
    assert prepared.message == NEGATIVE_OMITTED and backend.negative_prompt_entered("job_golden") is False
    assert len(prepared.screenshot_names) == 2
    assert all((tmp_path / "artifacts" / "job_golden" / name).is_file() for name in prepared.screenshot_names)

    ledger = site.state.ledger
    assert [(u["filename"], u["accepted"]) for u in ledger.uploads] == [("bg11-1.png", True), ("p2-1.png", True), ("p3-1.png", True)]
    assert [u["sha256"] for u in ledger.uploads] == [sha256_of(repo / ASSETS[name][1]) for name in ("bg11-1", "p2-1", "p3-1")]
    shown = {entry["control"]: entry["display"] for entry in ledger.param_sets}
    assert shown == {"type": "视频生成", "model": "即梦 Seedance 2.5", "mode": "全能参考", "ratio": "16:9",
                     "resolution": "720P", "count": "1", "duration": "22"}

    outcome = backend.submit("job_golden", request)
    assert outcome.platform_task_id is not None and outcome.rejection is None, outcome
    assert site.counts()["generate_clicks"] == 1
    (click,) = ledger.generate_clicks
    assert click["mentions"] == MENTIONS and click["accepted"] is True
    assert str(click["text"]).startswith("shot02\n参考: `bg11-1(场景参考图)=>bg11-1`，`砌炉的老人(Seedance 人物 entity)=>hy3_主角`")

    final = poll_until(backend, outcome.platform_task_id, lambda r: r.status is RemoteStatus.SUCCEEDED)
    assert (final.status, final.progress_pct, final.failure) == (RemoteStatus.SUCCEEDED, 100, None)

    downloaded = backend.download("job_golden", outcome.platform_task_id)
    assert downloaded.sha256 == hashlib.sha256(site.video.data).hexdigest()
    assert downloaded.size == len(site.video.data) == Path(downloaded.temp_path).stat().st_size
    assert Path(downloaded.temp_path).is_relative_to(tmp_path / "tmp")
    assert downloaded.credits_charged == 440
    assert site.counts()["generate_clicks"] == 1


def test_negative_prompt_entered_when_the_page_has_the_field(backend: WebUiBackend, fake_jimeng_site: FakeJimengSite, client: JimengBrowserClient, repo: Path) -> None:  # noqa: F811
    fresh_page(client, fake_jimeng_site, negative_box=True)
    prepared = backend.prepare("job_negative", frozen(repo, negative="人群, 水印"), PreparingStep.FILL)
    assert prepared.pause_reason is None, prepared.message
    assert prepared.message == NEGATIVE_ENTERED and backend.negative_prompt_entered("job_negative") is True
    value = client.run(lambda session: session.page.get_by_label("负向提示词", exact=True).input_value())
    assert value == "人群, 水印"


def test_health_canary_is_read_only(backend: WebUiBackend, fake_jimeng_site: FakeJimengSite) -> None:  # noqa: F811
    health = backend.health()
    assert health.ok and health.pause_reason is None, health
    assert health.version == "7.5.0-fake"
    counts = fake_jimeng_site.counts()
    assert (counts["generate_clicks"], counts["param_sets"], counts["uploads"]) == (0, 0, 0)


def test_layout_change_breaks_the_page_contract(backend: WebUiBackend, fake_jimeng_site: FakeJimengSite) -> None:  # noqa: F811
    fake_jimeng_site.inject("layout_next", times=1)
    time.sleep(0.8)
    health = backend.health()
    assert health.pause_reason is PauseReason.PAGE_CONTRACT_BROKEN
    assert {"editor", "generate_button"} <= set(health.failed_checks)


def test_pre_click_parallel_notice_does_not_click(backend: WebUiBackend, fake_jimeng_site: FakeJimengSite, client: JimengBrowserClient, repo: Path) -> None:  # noqa: F811
    fresh_page(client, fake_jimeng_site, external_running=3)
    request = frozen(repo)
    assert backend.prepare("job_busy", request, PreparingStep.VERIFY).pause_reason is None
    outcome = backend.submit("job_busy", request)
    assert (outcome.platform_task_id, outcome.rejection) == (None, None)
    assert outcome.message is not None and outcome.message.startswith(CONCURRENCY_LIMIT_PRE_CLICK)
    assert outcome.message.startswith(NOT_NOW_PREFIX)
    assert fake_jimeng_site.counts()["generate_clicks"] == 0


def test_post_click_parallel_limit_is_a_rejection_and_never_reclicked(backend: WebUiBackend, fake_jimeng_site: FakeJimengSite, repo: Path) -> None:  # noqa: F811
    request = frozen(repo)
    assert backend.prepare("job_backpressure", request, PreparingStep.VERIFY).pause_reason is None
    fake_jimeng_site.inject("backpressure", times=1)
    outcome = backend.submit("job_backpressure", request)
    assert outcome.rejection is PauseReason.SUBMIT_REJECTED and outcome.rejection in POST_CLICK_REJECTIONS
    assert outcome.platform_task_id is None and "并行任务已达上限" in (outcome.message or "")
    counts = fake_jimeng_site.counts()
    assert (counts["generate_clicks"], counts["accepted_submits"]) == (1, 0)


def test_unknown_submit_outcome_is_submit_unconfirmed(backend: WebUiBackend, fake_jimeng_site: FakeJimengSite, repo: Path) -> None:  # noqa: F811
    request = frozen(repo)
    assert backend.prepare("job_unknown", request, PreparingStep.VERIFY).pause_reason is None
    fake_jimeng_site.hold("submit_response")
    try:
        outcome = backend.submit("job_unknown", request)
    finally:
        fake_jimeng_site.release("submit_response")
        deadline = time.monotonic() + 5
        while not fake_jimeng_site.state.ledger.submits and time.monotonic() < deadline:
            time.sleep(0.05)
    assert (outcome.platform_task_id, outcome.rejection) == (None, PauseReason.SUBMIT_UNCONFIRMED)
    assert fake_jimeng_site.counts()["generate_clicks"] == 1


def test_hidden_submit_response_falls_back_to_history(backend: WebUiBackend, fake_jimeng_site: FakeJimengSite, repo: Path) -> None:  # noqa: F811
    request = frozen(repo)
    assert backend.prepare("job_hidden", request, PreparingStep.VERIFY).pause_reason is None
    fake_jimeng_site.inject("submit_response_hidden", times=1)
    outcome = backend.submit("job_hidden", request)
    (hidden,) = [s for s in fake_jimeng_site.state.ledger.submits if str(s["path"]).endswith("generate_alt")]
    assert hidden["accepted"] and outcome.platform_task_id == hidden["task_id"] and "history" in (outcome.message or "")
    assert fake_jimeng_site.counts()["generate_clicks"] == 1


def test_captcha_pauses_the_queue_without_touching_it(backend: WebUiBackend, fake_jimeng_site: FakeJimengSite, repo: Path) -> None:  # noqa: F811
    fake_jimeng_site.inject("captcha_popup", times=1)
    prepared = backend.prepare("job_captcha", frozen(repo), PreparingStep.VERIFY)
    assert prepared.pause_reason is PauseReason.CAPTCHA_OR_RISK_POPUP, prepared.message
    counts = fake_jimeng_site.counts()
    assert (counts["generate_clicks"], counts["uploads"]) == (0, 0)


def test_login_expired_pauses_with_login_expired(backend: WebUiBackend, fake_jimeng_site: FakeJimengSite, repo: Path) -> None:  # noqa: F811
    fake_jimeng_site.inject("login_expired", times=1)
    time.sleep(0.6)
    prepared = backend.prepare("job_login", frozen(repo), PreparingStep.VERIFY)
    assert prepared.pause_reason is PauseReason.LOGIN_EXPIRED, prepared.message
    assert backend.health().pause_reason is PauseReason.LOGIN_EXPIRED
    assert fake_jimeng_site.counts()["login_inputs"] == 0


def test_insufficient_credit_after_click(backend: WebUiBackend, fake_jimeng_site: FakeJimengSite, repo: Path) -> None:  # noqa: F811
    request = frozen(repo)
    assert backend.prepare("job_credit", request, PreparingStep.VERIFY).pause_reason is None
    fake_jimeng_site.inject("insufficient_credit", times=1)
    outcome = backend.submit("job_credit", request)
    assert outcome.rejection is PauseReason.SUBMIT_REJECTED and "积分不足" in (outcome.message or "")
    assert backend.health().pause_reason is PauseReason.INSUFFICIENT_CREDIT
    assert fake_jimeng_site.counts()["generate_clicks"] == 1


def test_upload_rejection_is_retried_then_upload_rejected(client: JimengBrowserClient, fake_jimeng_site: FakeJimengSite, repo: Path, tmp_path: Path) -> None:  # noqa: F811
    backend = make_backend(client, fake_jimeng_site, repo, tmp_path, upload=3)
    fake_jimeng_site.inject("upload_reject", times=10, stem="p2-1")
    prepared = backend.prepare("job_upload", frozen(repo), PreparingStep.VERIFY)
    assert (prepared.reached_step, prepared.pause_reason) == (PreparingStep.UPLOAD, PauseReason.UPLOAD_REJECTED)
    assert len([u for u in fake_jimeng_site.state.ledger.uploads if u["stem"] == "p2-1"]) == 4
    assert fake_jimeng_site.counts()["generate_clicks"] == 0


def test_real_face_notice_fails_without_retry(backend: WebUiBackend, fake_jimeng_site: FakeJimengSite, repo: Path) -> None:  # noqa: F811
    fake_jimeng_site.inject("real_face_rejected", times=5, stem="bg11-1")
    prepared = backend.prepare("job_face", frozen(repo), PreparingStep.VERIFY)
    assert prepared.pause_reason is PauseReason.REAL_FACE_REJECTED
    assert len(fake_jimeng_site.state.ledger.uploads) == 1


def test_inputs_changed_after_confirmation(backend: WebUiBackend, fake_jimeng_site: FakeJimengSite, repo: Path, tmp_path: Path) -> None:  # noqa: F811
    request = frozen(repo)
    target = repo / ASSETS["p3-1"][1]
    original = target.read_bytes()
    make_png(target, (1, 2, 3))
    try:
        prepared = backend.prepare("job_changed", request, PreparingStep.VERIFY)
    finally:
        target.write_bytes(original)
    assert prepared.pause_reason is PauseReason.INPUTS_CHANGED and "p3-1" in (prepared.message or "")
    assert fake_jimeng_site.counts()["uploads"] == 0


@pytest.mark.parametrize(("times", "expected"), [(2, None), (3, PauseReason.FILL_MISMATCH)])
def test_append_on_refill_is_caught_by_verify(
    backend: WebUiBackend, fake_jimeng_site: FakeJimengSite, client: JimengBrowserClient, repo: Path, times: int, expected: PauseReason | None  # noqa: F811
) -> None:
    fresh_page(client, fake_jimeng_site, draft="上次没发出去的草稿")
    fake_jimeng_site.inject("editor_append_on_refill", times=times)
    prepared = backend.prepare("job_refill", frozen(repo), PreparingStep.VERIFY)
    assert prepared.pause_reason is expected, prepared.message
    assert fake_jimeng_site.counts()["generate_clicks"] == 0


def test_control_readback_mismatch_exhausts_retries(client: JimengBrowserClient, fake_jimeng_site: FakeJimengSite, repo: Path, tmp_path: Path) -> None:  # noqa: F811
    backend = make_backend(client, fake_jimeng_site, repo, tmp_path, set_params=1)
    fake_jimeng_site.inject("control_readback_mismatch", times=10, control="duration", display="15")
    prepared = backend.prepare("job_readback", frozen(repo), PreparingStep.SET_PARAMS)
    assert prepared.pause_reason is PauseReason.STEP_FAILED and "时长" in (prepared.message or "")
    assert len([p for p in fake_jimeng_site.state.ledger.param_sets if p["control"] == "duration"]) == 2


def test_moderation_reject_surfaces_on_poll(backend: WebUiBackend, fake_jimeng_site: FakeJimengSite, repo: Path) -> None:  # noqa: F811
    fake_jimeng_site.inject("moderation_reject", times=1)
    task_id = prepared_and_submitted(backend, repo, "job_moderation")
    result = poll_until(backend, task_id, lambda r: r.status is RemoteStatus.FAILED)
    assert (result.status, result.failure) == (RemoteStatus.FAILED, PauseReason.MODERATION_REJECT)
    assert fake_jimeng_site.counts()["generate_clicks"] == 1


def test_malformed_status_bodies_break_the_contract_at_threshold(backend: WebUiBackend, fake_jimeng_site: FakeJimengSite, repo: Path) -> None:  # noqa: F811
    fake_jimeng_site.hold("completion")
    try:
        task_id = prepared_and_submitted(backend, repo, "job_malformed")
        assert poll_until(backend, task_id, lambda r: r.status is RemoteStatus.GENERATING).failure is None
        fake_jimeng_site.inject("status_malformed", times=40)
        result = poll_until(backend, task_id, lambda r: r.failure is not None, timeout_s=10)
    finally:
        fake_jimeng_site.release("completion")
    assert result.failure is PauseReason.PAGE_CONTRACT_BROKEN


def test_page_reload_mid_generation_keeps_observing(backend: WebUiBackend, fake_jimeng_site: FakeJimengSite, repo: Path) -> None:  # noqa: F811
    fake_jimeng_site.hold("completion")
    task_id = prepared_and_submitted(backend, repo, "job_reload")
    loads = fake_jimeng_site.counts()["page_loads"]
    fake_jimeng_site.inject("page_reload_mid_generation", times=1)
    deadline = time.monotonic() + 5
    while fake_jimeng_site.counts()["page_loads"] == loads and time.monotonic() < deadline:
        time.sleep(0.1)
    fake_jimeng_site.release("completion")
    assert fake_jimeng_site.counts()["page_loads"] > loads
    assert poll_until(backend, task_id, lambda r: r.status is RemoteStatus.SUCCEEDED).status is RemoteStatus.SUCCEEDED
    assert fake_jimeng_site.counts()["generate_clicks"] == 1


def test_truncated_download_is_retryable(backend: WebUiBackend, fake_jimeng_site: FakeJimengSite, repo: Path) -> None:  # noqa: F811
    task_id = prepared_and_submitted(backend, repo, "job_truncated")
    assert poll_until(backend, task_id, lambda r: r.status is RemoteStatus.SUCCEEDED).status is RemoteStatus.SUCCEEDED
    fake_jimeng_site.inject("download_truncated", times=1)
    with pytest.raises(WebBackendError) as caught:
        backend.download("job_truncated", task_id)
    assert caught.value.reason is PauseReason.DOWNLOAD_FAILED and caught.value.retryable
    retried = backend.download("job_truncated", task_id)
    assert retried.sha256 == hashlib.sha256(fake_jimeng_site.video.data).hexdigest()


def test_browser_closed_mid_step_is_browser_lost(fake_jimeng_site: FakeJimengSite, repo: Path, tmp_path: Path) -> None:  # noqa: F811
    lost_client = start_client(fake_jimeng_site, tmp_path / "lost_profile")
    try:
        backend = make_backend(lost_client, fake_jimeng_site, repo, tmp_path)
        fake_jimeng_site.hold("upload_done")
        results: list[object] = []
        worker = threading.Thread(target=lambda: results.append(backend.prepare("job_lost", frozen(repo), PreparingStep.VERIFY)))
        worker.start()
        session: BrowserSession = lost_client._session  # type: ignore[assignment]
        loop = lost_client._loop
        assert loop is not None
        deadline = time.monotonic() + 15
        while time.monotonic() < deadline:
            if asyncio.run_coroutine_threadsafe(session.page.locator(".ref-tile").count(), loop).result(5):
                break
            time.sleep(0.1)
        asyncio.run_coroutine_threadsafe(session.page.close(), loop).result(10)
        worker.join(timeout=30)
        fake_jimeng_site.release("upload_done")
        (prepared,) = results
        assert prepared.pause_reason is PauseReason.BROWSER_LOST  # type: ignore[attr-defined]
        assert backend.poll("anything").failure is PauseReason.BROWSER_LOST
        recovered = backend.recover_browser()
        assert recovered.ok, recovered
    finally:
        fake_jimeng_site.release("upload_done")
        lost_client.close()
    assert fake_jimeng_site.counts()["generate_clicks"] == 0


def test_entity_gateway_sync_create_reuse_and_unverified(client: JimengBrowserClient, fake_jimeng_site: FakeJimengSite, repo: Path) -> None:  # noqa: F811
    fresh_page(client, fake_jimeng_site)
    gateway = WebEntityGateway(client, sync_timeout_s=8.0)
    names = [item["name"] for item in gateway.sync_snapshot()]
    assert "hy3_主角" in names

    portrait = repo / CHARACTER_CARD
    created = gateway.create("hy3_獾", "灰褐色的獾", [portrait])
    assert (created["created"], created["reused"], created["verified"]) == (True, False, True)
    (save,) = fake_jimeng_site.state.ledger.entity_saves
    assert (save["name"], save["description"]) == ("hy3_獾", "灰褐色的獾")

    reused = gateway.create("hy3_獾", "灰褐色的獾", [portrait])
    assert (reused["created"], reused["reused"]) == (False, True)
    assert len(fake_jimeng_site.state.ledger.entity_saves) == 1

    fake_jimeng_site.inject("entity_save_fail", times=1)
    unverified = gateway.create("hy3_狐", "", [portrait])
    assert (unverified["created"], unverified["verified"]) == (True, False)

    with pytest.raises(WebBackendError):
        gateway.create("名" * 21, "", [portrait])
    assert fake_jimeng_site.counts()["generate_clicks"] == 0
