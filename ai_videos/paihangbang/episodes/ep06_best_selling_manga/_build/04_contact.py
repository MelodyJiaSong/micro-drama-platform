# -*- coding: utf-8 -*-
"""ep06：每部作品一行，列出全部候选（按分数），标编号、分辨率、来源，供人工逐张核对作品与择优。"""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
EP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EP.parents[1] / "_tools")); sys.path.insert(0, str(EP.parents[3]))
from image_reselect import item_key
d = json.loads((EP / "data.json").read_text(encoding="utf-8"))
C = EP / "_build" / "reselect" / "cand"; OUT = EP / "_build" / "contact"; OUT.mkdir(exist_ok=True)
TW, TH, PER = 150, 210, 6
f = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 16); fs = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 12)
items = list(enumerate(d["items"]))
for p in range(0, len(items), PER):
    rows = items[p:p + PER]
    sheet = Image.new("RGB", (170 + 10 * (TW + 6), len(rows) * (TH + 34) + 8), (24, 24, 28)); dr = ImageDraw.Draw(sheet)
    for r, (i, it) in enumerate(rows):
        dd = C / item_key(i, it); y = 6 + r * (TH + 34)
        dr.text((6, y), f"{i}: #{it['rank']}", font=f, fill=(255, 255, 255)); dr.text((6, y + 22), it["name"][:20], font=fs, fill=(220, 220, 220))
        meta = json.loads((dd / "meta.json").read_text(encoding="utf-8")) if (dd / "meta.json").exists() else []
        for k, m in enumerate(meta[:10]):
            x = 170 + k * (TW + 6)
            try:
                with Image.open(dd / m["file"]) as im:
                    sheet.paste(ImageOps.contain(ImageOps.exif_transpose(im).convert("RGB"), (TW, TH)), (x, y))
            except Exception: pass
            dr.text((x, y + TH + 2), f"{m['id']} {m.get('w')}x{m.get('h')} {m.get('score')}", font=fs, fill=(255, 220, 120) if k == 0 else (200, 200, 200))
            dr.text((x, y + TH + 16), (m.get("source") or "")[:22], font=fs, fill=(150, 150, 160))
    sheet.save(OUT / f"all_{p // PER + 1}.jpg", quality=88)
print("ok")
