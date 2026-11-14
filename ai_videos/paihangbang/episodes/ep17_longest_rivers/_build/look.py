# -*- coding: utf-8 -*-
"""放大看几张候选：python look.py out.jpg key:cid key:cid ...（横排，每张高 520）"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
C = Path(__file__).parent / "reselect" / "cand"
H = 520
ims = []
for a in sys.argv[2:]:
    p = Path(a)
    if ":" in a and not p.exists():
        k, c = a.split(":")
        p = C / k / f"{c}.jpg"
    im = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
    im = im.resize((int(im.width * H / im.height), H))
    ImageDraw.Draw(im).text((8, 8), a, fill=(255, 255, 0), font=ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 22))
    ims.append(im)
W = sum(i.width for i in ims) + 8 * len(ims)
out = Image.new("RGB", (W, H), (0, 0, 0))
x = 0
for i in ims:
    out.paste(i, (x, 0)); x += i.width + 8
out.save(sys.argv[1], quality=85)
