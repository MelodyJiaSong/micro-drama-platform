# -*- coding: utf-8 -*-
"""items_def.py → data.json（保留已有 image / image_credit / image_focus / image_risk / image_alt 等图片字段）。"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
EP = HERE.parent
sys.path.insert(0, str(HERE))
from items_def import ITEMS  # noqa: E402

RETRIEVED = "2026-11-03"
OLD_VALUE_FIRST = {"lago_ohiggins", "lago_viedma", "lago_argentino", "issyk_kul", "salvatnet"}
KEEP = ("image", "image_credit", "image_focus", "image_risk", "image_note", "image_alt", "image_alt_credit")


def floor_tag(surface: float, depth: float) -> dict:
    x = surface - depth
    f = int(abs(x) + 0.5) * (-1 if x < 0 else 1)   # half away from zero (Baikal -1,186.5 -> -1,187)
    return {"icon": "map-pin", "text": f"Floor {abs(f):,} m {'below' if f < 0 else 'above'} sea"}


def main() -> None:
    old = {}
    p = EP / "data.json"
    if p.exists():
        for it in json.loads(p.read_text(encoding="utf-8"))["items"]:
            old[it["name"]] = it
    rows = sorted(ITEMS, key=lambda d: (-d["value"], d["name"]))
    items = []
    for i, d in enumerate(rows):
        rank = 1 + sum(1 for x in rows if x["value"] > d["value"])
        approx = "~" if d.get("approx") else ""
        ft = round(d["value"] * 3.28084)
        tags = [floor_tag(d["surface"], d["value"])]
        if d.get("tag2"):
            t2 = {"icon": d["tag2"][0], "text": d["tag2"][1]}
            # 改正旧值的标签（D2）放第一个：渲染器从后往前丢标签（QC 2026-11-04 minor 2）
            if d["key"] in OLD_VALUE_FIRST:
                tags.insert(0, t2)
            else:
                tags.append(t2)
        xv = d["xc"][2]
        it = {
            "rank": rank, "name": d["name"], "subtitle": d["subtitle"],
            "country_iso2": d["iso2"], "country_name": d["country"], "continent": d["continent"],
            "value": d["value"], "value_display": f"{approx}{d['value']:,} m", "secondary_display": f"{approx}{ft:,} ft",
            "badge": d["badge"], "tags": tags,
            "image": f"assets/img/{rank:02d}_{d['key']}.jpg",
            "image_hint": d["hint"],
            "source": {"name": d["src"][0], "url": d["src"][1], "tier": d["src"][2], "method": d["src"][3], "retrieved_at": RETRIEVED},
            "cross_check": {"name": d["xc"][0], "url": d["xc"][1], "value": xv, "diff_pct": round(abs(d["value"] - xv) / d["value"] * 100, 1)},
            "surface_m": d["surface"], "surface_source": d["surface_src"],
            "notes": d["notes"],
        }
        if not it["badge"]:
            del it["badge"]
        prev = old.get(d["name"])
        if prev:
            for k in KEEP:
                if k in prev:
                    it[k] = prev[k]
        items.append(it)
    data = {
        "episode": "ep15_deepest_lakes",
        "title": "Deepest Lakes in the World",
        "kicker": f"TOP {len(items)}",
        "metric_label": "Maximum depth",
        "unit": "m",
        "period_label": "Data as of Nov 2026",
        "source_line": "Sources: lake surveys & papers, ILEC, FAO, USGS, NVE, Wikipedia",
        "theme": "abyss",
        "tally": {"by": "continent", "title": "Deep lakes by continent"},
        "items": items,
        "insights": [
            {"after_rank": 30, "text": "Old lists: Poso 450 m, Wakatipu 420 m. Surveys show 395 m and ~380 m, so both are out."},
            {"after_rank": 17, "text": "Next: Sarez Lake, born in 1911 when a quake-triggered landslide dammed a Pamir river."},
            {"after_rank": 11, "text": "Three of the top 10 are Patagonian lakes, carved by glaciers that are still retreating."},
            {"after_rank": 6, "text": "Next: Viedma. A 2022 survey reported 900 m (unpublished); peer-reviewed sonar: ~750 m."},
            {"after_rank": 2, "text": "Next, No. 1: a lake holding about 20% of the world's unfrozen fresh water (UNESCO)."},
        ],
        "scope_note": ("What counts: natural lakes whose maximum measured depth exceeds 400 m, ranked by that depth "
                       "(metres; feet = m x 3.28084). Natural lakes raised by a small dam (Lake Chelan) count; reservoirs and "
                       "subglacial lakes such as Vostok do not. The Caspian Sea is counted as a lake. Where surveys disagree we use "
                       "the latest published sounding and flag DEPTH DISPUTED. Shared lakes show the flag of the country with the "
                       "largest share of the lake (Caspian: longest shoreline, though its deepest point is in the South Caspian). Equal depths share a rank."),
        "layout": {"card_w": 720, "focus": [0.5, 0.5], "intro_hold": 2.5,
                   "image_prefer": ("a real landscape photograph of this specific lake: wide view of the water with its "
                                    "characteristic shoreline, mountains, glacier or island, clear weather and strong colour, "
                                    "landscape orientation preferred; no people as the main subject, no buildings dominating")},
    }
    (EP / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(items)} items; last rank {items[-1]['rank']}")
    for it in items:
        print(it["rank"], it["name"], it["value_display"], it["country_iso2"], it["continent"], "|", " · ".join(t["text"] for t in it["tags"]), "|", it.get("badge", ""))
    for x in data["insights"]:
        print(len(x["text"]), x["text"])
    print("scope", len(data["scope_note"]), "source_line", len(data["source_line"]))


if __name__ == "__main__":
    main()
