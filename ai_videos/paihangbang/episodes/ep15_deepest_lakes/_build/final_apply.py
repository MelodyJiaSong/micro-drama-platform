# -*- coding: utf-8 -*-
"""逐张看拼图后的最终选图（follow-up 016/023 + 契约 v1.4 image_alt）。
CHOICES[idx] = (主图候选 id, 默认版替代候选 id 或 None, 裁切焦点 [x, y] 或 None)
- 主图许可可商用 → 直接作 image（alt 忽略）。
- 主图许可不明 → image 标 image_risk="licence unknown"（只进 _with-risk-images 版），alt 若有则作 image_alt（默认版用）。
重写 data.json 图片字段与 assets.json（全量重建）。"""
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

from PIL import Image, ImageOps

sys.stdout.reconfigure(encoding="utf-8")
EP = Path(__file__).resolve().parents[1]
REPO = EP.parents[3]
sys.path.insert(0, str(REPO / "projects" / "rank_scroll"))
from rank_scroll.contract import _licence_ok  # noqa: E402

CAND = EP / "_build" / "reselect" / "cand"
LONG = 2400
TODAY = date.today().isoformat()

CHOICES: dict[int, tuple] = json.loads((EP / "_build" / "choices.json").read_text(encoding="utf-8"))


def licence_url(lic: str) -> str:
    low = lic.lower()
    if "pexels" in low: return "https://www.pexels.com/license/"
    if "unsplash" in low: return "https://unsplash.com/license"
    if "pixabay" in low: return "https://pixabay.com/service/license-summary/"
    if "cc0" in low: return "https://creativecommons.org/publicdomain/zero/1.0/"
    if "public domain" in low: return "https://creativecommons.org/publicdomain/mark/1.0/"
    m = re.search(r"cc[ -]by(-sa)?\s*([\d.]+)?", low)
    if m:
        return f"https://creativecommons.org/licenses/{'by-sa' if m.group(1) else 'by'}/{m.group(2) or '4.0'}/"
    return ""


def put_gen(src_rel: str, rel: str):
    """Codex 生成图（follow-up 016/020）：转 JPEG 落到 rel，账本记 AI-generated。"""
    src = EP / src_rel
    dst = EP / rel
    with Image.open(src) as im:
        im = im.convert("RGB")
        dst.parent.mkdir(parents=True, exist_ok=True)
        im.save(dst, quality=92)
        size = im.size
    prompt = (EP / "_build" / "gen").glob(Path(src_rel).stem.replace("_gen_alt", "_alt").replace("_gen", "") + "*.txt")
    pf = next(prompt, None)
    entry = {"file": rel, "source_page": "", "source_url": "generated for this video (Codex image_gen)", "generated_file": src_rel, "author": "AI-generated", "licence": "AI-generated (Codex image_gen)",
             "licence_url": "", "attribution_required": False,
             "modified": f"generated {size[0]}x{size[1]} PNG via tools/codex_image.py, re-encoded as JPEG; renderer will crop",
             "sha256": hashlib.sha256(dst.read_bytes()).hexdigest(), "retrieved_at": TODAY, "fop_note": "",
             "selected_by": "follow-up 016/023 最后手段：全网无合格可商用图，Codex 生成（request_log 由脚本自动记）",
             "prompt_file": f"_build/gen/{pf.name}" if pf else "", "synthetic": True}
    return entry, "AI-generated image (not a photo)", True


def put(key: str, cid: str, rel: str) -> tuple[dict, str]:
    if cid.startswith("gen:"):
        return put_gen(cid[4:], rel)
    meta = json.loads((CAND / key / "meta.json").read_text(encoding="utf-8"))
    m = next(x for x in meta if x["id"] == cid)
    dst = EP / rel
    with Image.open(CAND / key / m["file"]) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        if max(im.size) > LONG:
            im.thumbnail((LONG, LONG), Image.LANCZOS)
        dst.parent.mkdir(parents=True, exist_ok=True)
        im.save(dst, quality=90)
        size = im.size
    lic = m["licence"].strip()
    free = _licence_ok(lic)
    entry = {"file": rel, "source_page": m.get("page_url", ""), "source_url": m.get("image_url", ""), "author": m.get("author", "") or "unknown",
             "licence": lic if free else (lic or "unknown"), "licence_url": licence_url(lic) if free else "",
             "attribution_required": free and not re.match(r"(public domain|pd|cc0|pexels|unsplash|pixabay)", lic, re.I),
             "modified": f"downscaled to {size[0]}x{size[1]} px and re-encoded as JPEG; renderer will crop",
             "sha256": hashlib.sha256(dst.read_bytes()).hexdigest(), "retrieved_at": TODAY, "fop_note": "",
             "selected_by": f"follow-up 016/023 逐张看图（{m.get('source', '')}；候选 {key}/{cid}）"}
    if m.get("licence_as_stated"):
        entry["licence_as_stated"] = m["licence_as_stated"]
    # 许可不明的图：卡面只写作者或来源站名，不写「licence unknown」（QC 2026-11-04 M3）
    site = re.sub(r"^www\.", "", (re.match(r"https?://([^/]+)", m.get("page_url", "")) or [None, m.get("source", "")])[1])
    credit = f"{entry['author']} / {lic}" if free else (entry["author"] if entry["author"] not in ("", "unknown") else site)
    return entry, credit, free


def main() -> None:
    data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    assets = []
    for i, it in enumerate(data["items"]):
        for k in ("image_risk", "image_note", "image_alt", "image_alt_credit", "image_focus"):
            it.pop(k, None)
        ch = CHOICES.get(str(i))
        stem = Path(it["image"]).stem
        key = f"{i:02d}_{stem}"
        if not ch:
            print("NO CHOICE", i, it["name"])
            continue
        main_id, alt_id, focus = (list(ch) + [None, None])[:3]
        e, credit, free = put(key, main_id, f"assets/img/{stem}.jpg")
        assets.append(e)
        it["image"], it["image_credit"] = e["file"], credit
        if focus:
            it["image_focus"] = focus
        if not free:
            it["image_risk"] = "licence unknown"
            it["image_note"] = "Photo withheld: licence unclear"
            if alt_id:
                ea, ca, fa = put(key, alt_id, f"assets/img/{stem}_alt.jpg")
                assert fa, f"alt for {key} not free"
                assets.append(ea)
                it["image_alt"], it["image_alt_credit"] = ea["file"], ca
        print(f"{it['rank']:>2} {it['name'][:24]:24} main {main_id} {'FREE' if free else 'RISK'}" + (f" alt {alt_id}" if (not free and alt_id) else ""))
    (EP / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (EP / "assets.json").write_text(json.dumps(assets, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
