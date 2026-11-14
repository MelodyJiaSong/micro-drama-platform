# -*- coding: utf-8 -*-
"""items_ab.py + items_c.py + 片头字段与洞察卡 → items_def.json（build.py 的输入）。"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from items_ab import ITEMS_AB  # noqa: E402
from items_c import ITEMS_C  # noqa: E402

HEAD = {
    "episode": "ep03_ai_companies",
    "mode": "list",
    "title": "30 AI Companies Shaping the Future",
    "youtube_title": "30 AI Companies Shaping the Future (2026)",
    "kicker": "30 AI COMPANIES",
    "metric_label": "Latest valuation",
    "unit": "USD",
    "period_label": "Data as of Nov 3, 2026",
    "source_line": "Sources: company releases, Bloomberg, TechCrunch, Caixin, exchanges",
    "theme": "tech",
    "tally": {"by": "country", "title": "Companies by country"},
    "layout": {"card_w": 720, "focus": [0.5, 0.4], "intro_hold": 2.5},
    "scope_note": ("30 well-known AI-native companies (language, image, video, voice & music, coding, search, robotics), "
                   "listed by founding year, not ranked. Value = latest completed private round (post-money), market cap for "
                   "listed companies (close of Nov 3, 2026 unless dated otherwise), or the acquisition price for companies "
                   "bought by others. Where no recent valuation exists, the card says what the number is (raised / ARR / share sale / "
                   "pre-money). Flags show headquarters country. Sources for every number are listed below."),
}

INSIGHTS = [
    {"after_slug": "hugging_face", "text": "Hugging Face began as a chatbot app for teenagers before becoming the hub for AI models."},
    {"after_slug": "runway", "text": "Next: Cohere. Its CEO co-wrote 'Attention Is All You Need', the 2017 Transformer paper."},
    {"after_slug": "midjourney", "text": "Midjourney never took outside money. Meta licensed its tech instead (Aug 2025)."},
    {"after_slug": "deepseek", "text": "Fears over DeepSeek-R1 wiped about $589B off Nvidia's value in one day (Jan 27, 2025)."},
    {"after_slug": "black_forest_labs", "text": "Google owns DeepMind, SpaceX owns xAI and Cursor, and Nvidia is buying Hugging Face."},
]

items = []
for r in ITEMS_AB + ITEMS_C:
    r = dict(r)
    r["corner"] = f"EST. {r['founded'][:4]}"
    items.append(r)
assert len(items) == 30 and len({r["slug"] for r in items}) == 30, len(items)
for x in INSIGHTS:
    assert len(x["text"]) <= 90, (len(x["text"]), x["text"])
(HERE / "items_def.json").write_text(json.dumps({"episode": HEAD, "items": items, "insights": INSIGHTS}, ensure_ascii=False, indent=1), encoding="utf-8")
print("items_def.json:", len(items), "items")
