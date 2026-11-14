# -*- coding: utf-8 -*-
"""follow-up 023 / 追加要求 3：打开来源页，列出 og:image 与页面里的大图直链（只读公开页面）。
python -I page_imgs.py <url> [filter_regex]"""
import html
import re
import sys
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
url = sys.argv[1]
flt = re.compile(sys.argv[2], re.I) if len(sys.argv) > 2 else None
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36",
      "Accept-Language": "en-US,en;q=0.9"}
t = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read().decode("utf-8", "replace")
seen = []
for m in re.finditer(r'<meta[^>]+(?:property|name)="(?:og:image|twitter:image)[^"]*"[^>]+content="([^"]+)"', t):
    seen.append(("og", m.group(1)))
for m in re.finditer(r'(?:src|data-src|data-lazy-src|href|data-full|data-large-file|data-orig-file)="([^"]+\.(?:jpe?g|png|webp)(?:\?[^"]*)?)"', t, re.I):
    seen.append(("img", m.group(1)))
for m in re.finditer(r'srcset="([^"]+)"', t):
    parts = [p.strip().split(" ")[0] for p in m.group(1).split(",") if p.strip()]
    if parts:
        seen.append(("srcset", parts[-1]))
out = []
for kind, u in seen:
    u = urllib.parse.urljoin(url, html.unescape(u))
    if u in [x for _, x in out] or (flt and not flt.search(u)):
        continue
    if re.search(r"logo|icon|avatar|sprite|badge|flag|emoji|favicon", u, re.I):
        continue
    out.append((kind, u))
for k, (kind, u) in enumerate(out):
    print(k, kind, u)
title = re.search(r"<title>(.*?)</title>", t, re.S)
print("TITLE:", html.unescape(title.group(1).strip()) if title else "")
for m in re.finditer(r"(?:©|&copy;|Copyright|licen[cs]e[d]?)[^<]{0,120}", t):
    print("LIC:", html.unescape(m.group(0))[:140])
    break
