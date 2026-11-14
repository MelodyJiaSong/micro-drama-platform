"""Card layout v0.2 settings (2026-11-03, follow-up 004: photo first, flag second, key stat third). Idempotent.

Run after post_qc_fixes.py. Mountain photos are landscape, so this episode uses wider 720x800 cards
(crop keeps ~60% of a 3:2 photo's width instead of ~50%).
"""
import json
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
data["layout"] = {"card_w": 720}
(EP / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("layout", data["layout"])
