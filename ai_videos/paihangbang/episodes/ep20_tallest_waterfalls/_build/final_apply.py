# -*- coding: utf-8 -*-
"""ep20 定稿图片（follow-up 016 / 023 / 024，逐张亲眼看过后人工指定）→ assets/img + assets.json + data.json 的 image* 字段。
三类：OK = 可商用照片作 image；RISK = 许可不明照片作 image（image_risk，进 _with-risk-images 版）+ Codex 生成图作 image_alt（默认版）；
GEN = 只有 Codex 生成图（两轮可商用搜索 + 放开来源检索都没有可用照片），直接作 image。
python -I final_apply.py"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import date
from pathlib import Path

from PIL import Image, ImageOps

HERE = Path(__file__).parent
EP = HERE.parent
CAND = HERE / "reselect" / "cand"
WEB = HERE / "web"
TODAY = date.today().isoformat()
LONG = 2400

# idx: (kind, main_src, author, licence, source_page, source_url, crop_box | None, note)
OK, RISK, GEN = "ok", "risk", "gen"
SPEC = {
    0: (OK, CAND / "00_01_angel_falls/c10.jpg", "Jorge Saturno", "CC BY-SA 3.0", "https://imaggeo.egu.eu/view/19005/",
        "https://imaggeo.egu.eu/media/uploads/2025/03/31/19005/59eb139b8ee0dc0c95337efaafa14ba7420a", None, "Imaggeo (EGU) open-access geoscience image library"),
    1: (RISK, CAND / "01_02_tugela_falls/c15.jpg", "Hougaard Malan", "unknown (fine-art print gallery)", "https://osnerartgallery.com/products/tugela-falls",
        "https://osnerartgallery.com/cdn/shop/products/HOUGAARDMALANVERT.jpg?v=1633511057", None, ""),
    2: (RISK, CAND / "02_03_mattenbach_falls/c7.jpg", "unknown", "All rights reserved", "https://www.europeanwaterfalls.com/waterfalls/mattenbachfall/",
        "https://www.europeanwaterfalls.com/wp-content/uploads/Mattenbachfalle-10.jpg", None, ""),
    3: (OK, WEB / "fl_4658174737_8e793a10a7_o.jpg", "Paulo Tomaz", "CC BY-SA 2.0", "https://www.flickr.com/photos/locoperucho/4658174737/",
        "https://live.staticflickr.com/4056/4658174737_8e793a10a7_o.jpg", None, "Flickr 'amazonas bongará Catarata Yumbilla 2'"),
    4: (RISK, CAND / "04_05_skorga_falls/c1.jpg", "Sylwia Smolkowska", "All rights reserved (Wszystkie prawa zastrzeżone)", "https://kieruneknorwegia.pl/najwyzszy-wodospad-w-norwegii/",
        "https://kieruneknorwegia.pl/wp-content/uploads/2020/09/DSC_0462-kopia-2.jpg", None, ""),
    5: (RISK, CAND / "05_06_vinnufossen/c5.jpg", "Johnny Cheng", "All Rights Reserved", "https://www.world-of-waterfalls.com/waterfalls/norway-vinnufossen/",
        "", None, ""),
    6: (GEN, None, None, None, None, None, None, ""),
    7: (OK, CAND / "07_08_browne_falls/c0.jpg", "Floyd Wilde", "CC BY-SA 2.0", "https://www.wondermondo.com/browne-falls/",
        "https://www.wondermondo.com/wp-content/uploads/2017/09/BrowneFalls.jpg", None, "credited 'Floyd Wilde, CC BY-SA 2.0' on the source page"),
    8: (RISK, CAND / "08_09_kjerrskredfossen/c11.jpg", "John Wise", "unknown", "https://www.johnwise.com/2023/09/08/fjord-cruise-to-gudvangen/",
        "https://www.johnwise.com/wp-content/uploads/2023/09/IMG_7452.jpg", None, ""),
    9: (RISK, CAND / "09_10_waihilau_falls/c3.jpg", "Bruce Omori", "unknown", "https://instagrammernews.com/detail/2517112525487862305",
        "https://ignewsimg.s3.ap-northeast-1.wasabisys.com/CLulIAxouGR", None, ""),
    10: (RISK, WEB / "1311979387-Colonial-Creek-Falls-WA_.jpg", "Northwest Waterfall Survey", "All rights reserved (© Northwest Waterfall Survey)",
         "https://www.waterfallsnorthwest.com/waterfall/Colonial-Creek-Falls-4738", "https://www.waterfallsnorthwest.com/pictures/1311979387-Colonial-Creek-Falls-WA_.jpg", None, ""),
    11: (OK, WEB / "fl_30849364486_803060df90_o.jpg", "MI PERÚ", "Public Domain Mark 1.0", "https://www.flickr.com/photos/134894678@N07/30849364486/",
         "https://live.staticflickr.com/5579/30849364486_803060df90_o.jpg", None, "Flickr 'Cataratas Gocta, Distrito de San Pablo, Bongara, Amazonas, Perú'"),
    12: (OK, WEB / "fl_54396656048_70833b8b73_6k.jpg", "Øyvind Holmstad", "CC BY-SA 2.0", "https://www.flickr.com/photos/78304219@N06/54396656048/",
         "https://live.staticflickr.com/65535/54396656048_70833b8b73_6k.jpg", (3300, 1100, 4530, 2640), "Flickr 'Kjelfossen Waterfalls from Gudvangen'; cropped to the main fall, above the roof in the foreground"),
    13: (RISK, CAND / "13_14_isella_falls/c3.jpg", "Kyle McCrohan", "unknown", "https://climberkyle.com/", "", None, ""),
    14: (GEN, None, None, None, None, None, None, ""),
    15: (RISK, CAND / "15_16_tjotafossen/c9.jpg", "Arnt Flatmo", "unknown", "https://www.westcoastpeaks.com/", "", None, ""),
    16: (RISK, CAND / "16_17_dontefossen/c3.jpg", "World of Waterfalls (Johnny Cheng)", "All Rights Reserved", "https://www.world-of-waterfalls.com/waterfalls/norway-dontefossen/", "", None, ""),
    17: (OK, CAND / "17_18_yosemite_falls/c10.jpg", "Barbara Sheldrake", "Pexels License", "", "", None, "Pexels"),
    18: (GEN, None, None, None, None, None, None, ""),
    19: (GEN, None, None, None, None, None, None, ""),
    20: (OK, WEB / "fl_2639508789_49254220dd_o.jpg", "Jean-Marc Astesana", "CC BY-SA 2.0", "https://www.flickr.com/photos/jean-marc_astesana/2639508789/",
         "https://live.staticflickr.com/2316/2639508789_49254220dd_o.jpg", None, "Flickr 'Trou de fer'"),
    21: (GEN, None, None, None, None, None, None, ""),
    22: (GEN, None, None, None, None, None, None, ""),
    23: (RISK, WEB / "1601936279-Tagfossen-2.jpg", "World Waterfall Database", "All rights reserved (WWD: photos may not be used without written consent)",
         "https://www.worldwaterfalldatabase.com/waterfall/Tagfossen-6273", "https://www.worldwaterfalldatabase.com/pictures/1601936279-Tagfossen-2.jpg", None, ""),
    24: (GEN, None, None, None, None, None, None, ""),
    25: (GEN, None, None, None, None, None, None, ""),
    26: (GEN, None, None, None, None, None, None, ""),
    27: (GEN, None, None, None, None, None, None, ""),
    28: (GEN, None, None, None, None, None, None, ""),
    29: (RISK, WEB / "1311751298-Seahpo-Peak-Falls-WA-85-2.jpg", "Northwest Waterfall Survey", "All rights reserved (© Northwest Waterfall Survey)",
         "https://www.waterfallsnorthwest.com/waterfall/Seahpo-Peak-Falls-4962", "https://www.waterfallsnorthwest.com/pictures/1311751298-Seahpo-Peak-Falls-WA-85-2.jpg", None, ""),
    30: (RISK, WEB / "1311757704-Sulphide-Creek-Falls-WA-83-2.jpg", "Northwest Waterfall Survey", "All rights reserved (© Northwest Waterfall Survey)",
         "https://www.waterfallsnorthwest.com/waterfall/Sulphide-Creek-Falls-3367", "https://www.waterfallsnorthwest.com/pictures/1311757704-Sulphide-Creek-Falls-WA-83-2.jpg", None, ""),
    31: (GEN, None, None, None, None, None, None, ""),
    32: (OK, WEB / "fl_46267954504_efa320d93f_o.jpg", "Stefan Serena", "CC0 1.0", "https://www.flickr.com/photos/146738176@N02/46267954504/",
         "https://live.staticflickr.com/7887/46267954504_efa320d93f_o.jpg", None, "Flickr 'Mardalsfossen, Norway'"),
    33: (OK, WEB / "fl_31440817111_b84e510e44_o.jpg", "VillageHero", "CC BY-SA 2.0", "https://www.flickr.com/photos/villagehero/31440817111/",
         "https://live.staticflickr.com/742/31440817111_b84e510e44_o.jpg", None, "Flickr 'Cascade Blanche 2'"),
    34: (RISK, WEB / "1735764090-DSC_0206.jpg", "World Waterfall Database", "All rights reserved (WWD: photos may not be used without written consent)",
         "https://www.worldwaterfalldatabase.com/waterfall/Sentinel-Fall-24", "https://www.worldwaterfalldatabase.com/pictures/1735764090-DSC_0206.jpg", None, ""),
}
GEN_PICK: dict[int, str] = {}   # idx → 生成图文件名后缀（重出时如 "b"），缺省 ""
# 风险项的默认版替代图：有可商用实拍就用它，不用 AI 图（审片第 1 轮 major #2 后补搜，2026-11-04）
ALT_PHOTO = {
    1: (WEB / "fl_39498453682_d1cf642587_k.jpg", "Mike and Lara Wolfe", "CC0 1.0", "https://www.flickr.com/photos/threepwolfe/39498453682/",
        "https://live.staticflickr.com/4682/39498453682_d1cf642587_k.jpg", (779, 0, 1802, 1365), "Flickr 'Tugela falls' (Amphitheatre, Royal Natal NP); cropped to the falls"),
}
FOCUS = {7: [0.7, 0.5]}   # Browne：瀑布在原图右侧（来源页图注「to the right」）


def licence_url(lic: str) -> str:
    low = lic.lower()
    if "pexels" in low: return "https://www.pexels.com/license/"
    if "unsplash" in low: return "https://unsplash.com/license"
    if "cc0" in low: return "https://creativecommons.org/publicdomain/zero/1.0/"
    if "public domain mark" in low: return "https://creativecommons.org/publicdomain/mark/1.0/"
    m = re.search(r"cc[ -]by(-sa)?\s*([\d.]+)?", low)
    if m:
        return f"https://creativecommons.org/licenses/{'by-sa' if m.group(1) else 'by'}/{m.group(2) or '4.0'}/"
    return ""


def save_jpg(src: Path, dst: Path, crop) -> tuple[int, int]:
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        if crop:
            im = im.crop(crop)
        if max(im.size) > LONG:
            im.thumbnail((LONG, LONG), Image.LANCZOS)
        dst.parent.mkdir(parents=True, exist_ok=True)
        im.save(dst, quality=90)
        return im.size


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    ledger = []
    counts = {OK: 0, RISK: 0, GEN: 0}
    for i, it in enumerate(data["items"]):
        kind, src, author, lic, page, url, crop, note = SPEC[i]
        counts[kind] += 1
        stem = Path(it["image"]).stem.replace("_gen", "")
        for k in ("image_risk", "image_note", "image_alt", "image_alt_credit", "image_focus"):
            it.pop(k, None)
        gen_rel = f"assets/img/{stem}_gen{GEN_PICK.get(i, '')}.png"
        if i in FOCUS:
            it["image_focus"] = FOCUS[i]
        if kind == RISK and i in ALT_PHOTO:
            asrc, aauth, alic, apage, aurl, acrop, anote = ALT_PHOTO[i]
            arel = f"assets/img/{stem}_alt.jpg"
            aw, ah = save_jpg(asrc, EP / arel, acrop)
            ledger.append({"file": arel, "source_page": apage, "source_url": aurl, "author": aauth, "licence": alic,
                           "licence_url": licence_url(alic), "attribution_required": not re.match(r"(public domain|pd|cc0|pexels|unsplash|pixabay)", alic, re.I),
                           "modified": f"{'cropped, ' if acrop else ''}downscaled to {aw}x{ah} px and re-encoded as JPEG; renderer crops to the card",
                           "sha256": sha(EP / arel), "retrieved_at": TODAY, "fop_note": "",
                           "selected_by": f"2026-11-04 QC follow-up: commercially licensed photo replaces the AI image in the default master ({anote})"})
        if kind in (RISK, GEN) and not (kind == RISK and i in ALT_PHOTO):
            g = EP / gen_rel
            if not g.exists():
                raise SystemExit(f"missing generated image for idx {i}: {gen_rel}")
            with Image.open(g) as im:
                gw, gh = im.size
            ledger.append({"file": gen_rel, "source_page": "", "source_url": "", "author": "AI-generated",
                           "licence": "AI-generated (Codex image_gen)", "licence_url": "", "attribution_required": False,
                           "modified": f"generated {gw}x{gh} px by Codex image_gen (ChatGPT subscription), prompt _build/gen_prompts/{i:02d}{GEN_PICK.get(i, '')}.txt; illustrative, not a photo of the real waterfall",
                           "sha256": sha(g), "retrieved_at": TODAY, "fop_note": "",
                           "selected_by": "follow-up 016/024: no commercially licensed photo found after Flickr CC / Pexels / Unsplash search; Codex used for generation only"})
        if kind == GEN:
            it["image"] = gen_rel
            it["image_credit"] = "AI-generated illustration"
            continue
        if CAND in src.parents:   # 候选来自下载步骤：来源页 / 直链以 meta.json 的原始记录为准
            m = next(x for x in json.loads((src.parent / "meta.json").read_text(encoding="utf-8")) if x["file"] == src.name)
            page, url = m.get("page_url") or page, m.get("image_url") or url
        rel = f"assets/img/{stem}.jpg"
        w, h = save_jpg(src, EP / rel, crop)
        ledger.append({"file": rel, "source_page": page, "source_url": url, "author": author, "licence": lic,
                       "licence_url": licence_url(lic), "attribution_required": not re.match(r"(public domain|pd|cc0|pexels|unsplash|pixabay)", lic, re.I),
                       "modified": f"{'cropped, ' if crop else ''}downscaled to {w}x{h} px and re-encoded as JPEG; renderer crops to the card",
                       "sha256": sha(EP / rel), "retrieved_at": TODAY, "fop_note": "",
                       "selected_by": ("follow-up 023: Claude search, checked by eye" + (f" ({note})" if note else "")) if kind == OK else
                       "follow-up 024 open-source search (licence unknown / all rights reserved): risk version only, user signs off before publishing"})
        it["image"] = rel
        it["image_credit"] = f"{author} / {lic.split(' (')[0]}"
        if kind == RISK:
            it["image_risk"] = "licence unknown"
            if i in ALT_PHOTO:
                it["image_alt"] = f"assets/img/{stem}_alt.jpg"
                it["image_alt_credit"] = f"{ALT_PHOTO[i][1]} / {ALT_PHOTO[i][2]}"
            else:
                it["image_alt"] = gen_rel
                it["image_alt_credit"] = "AI-generated illustration"
    (EP / "assets.json").write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (EP / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(counts, len(ledger), "ledger entries")


if __name__ == "__main__":
    main()
