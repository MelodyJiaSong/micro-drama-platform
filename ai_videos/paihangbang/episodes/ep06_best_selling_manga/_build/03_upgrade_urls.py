# -*- coding: utf-8 -*-
"""ep06：把 Codex 候选里的缩略图链接改写成原图（Amazon 去尺寸后缀、Kobo 取最大档、X 取 orig），
原地改 `_build/reselect/codex_b*.json`（原文件先备份到 reselect/orig/，不能留在同目录，否则 download 的 glob 会重复读），并删掉因此失效的已下载候选，
之后重跑 `image_reselect.py download` 即按新链接重下。"""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
B = EP / "_build" / "reselect"


def upgrade(u: str) -> str:
    u2 = re.sub(r"(m\.media-amazon\.com/images/I/[^./]+)\.[^/]*?(\.jpe?g|\.png)$", r"\1\2", u)
    u2 = re.sub(r"(images-na\.ssl-images-amazon\.com/images/I/[^./]+)\.[^/]*?(\.jpe?g|\.png)$", r"\1\2", u2)
    u2 = re.sub(r"(cdn\.kobo\.com/book-images/[^/]+)/\d+/\d+/\d+/False/", r"\1/1650/2200/100/False/", u2)
    u2 = re.sub(r"(pbs\.twimg\.com/media/[^?]+)\?.*$", r"\1?name=orig", u2)
    return u2


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    n = 0
    for f in sorted(B.glob("codex_b*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        changed = False
        for row in d.get("items", []):
            for img in row["images"]:
                new = upgrade(img["image_url"])
                if new != img["image_url"]:
                    img["image_url_original_link"] = img["image_url"]
                    img["image_url"] = new
                    changed = True
                    n += 1
        if changed:
            bak = B / "orig" / f.name
            bak.parent.mkdir(exist_ok=True)
            if not bak.exists():
                shutil.copy2(f, bak)
            f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    # 已下载候选按 meta 里的旧链接找，链接变了就删文件，download 会重下
    removed = 0
    for meta in B.glob("cand/*/meta.json"):
        for m in json.loads(meta.read_text(encoding="utf-8")):
            if m.get("id") != "current" and upgrade(m.get("image_url", "")) != m.get("image_url", ""):
                (meta.parent / m["file"]).unlink(missing_ok=True)
                removed += 1
    print(f"改写 {n} 条链接，删除 {removed} 个待重下的候选")


if __name__ == "__main__":
    main()
