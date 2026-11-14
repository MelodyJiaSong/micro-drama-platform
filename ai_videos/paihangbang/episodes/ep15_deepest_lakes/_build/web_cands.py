# -*- coding: utf-8 -*-
"""用户追加要求 5：全网找图。给定条目 key 与若干网页 URL：抓页面（curl），取 og:image 与页面里的大图，
探测尺寸，长边 ≥ 1000 px 的作为候选追加到 reselect/claude_web.json（许可照实写 unknown，作者尽量取 meta）。

    python web_cands.py <key> <page_url> [<page_url> ...] [--min 1000]
"""
import argparse
import io
import json
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
OUT = HERE / "reselect" / "claude_web.json"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"


def curl(url: str, binary: bool = False):
    r = subprocess.run(["curl", "-sL", "--max-time", "60", "-A", UA, url], capture_output=True)
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("key")
    ap.add_argument("pages", nargs="+")
    ap.add_argument("--min", type=int, default=1000)
    ap.add_argument("--direct", action="store_true", help="pages 即图片直链（page 用第一个非图片参数）")
    a = ap.parse_args()
    data = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {"items": []}
    row = next((r for r in data["items"] if r["key"] == a.key), None)
    if not row:
        row = {"key": a.key, "images": []}
        data["items"].append(row)
    have = {i["image_url"] for i in row["images"]}
    for page in a.pages:
        html = curl(page)
        site = urllib.parse.urlparse(page).netloc
        author = ""
        m = re.search(r'<meta[^>]+name="author"[^>]+content="([^"]+)"', html)
        if m:
            author = m.group(1)
        urls = re.findall(r'<meta[^>]+property="og:image(?::secure_url)?"[^>]+content="([^"]+)"', html)
        urls += re.findall(r'<meta[^>]+content="([^"]+)"[^>]+property="og:image"', html)
        for src in re.findall(r'<img[^>]+(?:data-src|data-lazy-src|src)="([^"]+\.(?:jpe?g|png|webp)[^"]*)"', html, re.I):
            urls.append(src)
        for srcset in re.findall(r'srcset="([^"]+)"', html):
            parts = [p.strip().split(" ")[0] for p in srcset.split(",") if p.strip()]
            if parts:
                urls.append(parts[-1])
        seen = []
        for u in urls:
            u = urllib.parse.urljoin(page, u.replace("&amp;", "&"))
            if u not in seen and not re.search(r"logo|icon|avatar|sprite|banner-ad|placeholder", u, re.I):
                seen.append(u)
        added = 0
        for u in seen[:25]:
            if u in have:
                continue
            blob = curl(u, binary=True)
            try:
                with Image.open(io.BytesIO(blob)) as im:
                    w, h = im.size
            except Exception:  # noqa: BLE001
                continue
            if max(w, h) < a.min:
                continue
            row["images"].append({"image_url": u, "page_url": page, "source": site, "author": author or "unknown",
                                  "licence": "unknown", "why": f"open-web page image {w}x{h} from {site}"})
            have.add(u)
            added += 1
            print("  +", w, h, u[:120])
        print(a.key, page[:80], "added", added)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
