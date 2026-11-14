# -*- coding: utf-8 -*-
"""用户追加要求 5（质量优先）：把更好的许可不明图设为 image（风险版），现有可商用图降为 image_alt（默认版）。
    python upgrade_risk.py
"""
import hashlib
import json
import shutil
import sys
from datetime import date
from pathlib import Path

from PIL import Image, ImageOps

EP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EP.parents[1] / "_tools"))
from image_reselect import licence_url  # noqa: E402

UPGRADES = {10: ("c1", "Hanspeter Gass / licence unknown")}   # data 下标 → (候选 id, 卡上署名)


def main() -> None:
    data = json.load(open(EP / "data.json", encoding="utf-8"))
    assets = json.load(open(EP / "assets.json", encoding="utf-8"))
    by = {a["file"]: a for a in assets}
    for idx, (cid, credit) in UPGRADES.items():
        it = data["items"][idx]
        rel = it["image"]
        stem = Path(rel).stem
        alt_rel = f"assets/img/{stem}_alt.jpg"
        if not it.get("image_alt"):                       # 现图 → 替代图
            shutil.copy2(EP / rel, EP / alt_rel)
            alt = dict(by[rel], file=alt_rel)
            assets.append(alt)
            it["image_alt"], it["image_alt_credit"] = alt_rel, it["image_credit"]
        d = EP / "_build" / "reselect" / "cand" / f"{idx:02d}_{stem}"
        m = next(x for x in json.load(open(d / "meta.json", encoding="utf-8")) if x["id"] == cid)
        with Image.open(d / m["file"]) as im:
            im = ImageOps.exif_transpose(im).convert("RGB")
            im.thumbnail((2400, 2400), Image.LANCZOS)
            im.save(EP / rel, quality=90)
            size = im.size
        lic = m["licence"].strip()
        entry = {"file": rel, "source_page": m.get("page_url", ""), "source_url": m.get("image_url", ""), "author": m.get("author", ""),
                 "licence": lic, "licence_url": licence_url(lic), "attribution_required": True,
                 "modified": f"downscaled to {size[0]}x{size[1]} px and re-encoded as JPEG; renderer will crop",
                 "sha256": hashlib.sha256((EP / rel).read_bytes()).hexdigest(), "retrieved_at": date.today().isoformat(),
                 "fop_note": "", "selected_by": "用户追加要求 5 质量优先：风险版用图（许可不明）"}
        assets = [a for a in assets if a["file"] != rel] + [entry]
        it["image_credit"] = credit
        it["image_risk"] = "licence unknown"
        it["image_note"] = "Photo withheld: licence unclear"
        it.pop("image_focus", None)
        print(idx, it["name"], "risk", rel, "| alt", it["image_alt"])
    (EP / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (EP / "assets.json").write_text(json.dumps(assets, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
