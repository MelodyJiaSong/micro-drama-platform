# -*- coding: utf-8 -*-
"""Claude 自己找图（follow-up 022）补充路：Openverse 公开 API（免 key，聚合 Flickr 等 CC 图），只要可商用许可，
排除维基共享资源（follow-up 009），下载并入 reselect/cand/<key>/meta.json（id 前缀 o）。另可走 iNaturalist 放宽检索（captive 任意、限地点）。
用法：python -I <本文件> "idx:query" [...] [--per 10]
"""
import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

EP = Path(__file__).resolve().parents[1]
CAND = EP / "_build" / "reselect" / "cand"
UA = {"User-Agent": "paihangbang-ep04/1.0 (research script)"}


def get_json(url):
    return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())


def lic_name(lic: str, ver: str) -> str:
    lic = lic.lower()
    if lic in ("cc0", "pdm"):
        return "CC0" if lic == "cc0" else "Public domain"
    return f"CC {lic.upper().replace('-', '-')} {ver}".replace("CC BY-SA", "CC BY-SA").strip()


def run(idx: int, query: str, per: int, data: dict) -> str:
    it = data["items"][idx]
    key = f"{idx:02d}_" + re.sub(r"[^a-z0-9]+", "_", it["name"].lower()).strip("_")
    d = CAND / key
    meta_p = d / "meta.json"
    meta = json.loads(meta_p.read_text(encoding="utf-8")) if meta_p.exists() else []
    meta = [m for m in meta if not m["id"].startswith("o")]
    q = urllib.parse.urlencode({"q": query, "license_type": "commercial", "page_size": 40, "mature": "false"})
    res = get_json(f"https://api.openverse.org/v1/images/?{q}")["results"]
    n = 0
    for r in res:
        if n >= per:
            break
        if "wikimedia" in (r.get("source") or "") or "wikimedia" in (r.get("url") or ""):
            continue
        f = d / f"o{n}.jpg"
        try:
            if not f.exists():
                f.write_bytes(urllib.request.urlopen(urllib.request.Request(r["url"], headers=UA), timeout=60).read())
                time.sleep(0.5)
            with Image.open(f) as im:
                w, h = im.size
        except Exception:  # noqa: BLE001
            f.unlink(missing_ok=True)
            continue
        if min(w, h) < 900:
            f.unlink(missing_ok=True)
            continue
        meta.append({"id": f"o{n}", "file": f.name, "image_url": r["url"], "page_url": r.get("foreign_landing_url", ""),
                     "source": f"Openverse/{r.get('source')}", "author": r.get("creator") or "",
                     "licence": lic_name(r.get("license", ""), r.get("license_version", "")),
                     "why": (r.get("title") or "")[:120], "attribution": r.get("attribution", ""), "w": w, "h": h})
        n += 1
    meta_p.write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    return f"{key}: Openverse +{n}（结果 {len(res)} 条）"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("pairs", nargs="+")
    ap.add_argument("--per", type=int, default=10)
    a = ap.parse_args()
    data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    for p in a.pairs:
        idx, q = p.split(":", 1)
        print(run(int(idx), q.strip(), a.per, data), flush=True)


if __name__ == "__main__":
    main()
