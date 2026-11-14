# -*- coding: utf-8 -*-
"""follow-up 023：Claude 自己找图——Pexels 网页搜索（Pexels License，可商用免署名），解析 __NEXT_DATA__，
按描述 / alt / 标签含火山名过滤，写 _build/reselect/claude_pexels_<批>.json（与 codex 输出同 schema）。

    python _build/pexels_search.py <batch_tag> <rank>[:query1|query2] ...
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
GENERIC = {"volcan", "volcano", "volcán", "mount", "cerro", "nevado", "nevados", "sierra", "pico"}


def search(q: str) -> list[dict]:
    url = f"https://www.pexels.com/search/{urllib.parse.quote(q)}/"
    import subprocess   # urllib 被 Pexels 403，curl 可以
    s = subprocess.run(["C:/Program Files/Git/mingw64/bin/curl.exe", "-s", "-L", "-m", "60", "-A", UA["User-Agent"], url], capture_output=True).stdout.decode("utf-8", "replace")
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', s, re.S)
    if not m:
        return []
    d = json.loads(m.group(1))
    out = []
    for x in d["props"]["pageProps"].get("initialData", {}).get("data", []):
        a = x.get("attributes", {})
        if x.get("type") != "photo" or not a.get("image"):
            continue
        tags = " ".join(t.get("name", "") for t in a.get("tags", []) or [])
        loc = json.dumps(a.get("location") or "", ensure_ascii=False)
        user = a.get("user") or {}
        name = " ".join(filter(None, [user.get("first_name"), user.get("last_name")])) or user.get("username", "")
        out.append({"id": a["id"], "text": " ".join(filter(None, [a.get("title"), a.get("description"), a.get("alt"), tags, loc])),
                    "w": a.get("width"), "h": a.get("height"), "author": name,
                    "url": f"https://images.pexels.com/photos/{a['id']}/pexels-photo-{a['id']}.jpeg?auto=compress&cs=tinysrgb&w=3000",
                    "page": f"https://www.pexels.com/photo/{a.get('slug', '')}-{a['id']}/", "title": a.get("alt") or a.get("title") or ""})
    return out


def main() -> None:
    tag = sys.argv[1]
    data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    res = []
    for arg in sys.argv[2:]:
        rank, _, qs = arg.partition(":")
        i, it = next((i, it) for i, it in enumerate(data["items"]) if it["rank"] == int(rank))
        queries = qs.split("|") if qs else [it["name"]]
        must = {w.lower() for w in re.split(r"[ |]", qs or it["name"]) if len(w) > 3 and w.lower() not in GENERIC}
        seen, imgs = set(), []
        for q in queries:
            try:
                found = search(q)
            except Exception as e:  # noqa: BLE001
                print("ERR", q, e); found = []
            time.sleep(2)
            for f in found:
                if f["id"] in seen or (must and not any(m_ in f["text"].lower() for m_ in must)):
                    continue
                seen.add(f["id"]); imgs.append(f)
        res.append({"key": f"{i:02d}_{Path(it['image']).stem}",
                    "images": [{"image_url": f["url"], "page_url": f["page"], "source": "Pexels", "author": f["author"],
                                "licence": "Pexels License", "why": f"Pexels search '{queries[0]}': {f['title'][:90]} ({f['w']}x{f['h']})"}
                               for f in imgs[:10]]})
        print(rank, it["name"], len(imgs), [f["title"][:40] for f in imgs[:8]], flush=True)
    (H / "reselect" / f"claude_pexels_{tag}.json").write_text(json.dumps({"items": res}, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
