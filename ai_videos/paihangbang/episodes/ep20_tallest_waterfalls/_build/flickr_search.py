# -*- coding: utf-8 -*-
"""follow-up 023：Claude 自己找图——Flickr 网页搜索（只取可商用许可），结果写 reselect/claude_flickr_<批>.json（与 codex 输出同 schema）。
用法：python -I flickr_search.py <批名> idx:必含词1,词2:query[|query2...] ...（标题须含任一必含词）
只读公开搜索页（与浏览器访问同），每次请求间隔 2 s；原始 HTML 存 raw/flickr/。
许可 id（Flickr）：4 CC BY 2.0、5 CC BY-SA 2.0、8 US Government Work、9 CC0、10 Public Domain Mark、11 CC BY 4.0、12 CC BY-SA 4.0。"""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
EP = HERE.parent
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"}
LIC = {4: "CC BY 2.0", 5: "CC BY-SA 2.0", 8: "Public domain (US Government Work)", 9: "CC0 1.0", 10: "Public Domain Mark 1.0",
       11: "CC BY 4.0", 12: "CC BY-SA 4.0"}
SIZE_ORDER = ["o", "6k", "5k", "4k", "3k", "k", "h", "l", "c", "z"]


def dec(x: str) -> str:
    try:
        return json.loads('"' + x + '"')
    except Exception:  # noqa: BLE001
        return x


def item_key(i: int, it: dict) -> str:
    return f"{i:02d}_{Path(it['image']).stem}"


def search(query: str) -> list[dict]:
    url = "https://www.flickr.com/search/?" + urllib.parse.urlencode({"text": query, "license": ",".join(map(str, LIC)), "sort": "relevance"})
    fn = HERE / "raw" / "flickr" / (re.sub(r"[^\w]+", "_", query)[:80] + ".html")
    if fn.exists():
        t = fn.read_text(encoding="utf-8", errors="replace")
    else:
        t = ""
        for k in range(3):
            try:
                t = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read().decode("utf-8", "replace")
                break
            except Exception as e:  # noqa: BLE001
                print("  retry", query, e, flush=True)
                time.sleep(5 * (k + 1))
        if not t:
            return []
        fn.write_text(t, encoding="utf-8")
        time.sleep(2)
    out = []
    for m in re.finditer(r'\{"data":\{"_flickrModelRegistry":"photo-lite-models",(.*?)"exportMetaType"', t):
        pass
    # 逐个 photo-lite 对象切片解析
    starts = [m.start() for m in re.finditer(r'"_flickrModelRegistry":"photo-lite-models"', t)]
    for k, s in enumerate(starts):
        chunk = t[s: starts[k + 1] if k + 1 < len(starts) else s + 20000]
        g = lambda pat: (re.search(pat, chunk) or [None, ""])[1]  # noqa: E731
        lic = g(r'"license":(\d+)')
        if not lic or int(lic) not in LIC:
            continue
        pid = g(r'"id":"(\d+)"')
        sizes = {}
        for sm in re.finditer(r'"([a-z0-9]{1,2})":\{"data":\{"displayUrl":"([^"]+)","width":(\d+),"height":(\d+)', chunk):
            sizes[sm.group(1)] = ("https:" + sm.group(2).replace("\\/", "/"), int(sm.group(3)), int(sm.group(4)))
        best = next((sizes[z] for z in SIZE_ORDER if z in sizes), None)
        if not best:
            continue
        owner = g(r'"pathAlias":"([^"]*)"') or g(r'"ownerNsid":"([^"]+)"')
        if not pid:
            mm = re.search(r"/(\d+)_[0-9a-f]+", best[0])
            pid = mm.group(1) if mm else ""
        name = g(r'"realname":"([^"]*)"') or g(r'"username":"([^"]*)"')
        title = g(r'"title":"([^"]*)"')
        out.append({"image_url": best[0], "page_url": f"https://www.flickr.com/photos/{owner}/{pid}/", "source": "Flickr",
                    "author": dec(name) if name else "unknown", "licence": LIC[int(lic)],
                    "why": f"Flickr '{dec(title)}' {best[1]}x{best[2]} (query: {query})",
                    "_w": best[1], "_h": best[2], "_title": dec(title)})
    return out


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    batch = sys.argv[1]
    data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    res = []
    args = sys.argv[2:]
    if len(args) == 1 and args[0].startswith("@"):
        args = [l.strip() for l in open(args[0][1:], encoding="utf-8") if l.strip()]
    for arg in args:
        idx, toks, qs = arg.split(":", 2)
        i = int(idx)
        toks = [x.lower() for x in toks.split(",") if x]
        seen, imgs = set(), []
        for q in qs.split("|"):
            for c in search(q):
                if c["page_url"] in seen or (toks and not any(tk in c["_title"].lower() for tk in toks)):
                    continue
                seen.add(c["page_url"])
                imgs.append(c)
        print(f"{i:02d} {data['items'][i]['name']}: {len(imgs)}")
        for c in imgs[:14]:
            print("    ", c["_w"], "x", c["_h"], c["licence"], "|", c["author"][:20], "|", c["why"][:90])
        res.append({"key": item_key(i, data["items"][i]), "images": [{k: v for k, v in c.items() if not k.startswith("_")} for c in imgs[:20]]})
    (HERE / "reselect" / f"claude_flickr_{batch}.json").write_text(json.dumps({"items": res}, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
