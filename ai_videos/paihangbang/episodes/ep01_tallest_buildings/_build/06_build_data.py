"""Build data.json from CTBUH (primary), Wikidata (cross-check), Wikipedia list (fallback cross-check),
entity mapping and the selected images.

Usage: python -I 06_build_data.py <build_dir> <episode_dir>
Reads: ctbuh_top100.json, entities.json, wikidata.json, raw/wp_tallest.json, images.json (optional)
Writes: <episode_dir>/data.json and <build_dir>/crosscheck_report.json
"""
import json
import os
import re
import sys
from collections import Counter

RETRIEVED = "2026-11-03"
COUNTRY = {"AE": "United Arab Emirates", "MY": "Malaysia", "CN": "China", "SA": "Saudi Arabia", "KR": "South Korea",
           "US": "United States", "TW": "Taiwan", "RU": "Russia", "VN": "Vietnam", "KW": "Kuwait", "EG": "Egypt"}
CONTINENT = {"AE": "Asia", "MY": "Asia", "CN": "Asia", "SA": "Asia", "KR": "Asia", "US": "North America",
             "TW": "Asia", "RU": "Europe", "VN": "Asia", "KW": "Asia", "EG": "Africa"}
FT = 0.3048

# Explanations of cross-check differences > 0.5 % (researched by hand, see sources.md)
EXPLAIN = {
    "Makkah Royal Clock Tower": "Wikidata 607 m (+1.0 %) is not referenced to CTBUH and likely uses a different height definition (e.g. to the finial tip); CTBUH architectural height 601 m used, Wikipedia list also 601 m.",
    "Wuhan Tower": "Wikidata 438 m (-1.2 %) matches the originally announced design height; CTBUH as-built architectural height 443.13 m used (Wikipedia list 443.1 m).",
    "Minying International Trade Center T2": "Wikidata 426.9 m (+1.0 %) is not referenced to CTBUH (probably a design/tip figure); CTBUH 422.6 m used, Wikipedia list also 422.6 m.",
}


def fmt_m(v, decimals):
    return (f"{v:,.{decimals}f}" if decimals else f"{round(v):,}") + " m"


def slug(s):
    s = s.lower().replace("&", "and")
    s = re.sub(r"\(.*?\)", "", s)
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")


def wp_heights(wp_raw):
    w = json.load(open(wp_raw, encoding="utf-8"))["parse"]["wikitext"]
    start = w.find('{| class="sortable wikitable sticky-header-multi')
    end = w.find("\n|}", start)
    out = {}
    for r in re.split(r"\n\|-[^\n]*", w[start:end]):
        links = [x.split("|")[0].strip() for x in re.findall(r"\[\[([^\]]+)\]\]", r) if not x.startswith("File:")]
        h = re.findall(r"\{\{cvt\|([0-9.]+)\|m", r)
        if links and h:
            out[links[0]] = float(h[0])
    return out


def main(bdir, edir):
    ctbuh = json.load(open(os.path.join(bdir, "ctbuh_top100.json"), encoding="utf-8"))[:50]
    assert ctbuh[-1]["ctbuh_rank"] <= 50 and json.load(open(os.path.join(bdir, "ctbuh_top100.json"), encoding="utf-8"))[50]["height_m"] < ctbuh[-1]["height_m"]
    ents = json.load(open(os.path.join(bdir, "entities.json"), encoding="utf-8"))
    wd = json.load(open(os.path.join(bdir, "wikidata.json"), encoding="utf-8"))
    wph = wp_heights(os.path.join(bdir, "raw", "wp_tallest.json"))
    ip = os.path.join(bdir, "images.json")
    images = json.load(open(ip, encoding="utf-8")) if os.path.exists(ip) else {}

    # stable order: height desc, then display name (CTBUH already competition-ranks ties)
    rows = []
    for c in ctbuh:
        e = ents[c["name"]]
        rows.append((c, e))
    rows.sort(key=lambda ce: (-ce[0]["height_m"], ce[1]["name"]))
    # competition ranking (1,2,2,4) as CTBUH does
    ranks = []
    for i, (c, e) in enumerate(rows):
        if i and c["height_m"] == rows[i - 1][0]["height_m"]:
            ranks.append(ranks[-1])
        else:
            ranks.append(i + 1)
    for (c, e), r in zip(rows, ranks):
        assert r == c["ctbuh_rank"], (c["name"], r, c["ctbuh_rank"])

    # display precision: integer metres (3 s.f.), but 1 decimal where two different heights would show the same integer
    rounded = Counter(round(c["height_m"]) for c, e in rows)
    heights_by_round = {}
    for c, e in rows:
        heights_by_round.setdefault(round(c["height_m"]), set()).add(c["height_m"])

    items, report = [], []
    for (c, e), r in zip(rows, ranks):
        key = c["name"]
        w = wd.get(key, {})
        cands = []
        for h, unit, rank in w.get("heights", []) or []:
            m = h if unit == "metre" else (h * FT if unit == "foot" else None)
            if m and m > 100:
                cands.append((m, unit, rank, h))
        cross = None
        notes = []
        if cands:
            best = min(cands, key=lambda x: abs(x[0] - c["height_m"]))
            pref = [x for x in cands if x[2] == "PreferredRank"]
            diff = round((best[0] - c["height_m"]) / c["height_m"] * 100, 2)
            cross = {"name": "Wikidata " + w["qid"] + " (P2048 height, closest statement)",
                     "url": "https://www.wikidata.org/wiki/" + w["qid"],
                     "value": round(best[0], 2), "diff_pct": diff}
            if best[1] == "foot":
                notes.append(f"Wikidata height stated as {best[3]:g} ft, converted.")
            others = sorted({round(x[0], 1) for x in cands if abs(x[0] - best[0]) > 0.5})
            if others:
                notes.append("Other Wikidata height statements (other height definitions): " + ", ".join(f"{o:g} m" for o in others) + ".")
            if pref and abs(pref[0][0] - best[0]) > 0.5:
                notes.append(f"Wikidata preferred-rank value is {pref[0][0]:g} m.")
        else:
            wv = wph.get(e["enwiki"]) or wph.get(e["enwiki"].replace("–", "-"))
            if wv is None:
                for k, v in wph.items():
                    if k.split("|")[0] == e["enwiki"]:
                        wv = v
            if wv is not None:
                diff = round((wv - c["height_m"]) / c["height_m"] * 100, 2)
                cross = {"name": "Wikipedia 'List of tallest buildings' (no Wikidata height; Wikipedia cites CTBUH, so not independent)",
                         "url": "https://en.wikipedia.org/wiki/List_of_tallest_buildings", "value": wv, "diff_pct": diff}
                notes.append("Wikidata item has no height statement; cross-checked against Wikipedia list instead.")
        if cross and abs(cross["diff_pct"]) > 0.5:
            notes.append(EXPLAIN.get(key, "UNEXPLAINED difference > 0.5 %"))
        # floors cross-check
        wf = [int(x) for x in (w.get("floors") or []) if str(x).isdigit()]
        if c["floors"] and wf and c["floors"] not in wf:
            notes.append(f"Floors: CTBUH {c['floors']} above ground; Wikidata P1101 {', '.join(map(str, wf))} (CTBUH used).")
        # year cross-check against Wikidata opening (P1619) / inception (P571)
        wy = sorted({int(x[:4]) for x in (w.get("opened") or [])})
        if wy and c["year"] not in wy:
            notes.append(f"Completion year: CTBUH {c['year']}; Wikidata P1619 opening {', '.join(map(str, wy))} (CTBUH used).")
        if e["name"] != key:
            notes.append(f"CTBUH name: {key}.")
        if w.get("country") and not any(iso == e["iso2"] for _, iso in w["country"]):
            notes.append("Country differs from Wikidata P17: " + str(w["country"]))
        hr = round(c["height_m"])
        dec = 1 if len(heights_by_round[hr]) > 1 else 0
        if dec:
            notes.append("Shown with 1 decimal because another building rounds to the same whole metre.")
        ft = re.search(r"/\s*([0-9,]+)\s*ft", c["height_text"].replace("\xa0", " "))
        ft_txt = (ft.group(1) if ft else f"{round(c['height_m'] / FT):,}") + " ft"
        badge = f"NEW {c['year']}" if c["year"] in (2025, 2026) else None
        tags = []
        if c["floors"]:
            tags.append({"icon": "stairs", "text": f"{c['floors']} floors"})
        if c["year"]:
            tags.append({"icon": "calendar", "text": f"Completed {c['year']}"})
        img = images.get(key)
        reasons = json.load(open(os.path.join(bdir, "override_reasons.json"), encoding="utf-8"))
        if not img:
            notes.append("IMAGE: none (image=null) - " + reasons.get(key, "the only candidates carry a {{NoFoP-...}} template (no commercial FoP in this country); renderer should use a silhouette/placeholder."))
        elif key in reasons:
            notes.append("IMAGE: " + reasons[key])
        item = {
            "rank": r,
            "name": e["name"],
            "subtitle": e["subtitle"],
            "country_iso2": e["iso2"],
            "country_name": COUNTRY[e["iso2"]],
            "continent": CONTINENT[e["iso2"]],
            "value": c["height_m"],
            "value_display": fmt_m(c["height_m"], dec),
            "secondary_display": ft_txt,
            "badge": badge,
            "tags": tags,
            "image": img["file"] if img else None,
            "image_credit": img["credit"] if img else None,
            "source": {"name": "CTBUH Skyscraper Center, 100 Tallest Completed Buildings in the World",
                       "url": "https://www.skyscrapercenter.com" + c["ctbuh_path"], "retrieved_at": RETRIEVED},
            "cross_check": cross,
            "notes": " ".join(notes),
        }
        if badge is None:
            del item["badge"]
        items.append(item)
        report.append({"rank": r, "name": e["name"], "ctbuh": c["height_m"], "cross": cross, "notes": item["notes"]})

    data = {
        "episode": "ep01_tallest_buildings",
        "title": "World's Tallest Buildings",
        "kicker": "TOP 50",
        "metric_label": "Height",
        "unit": "m",
        "period_label": "Completed buildings, Nov 2026",
        "source_line": "Data: CTBUH Skyscraper Center, Wikidata (CC0)",
        "theme": "skyline",
        "tally": {"by": "country", "title": "Buildings by country"},
        "items": items,
        "insights": json.load(open(os.path.join(bdir, "insights.json"), encoding="utf-8")),
    }
    json.dump(data, open(os.path.join(edir, "data.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    json.dump(report, open(os.path.join(bdir, "crosscheck_report.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for x in report:
        print(x["rank"], ascii(x["name"]), x["ctbuh"], x["cross"]["value"] if x["cross"] else None,
              x["cross"]["diff_pct"] if x["cross"] else None, ascii(x["notes"])[:220])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
