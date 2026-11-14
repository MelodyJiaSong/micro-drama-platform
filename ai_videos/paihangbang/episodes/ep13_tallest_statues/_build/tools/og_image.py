# -*- coding: utf-8 -*-
"""follow-up 023 / 追加要求 3：放开来源时，从网页取主图直链（og:image / twitter:image / 页面里的大图），打印候选。

    python -I og_image.py <page_url> [<page_url> ...]
"""
import html
import re
import sys
import urllib.parse
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"}


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    for page in sys.argv[1:]:
        try:
            t = urllib.request.urlopen(urllib.request.Request(page, headers=UA), timeout=30).read().decode("utf-8", "replace")
        except Exception as e:  # noqa: BLE001
            print(f"## {page}\n  ERROR {e}")
            continue
        print(f"## {page}")
        seen = []
        for m in re.finditer(r'<meta[^>]+(?:property|name)=["\'](?:og:image|twitter:image)(?::src)?["\'][^>]*content=["\']([^"\']+)', t, re.I):
            seen.append(("og", m.group(1)))
        for m in re.finditer(r'<img[^>]+(?:data-src|data-original|src)=["\']([^"\']+\.(?:jpe?g|png|webp)[^"\']*)', t, re.I):
            seen.append(("img", m.group(1)))
        out = []
        for kind, u in seen:
            u = urllib.parse.urljoin(page, html.unescape(u))
            if u not in [x[1] for x in out] and not re.search(r"logo|icon|avatar|sprite|banner|ads?/", u, re.I):
                out.append((kind, u))
        for kind, u in out[:12]:
            print(f"  {kind} {u}")


if __name__ == "__main__":
    main()
