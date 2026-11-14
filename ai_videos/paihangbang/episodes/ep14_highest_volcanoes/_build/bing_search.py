# -*- coding: utf-8 -*-
"""追加要求 3：放开来源的全网检索（Bing 图片结果页的 murl 原图链接），许可一律 "unknown"（进风险版）。
排除图库水印站、Pinterest、维基、YouTube 缩略图；标题或来源页须含火山名关键词。
写 _build/reselect/claude_bing_<批>.json（与 codex 输出同 schema）。

    python _build/bing_search.py <batch_tag> <rank>:<query>[|<keyword>,<keyword>] ...
"""
import html
import json
import re
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

H = Path(__file__).resolve().parent
EP = H.parent
CURL = "C:/Program Files/Git/mingw64/bin/curl.exe"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"
BAD = ("getty", "shutterstock", "alamy", "dreamstime", "istock", "123rf", "depositphotos", "pinimg", "pinterest",
       "wikimedia", "wikipedia", "ytimg", "youtube", "fbcdn", "facebook", "instagram", "twimg", "agefotostock",
       "vecteezy", "freepik", "stock.adobe", "bigstock", "superstock", "tiktok")


def search(q: str) -> list[dict]:
    url = "https://www.bing.com/images/search?" + urllib.parse.urlencode({"q": q, "form": "HDRSC3", "first": 1, "qft": "+filterui:imagesize-large"})
    s = subprocess.run([CURL, "-s", "-m", "60", "-H", "Accept-Language: en-US,en;q=0.9", "-A", UA, url], capture_output=True).stdout.decode("utf-8", "replace")
    out = []
    for m in re.findall(r'class="iusc"[^>]*m="([^"]+)"', s):
        try:
            d = json.loads(html.unescape(m))
        except Exception:  # noqa: BLE001
            continue
        out.append({"murl": d.get("murl", ""), "purl": d.get("purl", ""), "t": d.get("t", "")})
    return out


def main() -> None:
    tag = sys.argv[1]
    data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    res = []
    for arg in sys.argv[2:]:
        rank, _, rest = arg.partition(":")
        q, _, kws = rest.partition("|")
        i, it = next((i, it) for i, it in enumerate(data["items"]) if it["rank"] == int(rank))
        keys = [k.strip().lower() for k in (kws or it["name"]).split(",")]
        found = search(q)
        time.sleep(2)
        imgs, seen = [], set()
        for f in found:
            low = (f["murl"] + " " + f["purl"]).lower()
            txt = (f["t"] + " " + f["purl"] + " " + f["murl"]).lower()
            if not f["murl"].startswith("http") or any(b in low for b in BAD) or f["murl"] in seen:
                continue
            if not any(k in txt for k in keys):
                continue
            seen.add(f["murl"])
            host = urllib.parse.urlparse(f["purl"]).netloc
            imgs.append({"image_url": f["murl"], "page_url": f["purl"], "source": host, "author": "unknown",
                         "licence": "unknown", "why": f"Bing image search '{q}': {f['t'][:90]}"})
        res.append({"key": f"{i:02d}_{Path(it['image']).stem}", "images": imgs[:8]})
        print(rank, it["name"], len(imgs), [x["source"] for x in imgs[:8]], flush=True)
    (H / "reselect" / f"claude_bing_{tag}.json").write_text(json.dumps({"items": res}, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
