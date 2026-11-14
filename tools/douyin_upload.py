"""抖音自动填表：用本机 Chrome 打开创作者中心上传页，传片、填标题与描述话题、传封面、勾 AI 声明；
「发布」永远由人亲手点（抖音没有个人可用的官方投稿接口，网页自动化只做到填表为止）。

    python tools/douyin_upload.py login    # 首次：弹出 Chrome 扫码登录，登录态存本机，关窗结束

登录态放仓库外：%USERPROFILE%\\.micro_drama\\douyin_profile（独立 Chrome 配置，不碰你日常的 Chrome）。
剧级适配器（如 ai_videos/paihangbang/_tools/upload.py）组装 DouyinJob 后调用 fill()。
页面改版时某一步找不到控件，就跳过那一步并在终端说明，由你在浏览器里手动补；不会因此误点发布。
"""
from __future__ import annotations

import argparse
import re
import sys
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from playwright.sync_api import BrowserContext, Error, Page, TimeoutError as PWTimeout, sync_playwright

PROFILE = Path.home() / ".micro_drama" / "douyin_profile"
UPLOAD_URL = "https://creator.douyin.com/creator-micro/content/upload"
PUBLISHED_URL = re.compile(r"/content/manage")
TITLE_MAX = 30
DESCRIPTION_MAX = 1000
LOGIN_WAIT_MS = 300_000
UPLOAD_WAIT_MS = 1_800_000

Log = Callable[[str], None]


@dataclass(frozen=True)
class DouyinJob:
    video: Path
    title: str
    description: str          # 不含话题
    topics: list[str]         # 不带 #
    ai_generated: bool
    cover_vertical: Path | None = None    # 3:4
    cover_horizontal: Path | None = None  # 4:3

    def problems(self) -> list[str]:
        out: list[str] = []
        for p in (self.video, self.cover_vertical, self.cover_horizontal):
            if p and not p.is_file():
                out.append(f"文件不存在：{p}")
        if not 0 < len(self.title) <= TITLE_MAX:
            out.append(f"标题 {len(self.title)} 字，须 1–{TITLE_MAX}")
        total = len(self.description) + sum(len(t) + 2 for t in self.topics)
        if total > DESCRIPTION_MAX:
            out.append(f"描述连话题 {total} 字，超过 {DESCRIPTION_MAX}")
        return out


def _open(p) -> BrowserContext:  # type: ignore[no-untyped-def]
    PROFILE.mkdir(parents=True, exist_ok=True)
    return p.chromium.launch_persistent_context(
        str(PROFILE), channel="chrome", headless=False, no_viewport=True,
        args=["--start-maximized", "--disable-blink-features=AutomationControlled"])


def _upload_ready(page: Page, timeout_ms: int) -> bool:
    try:
        page.locator("input[type=file]").first.wait_for(state="attached", timeout=timeout_ms)
        return True
    except PWTimeout:
        return False


def _ensure_login(page: Page, log: Log) -> None:
    """停在上传页并确认已登录：未登录时上传页只显示落地介绍页（网址不变、没有上传控件）。"""
    page.goto(UPLOAD_URL, wait_until="domcontentloaded")
    if _upload_ready(page, 15_000):
        return
    log("请在弹出的 Chrome 里点「登录」扫码登录抖音创作者中心（5 分钟内）…")
    deadline = time.monotonic() + LOGIN_WAIT_MS / 1000
    while time.monotonic() < deadline:
        if _upload_ready(page, 5_000):
            return
        if "content/upload" not in page.url and "creator-micro" in page.url:
            page.goto(UPLOAD_URL, wait_until="domcontentloaded")
    raise SystemExit("5 分钟内没检测到登录")


def _try(step: str, action: Callable[[], None], log: Log, manual: str) -> bool:
    try:
        action()
        log(f"  ✓ {step}")
        return True
    except (PWTimeout, Error) as e:
        log(f"  ✗ {step}没自动完成（{str(e).splitlines()[0][:120]}）→ 请手动：{manual}")
        return False


def _fill_title(page: Page, title: str) -> None:
    box = page.get_by_placeholder(re.compile("标题")).first
    box.wait_for(timeout=30_000)
    box.fill(title)


def _fill_description(page: Page, description: str, topics: list[str]) -> None:
    editor = page.locator(".zone-container[contenteditable=true], [contenteditable=true]").first
    editor.wait_for(timeout=30_000)
    editor.click()
    page.keyboard.press("Control+A")
    page.keyboard.press("Delete")
    for i, line in enumerate(description.splitlines()):
        if i:
            page.keyboard.press("Shift+Enter")
        page.keyboard.insert_text(line)
    page.keyboard.press("Shift+Enter")
    for t in topics:
        page.keyboard.type(f"#{t}", delay=60)
        page.wait_for_timeout(800)
        page.keyboard.press("Space")


def _set_cover(page: Page, vertical: Path | None, horizontal: Path | None) -> None:
    page.get_by_text("选择封面").first.click(timeout=15_000)
    modal = page.locator("[class*=modal]").filter(has=page.locator("input[type=file]")).last
    modal.wait_for(timeout=15_000)
    for label, path in (("竖封面", vertical), ("横封面", horizontal)):
        if not path:
            continue
        tab = modal.get_by_text(re.compile(f"设置{label}|{label}")).first
        if tab.count():
            tab.click()
            page.wait_for_timeout(800)
        modal.locator("input[type=file]").last.set_input_files(str(path))
        page.wait_for_timeout(3000)
    modal.get_by_role("button", name=re.compile("完成|确定")).last.click(timeout=15_000)
    page.wait_for_timeout(1500)


def _declare_ai(page: Page) -> None:
    page.get_by_text(re.compile("添加声明|自主声明|作品声明")).first.click(timeout=15_000)
    page.get_by_text("内容由AI生成").first.click(timeout=15_000)
    page.get_by_role("button", name=re.compile("确定|确认|完成")).last.click(timeout=15_000)


def _wait_uploaded(page: Page, log: Log) -> None:
    log("  视频上传中（页面上能看到进度）…")
    page.get_by_text(re.compile("重新上传|上传成功|更换视频")).first.wait_for(timeout=UPLOAD_WAIT_MS)


def fill(job: DouyinJob, log: Log = print) -> bool:
    """填好表后等你在浏览器里亲手点「发布」或关窗；返回是否检测到已发布。"""
    problems = job.problems()
    if problems:
        raise ValueError("\n".join(problems))
    with sync_playwright() as p:
        ctx = _open(p)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        _ensure_login(page, log)
        page.locator("input[type=file]").first.set_input_files(str(job.video), timeout=60_000)
        page.wait_for_url(re.compile(r"/content/(publish|post)"), timeout=120_000)
        log("已进入发布页，开始填表：")
        _try("标题", lambda: _fill_title(page, job.title), log, f"标题填「{job.title}」")
        _try("描述与话题", lambda: _fill_description(page, job.description, job.topics), log,
             "描述框粘贴终端上方打印的作品描述")
        if job.cover_vertical or job.cover_horizontal:
            _try("封面", lambda: _set_cover(page, job.cover_vertical, job.cover_horizontal), log,
                 f"点「选择封面」，竖封面 {job.cover_vertical}，横封面 {job.cover_horizontal}")
        if job.ai_generated:
            _try("AI 生成声明", lambda: _declare_ai(page), log, "在「添加声明」里勾选「内容由AI生成」")
        _try("视频上传完成", lambda: _wait_uploaded(page, log), log, "等页面上传进度走完")
        log("\n表已填好。请在浏览器里逐项核对，确认无误后亲手点「发布」；不发就直接关掉浏览器窗口。")
        published = False
        try:
            while not page.is_closed():
                if PUBLISHED_URL.search(page.url):
                    published = True
                    log("检测到已发布（跳到了作品管理页）。")
                    page.wait_for_timeout(3000)
                    break
                page.wait_for_timeout(1000)
        except Error:
            pass
        try:
            ctx.close()
        except Error:
            pass
        return published


def login(log: Log = print) -> None:
    with sync_playwright() as p:
        ctx = _open(p)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        _ensure_login(page, log)
        log(f"已登录，登录态存于 {PROFILE}；关闭浏览器窗口结束。")
        try:
            while not page.is_closed():
                page.wait_for_timeout(1000)
        except Error:
            pass


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["login"])
    ap.parse_args()
    login()


if __name__ == "__main__":
    sys.exit(main())
