# -*- coding: utf-8 -*-
"""排行榜主图多来源重挑（bible §4，follow-up 005–007）。每步落盘、可续跑：

    python ai_videos/paihangbang/_tools/image_reselect.py search   <ep_dir> [--workers 4] [--batch 5]
    python ai_videos/paihangbang/_tools/image_reselect.py download <ep_dir>
    python ai_videos/paihangbang/_tools/image_reselect.py score    <ep_dir>      # 自动打分 + 新旧对照拼图
    python ai_videos/paihangbang/_tools/image_reselect.py apply    <ep_dir> [--override idx=cand ...]

- search：每 batch 项一包交给 Codex 联网搜（`codex --search exec`，ChatGPT 订阅），先经 RequestLog 记日志；只找链接，不生成图。
- download：下载候选并把现用图也作为候选 `current`；只收可商用许可（与 rank_scroll 校验同一份前缀表）。
- score：分辨率、与卡片比例的契合、色彩、对比、清晰度合成分数，写 picks.json 与对照拼图 review_*.jpg。
- apply：旧图移到 `_build/old_img/`，新图缩到长边 ≤ 2400 写回同名文件，改 assets.json / image_credit，换图项清掉 image_focus。
  image_risk 原样保留（是否放由人在发布前定）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageStat

REPO = Path(__file__).resolve().parents[5]   # ep17 副本：_build → 仓库根
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "projects" / "rank_scroll"))
from rank_scroll.contract import _licence_ok  # noqa: E402  —— 许可白名单只有一处定义
from tools.service_request import RequestLog  # noqa: E402

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"}
LONG_SIDE = 2400
CARD_H = 800
TODAY = date.today().isoformat()

SCHEMA = {"type": "object", "additionalProperties": False, "required": ["items"], "properties": {"items": {"type": "array", "items": {
    "type": "object", "additionalProperties": False, "required": ["key", "images"], "properties": {
        "key": {"type": "string"},
        "images": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                   "required": ["image_url", "page_url", "source", "author", "licence", "why"],
                   "properties": {k: {"type": "string"} for k in ("image_url", "page_url", "source", "author", "licence", "why")}}}}}}}}

PROMPT = """Use web search to find the best real photographs (not AI-generated, not renders) for each subject below, for a full-bleed {shape} poster card in a YouTube ranking video.
For EACH subject return {n} candidates (search thoroughly: Pexels, Unsplash, Pixabay, Flickr Creative Commons, Openverse, tourism boards, photographers; at least 6 if they exist). Prefer: {prefer}; strong colour (clear sky, golden hour, blue hour or night lights); sharp; long side >= 2000 px; no watermarks, no text overlays, no logos/brand signage dominating, no collage.
Do NOT use Wikimedia Commons / Wikipedia images at all (no upload.wikimedia.org). Look anywhere else: Pexels, Unsplash, Pixabay, Flickr, official building / tourism / developer / park sites, photographers' sites, travel sites.
Image quality and the classic view come first. Report the licence EXACTLY as stated on the source page (e.g. "Pexels License", "CC BY 2.0", "All rights reserved"); write "unknown" if the page does not state one. Prefer a freely licensed photo when two are equally good. Avoid stock-agency previews with watermarks (Getty, Shutterstock, Alamy, Dreamstime).
For each candidate give a DIRECT image file URL that downloads the image itself (e.g. images.pexels.com/photos/..., images.unsplash.com/photo-..., upload.wikimedia.org/..., live.staticflickr.com/..._o.jpg / _b.jpg), the page URL, the source site, the author, the exact licence name, and a short reason.
Copy each subject's key exactly. Do not run shell commands. Return only the JSON.

Subjects:
{subjects}"""


def ep_paths(ep: Path) -> dict[str, Path]:
    b = ep / "_build" / "reselect"
    return {"build": b, "cand": b / "cand", "old": ep / "_build" / "old_img", "data": ep / "data.json", "assets": ep / "assets.json"}


def load(ep: Path) -> tuple[dict, list[dict]]:
    p = ep_paths(ep)
    return json.loads(p["data"].read_text(encoding="utf-8")), json.loads(p["assets"].read_text(encoding="utf-8"))


def item_key(i: int, it: dict) -> str:
    stem = Path(it["image"]).stem if it.get("image") else re.sub(r"[^a-z0-9]+", "_", it["name"].lower()).strip("_")
    return f"{i:02d}_{stem}"


WIKI_UA = {"User-Agent": "paihangbang-image-reselect/1.0 (python-urllib; bulk thumbnail fetch, 1 req per s)"}
_wiki_lock = threading.Lock()
_wiki_last = [0.0]


def _wiki_thumb(url: str, width: int = 1920) -> str:   # 标准档宽度有缓存，非标准宽度现算、限流更严
    """upload.wikimedia.org 原图 → 指定宽度缩略图（服务器缓存命中率高、流量小，限流也松）。"""
    m = re.match(r"(https://upload\.wikimedia\.org/wikipedia/commons)/(\w)/(\w\w)/([^/]+)$", url)
    return f"{m.group(1)}/thumb/{m.group(2)}/{m.group(3)}/{m.group(4)}/{width}px-{m.group(4)}" if m else url


def get(url: str, timeout: int = 60) -> bytes:
    if "upload.wikimedia.org" not in url:
        h = dict(UA, Referer="https://www.flickr.com/", Accept="image/avif,image/webp,image/*,*/*") if "staticflickr.com" in url else UA
        return urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=timeout).read()
    # Wikimedia：单线程排队、≥1.2 s 间隔、描述性 UA；429 退避重试。并发 8 线程实测整批被 429（follow-up 007）
    tries = [_wiki_thumb(url), url] if _wiki_thumb(url) != url else [url]
    for attempt in range(5):
        for u in tries:
            with _wiki_lock:
                wait = 1.2 - (time.monotonic() - _wiki_last[0])
                if wait > 0:
                    time.sleep(wait)
                try:
                    return urllib.request.urlopen(urllib.request.Request(u, headers=WIKI_UA), timeout=timeout).read()
                except urllib.error.HTTPError as e:
                    if e.code == 429:
                        break                    # 退避后整轮重试
                    if u is tries[-1]:
                        raise
                finally:
                    _wiki_last[0] = time.monotonic()
        time.sleep(6 * (attempt + 1))
    raise RuntimeError(f"Wikimedia 429 重试 5 次仍失败：{url}")


# ── search ────────────────────────────────────────────────────────────────
def subject_line(i: int, it: dict) -> str:
    where = ", ".join(x for x in (it.get("subtitle"), it.get("country_name")) if x)
    view = ""
    if it.get("badge", "").startswith("SHARED WITH"):
        view = f" (prefer a view from the {it['country_name']} side)"
    if it.get("image_hint"):                                   # 单项补充说明（如「野生个体，不要家养型」）
        view += f" ({it['image_hint']})"
    return f"- key {item_key(i, it)}: {it['name']} — {where}{view}"


def run_search(ep: Path, batch: list[tuple[int, dict]], tag: str, shape: str, prefer: str, n: int) -> str:
    p = ep_paths(ep)
    out = p["build"] / f"codex_{tag}.json"
    if out.exists():
        return f"{tag} 已有，跳过"
    prompt = PROMPT.format(shape=shape, n=n, prefer=prefer, subjects="\n".join(subject_line(i, it) for i, it in batch))
    schema = p["build"] / "codex_schema.json"
    argv = [shutil.which("codex") or "codex", "--search", "exec", "--skip-git-repo-check", "--sandbox", "read-only",
            "--output-schema", str(schema), "-o", str(out), "-"]
    req = {"argv": argv, "prompt": prompt, "purpose": "排行榜主图候选链接（只找链接，不生成图）", "output": str(out), "cost": "ChatGPT 订阅额度，未知"}
    r = RequestLog(ep).invoke("codex_cli", "web_search", req, lambda: subprocess.run(
        argv, input=prompt, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=1200))
    return f"{tag} rc={r.returncode} {'ok' if out.exists() else 'NO OUTPUT ' + r.stderr[-200:]}"


def cmd_search(ep: Path, workers: int, size: int, only: list[int] | None = None, tag: str = "b", n: int = 6) -> None:
    p = ep_paths(ep)
    p["build"].mkdir(parents=True, exist_ok=True)
    (p["build"] / "codex_schema.json").write_text(json.dumps(SCHEMA), encoding="utf-8")
    data, _ = load(ep)
    card_w = (data.get("layout") or {}).get("card_w", 600)
    tall = card_w / CARD_H < 0.8
    shape = "portrait (3:4)" if tall else "near-square (9:10)"
    prefer = ("the whole building visible from base to spire, a classic recognisable angle, portrait orientation" if tall else
              "the summit clearly visible and recognisable, the classic view of this mountain, landscape or portrait both fine")
    prefer = (data.get("layout") or {}).get("image_prefer") or prefer   # 每期可自定（ep04 动物：野外个体、物种认得准）
    items = list(enumerate(data["items"]))
    if only:
        items = [x for x in items if x[0] in only]
    batches = [items[k:k + size] for k in range(0, len(items), size)]
    with ThreadPoolExecutor(workers) as ex:
        for msg in ex.map(lambda kb: run_search(ep, kb[1], f"{tag}{kb[0]:02d}", shape, prefer, n), enumerate(batches)):
            print(msg, flush=True)


# ── download ──────────────────────────────────────────────────────────────
def cmd_download(ep: Path) -> None:
    p = ep_paths(ep)
    data, assets = load(ep)
    by_file = {a["file"]: a for a in assets}
    found: dict[str, list[dict]] = {}
    for f in sorted(x for x in p["build"].glob("codex_*.json") if x.name != "codex_schema.json") + sorted(p["build"].glob("claude_*.json")):   # 顺序固定：codex 在前，claude 在后（候选编号 c{k} 依赖顺序）
        for row in json.loads(f.read_text(encoding="utf-8")).get("items", []):
            found.setdefault(row["key"], []).extend(row["images"])
    jobs = []
    for i, it in enumerate(data["items"]):
        key = item_key(i, it)
        d = p["cand"] / key
        d.mkdir(parents=True, exist_ok=True)
        meta = []
        fallback = None
        if it.get("image") and (ep / it["image"]).exists():          # 现图（维基）只在 Codex 一张也没找到时临时沿用
            a = by_file.get(it["image"], {})
            shutil.copy2(ep / it["image"], d / "current.jpg")
            fallback = {"id": "current", "file": "current.jpg", "licence": a.get("licence", ""), "author": a.get("author", ""),
                        "page_url": a.get("commons_page") or a.get("source_page", ""), "image_url": a.get("source_url", ""), "source": "current"}
        for k, c in enumerate(found.get(key, [])):
            if "wikimedia.org" in c["image_url"] or "wikipedia.org" in c["image_url"]:
                continue                                              # 维基只出数据文字（follow-up 009）
            meta.append({**c, "id": f"c{k}", "file": f"c{k}.jpg"})
        jobs.append((d, meta, fallback))

    def fetch(job):
        d, meta, fallback = job
        kept = []
        for m in meta:
            f = d / m["file"]
            if m["id"] != "current" and not f.exists():
                try:
                    blob = get(m["image_url"])
                    if len(blob) < 50_000:
                        continue
                    f.write_bytes(blob)
                except Exception:  # noqa: BLE001 —— 单张下载失败不影响其他候选
                    continue
            try:
                with Image.open(f) as im:
                    m["w"], m["h"] = im.size
                kept.append(m)
            except Exception:  # noqa: BLE001
                f.unlink(missing_ok=True)
        if not kept and fallback:
            with Image.open(d / fallback["file"]) as im:
                fallback["w"], fallback["h"] = im.size
            kept.append(fallback)
        (d / "meta.json").write_text(json.dumps(kept, ensure_ascii=False, indent=1), encoding="utf-8")
        return d.name, len(kept) if not (len(kept) == 1 and kept[0]["id"] == "current") else "0（沿用现图）"

    with ThreadPoolExecutor(8) as ex:
        for name, n in ex.map(fetch, jobs):
            print(f"{name}: {n} 张", flush=True)


# ── score ─────────────────────────────────────────────────────────────────
def metrics(path: Path, target: float) -> dict:
    with Image.open(path) as im0:
        im = ImageOps.exif_transpose(im0).convert("RGB")
    w, h = im.size
    a = w / h
    keep = target / a if a > target else a / target            # 裁成卡片比例后保留的比例
    s = im.copy()
    s.thumbnail((800, 800))
    r, g, b = [ImageStat.Stat(c) for c in s.split()]
    rg = [x - y for x, y in zip(s.getchannel("R").getdata(), s.getchannel("G").getdata())]
    yb = [(x + y) / 2 - z for x, y, z in zip(s.getchannel("R").getdata(), s.getchannel("G").getdata(), s.getchannel("B").getdata())]
    def sd(v):
        m = sum(v) / len(v)
        return math.sqrt(sum((x - m) ** 2 for x in v) / len(v)), m
    srg, mrg = sd(rg); syb, myb = sd(yb)
    colour = math.sqrt(srg ** 2 + syb ** 2) + 0.3 * math.sqrt(mrg ** 2 + myb ** 2)
    lum = s.convert("L")
    contrast = ImageStat.Stat(lum).stddev[0]
    edges = lum.filter(ImageFilter.FIND_EDGES)
    sharp = ImageStat.Stat(edges).stddev[0]
    return {"w": w, "h": h, "keep": round(keep, 3), "colour": round(colour, 1), "contrast": round(contrast, 1), "sharp": round(sharp, 1)}


def total(m: dict) -> float:
    res = min(1.0, min(m["w"], m["h"]) / 1800)
    return round(30 * res + 25 * min(1.0, m["keep"] / 0.75) + 20 * min(1.0, m["colour"] / 60)
                 + 10 * min(1.0, m["contrast"] / 60) + 15 * min(1.0, m["sharp"] / 30), 1)


def cmd_score(ep: Path) -> None:
    p = ep_paths(ep)
    data, _ = load(ep)
    target = (data.get("layout") or {}).get("card_w", 600) / CARD_H
    picks = {}
    for i, it in enumerate(data["items"]):
        d = p["cand"] / item_key(i, it)
        meta = json.loads((d / "meta.json").read_text(encoding="utf-8")) if (d / "meta.json").exists() else []
        for m in meta:
            try:
                m.update(metrics(d / m["file"], target)); m["score"] = total(m)
            except Exception:  # noqa: BLE001
                m["score"] = -1
        meta.sort(key=lambda m: -m["score"])
        (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
        picks[d.name] = meta[0]["id"] if meta else None
    (p["build"] / "picks.json").write_text(json.dumps(picks, ensure_ascii=False, indent=1), encoding="utf-8")
    review_sheets(ep, data, target)
    changed = sum(1 for v in picks.values() if v and v != "current")
    print(f"自动选图：{changed} 项换新，{sum(1 for v in picks.values() if v == 'current')} 项保留现图，{sum(1 for v in picks.values() if not v)} 项无候选")


def review_sheets(ep: Path, data: dict, target: float, per: int = 10) -> None:
    """每行一项：现图 | 自动选中 | 第 2、3、4 名。现图框灰，选中框绿。"""
    p = ep_paths(ep)
    picks = json.loads((p["build"] / "picks.json").read_text(encoding="utf-8"))
    TW = 220
    TH = int(TW / target)
    f = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 18)
    fs = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 14)
    items = list(enumerate(data["items"]))
    for page in range(0, len(items), per):
        rows = items[page:page + per]
        sheet = Image.new("RGB", (240 + 5 * (TW + 8), len(rows) * (TH + 30) + 10), (22, 22, 26))
        dr = ImageDraw.Draw(sheet)
        for r, (i, it) in enumerate(rows):
            key = item_key(i, it)
            d = p["cand"] / key
            meta = json.loads((d / "meta.json").read_text(encoding="utf-8")) if (d / "meta.json").exists() else []
            y = 10 + r * (TH + 30)
            dr.text((8, y), f"#{it['rank']} {it['name'][:22]}", font=f, fill=(240, 240, 240))
            dr.text((8, y + 26), f"{it.get('country_name','')}  idx {i}", font=fs, fill=(170, 170, 170))
            if it.get("image_risk"):
                dr.text((8, y + 46), "FoP 风险", font=fs, fill=(230, 90, 70))
            cur = next((m for m in meta if m["id"] == "current"), None)
            others = [m for m in meta if m["id"] != picks.get(key) and m["id"] != "current"][:3]
            chosen = next((m for m in meta if m["id"] == picks.get(key)), None)
            slots = [("现图", cur, (120, 120, 120)), ("选中", chosen, (40, 170, 80))] + [(m["id"], m, (70, 70, 80)) for m in others]
            for s, (lab, m, col) in enumerate(slots):
                x = 240 + s * (TW + 8)
                dr.rectangle([x, y, x + TW - 1, y + TH - 1], fill=col)
                if m:
                    try:
                        with Image.open(d / m["file"]) as im:
                            sheet.paste(ImageOps.fit(ImageOps.exif_transpose(im).convert("RGB"), (TW - 6, TH - 6)), (x + 3, y + 3))
                    except Exception:  # noqa: BLE001
                        pass
                    dr.text((x + 4, y + TH + 4), f"{lab} {m.get('score','')} {m.get('w','?')}×{m.get('h','?')} {m.get('source','')[:10]}", font=fs, fill=col if lab == "选中" else (200, 200, 200))
                else:
                    dr.text((x + 8, y + 8), f"{lab}：无", font=fs, fill=(230, 230, 230))
        sheet.save(p["build"] / f"review_{page // per + 1:02d}.jpg", quality=86)


# ── apply ─────────────────────────────────────────────────────────────────
def cmd_apply(ep: Path, overrides: dict[int, str]) -> None:
    p = ep_paths(ep)
    data, assets = load(ep)
    picks = json.loads((p["build"] / "picks.json").read_text(encoding="utf-8"))
    by_file = {a["file"]: a for a in assets}
    p["old"].mkdir(parents=True, exist_ok=True)
    changed = 0
    for i, it in enumerate(data["items"]):
        key = item_key(i, it)
        choice = overrides.get(i, picks.get(key))
        if not choice or choice == "current":
            continue
        d = p["cand"] / key
        m = next(x for x in json.loads((d / "meta.json").read_text(encoding="utf-8")) if x["id"] == choice)
        rel = it.get("image") or f"assets/img/{key[3:]}.jpg"
        dst = ep / rel
        if dst.exists():
            shutil.move(str(dst), p["old"] / dst.name)
        with Image.open(d / m["file"]) as im:
            im = ImageOps.exif_transpose(im).convert("RGB")
            if max(im.size) > LONG_SIDE:
                im.thumbnail((LONG_SIDE, LONG_SIDE), Image.LANCZOS)
            dst.parent.mkdir(parents=True, exist_ok=True)
            im.save(dst, quality=90)
            size = im.size
        lic = m["licence"].strip()
        attrib = not re.match(r"(public domain|pd|cc0|pexels|unsplash|pixabay)", lic, re.I)
        old = by_file.get(rel, {})
        entry = {"file": rel, "source_page": m.get("page_url", ""), "source_url": m.get("image_url", ""), "author": m.get("author", ""),
                 "licence": lic, "licence_url": licence_url(lic), "attribution_required": attrib,
                 "modified": f"downscaled to {size[0]}x{size[1]} px and re-encoded as JPEG; renderer will crop",
                 "sha256": hashlib.sha256(dst.read_bytes()).hexdigest(), "retrieved_at": TODAY,
                 "fop_note": old.get("fop_note", ""), "selected_by": f"follow-up 009 Codex 联网择优（{m.get('source','')}）"}
        if rel in by_file:
            assets[assets.index(by_file[rel])] = entry
        else:
            assets.append(entry)
        it["image"] = rel
        it["image_credit"] = f"{m.get('author') or 'Unknown'} / {lic}"
        it.pop("image_focus", None)
        risks = [r for r in str(it.get("image_risk") or "").split("; ") if r and r != "licence unknown"]
        if not _licence_ok(lic):
            risks.append("licence unknown")                       # 并入风险图签字机制（follow-up 009）
        if risks:
            it["image_risk"] = "; ".join(risks)
            it["image_note"] = it.get("image_note") or ("Photo withheld: licence unclear" if risks == ["licence unknown"] else "Photo withheld: architecture copyright")
        else:
            it.pop("image_risk", None)
            it.pop("image_note", None)
        changed += 1
    p["data"].write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    p["assets"].write_text(json.dumps(assets, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"已换 {changed} 张；旧图在 {p['old']}")


def licence_url(lic: str) -> str:
    low = lic.lower()
    if "pexels" in low: return "https://www.pexels.com/license/"
    if "unsplash" in low: return "https://unsplash.com/license"
    if "pixabay" in low: return "https://pixabay.com/service/license-summary/"
    if "cc0" in low: return "https://creativecommons.org/publicdomain/zero/1.0/"
    m = re.search(r"cc[ -]by(-sa)?\s*([\d.]+)?", low)
    if m:
        kind = "by-sa" if m.group(1) else "by"
        return f"https://creativecommons.org/licenses/{kind}/{m.group(2) or '4.0'}/"
    return ""


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=("search", "download", "score", "apply"))
    ap.add_argument("ep")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--batch", type=int, default=5)
    ap.add_argument("--only", nargs="*", type=int, default=None, help="只搜这些 idx（补搜轮）")
    ap.add_argument("--tag", default="b", help="补搜轮输出前缀，如 r2_")
    ap.add_argument("--n", type=int, default=6)
    ap.add_argument("--override", nargs="*", default=[], help="idx=候选 id（current 表示保留现图）")
    a = ap.parse_args()
    ep = Path(a.ep).resolve()
    if a.step == "search":
        cmd_search(ep, a.workers, a.batch, a.only, a.tag, a.n)
    elif a.step == "download":
        cmd_download(ep)
    elif a.step == "score":
        cmd_score(ep)
    else:
        cmd_apply(ep, {int(k): v for k, v in (o.split("=", 1) for o in a.override)})


if __name__ == "__main__":
    main()
