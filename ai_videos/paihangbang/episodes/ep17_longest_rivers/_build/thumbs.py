# -*- coding: utf-8 -*-
"""下载 Flickr 缩略图拼图：python thumbs.py <名> url1 url2 ...  → raw/flickr/<名>.jpg（每格标 photo id）"""
import re, sys, urllib.request, io
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
D = Path(__file__).parent / "raw" / "flickr"; D.mkdir(parents=True, exist_ok=True)
name, urls = sys.argv[1], sys.argv[2:]
T = 300; cols = 6
sheet = Image.new("RGB", (cols * (T + 6), ((len(urls) + cols - 1) // cols) * (T + 28)), (20, 20, 20))
dr = ImageDraw.Draw(sheet); f = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 16)
for i, u in enumerate(urls):
    pid = re.search(r"/(\d+)_", u).group(1)
    try:
        b = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36", "Referer": "https://www.flickr.com/", "Accept": "image/avif,image/webp,image/*,*/*"}), timeout=30).read()
        im = ImageOps.fit(Image.open(io.BytesIO(b)).convert("RGB"), (T, T))
    except Exception as e:  # noqa: BLE001
        im = Image.new("RGB", (T, T), (90, 0, 0))
    x, y = (i % cols) * (T + 6), (i // cols) * (T + 28)
    sheet.paste(im, (x, y)); dr.text((x + 4, y + T + 4), f"{i} {pid}", font=f, fill=(255, 255, 0))
sheet.save(D / f"{name}.jpg", quality=85); print(D / f"{name}.jpg")
