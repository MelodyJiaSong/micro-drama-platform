# -*- coding: utf-8 -*-
"""给 region_blockout.py 的干净渲染加对象编号，供人看与管理站对照（标注图不进生成参考）。

    python annotate_layout.py <_blender 目录>
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT = "C:/Windows/Fonts/msyh.ttc"
COLORS = {"bg": (185, 28, 28), "m": (8, 125, 71), "SPAWN": (29, 78, 216), "doodad": (120, 72, 0)}


def color(key: str) -> tuple[int, int, int]:
    if key.startswith("SPAWN"):
        return COLORS["SPAWN"]
    if key.startswith("m"):
        return COLORS["m"]
    return COLORS["bg"] if key.startswith("bg") else COLORS["doodad"]


def short(key: str, label: str) -> str:
    if key.startswith("SPAWN"):
        return "P" + key[-1]
    if key.startswith(("bg", "m")) or (key[:1] in "JKR" and key[1:].isdigit()):
        return label
    return label.split(" ")[-1]


def main() -> None:
    root = Path(sys.argv[1])
    proj = json.loads((root / "layout_projection.json").read_text("utf8"))
    for view_id, view in proj["views"].items():
        im = Image.open(root / view["file"]).convert("RGB")
        d = ImageDraw.Draw(im)
        font = ImageFont.truetype(FONT, 17 if view_id == "top" else 19)
        for full_key, p in view["points"].items():
            key = full_key.split(":")[-1]
            x, y = p["px"]
            c = color(key)
            text = short(key, p["label"])
            d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=c, outline="white", width=2)
            tx, ty = x + 8, y - 24
            box = d.textbbox((tx, ty), text, font=font)
            d.rectangle((box[0] - 3, box[1] - 2, box[2] + 3, box[3] + 2), fill="white", outline=c)
            d.text((tx, ty), text, font=font, fill=c)
        legend = f"{proj['region']} · {view_id} · 技术布局（非成片画面）· 北{'↑' if view_id == 'top' or proj['region'] == 'all-regions' else '见 projection.json'}"
        if any(k[:1] in "JK" and k[1:].isdigit() for k in view["points"]):
            legend += " · 营地外框：品红远古 / 橙大营 / 黄中营 / 绿小营"
        d.rectangle((0, im.height - 30, im.width, im.height), fill=(255, 255, 255))
        d.text((10, im.height - 27), legend, font=ImageFont.truetype(FONT, 18), fill=(30, 41, 59))
        im.save(root / view["file"].replace(".png", "_labeled.png"))
        print("labeled", view_id, len(view["points"]))


main()
