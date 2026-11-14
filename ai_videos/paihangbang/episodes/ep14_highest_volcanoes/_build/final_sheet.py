# 终版逐张核对拼图：每项 [image | image_alt]，标名次、名称、许可
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
EP = Path(__file__).resolve().parents[1]
d = json.loads((EP / "data.json").read_text(encoding="utf-8")); A = {a["file"]: a for a in json.loads((EP / "assets.json").read_text(encoding="utf-8"))}
lo, hi = int(sys.argv[2]), int(sys.argv[3])
items = [it for it in d["items"] if lo <= it["rank"] <= hi]
TW, TH = 252, 280
f = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 13)
cols = 5
sheet = Image.new("RGB", (cols * (2 * TW + 14), ((len(items) + cols - 1) // cols) * (TH + 40)), (20, 20, 24))
dr = ImageDraw.Draw(sheet)
for n, it in enumerate(items):
    x0 = (n % cols) * (2 * TW + 14); y0 = (n // cols) * (TH + 40)
    for k, key in enumerate(("image", "image_alt")):
        rel = it.get(key)
        if rel and (EP / rel).exists():
            im = ImageOps.fit(Image.open(EP / rel).convert("RGB"), (TW - 4, TH - 4), centering=tuple(it.get("image_focus", [0.5, 0.4])))
            sheet.paste(im, (x0 + k * TW + 2, y0 + 2))
    lic = (A.get(it.get("image"), {}).get("licence", "-"))[:18]
    risk = "R " if it.get("image_risk") else ""
    dr.text((x0 + 2, y0 + TH + 2), f"#{it['rank']} {it['name'][:20]} | {risk}{lic}", font=f, fill=(240, 240, 240))
    dr.text((x0 + 2, y0 + TH + 19), f"alt: {A.get(it.get('image_alt'), {}).get('licence', '-')[:30]}", font=f, fill=(170, 200, 170))
sheet.save(sys.argv[1], quality=85); print(sheet.size)
