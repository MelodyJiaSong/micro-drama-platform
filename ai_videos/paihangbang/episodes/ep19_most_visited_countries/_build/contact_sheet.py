# -*- coding: utf-8 -*-
"""每项全部候选的缩略拼图（按 9:10 卡片比例裁切预览），供亲眼选图：reselect/sheet_NN.jpg，每页 5 项。"""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
HERE = Path(__file__).resolve().parent
EP = HERE.parent
data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
TW, TH = 180, 200
f = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 16)
fs = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 12)
only = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else None
items = [(i, it) for i, it in enumerate(data["items"]) if only is None or i in only]
per = 5
for page in range(0, len(items), per):
    rows = items[page:page + per]
    W = 160 + 13 * (TW + 6)
    sheet = Image.new("RGB", (W, len(rows) * (TH + 22) + 8), (22, 22, 26))
    dr = ImageDraw.Draw(sheet)
    for r, (i, it) in enumerate(rows):
        key = f"{i:02d}_{Path(it['image']).stem}"
        d = HERE / "reselect" / "cand" / key
        meta = json.loads((d / "meta.json").read_text(encoding="utf-8")) if (d / "meta.json").exists() else []
        y = 6 + r * (TH + 22)
        dr.text((6, y), f"#{it['rank']} {it['name']}", font=f, fill=(240, 240, 240))
        dr.text((6, y + 24), f"idx {i}", font=fs, fill=(170, 170, 170))
        dr.text((6, y + 42), it["landmark"][:22], font=fs, fill=(170, 170, 170))
        for s, m in enumerate(meta[:13]):
            x = 160 + s * (TW + 6)
            try:
                with Image.open(d / m["file"]) as im:
                    sheet.paste(ImageOps.fit(ImageOps.exif_transpose(im).convert("RGB"), (TW, TH), centering=(0.5, 0.45)), (x, y))
            except Exception:
                pass
            dr.text((x + 2, y + TH + 2), f"{m['id']} {m.get('w','?')}x{m.get('h','?')} {m.get('source','')[:8]}", font=fs, fill=(220, 220, 220))
    out = HERE / "reselect" / (f"sheet_{page // per + 1:02d}.jpg" if only is None else f"sheet_x{page // per + 1:02d}.jpg")
    sheet.save(out, quality=85)
    print(out.name)
