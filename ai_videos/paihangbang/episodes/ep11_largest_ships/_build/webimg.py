# -*- coding: utf-8 -*-
"""全网找图辅助（follow-up 用户追加要求 5）：打开候选页面，取 og:image / twitter:image / 页面里最大的图片链接，
下载到 _build/web/<key>/，追加写 reselect/claude_web_<NN>.json（同 schema，licence 照来源页写，默认 unknown）。

用法：python webimg.py <item_key> <page_url> [<page_url> ...]          # 自动取页面主图
      python webimg.py <item_key> --img <image_url> <page_url> [licence] [author]   # 已知原图直链
"""
import html as H
import json
import re
import sys
import urllib.request
from pathlib import Path

B = Path(__file__).parent
EP = B.parent
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "_tools"))
from image_reselect import item_key  # noqa: E402

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36",
      "Accept-Language": "en-US,en;q=0.9"}


def fetch(url, binary=False):
    r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40)
    b = r.read()
    return b if binary else b.decode("utf-8", "replace")


def main_images(page):
    t = fetch(page)
    found = []
    for pat in (r'<meta[^>]+property=["\']og:image(?::url)?["\'][^>]+content=["\']([^"\']+)', r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image',
                r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)'):
        found += re.findall(pat, t, re.I)
    # 页面里写了大尺寸的图（srcset 里最大的 / data-src）
    for m in re.finditer(r'srcset=["\']([^"\']+)["\']', t, re.I):
        best = None
        for part in m.group(1).split(","):
            bits = part.strip().split()
            if len(bits) == 2 and bits[1].endswith("w") and bits[1][:-1].isdigit():
                w = int(bits[1][:-1])
                if not best or w > best[0]:
                    best = (w, bits[0])
        if best and best[0] >= 1600:
            found.append(best[1])
    out = []
    for u in found:
        u = H.unescape(u)
        if u.startswith("//"):
            u = "https:" + u
        elif u.startswith("/"):
            u = re.match(r"https?://[^/]+", page).group(0) + u
        if u not in out:
            out.append(u)
    return out


def add(key_name, rows):
    data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    idx = next(i for i, it in enumerate(data["items"]) if it["key"] == key_name)
    k = item_key(idx, data["items"][idx])
    f = EP / "_build" / "reselect" / f"claude_0web_{idx:02d}.json"
    d = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {"items": [{"key": k, "images": []}]}
    have = {x["image_url"] for x in d["items"][0]["images"]}
    for r in rows:
        if r["image_url"] not in have:
            d["items"][0]["images"].append(r)
    f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{k}: {len(d['items'][0]['images'])} web candidates")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    key_name = sys.argv[1]
    rows = []
    if sys.argv[2] == "--img":
        img, page = sys.argv[3], sys.argv[4]
        lic = sys.argv[5] if len(sys.argv) > 5 else "unknown"
        author = sys.argv[6] if len(sys.argv) > 6 else ""
        rows.append({"image_url": img, "page_url": page, "source": re.sub(r"^https?://(www\.)?([^/]+).*", r"\2", page),
                     "author": author, "licence": lic, "why": "web: direct image link from source page"})
    else:
        for page in sys.argv[2:]:
            try:
                imgs = main_images(page)
            except Exception as e:  # noqa: BLE001
                print("fail", page, e)
                continue
            for u in imgs[:3]:
                rows.append({"image_url": u, "page_url": page, "source": re.sub(r"^https?://(www\.)?([^/]+).*", r"\2", page),
                             "author": "", "licence": "unknown", "why": "web: page main image (og:image / largest srcset)"})
            print(page, "->", imgs[:3])
    add(key_name, rows)
