# -*- coding: utf-8 -*-
"""ep16 自己找图（follow-up 023：不用 Codex）：Flickr 公开搜索页，只取可商用许可，按辨认词过滤，
再打开每张候选的照片页取大图直链（k 2048 / h 1600 / o），写 _build/reselect/claude_flickr_<批>.json（image_reselect 同一 schema）。

    python _build/flickr_search.py [--only idx,idx] [--tag b2] [--extra "idx=query;query"]

许可代码（flickr.com/services/api/flickr.photos.licenses.getInfo）：4 CC BY 2.0、5 CC BY-SA 2.0、9 CC0、10 PDM、11 CC BY 4.0、12 CC BY-SA 4.0、8 US Gov。
NC / ND / All rights reserved 不搜。"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

B = Path(__file__).resolve().parent
EP = B.parent
sys.path.insert(0, str(B))
from img_queries import Q  # noqa: E402

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"}
LIC = {4: "CC BY 2.0", 5: "CC BY-SA 2.0", 8: "Public domain (US Government work)", 9: "CC0 1.0", 10: "Public domain (Public Domain Mark 1.0)",
       11: "CC BY 4.0", 12: "CC BY-SA 4.0"}
_last = [0.0]


def fetch(url: str) -> str:
    wait = 3.0 - (time.monotonic() - _last[0])          # QC 轮：Flickr 单线程、间隔 ≥ 3 s
    if wait > 0:
        time.sleep(wait)
    for k in range(3):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read().decode("utf-8", "replace")
            _last[0] = time.monotonic()
            return r
        except Exception as e:  # noqa: BLE001
            print("  retry", k, e, flush=True)
            time.sleep(5 * (k + 1))
    return ""


def models(t: str, registry: str) -> list[dict]:
    dec, out = json.JSONDecoder(), []
    for m in re.finditer(re.escape(f'"_flickrModelRegistry":"{registry}"'), t):
        st = t.rfind('{"data":', 0, m.start())
        try:
            obj, _ = dec.raw_decode(t[st:])
            out.append(obj["data"])
        except Exception:  # noqa: BLE001
            pass
    return out


def search(q: str) -> list[dict]:
    url = "https://www.flickr.com/search/?" + urllib.parse.urlencode({"text": q, "license": ",".join(map(str, LIC)), "sort": "relevance"})
    return models(fetch(url), "photo-lite-models")


def biggest(nsid: str, pid: str) -> tuple[str, int, int] | None:
    t = fetch(f"https://www.flickr.com/photos/{nsid}/{pid}/")
    best = None
    for key in ("k", "o", "h", "l"):          # k(2048) 优先：够满版卡用、下载快
        m = re.search(r'"%s":\{"data":\{"displayUrl":"([^"]+)","width":(\d+),"height":(\d+)' % key, t)
        if m:
            w, h = int(m.group(2)), int(m.group(3))
            if key == "o" and max(w, h) > 6000:
                continue                         # 原图过大就退到 k
            best = ("https:" + m.group(1).replace("\\/", "/"), w, h)
            break
    return best


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--tag", default="b1")
    ap.add_argument("--extra", nargs="*", default=[], help="idx=查询1;查询2（替换该项默认查询）")
    ap.add_argument("--max", type=int, default=10)
    ap.add_argument("--notoken", default="", help="这些 idx 不做辨认词过滤")
    ap.add_argument("--prefix", default="flickr", help="输出名 claude_<prefix>_<tag>.json；补搜用 zz… 保证排在已下载候选之后")
    a = ap.parse_args()
    data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    only = {int(x) for x in a.only.split(",") if x}
    extra = {}
    for e in a.extra:
        i, qs = e.split("=", 1)
        extra[int(i)] = qs.split(";")
    notoken = {int(x) for x in a.notoken.split(",") if x}
    out_items = []
    for i, it in enumerate(data["items"]):
        if only and i not in only:
            continue
        hint, queries, tokens = Q[it["slug"]]
        queries = extra.get(i, queries)
        key = f"{i:02d}_{Path(it['image']).stem}"
        seen, cands = set(), []
        for q in queries:
            for p in search(q):
                pid = str(p.get("id"))
                if pid in seen or p.get("license") not in LIC:
                    continue
                seen.add(pid)
                text = " ".join(str(p.get(k) or "") for k in ("title", "description")).lower()
                if i not in notoken and not any(tok in text for tok in tokens):
                    continue
                cands.append(p)
        print(f"{key}: {len(cands)} matching", flush=True)
        images = []
        for p in cands[: a.max]:
            nsid, pid = p.get("ownerNsid"), str(p.get("id"))
            big = biggest(nsid, pid)
            if not big:
                continue
            url, w, h = big
            author = html.unescape(p.get("realname") or p.get("username") or "unknown")
            images.append({"image_url": url, "page_url": f"https://www.flickr.com/photos/{p.get('pathAlias') or nsid}/{pid}/",
                           "source": "Flickr", "author": author, "licence": LIC[p["license"]],
                           "why": f"{html.unescape(p.get('title') or '')[:80]} ({w}x{h})"})
        out_items.append({"key": key, "images": images})
    dst = B / "reselect" / f"claude_{a.prefix}_{a.tag}.json"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps({"items": out_items}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", dst, sum(len(x["images"]) for x in out_items), "images")


if __name__ == "__main__":
    main()
