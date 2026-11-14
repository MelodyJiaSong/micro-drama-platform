# -*- coding: utf-8 -*-
"""ep12 data.json 生成：主值 UN DYB 2024 Table 3（Sudan 例外用 World Bank），交叉核对 CIA World Factbook
（2026-01 最终版，factbook.json CC0 镜像）。重跑会保留已有 data.json 里的图片相关字段与 layout。

    python build.py        # 在 _build/ 下运行
"""
import json
import re
import unicodedata
from pathlib import Path

from items_def import BADGES, BOUNDARY, COUNTRIES, NOTES, REGION, TAGS

B = Path(__file__).parent
R = B / "raw"
EP = B.parent
TODAY = "2026-11-03"
DYB_URL = "https://unstats.un.org/unsd/demographic-social/products/dyb/documents/dyb2024/table03.pdf"
FB_URL = "https://github.com/factbook/factbook.json"
WB_URL = "https://data.worldbank.org/indicator/AG.SRF.TOTL.K2"
SQMI = 0.386102158542446

# DYB 行名关键词（raw/dyb2024_area_rows.json 里 name 字段的唯一子串）
DYB_KEY = {"RU": "Russian Federation", "CA": "Canada", "US": "United States of America", "CN": "China - Chine", "BR": "Brazil",
           "AU": "Australia - Australie", "IN": "India - Inde", "KZ": "Kazakhstan", "DZ": "Algeria",
           "CD": "démocratique du Congo", "SA": "Saudi Arabia", "MX": "Mexico", "LY": "Libya",
           "IR": "Iran (République", "MN": "Mongolia", "PE": "Peru", "TD": "Chad", "NE": "Niger", "AO": "Angola", "ML": "Mali",
           "ZA": "South Africa", "CO": "Colombia", "ET": "Ethiopia", "BO": "Bolivia", "MR": "Mauritania", "EG": "Egypt",
           "TZ": "Tanzanie", "VE": "Venezuela", "NG": "Nigeria", "NA": "Namibia", "MZ": "Mozambique", "PK": "Pakistan",
           "TR": "Türkiye", "CL": "Chile - Chili", "ZM": "Zambia", "MM": "Myanmar", "SS": "South Sudan", "AF": "Afghanistan",
           "SO": "Somalia", "CF": "Central African", "UA": "Ukraine", "KE": "Kenya", "MG": "Madagascar", "BW": "Botswana",
           "FR": "France", "YE": "Yemen", "TH": "Thailand", "ES": "Spain", "TM": "Turkmenistan", "CM": "Cameroon",
           "PG": "Papua New Guinea", "GL": "Greenland", "HK": "Hong Kong"}


def dyb_values() -> dict:
    rows = json.load(open(R / "dyb2024_area_rows.json", encoding="utf-8"))
    out = {}
    for iso, key in DYB_KEY.items():
        hits = [r for r in rows if key in r["name"] and re.match(r"^\d", r["area_raw"])]
        if iso == "NE":
            hits = [r for r in hits if "Nigeria" not in r["name"]]
        assert len(hits) == 1, (iso, hits)
        p = hits[0]["area_raw"].split()
        out[iso] = (int(p[0] + "".join(x[:3] for x in p[1:])) if len(p) > 1 else int(p[0]), hits[0]["page"])
    # 脚注上标与数字粘连、列位置偏移的两项，按 PDF 逐字核读（sources.md §2）：
    out["AR"] = (2796427, 4)   # "2 796 427" + footnote 68
    out["ID"] = (1892410, 6)   # "1 892 410" + footnote 97
    out["HK"] = (1115, 5)
    return out


def fb_values() -> dict:
    d = json.load(open(R / "factbook_area.json", encoding="utf-8"))

    def num(s):
        m = re.match(r"([\d,.]+)\s*(million)?\s*sq km", s or "")
        if not m:
            return None
        v = float(m.group(1).replace(",", ""))
        return v * 1e6 if m.group(2) else v
    return {k: {kk: num(vv) for kk, vv in v["area"].items()} for k, v in d.items()}


def wb_values(ind: str) -> dict:
    d = json.load(open(R / f"wb_{ind}.json"))[1]
    out = {}
    for r in d:
        if r["value"] is None:
            continue
        k = r["countryiso3code"]
        if k not in out or r["date"] > out[k][0]:
            out[k] = (r["date"], r["value"])
    return out


def sig3(v: float) -> str:
    """3 位有效数字（bible §3.4）：≥1M 用 M，其余整数加千分位。"""
    if v >= 1e6:
        x = v / 1e6
        return f"{x:.1f}M" if x >= 10 else f"{x:.2f}M"
    e = len(str(int(v))) - 3
    return f"{int(round(v / 10 ** e) * 10 ** e):,}"


def main() -> None:
    dyb, fb, wb, wbl = dyb_values(), fb_values(), wb_values("AG.SRF.TOTL.K2"), wb_values("AG.LND.TOTL.K2")
    old_data = json.load(open(EP / "data.json", encoding="utf-8")) if (EP / "data.json").exists() else {}
    old = {it["country_iso2"]: it for it in old_data.get("items", [])}
    rows = []
    for iso2, iso3, fbp, name, cont, place, hint in COUNTRIES:
        if iso2 == "SD":
            val = wb[iso3][1]
            src = {"name": "World Bank WDI AG.SRF.TOTL.K2, 2024 (FAO; CC BY 4.0); no value in UN DYB 2024", "url": WB_URL, "retrieved_at": TODAY}
        else:
            val = dyb[iso2][0]
            src = {"name": f"UN Demographic Yearbook 2024, Table 3, surface area 2024 (p.{dyb[iso2][1]})", "url": DYB_URL, "retrieved_at": TODAY}
        rows.append(dict(iso2=iso2, iso3=iso3, name=name, cont=cont, place=place, hint=hint, value=val, src=src,
                         fb=fb[fbp]["total"], fb_land=fb[fbp].get("land"), fb_water=fb[fbp].get("water"),
                         wb=wb.get(iso3, (None, None))[1], wb_land=wbl.get(iso3, (None, None))[1]))
    rows.sort(key=lambda r: -r["value"])
    items = []
    for i, r in enumerate(rows):
        rank = i + 1
        o = old.get(r["iso2"], {})
        slug = re.sub(r"[^a-z0-9]+", "_", unicodedata.normalize("NFKD", r["name"]).encode("ascii", "ignore").decode().lower()).strip("_")
        it = {"rank": rank, "name": r["name"], "subtitle": r["place"], "country_iso2": r["iso2"], "country_name": REGION[r["iso2"]],
              "continent": r["cont"], "value": r["value"],
              "value_display": f"{sig3(r['value'])} km²", "secondary_display": f"{sig3(r['value'] * SQMI)} sq mi"}
        if r["iso2"] in BADGES:
            it["badge"] = BADGES[r["iso2"]]
        it["tags"] = [{"icon": a, "text": b} for a, b in TAGS.get(r["iso2"], [])]
        it["image"] = o.get("image") or f"assets/img/{rank:02d}_{slug}.jpg"
        for k in ("image_credit", "image_focus", "image_risk", "image_note", "image_alt", "image_alt_credit"):
            if k in o:
                it[k] = o[k]
        it["image_hint"] = o.get("image_hint") or r["hint"]
        it["source"] = r["src"]
        it["cross_check"] = {"name": "CIA World Factbook, final edition (Jan 2026, public domain)", "url": FB_URL,
                             "value": r["fb"], "diff_pct": round(abs(r["fb"] - r["value"]) / r["value"] * 100, 2)}
        it["notes"] = NOTES.get(r["iso2"], "")
        it["extra"] = {"wb_2024_surface_km2": r["wb"], "wb_2024_land_km2": r["wb_land"],
                       "fb_land_km2": r["fb_land"], "fb_water_km2": r["fb_water"]}
        items.append(it)
    data = {
        "episode": "ep12_largest_countries_by_area",
        "title": "Largest Countries in the World by Area",
        "kicker": "TOP 50",
        "metric_label": "Total area (land + inland water)",
        "unit": "km²",
        "period_label": "Data as of 2024",
        "source_line": "Sources: UN Demographic Yearbook 2024, CIA World Factbook",
        "theme": "atlas",
        "tally": {"by": "continent", "title": "Countries by continent"},
        "items": items,
        "insights": json.load(open(B / "insights.json", encoding="utf-8")),
        "scope_note": json.load(open(B / "scope_note.json", encoding="utf-8")),
        "layout": old_data.get("layout") or {
            "card_w": 720, "focus": [0.5, 0.5],
            "image_prefer": ("the exact named natural landscape or landform, the classic recognisable view, wide landscape, "
                             "vivid natural colour, no people as the main subject, no modern buildings, no maps or flags")},
    }
    (EP / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for it in items:
        print(it["rank"], it["country_iso2"], it["value"], it["value_display"], it["secondary_display"],
              it["cross_check"]["value"], it["cross_check"]["diff_pct"], it["extra"]["wb_2024_surface_km2"])
    for iso2, iso3, fbp, name in BOUNDARY:
        print("BOUNDARY", name, dyb.get(iso2), fb[fbp]["total"], wb.get(iso3))
    print("Greenland", dyb.get("GL"), "HK", dyb.get("HK"))


if __name__ == "__main__":
    main()
