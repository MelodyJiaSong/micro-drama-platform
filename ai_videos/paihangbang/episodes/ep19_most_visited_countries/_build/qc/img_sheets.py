"""QC: contact sheets of all on-screen images (assets/img) with size labels."""
import json, pathlib
from PIL import Image, ImageDraw
ep = pathlib.Path(__file__).resolve().parents[2]
d = json.load(open(ep / "data.json", encoding="utf-8"))
out = ep / "_build" / "qc" / "img_sheets"; out.mkdir(exist_ok=True)
items = d["items"]
W, H = 640, 427
for s in range(0, len(items), 9):
    sheet = Image.new("RGB", (W * 3, H * 3), "black"); dr = ImageDraw.Draw(sheet)
    for i, it in enumerate(items[s:s + 9]):
        im = Image.open(ep / it["image"]); sz = im.size
        im = im.convert("RGB"); im.thumbnail((W, H))
        x, y = (i % 3) * W, (i // 3) * H
        sheet.paste(im, (x + (W - im.width) // 2, y + (H - im.height) // 2))
        dr.rectangle([x, y, x + W, y + 18], fill="black")
        lab = f"#{it['rank']} {it['country_name']} | {[t['text'] for t in it.get('tags',[])][:1]} {sz[0]}x{sz[1]}"
        dr.text((x + 4, y + 3), lab, fill="yellow")
    p = out / f"imgs_{s // 9:02d}.jpg"; sheet.save(p, quality=85); print(p.name)
