"""Card layout v0.2 settings (2026-11-03, follow-up 004: photo first, flag second, key stat third). Idempotent.

Run after 11_post_qc_fixes.py. Portrait tower photos fill a 600x800 card; the crop keeps the top of the
photo (spires) by default; three landscape photos get a horizontal focus so the tower is not under the
flag / rank pill.
"""
import json
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
data["layout"] = {"card_w": 600, "focus": [0.5, 0.04]}
FOCUS = {
    "Lakhta Center": [0.72, 0.04],
    "Petronas Tower 2": [0.75, 0.04],
    "Iconic Tower": [0.0, 0.04],
}
for it in data["items"]:
    if it["name"] in FOCUS:
        it["image_focus"] = FOCUS[it["name"]]
(EP / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("layout", data["layout"], "focus", {i["name"]: i["image_focus"] for i in data["items"] if "image_focus" in i})
