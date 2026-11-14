# -*- coding: utf-8 -*-
"""每项一行、全部候选的拼图（绿 = 可商用许可，红 = 许可不明 / 不允许）。_build/reselect/contact_NN.jpg

    python contact.py [idx,idx,...]
"""
import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
EP = HERE.parent
sys.path.insert(0, str(EP.parents[3] / "projects" / "rank_scroll"))
from rank_scroll.contract import _licence_ok  # noqa: E402

data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
only = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else None
TW, TH, PER, COLS = 150, 200, 5, 14
f = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 16)
fs = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 12)
items = [(i, it) for i, it in enumerate(data["items"]) if only is None or i in only]
for page in range(0, len(items), PER):
    rows = items[page:page + PER]
    sheet = Image.new("RGB", (200 + COLS * (TW + 6), len(rows) * (TH + 34) + 10), (22, 22, 26))
    dr = ImageDraw.Draw(sheet)
    for r, (i, it) in enumerate(rows):
        key = Path(it["image"]).stem
        d = HERE / "reselect" / "cand" / key
        meta = json.loads((d / "meta.json").read_text(encoding="utf-8")) if (d / "meta.json").exists() else []
        y = 8 + r * (TH + 34)
        dr.text((6, y), f"[{i}] #{it['rank']}", font=f, fill=(240, 240, 240))
        dr.text((6, y + 22), it["name"][:24], font=fs, fill=(220, 220, 220))
        dr.text((6, y + 40), it["country_name"], font=fs, fill=(170, 170, 170))
        if it.get("image_risk", "").startswith("FoP"):
            dr.text((6, y + 58), "FoP risk", font=fs, fill=(230, 90, 70))
        for c, m in enumerate(sorted(meta, key=lambda m: int(re.sub(r"\D", "", m["id"]) or 0))[:COLS]):
            x = 200 + c * (TW + 6)
            ok = _licence_ok(m.get("licence", ""))
            col = (40, 170, 80) if ok else (200, 60, 50)
            dr.rectangle([x, y, x + TW - 1, y + TH - 1], fill=col)
            try:
                with Image.open(d / m["file"]) as im:
                    sheet.paste(ImageOps.fit(ImageOps.exif_transpose(im).convert("RGB"), (TW - 6, TH - 6), centering=(0.5, 0.3)), (x + 3, y + 3))
            except Exception:  # noqa: BLE001
                pass
            dr.text((x + 2, y + TH + 2), f"{m['id']} {m.get('w','?')}x{m.get('h','?')} {m.get('licence','')[:14]}", font=fs, fill=col)
            dr.text((x + 2, y + TH + 16), f"{m.get('source','')[:24]}", font=fs, fill=(180, 180, 180))
    sheet.save(HERE / "reselect" / f"contact_{page // PER + 1:02d}.jpg", quality=85)
print("ok", (len(items) + PER - 1) // PER, "sheets")
