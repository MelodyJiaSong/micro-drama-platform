# -*- coding: utf-8 -*-
"""ep06：`image_reselect.py apply` 之后的收尾。

- 切掉封面扫描图四周的纯白 / 纯黑留边（Doraemon 官方图带白边），重算账本 sha256；
- 所有封面统一 image_risk = "copyrighted artwork"（follow-up 014：默认母版扣下，_with-risk-images 放入，用户发布前定）；
- image_note 写真实原因；image_credit 写「© 作者 / 出版社」；账本补 rights_holder 与 risk 说明。
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image, ImageChops

EP = Path(__file__).resolve().parents[1]
TRIM = {"Doraemon"}   # 只切人工看过确有留边的图；白底封面自动切会误伤


def trim(path: Path) -> tuple[int, int] | None:
    with Image.open(path) as im0:
        im = im0.convert("RGB")
    w, h = im.size
    best = None
    for bg in ((255, 255, 255), (0, 0, 0)):
        diff = ImageChops.difference(im, Image.new("RGB", im.size, bg)).convert("L").point(lambda v: 255 if v > 18 else 0)
        box = diff.getbbox()
        if box and (box[2] - box[0]) * (box[3] - box[1]) < 0.97 * w * h:
            best = box if best is None or (box[2] - box[0]) * (box[3] - box[1]) < (best[2] - best[0]) * (best[3] - best[1]) else best
    if not best:
        return None
    im.crop(best).save(path, quality=92)
    return best[2] - best[0], best[3] - best[1]


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    d = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    assets = json.loads((EP / "assets.json").read_text(encoding="utf-8"))
    by = {a["file"]: a for a in assets}
    for it in d["items"]:
        f = EP / it["image"]
        if not f.exists():
            print("缺图", it["rank"], it["name"])
            continue
        size = trim(f) if it["name"] in TRIM else None
        a = by.get(it["image"])
        if a is None:
            print("账本缺", it["image"])
            continue
        if size:
            a["modified"] = f"trimmed border to {size[0]}x{size[1]} px; " + a.get("modified", "")
            print("切边", it["name"], size)
        a["sha256"] = hashlib.sha256(f.read_bytes()).hexdigest()
        pub = it["country_name"]
        a["rights_holder"] = f"{it['author']} / {pub}" if it.get("author") else pub
        a["risk_note"] = "Copyrighted cover artwork; not licensed. Used only in the _with-risk-images render if the user signs off before publishing (follow-up 014)."
        it["image_risk"] = "copyrighted artwork"
        it["image_note"] = "Cover withheld: copyrighted artwork"
        holder = it.get("tags", [{}])[0].get("text", "")
        it["image_credit"] = f"Illustration: © {holder} / {pub}"
    (EP / "data.json").write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (EP / "assets.json").write_text(json.dumps(assets, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("完成")


if __name__ == "__main__":
    main()
