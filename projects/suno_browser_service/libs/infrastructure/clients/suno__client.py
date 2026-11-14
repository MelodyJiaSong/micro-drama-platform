import json
import re
import time
from pathlib import Path

from playwright.sync_api import Locator, Page

from projects.suno_browser_service.libs.common.errors import ServiceError
from projects.suno_browser_service.libs.common.settings import SUNO_URL
from projects.suno_browser_service.libs.infrastructure.clients.audit__client import AuditClient


class SunoClient:
    """页面控件未唯一匹配时停机；覆盖配置只接受 CSS locator，不执行脚本。"""

    def __init__(self, page: Page, audit: AuditClient, config_path: Path) -> None:
        self.page = page
        self.audit = audit
        self.diagnostic_dir = config_path.parent
        self.before_submit_check = None
        self.applied_options: dict = {}
        self.title_field = True
        # Without a title field (Sounds) clips are claimed by the prompt shown in their library row.
        self.match_prompt: str | None = None
        # Seconds to wait for a person to finish a verification in the visible window; 0 pauses at once.
        self.challenge_wait = 0
        # Called with the human_action a person should take in the open window, then with None once done.
        self.on_challenge = None
        self.login_hint = "请运行 login.ps1，在专用窗口完成 Suno 登录"
        # monotonic time a person last finished a verification or login; claim() restarts its clip deadline from it.
        self.human_cleared_at = 0.0
        self.current_url: str | None = None
        # Attached mode: returns a new work tab when the current one stops responding (see navigate).
        self.renew_page = None
        # Responses to Suno's generate request after this client's Create click, and the clip urls they named.
        self.create_responses: list = []
        self._created: list[str] | None = None
        self.watch_consent()
        self.overrides: dict[str, str] = json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
        allowed = {"custom", "style", "title", "lyrics", "instrumental", "create", "more", "download", "mp3", "wav"}
        allowed |= {"simple", "prompt", "model", "model_choice", "voice_name", "voice_name_choice", "inspiration_name", "inspiration_name_choice",
                    "exclude_styles", "vocal_gender", "weirdness", "style_influence", "audio_influence", "variety", "duration_seconds",
                    "max_mode", "my_taste", "sound_type", "bpm", "upload_input", "add_reference", "upload_confirm", "reference_chip", "reference_url", "attach_reference"}
        if self.overrides.keys() - allowed or any(not isinstance(v, str) for v in self.overrides.values()):
            raise ServiceError("invalid_selectors", "selectors.json 含未知键或非字符串值")

    def control(self, key: str) -> Locator:
        if key in self.overrides:
            candidates = [self.page.locator(self.overrides[key])]
        else:
            names = {
                "custom": r"^(?:Advanced|Custom)$", "style": r"^(?:Styles?|Style of Music|Music Style)$",
                "title": r"Title|Song Title", "lyrics": r"Lyrics", "instrumental": r"^Instrumental$",
                "create": r"^Create(?: song)?$", "more": r"More Actions|More options|More menu",
                "download": r"^Download$", "mp3": r"^(?:Download )?(?:MP3|Audio \(MP3\)|MP3 Audio)$",
                "wav": r"^(?:Download )?(?:WAV|Audio \(WAV\)|WAV Audio)$",
            }
            pattern = re.compile(names[key], re.I)
            if key in {"style", "title", "lyrics"}:
                candidates = [self.page.get_by_role("textbox", name=pattern), self.page.get_by_placeholder(pattern)]
                if key == "style" and self.page.get_by_role("tab", name="Advanced", exact=True).count():
                    candidates.append(self.page.locator('textarea[maxlength="1000"]:not([aria-label])'))
            else:
                roles = ["checkbox", "switch"] if key == "instrumental" else ["button", "tab", "menuitem"]
                if key == "custom":
                    roles = ["tab", "button"]
                candidates = [self.page.get_by_role(role, name=pattern) for role in roles]
        deadline = time.monotonic() + 15
        while time.monotonic() < deadline:
            self.guard()
            for candidate in candidates:
                visible = candidate.filter(visible=True)
                if visible.count() == 1:
                    return visible
                if visible.count() > 1:
                    raise ServiceError("ui_ambiguous", f"{key} 匹配多个可见控件；需校准 selectors.json")
            self.page.wait_for_timeout(250)
        self.diagnose_missing(key, candidates)
        raise ServiceError("ui_changed", f"找不到唯一的 {key} 控件；需登录后校准 selectors.json")

    def diagnose_missing(self, key: str, candidates: list) -> None:
        """Keep what the page looked like when a control was not found (counts, modal, screenshot); never raises."""
        try:
            counts = [[c.count(), c.filter(visible=True).count()] for c in candidates]
            modal = self.page.locator('[aria-modal="true"]:visible, [role="dialog"]:visible, [role="alertdialog"]:visible')
            texts = modal.evaluate_all("els => els.map(e => (e.getAttribute('aria-label') || e.innerText || '').slice(0, 160))")
            self.audit.call("control_missing", {"control": key}, lambda: {"candidates_total_visible": counts,
                            "url": self.page.url, "modals": texts})
            self.page.screenshot(path=str(self.diagnostic_dir / f"missing-{key}.png"), timeout=10000)
        except Exception:
            pass

    def challenge(self, body: str) -> str | None:
        if re.search(r"verify (?:that )?you are human|unusual traffic|access denied|account suspended", body, re.I):
            return "Suno 要求人工验证或拒绝访问；自动化已停止"
        if self.page.locator('iframe[src*="captcha"]:visible, [data-sitekey]:visible').count():
            return "页面出现验证码；自动化已停止"
        return None

    LOGIN_WALL = re.compile(r"Continue with Google|Welcome to Suno|Sign in to Suno|Log in to Suno", re.I)

    def blocked(self, kind: str) -> bool:
        body = self.page.locator("body").inner_text(timeout=10000)
        return bool(self.challenge(body) or kind == "login" and self.LOGIN_WALL.search(body))

    def wait_for_person(self, kind: str = "challenge") -> bool:
        """Leave the verification or login to a person in the visible window; never interact with it."""
        action_name = "complete_suno_login_in_open_window" if kind == "login" else "complete_suno_verification_in_open_window"

        def action() -> dict:
            if self.on_challenge:
                self.on_challenge(action_name)
            try:
                self.page.bring_to_front()
                deadline = time.monotonic() + self.challenge_wait
                while time.monotonic() < deadline:
                    self.page.wait_for_timeout(2000)
                    if not self.blocked(kind):
                        return {"cleared": True}
                return {"cleared": False}
            finally:
                self.human_cleared_at = time.monotonic()
                if self.on_challenge:
                    self.on_challenge(None)
        return self.audit.call("login_wait_person" if kind == "login" else "challenge_wait_person",
                               {"seconds": self.challenge_wait}, action)["cleared"]

    # Accessible names: Suno's "Reject All" button is labelled "Deny all optional cookies" (2026-11-03).
    CONSENT_REJECT = re.compile(r"^(?:Reject All|Deny all optional cookies|Reject all cookies|Only necessary|Necessary only|Decline all)$", re.I)

    def dismiss_consent(self) -> None:
        """Suno's cookie banner sits over the form; on 2026-11-03 it intercepted the click on Create. The service
        declines optional cookies (Reject All keeps only what the site needs) and records the choice."""
        banner = self.page.locator("#cmp-banner-container")
        if not banner.count():
            return
        button = banner.get_by_role("button", name=self.CONSENT_REJECT).filter(visible=True)
        if not button.count():
            return
        self.audit.call("consent_reject", {"banner": "cookie consent", "choice": "Reject All (necessary cookies only)"},
                        lambda: button.first.click(timeout=5000) or {"clicked": True})
        self.page.wait_for_timeout(500)

    def watch_consent(self) -> None:
        """The banner shows up after the page loaded, between checks; Playwright runs this handler before any click or
        fill while it is visible. One handler per tab: the previous job's is replaced."""
        try:
            # Two layers exist; the second (settings) one is inert until opened, so a plain match is ambiguous.
            banner = self.page.locator("#cmp-banner-container [role=dialog]:not([inert])").first
            self.page.remove_locator_handler(banner)
            self.page.add_locator_handler(banner, self.dismiss_consent)
        except AttributeError:
            pass  # test doubles without locator handlers

    def guard(self) -> None:
        self.dismiss_consent()
        body = self.page.locator("body").inner_text(timeout=10000)
        if self.LOGIN_WALL.search(body):
            if not (self.challenge_wait > 0 and self.wait_for_person("login")):
                raise ServiceError("needs_login", self.login_hint)
            if self.current_url and self.page.url.split("?")[0].rstrip("/") != self.current_url.rstrip("/"):
                self.page.goto(self.current_url, wait_until="domcontentloaded", timeout=60000)
                self.page.wait_for_timeout(2000)
            body = self.page.locator("body").inner_text(timeout=10000)
            if self.LOGIN_WALL.search(body):
                raise ServiceError("needs_login", self.login_hint)
        reason = self.challenge(body)
        if reason and self.challenge_wait > 0:
            self.capture_state("challenge")
            if self.wait_for_person():
                body = self.page.locator("body").inner_text(timeout=10000)
                reason = None
        if reason:
            self.capture_state("challenge")
            raise ServiceError("challenge", reason)
        if re.search(r"not enough credits|insufficient credits|download limit reached|no downloads left|out of downloads|used all your downloads", body, re.I):
            raise ServiceError("quota_exhausted", "Suno 生成或下载额度不足")

    def navigate(self, url: str = SUNO_URL) -> None:
        def action() -> dict:
            self.current_url = url
            try:
                self.page.goto(url, wait_until="domcontentloaded", timeout=60000)
            except Exception as exc:
                # A stuck work tab (dialog, hung renderer) is replaced once; a fresh tab loads in seconds.
                if self.renew_page is None or "Timeout" not in type(exc).__name__ + str(exc):
                    raise
                self.page = self.renew_page()
                self.watch_consent()
                self.audit.call("work_tab_renewed", {"url": url, "reason": type(exc).__name__}, lambda: {"ok": True})
                self.page.goto(url, wait_until="domcontentloaded", timeout=60000)
            self.page.locator("body").wait_for()
            self.guard()
            return {"url": self.page.url}
        self.audit.call("navigate", {"url": url}, action)

    def refresh(self) -> None:
        """Reload the current page: the clip list does not show newly created clips by itself."""
        self.navigate(self.current_url or SUNO_URL)

    def prepare(self, prompt: str, title: str, instrumental: bool, lyrics: str | None) -> list[str]:
        def action() -> list[str]:
            self.guard()
            songs = self.page.get_by_role("tab", name="Songs", exact=True)
            if songs.count() == 1 and songs.get_attribute("aria-selected") != "true":
                songs.click(timeout=10000)
            custom = self.control("custom")
            if custom.get_attribute("aria-selected") != "true" and custom.get_attribute("aria-pressed") != "true":
                custom.click(timeout=10000)
            advanced = custom.inner_text().strip() == "Advanced"
            editor = self.control("lyrics") if advanced else None
            style = self.control("style")
            limit = style.get_attribute("maxlength")
            if limit and len(prompt) > int(limit):
                raise ServiceError("prompt_too_long", f"当前页面 Styles 最长 {limit} 字符；未提交")
            style.fill(prompt, timeout=10000)
            self.control("title").fill(title, timeout=10000)
            if editor is not None:
                editor.fill("" if instrumental else lyrics or "", timeout=10000)
                if instrumental and editor.inner_text().strip():
                    raise ServiceError("form_changed", "纯音乐模式歌词未清空；未提交")
            else:
                self.control("instrumental").set_checked(instrumental, timeout=10000)
                self.control("lyrics").fill(lyrics or "", timeout=10000)
            if style.input_value() != prompt:
                raise ServiceError("form_changed", "Styles 内容与请求不一致；未提交")
            if not self.control("create").is_enabled():
                raise ServiceError("create_disabled", "Create 不可用；检查表单、额度与账号")
            return self.song_links()
        return self.audit.call("prepare", {"prompt": prompt, "title": title, "instrumental": instrumental, "lyrics": lyrics}, action)

    def submit(self, title: str) -> None:
        def action() -> dict:
            self.guard()
            if self.before_submit_check:
                self.before_submit_check()
            if self.title_field and self.control("title").input_value() != title:
                raise ServiceError("form_changed", "歌曲任务标记已改变，停止提交")
            # Suno sends its generate request only after its own checks, sometimes minutes later; keep listening so
            # the tab is not reloaded before it is sent and its clip ids can be used directly (no headers or cookies kept).
            self.create_responses = []
            self.page.on("response", lambda response: self.create_responses.append(response)
                         if response.request.method == "POST" and self.generate_call(response) else None)
            self.control("create").click(timeout=15000, no_wait_after=True)
            self.page.wait_for_timeout(1500)
            snapshot = self.capture_state("after-submit", title)
            self.guard()
            return {"clicked": True, "title": title, "cost": "unknown", "diagnostic": str(snapshot)}
        self.audit.call("create", {"title": title, "attempt": 1}, action)

    def create_sent(self) -> bool:
        """True once Suno's generate request for this Create was answered; until then the tab must not be reloaded."""
        return bool(self.create_responses)

    def created_songs(self) -> list[str]:
        """The clips Suno's answer to Create named, logged once; empty until the answer arrived or when it had none."""
        if not self.create_responses:
            return []
        if self._created is None:
            summaries = [self.summarize(r) for r in self.create_responses]
            ids = {i.lower() for item in summaries for i in item.get("clip_ids", [])
                   if isinstance(i, str) and re.fullmatch(r"[0-9a-fA-F-]{36}", i)}
            self._created = sorted("https://suno.com/song/" + i for i in ids)
            self.audit.call("create_response", {"responses": len(summaries)},
                            lambda: {"answers": [{k: v for k, v in item.items() if k != "generate"} for item in summaries]})
        return self._created

    @staticmethod
    def generate_call(response) -> bool:
        return bool(re.search(r"/generate", response.url.split("?")[0], re.I))

    @classmethod
    def summarize(cls, response) -> dict:
        from urllib.parse import urlsplit
        url = urlsplit(response.url)
        item = {"host": url.hostname, "path": url.path, "status": response.status, "generate": cls.generate_call(response)}
        if item["generate"]:
            try:
                body = response.json()
            except Exception:
                body = None
            if isinstance(body, dict):
                item["detail"] = body.get("detail") or body.get("error") or body.get("message")
                clips = body.get("clips")
                if isinstance(clips, list):
                    item["clip_ids"] = [c.get("id") for c in clips if isinstance(c, dict)][:4]
        return item

    def capture_state(self, name: str, title: str | None = None, **extra) -> Path:
        snapshot = self.diagnostic_dir / f"{name}.json"
        snapshot.write_text(json.dumps({"title": title, "url": self.page.url,
                                       "visible_text": self.page.locator("body").inner_text(), **extra},
                                      ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        try:
            self.page.screenshot(path=str(self.diagnostic_dir / f"{name}.png"), timeout=10000)
        except Exception:
            pass  # 2026-11-03 ep20: a screenshot timing out right after Create turned a created job into uncertain
        return snapshot

    @staticmethod
    def fingerprint(text: str) -> str:
        # Suno rewrites punctuation in displayed prompts (". " becomes ", "), so compare letters and digits only.
        return re.sub(r"[^0-9a-z]+", "", text.casefold())

    def song_links(self, title: str | None = None, prompt: str | None = None) -> list[str]:
        links = self.page.locator('a[href*="/song/"]')
        if title is not None:
            links = links.filter(has_text=re.compile(r"^\s*" + re.escape(title) + r"\s*$"))
        if prompt is not None:
            rows = links.evaluate_all("""els => els.map(a => { let n = a;
                for (let k = 0; k < 10 && n; k++) { n = n.parentElement; if (n && n.querySelector('[aria-label="More options"]')) break }
                return [a.getAttribute('href'), n ? n.innerText : ''] })""")
            wanted = self.fingerprint(prompt)[:80]
            hrefs = [href for href, text in rows if wanted and wanted in self.fingerprint(text)]
        else:
            hrefs = links.evaluate_all("els => els.map(e => e.getAttribute('href'))")
        result = set()
        for href in hrefs:
            match = re.fullmatch(r"(?:https://suno\.com)?/song/([0-9a-fA-F-]{36})", href or "")
            if match:
                result.add("https://suno.com/song/" + match[1].lower())
        return sorted(result)

    def search(self, text: str) -> None:
        """Narrow the clip list so older clips beyond the first page are found; skipped when the box is absent."""
        box = self.page.get_by_role("textbox", name="Search clips", exact=True).filter(visible=True)
        if box.count() == 1:
            box.fill(text[:40])
            self.page.wait_for_timeout(3000)

    def collect(self, title: str, baseline: list[str]) -> list[str]:
        def action() -> list[str]:
            self.guard()
            found = self.song_links(title) if self.title_field else self.song_links(prompt=self.match_prompt or "")
            songs = sorted(set(found) - set(baseline))
            if len(songs) > 2:
                raise ServiceError("song_ambiguous", "同一任务标题找到超过两首歌曲，停止收取" if self.title_field else "同一 prompt 的新片段超过两条，停止收取")
            return songs
        return self.audit.call("poll_generation", {"title": title}, action)
