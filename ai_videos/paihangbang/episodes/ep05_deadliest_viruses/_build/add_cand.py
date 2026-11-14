# -*- coding: utf-8 -*-
"""Claude 自己补候选（follow-up 024）：把找到的图下载进某张卡的候选目录并写 meta.json。

    python add_cand.py <virus_key> phil:<pid> [phil:<pid> ...]          # CDC PHIL 原始 TIFF；从详情页读版权说明
    python add_cand.py <virus_key> flickr:<user>/<photo_id> ...          # Flickr 原图（sizes/o 页），许可从页面读
    python add_cand.py <virus_key> url:<direct_url> --page P --source S --author A --licence L --why W
    python add_cand.py --upgrade-flickr                                  # 已有候选里的 Flickr _b 小图全部换原图
"""
from __future__ import annotations

import argparse
import json
import re
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image

Image.MAX_IMAGE_PIXELS = None
EP = Path(__file__).resolve().parents[1]
CAND = EP / "_build" / "reselect" / "cand"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130 Safari/537.36"}
FLICKR_LIC = {"by/": "CC BY 2.0", "by-sa/": "CC BY-SA 2.0", "mark": "Public domain (PDM 1.0)",
              "zero": "CC0", "by-nc": "CC BY-NC (rejected)", "by-nd": "CC BY-ND (rejected)"}


def get(url: str, timeout: int = 180) -> bytes:
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()


def cand_dir(key: str) -> Path:
    data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    for i, it in enumerate(data["items"]):
        if it["key"] == key:
            return CAND / f"{i:02d}_{Path(it['image']).stem}"
    raise SystemExit(f"unknown key {key}")


def save(d: Path, cid: str, blob: bytes, meta: dict) -> str:
    im = Image.open(BytesIO(blob)).convert("RGB")
    if max(im.size) > 4000:
        im.thumbnail((4000, 4000), Image.LANCZOS)
    d.mkdir(parents=True, exist_ok=True)
    f = d / f"{cid}.jpg"
    im.save(f, quality=92)
    mp = d / "meta.json"
    rows = json.loads(mp.read_text(encoding="utf-8")) if mp.exists() else []
    rows = [r for r in rows if r["id"] != cid] + [{**meta, "id": cid, "file": f.name, "w": im.size[0], "h": im.size[1], "found_by": "claude"}]
    mp.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    return f"{cid} {im.size[0]}x{im.size[1]} {meta['licence']}"


def phil(d: Path, pid: str) -> str:
    page = f"https://wwwn.cdc.gov/phil/Details.aspx?pid={pid}"
    html = get(page).decode("utf-8", "replace")
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text)
    cap = re.search(r"Caption:\s*(.{0,300})", text)
    field = re.search(r"Copyright Restrictions:\s*(.{0,120})", text)
    f = field.group(1) if field else ""
    pd = f.startswith("Permission is not required for public domain") or f.startswith("None - This image is in the public domain")
    lic = "Public domain" if pd else f"unknown (PHIL: {f[:60]})"
    credit = re.search(r"Photo Credit:\s*([^\n]{0,80})", text)
    blob = get(f"https://wwwn.cdc.gov/phil/PHIL_Images/{pid}/{pid}.tif")
    return save(d, f"p{pid}", blob, {"image_url": f"https://wwwn.cdc.gov/phil/PHIL_Images/{pid}/{pid}.tif", "page_url": page,
                                     "source": "CDC Public Health Image Library", "author": (credit.group(1).strip() if credit else "CDC"),
                                     "licence": lic, "why": (cap.group(1).strip()[:200] if cap else "")})


def flickr(d: Path, ref: str, cid: str | None = None) -> str:
    user, pid = ref.split("/")
    urls, html = [], ""
    for s in ("o", "k", "h", "l", "b"):
        try:
            page = get(f"https://www.flickr.com/photos/{user}/{pid}/sizes/{s}/").decode("utf-8", "replace")
        except Exception:  # noqa: BLE001 —— 该尺寸不开放
            continue
        html = html or page
        urls = sorted(set(re.findall(rf"https://live\.staticflickr\.com/\d+/{pid}_[a-z0-9]+_{s}\.(?:jpg|png)", page)))
        if urls:
            html = page
            break
    if not urls:
        return f"{ref}: no size page reachable"
    m = re.search(r"creativecommons\.org/(licenses|publicdomain)/([a-z-]+(?:/[\d.]+)?)", html)
    lic = "unknown"
    if m:
        k = m.group(2)
        lic = next((v for kk, v in sorted(FLICKR_LIC.items(), key=lambda kv: -len(kv[0])) if k.startswith(kk)), f"CC {k}")
    title = re.search(r"<title>([^<]*)</title>", html)
    return save(d, cid or f"f{pid}", get(urls[0]), {"image_url": urls[0], "page_url": f"https://www.flickr.com/photos/{user}/{pid}/",
                                                    "source": f"Flickr — {user}", "author": {"niaid": "NIAID", "nihgov": "NIH"}.get(user, user),
                                                    "licence": lic, "why": title.group(1).strip()[:200] if title else ""})


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("key", nargs="?")
    ap.add_argument("refs", nargs="*")
    ap.add_argument("--page", default="")
    ap.add_argument("--source", default="")
    ap.add_argument("--author", default="")
    ap.add_argument("--licence", default="unknown")
    ap.add_argument("--why", default="")
    ap.add_argument("--upgrade-flickr", action="store_true")
    a = ap.parse_args()
    if a.upgrade_flickr:
        for d in sorted(CAND.iterdir()):
            mp = d / "meta.json"
            if not mp.exists():
                continue
            done = set()
            for m in json.loads(mp.read_text(encoding="utf-8")):
                g = re.search(r"flickr\.com/photos/([^/]+)/(\d+)", m.get("page_url", ""))
                if g and "staticflickr" in m.get("image_url", "") and not m["id"].startswith("f") and g.group(2) not in done:
                    done.add(g.group(2))
                    try:
                        print(d.name, flickr(d, f"{g.group(1)}/{g.group(2)}"), flush=True)
                    except Exception as e:  # noqa: BLE001
                        print(d.name, g.group(2), "FAIL", e, flush=True)
        return
    d = cand_dir(a.key)
    for n, r in enumerate(a.refs):
        try:
            if r.startswith("phil:"):
                print(phil(d, r[5:]))
            elif r.startswith("flickr:"):
                print(flickr(d, r[7:]))
            elif r.startswith("url:"):
                k = len([p for p in d.glob("u*.jpg")])
                print(save(d, f"u{k}", get(r[4:]), {"image_url": r[4:], "page_url": a.page, "source": a.source,
                                                    "author": a.author, "licence": a.licence, "why": a.why}))
        except Exception as e:  # noqa: BLE001
            print(r, "FAIL", e)


if __name__ == "__main__":
    main()
