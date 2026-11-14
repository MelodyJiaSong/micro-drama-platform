import hashlib
import os
import re
import time
from pathlib import Path
from playwright.sync_api import expect

from projects.suno_browser_service.libs.common.errors import ServiceError
from projects.suno_browser_service.libs.infrastructure.clients.suno__client import SunoClient


class AudioWriter:
    def __init__(self, ui: SunoClient, output: Path, capture=None) -> None:
        self.ui = ui
        self.output = output.absolute()
        # Attached window: BrowserClient.capture_download(page, click, dest, timeout_ms) replaces Playwright's download object.
        self.capture = capture
        # Seconds to wait for a still-generating clip's Download item to become available.
        self.ready_wait = 600

    def download(self, url: str, format: str) -> dict:
        song_id = url.rsplit("/", 1)[-1]
        if not re.fullmatch(r"[0-9a-fA-F-]{36}", song_id) or format not in {"mp3", "wav"}:
            raise ServiceError("invalid_song", "无效歌曲或格式")
        dest = self.output / f"{song_id}.{format}"
        partial = dest.with_suffix(dest.suffix + ".part")
        if self.output.resolve() != self.output or dest.resolve() != dest or partial.resolve() != partial:
            raise ServiceError("unsafe_output", "输出路径含重定向链接，停止下载")
        self.output.mkdir(parents=True, exist_ok=True)
        if self.output.resolve() != self.output:
            raise ServiceError("unsafe_output", "输出路径在创建时被重定向，停止下载")
        self.ui.navigate(url)

        def action() -> dict:
            self.ui.guard()
            # Clips are listed while still generating; their Download item stays disabled until they are finished.
            deadline = time.monotonic() + self.ready_wait
            while True:
                self.more_button(song_id).click(timeout=15000)
                download = self.ui.control("download")
                if download.is_enabled():
                    break
                self.ui.page.keyboard.press("Escape")
                if time.monotonic() >= deadline:
                    raise ServiceError("song_not_ready", "歌曲仍在生成，下载项不可用；稍后恢复任务补收")
                self.ui.page.wait_for_timeout(15000)
                self.ui.page.reload(wait_until="domcontentloaded", timeout=60000)
                self.ui.page.wait_for_timeout(2000)
            download.click(timeout=10000)
            option = self.dialog_option(format) or self.ui.control(format)
            expect(option).to_be_enabled(timeout=180000)
            self.ui.guard()
            if self.capture:
                self.capture(self.ui.page, lambda: option.click(timeout=15000), partial, 180000)
            else:
                with self.ui.page.expect_download(timeout=180000) as pending:
                    option.click(timeout=15000)
                pending.value.save_as(str(partial))
                error = pending.value.failure()
                if error:
                    raise ServiceError("download_failed", "官方下载失败；可恢复补收")
            self.validate(partial, format)
            os.replace(partial, dest)
            return self.metadata(dest, url)

        return self.ui.audit.call("download_official", {"song_url": url, "format": format, "output": str(dest)}, action)

    def more_button(self, song_id: str):
        """The song's own menu: live song pages also carry the player's "More actions" and recommendation menus."""
        if "more" not in self.ui.overrides:
            # 2026-11-14 live Suno: the song's own menu is labelled "More options for <title>" (recommendations keep plain "More options").
            titled = self.ui.page.locator(f'xpath=//button[starts-with(@aria-label,"More options for ")][ancestor::*[position()<=4][.//a[starts-with(@href,"/song/{song_id}")]]]')
            own = self.ui.page.locator(f'xpath=//button[@aria-label="More options"][ancestor::*[position()<=3][.//a[starts-with(@href,"/song/{song_id}")]]]')
            deadline = time.monotonic() + 15
            while time.monotonic() < deadline:
                if titled.filter(visible=True).count() == 1:
                    return titled.filter(visible=True)
                visible = own.filter(visible=True)
                if visible.count() == 1:
                    return visible
                if visible.count() > 1:
                    raise ServiceError("ui_ambiguous", "本歌曲有多个 More options；需校准 selectors.json")
                if not self.ui.page.get_by_role("button", name=re.compile(r"^More options( for .+)?$")).count():
                    break
                self.ui.page.wait_for_timeout(250)
        return self.ui.control("more")

    def dialog_option(self, format: str):
        """Live Suno: Download opens a multi-select format dialog (MP3 pre-checked); keep only the requested format, then use its Download button."""
        if format in self.ui.overrides:
            return None
        page = self.ui.page
        go_name = re.compile(r"^(?:Unlock & )?Download$")
        dialog = page.get_by_role("dialog").filter(visible=True).filter(has=page.get_by_role("button", name=go_name))
        try:
            dialog.first.wait_for(state="visible", timeout=5000)
        except Exception:
            return None
        if dialog.count() != 1:
            raise ServiceError("ui_ambiguous", "下载弹窗不唯一；未下载")
        checked = "e => e.querySelector('svg') !== null"
        for name in ("M4A", "MP3", "WAV", "MP4 video asset"):
            button = dialog.get_by_role("button", name=name, exact=True)
            if button.count() != 1:
                continue
            if button.evaluate(checked) != (name == format.upper()):
                button.click()
                page.wait_for_timeout(300)
            if button.evaluate(checked) != (name == format.upper()):
                raise ServiceError("unverified_option", f"下载格式 {name} 勾选状态读回不符；未下载")
        go = dialog.get_by_role("button", name=go_name)
        if go.count() != 1:
            raise ServiceError("ui_ambiguous", "下载弹窗的 Download 按钮不唯一；未下载")
        return go

    @staticmethod
    def validate(path: Path, format: str) -> None:
        with path.open("rb") as file:
            header = file.read(16)
        valid = (header[:4] in {b"RIFF", b"RF64"} and header[8:12] == b"WAVE") if format == "wav" else (
            header[:3] == b"ID3" or len(header) >= 2 and header[0] == 255 and header[1] & 224 == 224)
        if not valid or path.stat().st_size < 128:
            raise ServiceError("invalid_audio", "下载结果为空或不是所选音频格式")

    @staticmethod
    def metadata(path: Path, url: str) -> dict:
        digest = hashlib.sha256()
        with path.open("rb") as file:
            for chunk in iter(lambda: file.read(1024 * 1024), b""):
                digest.update(chunk)
        return {"name": path.name, "bytes": path.stat().st_size, "sha256": digest.hexdigest(), "song_url": url}
