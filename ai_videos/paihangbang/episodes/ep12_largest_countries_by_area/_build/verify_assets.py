# -*- coding: utf-8 -*-
"""核对上屏图与 assets.json 的 source_url 是同一张图（重新下载 source_url，与本地文件比 32x32 灰度差）。"""
import io, json, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from PIL import Image, ImageOps
Image.MAX_IMAGE_PIXELS = None
EP = Path(__file__).resolve().parents[1]
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"}
def sig(im):
    im = ImageOps.exif_transpose(im).convert("L")
    return list(ImageOps.fit(im, (32, 32)).getdata()), im.size[0] / im.size[1]
def check(a):
    try:
        blob = urllib.request.urlopen(urllib.request.Request(a["source_url"], headers=UA), timeout=120).read()
        s1, r1 = sig(Image.open(io.BytesIO(blob)))
        s2, r2 = sig(Image.open(EP / a["file"]))
        diff = sum(abs(x - y) for x, y in zip(s1, s2)) / len(s1)
        return a["file"], round(diff, 1), round(r1, 2), round(r2, 2), a["author"][:24]
    except Exception as e:  # noqa: BLE001
        return a["file"], None, None, None, str(e)[:60]
assets = [a for a in json.load(open(EP / "assets.json", encoding="utf-8")) if not sys.argv[1:] or any(k in a["file"] for k in sys.argv[1:])]
bad = 0
with ThreadPoolExecutor(6) as ex:
    for f, diff, r1, r2, au in ex.map(check, assets):
        flag = "OK " if diff is not None and diff < 12 and abs(r1 - r2) < 0.03 else "CHK"
        bad += flag != "OK "
        print(flag, f, diff, r1, r2, au)
print("needs check:", bad)
