# -*- coding: utf-8 -*-
"""ep19：items_def.py + research/*.json + landmarks.py → ../data.json（保留已有的 image / image_credit / image_focus /
image_risk / image_alt 等找图字段）。用法：python -I _build/build.py"""
import json
import re
import sys
import unicodedata
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
EP = HERE.parent
sys.path.insert(0, str(HERE))
from items_def import CROSS, INSIGHTS, ROWS  # noqa: E402
from landmarks import LANDMARKS  # noqa: E402

RETRIEVED = "2026-11-03"
UN_DB = {"name": "UN Tourism Statistics Database (bulk download 12/2025), inbound overnight visitors (tourists)",
         "url": "https://www.untourism.int/tourism-statistics/tourism-statistics-database", "retrieved_at": RETRIEVED}
SRC_NAME = {  # 屏外描述框也只用英文：调研 JSON 里带中文说明的来源名改写
    "Türkiye": "Invest in Türkiye: Tourism sector (citing the UN Tourism World Tourism Barometer)",
    "Greece": "Bank of Greece: balance of travel services, December 2024 (press release via abnase.com)",
    "Thailand": "Ministry of Tourism and Sports 2024 foreign arrivals (via Sripatum University summary)",
    "Ireland": "CSO Inbound Tourism December 2024, Table 1 (annual total)",
    "Switzerland": "Eurostat tour_occ_arnat: non-resident arrivals, commercial accommodation (BFS data)",
    "Sweden": "Eurostat tour_occ_arnat: non-resident arrivals, commercial accommodation (Swedish data)",
    "Norway": "Eurostat tour_occ_arnat: non-resident arrivals, commercial accommodation (SSB data)",
    "France": "Atout France: Une année 2024 record pour le tourisme français (press release)",
}
KEEP = ("image", "image_credit", "image_focus", "image_risk", "image_note", "image_alt", "image_alt_credit")
LM_KEY = {"Hong Kong": "Hong Kong", "Macao": "Macao", "South Korea": "South Korea", "Vietnam": "Viet Nam",
          "Taiwan": "Taiwan", "Dominican Rep.": "Dominican Republic", "Türkiye": "Türkiye"}


def slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def sig3(v: float) -> str:
    """3 位有效数字（bible §3.4），百万为单位。"""
    d = Decimal(str(v))
    q = Decimal("1") if v >= 100 else Decimal("0.1") if v >= 10 else Decimal("0.01")
    return f"{d.quantize(q, rounding=ROUND_HALF_UP)}M"


def change(v: float, base: float, year: int) -> tuple[str, float]:
    pct = (v / base - 1) * 100
    r = int(Decimal(str(abs(pct))).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    if r == 0:
        return f"≈ {year} level", pct
    return f"{'▲' if pct > 0 else '▼'} {r}% vs {year}", pct


def research() -> dict:
    out = {}
    for g in ("europe", "asia", "africa_americas", "extra"):
        for r in json.loads((HERE / "research" / f"{g}.json").read_text(encoding="utf-8")):
            out[r["country"]] = r
    return out


def main() -> None:
    res = research()
    old = {}
    if (EP / "data.json").exists():
        for it in json.loads((EP / "data.json").read_text(encoding="utf-8"))["items"]:
            old[it["country_iso2"]] = it
    rows = sorted(ROWS, key=lambda r: -r[5])
    items = []
    for i, (key, name, iso, region, cont, v, by, base, src, badge, tags, note) in enumerate(rows, 1):
        r = res.get(key, {})
        lm = LANDMARKS[LM_KEY.get(name, name)]
        sec, pct = change(v, base, by)
        if src == "db":
            source = dict(UN_DB)
        else:
            s = r.get("v2024_source") or {}
            source = {"name": SRC_NAME.get(key) or re.sub(r"[（(][^）)]*[一-鿿][^）)]*[）)]", "", s.get("name", "")).strip(),
                      "url": s.get("url") or "", "retrieved_at": RETRIEVED}
        cc = r.get("cross_check") or {}
        cross = None
        if cc.get("value_2024") is not None and cc.get("url"):
            cross = {"name": cc.get("name", ""), "url": cc["url"], "value": cc["value_2024"],
                     "diff_pct": round(abs(cc["value_2024"] - v) / v * 100, 1)}
        if key in CROSS:
            c = CROSS[key]
            cross = {**c, "diff_pct": round(abs(c["value"] - v) / v * 100, 1)}
        it = {
            "rank": i, "name": name, "subtitle": lm[1], "country_iso2": iso, "country_name": region, "continent": cont,
            "value": v, "value_display": sig3(v), "secondary_display": sec,
            "change_pct": round(pct, 1), "change_base": {"year": by, "value": base},
            "badge": badge, "tags": tags,
            "image": f"assets/img/{i:02d}_{slug(name)}.jpg",
            "image_hint": f"Photograph of {lm[0]} ({name}): {lm[3]}",
            "landmark": lm[0],
            "source": source, "cross_check": cross,
            "notes": note,
        }
        prev = old.get(iso.lower()) or old.get(iso)
        if prev:
            for k in KEEP:
                if k in prev:
                    it[k] = prev[k]
        items.append(it)
    cont_count: dict[str, int] = {}
    for it in items:
        cont_count[it["continent"]] = cont_count.get(it["continent"], 0) + 1
    data = {
        "episode": "ep19_most_visited_countries",
        "title": "Most Visited Countries in the World",
        "kicker": "TOP 50",
        "metric_label": "International tourist arrivals",
        "unit": "M",
        "period_label": "Data: 2024 full year",
        "source_line": "Sources: UN Tourism, national tourism statistics",
        "theme": "voyage",
        "tally": {"by": "continent", "title": "Countries by continent"},
        "items": items,
        "insights": INSIGHTS,
        "scope_note": ("What counts: international tourist arrivals in 2024 (overnight visitors, millions) as compiled by UN Tourism; "
                       "where its database has no 2024 value, the national figure from the same series is used. Some countries count "
                       "at the border, others at hotels, and a few include same-day visits or citizens living abroad (noted on the card). "
                       "Hong Kong and Macao are listed separately, as UN Tourism does. Not ranked for lack of a 2024 figure: China, UAE, "
                       "Denmark, Bulgaria, Russia. Change vs 2019 uses the same series."),
        "layout": {"card_w": 720, "focus": [0.5, 0.45],
                   "image_prefer": ("the specific landmark named in the subject note, instantly recognisable in its classic postcard view, "
                                    "a landscape travel photograph with strong natural colour (blue sky, golden hour or blue hour); "
                                    "the landmark fills the frame and is centred; no people as the main subject; landscape orientation preferred")},
    }
    for k in ("image_prefer",):
        pass
    old_top = json.loads((EP / "data.json").read_text(encoding="utf-8")) if (EP / "data.json").exists() else {}
    if old_top.get("layout"):
        data["layout"] = {**data["layout"], **{k: v for k, v in old_top["layout"].items() if k not in ("image_prefer",)}}
    (EP / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not (EP / "assets.json").exists():
        (EP / "assets.json").write_text("[]\n", encoding="utf-8")
    print(f"{len(items)} items; scope_note {len(data['scope_note'])} chars; continents {cont_count}")
    for it in items:
        print(f"{it['rank']:>2} {it['name']:<15} {it['value_display']:>6}  {it['secondary_display']:<18} {it['badge']}")


if __name__ == "__main__":
    main()
