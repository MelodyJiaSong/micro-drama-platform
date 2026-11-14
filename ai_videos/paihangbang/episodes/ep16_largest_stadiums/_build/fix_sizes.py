# -*- coding: utf-8 -*-
"""ep16：Flickr 原图（_o）被 429 限流，把候选 JSON 里的 _o 直链就地换成同一照片的 k(2048)/h(1600) 直链（编号不变）。
    python _build/fix_sizes.py reselect/claude_flickr_p1.json ..."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

B = Path(__file__).resolve().parent
sys.path.insert(0, str(B))
from flickr_search import fetch  # noqa: E402

for fn in sys.argv[1:]:
    p = B / fn
    d = json.loads(p.read_text(encoding="utf-8"))
    n = 0
    for row in d["items"]:
        for c in row["images"]:
            if not c["image_url"].endswith("_o.jpg") or "flickr.com/photos/" not in c["page_url"]:
                continue
            t = fetch(c["page_url"])
            for key in ("k", "h"):
                s = re.search(r'"%s":\{"data":\{"displayUrl":"([^"]+)","width":(\d+),"height":(\d+)' % key, t)
                if s:
                    c["image_url"] = "https:" + s.group(1).replace("\\/", "/")
                    c["why"] = re.sub(r"\(\d+x\d+\)$", f"({s.group(2)}x{s.group(3)})", c["why"])
                    n += 1
                    break
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(fn, "replaced", n, flush=True)
