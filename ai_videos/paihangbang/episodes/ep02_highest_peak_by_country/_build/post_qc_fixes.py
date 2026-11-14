"""Post-QC additions (2026-11-03). Idempotent; run after build.py.

- scope_note for the YouTube description (attribution rule, shared summits, ties).
- image_note for the one card without a photo.
"""
import json
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
data["scope_note"] = (
    "What counts: the highest point of each sovereign country, listed under the country that controls it "
    "(de-facto administration). Summits on a border count for every country that shares them, so Everest "
    "appears for both China and Nepal and Mont Blanc for both France and Italy. Equal heights share a rank."
)
for it in data["items"]:
    if not it.get("image"):
        it["image_note"] = "No free-licensed photo found"
(EP / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("ok", [i["name"] for i in data["items"] if i.get("image_note")])
