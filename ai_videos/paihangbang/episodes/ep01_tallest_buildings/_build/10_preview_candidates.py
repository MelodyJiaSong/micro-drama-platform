"""Download 330 px standard thumbnails of given candidates and make one labelled preview sheet.

Usage: python -I 10_preview_candidates.py <build_dir> <out.jpg> "<ctbuh name>::<index>" ...
"""
import io
import json
import os
import sys
import time
import urllib.request

from PIL import Image, ImageDraw

UA = "paihangbang-research/0.1 (ranking-video image licensing check; python-urllib)"


def main(bdir, out, *specs):
    c = json.load(open(os.path.join(bdir, "candidates.json"), encoding="utf-8"))
    os.makedirs(os.path.join(bdir, "dl", "preview"), exist_ok=True)
    tiles = []
    for sp in specs:
        key, idx = sp.rsplit("::", 1)
        x = c[key][int(idx)]
        o = x["orig_url"].split("?")[0]
        name = o.rsplit("/", 1)[1]
        url = o.replace("/wikipedia/commons/", "/wikipedia/commons/thumb/") + f"/330px-{name}"
        for attempt in range(4):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA})
                raw = urllib.request.urlopen(req, timeout=60).read()
                break
            except Exception as e:  # noqa: BLE001
                print("retry", e, file=sys.stderr)
                time.sleep(15 * (attempt + 1))
        else:
            continue
        time.sleep(1.5)
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        im.thumbnail((260, 300))
        t = Image.new("RGB", (270, 330), "white")
        t.paste(im, ((270 - im.width) // 2, 5))
        ImageDraw.Draw(t).text((4, 312), f"{key[:28]}::{idx}", fill="black")
        tiles.append(t)
    cols = 5
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 270, rows * 330), "gray")
    for i, t in enumerate(tiles):
        sheet.paste(t, ((i % cols) * 270, (i // cols) * 330))
    sheet.save(out, quality=80)
    print(out, len(tiles))


if __name__ == "__main__":
    main(*sys.argv[1:])
