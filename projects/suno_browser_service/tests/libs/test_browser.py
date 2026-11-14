"""真实 Chrome + 本机 HTTP fixture；不是 Suno 或 Browserless 联调证据。"""

import hashlib
import io
import json
import shutil
import subprocess
import threading
import wave
from collections.abc import Iterator
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

import pytest
from playwright.sync_api import BrowserContext, Route

from projects.suno_browser_service.libs.common.errors import ServiceError
from projects.suno_browser_service.libs.common.settings import Settings
from projects.suno_browser_service.libs.infrastructure.clients.audit__client import AuditClient
from projects.suno_browser_service.libs.infrastructure.clients.browser__client import BrowserClient
from projects.suno_browser_service.libs.infrastructure.clients.suno__client import SunoClient
from projects.suno_browser_service.libs.infrastructure.writers.audio__writer import AudioWriter


SONG_IDS = [f"00000000-0000-4000-8000-{index:012d}" for index in range(1, 5)]
FORM = """<!doctype html><html><body>
<button aria-pressed="false" onclick="this.setAttribute('aria-pressed','true')">Custom</button>
<label>Style of Music<textarea id="style"></textarea></label>
<label>Song Title<input id="title"></label>
<label>Instrumental<input id="instrumental" type="checkbox"></label>
<label>Lyrics<textarea id="lyrics"></textarea></label>
<button id="create">Create</button><div id="songs"></div>
<script>
window.createClicks = 0;
function song(id, title) {
  const link = document.createElement('a');
  link.href = 'https://suno.com/song/' + id;
  link.textContent = title;
  document.querySelector('#songs').append(link);
}
song('00000000-0000-4000-8000-000000000004', 'Existing library song');
document.querySelector('#create').onclick = async () => {
  window.createClicks += 1;
  const payload = Object.fromEntries(['style', 'title', 'lyrics'].map(
    key => [key, document.getElementById(key).value]));
  payload.instrumental = document.querySelector('#instrumental').checked;
  const response = await fetch('/created', {method:'POST', body:JSON.stringify(payload)});
  for (const item of await response.json()) song(item.id, item.title);
};
</script></body></html>"""
SONG = """<!doctype html><html><body><h1>Fixture song</h1>
<button onclick="document.querySelector('#menu').hidden=false">More Actions</button>
<div id="menu" hidden>
  <button onmouseover="document.querySelector('#formats').hidden=false"
          onclick="document.querySelector('#formats').hidden=false">Download</button>
  <div id="formats" hidden>
    <a role="menuitem" href="/audio/fixture.mp3">MP3</a>
    <a role="menuitem" href="/audio/fixture.wav">WAV</a>
  </div>
</div></body></html>"""


@dataclass
class FixtureSite:
    audio: dict[str, bytes]
    base_url: str = ""
    submissions: list[dict] = field(default_factory=list)
    requests: list[str] = field(default_factory=list)
    invalid_audio: bool = False


@pytest.fixture(scope="module")
def fixture_site() -> Iterator[FixtureSite]:
    wav = io.BytesIO()
    with wave.open(wav, "wb") as output:
        output.setparams((1, 2, 8000, 0, "NONE", "not compressed"))
        output.writeframes(b"\0\0" * 800)
    audio = {"wav": wav.getvalue()}
    if ffmpeg := shutil.which("ffmpeg"):
        audio["mp3"] = subprocess.run(
            [ffmpeg, "-v", "error", "-f", "wav", "-i", "pipe:0", "-f", "mp3", "pipe:1"],
            input=audio["wav"], capture_output=True, check=True, timeout=15,
        ).stdout
    site = FixtureSite(audio)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_args: object) -> None:
            pass

        def respond(self, content: bytes, content_type: str, *, download: bool = False) -> None:
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            if download:
                self.send_header("Content-Disposition", 'attachment; filename="fixture-audio"')
            self.end_headers()
            self.wfile.write(content)

        def do_GET(self) -> None:
            site.requests.append(self.path)
            if self.path.startswith("/audio/"):
                format_name = self.path.rsplit(".", 1)[-1]
                payload = b"<html>Account download unavailable</html>" if site.invalid_audio else site.audio[format_name]
                self.respond(payload, "application/octet-stream", download=True)
            else:
                page = SONG if self.path.startswith("/song/") else FORM
                self.respond(page.encode(), "text/html; charset=utf-8")

        def do_POST(self) -> None:
            assert self.path == "/created"
            payload = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            site.submissions.append(payload)
            songs = [{"id": song_id, "title": payload["title"]} for song_id in SONG_IDS[:2]]
            songs.append({"id": SONG_IDS[2], "title": "Unrelated manual generation"})
            self.respond(json.dumps(songs).encode(), "application/json")

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    site.base_url = f"http://127.0.0.1:{server.server_port}"
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield site
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


@pytest.fixture
def browser_context(tmp_path_factory: pytest.TempPathFactory, fixture_site: FixtureSite) -> Iterator[BrowserContext]:
    root = tmp_path_factory.mktemp("suno-browser-offline")
    audit = AuditClient(root / "ai_videos" / "browser_fixture")
    with BrowserClient(Settings(data_dir=root / "browser", channel="chrome")).session(audit) as context:
        def route_fixture(route: Route) -> None:
            url = urlsplit(route.request.url)
            if url.hostname == "suno.com":
                local = fixture_site.base_url + url.path + ("?" + url.query if url.query else "")
                response = route.fetch(url=local)
                route.fulfill(response=response)
            elif url.hostname == "127.0.0.1":
                route.continue_()
            else:
                route.abort("blockedbyclient")

        context.route("**/*", route_fixture)
        yield context


@pytest.fixture
def ui(browser_context: BrowserContext, fixture_site: FixtureSite, tmp_path: Path) -> Iterator[SunoClient]:
    fixture_site.submissions.clear()
    fixture_site.requests.clear()
    fixture_site.invalid_audio = False
    page = browser_context.new_page()
    audit = AuditClient(tmp_path / "ai_videos" / "browser_fixture")
    client = SunoClient(page, audit, tmp_path / "selectors.json")
    client.navigate(fixture_site.base_url + "/create")
    try:
        yield client
    finally:
        page.close()


@pytest.mark.parametrize(("instrumental", "format_name"), [(True, "mp3"), (False, "wav")])
def test_real_chrome_form_create_collect_and_official_download(
    ui: SunoClient, fixture_site: FixtureSite, tmp_path: Path, instrumental: bool, format_name: str,
) -> None:
    if format_name not in fixture_site.audio:
        pytest.skip("MP3 fixture requires local ffmpeg; WAV test still covers HTTP downloads")
    title = "task-7b4a-deadbeef"
    prompt = "温暖钢琴\nA quiet ending with strings"
    lyrics = "A new day\nA new way" if not instrumental else None
    baseline = ui.prepare(prompt, title, instrumental, lyrics)
    assert baseline == [f"https://suno.com/song/{SONG_IDS[3]}"]
    ui.submit(title)
    ui.page.get_by_role("link", name=title, exact=True).first.wait_for()
    songs = ui.collect(title, baseline)
    assert songs == [f"https://suno.com/song/{song_id}" for song_id in SONG_IDS[:2]]
    assert fixture_site.submissions == [{"style": prompt, "title": title, "lyrics": lyrics or "", "instrumental": instrumental}]
    assert ui.page.evaluate("window.createClicks") == 1
    files = [AudioWriter(ui, tmp_path / "audio").download(url, format_name) for url in songs]
    payload = fixture_site.audio[format_name]
    for item in files:
        path = tmp_path / "audio" / item["name"]
        assert path.read_bytes() == payload
        assert item["bytes"] == len(payload)
        assert item["sha256"] == hashlib.sha256(payload).hexdigest()
        assert path.suffix == f".{format_name}"
        assert not path.with_suffix(path.suffix + ".part").exists()
    assert len(fixture_site.submissions) == 1
    assert fixture_site.requests.count(f"/audio/fixture.{format_name}") == 2


@pytest.mark.parametrize(("message", "code"), [
    ("Continue with Google", "needs_login"),
    ("Verify that you are human", "challenge"),
    ("Access denied", "challenge"),
    ("Not enough credits", "quota_exhausted"),
])
def test_login_challenge_or_quota_stops_before_create(ui: SunoClient, fixture_site: FixtureSite, message: str, code: str) -> None:
    ui.page.locator("body").evaluate("(body, text) => body.append(document.createTextNode(text))", message)
    with pytest.raises(ServiceError) as error:
        ui.prepare("test", "task-guard", True, None)
    assert error.value.code == code
    assert ui.page.evaluate("window.createClicks") == 0
    assert fixture_site.submissions == []


def test_duplicate_visible_control_stops_before_create(ui: SunoClient, fixture_site: FixtureSite) -> None:
    ui.page.locator("body").evaluate("body => body.insertAdjacentHTML('beforeend', '<label>Song Title<input></label>')")
    with pytest.raises(ServiceError) as error:
        ui.prepare("test", "task-ambiguous", True, None)
    assert error.value.code == "ui_ambiguous"
    assert fixture_site.submissions == []
    assert ui.page.evaluate("window.createClicks") == 0


def test_changed_form_does_not_submit(ui: SunoClient, fixture_site: FixtureSite) -> None:
    ui.prepare("test", "task-original", True, None)
    ui.page.get_by_label("Song Title").fill("manual edit")
    with pytest.raises(ServiceError) as error:
        ui.submit("task-original")
    assert error.value.code == "form_changed"
    assert fixture_site.submissions == []


def test_more_than_two_matching_songs_stops(ui: SunoClient) -> None:
    ui.page.evaluate("ids => ids.forEach(id => song(id, 'task-duplicate'))", SONG_IDS[:3])
    with pytest.raises(ServiceError) as error:
        ui.collect("task-duplicate", [])
    assert error.value.code == "song_ambiguous"


def test_title_substring_cannot_claim_unrelated_song(ui: SunoClient) -> None:
    ui.page.evaluate("id => song(id, 'task-unique-123 another manual song')", SONG_IDS[0])
    assert ui.collect("task-unique-123", []) == []


def test_html_attachment_is_not_published(ui: SunoClient, fixture_site: FixtureSite, tmp_path: Path) -> None:
    fixture_site.invalid_audio = True
    writer = AudioWriter(ui, tmp_path / "audio")
    with pytest.raises(ServiceError) as error:
        writer.download(f"https://suno.com/song/{SONG_IDS[0]}", "wav")
    assert error.value.code == "invalid_audio"
    assert not (tmp_path / "audio" / f"{SONG_IDS[0]}.wav").exists()
    assert fixture_site.submissions == []


def test_audit_write_failure_prevents_click(ui: SunoClient, fixture_site: FixtureSite, monkeypatch: pytest.MonkeyPatch) -> None:
    ui.prepare("test", "task-audit", True, None)
    def unavailable(_event: dict) -> None:
        raise OSError("fixture audit disk unavailable")
    monkeypatch.setattr(ui.audit.log, "append", unavailable)
    with pytest.raises(OSError, match="fixture audit disk unavailable"):
        ui.submit("task-audit")
    assert ui.page.evaluate("window.createClicks") == 0
    assert fixture_site.submissions == []


def test_dedicated_local_profile_preserves_cookie(tmp_path: Path) -> None:
    audit = AuditClient(tmp_path / "ai_videos" / "browser_fixture")
    browser = BrowserClient(Settings(data_dir=tmp_path / "isolated-browser", channel="chrome"))
    with browser.session(audit) as context:
        context.add_cookies([{"name": "fixture_login", "value": "local-only", "domain": "fixture.invalid", "path": "/", "expires": 4102444800}])
    with browser.session(audit) as context:
        cookies = {cookie["name"]: cookie["value"] for cookie in context.cookies()}
        assert cookies["fixture_login"] == "local-only"


V6_FORM = """<button role="tab" aria-selected="true">Songs</button>
<button role="tab" aria-selected="true">Advanced</button>
<button>Custom</button><!-- duration mode, not the form mode -->
<div role="textbox" aria-label="Lyrics editor" contenteditable="true">old draft lyrics</div>
<textarea maxlength="1000" placeholder="random style suggestions"></textarea>
<textarea maxlength="1000" aria-label="Tone" hidden></textarea>
<input placeholder="Song Title (Optional)">
<input placeholder="Song Title (Optional)" hidden>
<button aria-label="Create song" onclick="window.createClicks++">Create</button>
<script>window.createClicks=0</script>"""


@pytest.mark.parametrize("instrumental", [True, False])
def test_v6_advanced_editor_clears_old_lyrics_and_ignores_duration_custom(ui: SunoClient, instrumental: bool) -> None:
    ui.page.set_content(V6_FORM)
    lyrics = None if instrumental else "A quiet road"
    ui.prepare("Gentle strings", "task-v6", instrumental, lyrics)
    assert ui.page.get_by_role("textbox", name="Lyrics editor").inner_text().strip() == (lyrics or "")
    assert ui.page.locator('textarea:not([aria-label])').input_value() == "Gentle strings"
    ui.submit("task-v6")
    assert ui.page.evaluate("window.createClicks") == 1


def test_v6_prompt_over_page_limit_never_submits(ui: SunoClient) -> None:
    ui.page.set_content(V6_FORM)
    with pytest.raises(ServiceError) as error:
        ui.prepare("x" * 1001, "task-long", True, None)
    assert error.value.code == "prompt_too_long"
    assert ui.page.evaluate("window.createClicks") == 0


CAPTCHA = '<div id="cap" data-sitekey="x">verify</div><button aria-label="Create song">Create</button>'


def test_visible_window_waits_for_person_to_finish_verification(ui):
    ui.page.set_content(CAPTCHA + "<script>setTimeout(()=>document.getElementById('cap').remove(),1500)</script>")
    seen = []
    ui.challenge_wait, ui.on_challenge = 20, seen.append
    ui.guard()
    assert seen == ["complete_suno_verification_in_open_window", None]
    assert "challenge_wait_person" in ui.audit.log.path.read_text(encoding="utf-8")
    assert ui.human_cleared_at > 0


def test_visible_window_waits_for_person_to_log_in(ui):
    ui.page.set_content('<div id="wall">Continue with Google</div>'
                        "<script>setTimeout(()=>document.getElementById('wall').textContent='Create',1500)</script>")
    seen = []
    ui.challenge_wait, ui.on_challenge = 20, seen.append
    ui.guard()
    assert seen == ["complete_suno_login_in_open_window", None]
    assert "login_wait_person" in ui.audit.log.path.read_text(encoding="utf-8")


def test_login_not_finished_reports_needs_login_with_hint(ui):
    ui.page.set_content("<div>Continue with Google</div>")
    ui.challenge_wait, ui.login_hint = 3, "在常驻窗口里登录"
    with pytest.raises(ServiceError) as error:
        ui.guard()
    assert error.value.code == "needs_login" and "常驻窗口" in str(error.value)


def test_unfinished_verification_still_stops_automation(ui):
    ui.page.set_content(CAPTCHA)
    ui.challenge_wait = 3
    with pytest.raises(ServiceError) as error:
        ui.guard()
    assert error.value.code == "challenge"


def test_headless_never_waits_on_verification(ui):
    ui.page.set_content(CAPTCHA)
    with pytest.raises(ServiceError) as error:
        ui.guard()
    assert error.value.code == "challenge"


LIVE_SONG = """<!doctype html><html><body>
<div><button aria-label="More actions" aria-haspopup="dialog" onclick="document.querySelector('#player').hidden=false">P</button><div id="player" role="dialog" hidden>Player</div></div>
<div><div><div><a href="/song/11111111-1111-4111-8111-111111111111">Other</a><div><button aria-label="More options">x</button></div></div></div></div>
<div><div><div><a href="/song/SONGID?show_comments=true">c</a><div><button aria-label="More options" onclick="document.querySelector('#menu').hidden=false">o</button></div></div></div></div>
<div id="menu" role="menu" hidden><div role="menuitem" aria-label="Download" onclick="document.querySelector('#dlg').hidden=false">Download</div></div>
<div id="dlg" role="dialog" hidden>Download
<button onclick="toggle(this)">M4A</button><button onclick="toggle(this)">MP3<svg></svg></button><button onclick="toggle(this)">WAV</button>
<button onclick="const on=[...document.querySelectorAll('#dlg button')].filter(b=>b.querySelector('svg')).map(b=>b.textContent.trim());location.href=on.length===1&&on[0]==='WAV'?'/audio/fixture.wav':'/audio/fixture.mp3'">Unlock &amp; Download</button></div>
<script>function toggle(b){const s=b.querySelector('svg'); if(s) s.remove(); else b.append(document.createElementNS('http://www.w3.org/2000/svg','svg'))}</script>
</body></html>"""


def test_live_song_page_uses_own_menu_and_download_dialog(ui, fixture_site, tmp_path):
    song_id = "00000000-0000-4000-8000-000000000009"
    ui.page.route("**/song/" + song_id, lambda route: route.fulfill(content_type="text/html", body=LIVE_SONG.replace("SONGID", song_id)))
    writer = AudioWriter(ui, tmp_path / "audio")
    result = writer.download(fixture_site.base_url + "/song/" + song_id, "wav")
    assert result["name"] == song_id + ".wav"
    assert ui.page.locator("#player").is_hidden()


def test_live_song_page_own_menu_labelled_with_title(ui, fixture_site, tmp_path):
    """2026-11-14 live Suno: the song's own menu is "More options for <title>" next to plain "More options" recommendation menus."""
    song_id = "00000000-0000-4000-8000-00000000000b"
    page = LIVE_SONG.replace('<button aria-label="More options" onclick', '<button aria-label="More options for My bed · suno-job-x" onclick')
    page = page.replace("<div id=\"menu\"", '<div><button aria-label="More options">r1</button></div><div><button aria-label="More options">r2</button></div><div id="menu"')
    ui.page.route("**/song/" + song_id, lambda route: route.fulfill(content_type="text/html", body=page.replace("SONGID", song_id)))
    writer = AudioWriter(ui, tmp_path / "audio")
    result = writer.download(fixture_site.base_url + "/song/" + song_id, "wav")
    assert result["name"] == song_id + ".wav"


def test_download_waits_until_clip_finished_generating(ui, fixture_site, tmp_path):
    song_id = "00000000-0000-4000-8000-00000000000a"
    served = []

    def page(route):
        served.append(1)
        body = LIVE_SONG.replace("SONGID", song_id)
        if len(served) == 1:  # 第一次打开：还在生成，Download 不可用
            body = body.replace('role="menuitem" aria-label="Download"', 'role="menuitem" aria-disabled="true" aria-label="Download"')
        route.fulfill(content_type="text/html", body=body)

    ui.page.route("**/song/" + song_id, page)
    writer = AudioWriter(ui, tmp_path / "audio")
    result = writer.download(fixture_site.base_url + "/song/" + song_id, "mp3")
    assert result["name"] == song_id + ".mp3" and len(served) >= 2


def test_download_gives_up_on_unfinished_clip(ui, fixture_site, tmp_path):
    song_id = "00000000-0000-4000-8000-00000000000b"
    body = LIVE_SONG.replace("SONGID", song_id).replace('role="menuitem" aria-label="Download"', 'role="menuitem" aria-disabled="true" aria-label="Download"')
    ui.page.route("**/song/" + song_id, lambda route: route.fulfill(content_type="text/html", body=body))
    writer = AudioWriter(ui, tmp_path / "audio")
    writer.ready_wait = 0
    with pytest.raises(ServiceError) as error:
        writer.download(fixture_site.base_url + "/song/" + song_id, "mp3")
    assert error.value.code == "song_not_ready"
