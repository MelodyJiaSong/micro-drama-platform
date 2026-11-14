# -*- coding: utf-8 -*-
"""全部候选拼图：每行一项，列出该项所有已下载候选（id、许可色、尺寸、来源）。python sheet_all.py [idx ...]"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

sys.stdout.reconfigure(encoding="utf-8")
EP = Path(__file__).resolve().parents[1]
CAND = EP / "_build" / "reselect" / "cand"
OUT = EP / "_build" / "sheets"
OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(EP.parents[3] / "projects" / "rank_scroll"))
from rank_scroll.contract import _licence_ok  # noqa: E402

data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
only = [int(x) for x in sys.argv[1:]]
TW, TH = 252, 280
f = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 17)
fs = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 13)
rows = [(i, it) for i, it in enumerate(data["items"]) if not only or i in only]
for page in range(0, len(rows), 6):
    chunk = rows[page:page + 6]
    sheet = Image.new("RGB", (200 + 8 * (TW + 6), len(chunk) * (TH + 40) + 10), (20, 20, 24))
    dr = ImageDraw.Draw(sheet)
    for r, (i, it) in enumerate(chunk):
        key = f"{i:02d}_{Path(it['image']).stem}"
        d = CAND / key
        meta = json.loads((d / "meta.json").read_text(encoding="utf-8")) if (d / "meta.json").exists() else []
        y = 10 + r * (TH + 40)
        dr.text((8, y), f"#{it['rank']} idx{i}", font=f, fill=(240, 240, 240))
        dr.text((8, y + 24), it["name"][:22], font=fs, fill=(200, 200, 200))
        dr.text((8, y + 44), f"{len(meta)} cand", font=fs, fill=(160, 160, 160))
        for s, m in enumerate(meta[:8]):
            x = 200 + s * (TW + 6)
            ok = _licence_ok(m.get("licence", ""))
            col = (40, 170, 80) if ok else (200, 60, 50)
            dr.rectangle([x, y, x + TW - 1, y + TH - 1], fill=col)
            try:
                with Image.open(d / m["file"]) as im:
                    sheet.paste(ImageOps.fit(ImageOps.exif_transpose(im).convert("RGB"), (TW - 6, TH - 6)), (x + 3, y + 3))
            except Exception:  # noqa: BLE001
                pass
            dr.text((x + 2, y + TH + 2), f"{m['id']} {m.get('w','?')}x{m.get('h','?')} {m.get('score','')}", font=fs, fill=(230, 230, 230))
            dr.text((x + 2, y + TH + 19), f"{m.get('source','')[:14]} | {m.get('licence','')[:16]}", font=fs, fill=col)
    out = OUT / f"all_{page // 6 + 1:02d}.jpg"
    sheet.save(out, quality=85)
    print(out)
