# -*- coding: utf-8 -*-
"""items_def.py → ../data.json（保留已有 image / image_credit / image_risk / image_alt / image_focus / image_hint 等图片字段）。"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from items_def import ITEMS  # noqa: E402
from img_hints import H  # noqa: E402

EP = Path(__file__).resolve().parents[1]
WP = json.loads((EP / "_build" / "raw" / "wp_rows.json").read_text(encoding="utf-8"))
WP_URL = "https://en.wikipedia.org/wiki/List_of_river_systems_by_length"
WP_REV = json.loads((EP / "_build" / "raw" / "wp_list.json").read_text(encoding="utf-8"))["parse"]["revid"]
LIU = ("Liu et al. 2009, Int. J. Digital Earth 2(1):80-87 (satellite + field survey)", "https://doi.org/10.1080/17538940902746082")
IMG_KEYS = ("image", "image_credit", "image_risk", "image_note", "image_alt", "image_alt_credit", "image_focus")


def wp_row(name):
    for r in WP:
        if r["river"].lower().startswith(name.lower()):
            return r
    for r in WP:
        if any(part.strip().lower().startswith(name.lower()) for part in re.split(r"[–-]", r["river"])):
            return r
    raise KeyError(name)


def mi(km):
    return round(km * 0.621371)


def main():
    old = {}
    p = EP / "data.json"
    if p.exists():
        for it in json.loads(p.read_text(encoding="utf-8"))["items"]:
            old[it["key"]] = {k: it[k] for k in IMG_KEYS if k in it}
    rows = sorted(ITEMS, key=lambda d: (-d["km"], d["name"]))
    items, prev, rank = [], None, 0
    for i, d in enumerate(rows):
        if d["km"] != prev:
            rank = i + 1
        prev = d["km"]
        if d.get("wp"):
            r = wp_row(d["wp"])
            cc_val = r["km"]
            cross = {"name": f"Wikipedia: List of river systems by length (revid {WP_REV}), row '{r['river'][:60]}'", "url": WP_URL,
                     "value": cc_val, "diff_pct": round(abs(cc_val - d["km"]) / d["km"] * 100, 1)}
        else:
            cross = {"name": d["xc"][0], "url": d["xc"][1], "value": d["xc"][2], "diff_pct": round(abs(d["xc"][2] - d["km"]) / d["km"] * 100, 1)}
        it = {
            "rank": rank, "key": d["key"], "name": d["name"], "subtitle": d["subtitle"],
            "country_iso2": d["iso2"], "country_name": f"Ends in {d['country']}", "continent": d["continent"],
            "value": d["km"], "value_display": f"{d['km']:,} km", "secondary_display": f"{mi(d['km']):,} mi",
        }
        if d.get("badge"):
            it["badge"] = d["badge"]
        tags = [{"icon": d["tag"][0], "text": d["tag"][1]}]
        if d.get("extra"):
            tags.append({"icon": d["extra"][0], "text": d["extra"][1]})
        it["tags"] = tags
        it["image"] = f"assets/img/{rank:02d}_{d['key']}.jpg"
        it["source"] = {"name": d["src"][0], "url": d["src"][1], "quote": d["quote"], "tier": d.get("tier", "primary (reference work)"),
                        "retrieved_at": "2026-11-03"}
        it["cross_check"] = cross
        if d.get("xc2"):
            it["cross_check_2"] = {"name": d["xc2"][0], "url": d["xc2"][1], "value": d["xc2"][2], "diff_pct": round(abs(d["xc2"][2] - d["km"]) / d["km"] * 100, 1)}
        if d.get("liu"):
            it["cross_check_2"] = {"name": LIU[0], "url": LIU[1], "value": d["liu"], "diff_pct": round(abs(d["liu"] - d["km"]) / d["km"] * 100, 1)}
        it["notes"] = d.get("notes", "")
        view, avoid = H[d["key"]]
        it["image_hint"] = (f"show {view}; {avoid}; if those exact views are not freely licensed, any sharp, colourful real photo "
                            f"in which this specific river is clearly the subject is acceptable (free licences first: Pexels, Unsplash, Pixabay, Flickr CC BY / CC BY-SA / CC0)")
        for k, v in old.get(d["key"], {}).items():
            # 图片路径一律保留（文件名里的名次前缀只是初版名次，2026-11-04 QC 后名次变动不改名）
            it[k] = v
        items.append(it)

    rk = {it["key"]: it["rank"] for it in items}
    insights = []
    for key, text in INSIGHTS_DEF:
        if key.endswith("@after"):
            insights.append({"after_rank": rk[key[:-6]], "text": text})
        else:
            insights.append({"after_rank": rk[key] + 1, "text": text})
    data = {
        "episode": "ep17_longest_rivers",
        "title": "Longest Rivers in the World",
        "kicker": "TOP 50",
        "metric_label": "Length",
        "unit": "km",
        "period_label": "Flag = where the river ends · Data as of Nov 2026",
        "source_line": "Sources: Encyclopaedia Britannica, Geoscience Australia",
        "theme": "delta",
        "tally": {"by": "continent", "title": "Rivers by continent"},
        "scope_note": ("Lengths as published by Encyclopaedia Britannica, to the farthest source where Britannica gives a river-system "
                       "figure (Mississippi–Missouri, Ob–Irtysh). Exceptions: Murray–Darling uses Geoscience Australia (Britannica gives only "
                       "its parts); Zambezi and Orinoco use the common figure, as Britannica's is 25%+ off for the same source and mouth. "
                       "Rivers inside a longer listed system are not repeated; big tributaries are. Flag = country where the river ends "
                       "(sea, lake or a bigger river)."),
        "insights": insights,
        "layout": {"card_w": 720, "focus": [0.5, 0.5], "intro_hold": 2.5,
                   "image_prefer": ("an iconic, instantly recognisable real photograph of THIS river: the river itself clearly visible as the subject "
                                    "(water, banks, bends, delta or gorge), a famous stretch, city or landmark on its banks; landscape orientation; "
                                    "aerial or elevated views welcome; no maps, no satellite false-colour imagery, no tiny river in a huge landscape")},
        "items": items,
    }
    if len(data["scope_note"]) > 600:
        raise SystemExit(f"scope_note too long {len(data['scope_note'])}")
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for it in items:
        print(it["rank"], it["name"], it["value_display"], it["country_name"], it["continent"], it["cross_check"]["value"], it["cross_check"]["diff_pct"])
    from collections import Counter
    print(Counter(i["continent"] for i in items).most_common())


INSIGHTS_DEF = [   # (显示在哪一项「之后」：该项名次；key 指下一张卡的河，after = 其名次 + 1)
    ("colorado", "Next: the Colorado. Dams and farms now take so much water it rarely reaches the sea."),
    ("ganges", "Next: the Ganges. It meets the Brahmaputra in Bangladesh and they share one huge delta."),
    ("danube", "Next: the Danube. It flows through 10 countries on its way to the Black Sea."),
    ("purus", "The next 3 rivers are only tributaries of the Amazon, yet each is longer than the Danube."),
    ("mekong", "Britannica gives the Mekong 4,350 km. A 2009 satellite survey measured 4,909 km."),
    ("amazon@after", "In 2008 Brazil's INPE measured the Amazon at 6,992 km. Is the Nile really No. 1?"),
]
INSIGHTS = []

if __name__ == "__main__":
    for x in [{"text": t} for _, t in INSIGHTS_DEF]:
        assert len(x["text"]) <= 90, (len(x["text"]), x["text"])
    main()
