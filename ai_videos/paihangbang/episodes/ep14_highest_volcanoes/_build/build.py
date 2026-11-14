# -*- coding: utf-8 -*-
"""ep14 data.json 生成：GVP Holocene 火山（WFS 2026-11-03 取数）按 GVP 海拔排序取前 50。
保留已有 data.json 里的图片字段（image / image_credit / image_focus / image_risk / image_alt*），只重算数据字段。"""
import json
from pathlib import Path

from items_def import ITEMS, eruption_tag

HERE = Path(__file__).resolve().parent
EP = HERE.parent
TODAY = "2026-11-03"
GVP_WFS = "https://webservices.volcano.si.edu/geoserver/GVP-VOTW/ows (Smithsonian_VOTW_Holocene_Volcanoes)"

# Wikipedia 交叉核对值（infobox elevation_m 或导言里的海拔；raw/wiki_extracts_2026-11-03.json）；None = 条目未给数值
WIKI = {355130: 6893, 355110: 6723, 355220: 6670, 355125: 6621, 354003: 6377, 355190: 6414, 355012: 6380,
        352071: 6263.47, 355107: None, 355131: 6215, 355123: 6137, 355160: 6095, 355020: 6071, 357020: 5856,
        355109: 6051, 355096: 6046, 355091: 5971, 354006: 5960, 355092: 5916, 352050: 5897, 355102: 5910,
        355124: 5906, 355090: 5884, 355011: 5860, 355101: 5852, 354040: 5815, 354010: 5822, 352006: 5790,
        355098: 5778, 352030: 5753, 355200: 5890, 355120: 5706, 355050: None, 355094: 5703, 232010: 5610,
        357010: 5682, 214010: 5642, 355095: 5631, 354060: None, 354020: 5672, 355093: 5076, 355100: 5592,
        341100: 5636, 355030: 5550, 354050: None, 355121: 5481, 355112: None, 355032: 5430, 355122: 5401,
        341090: 5393}

ISO = {"Chile": ("CL", "Chile"), "Argentina": ("AR", "Argentina"), "Bolivia": ("BO", "Bolivia"), "Peru": ("PE", "Peru"),
       "Ecuador": ("EC", "Ecuador"), "Iran": ("IR", "Iran"), "Russia": ("RU", "Russia"), "Mexico": ("MX", "Mexico")}
CONT = {"IR": "Asia", "RU": "Europe", "MX": "North America"}
# 审片修复 1：GVP WFS Elevation 字段错配的条目，用 GVP 同条目 Geological_Summary 的值（qc.md 问题 1）
ELEV_FIX = {357020: (5856, "GVP Geological Summary: 'San Jose is a 5856-m-high stratovolcano'; the WFS Elevation field (6,070 m) is the height of neighbouring Marmolejo.")}


def slug(s: str) -> str:
    import re, unicodedata
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def main() -> None:
    gvp = json.loads((HERE / "raw" / "gvp_holocene.json").read_text(encoding="utf-8"))
    props = [f["properties"] for f in gvp["features"]]
    for p in props:
        if p["Volcano_Number"] in ELEV_FIX:
            p["WFS_Elevation"] = p["Elevation"]
            p["Elevation"] = ELEV_FIX[p["Volcano_Number"]][0]
    rows = sorted(props, key=lambda p: -(p.get("Elevation") or -1e9))
    top = rows[:50]
    nxt = rows[50]
    old = {}
    if (EP / "data.json").exists():
        old = {it.get("gvp_volcano_number"): it for it in json.loads((EP / "data.json").read_text(encoding="utf-8"))["items"]}
    items = []
    for i, p in enumerate(top):
        vn = p["Volcano_Number"]
        name, sub, wiki, hint = ITEMS[vn]
        countries = p["Country"].split("-")
        iso, cname = ISO[countries[0]]
        elev = float(p["Elevation"])
        rank = i + 1
        it = {
            "rank": rank, "name": name, "subtitle": sub,
            "country_iso2": iso, "country_name": cname, "continent": CONT.get(iso, "South America"),
            "value": elev, "value_display": f"{elev:,.0f} m", "secondary_display": f"{round(elev * 3.28084):,} ft",
        }
        if len(countries) > 1:
            it["badge"] = f"SHARED WITH {countries[1].upper()}"
        elif p.get("Last_Eruption_Year") == 2026:
            it["badge"] = "ERUPTED IN 2026"
        tags = [{"icon": "calendar", "text": eruption_tag(p.get("Last_Eruption_Year"), p.get("Evidence_Category"))}]
        vtype = (p.get("Primary_Volcano_Type") or "").replace("(es)", "").replace("(s)", "s").replace("(pyroclastic)", "")
        if vtype and vtype != "Unknown":
            tags.append({"icon": "mountain", "text": vtype.strip()[:24]})
        it["tags"] = tags
        stem = f"{rank:02d}_{slug(name)}"
        prev = old.get(vn, {})
        it["image"] = prev.get("image", f"assets/img/{stem}.jpg")
        for k in ("image_credit", "image_focus", "image_risk", "image_alt", "image_alt_credit", "image_note", "thumb"):
            if k in prev:
                it[k] = prev[k]
        it["image_hint"] = hint
        it["source"] = {"name": f"Smithsonian GVP, Volcanoes of the World: {p['Volcano_Name']} ({vn})",
                        "url": f"https://volcano.si.edu/volcano.cfm?vn={vn}", "retrieved_at": TODAY}
        w = WIKI.get(vn)
        cc = {"name": f"Wikipedia: {wiki}", "url": "https://en.wikipedia.org/wiki/" + wiki.replace(" ", "_")}
        if w is not None:
            cc["value"] = w
            cc["diff_pct"] = round((w - elev) / elev * 100, 1)
        else:
            cc["value"] = None
        it["cross_check"] = cc
        notes = [f"GVP Holocene list; GVP country field '{p['Country']}'; type {p.get('Primary_Volcano_Type')}; "
                 f"last eruption {p.get('Last_Eruption_Year')} ({p.get('Evidence_Category')})."]
        if vn in ELEV_FIX:
            notes.append("CORRECTED: " + ELEV_FIX[vn][1])
            it["source"]["name"] += " - Geological Summary value"
        if w is not None and abs(cc["diff_pct"]) >= 1.0:
            notes.append(f"Wikipedia gives {w:,} m ({cc['diff_pct']:+.1f}%); ranking uses the GVP value throughout.")
        if rank == 50:
            notes.append(f"BOUNDARY: #51 is {nxt['Volcano_Name']} ({nxt['Elevation']} m GVP), {p['Elevation'] - nxt['Elevation']} m lower.")
        it["notes"] = " ".join(notes)
        it["gvp_volcano_number"] = vn
        items.append(it)

    data = {
        "episode": "ep14_highest_volcanoes",
        "title": "Highest Volcanoes in the World",
        "kicker": "TOP 50",
        "metric_label": "Active (Holocene) volcanoes by summit elevation",
        "unit": "m",
        "period_label": "Smithsonian GVP, Nov 2026",
        "source_line": "Source: Smithsonian GVP (VOTW) · Some images are AI-generated",
        "theme": "magma",
        "tally": {"by": "country", "title": "Volcanoes by country"},
        "scope_note": ("What counts: volcanoes on the Smithsonian Global Volcanism Program's Holocene list (activity in the "
                       "last ~11,700 years, including 6 that GVP lists with uncertain Holocene evidence), ranked by GVP's "
                       "summit elevation; San José uses the 5,856 m in GVP's own summary. Extinct volcanoes such as Kilimanjaro, "
                       "Sajama and Tupungato are not included. A border volcano shows the first country GVP lists, with a "
                       "SHARED WITH badge, and counts once in the country tally. Other surveys can differ by tens of metres."),
        "insights": json.loads((HERE / "insights.json").read_text(encoding="utf-8")) if (HERE / "insights.json").exists() else [],
        "layout": {"card_w": 720, "focus": [0.5, 0.4],
                   "image_prefer": ("the whole volcano clearly visible and recognisable (snow-capped cone, summit crater, "
                                    "eruption plume or its classic landscape view), the correct named volcano and not a "
                                    "neighbouring peak, landscape or portrait both fine")},
    }
    data["items"] = items
    (EP / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    from collections import Counter
    print(Counter(i["country_name"] for i in items).most_common())
    print(sum(1 for i in items if i.get("badge", "").startswith("SHARED")), "shared")


if __name__ == "__main__":
    main()
