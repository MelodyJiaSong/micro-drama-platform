# 模拟满版卡裁切（正方形，焦点 image_focus / layout.focus），底部 40% 叠暗渐变示意文字区，逐项检查船体是否被遮
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
EP = Path(__file__).resolve().parents[1]
d = json.loads((EP / "data.json").read_text(encoding="utf-8"))
f = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 16)
S = 240; cols = 7
alt = "--alt" in sys.argv
items = d["items"]
rows = (len(items) + cols - 1) // cols
sheet = Image.new("RGB", (cols * (S + 6) + 6, rows * (S + 26) + 6), (20, 20, 24))
dr = ImageDraw.Draw(sheet)
for k, it in enumerate(items):
    x = 6 + (k % cols) * (S + 6); y = 6 + (k // cols) * (S + 26)
    rel = it.get("image_alt") if (alt and it.get("image_alt")) else it.get("image")
    p = EP / rel if rel else None
    if p and p.exists():
        im = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
        fx, fy = it.get("image_focus") or d["layout"].get("focus", [0.5, 0.5])
        w, h = im.size; side = min(w, h)
        left = int(max(0, min(w - side, fx * w - side / 2))); top = int(max(0, min(h - side, fy * h - side / 2)))
        im = im.crop((left, top, left + side, top + side)).resize((S, S))
        ov = Image.new("L", (S, S), 0); od = ImageDraw.Draw(ov)
        for yy in range(int(S * 0.6), S): od.line([(0, yy), (S, yy)], fill=int(200 * (yy - S * 0.6) / (S * 0.4)))
        im = Image.composite(Image.new("RGB", (S, S), (6, 24, 42)), im, ov)
        sheet.paste(im, (x, y))
    tag = ("RISK " if it.get("image_risk") else "") + ("ALT " if it.get("image_alt") else "")
    dr.text((x, y + S + 2), f"#{it['rank']} {it['key'][:14]} {tag}", font=f, fill=(255, 200, 120) if tag else (220, 220, 220))
sheet.save(EP / "_build" / ("cropsheet_alt.jpg" if alt else "cropsheet.jpg"), quality=88)
print("ok")
