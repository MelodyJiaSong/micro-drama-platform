# -*- coding: utf-8 -*-
"""把 30 张卡渲染成拼图供逐张审看：python card_sheet.py [--risk]"""
import sys
from pathlib import Path
EP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EP.parents[3] / "projects" / "rank_scroll"))
import numpy as np
import skia
from PIL import Image
from rank_scroll.contract import load_episode
from rank_scroll.cards import card_image, PAD
from rank_scroll.theme import get_theme
from rank_scroll import draw as D

risk = "--risk" in sys.argv
ep, _ = load_episode(EP, allow_risk_images=risk)
th, _ = get_theme(ep.theme)
cols, sc = 6, 0.5
tiles = []
for it in ep.items:
    flags = []
    img = card_image(ep, it, th, sc, flag_out=flags)
    arr = img.toarray(colorType=skia.kRGBA_8888_ColorType)
    im = Image.fromarray(arr, "RGBA")
    tiles.append(im)
w, h = tiles[0].size
sheet = Image.new("RGB", (cols * w, ((len(tiles) + cols - 1) // cols) * h), (14, 12, 38))
for i, t in enumerate(tiles):
    sheet.paste(t, ((i % cols) * w, (i // cols) * h), t)
out = EP / "_build" / "card_sheets" / f"cards_{'risk' if risk else 'default'}.jpg"
sheet.save(out, quality=85)
print(out, sheet.size)
