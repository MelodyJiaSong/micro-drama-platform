# -*- coding: utf-8 -*-
"""候选拼图：python sheet.py <输出名> idx [idx ...]  → reselect/sheet_<名>.jpg（每行一项，列出全部候选；绿=可商用 红=不可/不明）"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "projects" / "rank_scroll"))
from rank_scroll.contract import _licence_ok  # noqa: E402

EP = Path(__file__).resolve().parents[1]
C = EP / "_build" / "reselect" / "cand"
data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
name, idxs = sys.argv[1], [int(x) for x in sys.argv[2:]]
TW, TH, PER = 260, 289, 8
f = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 16)
fs = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 12)
rows = []
for i in idxs:
    it = data["items"][i]
    key = f"{i:02d}_{Path(it['image']).stem}"
    meta = json.loads((C / key / "meta.json").read_text(encoding="utf-8")) if (C / key / "meta.json").exists() else []
    rows.append((i, it, key, meta))
ncol = max([min(PER, len(m)) for *_, m in rows] + [1])
sheet = Image.new("RGB", (180 + ncol * (TW + 6), len(rows) * (TH + 40) + 10), (20, 20, 24))
dr = ImageDraw.Draw(sheet)
for r, (i, it, key, meta) in enumerate(rows):
    y = 10 + r * (TH + 40)
    dr.text((6, y), f"idx{i} #{it['rank']}", font=f, fill=(240, 240, 240))
    dr.text((6, y + 22), it["name"][:20], font=f, fill=(240, 240, 240))
    for c, m in enumerate(meta[:PER]):
        x = 180 + c * (TW + 6)
        ok = _licence_ok(m.get("licence", ""))
        col = (40, 170, 80) if ok else (200, 60, 60)
        dr.rectangle([x, y, x + TW - 1, y + TH - 1], fill=col)
        try:
            with Image.open(C / key / m["file"]) as im:
                sheet.paste(ImageOps.fit(ImageOps.exif_transpose(im).convert("RGB"), (TW - 6, TH - 6), centering=(0.5, 0.5)), (x + 3, y + 3))
        except Exception:  # noqa: BLE001
            pass
        dr.text((x + 2, y + TH + 2), f"{m['id']} {m.get('w')}x{m.get('h')} {m.get('source','')[:10]}", font=fs, fill=(220, 220, 220))
        dr.text((x + 2, y + TH + 18), f"{m.get('licence','')[:24]}", font=fs, fill=col)
out = EP / "_build" / "reselect" / f"sheet_{name}.jpg"
sheet.save(out, quality=85)
print(out)
