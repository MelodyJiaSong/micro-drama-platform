"""Make contact sheets of the selected images for visual QC (subject = the building, completed, exterior).

Usage: python -I 09_contact_sheet.py <episode_dir> <out_dir> [per_sheet]
"""
import json
import os
import sys

from PIL import Image, ImageDraw


def main(edir, odir, per=10):
    per = int(per)
    os.makedirs(odir, exist_ok=True)
    assets = json.load(open(os.path.join(edir, "assets.json"), encoding="utf-8"))
    tiles = []
    for a in assets:
        im = Image.open(os.path.join(edir, a["file"])).convert("RGB")
        im.thumbnail((260, 260))
        t = Image.new("RGB", (270, 290), "white")
        t.paste(im, ((270 - im.width) // 2, 5))
        ImageDraw.Draw(t).text((5, 272), os.path.basename(a["file"])[:40], fill="black")
        tiles.append(t)
    cols = 5
    for s in range(0, len(tiles), per):
        chunk = tiles[s:s + per]
        rows = (len(chunk) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * 270, rows * 290), "gray")
        for i, t in enumerate(chunk):
            sheet.paste(t, ((i % cols) * 270, (i // cols) * 290))
        p = os.path.join(odir, f"sheet_{s // per + 1}.jpg")
        sheet.save(p, quality=80)
        print(p)


if __name__ == "__main__":
    main(*sys.argv[1:4])
