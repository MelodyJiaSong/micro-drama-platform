# -*- coding: utf-8 -*-
"""apply 之后跑：风险图（放开来源的全网图，许可不明）进 image（只在 _with-risk-images 版显示），
已 apply 的可商用图挪到 image_alt（默认母版用）。契约 v1.4。可重复运行。
RISK: data.json 下标 -> (web 目录 key, 文件 id, 作者/出处, 说明)
"""
import hashlib
import json
import shutil
from datetime import date
from pathlib import Path

from PIL import Image, ImageOps

HERE = Path(__file__).resolve().parent
EP = HERE.parent
TODAY = date.today().isoformat()

RISK = {
    0: ("00_01_yangwang_u9_xtreme", "w2", "BYD / Yangwang press photo (via Motoring Research)", "U9 Xtreme record car at ATP Papenburg, 3/4 front on the banking"),
    4: ("04_05_bugatti_w16_mistral", "w1", "Bugatti press photo (via Motoring Research)", "W16 Mistral record car at ATP Papenburg, 3/4 front, tracking shot"),
    6: ("06_07_hennessey_venom_f5", "w9", "Hennessey press photo (via Motor Authority)", "Venom F5 on the Kennedy Space Center runway, 3/4 front"),
    5: ("05_06_czinger_21c", "w1", "Goodwood Road & Racing (FOS 2023 event photo)", "orange 21C at Goodwood Festival of Speed, 3/4 front"),
    9: ("09_10_rimac_nevera_r", "w12", "Rimac press / CAR magazine gallery", "Nevera R (green, rear wing) at Monterey Car Week, 3/4 front"),
    12: ("12_13_dauer_962_le_mans", "w0", "evo magazine (A-Z of supercars)", "road-registered Dauer 962 LM with number plate, 3/4 front"),
    18: ("18_18_bugatti_centodieci", "w8", "Bugatti press photo (via Carscoops)", "white Centodieci, 3/4 front from above"),
}
EXTRA = {}  # 下标 -> 同上，但没有可商用替代（默认版保持该项原状）

data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
assets = json.loads((EP / "assets.json").read_text(encoding="utf-8"))
by_file = {a["file"]: a for a in assets}


def put(src: Path, rel: str) -> tuple[int, int]:
    dst = EP / rel
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        if max(im.size) > 2400:
            im.thumbnail((2400, 2400), Image.LANCZOS)
        im.save(dst, quality=90)
        return im.size


for idx, (key, wid, author, why) in RISK.items():
    it = data["items"][idx]
    stem = Path(it["image"]).stem.removesuffix("_alt")
    img_rel = f"assets/img/{stem}.jpg"
    alt_rel = f"assets/img/{stem}_alt.jpg"
    # 1) 现有可商用图 → _alt
    if it.get("image") == img_rel and not it.get("image_alt") and (EP / img_rel).exists() and img_rel in by_file and not str(by_file[img_rel].get("licence","")).startswith("unknown"):
        shutil.move(str(EP / img_rel), str(EP / alt_rel))
        a = by_file.pop(img_rel)
        a["file"] = alt_rel
        by_file[alt_rel] = a
        it["image_alt"] = alt_rel
        it["image_alt_credit"] = it.get("image_credit", "")
    # 2) 风险图 → image
    meta = json.loads((HERE / "find" / "web" / key / "meta.json").read_text(encoding="utf-8"))
    m = next(x for x in meta if x["id"] == wid)
    size = put(HERE / "find" / "web" / key / m["file"], img_rel)
    by_file[img_rel] = {"file": img_rel, "source_page": m["page_url"], "source_url": m["image_url"], "author": author,
                        "licence": "unknown (press / editorial image; licence not stated)", "licence_url": "", "attribution_required": True,
                        "modified": f"downscaled to {size[0]}x{size[1]} px and re-encoded as JPEG; renderer will crop",
                        "sha256": hashlib.sha256((EP / img_rel).read_bytes()).hexdigest(), "retrieved_at": TODAY, "fop_note": "",
                        "selected_by": f"follow-up 023 追加要求 3：Claude 全网检索（{why}）"}
    it["image"] = img_rel
    it["image_credit"] = author
    it["image_risk"] = "licence unknown"
    it["image_note"] = "Photo withheld: licence unclear"

(EP / "assets.json").write_text(json.dumps(list(by_file.values()), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(EP / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("risk items:", sorted(RISK))
