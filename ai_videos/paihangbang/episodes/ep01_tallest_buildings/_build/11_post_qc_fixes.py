"""Post-QC fixes (2026-11-03, after independent review qc.md). Idempotent; run after 06_build_data.py.

- image_risk: photos whose assets.json fop_note says RISK (no commercial freedom of panorama) are withheld
  by default; render with `--allow-risk-images` to include them (human decision before publishing).
- image_note: honest placeholder text for cards without a photo.
- short names for two titles that were ellipsised on screen.
- CTBUH renamed Council on Vertical Urbanism (CVU) on 2025-10-06.
- scope_note for the YouTube description (what counts as "completed", why two towers are excluded).
- strip the "User:" prefix from on-screen credits; author of the Burj Khalifa photo.
"""
import json
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
assets = json.loads((EP / "assets.json").read_text(encoding="utf-8"))
by_file = {a["file"]: a for a in assets}

SHORT = {
    "Guiyang International Financial Center T1": "Guiyang IFC T1",
    "Guangzhou International Finance Center": "Guangzhou IFC",
}
NO_PHOTO_NOTE = {
    "Lotte World Tower": "No usable photo: architecture copyright",
    "LCT The Sharp Landmark Tower": "No usable photo: architecture copyright",
    "Marina 101": "No usable photo: architecture copyright",
    "Princess Tower": "No usable photo: architecture copyright",
    "Guiyang IFC T1": "No identifiable free-licensed photo",
}

for it in data["items"]:
    if it["name"] in SHORT:
        full = it["name"]
        it["name"] = SHORT[full]
        note = f"Full name: {full}."
        if note not in (it.get("notes") or ""):
            it["notes"] = (note + " " + (it.get("notes") or "")).strip()
    a = by_file.get(it.get("image") or "")
    if a and "RISK" in (a.get("fop_note") or ""):
        it["image_risk"] = "No commercial freedom of panorama in " + it["country_name"] + " (see assets.json fop_note)"
        it.setdefault("image_note", "Photo withheld: architecture copyright")
    if not it.get("image") and it["name"] in NO_PHOTO_NOTE:
        it["image_note"] = NO_PHOTO_NOTE[it["name"]]
    if (it.get("image_credit") or "").startswith("User:"):
        it["image_credit"] = it["image_credit"][5:]

for a in assets:
    if (a.get("author") or "").startswith("User:"):
        a["author"] = a["author"][5:]
    if a["file"].endswith("01_burj_khalifa.jpg") and a.get("author") == "ECWiki1":
        a["author"] = "ECWiki1 (Eric Chamchoum)"
for it in data["items"]:
    if (it.get("image") or "").endswith("01_burj_khalifa.jpg"):
        it["image_credit"] = "ECWiki1 (Eric Chamchoum) / CC BY 4.0"

for it in data["items"]:                       # CTBUH became CVU on 2025-10-06 (round-2 review)
    src = it.get("source") or {}
    if "CTBUH" in (src.get("name") or "") and "CVU" not in src["name"]:
        src["name"] = src["name"].replace("CTBUH Skyscraper Center", "Skyscraper Center (CVU, formerly CTBUH)")
data["source_line"] = "Data: Skyscraper Center (CVU, ex-CTBUH), Wikidata (CC0)"
data["scope_note"] = (
    "What counts: buildings listed as completed by the Council on Vertical Urbanism (CVU, formerly CTBUH) "
    "Skyscraper Center on 3 Nov 2026, measured to the architectural top (spires count, antennas don't). "
    "Chongqing's International Land-Sea Center (458 m) and Shandong IFC (428 m) are topped out but not yet "
    "listed as completed by CVU, so they are not included. Hong Kong is counted under China."
)
(EP / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(EP / "assets.json").write_text(json.dumps(assets, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("risk:", [i["name"] for i in data["items"] if i.get("image_risk")])
print("notes:", {i["name"]: i.get("image_note") for i in data["items"] if i.get("image_note")})
