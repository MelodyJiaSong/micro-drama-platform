"""TikTok 自动填表：用本机 Chrome 打开 TikTok Studio 上传页，传片、填说明与话题、传封面、打开「AI 生成内容」标识；
「Post / 发布」永远由人亲手点（TikTok 官方 Content Posting API 须过应用审核，未审核只能发成仅自己可见；网页自动化只做到填表为止）。

    python tools/tiktok_upload.py login    # 首次：弹出 Chrome，在里面登录 TikTok，登录态存本机，关窗结束

两种收尾（fill(job, mode=…)）：
- "wait"（默认）：填好后停在页面，等你核对后亲手点 Post 或关窗；
- "rehearse"：演练，全部填完并读回核对、截图后直接关窗，不发布（验证页面改版后工具还好用）。
TikTok Studio 网页版（2026-11-07 实测）没有「存草稿」按钮，只有 Post / Discard，所以没有无人值守的草稿模式。

登录态放仓库外：%USERPROFILE%\\.micro_drama\\tiktok_profile（独立 Chrome 配置，不碰你日常的 Chrome；
日常 Chrome 里的登录不会带过来，要在弹出的窗口里再登一次）。
剧级适配器（如 ai_videos/paihangbang/_tools/upload.py）组装 TikTokJob 后调用 fill()。
页面改版或界面语言不同导致某一步找不到控件，就跳过那一步并在终端说明，由你在浏览器里手动补；不会因此误点发布。
每次运行把各步截图存到 PROFILE 旁的 tiktok_runs/<时间>/，失败时便于对照。
"""
from __future__ import annotations

import argparse
import re
import sys
import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from playwright.sync_api import BrowserContext, Error, Locator, Page, TimeoutError as PWTimeout, sync_playwright

PROFILE = Path.home() / ".micro_drama" / "tiktok_profile"
RUNS = Path.home() / ".micro_drama" / "tiktok_runs"
UPLOAD_URL = "https://www.tiktok.com/tiktokstudio/upload?from=creator_center"
LOGIN_URL = "https://www.tiktok.com/login?redirect_url=" + "https%3A%2F%2Fwww.tiktok.com%2Ftiktokstudio%2Fupload"
PUBLISHED_URL = re.compile(r"/tiktokstudio/content")
CAPTION_MAX = 4000            # TikTok Studio 网页版说明上限（含话题）
VIDEO_MAX_BYTES = 10 * 1024**3
LOGIN_WAIT_MS = 600_000
UPLOAD_WAIT_MS = 1_800_000
NAV_TRIES = 5
VIDEO_INPUT = "input[type=file][accept*=video]"
# 2026-11-07 实测页面结构：各区块有稳定的 data-e2e
FORM = "[data-e2e=caption_container]"
EDITOR = "[data-e2e=caption_container] .public-DraftEditor-content[contenteditable=true]"
COVER = "[data-e2e=cover_container]"
MORE = "[data-e2e=advanced_settings_container]"
AIGC = "[data-e2e=aigc_container]"
# 新手引导、功能介绍等会盖住表单的浮层上的「关掉」按钮（不含任何确认发布的字样）
DISMISS = re.compile(r"^(Got it|OK|Skip|Not now|Close|Maybe later|Dismiss|知道了|我知道了|跳过|关闭|暂不|以后再说|稍后)$", re.I)

Log = Callable[[str], None]


@dataclass(frozen=True)
class TikTokJob:
    video: Path
    caption: str              # 不含话题
    hashtags: list[str]       # 不带 #
    ai_generated: bool
    cover: Path | None = None

    def problems(self) -> list[str]:
        out: list[str] = []
        for p in (self.video, self.cover):
            if p and not p.is_file():
                out.append(f"文件不存在：{p}")
        if self.video.is_file() and self.video.stat().st_size > VIDEO_MAX_BYTES:
            out.append(f"片子 {self.video.stat().st_size / 1024**3:.1f} GB，超过网页版 10 GB 上限")
        if not self.caption.strip():
            out.append("说明为空")
        total = len(self.caption) + sum(len(t) + 2 for t in self.hashtags)
        if total > CAPTION_MAX:
            out.append(f"说明连话题 {total} 字符，超过 {CAPTION_MAX}")
        bad = [t for t in self.hashtags if not re.fullmatch(r"\w+", t)]
        if bad:
            out.append(f"话题里不能有空格或标点：{bad}")
        return out


class Shots:
    """每步截图，存 tiktok_runs/<时间>_<片名>/NN_<步骤>.png。"""

    def __init__(self, page: Page, name: str) -> None:
        self.page, self.n = page, 0
        self.dir = RUNS / f"{datetime.now():%Y%m%d_%H%M%S}_{name}"
        self.dir.mkdir(parents=True, exist_ok=True)

    def __call__(self, step: str) -> None:
        self.n += 1
        try:
            self.page.screenshot(path=str(self.dir / f"{self.n:02d}_{step}.png"), timeout=15_000)
        except (PWTimeout, Error):
            pass


def _open(p) -> BrowserContext:  # type: ignore[no-untyped-def]
    PROFILE.mkdir(parents=True, exist_ok=True)
    return p.chromium.launch_persistent_context(
        str(PROFILE), channel="chrome", headless=False, no_viewport=True,
        args=["--start-maximized", "--disable-blink-features=AutomationControlled"])


def _goto(page: Page, url: str, log: Log) -> None:
    """网络时好时坏（VPN 节点）：只等响应开始，失败重试。"""
    for i in range(1, NAV_TRIES + 1):
        try:
            page.goto(url, wait_until="commit", timeout=90_000)
            return
        except (PWTimeout, Error) as e:
            log(f"  打开 {url} 失败（第 {i} 次：{_why(e)}）")
            if i == NAV_TRIES:
                raise SystemExit(f"连不上 TikTok（试了 {NAV_TRIES} 次）；检查网络或 VPN 后重跑")
            page.wait_for_timeout(30_000 * i)


def _why(e: Exception) -> str:
    """Playwright 报错里最有用的几行：首行 + 「谁挡住了点击」之类的说明。"""
    lines = [s.strip() for s in str(e).splitlines() if s.strip()]
    keep = [lines[0][:120]] if lines else []
    keep += [s[:160] for s in lines[1:] if re.search(r"intercepts pointer|not visible|not enabled|detached|outside", s)][:2]
    return " | ".join(keep)


def _upload_ready(page: Page, timeout_ms: int) -> bool:
    try:
        page.locator(VIDEO_INPUT).first.wait_for(state="attached", timeout=timeout_ms)
        return True
    except PWTimeout:
        return False


def _decline_cookies(page: Page) -> None:
    """Cookie 横幅选最省隐私的「拒绝可选 Cookie」；没有横幅就什么都不做。"""
    btn = page.get_by_role("button", name=re.compile(r"Decline optional cookies|拒绝可选|拒绝非必要", re.I))
    try:
        if btn.count():
            btn.first.click(timeout=3_000)
    except (PWTimeout, Error):
        pass


def _dismiss_overlays(page: Page) -> int:
    """关掉新手引导 / 功能介绍浮层；返回关掉的个数。只点 DISMISS 里的字样，绝不点发布类按钮。"""
    closed = 0
    for _ in range(4):
        btn = page.get_by_role("button", name=DISMISS).locator("visible=true")
        if not btn.count():
            break
        try:
            btn.first.click(timeout=3_000)
            closed += 1
            page.wait_for_timeout(600)
        except (PWTimeout, Error):
            break
    return closed


def _click(loc: Locator, timeout: int = 15_000) -> None:
    """先正常点；被浮层挡住就直接在元素上派发 click（React 照样响应）。"""
    try:
        loc.click(timeout=timeout)
    except PWTimeout:
        loc.wait_for(state="attached", timeout=5_000)
        loc.dispatch_event("click")


def _ensure_login(page: Page, log: Log) -> None:
    """停在上传页并确认已登录：未登录时上传页会跳到登录页、没有视频上传控件。"""
    _goto(page, UPLOAD_URL, log)
    if _upload_ready(page, 60_000):
        _decline_cookies(page)
        return
    if "/login" not in page.url:
        _goto(page, LOGIN_URL, log)
    log(f"请在弹出的 Chrome 窗口里登录 TikTok（10 分钟内）。登录页：{LOGIN_URL}")
    deadline = time.monotonic() + LOGIN_WAIT_MS / 1000
    while time.monotonic() < deadline:
        page.wait_for_timeout(3_000)
        if "/login" in page.url:
            continue
        if "tiktokstudio/upload" not in page.url:
            _goto(page, UPLOAD_URL, log)
        if _upload_ready(page, 10_000):
            return
    raise SystemExit("10 分钟内没检测到登录")


def _try(step: str, action: Callable[[], None], log: Log, manual: str) -> bool:
    try:
        action()
        log(f"  ✓ {step}")
        return True
    except (PWTimeout, Error) as e:
        log(f"  ✗ {step}没自动完成（{_why(e)}）→ 请手动：{manual}")
        return False


def _fill_caption(page: Page, caption: str, hashtags: list[str]) -> None:
    editor = page.locator(EDITOR).first
    editor.wait_for(timeout=120_000)
    _dismiss_overlays(page)             # 引导浮层弹出会抢焦点、吞掉开头几个字（2026-11-07 实测）
    editor.focus()                      # 不用鼠标点：浮层挡着也能输入
    page.wait_for_timeout(500)
    page.keyboard.press("Control+A")
    page.keyboard.press("Delete")       # TikTok 会把文件名预填进说明，先清掉
    for i, line in enumerate(caption.splitlines()):
        if i:
            page.keyboard.press("Enter")
        if line:
            page.keyboard.insert_text(line)
    page.keyboard.press("Enter")
    for t in hashtags:
        page.keyboard.type(f"#{t}", delay=60)
        page.wait_for_timeout(1_200)
        page.keyboard.press("Space")    # 关掉话题联想框，不选联想项
        page.wait_for_timeout(300)
    got = editor.inner_text(timeout=5_000)
    first = next(s for s in caption.splitlines() if s.strip())
    if first[:30] not in got:
        raise Error(f"说明框读回不对：{got[:80]!r}")


def _set_cover(page: Page, cover: Path) -> None:
    _click(page.locator(f"{COVER} .edit-container").first, 20_000)
    page.wait_for_timeout(2_000)
    _click(page.get_by_text(re.compile(r"^(Upload cover|上传封面)$")).first)
    page.wait_for_timeout(800)
    page.locator("input[type=file][accept*=image]").last.set_input_files(str(cover), timeout=15_000)
    page.wait_for_timeout(5_000)
    _click(page.get_by_role("button", name=re.compile(r"^(Confirm|Save|Done|确认|确定|保存|完成)$")).locator("visible=true").last, 20_000)
    page.wait_for_timeout(1_500)


def _declare_ai(page: Page) -> None:
    more = page.locator(MORE).first
    if "collapsed" in (more.get_attribute("class", timeout=15_000) or ""):
        _click(more.locator(".more-btn").first, 10_000)
        page.wait_for_timeout(1_200)
    box = page.locator(AIGC).first
    box.scroll_into_view_if_needed(timeout=15_000)
    state = box.locator(".Switch__content").first
    toggle = box.locator("input[role=switch]").first

    def on() -> bool:
        return state.get_attribute("aria-checked", timeout=5_000) == "true"

    if not on():
        _click(toggle, 10_000)
        page.wait_for_timeout(1_000)
        confirm = page.get_by_role("button", name=re.compile(r"^(Turn on|开启|确认|确定)$")).locator("visible=true")
        if confirm.count():
            _click(confirm.last, 10_000)
            page.wait_for_timeout(800)
    if not on():
        raise Error("AI 生成内容开关点了但读回仍是关")


def _wait_uploaded(page: Page, log: Log) -> None:
    log("  视频上传中（页面上能看到进度）…")
    page.get_by_text(re.compile(r"Uploaded|上传完毕|已上传|上传成功")).first.wait_for(timeout=UPLOAD_WAIT_MS)


def fill(job: TikTokJob, log: Log = print, mode: str = "wait") -> str:
    """mode="wait"：填好后等你亲手点 Post 或关窗，返回 "published" / "filled"；
    mode="rehearse"：填完核对后直接关窗不发布，全部步骤成功返回 "rehearsed"，否则 "incomplete"。"""
    problems = job.problems()
    if problems:
        raise ValueError("\n".join(problems))
    with sync_playwright() as p:
        ctx = _open(p)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        shot = Shots(page, job.video.stem)
        _ensure_login(page, log)
        shot("upload_page")
        page.locator(VIDEO_INPUT).first.set_input_files(str(job.video), timeout=120_000)
        page.locator(FORM).first.wait_for(timeout=180_000)
        log("已选好片子，开始填表：")
        page.wait_for_timeout(5_000)   # 新手引导浮层在表单出来后几秒才弹
        n = _dismiss_overlays(page)
        if n:
            log(f"  关掉了 {n} 个引导浮层")
        shot("form")
        ok = {
            "caption": _try("说明与话题", lambda: _fill_caption(page, job.caption, job.hashtags), log,
                            "说明框粘贴终端上方打印的说明"),
        }
        shot("caption")
        ok["upload"] = _try("视频上传完成", lambda: _wait_uploaded(page, log), log, "等页面上传进度走完")
        _dismiss_overlays(page)
        if not ok["caption"]:   # 第一次多半是浮层晚到，关掉后再试一次
            ok["caption"] = _try("说明与话题（重试）", lambda: _fill_caption(page, job.caption, job.hashtags), log,
                                 "说明框粘贴终端上方打印的说明")
        if job.cover:
            ok["cover"] = _try("封面", lambda: _set_cover(page, job.cover), log,
                               f"点「Edit cover」→「Upload cover」传 {job.cover}")
            shot("cover")
        _dismiss_overlays(page)
        if job.ai_generated:
            ok["ai"] = _try("AI 生成内容标识", lambda: _declare_ai(page), log,
                            "点「Show more」，打开「AI-generated content」开关")
            shot("ai")
        log(f"  截图：{shot.dir}")
        result = "filled"
        if mode == "rehearse":
            failed = [k for k, v in ok.items() if not v]
            result = "incomplete" if failed else "rehearsed"
            log(f"  演练结束，未发布：{'全部步骤成功' if not failed else '没完成：' + str(failed)}")
            try:
                ctx.close()
            except Error:
                pass
            return result
        log("\n表已填好。请在浏览器里逐项核对（说明、封面、谁可以看、AI 标识），确认无误后亲手点「Post / 发布」；"
            "不发就直接关掉浏览器窗口。")
        try:
            while not page.is_closed():
                if PUBLISHED_URL.search(page.url):
                    result = "published"
                    log("检测到已发布（跳到了作品管理页）。")
                    page.wait_for_timeout(3_000)
                    break
                page.wait_for_timeout(1_000)
        except Error:
            pass
        try:
            ctx.close()
        except Error:
            pass
        return result


def login(log: Log = print) -> None:
    with sync_playwright() as p:
        ctx = _open(p)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        _ensure_login(page, log)
        log(f"已登录，登录态存于 {PROFILE}；关闭浏览器窗口结束。")
        try:
            while not page.is_closed():
                page.wait_for_timeout(1_000)
        except Error:
            pass


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["login"])
    ap.parse_args()
    login()


if __name__ == "__main__":
    sys.exit(main())
