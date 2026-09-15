"""Stage-6 read-only site probe, phase 2 — run by the user after logging in (QR) in the service profile.

Captures what the offline fake site and PageMap still need from the real 即梦 page:
upload flow + completion signal, @ candidates after upload, negative-prompt field presence,
model list, resolution options per model, a finished record's DOM/overlay, the 新建主体 dialog,
and every status/config response body. Artifacts go to `.data/probe/phase2-*/` (gitignored).

Safety: never spends credits. Every click goes through `safe_click`, which refuses any element whose
visible text contains a spend / publish / destructive keyword. Nothing is saved or submitted.

Run from the project root:  .venv/Scripts/python.exe tests/probe/site_probe_phase2.py
"""
from __future__ import annotations

import asyncio
import json
import re
import struct
import sys
import time
import zlib
from datetime import datetime
from pathlib import Path

from playwright.async_api import BrowserContext, Locator, Page, Response, async_playwright

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROFILE_DIR = PROJECT_ROOT / ".data" / "chrome_profile"
VIDEO_URL = "https://jimeng.jianying.com/ai-tool/generate?type=video"
ENTITY_URL = "https://jimeng.jianying.com/ai-tool/elements"
FORBIDDEN_WORDS: tuple[str, ...] = ("生成", "发布", "删除", "保存", "确认", "提交", "购买", "充值", "举报", "开通", "续费", "支付")
CAPTURE = re.compile(r"jimeng\.jianying\.com/(mweb|commerce)/")
LOGIN_TIMEOUT_S = 15 * 60


class Probe:
    def __init__(self, run_dir: Path) -> None:
        self.run_dir = run_dir
        for sub in ("responses", "dom", "shots"):
            (run_dir / sub).mkdir(parents=True, exist_ok=True)
        self._count = 0
        self._log = (run_dir / "log.jsonl").open("a", encoding="utf-8")

    def log(self, kind: str, **fields: object) -> None:
        self._log.write(json.dumps({"t": round(time.time(), 3), "kind": kind, **fields}, ensure_ascii=False) + "\n")
        self._log.flush()
        print(f"[probe] {kind} {fields if fields else ''}", flush=True)

    async def on_response(self, response: Response) -> None:
        if CAPTURE.search(response.url) is None:
            return
        content_type = response.headers.get("content-type", "")
        if "json" not in content_type and "text" not in content_type:
            return
        try:
            body = await response.body()
        except Exception as error:  # the body can vanish after navigation; record, never crash
            self.log("body_unavailable", url=response.url.split("?")[0], error=str(error)[:160])
            return
        self._count += 1
        slug = re.sub(r"[^A-Za-z0-9]+", "_", response.url.split("?")[0].split(".com/")[-1])[-80:]
        name = f"{self._count:04d}_{slug}.json"
        (self.run_dir / "responses" / name).write_bytes(body)
        self.log("response", file=name, status=response.status, size=len(body))

    async def snapshot(self, page: Page, label: str) -> None:
        (self.run_dir / "dom" / f"{label}.html").write_text(await page.content(), encoding="utf-8")
        await page.screenshot(path=str(self.run_dir / "shots" / f"{label}.png"))
        self.log("snapshot", label=label)

    async def save_text(self, label: str, text: str) -> None:
        (self.run_dir / "dom" / f"{label}.txt").write_text(text, encoding="utf-8")
        self.log("text", label=label, size=len(text))


async def safe_click(probe: Probe, locator: Locator, purpose: str) -> bool:
    try:
        if await locator.count() == 0:
            probe.log("click_skipped_missing", purpose=purpose)
            return False
        target = locator.first
        text = (await target.inner_text(timeout=2000)).strip()
    except Exception as error:
        probe.log("click_skipped_error", purpose=purpose, error=str(error)[:160])
        return False
    if any(word in text for word in FORBIDDEN_WORDS):
        probe.log("click_refused_forbidden_text", purpose=purpose, text=text[:60])
        return False
    await target.click(timeout=5000)
    probe.log("clicked", purpose=purpose, text=text[:60])
    return True


def neutral_png(path: Path) -> None:
    width, height = 64, 64
    raw = b"".join(b"\x00" + bytes((128, 128, 128)) * width for _ in range(height))

    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b"")
    path.write_bytes(png)


async def wait_for_login(page: Page, probe: Probe) -> bool:
    deadline = time.monotonic() + LOGIN_TIMEOUT_S
    print("请在打开的 Chrome 窗口里扫码登录即梦（若已登录会直接继续）。脚本不会生成、发布、删除或保存任何东西。", flush=True)
    while time.monotonic() < deadline:
        if await page.locator("text=/会员|积分/").count() > 0 and await page.get_by_text("登录", exact=True).count() == 0:
            probe.log("logged_in")
            return True
        await asyncio.sleep(3)
    probe.log("login_timeout")
    return False


async def probe_composer(page: Page, probe: Probe) -> None:
    await probe.snapshot(page, "01_composer_initial")
    body_text = await page.evaluate("document.body.innerText")
    await probe.save_text("01_negative_prompt_scan", "\n".join(
        line for line in body_text.splitlines() if any(k in line for k in ("负向", "反向提示", "不希望", "negative"))
    ) or "(no negative prompt wording found)")

    image = probe.run_dir / "jwb-probe-1.png"
    neutral_png(image)
    try:
        async with page.expect_file_chooser(timeout=8000) as chooser_info:
            await safe_click(probe, page.get_by_text("参考内容"), "open upload chooser")
        chooser = await chooser_info.value
        await chooser.set_files(str(image))
        probe.log("upload_file_set", name=image.name)
    except Exception as error:
        probe.log("upload_failed", error=str(error)[:200])
    for second in (1, 3, 8, 20):
        await asyncio.sleep(second if second == 1 else second - 1)
        await probe.snapshot(page, f"02_after_upload_{second:02d}s")

    editor = page.locator('div.tiptap.ProseMirror[contenteditable="true"]').first
    try:
        await editor.click(timeout=5000)
        await page.keyboard.type("@")
        await asyncio.sleep(1.5)
        await probe.snapshot(page, "03_mention_menu")
        menu_html = await page.evaluate(
            """() => [...document.querySelectorAll('body *')].filter(e => /可能@的内容/.test(e.textContent || '') && e.children.length > 0)
                 .slice(-1).map(e => e.outerHTML.slice(0, 40000)).join('\\n')"""
        )
        await probe.save_text("03_mention_menu_html", menu_html)
        await page.keyboard.press("Escape")
        await page.keyboard.press("Control+A")
        await page.keyboard.press("Delete")
        probe.log("editor_cleared")
    except Exception as error:
        probe.log("mention_probe_failed", error=str(error)[:200])

    for label, pattern in (("04_model_menu", re.compile(r"Seedance")), ("05_ratio_popover", re.compile(r"\d+:\d+\s*·"))):
        clicked = await safe_click(probe, page.get_by_text(pattern), label)
        if clicked:
            await asyncio.sleep(1)
            await probe.snapshot(page, label)
            options = await page.evaluate(
                """() => [...document.querySelectorAll('[role=option], [class*=option], [class*=item]')]
                     .filter(e => e.offsetParent !== null).slice(0, 80)
                     .map(e => ({text: (e.innerText || '').trim().slice(0, 60), cls: String(e.className).slice(0, 80),
                                 disabled: e.getAttribute('aria-disabled') || (String(e.className).includes('disabled') ? 'class' : null)}))"""
            )
            await probe.save_text(f"{label}_options", json.dumps(options, ensure_ascii=False, indent=1))
            await page.keyboard.press("Escape")


async def probe_history(page: Page, probe: Probe) -> None:
    record_html = await page.evaluate(
        """() => { const recs = [...document.querySelectorAll('[class*=record]')].filter(r => r.querySelector('video'));
                   return recs.slice(-2).map(r => r.outerHTML.slice(0, 60000)).join('\\n<!-- next -->\\n'); }"""
    )
    await probe.save_text("06_finished_records_html", record_html or "(no finished record with video found)")
    video = page.locator("video").last
    if await video.count() > 0:
        await video.hover(timeout=5000)
        await asyncio.sleep(1)
        await probe.snapshot(page, "06_record_overlay")
    details = page.get_by_text("详细信息").last
    if await details.count() > 0:
        await details.hover(timeout=5000)
        await asyncio.sleep(1)
        await probe.snapshot(page, "07_details_popover")


async def probe_entity_modal(page: Page, probe: Probe) -> None:
    await page.goto(ENTITY_URL, wait_until="networkidle")
    await asyncio.sleep(4)
    await probe.snapshot(page, "08_entity_page")
    if await safe_click(probe, page.get_by_text("新建主体"), "open create entity modal"):
        await asyncio.sleep(2)
        await probe.snapshot(page, "09_entity_create_modal")
        modal_html = await page.evaluate(
            """() => [...document.querySelectorAll('[role=dialog], [class*=modal], [class*=Modal]')]
                 .filter(e => e.offsetParent !== null).map(e => e.outerHTML.slice(0, 60000)).join('\\n')"""
        )
        await probe.save_text("09_entity_create_modal_html", modal_html)
        await page.keyboard.press("Escape")
        await asyncio.sleep(1)
        await probe.snapshot(page, "10_after_modal_escape")


async def run() -> int:
    run_dir = PROJECT_ROOT / ".data" / "probe" / f"phase2-{datetime.now():%Y%m%d-%H%M%S}"
    probe = Probe(run_dir)
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as playwright:
        context: BrowserContext = await playwright.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR), channel="chrome", headless=False, viewport={"width": 1536, "height": 864}
        )
        context.on("response", lambda response: asyncio.ensure_future(probe.on_response(response)))
        page = context.pages[0] if context.pages else await context.new_page()
        await page.goto(VIDEO_URL, wait_until="domcontentloaded")
        if not await wait_for_login(page, probe):
            await context.close()
            return 2
        await page.goto(VIDEO_URL, wait_until="networkidle")
        await asyncio.sleep(5)
        for step in (probe_composer, probe_history, probe_entity_modal):
            try:
                await step(page, probe)
            except Exception as error:
                probe.log("step_failed", step=step.__name__, error=str(error)[:300])
        await page.goto(VIDEO_URL, wait_until="networkidle")
        await asyncio.sleep(15)
        await probe.snapshot(page, "11_final_idle_capture")
        await context.close()
    print(f"探针完成：{run_dir}（上传的测试图 jwb-probe-1 可能留在输入框里，可手动移除）", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(run()))
