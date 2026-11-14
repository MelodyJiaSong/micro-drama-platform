# -*- coding: utf-8 -*-
"""Flickr 照片页 → 可下载的最大尺寸直链（o/6k/5k/4k/3k/k/h，照片页里公开给出的）。
python -I flickr_big.py <photo_page_url> ... → 打印 宽x高 url 与许可 id"""
import re
import sys
import time
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"}


def best(page: str) -> tuple[int, int, str, str]:
    t = urllib.request.urlopen(urllib.request.Request(page, headers=UA), timeout=60).read().decode("utf-8", "replace")
    pid = re.search(r"/(\d{6,})/?$", page.rstrip("/") + "/").group(1) if re.search(r"/(\d{6,})/?$", page) else ""
    sizes = []
    for m in re.finditer(r'"displayUrl":"(\\/\\/live\.staticflickr\.com\\/[^"]+)","width":"?(\d+)"?,"height":"?(\d+)"?', t):
        u = "https:" + m.group(1).replace("\\/", "/")
        if pid and pid not in u:
            continue
        sizes.append((int(m.group(2)), int(m.group(3)), u))
    lic = re.search(r'"license":(\d+)', t)
    if not sizes:
        return 0, 0, "", lic.group(1) if lic else ""
    w, h, u = max(sizes)
    return w, h, u, lic.group(1) if lic else ""


if __name__ == "__main__":
    for p in sys.argv[1:]:
        try:
            w, h, u, lic = best(p)
            print(f"{w}x{h} lic={lic} {u}  <- {p}", flush=True)
        except Exception as e:  # noqa: BLE001
            print("ERR", p, e)
        time.sleep(1.5)
