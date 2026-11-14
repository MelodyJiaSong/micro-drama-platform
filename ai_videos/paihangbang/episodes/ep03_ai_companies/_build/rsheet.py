# -*- coding: utf-8 -*-
"""按轮次前缀出候选拼图：python rsheet.py <prefix> <out_name> slug:kind ...（只列 id 以 prefix 开头的候选）"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ref_images as R
from PIL import Image, ImageDraw, ImageFont
prefix, name, rows = sys.argv[1], sys.argv[2], [a.split(":") for a in sys.argv[3:]]
tw, th, nc = 200, 222, 7
f = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 13)
sheet = Image.new("RGB", (160 + nc * (tw + 6), len(rows) * (th + 22) + 10), (24, 24, 28)); dr = ImageDraw.Draw(sheet)
for r, (s, k) in enumerate(rows):
    y = 10 + r * (th + 22); dr.text((6, y), f"{s}\n{k}", font=f, fill=(240, 240, 240))
    d = R.REF / s / k
    ms = [m for m in json.loads((d / "meta.json").read_text(encoding="utf-8")) if "file" in m and "error" not in m and m["id"].startswith(prefix)] if (d / "meta.json").exists() else []
    for i, m in enumerate(ms[:nc]):
        x = 160 + i * (tw + 6); t = R._thumb(d / m["file"], (tw, th), (60, 60, 60, 255))
        if t: sheet.paste(t, (x, y))
        dr.text((x, y + th + 2), f"{m['id']} {m.get('w')}x{m.get('h')} {m.get('licence','')[:12]}", font=f, fill=(200, 200, 200))
out = R.BUILD / "ref_sheets" / f"{name}.jpg"; sheet.save(out, quality=88); print(out)
