# -*- coding: utf-8 -*-
"""把人眼从拼图里挑出的候选（PICKS）解析成大图直链，写 _build/reselect/claude_b01.json（image_reselect download 读取）。
PICKS: key -> [(轮次, 序号, 说明)]；轮次 "" = find/<key>.json，"_r2" = find/<key>_r2.json。第一项是首选。
"""
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIND = HERE / "find"
OUT = HERE / "reselect"
OUT.mkdir(exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"}
sys.path.insert(0, str(HERE))
from picks import PICKS  # noqa: E402

CACHE = HERE / "find" / "large_cache.json"
cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}


def large(page_url: str, fallback: str) -> tuple[str, int, int]:
    if page_url in cache:
        return tuple(cache[page_url])
    try:
        s = urllib.request.urlopen(urllib.request.Request(page_url, headers=UA), timeout=40).read().decode("utf-8", "replace")
    except Exception as e:  # noqa: BLE001
        print("  page ERR", page_url, e)
        return fallback, 0, 0
    sizes = {}
    for m in re.finditer(r'"(\w{1,2})":\{"data":\{"displayUrl":"([^"]+)","width":(\d+),"height":(\d+)', s):
        sizes[m.group(1)] = ("https:" + m.group(2).replace("\\/", "/"), int(m.group(3)), int(m.group(4)))
    for k in ("k", "3k", "h", "o", "l", "c"):
        if k in sizes and (k != "o" or max(sizes[k][1], sizes[k][2]) <= 6500):
            cache[page_url] = sizes[k]
            CACHE.write_text(json.dumps(cache, indent=1), encoding="utf-8")
            time.sleep(0.6)
            return sizes[k]
    return fallback, 0, 0


items = []
for key, picks in PICKS.items():
    imgs = []
    for rnd, idx, why in picks:
        cands = json.loads((FIND / f"{key}{rnd}.json").read_text(encoding="utf-8"))["cands"]
        c = cands[idx]
        url, w, h = (large(c["page_url"], c["image_url"]) if c["source"] == "Flickr" else (c["image_url"], c["w"], c["h"]))
        imgs.append({"image_url": url, "page_url": c["page_url"], "source": c["source"], "author": c["author"] or "Flickr user",
                     "licence": c["licence"], "why": f"{why} [{c['title'][:60]}] {w}x{h}"})
        print(key, rnd or "r1", idx, w, h, c["licence"], c["author"])
    items.append({"key": key, "images": imgs})
(OUT / "claude_b01.json").write_text(json.dumps({"items": items}, ensure_ascii=False, indent=1), encoding="utf-8")
print("written", len(items))
