# -*- coding: utf-8 -*-
"""排行榜每张卡的主图：两步走（follow-up 021，用户 2026-11-03「先下载到内容，再根据内容让 Codex research 和下载或生成」）。

    python ai_videos/paihangbang/_tools/tile_images.py content  <ep_dir>                 # 第一步：下载内容
    python ai_videos/paihangbang/_tools/tile_images.py research <ep_dir> [--only k ...] [--workers 3] [--batch 2]
    python ai_videos/paihangbang/_tools/tile_images.py score    <ep_dir>                 # 打分 + 拼图（人工过）
    python ai_videos/paihangbang/_tools/tile_images.py generate <ep_dir> --only k ...    # 找不到合格真实照片时出图
    python ai_videos/paihangbang/_tools/tile_images.py apply    <ep_dir> [--override idx=cand ...]

第一步 content：每张卡按 Wikidata QID 找英文维基条目，存正文摘要、简介、坐标，再存 1 张维基首图 `ref.jpg`
  —— 只用来认主体（给 Codex 和人核对），不进成片（follow-up 009：维基只出内容与文字）。落盘 `_build/tiles/<key>/`。
第二步（follow-up 027 起由 Claude 子代理按同一格式完成，任务说明见同目录 tile_research_brief.md；下面的 research 命令是原 Codex 路径，保留备用）：Codex 联网（`codex --search exec`，工作区可写 + 联网下载）逐卡读 content.md 与 ref.jpg，先写视觉简报，
  再找 ≥ 6 张真实照片，自己下载到 `<key>/cand/`、核对主体，写 `<key>/candidates.json`（来源 / 作者 / 许可照实写）。
  调用前经 RequestLog 记日志。找不到合格照片的卡由 generate 走 tools/codex_image.py 出写实插图（卡上署名 Illustration: AI-generated, not a photo）。
每步落盘、可续跑；已有结果的卡跳过。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "projects" / "rank_scroll"))
sys.path.insert(0, str(HERE))
from image_reselect import get, licence_url  # noqa: E402  —— 维基限流下载、许可链接共用一处
from rank_scroll.contract import _licence_ok  # noqa: E402
from tools.service_request import RequestLog  # noqa: E402

CARD_H = 800
MIN_CROP_H = 1000        # 裁成卡片比例后的高度下限：1080p 下卡高 800×1.06，留余量不放大
LONG_SIDE = 2400
TODAY = date.today().isoformat()
WIKI_API = "https://en.wikipedia.org/w/api.php"
WD_API = "https://www.wikidata.org/w/api.php"


def tiles_dir(ep: Path) -> Path:
    return ep / "_build" / "tiles"


def load(ep: Path) -> tuple[dict, list[dict]]:
    return (json.loads((ep / "data.json").read_text(encoding="utf-8")),
            json.loads((ep / "assets.json").read_text(encoding="utf-8")))


def tile_key(i: int, it: dict) -> str:
    return f"{i:02d}_" + re.sub(r"[^a-z0-9]+", "_", it["name"].lower()).strip("_")


def target_aspect(data: dict) -> float:
    return (data.get("layout") or {}).get("card_w", 600) / CARD_H


API_UA = {"User-Agent": "paihangbang-tile-content/1.0 (ranking-video research script; python-urllib; 1 request per 1.5 s)"}
_api_last = [0.0]


def jget(url: str) -> dict:
    """维基 API：描述性 UA、≥1.5 s 间隔、429 / 5xx 按 Retry-After 退避（多会话同时访问时常被限流）。"""
    import urllib.error
    import urllib.request
    for attempt in range(8):
        wait = 1.5 - (time.monotonic() - _api_last[0])
        if wait > 0:
            time.sleep(wait)
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=API_UA), timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503, 504):
                raise
            ra = e.headers.get("Retry-After")
            time.sleep(int(ra) if ra and ra.isdigit() else 10 * (attempt + 1))
        finally:
            _api_last[0] = time.monotonic()
    raise RuntimeError(f"维基 API 重试 8 次仍失败：{url[:120]}")


# ── 第一步：内容 ─────────────────────────────────────────────────────────────
def qid_of(it: dict) -> str | None:
    if it.get("wikidata"):
        return it["wikidata"]
    for k in ("cross_check", "source"):
        m = re.search(r"wikidata\.org/wiki/(Q\d+)", str((it.get(k) or {}).get("url", "")))
        if m:
            return m.group(1)
    return None


def wiki_title(it: dict) -> tuple[str | None, str | None]:
    qid = qid_of(it)
    if qid:
        r = jget(f"{WD_API}?action=wbgetentities&ids={qid}&props=sitelinks|claims&sitefilter=enwiki&format=json")
        ent = r["entities"][qid]
        t = ent.get("sitelinks", {}).get("enwiki", {}).get("title")
        if t:
            return t, qid
    q = urllib.parse.quote(f"{it['name']} {it.get('subtitle') or ''} {it.get('country_name') or ''}")
    r = jget(f"{WIKI_API}?action=query&list=search&srsearch={q}&srlimit=1&format=json")
    hits = r.get("query", {}).get("search", [])
    return (hits[0]["title"] if hits else None), qid


def write_content(d: Path, it: dict, info: dict) -> None:
    (d / "content.json").write_text(json.dumps(info, ensure_ascii=False, indent=1), encoding="utf-8")
    # 给 Codex 读的精简版：卡片字段 + 简介 + 正文导言（外观、位置、历史）
    md = [f"# #{it['rank']} {it['name']}", "",
          f"- Card shows: {it['name']} — {it.get('subtitle') or ''}, {it.get('country_name') or ''}; {it.get('value_display') or ''}",
          f"- Wikipedia: {info['wiki_url'] or 'not found'} ({info['description']})",
          f"- Coordinates: {info['coords']}", f"- Identity reference photo (do not publish): {info['ref_image'] or 'none'}",
          f"- Notes from our data sheet: {it.get('notes') or ''}", "",
          "## Article text (lead section)", "", info["extract"][:6000]]
    (d / "content.md").write_text("\n".join(md), encoding="utf-8")


def cmd_content(ep: Path) -> None:
    """批量取：Wikidata 每次 50 个 QID、维基每次 20 个条目（导言、简介、坐标、首图链接），再逐张下首图做认主体参照。"""
    data, _ = load(ep)
    td = tiles_dir(ep)
    todo = [(i, it) for i, it in enumerate(data["items"]) if not (td / tile_key(i, it) / "content.json").exists()]
    qids = {i: qid_of(it) for i, it in todo}
    titles: dict[int, str | None] = {}
    ql = sorted({q for q in qids.values() if q})
    q2t = {}
    for k in range(0, len(ql), 50):
        r = jget(f"{WD_API}?action=wbgetentities&ids={'|'.join(ql[k:k + 50])}&props=sitelinks&sitefilter=enwiki&format=json")
        for q, ent in r.get("entities", {}).items():
            q2t[q] = ent.get("sitelinks", {}).get("enwiki", {}).get("title")
    for i, it in todo:
        titles[i] = q2t.get(qids[i]) if qids[i] else None
        if not titles[i]:
            q = urllib.parse.quote(f"{it['name']} {it.get('subtitle') or ''} {it.get('country_name') or ''}")
            hits = jget(f"{WIKI_API}?action=query&list=search&srsearch={q}&srlimit=1&format=json").get("query", {}).get("search", [])
            titles[i] = hits[0]["title"] if hits else None
    pages: dict[str, dict] = {}
    tl = sorted({t for t in titles.values() if t})
    for k in range(0, len(tl), 20):
        chunk = tl[k:k + 20]
        r = jget(f"{WIKI_API}?action=query&prop=extracts|description|coordinates|pageimages|info&inprop=url&exintro=1&explaintext=1"
                 f"&exlimit=max&piprop=thumbnail&pithumbsize=1600&pilimit=max&colimit=max&redirects=1&format=json"
                 f"&titles={urllib.parse.quote('|'.join(chunk))}")
        q = r.get("query", {})
        alias = {x["from"]: x["to"] for x in q.get("normalized", []) + q.get("redirects", [])}
        by_title = {pg.get("title"): pg for pg in q.get("pages", {}).values()}
        for t in chunk:
            tt = alias.get(alias.get(t, t), alias.get(t, t))
            pages[t] = by_title.get(tt, {})
    for i, it in todo:
        d = td / tile_key(i, it)
        d.mkdir(parents=True, exist_ok=True)
        page = pages.get(titles[i] or "", {})
        c = (page.get("coordinates") or [{}])[0]
        info = {"rank": it["rank"], "name": it["name"], "subtitle": it.get("subtitle"), "country": it.get("country_name"),
                "value": it.get("value_display"), "qid": qids[i], "wiki_title": page.get("title", titles[i]),
                "wiki_url": page.get("fullurl"), "description": page.get("description", ""),
                "coords": [c.get("lat"), c.get("lon")] if c else None, "extract": page.get("extract", "")[:9000],
                "ref_image": None, "ref_image_url": (page.get("thumbnail") or {}).get("source"), "retrieved_at": TODAY}
        if info["ref_image_url"]:
            try:
                (d / "ref.jpg").write_bytes(get(info["ref_image_url"]))
                info["ref_image"] = "ref.jpg"
            except Exception as e:  # noqa: BLE001
                info["ref_image_error"] = str(e)[:200]
        write_content(d, it, info)
        print(f"{d.name}: {info['wiki_title']} · ref {'有' if info['ref_image'] else '无'} · {len(info['extract'])} 字", flush=True)


# ── 第二步：Codex 研究 + 下载 ────────────────────────────────────────────────
SCHEMA = {"type": "object", "additionalProperties": False, "required": ["tiles"], "properties": {"tiles": {"type": "array", "items": {
    "type": "object", "additionalProperties": False, "required": ["key", "visual_brief", "downloaded", "notes"], "properties": {
        "key": {"type": "string"}, "visual_brief": {"type": "string"}, "notes": {"type": "string"},
        "downloaded": {"type": "array", "items": {"type": "object", "additionalProperties": False,
            "required": ["file", "image_url", "page_url", "source", "author", "licence", "width", "height", "subject_check", "why"],
            "properties": {"file": {"type": "string"}, "image_url": {"type": "string"}, "page_url": {"type": "string"},
                           "source": {"type": "string"}, "author": {"type": "string"}, "licence": {"type": "string"},
                           "width": {"type": "integer"}, "height": {"type": "integer"},
                           "subject_check": {"type": "string"}, "why": {"type": "string"}}}}}}}}}

PROMPT = """You are the photo researcher for a YouTube ranking video ("{title}"). Each ranked item gets a full-bleed {shape} poster card (about {card_w}x800 px on a 1080p screen), so each tile needs ONE excellent, unmistakable real photograph of its subject.

Work tile by tile. For each tile folder listed below (relative to the current directory):
1. CONTENT FIRST: read `<key>/content.md` (Wikipedia text: what the subject is, where, what it looks like) and look at `<key>/ref.jpg` if it exists (an identity reference only; never use or re-download it). Write a 2-4 sentence visual brief: the subject's distinctive shape/features, its setting, the classic recognisable viewpoint(s), and look-alikes it could be confused with (neighbouring towers / peaks, sister buildings).
2. RESEARCH with web search, guided by the brief: find the best real photographs (not AI images, not 3D renders, not illustrations, not maps) of exactly this subject. Wanted: {prefer}; strong colour and light (clear sky, golden hour, blue hour or night lights); sharp; the subject large and clearly identifiable; ideally long side >= 2400 px and at least 1600 px. No watermarks, no text overlays, no collages, no stock-agency previews (Getty, Shutterstock, Alamy, Dreamstime, Adobe Stock, 123rf, Depositphotos).
   Do NOT take images from Wikimedia Commons or Wikipedia (upload.wikimedia.org) - the Wikipedia text is only for content. Good places: Pexels, Unsplash, Pixabay, Flickr (original size), official building / developer / park / tourism-board media pages, photographers' sites, travel media.
3. DOWNLOAD: save 6 to 8 of the best distinct candidates into `<key>/cand/` as c1.jpg, c2.jpg, ... (use curl or python; follow redirects; send a browser User-Agent; for Unsplash use the raw/full URL, for Pexels the original, for Flickr the largest available size). After each download confirm the file really is an image (not HTML) and read its pixel size; delete failures and try another candidate. Keep going until at least 6 good files exist or you have genuinely exhausted the web.
4. VERIFY each kept file by looking at it: is it really this subject (compare with the brief and ref.jpg)? Write the verdict in subject_check ("match: ..." or "doubt: ..."). Delete files that show the wrong subject.
5. Report the licence EXACTLY as stated on the source page (e.g. "Pexels License", "Unsplash License", "CC BY 2.0", "All rights reserved"); "unknown" if not stated. Prefer freely licensed photos when quality is equal, but quality and correct subject come first.

Do not modify anything outside the listed tile folders. Return the JSON (one entry per tile, key copied exactly; downloaded = the files that remain in cand/).

Tiles:
{tiles}"""


def run_research(ep: Path, batch: list[tuple[int, dict]], meta: dict) -> str:
    td = tiles_dir(ep)
    keys = [tile_key(i, it) for i, it in batch]
    tag = "+".join(k[:2] for k in keys)
    out = td / f"_codex_{tag}.json"
    if out.exists():
        return f"{tag}: 已有"
    for k in keys:
        (td / k / "cand").mkdir(parents=True, exist_ok=True)
    tiles = "\n".join(f"- {k}  (#{it['rank']} {it['name']} — {it.get('subtitle') or ''}, {it.get('country_name') or ''})"
                      + (f"  note: {it['image_hint']}" if it.get("image_hint") else "")
                      + (f"  note: this summit is {it['badge'].lower()}; another tile shows the same peak for the other country, "
                         f"so prefer a view from the {it.get('country_name')} side and pick a clearly different photo"
                         if str(it.get("badge") or "").startswith("SHARED WITH") else "")
                      for k, (_, it) in zip(keys, batch))
    prompt = PROMPT.format(tiles=tiles, **meta)
    schema = td / "_schema.json"
    argv = [shutil.which("codex") or "codex", "--search", "exec", "--skip-git-repo-check", "--sandbox", "workspace-write",
            "-c", "sandbox_workspace_write.network_access=true", "-C", str(td),
            "--output-schema", str(schema), "-o", str(out), "-"]
    req = {"argv": argv, "prompt": prompt, "purpose": "主图研究与下载（第二步，follow-up 021；只下载真实照片，不生成）",
           "tiles": keys, "output": str(out), "cost": "ChatGPT 订阅额度，未知"}
    t0 = time.time()
    r = RequestLog(ep).invoke("codex_cli", "web_search_download", req, lambda: subprocess.run(
        argv, input=prompt, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=2400))
    if not out.exists():
        return f"{tag}: rc={r.returncode} 无输出 {r.stderr[-300:]}"
    res = json.loads(out.read_text(encoding="utf-8"))
    for row in res.get("tiles", []):
        if row["key"] in keys:
            (td / row["key"] / "candidates.json").write_text(json.dumps(row, ensure_ascii=False, indent=1), encoding="utf-8")
    n = {row["key"][:2]: len(row["downloaded"]) for row in res.get("tiles", [])}
    return f"{tag}: rc={r.returncode} {int(time.time() - t0)}s 候选 {n}"


def cmd_research(ep: Path, only: list[str], workers: int, size: int) -> None:
    data, _ = load(ep)
    td = tiles_dir(ep)
    (td / "_schema.json").write_text(json.dumps(SCHEMA), encoding="utf-8")
    tall = target_aspect(data) < 0.8
    meta = {"title": data.get("title", ""), "card_w": (data.get("layout") or {}).get("card_w", 600),
            "shape": "portrait 3:4" if tall else "near-square 9:10",
            "prefer": (data.get("layout") or {}).get("image_prefer") or (
                "the whole building visible from base to top, the classic recognisable angle, portrait orientation preferred" if tall else
                "the summit itself clearly visible and recognisable, the classic view of this mountain")}
    todo = [(i, it) for i, it in enumerate(data["items"])
            if (not only or tile_key(i, it)[:2] in only or str(i) in only) and not (td / tile_key(i, it) / "candidates.json").exists()]
    batches = [todo[k:k + size] for k in range(0, len(todo), size)]
    print(f"{len(todo)} 张卡，{len(batches)} 包", flush=True)
    with ThreadPoolExecutor(workers) as ex:
        for msg in ex.map(lambda b: run_research(ep, b, meta), batches):
            print(msg, flush=True)


def metrics(path: Path, target: float) -> dict:
    """与 image_reselect.metrics 同口径（色彩 / 对比 / 清晰度 / 裁成卡片后保留比例），numpy 实现；JPEG 用 draft 缩小解码。"""
    import numpy as np
    from PIL import ImageFilter
    Image.MAX_IMAGE_PIXELS = None
    with Image.open(path) as raw:
        rot = raw.getexif().get(274, 1) in (5, 6, 7, 8)      # EXIF 旋转 90° 时宽高互换
        rw, rh = (raw.size[1], raw.size[0]) if rot else raw.size
        raw.draft("RGB", (1600, 1600))
        im = ImageOps.exif_transpose(raw).convert("RGB")
    a = rw / rh
    keep = target / a if a > target else a / target
    im.thumbnail((800, 800))
    x = np.asarray(im, dtype=np.float32)
    r, g, b = x[..., 0], x[..., 1], x[..., 2]
    rg, yb = r - g, (r + g) / 2 - b
    colour = float(np.hypot(rg.std(), yb.std()) + 0.3 * np.hypot(rg.mean(), yb.mean()))
    lum = im.convert("L")
    contrast = float(np.asarray(lum, dtype=np.float32).std())
    sharp = float(np.asarray(lum.filter(ImageFilter.FIND_EDGES), dtype=np.float32).std())
    return {"w": rw, "h": rh, "keep": round(keep, 3), "colour": round(colour, 1), "contrast": round(contrast, 1), "sharp": round(sharp, 1)}


# ── 打分与拼图 ──────────────────────────────────────────────────────────────
def crop_h(w: int, h: int, target: float) -> int:
    return int(h if w / h >= target else w / target)


def cmd_score(ep: Path) -> None:
    data, _ = load(ep)
    target = target_aspect(data)
    td = tiles_dir(ep)
    picks, report = {}, []
    for i, it in enumerate(data["items"]):
        key = tile_key(i, it)
        d = td / key
        cj = d / "candidates.json"
        row = json.loads(cj.read_text(encoding="utf-8")) if cj.exists() else {"downloaded": []}
        if isinstance(row, list):                      # 个别研究员直接写了候选列表
            row = {"downloaded": row}
        cands = []
        for c in row["downloaded"]:
            f = d / c["file"] if (d / c["file"]).exists() else d / "cand" / Path(c["file"]).name
            if not f.exists():
                continue
            try:
                m = metrics(f, target)
            except Exception:  # noqa: BLE001
                continue
            ch = crop_h(m["w"], m["h"], target)
            ok_res = ch >= MIN_CROP_H
            doubt = not c["subject_check"].lower().startswith("match")
            score = (min(1.0, ch / 1600) * 35 + min(1.0, m["keep"] / 0.75) * 15 + min(1.0, m["colour"] / 60) * 20
                     + min(1.0, m["contrast"] / 60) * 10 + min(1.0, m["sharp"] / 30) * 10 + (20 if _licence_ok(c["licence"]) else 0))  # 质量接近时优先可商用（默认版不必扣图）
            if doubt:
                score -= 40
            cands.append({**c, "path": f.relative_to(d).as_posix(), **m, "crop_h": ch, "res_ok": ok_res, "doubt": doubt,
                          "licence_ok": _licence_ok(c["licence"]), "score": round(score, 1)})
        cands.sort(key=lambda c: (not c["res_ok"], c["doubt"], -c["score"]))
        (d / "scored.json").write_text(json.dumps(cands, ensure_ascii=False, indent=1), encoding="utf-8")
        best = cands[0] if cands and cands[0]["res_ok"] and not cands[0]["doubt"] else None
        picks[key] = best["path"] if best else None
        report.append((it["rank"], it["name"], len(cands), sum(c["res_ok"] and not c["doubt"] for c in cands),
                       best["licence"] if best else "—"))
    (td / "picks.json").write_text(json.dumps(picks, ensure_ascii=False, indent=1), encoding="utf-8")
    sheets(ep, data, target)
    for r in report:
        print(f"#{r[0]:>2} {r[1][:30]:30} 候选 {r[2]} 合格 {r[3]}  选中许可 {r[4]}")
    print("无合格候选：", [k for k, v in picks.items() if not v])


def sheets(ep: Path, data: dict, target: float, per: int = 8) -> None:
    """每行一张卡：维基参照 | 选中 | 其余候选（最多 5）。绿框 = 选中，红字 = 分辨率不够或主体存疑。"""
    td = tiles_dir(ep)
    picks = json.loads((td / "picks.json").read_text(encoding="utf-8"))
    TW = 170
    TH = int(TW / target)
    f = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 17)
    fs = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 12)
    items = list(enumerate(data["items"]))
    for page in range(0, len(items), per):
        rows = items[page:page + per]
        sheet = Image.new("RGB", (200 + 7 * (TW + 6), len(rows) * (TH + 34) + 10), (22, 22, 26))
        dr = ImageDraw.Draw(sheet)
        for r, (i, it) in enumerate(rows):
            key = tile_key(i, it)
            d = td / key
            sc = json.loads((d / "scored.json").read_text(encoding="utf-8")) if (d / "scored.json").exists() else []
            y = 10 + r * (TH + 34)
            dr.text((6, y), f"#{it['rank']} {it['name'][:18]}", font=f, fill=(240, 240, 240))
            dr.text((6, y + 24), f"idx {i} · {it.get('country_name','')[:16]}", font=fs, fill=(170, 170, 170))
            chosen = next((c for c in sc if c["path"] == picks.get(key)), None)
            slots = [("ref", {"path": "ref.jpg"} if (d / "ref.jpg").exists() else None)] + \
                    [("选中", chosen)] + [(Path(c["path"]).stem, c) for c in sc if c is not chosen][:5]
            for s, (lab, c) in enumerate(slots):
                x = 200 + s * (TW + 6)
                col = (40, 170, 80) if lab == "选中" else (90, 90, 100)
                dr.rectangle([x, y, x + TW - 1, y + TH - 1], fill=col)
                if c:
                    try:
                        with Image.open(d / c["path"]) as im:
                            sheet.paste(ImageOps.fit(ImageOps.exif_transpose(im).convert("RGB"), (TW - 6, TH - 6)), (x + 3, y + 3))
                    except Exception:  # noqa: BLE001
                        pass
                    if lab != "ref":
                        bad = (not c.get("res_ok")) or c.get("doubt")
                        lic = "绿" if c.get("licence_ok") else "红"
                        dr.text((x + 2, y + TH + 2), f"{lab} {c.get('score','')} h{c.get('crop_h','')} {lic}", font=fs,
                                fill=(235, 80, 70) if bad else (220, 220, 220))
                    else:
                        dr.text((x + 2, y + TH + 2), "维基参照（不用）", font=fs, fill=(170, 170, 170))
                else:
                    dr.text((x + 6, y + 6), f"{lab}：无", font=fs, fill=(230, 230, 230))
        sheet.save(td / f"_sheet_{page // per + 1:02d}.jpg", quality=86)


# ── 出图兜底 ────────────────────────────────────────────────────────────────
def cmd_generate(ep: Path, only: list[str]) -> None:
    data, _ = load(ep)
    td = tiles_dir(ep)
    tall = target_aspect(data) < 0.8
    for i, it in enumerate(data["items"]):
        key = tile_key(i, it)
        if key[:2] not in only and str(i) not in only:
            continue
        d = td / key
        info = json.loads((d / "content.json").read_text(encoding="utf-8"))
        cj = d / "candidates.json"
        brief = json.loads(cj.read_text(encoding="utf-8")).get("visual_brief", "") if cj.exists() else ""
        prompt = (f"Photorealistic travel photograph of {it['name']} ({info.get('description') or ''}), "
                  f"{it.get('subtitle') or ''}, {it.get('country_name') or ''}. {brief} "
                  f"{'Vertical 3:4 composition, the whole subject from base to top' if tall else 'Near-square composition, the subject large and centred'}, "
                  "golden-hour light, clear sky, crisp detail, natural colours, no people in focus, no text, no watermark, no logos. "
                  "The attached reference photo shows what the real subject looks like; match its shape and proportions faithfully.")
        custom = d / "gen_prompt_custom.txt"   # 非地标题材（如 ep21 大米）由主会话写专用 prompt，优先于上面的旅行照模板（follow-up 057）
        if custom.exists():
            prompt = custom.read_text(encoding="utf-8").strip()
        pf = d / "gen_prompt.txt"
        pf.write_text(prompt, encoding="utf-8")
        out = d / "cand" / "ai1.png"
        argv = [sys.executable, str(REPO / "tools" / "codex_image.py"), "--out", str(out.relative_to(REPO)).replace("\\", "/"),
                "--prompt-file", str(pf)]
        if (d / "ref.jpg").exists():
            argv += ["--ref", str(d / "ref.jpg")]
        print(key, "出图中…", flush=True)
        r = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=REPO)
        print(key, r.returncode, (r.stdout or r.stderr)[-300:], flush=True)
        if out.exists():
            row = json.loads(cj.read_text(encoding="utf-8")) if cj.exists() else {"key": key, "visual_brief": brief, "notes": "", "downloaded": []}
            with Image.open(out) as im:
                w, h = im.size
            row["downloaded"] = [x for x in row["downloaded"] if x["file"] != "cand/ai1.png"] + [{
                "file": "cand/ai1.png", "image_url": "", "page_url": "", "source": "AI illustration (Codex image_gen)",
                "author": "AI illustration", "licence": "AI-generated", "width": w, "height": h,
                "subject_check": "match: generated from the Wikipedia content and reference shape; check by eye", "why": "no adequate real photo"}]
            cj.write_text(json.dumps(row, ensure_ascii=False, indent=1), encoding="utf-8")


# ── 应用 ────────────────────────────────────────────────────────────────────
def cmd_apply(ep: Path, overrides: dict[int, str]) -> None:
    data, assets = load(ep)
    td = tiles_dir(ep)
    picks = json.loads((td / "picks.json").read_text(encoding="utf-8"))
    by_file = {a["file"]: a for a in assets}
    old_dir = ep / "_build" / "old_img"
    old_dir.mkdir(parents=True, exist_ok=True)
    changed, missing = 0, []
    for i, it in enumerate(data["items"]):
        key = tile_key(i, it)
        choice = overrides.get(i, picks.get(key))
        if choice == "keep":
            continue
        if not choice:
            missing.append(key)
            continue
        d = td / key
        c = next(x for x in json.loads((d / "scored.json").read_text(encoding="utf-8")) if x["path"].replace("\\", "/") == choice.replace("\\", "/"))
        rel = f"assets/img/{key}.jpg"
        dst = ep / rel
        prev = it.get("image")
        if prev and (ep / prev).exists() and prev != rel:
            shutil.move(str(ep / prev), old_dir / Path(prev).name)
        with Image.open(d / c["path"]) as im:
            im = ImageOps.exif_transpose(im).convert("RGB")
            if max(im.size) > LONG_SIDE:
                im.thumbnail((LONG_SIDE, LONG_SIDE), Image.LANCZOS)
            dst.parent.mkdir(parents=True, exist_ok=True)
            im.save(dst, quality=92)
            size = im.size
        lic = c["licence"].strip()
        ai = lic.lower().startswith("ai-generated")   # 含「AI-generated (Codex image_gen)」写法（follow-up 057）
        old = by_file.get(prev or "", {})
        entry = {"file": rel, "source_page": c.get("page_url", ""), "source_url": c.get("image_url", ""), "author": c.get("author", ""),
                 "licence": lic, "licence_url": licence_url(lic), "attribution_required": not ai and not re.match(r"(public domain|pd|cc0|pexels|unsplash|pixabay)", lic, re.I),
                 "modified": f"downscaled to {size[0]}x{size[1]} px and re-encoded as JPEG; renderer will crop",
                 "sha256": hashlib.sha256(dst.read_bytes()).hexdigest(), "retrieved_at": TODAY,
                 "fop_note": old.get("fop_note", ""), "subject_check": c.get("subject_check", ""),
                 "selected_by": "follow-up 021/027/033 两步走：内容 → Claude 研究下载（Codex 仅出图）→ 打分 + 人工拼图"}
        if prev in by_file and prev != rel:
            assets.remove(by_file[prev])
        assets = [a for a in assets if a["file"] != rel] + [entry]
        it["image"] = rel
        it["image_credit"] = "Illustration: AI-generated, not a photo" if ai else f"{c.get('author') or 'Unknown'} / {lic}"
        it.pop("image_focus", None)
        # 许可类风险每次按当前所选图重算；其他风险（如全景自由 FoP）原样保留
        risks = [r for r in str(it.get("image_risk") or "").split("; ") if r and not r.startswith(LICENCE_RISKS)]
        lic_risk = None if ai or _licence_ok(lic) else licence_risk(lic)
        if lic_risk:
            risks.append(lic_risk)
        if risks:
            it["image_risk"] = "; ".join(risks)
            it["image_note"] = "Photo withheld: licence unclear" if risks == [lic_risk] else "Photo withheld: architecture copyright"
        else:
            it.pop("image_risk", None)
            it.pop("image_note", None)
        changed += 1
    (ep / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ep / "assets.json").write_text(json.dumps(assets, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"已换 {changed} 张；无图 {missing}；旧图在 {old_dir}")


LICENCE_RISKS = ("licence unknown", "licence is non-commercial", "all rights reserved", "licence not stated")


def licence_risk(lic: str) -> str:
    """不可直接商用的许可 → 照实写进 image_risk（进签字机制，follow-up 009 / 033）。"""
    low = lic.lower()
    if re.search(r"\bnc\b|noncommercial|non-commercial", low.replace("-", " ")):
        return f"licence is non-commercial ({lic[:40]})"
    if "all rights reserved" in low or low.startswith("©"):
        return "all rights reserved (needs permission)"
    return "licence not stated on source page"


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=("content", "research", "score", "generate", "apply"))
    ap.add_argument("ep")
    ap.add_argument("--only", nargs="*", default=[], help="卡片序号（两位 idx，如 00 13）")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--batch", type=int, default=2)
    ap.add_argument("--override", nargs="*", default=[], help="idx=候选相对路径（cand/c3.jpg）或 keep")
    a = ap.parse_args()
    ep = Path(a.ep).resolve()
    {"content": lambda: cmd_content(ep),
     "research": lambda: cmd_research(ep, a.only, a.workers, a.batch),
     "score": lambda: cmd_score(ep),
     "generate": lambda: cmd_generate(ep, a.only),
     "apply": lambda: cmd_apply(ep, {int(k): v for k, v in (o.split("=", 1) for o in a.override)})}[a.step]()


if __name__ == "__main__":
    main()
