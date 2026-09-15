"""Stage-6 U4 read-only site probe, phase 1 (capture only — no clicks, no typing, no uploads).

Opens the service's dedicated Chrome profile, waits for the user to log in by hand, then only
navigates between the video creation page and the entity page while passively recording:
response bodies of the status/config/entity/credit endpoints, DOM snapshots and screenshots.
Everything lands under `.data/probe/run-*/` (gitignored). Nothing is ever clicked.

Run from the project root:  .venv/Scripts/python.exe tests/probe/site_probe_phase1.py
"""
from __future__ import annotations

import asyncio
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

from playwright.async_api import BrowserContext, Page, Response, async_playwright

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROFILE_DIR = PROJECT_ROOT / ".data" / "chrome_profile"
VIDEO_URL = "https://jimeng.jianying.com/ai-tool/generate?type=video"
ENTITY_URL = "https://jimeng.jianying.com/ai-tool/elements"
CAPTURE = re.compile(
    r"/(get_history_by_ids|get_history_queue_info|dreamina_subject/get|get_common_config|"
    r"user_credit|get_asset_list|get_agent_config|batch_get_user_benefit|subscribe_session)"
)
LOGIN_TIMEOUT_S = 15 * 60
IDLE_CAPTURE_S = 45


class Recorder:
    def __init__(self, run_dir: Path) -> None:
        self._run_dir = run_dir
        self._count = 0
        for sub in ("responses", "dom", "shots"):
            (run_dir / sub).mkdir(parents=True, exist_ok=True)
        self._log = (run_dir / "log.jsonl").open("a", encoding="utf-8")

    def log(self, kind: str, **fields: object) -> None:
        self._log.write(json.dumps({"t": round(time.time(), 3), "kind": kind, **fields}, ensure_ascii=False) + "\n")
        self._log.flush()

    async def on_response(self, response: Response) -> None:
        match = CAPTURE.search(response.url)
        if match is None:
            return
        try:
            body = await response.body()
        except Exception as error:  # body can vanish after navigation; count it, never crash the probe
            self.log("body_unavailable", url=response.url.split("?")[0], error=str(error)[:200])
            return
        self._count += 1
        name = f"{self._count:03d}_{match.group(1).replace('/', '_')}.json"
        (self._run_dir / "responses" / name).write_bytes(body)
        self.log("response", file=name, url=response.url.split("?")[0], status=response.status, size=len(body))

    async def snapshot(self, page: Page, label: str) -> None:
        (self._run_dir / "dom" / f"{label}.html").write_text(await page.content(), encoding="utf-8")
        await page.screenshot(path=str(self._run_dir / "shots" / f"{label}.png"), full_page=False)
        self.log("snapshot", label=label, url=page.url)


async def wait_for_login(page: Page, recorder: Recorder) -> bool:
    deadline = time.monotonic() + LOGIN_TIMEOUT_S
    print("请在打开的 Chrome 窗口里手动登录即梦（扫码）。脚本只等待，不会点击任何东西。", flush=True)
    while time.monotonic() < deadline:
        member_marks = await page.locator("text=/会员|积分/").count()
        login_buttons = await page.get_by_text("登录", exact=True).count()
        if member_marks > 0 and login_buttons == 0:
            recorder.log("logged_in")
            return True
        await asyncio.sleep(3)
    recorder.log("login_timeout")
    return False


async def run() -> int:
    run_dir = PROJECT_ROOT / ".data" / "probe" / f"run-{datetime.now():%Y%m%d-%H%M%S}"
    recorder = Recorder(run_dir)
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as playwright:
        context: BrowserContext = await playwright.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR), channel="chrome", headless=False, viewport={"width": 1536, "height": 864}
        )
        context.on("response", lambda response: asyncio.ensure_future(recorder.on_response(response)))
        page = context.pages[0] if context.pages else await context.new_page()
        recorder.log("browser", version=context.browser.version if context.browser else "persistent")
        await page.goto(VIDEO_URL, wait_until="domcontentloaded")
        if not await wait_for_login(page, recorder):
            print("登录超时，探针结束。", flush=True)
            await context.close()
            return 2
        await page.goto(VIDEO_URL, wait_until="networkidle")
        await asyncio.sleep(5)
        await recorder.snapshot(page, "video_page_loaded")
        await asyncio.sleep(IDLE_CAPTURE_S)
        await recorder.snapshot(page, "video_page_after_idle")
        await page.goto(ENTITY_URL, wait_until="networkidle")
        await asyncio.sleep(5)
        await recorder.snapshot(page, "entity_page")
        await page.goto(VIDEO_URL, wait_until="networkidle")
        await asyncio.sleep(10)
        await recorder.snapshot(page, "video_page_return")
        await context.close()
    print(f"探针完成：{run_dir}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(run()))
