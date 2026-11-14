# -*- coding: utf-8 -*-
"""ep16 全候选拼图：每项一行，列出 meta_comm.json 里所有候选（id、尺寸、来源、许可颜色：绿=免署名可商用，黄=CC 需署名，红=许可不明）。
    python _build/contact.py [--only idx,idx] [--per 6]  → _build/reselect/contact_NN.jpg"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

B = Path(__file__).resolve().parent
EP = B.parent


def colour(lic: str) -> tuple[int, int, int]:
    low = lic.lower()
    if re.match(r"(public domain|pd|cc0|pexels|unsplash|pixabay)", low):
        return (60, 190, 90)
    if low.startswith("cc by") and not re.search(r"\b(nc|nd)\b", low.replace("-", " ")):
        return (230, 200, 50)
    return (230, 80, 70)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--per", type=int, default=5)
    ap.add_argument("--cols", type=int, default=9)
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    only = [int(x) for x in a.only.split(",") if x] or list(range(len(data["items"])))
    f = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 18)
    fs = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 13)
    TW, TH = 200, 222
    for page in range(0, len(only), a.per):
        rows = only[page:page + a.per]
        cols = a.cols
        lines = []
        for i in rows:
            it = data["items"][i]
            key = f"{i:02d}_{Path(it['image']).stem}"
            d = B / "reselect" / "cand" / key
            meta = json.loads((d / "meta_comm.json").read_text(encoding="utf-8")) if (d / "meta.json").exists() else []
            for k in range(0, max(1, len(meta)), cols):
                lines.append((i, it, d, meta[k:k + cols], k == 0))
        sheet = Image.new("RGB", (210 + cols * (TW + 6), len(lines) * (TH + 36) + 10), (22, 22, 26))
        dr = ImageDraw.Draw(sheet)
        for r, (i, it, d, ms, first) in enumerate(lines):
            y = 10 + r * (TH + 36)
            if first:
                dr.text((8, y), f"#{it['rank']} idx{i}", font=f, fill=(240, 240, 240))
                dr.text((8, y + 26), it["name"][:24], font=fs, fill=(220, 220, 220))
                dr.text((8, y + 44), it["country_name"], font=fs, fill=(170, 170, 170))
            for s, m in enumerate(ms):
                x = 210 + s * (TW + 6)
                col = colour(m.get("licence", ""))
                dr.rectangle([x, y, x + TW - 1, y + TH - 1], fill=col)
                try:
                    with Image.open(d / m["file"]) as im:
                        sheet.paste(ImageOps.fit(ImageOps.exif_transpose(im).convert("RGB"), (TW - 6, TH - 6)), (x + 3, y + 3))
                except Exception:  # noqa: BLE001
                    pass
                dr.text((x + 2, y + TH + 2), f"{m['id']} {m.get('w','?')}x{m.get('h','?')}", font=fs, fill=(235, 235, 235))
                dr.text((x + 2, y + TH + 18), f"{(m.get('source') or '')[:14]} {(m.get('licence') or '')[:12]}", font=fs, fill=col)
        sheet.save(B / "reselect" / f"contact{a.tag}_{page // a.per + 1:02d}.jpg", quality=84)
    print("ok")


if __name__ == "__main__":
    main()
