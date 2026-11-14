# -*- coding: utf-8 -*-
"""Claude 自己找图（follow-up 022：不再用 Codex）。用 iNaturalist 公开 API（免 key、免费）取野外研究级观测里
CC0 / CC BY / CC BY-SA 的照片，按收藏数排序，下载原图（长边 ≤ 2048）并入 reselect/cand/<key>/meta.json（id 前缀 n）。
用法：python -I <本文件> idx:taxon [idx:taxon ...] [--per 12]
例：python -I inat_candidates.py "06:Rhinoceros sondaicus" "21:Equus grevyi"
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
UA = {"User-Agent": "paihangbang-ep04/1.0 (research script; contact via repo owner)"}
LIC = {"cc0": "CC0", "cc-by": "CC BY 4.0", "cc-by-sa": "CC BY-SA 4.0"}


def get_json(url: str) -> dict:
    return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())


def key_for(idx: int, data: dict) -> str:
    it = data["items"][idx]
    return f"{idx:02d}_" + re.sub(r"[^a-z0-9]+", "_", it["name"].lower()).strip("_")


def run(idx: int, taxon: str, per: int, data: dict) -> str:
    key = key_for(idx, data)
    d = CAND / key
    d.mkdir(parents=True, exist_ok=True)
    meta_p = d / "meta.json"
    meta = json.loads(meta_p.read_text(encoding="utf-8")) if meta_p.exists() else []
    meta = [m for m in meta if not m["id"].startswith("n")]          # 重跑时替换本脚本的旧结果
    captive = "false"
    if "|" in taxon:                      # "Taxon|any" = 圈养也收（野外照片为 0 的物种），"Taxon|place=ID" 限地点
        taxon, opt = taxon.split("|", 1)
        captive = None if opt == "any" else captive
    extra = {"captive": captive, "quality_grade": "research"} if captive else {}   # 圈养观测在 iNat 是 casual 级，不能限 research
    q = urllib.parse.urlencode({"taxon_name": taxon, **extra,
                                "photo_license": "cc0,cc-by,cc-by-sa", "order_by": "votes", "per_page": 60,
                                "photos": "true"})
    obs = get_json(f"https://api.inaturalist.org/v1/observations?{q}")["results"]
    n = 0
    for o in obs:
        if n >= per:
            break
        tname = (o.get("taxon") or {}).get("name", "")
        if not (tname.lower() == taxon.lower() or tname.lower().startswith(taxon.lower() + " ")) or "×" in tname or " x " in tname:
            continue                                  # 只要本种或其亚种；杂交（Equus grevyi × quagga）排除（独立审片 B1）
        ph = next((p for p in o.get("photos", []) if p.get("license_code") in LIC), None)
        if not ph:
            continue
        url = ph["url"].replace("/square.", "/original.")
        f = d / f"n{n}.jpg"
        try:
            if not f.exists():
                f.write_bytes(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())
                time.sleep(0.5)
            with Image.open(f) as im:
                w, h = im.size
        except Exception:  # noqa: BLE001
            f.unlink(missing_ok=True)
            continue
        if min(w, h) < 900:
            f.unlink(missing_ok=True)
            continue
        author = (o.get("user") or {}).get("name") or (o.get("user") or {}).get("login") or ""
        meta.append({"id": f"n{n}", "file": f.name, "image_url": url, "page_url": o.get("uri") or f"https://www.inaturalist.org/observations/{o['id']}",
                     "source": "iNaturalist", "taxon": tname, "author": author, "licence": LIC[ph["license_code"]],
                     "captive": captive is None and o.get("captive", False), "why": f"research-grade {'captive' if o.get('captive') else 'wild'} observation, {o.get('place_guess') or ''}, {o.get('observed_on') or ''}, faves {o.get('faves_count', 0)}",
                     "attribution": ph.get("attribution", ""), "w": w, "h": h})
        n += 1
    meta_p.write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    return f"{key}: iNaturalist +{n}（观测 {len(obs)} 条）"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("pairs", nargs="+")
    ap.add_argument("--per", type=int, default=12)
    a = ap.parse_args()
    data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    for p in a.pairs:
        idx, taxon = p.split(":", 1)
        print(run(int(idx), taxon.strip(), a.per, data), flush=True)


if __name__ == "__main__":
    main()
