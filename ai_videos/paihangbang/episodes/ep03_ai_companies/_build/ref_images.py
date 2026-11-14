# -*- coding: utf-8 -*-
"""ep03 参考图三件套：logo / 公司照片 / 创始人头像（bible §4 + follow-up 009：维基只出文字）。

2026-11-03 起（follow-up 023 / 025）本系列不再调用 Codex：`search` 子命令停用；搜图由 Claude 子代理用 WebSearch / WebFetch 完成，
结果按同一 SCHEMA 写 `_build/ref_codex/claude_<kind>_b<tag><NN>.json`，再跑 download / sheet。r1–r6 的 codex_*.json 是历史产物，照旧参与下载。

    python ai_videos/paihangbang/episodes/ep03_ai_companies/_build/ref_images.py search   [--workers 5] [--batch 5] [--kind logo|photo|person]
    python ai_videos/paihangbang/episodes/ep03_ai_companies/_build/ref_images.py download
    python ai_videos/paihangbang/episodes/ep03_ai_companies/_build/ref_images.py sheet

- search：每 batch 家一包交 Codex（`codex --search exec`，ChatGPT 订阅额度），先经 RequestLog 记日志；只找链接，不生成图。已有输出的包跳过。
- download：候选存 `assets/ref/<slug>/<kind>/cN.<ext>`，旁边 meta.json 记来源页、作者、许可、尺寸；排除维基链接。
- sheet：每类一张候选拼图 `_build/ref_sheets/<kind>_NN.jpg` 供人工挑选。
"""
from __future__ import annotations

import argparse
import io
import os
import time
import urllib.error
import json
import shutil
import subprocess
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

EP = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))
from tools.service_request import RequestLog  # noqa: E402

BUILD = EP / "_build"
OUT = BUILD / "ref_codex"
REF = EP / "assets" / "ref"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36",
      "Accept": "image/avif,image/webp,image/png,image/svg+xml,image/*,*/*;q=0.8"}
KINDS = ("logo", "photo", "person")

SCHEMA = {"type": "object", "additionalProperties": False, "required": ["items"], "properties": {"items": {"type": "array", "items": {
    "type": "object", "additionalProperties": False, "required": ["key", "images"], "properties": {
        "key": {"type": "string"},
        "images": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                   "required": ["image_url", "page_url", "source", "author", "licence", "why"],
                   "properties": {k: {"type": "string"} for k in ("image_url", "page_url", "source", "author", "licence", "why")}}}}}}}}

COMMON = """For EACH subject return up to {n} candidates. For each candidate give a DIRECT image file URL that downloads the image itself (not an HTML page), the page URL where it appears, the source site, the author / owner, the licence or usage terms EXACTLY as stated on the source page (e.g. "CC BY 2.0", "Pexels License", "press kit: free for editorial use", "All rights reserved"; write "unknown" if the page states nothing), and a short reason.
Do NOT use Wikimedia Commons / Wikipedia images at all (no upload.wikimedia.org, no wikipedia.org). Avoid stock-agency previews with watermarks (Getty, Shutterstock, Alamy, Dreamstime, 123rf), AI-generated images, collages and screenshots with UI chrome.
Copy each subject's key exactly. Do not run shell commands. Return only the JSON.

Subjects:
{subjects}"""

PROMPTS = {
    "logo": """Use web search to find the CURRENT official logo (as of late 2026) of each AI company below, for identification on a YouTube info card.
Best sources, in order: the company's own brand / press-kit / media-assets page, the logo file used on its official website (header SVG or PNG), its official GitHub or Hugging Face organisation avatar, reputable logo repositories that mirror the official file (e.g. Simple Icons, svgl, brandfetch CDN, seeklogo).
Prefer: (1) the full horizontal lockup (symbol + wordmark) in colour or black on a transparent background, SVG or large PNG; (2) also the symbol-only mark if it exists; (3) a white/reversed version only as an extra.
""" + COMMON,
    "photo": """Use web search to find the best real photographs that represent each AI company below, for the full-bleed background of a YouTube info card (portrait-ish 9:10 crop, text overlaid at the bottom).
Prefer, in order: the company's headquarters or office building with its name/logo signage visible; the office interior or reception with the logo; official newsroom / press-kit photos of the team, lab, robots or product in use; a well-known event or launch photo of the company. Real photos only (no renders of the logo, no product screenshots, no stock photos of generic offices that are not this company).
Long side >= 1600 px, sharp, good colour, no watermark. Flickr photos under Creative Commons (e.g. Web Summit, TechCrunch, conference accounts) and Unsplash / Pexels photos of the actual office are welcome; official press photos are fine too — report their terms exactly.
""" + COMMON,
    "person": """Use web search to find a clear, recent head-and-shoulders photograph (a "headshot") of the named founder of each AI company below, to be shown in a small circle on a YouTube info card.
Prefer: face clearly visible and roughly front-facing, sharp, eyes open, neutral or smiling, plain or softly blurred background, long side >= 800 px. Good sources: the company's official team / about / press page, official press-kit headshots, conference photos released under Creative Commons on Flickr (Web Summit, TechCrunch Disrupt, Collision, VivaTech, World Economic Forum, government / university accounts), university profile photos.
It must be the right person — double-check the name. No group photos where the face is tiny, no caricatures or AI images.
""" + COMMON,
}


def companies() -> list[dict]:
    return json.loads((BUILD / "companies.json").read_text(encoding="utf-8"))


RESEARCH = BUILD / "research"


def research() -> dict[str, dict]:
    """Step 1 output (follow-up 017): facts per slug, matched by order of companies.json within each batch file."""
    out: dict[str, dict] = {}
    rows = []
    for f in sorted(RESEARCH.glob("batch_*.json")):
        rows += json.loads(f.read_text(encoding="utf-8")).get("companies", [])
    def norm(x: str) -> str:
        return "".join(ch for ch in x.lower() if ch.isalnum())
    for c in companies():
        key = norm(c["name"].split("(")[0])
        for r in rows:
            if norm(str(r.get("name", "")).split("(")[0]).startswith(key[:6]) or key.startswith(norm(str(r.get("name", "")).split("(")[0])[:6]):
                out[c["slug"]] = r
                break
    return out


def content_line(kind: str, c: dict, r: dict) -> str:
    """Subject line written from the step-1 research, so Codex searches for what this company is actually known for."""
    prods = ", ".join(r.get("products") or [])
    cat = "/".join(r.get("category") or [])
    where = f"{r.get('hq_city') or c['hq']}, {r.get('country_name') or ''}".strip(", ")
    status = str(r.get("status") or "")[:220]
    if kind == "person":
        hf = r.get("headshot_founder")
        who = hf if isinstance(hf, str) else (hf or {}).get("name") or c["founder"]
        return (f"- key {c['slug']}: {who} — founder of {r.get('name') or c['name']} ({cat}; products: {prods}; {where}). "
                f"Company status: {status}")
    if kind == "logo":
        return f"- key {c['slug']}: {r.get('name') or c['name']} ({cat}; products: {prods}; {where}). Status: {status}"
    return (f"- key {c['slug']}: {r.get('name') or c['name']} — {cat} company in {where}; known for {prods}. Status: {status}\n"
            f"  Good subjects for this company: its headquarters / office with signage in {r.get('hq_city') or c['hq']}; "
            f"its products in real use ({prods}); its launch events, demos, robots or devices; its founders at the company.")


def subject_line(kind: str, c: dict) -> str:
    if kind == "person":
        return f"- key {c['slug']}: {c['founder']} — {c['role']} of {c['name']} ({c['hq']})"
    return f"- key {c['slug']}: {c['name']} — AI company, {c['hq']}"


def run_search(kind: str, k: int, batch: list[dict], n: int, tag: str = "", content: dict | None = None) -> str:
    out = OUT / f"codex_{kind}_b{tag}{k:02d}.json"
    if out.exists():
        return f"{out.name} 已有，跳过"
    lines = [content_line(kind, c, content[c["slug"]]) if content and c["slug"] in content else subject_line(kind, c) for c in batch]
    prompt = PROMPTS[kind].format(n=n, subjects="\n".join(lines))
    if content:
        prompt = prompt.replace("Subjects:", "Each subject comes with researched facts about the company (products, HQ, status). Use them to search for images of what the company is actually known for. Quality is essential: only high-resolution, sharp images; give as many good candidates as you can find, up to the limit.\n\nSubjects:")
    if tag:
        prompt = prompt.replace("Subjects:", "A previous search found nothing usable for these subjects (dead links, wrong person, tiny or off-topic images), so look harder and verify that each URL returns the image itself.\n\nSubjects:")
    schema = OUT / "codex_schema.json"
    argv = [shutil.which("codex") or "codex", "--search", "exec", "--skip-git-repo-check", "--sandbox", "read-only",
            "--output-schema", str(schema), "-o", str(out), "-"]
    req = {"argv": argv, "prompt": prompt, "purpose": f"ep03 参考图候选链接（{kind}；只找链接，不生成图）", "output": str(out),
           "cost": "ChatGPT 订阅额度，未知"}
    r = RequestLog(EP).invoke("codex_cli", "web_search", req, lambda: subprocess.run(
        argv, input=prompt, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=1500))
    return f"{out.name} rc={r.returncode} {'ok' if out.exists() else 'NO OUTPUT ' + r.stderr[-300:]}"


def cmd_search(workers: int, size: int, kinds: list[str], only: list[str] | None = None, tag: str = "", use_content: bool = False, n: int = 0) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "codex_schema.json").write_text(json.dumps(SCHEMA), encoding="utf-8")
    jobs = []
    for kind in kinds:
        cs = [c for c in companies() if not only or f"{kind}:{c['slug']}" in only or c["slug"] in only]
        nk = n or (4 if kind == "logo" else 6)
        content = research() if use_content else None
        if use_content:
            missing = [c["slug"] for c in cs if c["slug"] not in content]
            if missing:
                raise SystemExit(f"step 1 research missing for {missing}; finish the content research first (follow-up 017)")
        jobs += [(kind, k, cs[i:i + size], nk, tag, content) for k, i in enumerate(range(0, len(cs), size))]
    with ThreadPoolExecutor(workers) as ex:
        for msg in ex.map(lambda j: run_search(*j), jobs):
            print(msg, flush=True)


def _ext(blob: bytes, url: str) -> str | None:
    head = blob[:512].lstrip()
    if head[:5].lower() in (b"<?xml", b"<svg ") or b"<svg" in head.lower():
        return "svg"
    try:
        with Image.open(io.BytesIO(blob)) as im:
            return {"JPEG": "jpg", "PNG": "png", "WEBP": "webp", "GIF": "gif", "AVIF": "avif"}.get(im.format, None)
    except Exception:  # noqa: BLE001
        return None


def cmd_download() -> None:
    found: dict[tuple[str, str], list[dict]] = {}
    for f in sorted([*OUT.glob("codex_*_b*.json"), *OUT.glob("claude_*_b*.json")]):
        kind = f.stem.split("_")[1]
        rnd = f.name.split("_b")[1][:2] if "_br" in f.name else ""
        for row in json.loads(f.read_text(encoding="utf-8")).get("items", []):
            found.setdefault((row["key"], kind), []).extend({**x, "_rnd": rnd} for x in row["images"])
    jobs = []
    for c in companies():
        for kind in KINDS:
            cands = [x for x in found.get((c["slug"], kind), []) if "wikimedia.org" not in x["image_url"] and "wikipedia.org" not in x["image_url"]]
            jobs.append((c["slug"], kind, cands))

    def fetch(job):
        slug, kind, cands = job
        d = REF / slug / kind
        d.mkdir(parents=True, exist_ok=True)
        kept = []
        minsize = 1_500 if kind == "logo" else 15_000
        seen: dict[str, int] = {}
        for m in cands:
            rnd = m.pop("_rnd", "")
            k = seen[rnd] = seen.get(rnd, -1) + 1
            m = {**m, "id": f"{rnd}c{k}"}
            old = list(d.glob(f"{m['id']}.*"))
            if old:
                m["file"] = old[0].name
            else:
                blob = None
                for attempt in range(int(os.environ.get("DL_RETRIES", "1"))):
                    try:
                        blob = urllib.request.urlopen(urllib.request.Request(m["image_url"], headers=UA), timeout=45).read()
                        m.pop("error", None)
                        break
                    except urllib.error.HTTPError as e:  # Flickr 429：退避后重试（慢速模式）
                        m["error"] = str(e)[:120]
                        if e.code != 429:
                            break
                        time.sleep(30 * (attempt + 1))
                    except Exception as e:  # noqa: BLE001 —— 单张失败不影响其他候选
                        m["error"] = str(e)[:120]
                        break
                    finally:
                        time.sleep(float(os.environ.get("DL_DELAY", "0")))
                if blob is None:
                    kept.append(m)
                    continue
                ext = _ext(blob, m["image_url"])
                if not ext or len(blob) < minsize:
                    m["error"] = f"not an image or too small ({len(blob)} B)"
                    kept.append(m)
                    continue
                m["file"] = f"{m['id']}.{ext}"
                (d / m["file"]).write_bytes(blob)
            if m["file"].endswith(".svg"):
                m["w"] = m["h"] = None
            else:
                try:
                    with Image.open(d / m["file"]) as im:
                        m["w"], m["h"] = im.size
                except Exception:  # noqa: BLE001
                    m["error"] = "unreadable"
            kept.append(m)
        (d / "meta.json").write_text(json.dumps(kept, ensure_ascii=False, indent=1), encoding="utf-8")
        ok = sum(1 for m in kept if "file" in m and "error" not in m)
        return f"{slug}/{kind}: {ok}/{len(cands)}"

    with ThreadPoolExecutor(int(os.environ.get("DL_WORKERS", "10"))) as ex:
        for msg in ex.map(fetch, jobs):
            print(msg, flush=True)


def _thumb(path: Path, size: tuple[int, int], bg) -> Image.Image | None:
    try:
        if path.suffix == ".svg":
            sys.path.insert(0, str(BUILD))
            from svgfix import load_svg
            im = load_svg(path, size[1] * 2)
            if im is None:
                return None
        else:
            im = Image.open(path)
            im = ImageOps.exif_transpose(im).convert("RGBA")
        base = Image.new("RGBA", size, bg)
        im.thumbnail(size)
        base.alpha_composite(im, ((size[0] - im.width) // 2, (size[1] - im.height) // 2))
        return base.convert("RGB")
    except Exception:  # noqa: BLE001
        return None


GATE = {"photo": 1600, "person": 600}   # follow-up 017 quality gate: photo long side, headshot short side (px)


def gate(kind: str, m: dict) -> bool:
    w, h = m.get("w"), m.get("h")
    if kind == "logo":
        return m["file"].endswith(".svg") or (w or 0) >= 400 or (h or 0) >= 200
    if not w or not h:
        return False
    return (max(w, h) if kind == "photo" else min(w, h)) >= GATE[kind]


def cmd_sheet(per: int = 10) -> None:
    sd = BUILD / "ref_sheets"
    sd.mkdir(exist_ok=True)
    f = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 17)
    fs = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 13)
    cs = companies()
    for kind in KINDS:
        tw, th = {"logo": (240, 120), "photo": (220, 244), "person": (170, 200)}[kind]
        ncol = {"logo": 6, "photo": 8, "person": 8}[kind]
        for page in range(0, len(cs), per):
            rows = cs[page:page + per]
            sheet = Image.new("RGB", (190 + ncol * (tw + 8), len(rows) * (th + 34) + 10), (24, 24, 28))
            dr = ImageDraw.Draw(sheet)
            for r, c in enumerate(rows):
                y = 10 + r * (th + 34)
                dr.text((8, y), c["slug"][:18], font=f, fill=(240, 240, 240))
                if kind == "person":
                    dr.text((8, y + 24), c["founder"][:22], font=fs, fill=(170, 170, 170))
                d = REF / c["slug"] / kind
                meta = json.loads((d / "meta.json").read_text(encoding="utf-8")) if (d / "meta.json").exists() else []
                meta = [m for m in meta if "file" in m and "error" not in m]
                meta.sort(key=lambda m: (not gate(kind, m), -((m.get("w") or 9999) * (m.get("h") or 9999))))
                meta = meta[:ncol]
                for s, m in enumerate(meta):
                    x = 190 + s * (tw + 8)
                    bg = (235, 235, 235, 255) if kind == "logo" else (60, 60, 60, 255)
                    t = _thumb(d / m["file"], (tw, th), bg)
                    if t:
                        sheet.paste(t, (x, y))
                    lic = m.get("licence", "")[:16]
                    dims = f"{m.get('w') or 'svg'}x{m.get('h') or ''}"
                    ok = gate(kind, m)
                    dr.rectangle([x, y + th, x + tw - 1, y + th + 2], fill=(40, 190, 90) if ok else (220, 60, 50))
                    dr.text((x + 2, y + th + 3), f"{m['id']} {dims} {lic}", font=fs, fill=(200, 200, 200) if ok else (230, 120, 110))
            out = sd / f"{kind}_{page // per + 1:02d}.jpg"
            sheet.save(out, quality=88)
            print(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search")
    s.add_argument("--workers", type=int, default=5)
    s.add_argument("--batch", type=int, default=5)
    s.add_argument("--kind", choices=KINDS, action="append")
    s.add_argument("--only", nargs="*", default=None, help="kind:slug or slug")
    s.add_argument("--tag", default="", help="round tag for output names, e.g. r2_")
    s.add_argument("--content", action="store_true", help="write subject lines from the step-1 research (follow-up 017)")
    s.add_argument("--n", type=int, default=0, help="candidates per subject")
    sub.add_parser("download")
    sub.add_parser("sheet")
    a = ap.parse_args()
    if a.cmd == "search":
        raise SystemExit("search 已停用（follow-up 023 / 025）：由 Claude 子代理搜图并写 claude_<kind>_b<tag><NN>.json，再跑 download")
        kinds = a.kind or (sorted({x.split(":")[0] for x in a.only if ":" in x}) if a.only else None) or list(KINDS)
        cmd_search(a.workers, a.batch, kinds, a.only, a.tag, a.content, a.n)
    elif a.cmd == "download":
        cmd_download()
    else:
        cmd_sheet()


if __name__ == "__main__":
    main()
