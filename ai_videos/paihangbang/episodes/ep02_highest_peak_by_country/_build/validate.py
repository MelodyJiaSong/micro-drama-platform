"""Validate ep02 package against data_contract.md v1. Usage: python -I <this dir>/validate.py"""
import hashlib, json, re, sys
from pathlib import Path

EP = Path(__file__).resolve().parent.parent
ICONS = {"mountain", "calendar", "building", "stairs", "map-pin", "ruler", "flag", "trophy", "users", "globe"}
errs, warns = [], []
d = json.loads((EP / "data.json").read_text(encoding="utf-8"))
assets = json.loads((EP / "assets.json").read_text(encoding="utf-8"))
amap = {a["file"]: a for a in assets}

for k in ["episode", "title", "kicker", "metric_label", "unit", "period_label", "source_line", "theme", "tally", "items", "insights"]:
    if k not in d: errs.append(f"missing top-level {k}")
if len(d["source_line"]) > 70: errs.append("source_line > 70")
if d["tally"].get("by") not in ("country", "continent"): errs.append("tally.by")
items = d["items"]
if len(items) != 50: errs.append(f"items={len(items)}")
# ranks ascending, competition ranking consistent with values, stable tie order by country name
for i, it in enumerate(items):
    if i:
        p = items[i - 1]
        if it["rank"] < p["rank"]: errs.append(f"rank order at {i}")
        if it["value"] > p["value"]: errs.append(f"value order at {i}")
        if it["value"] == p["value"]:
            if it["rank"] != p["rank"]: errs.append(f"tie rank mismatch at {i}")
            if it["country_name"] < p["country_name"]: errs.append(f"tie order at {i}")
        elif it["rank"] != i + 1: errs.append(f"rank {it['rank']} should be {i+1}")
    elif it["rank"] != 1: errs.append("first rank != 1")
    for k in ["rank", "name", "subtitle", "country_iso2", "country_name", "continent", "value", "value_display",
              "secondary_display", "tags", "image", "image_credit", "source", "cross_check", "notes"]:
        if k not in it: errs.append(f"{it.get('name')}: missing {k}")
    if not re.fullmatch(r"[A-Z]{2}", it["country_iso2"]): errs.append(f"iso {it['country_iso2']}")
    if it["continent"] not in {"Asia", "Europe", "Africa", "North America", "South America", "Oceania"}: errs.append(f"continent {it['continent']}")
    exp = f"{int(__import__('decimal').Decimal(str(it['value'])).quantize(1, rounding='ROUND_HALF_UP')):,} m"
    if it["value_display"] != exp: errs.append(f"{it['name']} display {it['value_display']} != {exp}")
    if "badge" in it and (len(it["badge"]) > 22 or it["badge"] != it["badge"].upper()): errs.append(f"badge {it['badge']}")
    if len(it["tags"]) > 2: errs.append(f"{it['name']}: >2 tags")
    for t in it["tags"]:
        if t["icon"] not in ICONS: errs.append(f"icon {t['icon']}")
        if len(t["text"]) > 24: errs.append(f"tag text >24: {t['text']}")
    for k in ["name", "url", "retrieved_at"]:
        if k not in it["source"]: errs.append(f"{it['name']} source.{k}")
    for k in ["name", "url", "value", "diff_pct"]:
        if k not in it["cross_check"]: errs.append(f"{it['name']} cross_check.{k}")
    if it["cross_check"]["diff_pct"] > 0.5 and not it["notes"]: errs.append(f"{it['name']}: diff >0.5% without notes")
    if it["image"] is None:
        warns.append(f"#{it['rank']} {it['country_name']} {it['name']}: no image")
        continue
    f = EP / it["image"]
    if not f.exists(): errs.append(f"missing file {it['image']}"); continue
    if not re.fullmatch(r"assets/img/\d{2}_[a-z0-9_]+\.jpg", it["image"]) or int(it["image"][11:13]) != it["rank"]:
        errs.append(f"bad filename {it['image']}")
    a = amap.get(it["image"])
    if not a: errs.append(f"not in assets.json: {it['image']}"); continue
    if hashlib.sha256(f.read_bytes()).hexdigest() != a["sha256"]: errs.append(f"sha mismatch {it['image']}")
    lic = a["licence"].lower()
    if re.search(r"\b(nc|nd)\b", lic) or not (lic.startswith(("cc by ", "cc by-sa ", "cc0")) or lic == "public domain"):
        errs.append(f"licence {a['licence']} {it['image']}")
    if a["licence"] != "Public domain" and not it["image_credit"].endswith(a["licence"]): errs.append(f"credit/licence mismatch {it['image']}")
    for k in ["file", "commons_page", "source_url", "author", "licence", "licence_url", "attribution_required", "modified", "sha256", "retrieved_at", "fop_note"]:
        if k not in a: errs.append(f"assets {it['image']} missing {k}")
used = {it["image"] for it in items if it["image"]}
for a in assets:
    if a["file"] not in used: warns.append(f"asset not used: {a['file']}")
ranks = {it["rank"] for it in items}
for ins in d["insights"]:
    if len(ins["text"]) > 90: errs.append(f"insight >90: {ins['text']}")
    if ins["after_rank"] not in ranks: errs.append(f"insight after_rank {ins['after_rank']} not a rank")
    if sum(1 for it in items if it["rank"] == ins["after_rank"]) > 1: warns.append(f"insight after tied rank {ins['after_rank']}")
from collections import Counter
print("items:", len(items), "| images:", sum(1 for it in items if it["image"]), "| assets:", len(assets))
print("licences:", dict(Counter(a["licence"] for a in assets)))
print("tally:", dict(Counter(it["continent"] for it in items)))
print("insights:", [i["after_rank"] for i in d["insights"]])
for w in warns: print("WARN", w)
for e in errs: print("ERROR", e)
print("RESULT:", "PASS" if not errs else f"FAIL ({len(errs)} errors)")
sys.exit(1 if errs else 0)
