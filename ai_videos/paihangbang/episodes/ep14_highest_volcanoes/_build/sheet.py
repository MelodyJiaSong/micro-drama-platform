# 自用候选拼图：每行一项，全部候选（含许可颜色：绿=可商用，红=风险），用于逐张看图
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
sys.path.insert(0, "C:/workspace/micro-drama-platform/projects/rank_scroll")
from rank_scroll.contract import _licence_ok
H = Path(__file__).resolve().parent
C = H / "reselect" / "cand"
def okl(l):
    l2 = l.lower().replace("creative commons attribution-sharealike", "cc by-sa").replace("creative commons attribution", "cc by").replace("attribution 4.0", "by 4.0")
    return _licence_ok(l) or _licence_ok(l2) or "public domain" in l.lower() or "cc0" in l.lower()
keys = sys.argv[2:]
out = sys.argv[1]
TW, TH, PER = 230, 256, 7
f = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 16); fs = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 12)
rows = []
for k in keys:
    d = next(C.glob(f"*_{k}*")) if not (C / k).exists() else C / k
    meta = json.loads((d / "meta.json").read_text(encoding="utf-8"))
    rows.append((d.name, meta))
ncol = max(1, max(len(m) for _, m in rows))
ncol = min(ncol, 12)
sheet = Image.new("RGB", (200 + ncol * (TW + 6), len(rows) * (TH + 44) + 10), (20, 20, 24))
dr = ImageDraw.Draw(sheet)
for r, (name, meta) in enumerate(rows):
    y = 8 + r * (TH + 44)
    dr.text((6, y), name[3:28], font=f, fill=(240, 240, 240))
    for s, m in enumerate(meta[:ncol]):
        x = 200 + s * (TW + 6)
        col = (40, 180, 80) if okl(m.get("licence", "")) else (200, 60, 50)
        dr.rectangle([x, y, x + TW - 1, y + TH - 1], fill=col)
        try:
            with Image.open(C / name / m["file"]) as im:
                sheet.paste(ImageOps.fit(ImageOps.exif_transpose(im).convert("RGB"), (TW - 6, TH - 6)), (x + 3, y + 3))
        except Exception:
            pass
        dr.text((x + 2, y + TH + 2), f"{m['id']} {m.get('w')}x{m.get('h')} {m.get('source','')[:18]}", font=fs, fill=(220, 220, 220))
        dr.text((x + 2, y + TH + 18), f"{m.get('licence','')[:16]} | {m.get('author','')[:12]}", font=fs, fill=col)
sheet.save(out, quality=85)
print(out, sheet.size)
