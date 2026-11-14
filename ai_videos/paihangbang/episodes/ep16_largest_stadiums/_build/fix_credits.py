# -*- coding: utf-8 -*-
"""ep16：许可不明 / 无作者的图，卡上署名写来源站（via <domain> / licence unknown），账本 author 补来源说明。python _build/fix_credits.py"""
import json
from pathlib import Path
from urllib.parse import urlparse
EP = Path(__file__).resolve().parents[1]
d = json.loads((EP / "data.json").read_text(encoding="utf-8")); A = json.loads((EP / "assets.json").read_text(encoding="utf-8"))
by = {a["file"]: a for a in A}
for it in d["items"]:
    for fk, ck in (("image", "image_credit"), ("image_alt", "image_alt_credit")):
        a = by.get(it.get(fk) or "")
        if not a or a.get("licence", "").startswith("AI-generated"):
            continue
        dom = urlparse(a.get("source_page") or a.get("source_url") or "").netloc.replace("www.", "")
        if not a.get("author") or a["author"].startswith("Unknown"):
            a["author"] = f"unknown (via {dom})" if a["licence"] == "unknown" else f"{dom} contributor"
        it[ck] = f"via {dom} / licence unknown" if a["licence"] == "unknown" else f"{a['author']} / {a['licence']}"
(EP / "data.json").write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(EP / "assets.json").write_text(json.dumps(A, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("credits fixed")
