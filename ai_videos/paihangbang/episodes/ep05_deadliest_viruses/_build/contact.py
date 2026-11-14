# -*- coding: utf-8 -*-
"""候选拼图：每行一种病毒，列出全部已下载候选（编号、来源、许可色、分辨率）。绿=可商用免署名，黄=需署名，红=许可不明。"""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
EP = Path(__file__).resolve().parents[1]
cand = EP / "_build" / "reselect" / "cand"
keys = sorted(p.name for p in cand.iterdir() if p.is_dir())
only = sys.argv[1:]
if only: keys = [k for k in keys if any(o in k for o in only)]
TW, TH, per = 260, 290, 8
f = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 18); fs = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 13)
def col(lic):
    l = lic.lower()
    if l.startswith(("public domain", "pd", "cc0", "pexels", "unsplash", "pixabay", "ai-generated")): return (60, 200, 90)
    if l.startswith(("cc by", "cc-by")) and " nc" not in l.replace("-", " ") and " nd" not in l.replace("-", " "): return (230, 190, 40)
    return (220, 70, 60)
for page in range(0, len(keys), per):
    rows = keys[page:page + per]
    maxc = max([len(json.loads((cand / k / "meta.json").read_text(encoding="utf-8"))) if (cand / k / "meta.json").exists() else 0 for k in rows] + [1])
    sheet = Image.new("RGB", (200 + maxc * (TW + 8), len(rows) * (TH + 44) + 10), (20, 20, 24))
    d = ImageDraw.Draw(sheet)
    for r, k in enumerate(rows):
        y = 10 + r * (TH + 44)
        d.text((8, y), k[3:], font=f, fill=(240, 240, 240))
        meta = json.loads((cand / k / "meta.json").read_text(encoding="utf-8")) if (cand / k / "meta.json").exists() else []
        for c, m in enumerate(meta):
            x = 200 + c * (TW + 8)
            try:
                with Image.open(cand / k / m["file"]) as im:
                    sheet.paste(ImageOps.fit(ImageOps.exif_transpose(im).convert("RGB"), (TW, TH)), (x, y))
            except Exception:
                pass
            d.rectangle([x, y, x + TW - 1, y + TH - 1], outline=col(m.get("licence", "")), width=4)
            d.text((x + 2, y + TH + 2), f"{m['id']} {m.get('w')}x{m.get('h')} {m.get('source','')[:16]}", font=fs, fill=(220, 220, 220))
            d.text((x + 2, y + TH + 20), m.get("licence", "")[:30], font=fs, fill=col(m.get("licence", "")))
    out = EP / "_build" / f"contact_{page // per + 1:02d}.jpg"
    sheet.save(out, quality=85); print(out)
