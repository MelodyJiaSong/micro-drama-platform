# -*- coding: utf-8 -*-
"""items_def.py + hints.py → data.json（保留已有的 image / image_credit / image_alt / image_focus 等图片字段）。

    python ai_videos/paihangbang/episodes/ep13_tallest_statues/_build/build.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EP = HERE.parent
sys.path.insert(0, str(HERE))
from items_def import ITEMS, WPL  # noqa: E402
from hints import hint  # noqa: E402

TODAY = "2026-11-03"
FT = 3.28084

# 所在国对「雕塑的商用复制」有无全景自由（依据见 sources.md §3；Commons 各国 FoP 页 + 法条）
FOP_REASON = {
    "JP": "FoP: Japan Copyright Act Art. 46(iv) excludes artistic works reproduced for sale; sculpture not covered for commercial use",
    "TW": "FoP: Taiwan Copyright Act Art. 58(4) same as Japan; sculpture not covered for commercial use",
    "PH": "FoP: Philippines IP Code has no freedom of panorama",
    "MM": "FoP: Myanmar Copyright Law 2019 has no freedom of panorama",
    "ID": "FoP: Indonesia Copyright Law 2014 has no commercial freedom of panorama",
    "VN": "FoP: Vietnam IP Law (2022 amendment) allows only non-commercial use",
    "RU": "FoP: Russia Civil Code Art. 1276 excludes sculpture used as main subject / for profit",
    "UA": "FoP: Ukraine Copyright Law 2022 Art. 22(10) only without independent economic value",
    "BT": "FoP: Bhutan Copyright Act 2001 has no freedom of panorama",
    "SN": "FoP: Senegal Copyright Law 2008 Art. 46 excludes commercial use as main subject",
}


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower().replace("'", "")).strip("_")


def disp(v: float) -> str:
    if v >= 100 or float(v).is_integer():
        return f"{round(v):,} m"
    if v < 100:
        s = f"{v:.1f}"
        return f"{s} m"
    return f"{v} m"


def ranks(vals: list[float]) -> list[int]:
    out = []
    for i, v in enumerate(vals):
        out.append(out[-1] if i and v == vals[i - 1] else i + 1)
    return out


def tags_for(it: dict) -> list[dict]:
    tags = []
    if it.get("tag_total"):
        tags.append({"icon": "ruler", "text": it["tag_total"]})
    elif it.get("total") and it["total"] - it["value"] >= 1:
        tags.append({"icon": "ruler", "text": f"{disp(it['total'])} with base"})
    y = it.get("year")
    if it["name"] == "Leshan Giant Buddha":
        tags.append({"icon": "calendar", "text": "Carved 713–803 AD"})
    elif it.get("tag_year"):
        tags.append({"icon": "calendar", "text": it["tag_year"]})
    elif y:
        tags.append({"icon": "calendar", "text": f"Completed {y}"})
    return tags[:2]


def main() -> None:
    items_src = sorted(ITEMS, key=lambda d: -d["value"])
    rk = ranks([d["value"] for d in items_src])
    old = {}
    dp = EP / "data.json"
    if dp.exists():
        for o in json.loads(dp.read_text(encoding="utf-8"))["items"]:
            old[o["name"]] = o
    items = []
    for i, (it, r) in enumerate(zip(items_src, rk), 1):
        o = old.get(it["name"], {})
        rec = {
            "rank": r,
            "name": it["name"],
            "subtitle": it["subtitle"],
            "country_iso2": it["iso2"],
            "country_name": it["country"],
            "continent": it["continent"],
            "value": it["value"],
            "value_display": disp(it["value"]),
            "secondary_display": f"{round(it['value'] * FT):,} ft",
        }
        if it.get("badge"):
            rec["badge"] = it["badge"]
        rec["tags"] = tags_for(it)
        rec["image"] = o.get("image") or f"assets/img/{i:02d}_{slug(it['name'])}.jpg"
        for k in ("image_credit", "image_alt", "image_alt_credit", "image_focus", "image_note"):
            if o.get(k):
                rec[k] = o[k]
        rec["image_hint"] = hint(it["name"])
        risks = [x for x in str(o.get("image_risk") or "").split("; ") if x and not x.startswith("FoP:")]
        if it["fop"] == "risk":
            risks.insert(0, FOP_REASON[it["iso2"]])
        if risks:
            rec["image_risk"] = "; ".join(risks)
        rec["source"] = {"name": it["src"][0], "url": it["src"][1], "retrieved_at": TODAY}
        if it.get("cross") is not None:
            rec["cross_check"] = {"name": WPL[0], "url": WPL[1], "value": it["cross"],
                                  "diff_pct": round(abs(it["value"] - it["cross"]) / it["value"] * 100, 1)}
        rec["total_height_m"] = it.get("total")
        rec["fop"] = it["fop"]
        rec["notes"] = it["notes"]
        items.append(rec)

    data = {
        "episode": "ep13_tallest_statues",
        "title": "Tallest Statues in the World",
        "kicker": f"TOP {len(items)}",
        "metric_label": "Statue height",
        "unit": "m",
        "period_label": "Completed statues, Nov 2026",
        "source_line": "Sources: builders, governments & news; Wikipedia cross-check",
        "theme": "monument",
        "tally": {"by": "country", "title": "Statues by country"},
        "items": items,
        "insights": json.loads((HERE / "insights.json").read_text(encoding="utf-8")) if (HERE / "insights.json").exists() else [],
        "scope_note": ("What counts: completed statues (free-standing figures of people, gods or animals, busts included). "
                       "Height = the figure itself, from its feet or seat to the highest point of the figure, "
                       "including anything it holds (a sword, a torch), but not its lotus throne, pedestal, building or hill; "
                       "totals with the base are shown on each card. Reclining statues and statues still under construction "
                       "are not included. Equal heights share a rank. Listed under the country where the statue stands; "
                       "Hong Kong is counted under China."),
        "layout": {"card_w": 600, "focus": [0.5, 0.2],
                   "image_prefer": "the WHOLE statue clearly visible from head to feet/base (never cropped), the classic "
                                   "recognisable view of that exact statue, portrait orientation preferred, sky behind the head"},
    }
    dp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"data.json: {len(items)} items; ranks {rk[0]}..{rk[-1]}")
    from collections import Counter
    print(Counter(d["country_name"] for d in items).most_common())
    print("FoP risk:", sum(1 for d in items if d["fop"] == "risk"))


if __name__ == "__main__":
    main()
