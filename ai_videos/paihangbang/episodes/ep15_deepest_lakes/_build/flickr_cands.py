# -*- coding: utf-8 -*-
"""follow-up 023：Claude 自己找图（不走 Codex）。Flickr 站内搜索（只要可商用许可：CC BY / CC BY-SA / CC0 / PDM），
逐张打开照片页读标题、作者、许可与最大尺寸直链，输出与 codex 同 schema 的候选。

    python flickr_cands.py "<key>" "<query>" [--max 10] [--page-cache raw/pages]
结果追加到 _build/reselect/claude_flickr.json（同 key 去重）。
"""
import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
OUT = HERE / "reselect" / "claude_flickr.json"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"}
LIC = {"4": "CC BY 2.0", "5": "CC BY-SA 2.0", "9": "CC0 1.0", "10": "Public domain (PDM)"}
SIZES = ["o", "6k", "5k", "4k", "3k", "k", "h", "l", "c", "b"]


def get(url: str) -> str:
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read().decode("utf-8", "replace")


def photo_info(pid: str) -> dict | None:
    cache = HERE / "raw" / "pages" / f"flickr_{pid}.html"
    if not cache.exists():
        cache.write_text(get(f"https://www.flickr.com/photo.gne?id={pid}"), encoding="utf-8")
        time.sleep(0.6)
    t = cache.read_text(encoding="utf-8")
    m = re.search(r'<meta property="og:url" content="([^"]+)"', t)
    page = m.group(1) if m else f"https://www.flickr.com/photo.gne?id={pid}"
    title = (re.search(r'<meta property="og:title" content="([^"]*)"', t) or [None, ""])[1]
    desc = (re.search(r'<meta property="og:description" content="([^"]*)"', t) or [None, ""])[1]
    lic = re.findall(r'"license":"?(\d+)', t)
    lic = lic[0] if lic else ""
    real = (re.search(r'"realname":"([^"]*)"', t) or [None, ""])[1]
    user = (re.search(r'"username":"([^"]*)"', t) or [None, ""])[1]
    m = re.search(r'"sizes":\{(.*?)\}\}', t)
    best = None
    if m:
        blob = m.group(0)
        for key in SIZES:
            mm = re.search(r'"' + key + r'":\{"displayUrl":"([^"]+)","width":"?(\d+)"?,"height":"?(\d+)"?', blob)
            if mm:
                best = ("https:" + mm.group(1).replace("\\/", "/"), int(mm.group(2)), int(mm.group(3)), key)
                break
    if lic not in LIC or not best:
        return None
    return {"image_url": best[0], "page_url": page, "source": "Flickr", "author": real or user,
            "licence": LIC[lic], "why": f"Flickr '{title}' ({best[1]}x{best[2]}, size {best[3]}); {desc[:120]}"}


def search(query: str) -> list[str]:
    url = "https://www.flickr.com/search/?" + urllib.parse.urlencode({"text": query, "license": "4,5,9,10", "media": "photos"}, quote_via=urllib.parse.quote)
    import subprocess  # urllib 拿到的搜索页常缺结果 JSON，curl 稳定
    t = subprocess.run(["curl", "-sL", "-A", UA["User-Agent"], url], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    ids = re.findall(r'"id":"(\d{8,12})"', t) + re.findall(r'live\.staticflickr\.com\\?/\d+\\?/(\d{8,12})_', t)
    return list(dict.fromkeys(ids))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("key")
    ap.add_argument("query")
    ap.add_argument("--max", type=int, default=10)
    a = ap.parse_args()
    (HERE / "raw" / "pages").mkdir(parents=True, exist_ok=True)
    ids = search(a.query)
    found = []
    for pid in ids[: a.max * 2]:
        try:
            info = photo_info(pid)
        except Exception as e:  # noqa: BLE001
            print("  fail", pid, e)
            continue
        if info:
            found.append(info)
            print("  +", pid, info["licence"], "|", info["why"][:110])
        if len(found) >= a.max:
            break
    data = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {"items": []}
    row = next((r for r in data["items"] if r["key"] == a.key), None)
    if not row:
        row = {"key": a.key, "images": []}
        data["items"].append(row)
    have = {i["image_url"] for i in row["images"]}
    row["images"] += [f for f in found if f["image_url"] not in have]
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(a.key, "ids", len(ids), "added", len([f for f in found if f["image_url"] not in have]), "total", len(row["images"]))


if __name__ == "__main__":
    main()
