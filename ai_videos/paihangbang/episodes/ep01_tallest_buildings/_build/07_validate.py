"""Validate data.json + assets.json against data_contract.md v1.

Usage: python -I 07_validate.py <episode_dir>
"""
import hashlib
import json
import os
import re
import sys

ICONS = {"mountain", "calendar", "building", "stairs", "map-pin", "ruler", "flag", "trophy", "users", "globe"}
LIC_OK = re.compile(r"^(Public domain|CC0( 1\.0)?|CC BY( \d\.\d)?|CC BY-SA( \d\.\d)?( [a-z]{2})?)$")


def main(edir):
    errs, warns = [], []
    d = json.load(open(os.path.join(edir, "data.json"), encoding="utf-8"))
    assets = json.load(open(os.path.join(edir, "assets.json"), encoding="utf-8"))
    for k in ["episode", "title", "kicker", "metric_label", "unit", "period_label", "source_line", "theme", "tally", "items", "insights"]:
        if k not in d:
            errs.append("missing top-level " + k)
    if len(d["source_line"]) > 70:
        errs.append("source_line > 70")
    if d["tally"].get("by") not in ("country", "continent"):
        errs.append("tally.by")
    items = d["items"]
    if len(items) != 50:
        errs.append(f"{len(items)} items")
    prev = None
    for i, it in enumerate(items):
        tag = f"#{i} {it.get('name')}"
        for k in ["rank", "name", "subtitle", "country_iso2", "country_name", "continent", "value", "value_display",
                  "secondary_display", "tags", "image", "image_credit", "source", "cross_check", "notes"]:
            if k not in it:
                errs.append(f"{tag}: missing {k}")
        if prev:
            if it["value"] > prev["value"]:
                errs.append(f"{tag}: not sorted by value")
            if it["value"] == prev["value"]:
                if it["rank"] != prev["rank"]:
                    errs.append(f"{tag}: tie but rank differs")
                if it["name"] < prev["name"]:
                    errs.append(f"{tag}: tie order not by name")
            elif it["rank"] != i + 1:
                errs.append(f"{tag}: rank {it['rank']} != competition rank {i + 1}")
        elif it["rank"] != 1:
            errs.append("first rank != 1")
        prev = it
        if not isinstance(it["value"], (int, float)):
            errs.append(f"{tag}: value not number")
        if "badge" in it and it["badge"] is not None:
            b = it["badge"]
            if len(b) > 22 or b != b.upper():
                errs.append(f"{tag}: badge {b!r}")
        if len(it["tags"]) > 2:
            errs.append(f"{tag}: >2 tags")
        for t in it["tags"]:
            if t["icon"] not in ICONS:
                errs.append(f"{tag}: icon {t['icon']}")
            if len(t["text"]) > 24:
                errs.append(f"{tag}: tag text > 24")
        if not re.fullmatch(r"[A-Z]{2}", it["country_iso2"]):
            errs.append(f"{tag}: iso2")
        if it["image"]:
            p = os.path.join(edir, it["image"])
            if not os.path.exists(p):
                errs.append(f"{tag}: image file missing")
            a = [x for x in assets if x["file"] == it["image"]]
            if len(a) != 1:
                errs.append(f"{tag}: image not (uniquely) in assets.json")
            else:
                a = a[0]
                if not LIC_OK.match(a["licence"]):
                    errs.append(f"{tag}: licence {a['licence']}")
                if os.path.exists(p) and hashlib.sha256(open(p, "rb").read()).hexdigest() != a["sha256"]:
                    errs.append(f"{tag}: sha256 mismatch")
                if not it["image_credit"]:
                    errs.append(f"{tag}: no image_credit")
                if "RISK" in a.get("fop_note", ""):
                    warns.append(f"{tag}: FoP risk flagged")
            if not re.fullmatch(r"assets/img/\d\d_[a-z0-9_]+\.jpg", it["image"]) or not it["image"].startswith(f"assets/img/{it['rank']:02d}_"):
                errs.append(f"{tag}: image filename pattern")
        else:
            warns.append(f"{tag}: no image")
        cc = it["cross_check"]
        if cc is None:
            warns.append(f"{tag}: no cross-check")
        elif abs(cc["diff_pct"]) > 0.5 and "UNEXPLAINED" in it["notes"]:
            errs.append(f"{tag}: unexplained cross-check diff")
    for a in assets:
        if not os.path.exists(os.path.join(edir, a["file"])):
            errs.append("ledger file missing " + a["file"])
        for k in ["file", "commons_page", "source_url", "author", "licence", "licence_url", "attribution_required",
                  "modified", "sha256", "retrieved_at", "fop_note"]:
            if k not in a:
                errs.append(f"ledger {a['file']}: missing {k}")
    used = {it["image"] for it in items if it["image"]}
    for a in assets:
        if a["file"] not in used:
            warns.append("ledger entry not used: " + a["file"])
    ranks = [it["rank"] for it in items]
    for ins in d["insights"]:
        if len(ins["text"]) > 90:
            errs.append("insight > 90: " + ins["text"])
        if ins["after_rank"] not in ranks:
            errs.append("insight after_rank not a rank")
    gaps = sorted(ins["after_rank"] for ins in d["insights"])
    print("ERRORS:", len(errs))
    for e in errs:
        print("  E", ascii(e))
    print("WARNINGS:", len(warns))
    for w in warns:
        print("  W", ascii(w))
    print("items", len(items), "images", sum(1 for it in items if it["image"]), "ledger", len(assets), "insights at", gaps)
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main(sys.argv[1])
