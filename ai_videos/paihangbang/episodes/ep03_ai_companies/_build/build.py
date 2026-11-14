# -*- coding: utf-8 -*-
"""ep03 组装：items_def.json（代理按调研定稿的屏上字段）+ selection.json（选中的参考图）→ data.json / assets.json / assets/{img,logo,person}。

    python ai_videos/paihangbang/episodes/ep03_ai_companies/_build/build.py

- 顺序：按 founded（YYYY-MM）从老到新，rank = 出场位置（列表模式，屏上不显示名次）。
- 图片：照片长边缩到 ≤ 2400、头像 ≤ 1000，转 JPEG；logo 一律转 PNG（SVG 用 skia 栅格化），裁掉透明 / 纯白边。
- 许可：照片、头像的许可不在可商用白名单里就标 image_risk = "licence unknown"（默认母版扣下，签字版放进去，follow-up 009）；
  logo 记 kind = "logo"，许可写商标、仅作指认（bible §4）。
"""
from __future__ import annotations

import hashlib
import io
import json
import sys
from datetime import date
from pathlib import Path

from PIL import Image, ImageChops, ImageOps

EP = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "projects" / "rank_scroll"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from rank_scroll.contract import _licence_ok  # noqa: E402

BUILD = EP / "_build"
REF = EP / "assets" / "ref"
TODAY = date.today().isoformat()
import re  # noqa: E402
THUMB = {"openai", "anthropic", "deepseek"}   # cover draft: three widely recognised names
AGENCY = re.compile(r"getty|reuters|associated press|AP|afp|shutterstock|alamy", re.I)
LICENCE_URLS = {"cc by 2.0": "https://creativecommons.org/licenses/by/2.0/", "cc by 3.0": "https://creativecommons.org/licenses/by/3.0/",
                "cc by 4.0": "https://creativecommons.org/licenses/by/4.0/", "cc by-sa 2.0": "https://creativecommons.org/licenses/by-sa/2.0/",
                "cc by-sa 3.0": "https://creativecommons.org/licenses/by-sa/3.0/", "cc by-sa 4.0": "https://creativecommons.org/licenses/by-sa/4.0/",
                "cc0": "https://creativecommons.org/publicdomain/zero/1.0/", "pexels license": "https://www.pexels.com/license/",
                "unsplash license": "https://unsplash.com/license", "pixabay content license": "https://pixabay.com/service/license-summary/"}


def prompt_of(gen: str) -> str:
    """assets/gen/x_v1.png → assets/gen/x_prompt.txt; x_v2.png → x_prompt_v2.txt."""
    base, ver = gen[:-4].rsplit("_v", 1)
    return f"{base}_prompt.txt" if ver == "1" else f"{base}_prompt_v{ver}.txt"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def cand(slug: str, kind: str, cid: str) -> tuple[Path, dict]:
    d = REF / slug / kind
    meta = {m["id"]: m for m in json.loads((d / "meta.json").read_text(encoding="utf-8"))}
    m = meta[cid]
    return d / m["file"], m


def raster_svg(path: Path, height: int = 480) -> Image.Image:
    from svgfix import load_svg
    im = load_svg(path, height)
    if im is None:
        raise ValueError(f"cannot parse SVG {path}")
    return im


def trim(im: Image.Image) -> Image.Image:
    im = im.convert("RGBA")
    alpha_box = im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    if alpha_box and alpha_box != (0, 0, *im.size):
        im = im.crop(alpha_box)
    rgb = Image.new("RGB", im.size, (255, 255, 255))
    rgb.paste(im, mask=im.getchannel("A"))
    diff = ImageChops.difference(rgb, Image.new("RGB", im.size, (255, 255, 255))).convert("L").point(lambda v: 255 if v > 12 else 0)
    box = diff.getbbox()
    return im.crop(box) if box else im


def trim_corner(im: Image.Image, pad: int = 12) -> Image.Image:
    """Logos drawn on their own solid plate (e.g. Cursor's dark rectangle): trim everything matching the corner colour."""
    rgb = im.convert("RGB")
    bg = Image.new("RGB", rgb.size, rgb.getpixel((2, 2)))
    box = ImageChops.difference(rgb, bg).convert("L").point(lambda v: 255 if v > 24 else 0).getbbox()
    if not box:
        return im
    x0, y0, x1, y1 = box
    return im.crop((max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad)))


def prep_logo(src: Path, dst: Path, corner_trim: bool = False) -> tuple[int, int]:
    im = raster_svg(src) if src.suffix == ".svg" else ImageOps.exif_transpose(Image.open(src)).convert("RGBA")
    im = trim(im)
    if corner_trim:
        im = trim_corner(im)
    if im.height > 600:
        im = im.resize((int(im.width * 600 / im.height), 600), Image.LANCZOS)
    dst.parent.mkdir(parents=True, exist_ok=True)
    im.save(dst)
    return im.size


def prep_jpeg(src: Path, dst: Path, long_side: int, box: list | None = None) -> tuple[int, int]:
    """box = [x0, y0, x1, y1] fractions: crop before resizing (headshots where the face is small in frame)."""
    if src.suffix == ".svg":
        raise ValueError(f"{src} is SVG, not a photo")
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    if box:
        w, h = im.size
        im = im.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)))
    if max(im.size) > long_side:
        im.thumbnail((long_side, long_side), Image.LANCZOS)
    dst.parent.mkdir(parents=True, exist_ok=True)
    im.save(dst, quality=92)
    return im.size


def ledger_entry(file: str, m: dict, kind: str, size: tuple[int, int], company: str) -> dict:
    lic = (m.get("licence") or "unknown").strip()
    e = {"file": file, "kind": kind, "source_page": m.get("page_url", ""), "source_url": m.get("image_url", ""),
         "source_site": m.get("source", ""), "author": m.get("author", ""), "retrieved_at": TODAY, "selected_by": "代理看候选拼图（Codex 联网搜，follow-up 010）"}
    if kind == "logo":
        e.update(licence=f"Trademark of {company}; identification only (source terms: {lic})", attribution_required=False,
                 modified=f"converted to PNG, margins trimmed, {size[0]}x{size[1]} px; colours and shape unchanged")
    else:
        e.update(licence=lic, licence_url=LICENCE_URLS.get(lic.lower(), ""), attribution_required=lic.lower().startswith("cc by"),
                 modified=f"downscaled to {size[0]}x{size[1]} px and re-encoded as JPEG; renderer will crop")
    return e


def main() -> None:
    items_def = json.loads((BUILD / "items_def.json").read_text(encoding="utf-8"))
    sel = json.loads((BUILD / "selection.json").read_text(encoding="utf-8"))
    head = items_def["episode"]
    rows = sorted(items_def["items"], key=lambda r: (r["founded"], r["name"]))
    items, ledger = [], []
    for pos, r in enumerate(rows, 1):
        slug, s = r["slug"], sel.get(r["slug"], {})
        it = {k: v for k, v in r.items() if k not in ("slug", "founded", "person")}
        it["rank"] = pos
        it = {"rank": pos, **{k: v for k, v in it.items() if k != "rank"}}
        if s.get("photo_gen"):                        # own Codex image_gen illustration (follow-up 017): no real person, no logo
            src = EP / s["photo_gen"]
            rel = f"assets/img/{pos:02d}_{slug}.jpg"
            size = prep_jpeg(src, EP / rel, 2400)
            ledger.append({"file": rel, "kind": "photo", "source_page": "", "source_url": "", "source_site": "Codex image_gen",
                           "author": "AI-generated illustration (Codex image_gen)", "prompt_file": prompt_of(s["photo_gen"]),
                           "licence": "AI-generated", "attribution_required": False, "retrieved_at": TODAY,
                           "modified": f"re-encoded as JPEG {size[0]}x{size[1]}", "synthetic": True,
                           "selected_by": "代理：真实照片无合格候选，按 follow-up 017 生成", "sha256": sha(EP / rel)})
            it["image"] = rel
            it["image_credit"] = "Illustration: AI-generated, not a photo"
            if s.get("photo_focus"):
                it["image_focus"] = s["photo_focus"]
        elif s.get("photo"):
            src, m = cand(slug, "photo", s["photo"])
            rel = f"assets/img/{pos:02d}_{slug}.jpg"
            size = prep_jpeg(src, EP / rel, 2400, s.get("photo_box"))
            ledger.append({**ledger_entry(rel, m, "photo", size, r["name"]), "sha256": sha(EP / rel)})
            it["image"] = rel
            lic = m.get("licence", "unknown")
            it["image_credit"] = f"{m.get('author') or m.get('source')} / {lic}"[:80]
            if not _licence_ok(lic):
                it["image_risk"] = "licence unknown"
            if AGENCY.search(it["image_credit"] + " " + (m.get("source") or "")):
                it["image_risk"] = "news-agency photo (Getty/Reuters/AP): highest takedown risk"
            if s.get("photo_focus"):
                it["image_focus"] = s["photo_focus"]
            if it.get("image_risk"):
                it["image_note"] = "Photo withheld: licence not cleared"
                if s.get("photo_alt_gen"):            # no free real photo after Claude's searches → Codex illustration (follow-up 032)
                    rel_a = f"assets/img/{pos:02d}_{slug}_alt.jpg"
                    size = prep_jpeg(EP / s["photo_alt_gen"], EP / rel_a, 2400)
                    ledger.append({"file": rel_a, "kind": "photo", "source_page": "", "source_url": "", "source_site": "Codex image_gen",
                                   "author": "AI-generated illustration (Codex image_gen)", "prompt_file": prompt_of(s["photo_alt_gen"]),
                                   "licence": "AI-generated", "attribution_required": False, "retrieved_at": TODAY,
                                   "modified": f"re-encoded as JPEG {size[0]}x{size[1]}", "synthetic": True,
                                   "selected_by": "Claude 多轮搜索无可商用实拍（follow-up 020 / 032），默认母版用 Codex 生成插图", "sha256": sha(EP / rel_a)})
                    it["image_alt"] = rel_a
                    it["image_alt_credit"] = "Illustration: AI-generated, not a photo"
                elif s.get("photo_alt"):              # v1.4 image_alt (follow-up 020): free-licensed stand-in for the default master
                    src, m = cand(slug, "photo", s["photo_alt"])
                    lic_a = m.get("licence", "unknown")
                    if not _licence_ok(lic_a):
                        raise SystemExit(f"{slug}: photo_alt {s['photo_alt']} licence {lic_a!r} is not commercially usable")
                    rel_a = f"assets/img/{pos:02d}_{slug}_alt.jpg"
                    size = prep_jpeg(src, EP / rel_a, 2400, s.get("photo_alt_box"))
                    ledger.append({**ledger_entry(rel_a, m, "photo", size, r["name"]), "sha256": sha(EP / rel_a)})
                    it["image_alt"] = rel_a
                    it["image_alt_credit"] = f"{m.get('author') or m.get('source')} / {lic_a}"[:80]
        else:
            it["image_note"] = s.get("photo_note", "No usable photo found")
        if r["slug"] in THUMB:
            it["thumb"] = True
        if s.get("logo"):
            src, m = cand(slug, "logo", s["logo"])
            rel = f"assets/logo/{slug}.png"
            size = prep_logo(src, EP / rel, bool(s.get("logo_corner_trim")))
            ledger.append({**ledger_entry(rel, m, "logo", size, r["name"]), "sha256": sha(EP / rel)})
            it["logo"] = rel
            if s.get("logo_bg"):
                it["logo_bg"] = s["logo_bg"]
        person = dict(r["person"])
        if s.get("person"):
            src, m = cand(slug, s.get("person_kind", "person"), s["person"])   # a face can be cropped from a CC stage photo
            rel = f"assets/person/{slug}.jpg"
            size = prep_jpeg(src, EP / rel, 1000, s.get("person_box"))
            ledger.append({**ledger_entry(rel, m, "person", size, r["name"]), "sha256": sha(EP / rel)})
            lic = m.get("licence", "unknown")
            person.update(image=rel, credit=f"{m.get('author') or m.get('source')} / {lic}"[:110])
            if not _licence_ok(lic):
                person["image_risk"] = "licence unknown"
            if s.get("person_focus"):
                person["focus"] = s["person_focus"]
        it["person"] = person
        items.append(it)
    pos_of = {r["slug"]: n for n, r in enumerate(rows, 1)}           # insights are keyed by slug, positions follow the sort
    insights = [{"after_rank": pos_of[x["after_slug"]], "text": x["text"]} for x in items_def.get("insights", [])]
    data = {**head, "items": items, "insights": sorted(insights, key=lambda x: x["after_rank"])}
    (EP / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    (EP / "assets.json").write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")
    risk = sum(1 for i in items if i.get("image_risk")) + sum(1 for i in items if i["person"].get("image_risk"))
    print(f"data.json: {len(items)} items; assets.json: {len(ledger)} entries; risk-flagged images: {risk}")


if __name__ == "__main__":
    main()
