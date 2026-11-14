# -*- coding: utf-8 -*-
"""QC 第 1 轮（2026-11-04）后的图片更换：Araguaia 新图、Indus 换巴基斯坦境内图、Lena / Pilcomayo 替代图升级到 2048 px。"""
import hashlib
import json
from datetime import date
from pathlib import Path

from PIL import Image, ImageOps

EP = Path(__file__).resolve().parents[1]
X = EP / "_build" / "reselect" / "extra"
# key: (字段, 源文件, 目标相对路径, 作者, 许可, 许可链接, 来源页, 直链, 说明)
JOBS = [
    ("araguaia", "image", X / "aragua_k.jpg", "assets/img/32_araguaia.jpg", "Augusto Miranda / MTur", "Public domain",
     "https://creativecommons.org/publicdomain/mark/1.0/", "https://www.flickr.com/photos/mturdestinos/26088774777",
     "https://live.staticflickr.com/4794/26088774777_d9591e12d5_k.jpg",
     "Flickr MTur Destinos (Brazil Ministry of Tourism), title 'AugustoMiranda_Rio Araguaia_Aruana_GO'; Public Domain Mark; page asks for credit 'Augusto Miranda/MTur'"),
    ("indus", "image", X / "indus_BfKHN4uIUx8.jpg", "assets/img/21_indus.jpg", "Danish Rasool", "Unsplash License",
     "https://unsplash.com/license", "https://unsplash.com/photos/a-large-body-of-water-with-a-bridge-in-the-background-BfKHN4uIUx8",
     "https://images.unsplash.com/photo-1708516281145-74a756d710e9?ixid=NHwxMjA3fDA&ixlib=rb-4.1.0&fm=jpg&q=85&w=3000",
     "Unsplash tags 'indus river', 'pakistan', 'bridge'; shows the Lansdowne (cantilever) and Ayub (arch) bridges over the Indus at Sukkur, Sindh, Pakistan (QC M4: replaces the Ladakh photo)"),
    ("lena", "image", X / "lena_k.jpg", "assets/img/11_lena.jpg", "Artem Svetlov", "CC BY 2.0",
     "https://creativecommons.org/licenses/by/2.0/", "https://www.flickr.com/photos/trolleway/35052951020",
     "https://live.staticflickr.com/4250/35052951020_12a0ee25f3_k.jpg", "Flickr 'Lena Cheeks', Lena River cruise; Large 2048 (original 429-throttled)"),
    ("pilcomayo", "image_alt", X / "pilco_k.jpg", "assets/img/38_pilcomayo_alt.jpg", "Dan Lundberg", "CC BY-SA 2.0",
     "https://creativecommons.org/licenses/by-sa/2.0/", "https://www.flickr.com/photos/9508280@N07/37949273732",
     "https://live.staticflickr.com/4458/37949273732_29dce1e429_k.jpg", "Flickr: Puente Sucre over the Pilcomayo, Bolivia; Large 2048"),
]

data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
assets = json.loads((EP / "assets.json").read_text(encoding="utf-8"))
by = {a["file"]: i for i, a in enumerate(assets)}
items = {it["key"]: it for it in data["items"]}
for key, field, src, rel, author, lic, lurl, page, url, why in JOBS:
    it = items[key]
    dst = EP / rel
    old = it.get(field)
    if old and old != rel and (EP / old).exists() and old not in [x[3] for x in JOBS]:
        (EP / old).replace(EP / "_build" / "old_img" / Path(old).name)
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        if max(im.size) > 2400:
            im.thumbnail((2400, 2400), Image.LANCZOS)
        im.save(dst, quality=90)
        size = im.size
    e = {"file": rel, "source_page": page, "source_url": url, "author": author, "licence": lic, "licence_url": lurl,
         "attribution_required": not lic.startswith(("Public domain", "Unsplash")),
         "modified": f"downscaled to {size[0]}x{size[1]} px and re-encoded as JPEG; renderer will crop",
         "sha256": hashlib.sha256(dst.read_bytes()).hexdigest(), "retrieved_at": date.today().isoformat(), "fop_note": "",
         "selected_by": f"ep17 QC 第 1 轮修订（Claude 选图）：{why}"}
    if old and old in by and old != rel:
        assets[by[old]] = e
    elif rel in by:
        assets[by[rel]] = e
    else:
        assets.append(e)
    by = {a["file"]: i for i, a in enumerate(assets)}
    it[field] = rel
    it["image_credit" if field == "image" else "image_alt_credit"] = f"{author} / {lic}"
    if field == "image":
        for k in ("image_risk", "image_note", "image_alt", "image_alt_credit", "image_focus"):
            if key in ("araguaia", "indus"):
                it.pop(k, None)
    print(key, field, rel, size)
refs = {it[k] for it in data["items"] for k in ("image", "image_alt") if it.get(k)}
assets = [a for a in assets if a["file"] in refs]
(EP / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(EP / "assets.json").write_text(json.dumps(assets, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
