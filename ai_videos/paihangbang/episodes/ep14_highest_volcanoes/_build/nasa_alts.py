# -*- coding: utf-8 -*-
"""审片修复 4：用 NASA 公有领域的 ISS / Earth Observatory 真实影像替换默认版的 AI 图（作 image_alt；AI-only 项作 image）。
每项按看图确定的中心点裁成 9:10，原分辨率（不放大）；账本 licence 写 "Public domain (NASA)"。

    python _build/nasa_alts.py           # 裁切 + 写 data.json / assets.json
"""
import hashlib
import json
from datetime import date
from pathlib import Path

from PIL import Image

H = Path(__file__).resolve().parent
EP = H.parent
C = H / "reselect" / "cand"
N = H / "nasa"

# gvp_volcano_number: (源文件, 中心 x, 中心 y（0–1）, 裁切高占原图比例, 作者, 来源页, 原图 URL)
ALTS = {
    355130: (N / "iss074e0760459.jpg", 0.53, 0.55, 0.62, "NASA / ISS Expedition 74 crew (iss074e0760459)",
             "https://www.nasa.gov/image-detail/amf-iss074e0760459/", "https://images-assets.nasa.gov/image/iss074e0760459/iss074e0760459~orig.jpg"),
    355110: (C / "01_02_llullaillaco" / "c12.jpg", 0.56, 0.58, 0.80, "NASA / ISS Expedition 22 crew (ISS022-E-8285)",
             "https://science.nasa.gov/earth/earth-observatory/llullaillaco-volcano-argentina-chile-border-43256/", "https://eol.jsc.nasa.gov/DatabaseImages/ESC/large/ISS022/ISS022-E-8285.JPG"),
    354003: (C / "04_05_coropuna" / "c11.jpg", 0.46, 0.50, 0.70, "NASA / ISS Expedition 25 crew (ISS025-E-6163)",
             "https://science.nasa.gov/earth/earth-observatory/nevado-coropuna-peru-47114", "https://eol.jsc.nasa.gov/DatabaseImages/ESC/large/ISS025/ISS025-E-6163.JPG"),
    355190: (N / "iss024e012425.jpg", 0.22, 0.22, 0.45, "NASA / ISS Expedition 24 crew (ISS024-E-12425)",
             "https://images.nasa.gov/details/iss024e012425", "https://images-assets.nasa.gov/image/iss024e012425/iss024e012425~orig.jpg"),
    355012: (C / "06_07_parinacota" / "c16.jpg", 0.45, 0.45, 1.00, "NASA Earth Observatory / ISS crew (Volcanic Duo in the Andes)",
             "https://science.nasa.gov/earth/earth-observatory/volcanic-duo-in-the-andes-mountains-152044/", None),
    355032: (N / "iss035e018006.jpg", 0.45, 0.42, 0.60, "NASA / ISS Expedition 35 crew (ISS035-E-18006)",
             "https://images.nasa.gov/details/iss035e018006", "https://images-assets.nasa.gov/image/iss035e018006/iss035e018006~orig.jpg"),
    354020: (N / "iss013e66488.jpg", 0.62, 0.55, 0.85, "NASA / ISS Expedition 13 crew (ISS013-E-66488)",
             "https://images.nasa.gov/details/iss013e66488", "https://images-assets.nasa.gov/image/iss013e66488/iss013e66488~orig.jpg"),
    355160: (C / "11_12_aracar" / "c11.jpg", 0.49, 0.52, 0.55, "NASA / ISS Expedition 6 crew (ISS006-E-13813)",
             "https://eol.jsc.nasa.gov/SearchPhotos/photo.pl?mission=ISS006&roll=E&frame=13813", "https://eol.jsc.nasa.gov/DatabaseImages/ESC/large/ISS006/ISS006-E-13813.JPG"),
    355020: (C / "12_13_guallatiri" / "c11.jpg", 0.28, 0.55, 0.55, "NASA / ISS Expedition 9 crew (ISS009-E-6848)",
             "https://eol.jsc.nasa.gov/SearchPhotos/photo.pl?mission=ISS009&roll=E&frame=6848", "https://eol.jsc.nasa.gov/DatabaseImages/ESC/large/ISS009/ISS009-E-6848.JPG"),
    355107: (C / "08_09_pular" / "c8.jpg", 0.50, 0.50, 0.80, "NASA / ISS Expedition 29 crew (ISS029-E-17352)",
             "https://eol.jsc.nasa.gov/SearchPhotos/photo.pl?mission=ISS029&roll=E&frame=17352", "https://eol.jsc.nasa.gov/DatabaseImages/ESC/large/ISS029/ISS029-E-17352.JPG"),
}


def crop(src: Path, cx: float, cy: float, hfrac: float, dst: Path) -> tuple[int, int]:
    im = Image.open(src).convert("RGB")
    w, h = im.size
    ch = int(h * hfrac)
    cw = int(ch * 0.9)
    if cw > w:
        cw = w; ch = int(cw / 0.9)
    x0 = max(0, min(w - cw, int(cx * w - cw / 2)))
    y0 = max(0, min(h - ch, int(cy * h - ch / 2)))
    im.crop((x0, y0, x0 + cw, y0 + ch)).save(dst, quality=92)
    return cw, ch


def main() -> None:
    d = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    assets = json.loads((EP / "assets.json").read_text(encoding="utf-8"))
    for it in d["items"]:
        vn = it["gvp_volcano_number"]
        if vn not in ALTS:
            continue
        src, cx, cy, hf, author, page, url = ALTS[vn]
        if url is None:
            meta = next(m for m in json.loads((src.parent / "meta.json").read_text(encoding="utf-8")) if m["file"] == src.name)
            url = meta["image_url"]
        stem = Path(it["image"]).stem.replace("_gen", "")
        rel = f"assets/img/{stem}_nasa.jpg"
        size = crop(src, cx, cy, hf, EP / rel)
        assets = [a for a in assets if a["file"] != rel] + [{
            "file": rel, "source_page": page, "source_url": url, "author": author, "licence": "Public domain (NASA)",
            "licence_url": "https://www.nasa.gov/nasa-brand-center/images-and-media/", "attribution_required": False,
            "modified": f"cropped to {size[0]}x{size[1]} px around the volcano; no other changes",
            "sha256": hashlib.sha256((EP / rel).read_bytes()).hexdigest(), "retrieved_at": date.today().isoformat(),
            "fop_note": "", "selected_by": "审片修复 4：NASA 公有领域宇航员照片，Claude 看图认对、裁切"}]
        credit = f"{author.split(' (')[0]} / Public domain"
        if it.get("image_risk"):
            it["image_alt"], it["image_alt_credit"] = rel, credit
        else:
            it["image"], it["image_credit"] = rel, credit
            it.pop("image_focus", None)
        print(it["rank"], it["name"], rel, size)
    used = {it.get("image") for it in d["items"]} | {it.get("image_alt") for it in d["items"]}
    assets = [a for a in assets if a["file"] in used]
    (EP / "data.json").write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (EP / "assets.json").write_text(json.dumps(assets, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
