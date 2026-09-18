# -*- coding: utf-8 -*-
"""出图适配器：ElevenLabs Flows（`/v1/flows/image`）。物件三视图与场景图都走它。

为什么是 ElevenLabs 而不是直连 OpenAI
------------------------------------
2026-09-17 用户指出网页端能选 GPT Image 2 —— 他是对的，我先前说「ElevenLabs 没有图像能力」
是错的。实测 `https://api.elevenlabs.io/openapi.json`：`/v1/flows/image` 是一个**多厂商**
图像入口，`model_id` 判别式支持
    gpt-image-1 / gpt-image-1.5 / **gpt-image-2**
    gemini-2.5-flash-image / gemini-3-pro-image / gemini-3.1-flash-image / -flash-lite
    bytedance-seedream-5-lite / **bytedance-seedream-5-pro**（本仓库一直在用的 Seedream 一家）
于是一个 key 同时覆盖出图与配音，不用再多要一把 OpenAI 的 key。

权限实测（同日）
    POST /v1/flows/image        → 422 参数错  ＝ **有权限**，只是 body 没写对
    GET  /v1/flows/image（列表） → 402 需要 Pro 套餐
    GET  /v1/voices、/v1/user    → 401 缺 voices_read / user_read
所以「创建图像」这一项当前 key 就能用；缺的是那几个**读**权限。

出图次序（用户 2026-09-17 定，`gen_object_cards.py` 的卡按它排）
    `-1 正面`  纯文字生成 → **它就是那张参考**
    `-2 侧面`  把 `-1` 挂进 `images`（按 generation_id 引用，不必重传字节），**只换机位**
    `-3 背面`  同上
三张正交图各自独立生成时不会互相同意——形制、比例、部件位置各漂各的；钉死一张，后两张只换机位。

用法（仓库根目录）：
    python tools/image_fetch.py --object p13            # 出该物件三视图
    python tools/image_fetch.py --object all            # 清单里所有物件
    python tools/image_fetch.py --scene bg1-1           # 场景图（16:9、2K）
    python tools/image_fetch.py --object p13 --dry-run  # 只看要发的 prompt，不花钱
    --model / --quality / --resolution 可改；默认 gpt-image-2 + medium（用户定）

key 只从环境 / 仓库根 gitignored `.env` 读（`ELEVENLABS_API_KEY`），不进任何被 git 跟踪的文件。
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import ssl
import subprocess
import sys
import time
import tomllib
import urllib.error
import urllib.request
import uuid
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent.parent
SK1 = REPO / "ai_videos" / "shikong_lvxing" / "sk1" / "2_世界观人设"
API = "https://api.elevenlabs.io/v1"
CTX = ssl.create_default_context()
TMP = Path(os.environ.get("TEMP") or "/tmp")
DEFAULT_MODEL = "gpt-image-2"
# 这几行是给出图的人看的上传说明，不是画面内容 —— 发给模型只会污染 prompt
DROP_FIELDS = ("参考:", "参考用法:", "比例:", "上传:")
MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}


def api_key() -> str:
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        env = REPO / ".env"
        if env.is_file():
            for line in env.read_text(encoding="utf-8").splitlines():
                if line.strip().startswith("ELEVENLABS_API_KEY="):
                    key = line.split("=", 1)[1].strip()
                    break
    if not key:
        raise SystemExit("缺 ELEVENLABS_API_KEY：写进仓库根的 .env（已 gitignore），或设进环境变量")
    return key


def _curl(args: list[str], *, timeout: int) -> tuple[int, bytes]:
    """所有 HTTP 都走 curl。

    2026-09-17 实测：urllib 打 `api.elevenlabs.io` 与 `storage.googleapis.com` 会间歇性
    `SSLEOFError` / `RemoteDisconnected`（同一个请求一分钟前还好好的），curl 带 --retry 稳。
    另外 curl 是 Windows 原生二进制，**不能直接写中文路径**（会报 `client returned ERROR on write`），
    所以一律先落 ASCII 临时文件，再由 Python 搬到目标位置。
    """
    out = TMP / f"curl_{uuid.uuid4().hex}.bin"
    cmd = ["curl", "-sS", "--retry", "8", "--retry-all-errors", "--retry-delay", "5",
           "--retry-connrefused",
           "-m", str(timeout), "-o", str(out), "-w", "%{http_code}", *args]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 60)
        code = int((r.stdout or "0").strip() or 0)
        data = out.read_bytes() if out.is_file() else b""
        if code == 0 and r.stderr:
            raise SystemExit(f"curl 失败：{r.stderr.strip()[:300]}")
        return code, data
    finally:
        out.unlink(missing_ok=True)


def _api(method: str, path: str, key: str, payload: dict | None = None, *, timeout: int = 600) -> dict:
    args = ["-X", method, f"{API}{path}", "-H", f"xi-api-key: {key}"]
    body_file = None
    if payload is not None:
        body_file = TMP / f"body_{uuid.uuid4().hex}.json"
        body_file.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        args += ["-H", "Content-Type: application/json", "--data-binary", f"@{body_file}"]
    try:
        code, data = _curl(args, timeout=timeout)
    finally:
        if body_file:
            body_file.unlink(missing_ok=True)
    txt = data.decode("utf-8", "replace")
    if code == 401:
        raise SystemExit(f"401 key 权限不够（网页端能用 ≠ API key 有这一项权限）：{txt[:200]}")
    if code == 402:
        raise SystemExit(f"402 套餐不够（/flows/image 需要 Pro 及以上）：{txt[:200]}")
    if not 200 <= code < 300:
        raise SystemExit(f"ElevenLabs {method} {path} HTTP {code}：{txt[:300]}")
    return json.loads(txt)


def download(url: str, dest: Path) -> Path:
    code, data = _curl(["-L", url], timeout=300)
    if not 200 <= code < 300 or not data:
        raise SystemExit(f"下载失败 HTTP {code}（signed URL 约 1 小时过期）")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return dest


def inline(p: Path) -> dict:
    return {"type": "inline_base64", "mime_type": MIME.get(p.suffix.lower(), "image/png"),
            "content_base64": base64.b64encode(p.read_bytes()).decode()}


def create(key: str, prompt: str, *, model: str, quality: str, aspect: str, resolution: str,
           refs: list[dict] | None = None) -> str:
    payload = {"model_id": model, "prompt": prompt, "quality": quality,
               "aspect_ratio": aspect, "resolution": resolution}
    if refs:
        payload["images"] = refs
    data = _api("POST", "/flows/image", key, payload)
    gid = data.get("id") or data.get("generation_id")
    if not gid:
        raise SystemExit(f"没拿到 generation id：{json.dumps(data, ensure_ascii=False)[:300]}")
    return gid


def wait_download(key: str, gid: str, out: Path, timeout_s: int = 600) -> Path:
    t0 = time.time()
    while True:
        d = _api("GET", f"/flows/image/{gid}", key, timeout=120)
        st = d.get("status")
        if st == "completed":
            return download(d["content_url"], out)
        if st == "failed":
            raise SystemExit(f"生成失败：{json.dumps(d, ensure_ascii=False)[:300]}")
        if time.time() - t0 > timeout_s:
            raise SystemExit(f"等超时（{timeout_s}s），最后状态 {st}")
        time.sleep(4)


def prompt_blocks(md: Path) -> list[tuple[str, str]]:
    """卡里的每个 ```text 块 → (路由键, 发给模型的 prompt)。"""
    out = []
    for m in re.finditer("```text" + chr(10) + "((?s:.)*?)" + chr(10) + "```", md.read_text(encoding="utf-8")):
        body = m.group(1)
        rk = body.split(chr(10))[0].strip().split("_")[0]
        if not re.fullmatch(r"(?:bg|p|c)\d+-\d+", rk):
            continue
        lines = [l for l in body.split(chr(10))[1:] if not l.startswith(DROP_FIELDS)]
        out.append((rk, chr(10).join(lines).strip()))
    return out


def run_object(key: str, pkey: str, args) -> None:
    hits = sorted((SK1 / "props").glob(f"{pkey}_*/{pkey}_*.md"))
    if len(hits) != 1:
        raise SystemExit(f"{pkey}：找到 {len(hits)} 张卡，要正好 1 张")
    card, folder = hits[0], hits[0].parent
    blocks = prompt_blocks(card)
    if len(blocks) != 3:
        raise SystemExit(f"{pkey}：卡里有 {len(blocks)} 个图 prompt，要正好 3 个（正/侧/背）")
    print(f"■ {folder.name}")
    front_gid: str | None = None
    for i, (rk, prompt) in enumerate(blocks):
        out = folder / f"{rk}.png"
        if out.is_file() and not args.force:
            print(f"  · {rk} 已存在，跳过（--force 覆盖）")
            continue
        if args.dry_run:
            print(f"  · {rk} {'[文生图]' if i == 0 else '[以 -1 为参考]'} {len(prompt)} 字")
            continue
        t0 = time.time()
        refs = None
        if i:
            # 优先按 generation_id 引用（省一次上传）；正面是上一轮出的就退回内联字节
            if front_gid:
                refs = [{"type": "generation", "generation_id": front_gid}]
            else:
                f = folder / f"{pkey}-1.png"
                if not f.is_file():
                    raise SystemExit(f"{rk} 要拿 {f.name} 当参考，但它还没出来")
                refs = [inline(f)]
        gid = create(key, prompt, model=args.model, quality=args.quality,
                     aspect=args.aspect, resolution=args.resolution, refs=refs)
        wait_download(key, gid, out)
        if i == 0:
            front_gid = gid
        print(f"  ✓ {rk}.png  {out.stat().st_size // 1024} KB  {time.time() - t0:.0f}s")


def run_scene(key: str, rk: str, args) -> None:
    stem = rk.split("-")[0]
    hits = (sorted(SK1.glob(f"scenes/*/{stem}_*/{stem}_*.md"))
            or sorted(SK1.glob(f"props/{stem}_*/{stem}_*.md"))
            or sorted(SK1.glob(f"characters/{stem}_*/{stem}_*.md")))
    if len(hits) != 1:
        raise SystemExit(f"{rk}：找到 {len(hits)} 张卡，要正好 1 张")
    card = hits[0]
    block = next((p for k, p in prompt_blocks(card) if k == rk), None)
    if block is None:
        raise SystemExit(f"{card.name} 里没有 {rk} 的 prompt")
    out = card.parent / f"{rk}.png"
    if out.is_file() and not args.force:
        print(f"· {rk} 已存在，跳过（--force 覆盖）")
        return
    if args.dry_run:
        print(f"· {rk} [文生图 {args.scene_aspect} {args.scene_resolution}] {len(block)} 字")
        return
    t0 = time.time()
    gid = create(key, block, model=args.model, quality=args.quality,
                 aspect=args.scene_aspect, resolution=args.scene_resolution)
    wait_download(key, gid, out)
    print(f"✓ {out.relative_to(REPO)}  {out.stat().st_size // 1024} KB  {time.time() - t0:.0f}s")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--object", help="pNN，或 all（清单里所有物件）")
    ap.add_argument("--scene", help="场景图路由键，如 bg1-1")
    ap.add_argument("--model", default=DEFAULT_MODEL,
                    help="gpt-image-2 / gpt-image-1.5 / gemini-3-pro-image / bytedance-seedream-5-pro …")
    ap.add_argument("--quality", default="medium", choices=("low", "medium", "high"))
    ap.add_argument("--resolution", default="1K", choices=("1K", "2K", "4K"), help="物件三视图（工装图，够喂重建即可）")
    ap.add_argument("--aspect", default="1:1", help="物件三视图画幅")
    ap.add_argument("--scene-resolution", default="2K", choices=("1K", "2K", "4K"))
    ap.add_argument("--scene-aspect", default="16:9")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true", help="已存在也重出")
    args = ap.parse_args()
    key = "DRY" if args.dry_run else api_key()

    if args.object:
        keys = [args.object]
        if args.object == "all":
            inv = tomllib.loads((SK1 / "object_inventory.toml").read_text(encoding="utf-8"))
            keys = [o["key"] for o in inv["object"]]
        failed: list[str] = []
        for k in keys:
            try:
                run_object(key, k, args)
            except SystemExit as e:              # 单个物件失败 → 记下、继续下一个
                print(f"  ✗ {k} 失败：{str(e)[:160]}", flush=True)
                failed.append(k)
        if failed:
            print("")
            names = ", ".join(failed)
            print(f"失败 {len(failed)} 个：{names}　（重跑同一条命令即可续，已出的会跳过）")
    elif args.scene:
        run_scene(key, args.scene, args)
    else:
        ap.error("给 --object 或 --scene")


if __name__ == "__main__":
    main()
