# -*- coding: utf-8 -*-
"""follow-up 023：Claude 自己找图——Flickr 公开搜索页（只取可商用许可：CC BY / CC BY-SA 2.0 & 4.0、CC0、PDM），
不调 Codex、不用 API key。每项用英文名 + 当地名称各搜一次，再打开候选的照片页取最大尺寸直链。
输出 _build/reselect/claude_flickr.json（与 codex 输出同 schema，key = 图片文件名 stem）。

    python flickr_search.py [idx,idx,...]
"""
from __future__ import annotations

import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
EP = BUILD.parent
sys.path.insert(0, str(BUILD))
from hints import LOCAL  # noqa: E402

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"}
LIC = {"4": "CC BY 2.0", "5": "CC BY-SA 2.0", "9": "CC0 1.0", "10": "Public Domain Mark 1.0",
       "11": "CC BY 4.0", "12": "CC BY-SA 4.0"}
QUERIES = json.loads((BUILD / "flickr_queries.json").read_text(encoding="utf-8")) if (BUILD / "flickr_queries.json").exists() else {}
SIZE_ORDER = ["o", "6k", "5k", "4k", "3k", "k", "h", "l", "c"]


def get(url: str) -> str:
    for a in range(2):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25).read().decode("utf-8", "replace")
        except Exception:  # noqa: BLE001
            time.sleep(3)
    return ""


def search(text: str) -> list[dict]:
    url = "https://www.flickr.com/search/?" + urllib.parse.urlencode({"text": text, "license": ",".join(LIC)})
    t = get(url)
    out = []
    # 每个照片模型：... "pathAlias":..,"username":..,"realname":..,"ownerNsid":..,"title":..,"license":N, ... "id":"123"
    for m in re.finditer(r'"pathAlias":("[^"]*"|null),"username":"([^"]*)","realname":"([^"]*)","ownerNsid":"([^"]+)".{0,400}?"title":"((?:[^"\\]|\\.)*)".{0,3000}?"license":(\d+),"sizes"(.{0,6000}?)"id":"(\d+)"\}', t):
        alias, user, real, nsid, title, lic, sizes, pid = m.groups()
        if lic not in LIC:
            continue
        owner = json.loads(alias) or nsid
        out.append({"id": pid, "owner": owner, "author": json.loads(f'"{real}"') or json.loads(f'"{user}"'),
                    "title": json.loads(f'"{title}"'), "licence": LIC[lic],
                    "page_url": f"https://www.flickr.com/photos/{owner}/{pid}/"})
    return out


def largest(c: dict) -> tuple[str, int, int] | None:
    t = get(c["page_url"])
    best = None
    for key in SIZE_ORDER:
        m = re.search(r'"' + re.escape(key) + r'":\{"data":\{"displayUrl":"([^"]+)","width":(\d+),"height":(\d+)', t)
        if m:
            best = ("https:" + m.group(1).replace("\\/", "/"), int(m.group(2)), int(m.group(3)))
            break
    if not best:
        m = re.search(r'(//live\.staticflickr\.com/[^"\\]+_[kbh]\.jpg)', t.replace("\\/", "/"))
        if m:
            best = ("https:" + m.group(1), 0, 0)
    return best


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    only = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else None
    outp = BUILD / "reselect" / f"claude_flickr{sys.argv[2] if len(sys.argv) > 2 else ''}.json"
    res = json.loads(outp.read_text(encoding="utf-8")) if outp.exists() else {"items": []}
    done = {r["key"] for r in res["items"]}
    for i, it in enumerate(data["items"]):
        key = Path(it["image"]).stem
        if (only is not None and i not in only) or key in done:
            continue
        queries = QUERIES.get(it["name"]) or [it["name"]]
        seen, cands = set(), []
        for q in queries:
            for c in search(q):
                if c["id"] not in seen:
                    seen.add(c["id"])
                    cands.append(c)
            time.sleep(2)
        images = []
        words = [w.lower() for q in queries for w in re.findall(r"\w{4,}", q)]
        rel = [c for c in cands if any(w in c["title"].lower() for w in words)] or cands
        for c in rel[:8]:
            big = largest(c)
            time.sleep(1.5)
            if not big:
                continue
            images.append({"image_url": big[0], "page_url": c["page_url"], "source": "Flickr", "author": c["author"],
                           "licence": c["licence"], "why": f"Flickr '{c['title'][:60]}' {big[1]}x{big[2]}"})
        res["items"].append({"key": key, "images": images})
        outp.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{key}: {len(cands)} found, {len(images)} kept", flush=True)


if __name__ == "__main__":
    main()
