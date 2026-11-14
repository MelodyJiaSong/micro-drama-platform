# -*- coding: utf-8 -*-
"""follow-up 023：Claude 自己找图——Flickr 网页搜索（许可过滤只留可商用：CC BY / CC BY-SA / CC0 / PDM），
解析搜索页内嵌的 photo-lite-models，按标题 / 描述含火山名过滤，写 _build/reselect/claude_flickr_<批>.json（与 codex 输出同 schema）。

    python _build/flickr_search.py <batch_tag> <rank>[:query1|query2] ...
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

H = Path(__file__).resolve().parent
EP = H.parent
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"}
LIC = {4: "CC BY 2.0", 5: "CC BY-SA 2.0", 9: "CC0 1.0", 10: "Public Domain Mark 1.0", 11: "CC BY 4.0", 12: "CC BY-SA 4.0"}
SIZE_ORDER = ["o", "6k", "5k", "4k", "3k", "k", "h", "l", "c", "b"]


def fetch(q: str) -> list[dict]:
    url = "https://www.flickr.com/search/?" + urllib.parse.urlencode({"text": q, "license": ",".join(map(str, LIC)), "sort": "relevance"})
    s = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25).read().decode("utf-8", "replace")
    m = re.search(r'"search-photos-lite-models":\[(\{.*?\})\],"', s)
    out = []
    # 逐个 photo-lite-models 对象用括号配对切出来
    for st in [x.start() for x in re.finditer(r'\{"data":\{"_flickrModelRegistry":"photo-lite-models"', s)]:
        depth, i = 0, st
        while i < len(s):
            c = s[i]
            if c == "{": depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0: break
            elif c == '"':
                i += 1
                while s[i] != '"':
                    i += 2 if s[i] == "\\" else 1
            i += 1
        try:
            d = json.loads(s[st:i + 1])["data"]
        except Exception:  # noqa: BLE001
            continue
        sizes = d.get("sizes", {}).get("data", {})
        best = next((k for k in SIZE_ORDER if k in sizes), None)
        if not best:
            continue
        sd = sizes[best]["data"]
        out.append({"id": d.get("id"), "owner": d.get("ownerNsid"), "author": d.get("realname") or d.get("username") or "",
                    "title": d.get("title", ""), "desc": d.get("description", ""), "license": d.get("license"),
                    "url": "https:" + sd["url"].replace("\\/", "/"), "w": sd.get("width"), "h": sd.get("height"),
                    "page": f"https://www.flickr.com/photos/{d.get('pathAlias') or d.get('ownerNsid')}/{d.get('id')}/"})
    return out


def resolve(page: str) -> dict:
    """照片页：取最大可用尺寸（≤ 4096）与页面上的许可编号。"""
    s = urllib.request.urlopen(urllib.request.Request(page, headers=UA), timeout=25).read().decode("utf-8", "replace")
    best = None
    for k, u, w, h in re.findall(r'"(\w+)":\{"data":\{"displayUrl":"([^"]+)","width":(\d+),"height":(\d+)', s):
        w, h = int(w), int(h)
        if max(w, h) <= 4096 and (best is None or w * h > best[1] * best[2]):
            best = ("https:" + u.replace("\/", "/"), w, h)
    lic = re.search(r'"license":(\d+)', s)
    out = {"license": int(lic.group(1))} if lic else {}
    if best:
        out.update({"url": best[0], "w": best[1], "h": best[2]})
    return out


def main() -> None:
    tag = sys.argv[1]
    data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    res = []
    for arg in sys.argv[2:]:
        rank, _, qs = arg.partition(":")
        i, it = next((i, it) for i, it in enumerate(data["items"]) if it["rank"] == int(rank))
        queries = qs.split("|") if qs else [it["name"], f"volcan {it['name']}"]
        must = [w.lower() for w in re.split(r"[ |]", (qs or it["name"])) if len(w) > 3 and w.lower() not in ("volcan", "volcano", "volcán", "mount", "cerro", "nevado", "nevados", "sierra")]
        seen, imgs = set(), []
        for q in queries:
            try:
                found = fetch(q)
            except Exception as e:  # noqa: BLE001
                print("ERR", q, e); found = []
            time.sleep(3)
            for f in found:
                if f["id"] in seen or f["license"] not in LIC:
                    continue
                txt = (f["title"] + " " + f["desc"]).lower()
                if must and not any(m_ in txt for m_ in must):
                    continue
                seen.add(f["id"])
                imgs.append(f)
        imgs = imgs[:9]
        for f in imgs:
            try:
                f.update(resolve(f["page"]))
            except Exception as e:  # noqa: BLE001
                print("resolve ERR", f["page"], e)
            time.sleep(3)
        imgs = [f for f in imgs if f["license"] in LIC]
        imgs.sort(key=lambda f: -(min(f["w"] or 0, f["h"] or 0)))
        stem = Path(it["image"]).stem
        key = f"{i:02d}_{stem}"
        res.append({"key": key, "images": [{"image_url": f["url"], "page_url": f["page"], "source": "Flickr", "author": f["author"],
                                            "licence": LIC[f["license"]], "why": f"Flickr search '{queries[0]}': {f['title'][:80]} ({f['w']}x{f['h']})"}
                                           for f in imgs[:10]]})
        (H / "reselect" / f"claude_flickr_{tag}.json").write_text(json.dumps({"items": res}, ensure_ascii=False, indent=1), encoding="utf-8")
        print(rank, it["name"], len(imgs), [(f["w"], f["h"], f["title"][:30]) for f in imgs[:10]], flush=True)
    (H / "reselect" / f"claude_flickr_{tag}.json").write_text(json.dumps({"items": res}, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
