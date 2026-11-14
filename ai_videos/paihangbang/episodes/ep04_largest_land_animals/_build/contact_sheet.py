# -*- coding: utf-8 -*-
"""每张卡的全部候选拼成一行（编号、分辨率、来源、许可颜色：绿=可商用免署名 / 黄=CC 需署名 / 红=许可不明），
供逐张看图核对物种与画质。输出 reselect/sheet_NN.jpg（每页 5 项）。用法：python -I <本文件> [--per 5]"""
import argparse
import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

EP = Path(__file__).resolve().parents[1]
B = EP / "_build" / "reselect"
TW, TH = 300, 334   # 卡片比例 720:800


def lic_colour(lic: str):
    low = lic.lower()
    if re.match(r"(public domain|pd|cc0|pexels|unsplash|pixabay)", low):
        return (60, 190, 90)
    if low.startswith(("cc by", "cc-by")) and not re.search(r"\b(nc|nd)\b", low.replace("-", " ")):
        return (230, 190, 40)
    return (225, 70, 60)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--per", type=int, default=5)
    ap.add_argument("--only", default="", help="逗号分隔的 idx")
    ap.add_argument("--prefix", default="", help="只看 id 以这些字母开头的候选，如 no")
    ap.add_argument("--name", default="sheet")
    a = ap.parse_args()
    data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    f = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 20)
    fs = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 14)
    rows = []
    for i, it in enumerate(data["items"]):
        key = f"{i:02d}_" + re.sub(r"[^a-z0-9]+", "_", it["name"].lower()).strip("_")
        d = B / "cand" / key
        meta = json.loads((d / "meta.json").read_text(encoding="utf-8")) if (d / "meta.json").exists() else []
        if a.prefix:
            meta = [m for m in meta if m["id"][0] in a.prefix]
        if not a.only or i in {int(x) for x in a.only.split(",")}:
            rows.append((i, it, d, meta))
    ncol = max([len(m) for *_, m in rows] + [1])
    for p in range(0, len(rows), a.per):
        page = rows[p:p + a.per]
        W = 230 + ncol * (TW + 8)
        sheet = Image.new("RGB", (W, len(page) * (TH + 52) + 10), (22, 22, 26))
        dr = ImageDraw.Draw(sheet)
        for r, (i, it, d, meta) in enumerate(page):
            y = 10 + r * (TH + 52)
            dr.text((8, y), f"#{it['rank']} {it['name']}", font=f, fill=(240, 240, 240))
            dr.text((8, y + 30), f"idx {i} · {len(meta)} 张", font=fs, fill=(170, 170, 170))
            for k, m in enumerate(meta):
                x = 230 + k * (TW + 8)
                col = lic_colour(m.get("licence", ""))
                dr.rectangle([x, y, x + TW - 1, y + TH - 1], fill=col)
                try:
                    with Image.open(d / m["file"]) as im:
                        sheet.paste(ImageOps.fit(ImageOps.exif_transpose(im).convert("RGB"), (TW - 8, TH - 8)), (x + 4, y + 4))
                except Exception:  # noqa: BLE001
                    dr.text((x + 8, y + 8), "读图失败", font=fs, fill=(255, 255, 255))
                dr.text((x + 2, y + TH + 2), f"{m['id']} {m.get('w','?')}×{m.get('h','?')} {m.get('source','')[:16]}", font=fs, fill=(225, 225, 225))
                dr.text((x + 2, y + TH + 20), f"{m.get('licence','')[:34]}", font=fs, fill=col)
        out = B / f"{a.name}_{p // a.per + 1:02d}.jpg"
        sheet.save(out, quality=82)
        print(out)


if __name__ == "__main__":
    main()
