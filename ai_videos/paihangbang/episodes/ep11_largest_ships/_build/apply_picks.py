# -*- coding: utf-8 -*-
"""按人工挑选结果（picks_manual.json）写图：主图 + 可选可商用替代图（image_alt）。

picks_manual.json：{"<idx>": {"cand": "c3", "alt": "c1"(可选), "focus": [x, y](可选), "alt_focus": [x, y](可选), "note": "..."}}
- 主图许可可商用 → image，清掉 image_risk / image_alt。
- 主图许可不明 → image + image_risk="licence unknown"（进 _with-risk-images 版）；alt 给默认版（image_alt / image_alt_credit）。
- 每张图写 assets.json（来源页、原图链接、作者、许可、修改说明、sha256）。
"""
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

from PIL import Image, ImageOps

EP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EP.parents[1] / "_tools"))
sys.path.insert(0, str(EP.parents[3] / "projects" / "rank_scroll"))
from image_reselect import item_key, licence_url  # noqa: E402
from rank_scroll.contract import _licence_ok  # noqa: E402

LONG = 2400


def save(src: Path, dst: Path, precrop=None):
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        if precrop:                                   # 预裁切（只裁不改，[x0, y0, x1, y1] 比例）：把船移到卡片文字区之上（QC 2026-11-04）
            w, h = im.size
            im = im.crop((int(precrop[0] * w), int(precrop[1] * h), int(precrop[2] * w), int(precrop[3] * h)))
        if max(im.size) > LONG:
            im.thumbnail((LONG, LONG), Image.LANCZOS)
        dst.parent.mkdir(parents=True, exist_ok=True)
        im.save(dst, quality=90)
        return im.size


def entry(rel, m, size, note):
    lic = (m.get("licence") or "unknown").strip()
    return {"file": rel, "source_page": m.get("page_url", ""), "source_url": m.get("image_url", ""), "author": m.get("author", "") or "unknown",
            "licence": lic, "licence_url": licence_url(lic), "attribution_required": not re.match(r"(public domain|pd|cc0|pexels|unsplash|pixabay)", lic, re.I),
            "modified": f"cropped and downscaled to {size[0]}x{size[1]} px, re-encoded as JPEG; renderer crops to the card", "sha256": hashlib.sha256((EP / rel).read_bytes()).hexdigest(),
            "retrieved_at": date.today().isoformat(), "fop_note": "", "subject_note": note,
            "selected_by": f"Claude 人工逐张看图挑选（{m.get('source','')}）"}


def credit(m):
    return f"{m.get('author') or 'Unknown'} / {(m.get('licence') or 'unknown').strip()}"


def main():
    data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    assets = json.loads((EP / "assets.json").read_text(encoding="utf-8"))
    picks = json.loads((EP / "_build" / "picks_by_key.json").read_text(encoding="utf-8"))   # 按船级 key（名次会变）
    by_file = {a["file"]: a for a in assets}
    for it in data["items"]:
        p = picks.get(it["key"])
        if not p:
            continue
        stem = f"{it['rank']:02d}_{it['key']}"
        if p.get("gen"):                                   # Codex 生成图（最后手段，follow-up 用户追加要求 4/5）
            rel = p["gen"]
            with Image.open(EP / rel) as im:
                size = im.size
            by_file[rel] = {"file": rel, "source_page": "", "source_url": "", "author": "AI-generated", "licence": "AI-generated (Codex image_gen)",
                            "licence_url": "", "attribution_required": False, "modified": "none (generated); renderer crops to the card",
                            "sha256": hashlib.sha256((EP / rel).read_bytes()).hexdigest(), "retrieved_at": date.today().isoformat(), "fop_note": "",
                            "subject_note": p.get("note", ""), "selected_by": "tools/codex_image.py（全网无合格真实照片时的最后手段；上传时勾选合成内容声明）",
                            "prompt_file": p.get("prompt_file", "")}
            it["image"], it["image_credit"] = rel, "AI-generated illustration"
            for k in ("image_risk", "image_note", "image_alt", "image_alt_credit", "image_focus"):
                it.pop(k, None)
            if p.get("focus"):
                it["image_focus"] = p["focus"]
            continue
        d = EP / "_build" / "reselect" / "cand" / p.get("cand_dir", "")
        meta = {m["id"]: m for m in json.loads((d / "meta.json").read_text(encoding="utf-8"))} if (d / "meta.json").exists() else {}
        for extra in ("src", "alt_src"):                     # 第三轮补图：直接给出本地文件与来源元数据（_build/r3/）
            if p.get(extra):
                m = dict(p[extra]); m["file"] = str((EP / "_build" / m["file"]).resolve()); m["id"] = extra
                meta[extra] = m
                p["cand" if extra == "src" else "alt"] = extra
        m = dict(meta[p["cand"]])
        if p.get("author_fix"):
            m["author"] = p["author_fix"]
        rel = f"assets/img/{stem}.jpg"
        size = save(Path(m["file"]) if Path(m["file"]).is_absolute() else d / m["file"], EP / rel, p.get("precrop"))
        by_file[rel] = entry(rel, m, size, p.get("note", ""))
        it["image"], it["image_credit"] = rel, credit(m)
        for k in ("image_risk", "image_note", "image_alt", "image_alt_credit", "image_focus"):
            it.pop(k, None)
        if p.get("focus"):
            it["image_focus"] = p["focus"]
        if not _licence_ok(m.get("licence", "")):
            it["image_risk"] = "licence unknown"
            it["image_note"] = "Photo withheld: licence unclear"
            if p.get("gen_alt"):                         # 无可商用替代 → Codex 生成写实插图作默认版替代（主代理决定，2026-11-04）
                arel = p["gen_alt"]
                with Image.open(EP / arel) as im:
                    gsize = im.size
                by_file[arel] = {"file": arel, "source_page": "", "source_url": "", "author": "AI-generated", "licence": "AI-generated (Codex image_gen)",
                                 "licence_url": "", "attribution_required": False, "modified": "none (generated); renderer crops to the card",
                                 "sha256": hashlib.sha256((EP / arel).read_bytes()).hexdigest(), "retrieved_at": date.today().isoformat(), "fop_note": "",
                                 "subject_note": p.get("alt_note", ""), "selected_by": "tools/codex_image.py（无可商用真实照片时的默认版替代；上传时勾选合成内容声明）",
                                 "prompt_file": p.get("alt_prompt_file", "")}
                it["image_alt"], it["image_alt_credit"] = arel, "AI-generated illustration"
            elif p.get("alt"):
                a = meta[p["alt"]]
                arel = f"assets/img/{stem}_alt.jpg"
                asz = save(Path(a["file"]) if Path(a["file"]).is_absolute() else d / a["file"], EP / arel, p.get("alt_precrop"))
                by_file[arel] = entry(arel, a, asz, p.get("alt_note", p.get("note", "")))
                it["image_alt"], it["image_alt_credit"] = arel, credit(a)
                if p.get("alt_focus"):
                    it["image_alt_focus"] = p["alt_focus"]
    (EP / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    used = set()
    for it in data["items"]:
        used.update(x for x in (it.get("image"), it.get("image_alt")) if x)
    assets = [a for f, a in sorted(by_file.items()) if f in used]
    (EP / "assets.json").write_text(json.dumps(assets, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"applied {len(picks)} picks; assets {len(assets)}")


if __name__ == "__main__":
    main()
