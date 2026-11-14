# -*- coding: utf-8 -*-
"""ep16 找图第二路（follow-up 023 / 追加要求 3）：Flickr 公开搜索页被限流后，改用 Bing 图片搜索（async 端点）。

    python _build/bing_search.py --only 10,11 --tag bA [--open]  [--extra "idx=查询;查询"]

- 默认带 Bing「可商用」许可过滤（filterui:license-L2_L3_L4）。结果里：
  * Flickr 照片页 → 打开照片页核对许可代码（只收 CC BY / BY-SA / CC0 / PDM / US Gov）、作者，取 k(2048)/o/h 直链；
  * Pexels / Unsplash / Pixabay → 照站方许可（Unsplash+ / premium 链接排除）；
  * 维基 / 维基共享资源一律跳过（follow-up 009）；其他站点不收（许可不明）。
- --open：放开许可过滤（追加要求 3），收任何站点的原图链接，licence 记 "unknown"（之后 apply 会标 image_risk = licence unknown）。
  图库水印站（getty / shutterstock / alamy / dreamstime / istock / 123rf / depositphotos / adobe stock）排除。
输出 _build/reselect/claude_bing_<tag>.json（image_reselect 同 schema）。"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import urllib.parse
from pathlib import Path

B = Path(__file__).resolve().parent
EP = B.parent
sys.path.insert(0, str(B))
from flickr_search import LIC, fetch  # noqa: E402
from img_queries import Q  # noqa: E402

STOCK = ("gettyimages", "shutterstock", "alamy", "dreamstime", "istockphoto", "123rf", "depositphotos", "stock.adobe", "agefotostock",
         "pond5", "vecteezy", "freepik", "wikipedia.org", "wikimedia.org", "pinterest", "facebook", "instagram", "x.com", "twitter")


def bing(q: str, open_: bool) -> list[dict]:
    p = {"q": q, "first": "0", "count": "50", "mmasync": "1"}
    if not open_:
        p["qft"] = "+filterui:license-L2_L3_L4"
    t = fetch("https://www.bing.com/images/async?" + urllib.parse.urlencode(p))
    out = []
    for m in re.findall(r'm="(\{[^"]+\})"', t):
        try:
            out.append(json.loads(html.unescape(m)))
        except Exception:  # noqa: BLE001
            pass
    return out


def flickr_photo(purl: str) -> dict | None:
    m = re.search(r"flickr\.com/photos/([^/]+)/(\d+)", purl)
    if not m:
        return None
    t = fetch(f"https://www.flickr.com/photos/{m.group(1)}/{m.group(2)}/")
    lic = re.search(r'"license":(\d+)', t)
    if not lic or int(lic.group(1)) not in LIC:
        return None
    best = None
    for key in ("k", "o", "h", "l"):
        s = re.search(r'"%s":\{"data":\{"displayUrl":"([^"]+)","width":(\d+),"height":(\d+)' % key, t)
        if s and not (key == "o" and max(int(s.group(2)), int(s.group(3))) > 6000):
            best = ("https:" + s.group(1).replace("\\/", "/"), int(s.group(2)), int(s.group(3)))
            break
    if not best:
        return None
    rn = re.search(r'"realname":"([^"]*)"', t)
    un = re.search(r'"username":"([^"]*)"', t)
    title = re.search(r'<meta property="og:title" content="([^"]*)"', t)
    author = (rn.group(1) if rn and rn.group(1) else (un.group(1) if un else "unknown"))
    return {"image_url": best[0], "page_url": f"https://www.flickr.com/photos/{m.group(1)}/{m.group(2)}/", "source": "Flickr",
            "author": html.unescape(author.encode().decode("unicode_escape", "ignore") if "\\u" in author else author),
            "licence": LIC[int(lic.group(1))], "why": f"{html.unescape(title.group(1) if title else '')[:80]} ({best[1]}x{best[2]})"}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--open", action="store_true")
    ap.add_argument("--extra", nargs="*", default=[])
    ap.add_argument("--max", type=int, default=8)
    ap.add_argument("--notoken", default="")
    ap.add_argument("--prefix", default="", help="输出文件名前缀（如 zalt），保证排序在已有候选之后")
    a = ap.parse_args()
    data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    only = {int(x) for x in a.only.split(",") if x}
    extra = {int(e.split("=", 1)[0]): e.split("=", 1)[1].split(";") for e in a.extra}
    notoken = {int(x) for x in a.notoken.split(",") if x}
    items = []
    for i, it in enumerate(data["items"]):
        if i not in only:
            continue
        _, queries, tokens = Q[it["slug"]]
        queries = extra.get(i, queries)
        key = f"{i:02d}_{Path(it['image']).stem}"
        seen, imgs = set(), []
        for q in queries:
            for r in bing(q, a.open):
                purl, murl = r.get("purl", ""), r.get("murl", "")
                if not murl or murl in seen or any(s in purl or s in murl for s in STOCK):
                    continue
                seen.add(murl)
                text = (r.get("t", "") + " " + r.get("desc", "") + " " + purl).lower()
                if i not in notoken and not any(tok in text for tok in tokens):
                    continue
                if "flickr.com/photos/" in purl:
                    c = flickr_photo(purl)
                    if c and c["image_url"] not in {x["image_url"] for x in imgs}:
                        imgs.append(c)
                elif "pexels.com" in purl:
                    imgs.append({"image_url": murl, "page_url": purl, "source": "Pexels", "author": "", "licence": "Pexels License", "why": r.get("t", "")[:80]})
                elif "unsplash.com" in purl and "plus.unsplash" not in murl and "premium" not in murl:
                    imgs.append({"image_url": murl, "page_url": purl, "source": "Unsplash", "author": "", "licence": "Unsplash License", "why": r.get("t", "")[:80]})
                elif "pixabay.com" in purl:
                    imgs.append({"image_url": murl, "page_url": purl, "source": "Pixabay", "author": "", "licence": "Pixabay Content License", "why": r.get("t", "")[:80]})
                elif a.open:
                    imgs.append({"image_url": murl, "page_url": purl, "source": urllib.parse.urlparse(purl).netloc, "author": "",
                                 "licence": "unknown", "why": r.get("t", "")[:80]})
                if len(imgs) >= a.max:
                    break
            if len(imgs) >= a.max:
                break
        print(f"{key}: {len(imgs)}", flush=True)
        items.append({"key": key, "images": imgs})
    dst = B / "reselect" / (f"claude_{a.prefix}_{a.tag}.json" if a.prefix else f"claude_zopen_{a.tag}.json" if a.open else f"claude_bing_{a.tag}.json")  # 新文件名排序在后，不打乱已下载候选的编号
    dst.write_text(json.dumps({"items": items}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", dst)


if __name__ == "__main__":
    main()
