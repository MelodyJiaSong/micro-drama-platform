# -*- coding: utf-8 -*-
"""契约 v1.4：风险图条目的默认版替代图（image_alt / image_alt_credit）。apply 之后运行。
    python add_alts.py
"""
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

from PIL import Image, ImageOps

EP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EP.parents[1] / "_tools"))
from image_reselect import licence_url  # noqa: E402

# data 下标 → 替代候选 id（必须是可商用许可）
ALTS = {21: "c0", 30: "c0", 39: "c0"}


def main() -> None:
    data = json.load(open(EP / "data.json", encoding="utf-8"))
    assets = json.load(open(EP / "assets.json", encoding="utf-8"))
    for idx, cid in ALTS.items():
        it = data["items"][idx]
        key = f"{idx:02d}_{Path(it['image']).stem}"
        d = EP / "_build" / "reselect" / "cand" / key
        m = next(x for x in json.load(open(d / "meta.json", encoding="utf-8")) if x["id"] == cid)
        rel = f"assets/img/{Path(it['image']).stem}_alt.jpg"
        with Image.open(d / m["file"]) as im:
            im = ImageOps.exif_transpose(im).convert("RGB")
            im.thumbnail((2400, 2400), Image.LANCZOS)
            im.save(EP / rel, quality=90)
            size = im.size
        lic = m["licence"].strip()
        entry = {"file": rel, "source_page": m.get("page_url", ""), "source_url": m.get("image_url", ""), "author": m.get("author", ""),
                 "licence": lic, "licence_url": licence_url(lic), "attribution_required": not lic.lower().startswith(("pexels", "unsplash", "public domain")),
                 "modified": f"downscaled to {size[0]}x{size[1]} px and re-encoded as JPEG; renderer will crop",
                 "sha256": hashlib.sha256((EP / rel).read_bytes()).hexdigest(), "retrieved_at": date.today().isoformat(),
                 "fop_note": "", "selected_by": "follow-up 023 Claude WebFetch 搜图（默认版替代图）"}
        assets = [a for a in assets if a["file"] != rel] + [entry]
        it["image_alt"] = rel
        it["image_alt_credit"] = f"{m.get('author') or 'Unknown'} / {lic}"
        print(idx, it["name"], "alt", rel, it["image_alt_credit"])
    (EP / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (EP / "assets.json").write_text(json.dumps(assets, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
