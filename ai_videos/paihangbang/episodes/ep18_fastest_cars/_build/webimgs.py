# -*- coding: utf-8 -*-
"""放开来源的全网图（追加要求 3）：抓页面 og:image 与正文大图链接，下载到 find/web/<key>/，出拼图供人眼看。
python _build/webimgs.py <key> <page_url> [<page_url> ...]
"""
import io
import json
import re
import sys
import subprocess
import urllib.parse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"


def curl(url, binary=False):
    r = subprocess.run(["curl", "-sL", "-m", "40", "-A", UA, "-H", "Accept-Language: en", url], capture_output=True)
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")


key, pages = sys.argv[1], sys.argv[2:]
out = HERE / "find" / "web" / key
out.mkdir(parents=True, exist_ok=True)
metaf = out / "meta.json"
meta = json.loads(metaf.read_text(encoding="utf-8")) if metaf.exists() else []
seen = {m["image_url"] for m in meta}
for page in pages:
    s = curl(page)
    urls = re.findall(r'<meta[^>]+property=["\']og:image(?::url)?["\'][^>]+content=["\']([^"\']+)', s)
    urls += re.findall(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image', s)
    urls += re.findall(r'(?:src|data-src|href|data-lazy-src)=["\']([^"\']+\.(?:jpe?g|webp|png)(?:\?[^"\']*)?)["\']', s, re.I)
    for u in urls:
        u = urllib.parse.urljoin(page, u.replace("&amp;", "&"))
        if u in seen or any(x in u.lower() for x in ("logo", "icon", "avatar", "sprite", "favicon")):
            continue
        seen.add(u)
        b = curl(u, binary=True)
        try:
            im = Image.open(io.BytesIO(b))
            w, h = im.size
        except Exception:  # noqa: BLE001
            continue
        if min(w, h) < 500:
            continue
        n = len(meta)
        ext = (im.format or "jpg").lower().replace("jpeg", "jpg")
        f = out / f"w{n}.{ext}"
        f.write_bytes(b)
        meta.append({"id": f"w{n}", "file": f.name, "image_url": u, "page_url": page, "w": w, "h": h})
        print(f"w{n} {w}x{h} {u[:110]}")
metaf.write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
# 拼图
TW, TH, cols = 300, 200, 5
rows = max(1, (len(meta) + cols - 1) // cols)
sheet = Image.new("RGB", (cols * (TW + 6) + 6, rows * (TH + 24) + 8), (20, 20, 24))
dr = ImageDraw.Draw(sheet)
fnt = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 13)
for n, m in enumerate(meta):
    x, y = 6 + (n % cols) * (TW + 6), 6 + (n // cols) * (TH + 24)
    try:
        with Image.open(out / m["file"]) as im:
            sheet.paste(ImageOps.contain(im.convert("RGB"), (TW, TH)), (x, y))
    except Exception:  # noqa: BLE001
        pass
    dr.text((x, y + TH + 2), f"{m['id']} {m['w']}x{m['h']} {urllib.parse.urlparse(m['page_url']).netloc[:28]}", font=fnt, fill=(220, 220, 220))
sheet.save(out / "sheet.jpg", quality=85)
print("sheet", out / "sheet.jpg", len(meta))
