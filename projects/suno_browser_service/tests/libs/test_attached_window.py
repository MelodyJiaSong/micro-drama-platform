"""常驻窗口模式：服务接管人一直开着的 Chrome（本机调试端口），不自己启动浏览器；用假 Playwright，不启动浏览器。"""

import time
from pathlib import Path

import pytest

from projects.suno_browser_service.libs.application.commands.runtime__command import RuntimeCommand
from projects.suno_browser_service.libs.common.errors import ServiceError
from projects.suno_browser_service.libs.common.settings import Settings
from projects.suno_browser_service.libs.infrastructure.clients import browser__client, manual_browser__client
from projects.suno_browser_service.libs.infrastructure.clients.audit__client import AuditClient
from projects.suno_browser_service.libs.infrastructure.clients.browser__client import BrowserClient


class FakePage:
    def __init__(self, context) -> None:
        self.context = context
        self.closed = False
        self.handlers: dict = {}

    def is_closed(self) -> bool:
        return self.closed

    def on(self, event, handler) -> None:
        self.handlers[event] = handler

    def close(self, run_before_unload: bool = True) -> None:
        self.closed = True


class FakeContext:
    def __init__(self) -> None:
        self.pages = [FakePage(self)]  # 人自己的标签页

    def new_page(self):
        self.pages.append(FakePage(self))
        return self.pages[-1]


class FakeBrowser:
    def __init__(self) -> None:
        self.contexts = [FakeContext()]
        self.connected = True
        self.closed = False

    def is_connected(self) -> bool:
        return self.connected

    def close(self) -> None:
        self.closed = True


class FakePlaywright:
    def __init__(self) -> None:
        self.chromium = self
        self.urls: list[str] = []
        self.browsers: list[FakeBrowser] = []
        self.stopped = False

    def connect_over_cdp(self, url, **_kwargs):
        self.urls.append(url)
        self.browsers.append(FakeBrowser())
        return self.browsers[-1]

    def launch_persistent_context(self, *_args, **_kwargs):
        raise AssertionError("常驻窗口模式不能自己启动 Chrome")

    def stop(self) -> None:
        self.stopped = True


@pytest.fixture
def fake(monkeypatch: pytest.MonkeyPatch):
    playwrights: list[FakePlaywright] = []
    state = {"open": True}

    class Starter:
        def start(self):
            playwrights.append(FakePlaywright())
            return playwrights[-1]

    monkeypatch.setattr(browser__client, "sync_playwright", lambda: Starter())
    monkeypatch.setattr(browser__client, "window_open", lambda _settings: state["open"])
    return playwrights, state


def settings(tmp_path: Path) -> Settings:
    return Settings(tmp_path / "data", attach_port=9333, keep_browser=True, headless=True)


def test_attached_mode_connects_to_open_window_and_uses_own_tab(tmp_path: Path, fake):
    playwrights, _state = fake
    audit = AuditClient(tmp_path / "ai_videos" / "attach_fixture")
    client = BrowserClient(settings(tmp_path))
    with client.session(audit) as first:
        work = client.page(first)
    with client.session(audit) as second:
        assert client.page(second) is work
    assert first is second and len(playwrights) == 1 and playwrights[0].urls == ["http://127.0.0.1:9333"]
    assert work is not first.pages[0], "人自己的标签页不被服务占用"

    work.closed = True  # 人把服务的标签页关了
    assert client.page(second) is not work

    client.close()
    assert playwrights[0].stopped and not playwrights[0].browsers[0].closed, "断开连接不关人的窗口"
    assert "browser_attach" in audit.log.path.read_text(encoding="utf-8")


def test_attached_mode_reconnects_after_window_reopened(tmp_path: Path, fake):
    playwrights, _state = fake
    audit = AuditClient(tmp_path / "ai_videos" / "attach_fixture")
    client = BrowserClient(settings(tmp_path))
    with client.session(audit):
        pass
    playwrights[0].browsers[0].connected = False  # 窗口关过又重开
    with client.session(audit):
        pass
    assert len(playwrights) == 2


def test_attached_mode_reports_closed_window(tmp_path: Path, fake):
    _playwrights, state = fake
    state["open"] = False
    with pytest.raises(ServiceError) as error:
        with BrowserClient(settings(tmp_path)).session(AuditClient(tmp_path / "ai_videos" / "attach_fixture")):
            pass
    assert error.value.code == "window_not_open"


def test_env_defaults_to_attached_and_zero_restores_launch(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("SUNO_CLIP_APPEAR_WAIT", raising=False)
    assert Settings.from_env().clip_appear_wait == 0, "实测 3-5 分钟才出现歌曲行，默认不提前报错"
    monkeypatch.delenv("SUNO_WINDOW_AUTO_OPEN", raising=False)
    assert Settings.from_env().window_auto_open and not Settings(Path(".")).window_auto_open
    monkeypatch.delenv("SUNO_BROWSER_ATTACH_PORT", raising=False)
    monkeypatch.delenv("SUNO_BROWSER_WS", raising=False)
    assert Settings.from_env().attached and Settings.from_env().attach_port == 9333
    monkeypatch.setenv("SUNO_BROWSER_ATTACH_PORT", "0")
    assert not Settings.from_env().attached
    monkeypatch.setenv("SUNO_BROWSER_ATTACH_PORT", "9333")
    monkeypatch.setenv("SUNO_BROWSER_WS", "ws://remote")
    assert not Settings.from_env().attached, "远程 Browserless 不走本机窗口"


def test_window_probe_is_false_without_listener(tmp_path: Path):
    assert manual_browser__client.window_open(Settings(tmp_path, attach_port=1)) is False
    assert manual_browser__client.window_open(Settings(tmp_path)) is False


class SilentUi:
    """Create 之后一直没有本任务的歌曲行。"""

    def __init__(self, human_cleared_at: float = 0.0) -> None:
        self.human_cleared_at = human_cleared_at
        self.calls = 0
        self.refreshes = 0

        self.sent = True
        self.direct: list[str] = []

    def refresh(self) -> None:
        self.refreshes += 1

    def create_sent(self) -> bool:
        return self.sent

    def created_songs(self) -> list[str]:
        return self.direct

    def collect(self, _title, _baseline):
        self.calls += 1
        return []


def test_no_clip_after_create_is_reported_early(tmp_path: Path):
    runtime = RuntimeCommand(Settings(tmp_path, poll_seconds=0.05, generation_timeout=600))
    started = time.monotonic()
    with pytest.raises(ServiceError) as error:
        runtime.claim(None, SilentUi(), "t", [], appear_wait=0.3)
    assert error.value.code == "no_clip_seen" and time.monotonic() - started < 5


def test_work_tab_is_reloaded_while_waiting_after_create(tmp_path: Path):
    runtime = RuntimeCommand(Settings(tmp_path, poll_seconds=0.05, refresh_seconds=0.1))
    ui = SilentUi()
    with pytest.raises(ServiceError):
        runtime.claim(None, ui, "t", [], timeout=0.5, refresh=True)
    assert ui.refreshes >= 2
    recollect = SilentUi()
    with pytest.raises(ServiceError):
        runtime.claim(None, recollect, "t", [], timeout=0.3)
    assert recollect.refreshes == 0, "recollect 已经是新打开的页面"


def test_tab_is_not_reloaded_before_suno_sent_the_create(tmp_path: Path):
    runtime = RuntimeCommand(Settings(tmp_path, poll_seconds=0.05, refresh_seconds=0.1))
    ui = SilentUi()
    ui.sent = False
    with pytest.raises(ServiceError):
        runtime.claim(None, ui, "t", [], timeout=0.5, refresh=True)
    assert ui.refreshes == 0, "生成请求还没发出时刷新会打断 Create"


def test_tab_is_reloaded_when_create_answer_never_seen(tmp_path: Path):
    """2026-11-03 ep13: created, answer never seen, list never refreshed, 10 minutes later uncertain."""
    runtime = RuntimeCommand(Settings(tmp_path, poll_seconds=0.05, refresh_seconds=0.1, unanswered_create_wait=0.3))
    ui = SilentUi()
    ui.sent = False
    with pytest.raises(ServiceError):
        runtime.claim(None, ui, "t", [], timeout=0.8, refresh=True)
    assert ui.refreshes >= 2


class FakeJob:
    def __init__(self) -> None:
        self.payload: dict = {}
        self.status = "waiting"
        self.version = 0


def test_clip_ids_from_create_answer_are_claimed_directly(tmp_path: Path):
    runtime = RuntimeCommand(Settings(tmp_path, poll_seconds=0.05))
    ui = SilentUi()
    ui.direct = ["https://suno.com/song/" + "1" * 8 + "-1111-4111-8111-" + "1" * 12,
                 "https://suno.com/song/" + "2" * 8 + "-2222-4222-8222-" + "2" * 12]
    changes = []
    runtime.change = lambda job, status=None, **fields: changes.append((status, fields))
    runtime.claim(FakeJob(), ui, "t", [], timeout=5, refresh=True)
    assert changes == [("downloading", {"song_urls": ui.direct})] and ui.calls == 0


def test_time_spent_by_person_does_not_count(tmp_path: Path):
    runtime = RuntimeCommand(Settings(tmp_path, poll_seconds=0.05, generation_timeout=600))
    ui = SilentUi(human_cleared_at=time.monotonic() + 0.5)  # 人刚做完验证
    started = time.monotonic()
    with pytest.raises(ServiceError):
        runtime.claim(None, ui, "t", [], appear_wait=0.3)
    assert time.monotonic() - started >= 0.75


def test_recollect_keeps_plain_timeout(tmp_path: Path):
    runtime = RuntimeCommand(Settings(tmp_path, poll_seconds=0.05))
    with pytest.raises(ServiceError) as error:
        runtime.claim(None, SilentUi(), "t", [], timeout=0.3)
    assert error.value.code == "generation_timeout"


class FakeDialog:
    def __init__(self, kind: str) -> None:
        self.type, self.answer = kind, None

    def accept(self) -> None:
        self.answer = "accept"

    def dismiss(self) -> None:
        self.answer = "dismiss"


def test_work_tab_leaves_on_leave_site_dialog_and_can_be_replaced(tmp_path: Path, fake):
    """2026-11-03: a dismissed "Leave site?" kept the work tab in place and 14 jobs timed out navigating."""
    audit = AuditClient(tmp_path / "ai_videos" / "attach_fixture")
    client = BrowserClient(settings(tmp_path))
    with client.session(audit) as context:
        work = client.page(context)
        leave, other = FakeDialog("beforeunload"), FakeDialog("alert")
        work.handlers["dialog"](leave)
        work.handlers["dialog"](other)
        assert (leave.answer, other.answer) == ("accept", "dismiss")
        fresh = client.renew_page(context)
        assert work.closed and fresh is not work and client.page(context) is fresh
        assert not context.pages[0].closed, "人自己的标签页不动"


class Body:
    def wait_for(self) -> None:
        pass


class LoadingPage:
    def __init__(self, stuck: bool) -> None:
        self.stuck, self.url, self.calls = stuck, "", 0

    def goto(self, url, **_kwargs) -> None:
        self.calls += 1
        if self.stuck:
            from playwright.sync_api import TimeoutError as PlaywrightTimeout
            raise PlaywrightTimeout("Page.goto: Timeout 60000ms exceeded.")
        self.url = url

    def locator(self, _selector):
        return Body()


def suno_ui(tmp_path: Path, page):
    from projects.suno_browser_service.libs.infrastructure.clients.suno__client import SunoClient
    ui = SunoClient(page, AuditClient(tmp_path / "ai_videos" / "attach_fixture"), tmp_path / "selectors.json")
    ui.guard = lambda: None
    return ui


def test_stuck_work_tab_is_replaced_once_and_navigation_retried(tmp_path: Path):
    stuck, fresh = LoadingPage(True), LoadingPage(False)
    ui = suno_ui(tmp_path, stuck)
    ui.renew_page = lambda: fresh
    ui.navigate("https://suno.com/create")
    assert ui.page is fresh and fresh.url == "https://suno.com/create" and stuck.calls == 1
    assert "work_tab_renewed" in (tmp_path / "ai_videos" / "attach_fixture" / "request_log.md").read_text(encoding="utf-8")

    still = suno_ui(tmp_path, LoadingPage(True))
    still.renew_page = lambda: LoadingPage(True)
    with pytest.raises(Exception, match="Timeout"):
        still.navigate("https://suno.com/create")


def test_without_renew_hook_timeout_is_reported(tmp_path: Path):
    with pytest.raises(Exception, match="Timeout"):
        suno_ui(tmp_path, LoadingPage(True)).navigate("https://suno.com/create")


class RetryJob:
    def __init__(self, status: str = "queued") -> None:
        self.payload = {"target": "", "song_urls": [], "files": []}
        self.status = status
        self.id = "job"


class BrokenSession:
    def __enter__(self):
        raise ServiceError("window_not_open", "closed")

    def __exit__(self, *_args):
        return False


def runtime_with_broken_window(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, freeze_status: str | None = None):
    from projects.suno_browser_service.libs.application.commands import runtime__command
    runtime = RuntimeCommand(Settings(tmp_path / "data", attach_port=9333))
    statuses: list = []

    def change(job, status=None, **fields):
        statuses.append(status)
        job.payload.update(fields)
        if status and not (freeze_status and status == "preparing"):
            job.status = status
    runtime.change = change
    runtime.stop_event.wait = lambda _seconds=None: False
    monkeypatch.setattr(runtime.browser, "session", lambda _audit: BrokenSession())
    monkeypatch.setattr(runtime__command, "AuditClient", lambda _target: None)
    return runtime, statuses


def test_window_failure_before_submit_requeues_up_to_three_times(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    runtime, statuses = runtime_with_broken_window(tmp_path, monkeypatch)
    job = RetryJob()
    for _ in range(4):
        runtime.process(job)
    assert statuses.count("queued") == 3 and job.status == "needs_attention" and job.payload["transient_retries"] == 3


def test_failure_after_create_is_never_retried(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    runtime, statuses = runtime_with_broken_window(tmp_path, monkeypatch, freeze_status="preparing")
    job = RetryJob("submitting")  # as if Create had been clicked when the window broke
    runtime.process(job)
    assert "queued" not in statuses and job.status == "uncertain"


def test_worker_reopens_stuck_window_at_most_once_a_minute(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    from projects.suno_browser_service.libs.application.commands import runtime__command
    calls = []

    class Manual:
        def __init__(self, _settings):
            pass

        def profile_in_use(self):
            return True

        def end_profile_processes(self):
            calls.append("end")
            return {"ended": 1, "profile_free": True}

        def open_window(self, _audit):
            calls.append("open")
            return "ok"
    monkeypatch.setattr(runtime__command, "ManualBrowserClient", Manual)
    runtime = RuntimeCommand(Settings(tmp_path / "ai_videos" / "data", attach_port=9333, window_auto_open=True))
    runtime.reopen_window()
    runtime.reopen_window()
    assert calls == ["end", "open"]
    assert "window_stuck_end" in (tmp_path / "ai_videos" / "data" / "request_log.md").read_text(encoding="utf-8")

    off = RuntimeCommand(Settings(tmp_path / "data2", attach_port=9333))
    off.reopen_window()
    assert calls == ["end", "open"], "SUNO_WINDOW_AUTO_OPEN=0 不自动开窗"


def test_profile_processes_ignores_chrome_on_other_profiles(tmp_path: Path):
    from projects.suno_browser_service.libs.infrastructure.clients.manual_browser__client import ManualBrowserClient
    assert ManualBrowserClient(Settings(tmp_path / "no-chrome-uses-this")).profile_processes() == []


def test_window_keeps_rendering_when_covered(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Throttled background window: form slower than the control wait, screenshots hung (2026-11-03)."""
    launched = []

    class Process:
        pid = 1

    states = iter([False, True])
    monkeypatch.setattr(manual_browser__client, "window_open", lambda _settings: next(states))
    monkeypatch.setattr(manual_browser__client.subprocess, "Popen", lambda argv, **_kwargs: launched.append(argv) or Process())
    client = manual_browser__client.ManualBrowserClient(Settings(tmp_path / "ai_videos" / "data", attach_port=9333))
    monkeypatch.setattr(client, "executable", lambda: Path("chrome.exe"))
    client.open_window(AuditClient(tmp_path / "ai_videos" / "data"))
    argv = launched[0]
    assert {"--disable-backgrounding-occluded-windows", "--disable-renderer-backgrounding",
            "--disable-background-timer-throttling"} <= set(argv)
    assert any(arg.startswith("--remote-debugging-port=") for arg in argv)
    assert not any("automation" in arg.lower() for arg in argv), "不隐藏自动化特征"


def test_jammed_port_moves_window_to_next_free_port(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    import socket
    jam = socket.socket()
    jam.bind(("127.0.0.1", 0))
    jam.listen()
    taken = jam.getsockname()[1]
    try:
        assert not manual_browser__client.port_free(taken)
        launched = []

        class Process:
            pid = 1
        states = iter([False, True])
        monkeypatch.setattr(manual_browser__client, "window_open", lambda _settings: next(states))
        monkeypatch.setattr(manual_browser__client.subprocess, "Popen", lambda argv, **_kwargs: launched.append(argv) or Process())
        config = Settings(tmp_path / "ai_videos" / "data", attach_port=taken)
        config.data_dir.mkdir(parents=True)
        client = manual_browser__client.ManualBrowserClient(config)
        monkeypatch.setattr(client, "executable", lambda: Path("chrome.exe"))
        client.open_window(AuditClient(config.data_dir))
        used = int(next(a for a in launched[0] if a.startswith("--remote-debugging-port=")).split("=")[1])
        assert used != taken and config.window_port == used and config.cdp_url == f"http://127.0.0.1:{used}"
    finally:
        jam.close()
    assert Settings(tmp_path / "other", attach_port=9333).cdp_url == "http://127.0.0.1:9333"


class ConsentButton:
    def __init__(self, page, name: str) -> None:
        self.page, self.name = page, name

    def filter(self, visible: bool):
        return self

    def count(self) -> int:
        return 1 if self.page.banner and self.name in self.page.buttons else 0

    @property
    def first(self):
        return self

    def click(self, timeout: int = 0) -> None:
        self.page.clicked.append(self.name)
        self.page.banner = False


class ConsentBanner:
    def __init__(self, page) -> None:
        self.page = page

    def count(self) -> int:
        return 1 if self.page.banner else 0

    def get_by_role(self, role: str, name):
        return ConsentButton(self.page, next((b for b in self.page.buttons if name.search(b)), ""))


class ConsentPage:
    def __init__(self, buttons) -> None:
        self.banner, self.buttons, self.clicked = True, buttons, []

    def locator(self, selector: str):
        class Selector:
            first = selector
        return ConsentBanner(self) if selector == "#cmp-banner-container" else Selector()

    def wait_for_timeout(self, _ms) -> None:
        pass


def test_cookie_banner_over_create_is_declined(tmp_path: Path):
    """2026-11-03: the consent banner intercepted the click on Create; Reject All keeps only necessary cookies."""
    page = ConsentPage(["Customize cookie preferences", "Deny all optional cookies", "Accept all cookies"])
    ui = suno_ui(tmp_path, page)
    ui.dismiss_consent()
    ui.dismiss_consent()
    assert page.clicked == ["Deny all optional cookies"], "Suno 的 Reject All 按钮可访问名称是 Deny all optional cookies"
    assert "consent_reject" in (tmp_path / "ai_videos" / "attach_fixture" / "request_log.md").read_text(encoding="utf-8")
    accept_only = ConsentPage(["Accept all cookies"])
    suno_ui(tmp_path, accept_only).dismiss_consent()
    assert accept_only.clicked == [], "没有拒绝选项时不替用户点同意"


def test_hung_tabs_are_closed_through_the_browser(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """2026-11-03: two hung /create tabs made every connect time out (window_not_open)."""
    import io
    import json as json_
    import websockets.sync.client as ws_client
    targets = [{"type": "page", "id": "OK", "url": "https://suno.com/create", "webSocketDebuggerUrl": "ws://ok"},
               {"type": "page", "id": "HUNG", "url": "https://suno.com/create", "webSocketDebuggerUrl": "ws://hung"},
               {"type": "iframe", "id": "F", "url": "https://js.stripe.com/x", "webSocketDebuggerUrl": "ws://f"}]
    opened = []

    class Response(io.BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

    def urlopen(url, timeout=0):
        opened.append(url)
        return Response(json_.dumps(targets).encode() if url.endswith("/json") else b"Target is closing")

    class Socket:
        def __init__(self, url):
            self.url = url

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def send(self, _message):
            pass

        def recv(self, timeout=0):
            if self.url == "ws://hung":
                raise TimeoutError
            return json_.dumps({"id": 1, "result": {"result": {"value": 1}}})

    monkeypatch.setattr(manual_browser__client.urllib.request, "urlopen", urlopen)
    monkeypatch.setattr(ws_client, "connect", lambda url, **_kwargs: Socket(url))
    result = manual_browser__client.close_hung_tabs(Settings(tmp_path, attach_port=9333), wait=0.2)
    assert result == {"pages": 2, "closed": ["/create"]}
    assert opened[-1].endswith("/json/close/HUNG") and not any(u.endswith("/close/OK") or u.endswith("/close/F") for u in opened)


def test_attach_retries_once_after_closing_hung_tabs(tmp_path: Path, fake, monkeypatch: pytest.MonkeyPatch):
    playwrights, _state = fake
    calls = []
    monkeypatch.setattr(browser__client, "close_hung_tabs", lambda _settings: calls.append("close") or {"pages": 2, "closed": ["/create"]})
    original = FakePlaywright.connect_over_cdp

    def flaky(self, url, **kwargs):
        if not calls:
            raise TimeoutError("connect_over_cdp: Timeout 15000ms exceeded")
        return original(self, url, **kwargs)
    monkeypatch.setattr(FakePlaywright, "connect_over_cdp", flaky)
    audit = AuditClient(tmp_path / "ai_videos" / "attach_fixture")
    with BrowserClient(settings(tmp_path)).session(audit) as context:
        assert context is playwrights[0].browsers[0].contexts[0]
    assert calls == ["close"] and "close_hung_tabs" in audit.log.path.read_text(encoding="utf-8")

    calls.clear()
    monkeypatch.setattr(browser__client, "close_hung_tabs", lambda _settings: calls.append("close") or {"pages": 1, "closed": []})
    monkeypatch.setattr(FakePlaywright, "connect_over_cdp", lambda self, url, **kw: (_ for _ in ()).throw(TimeoutError("t")))
    with pytest.raises(ServiceError) as error:
        with BrowserClient(settings(tmp_path)).session(audit):
            pass
    assert error.value.code == "window_not_open" and calls == ["close"]


def test_consent_handler_is_registered_once_per_tab(tmp_path: Path):
    class HandlerPage(ConsentPage):
        def __init__(self):
            super().__init__(["Reject All"])
            self.handlers = []

        def locator(self, selector: str):
            class Selector:
                first = selector
            return Selector() if selector != "#cmp-banner-container" else ConsentBanner(self)

        def add_locator_handler(self, locator, handler):
            self.handlers.append((locator, handler))

        def remove_locator_handler(self, locator):
            self.handlers = [h for h in self.handlers if h[0] != locator]

    page = HandlerPage()
    first = suno_ui(tmp_path, page)
    suno_ui(tmp_path, page)
    assert len(page.handlers) == 1 and page.handlers[0][0] == "#cmp-banner-container [role=dialog]:not([inert])"
    page.handlers[0][1]()
    assert page.clicked == ["Reject All"] and first is not None


CLEAR_PAGE = """<button aria-label="Clear all form inputs" onclick="document.getElementById('ask').hidden=false;
  document.getElementById('form').setAttribute('aria-hidden','true')">x</button>
<div id="form"><div role="tablist"><button role="tab">Advanced</button></div><textarea id="style">old prompt</textarea></div>
<div id="ask" role="alertdialog" aria-modal="true" hidden><p>Clear entire form?</p><p>This will reset all your inputs.</p>
  <button aria-label="Confirm clearing the form" onclick="document.getElementById('style').value='';document.getElementById('ask').hidden=true;
  document.getElementById('form').removeAttribute('aria-hidden')">Confirm</button><button>Cancel</button></div>"""


def test_clear_form_confirms_suno_modal_so_form_is_reachable_again():
    """2026-11-03: Suno's "Clear entire form?" modal hid the form; every job failed as ui_changed on Advanced."""
    from playwright.sync_api import sync_playwright
    from projects.suno_browser_service.libs.infrastructure.clients.form__client import FormClient

    class Ui:
        pass
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="chrome", headless=True)
        try:
            page = browser.new_page()
            page.set_content(CLEAR_PAGE)
            ui = Ui()
            ui.page = page
            FormClient(ui).clear_form()
            assert page.get_by_role("tab", name="Advanced").count() == 1
            assert page.locator("#style").input_value() == "" and page.locator("#ask").is_hidden()
            page.set_content(CLEAR_PAGE.replace('aria-label="Clear all form inputs"', 'aria-label="Clear all form inputs" disabled'))
            FormClient(ui).clear_form()
            assert page.locator("#style").input_value() == "old prompt", "按钮禁用时不点"
        finally:
            browser.close()


def test_out_of_downloads_modal_is_quota_and_pauses(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """2026-11-04: Suno's "Out of Downloads" modal was reported as ui_changed; it is the plan's download cap."""
    from projects.suno_browser_service.libs.infrastructure.clients.suno__client import SunoClient
    from projects.suno_browser_service.libs.infrastructure.readers.runtime__reader import RuntimeReader

    class Body:
        def inner_text(self, timeout=0):
            return "Out of Downloads\nYou've used all your downloads for now.\nDownloads\n0\nRefreshes\n11/25/26"

    class Page:
        def locator(self, selector):
            return Body() if selector == "body" else type("None_", (), {"count": lambda self: 0})()

    ui = SunoClient.__new__(SunoClient)
    ui.page, ui.challenge_wait = Page(), 0
    ui.challenge = lambda _body: None
    with pytest.raises(ServiceError) as error:
        ui.guard()
    assert error.value.code == "quota_exhausted"

    runtime, _statuses = runtime_with_broken_window(tmp_path, monkeypatch)

    class QuotaSession:
        def __enter__(self):
            raise ServiceError("quota_exhausted", "Suno 生成或下载额度不足")

        def __exit__(self, *_args):
            return False
    monkeypatch.setattr(runtime.browser, "session", lambda _audit: QuotaSession())
    job = RetryJob()
    runtime.process(job)
    assert job.status == "needs_attention" and RuntimeReader(runtime.settings.data_dir).automation_paused()
