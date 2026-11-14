# -*- coding: utf-8 -*-
"""ep06：按第 1 轮独立审片（_build/qc_round1_independent.md）改 data.json。幂等，可重跑。

用户 2026-11-03 睡前授权自主决策；每条改动注明对应的 QC 编号，判断依据写进 sources.md §2。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

EP = Path(__file__).resolve().parents[1]

# QC #4：「as of」统一 = 该数字首次被公布的年份（媒体后来复述不算）
FIRST_ANNOUNCED = {
    "One Piece": 2026, "Doraemon": 2024, "Golgo 13": 2021, "Detective Conan": 2023, "Dragon Ball": 2022,
    "Naruto": 2023, "Demon Slayer": 2025, "Slam Dunk": 2025, "KochiKame": 2014, "Jujutsu Kaisen": 2025,
    "Attack on Titan": 2024, "Oishinbo": 2020, "Bleach": 2022, "JoJo's Bizarre Adventure": 2022, "Kingdom": 2026,
    "Baki": 2024, "Fist of the North Star": 2019, "Hajime no Ippo": 2023, "Hunter × Hunter": 2026,
    "The Kindaichi Case Files": 2019, "My Hero Academia": 2024, "Touch": 2004, "Captain Tsubasa": 2023,
    "Fullmetal Alchemist": 2026, "Sazae-san": 1999, "Kinnikuman": 2025, "Vagabond": 2012, "Sangokushi": 2020,
    "Tokyo Revengers": 2024, "Haikyu!!": 2025,
}
BADGES = {   # QC #1 #12 #13 #14
    "Jujutsu Kaisen": "+50M IN 15 MONTHS",
    "Hunter × Hunter": "NEW: 100M IN JULY 2026",
    "Fullmetal Alchemist": "NEW: 90M IN 2026",
    "Golgo 13": "RECORD: 220+ VOLUMES",
    "Hajime no Ippo": "140+ VOLUMES",
}
CREDITS = {  # QC #11：英文版封面写明版本与现行版权方
    "Fist of the North Star": "Illustration: © Buronson & Tetsuo Hara / Coamix · English ed.",
    "Baki": "Illustration: © Keisuke Itagaki / Akita Shoten · English ed.",
}
INSIGHTS = [  # QC #1 #2 #3 #16
    (28, "Crayon Shin-chan's 148M is left out: it also counts ~20M non-manga books."),
    (23, "Next: seven series tied at the 100-million mark."),
    (11, "Jujutsu Kaisen added 50 million copies in the 15 months after its 2024 finale."),
    (8, "Demon Slayer has just 23 volumes: about 9.6M copies each, the most per volume here."),
    (2, "One Piece has sold about twice as many copies as any other manga."),
]
SOURCE_LINE = "Sources: publishers, Oricon, Mantan Web, ANN, other media, Wikipedia"   # QC #6
PERIOD = "Latest announced figure · year on each card"                                      # QC #5
SCOPE = ("What counts: manga series ranked by the latest cumulative circulation announced by the publisher "
         "(or reported from its announcement), including overseas and digital editions where the announcement does. "
         "Figures that bundle non-manga books are left out (Crayon Shin-chan's 148M, Astro Boy's 100M). "
         "Totals only go up, so older figures are kept as minimums; each card shows the year the figure was first announced. "
         "Equal figures share a rank.")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    p = EP / "data.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    for it in d["items"]:
        y = FIRST_ANNOUNCED[it["name"]]
        it["figure_year"] = y
        it["secondary_display"] = f"copies · as of {y}"
        if it["name"] in BADGES:
            it["badge"] = BADGES[it["name"]]
        if it["name"] in CREDITS:
            it["image_credit"] = CREDITS[it["name"]]
        assert len(it.get("badge", "")) <= 22, it["badge"]
    for a, t in INSIGHTS:
        assert len(t) <= 90, (len(t), t)
    assert len(SOURCE_LINE) <= 70, len(SOURCE_LINE)
    assert len(SCOPE) <= 600, len(SCOPE)
    d["insights"] = [{"after_rank": a, "text": t} for a, t in INSIGHTS]
    d["source_line"] = SOURCE_LINE
    d["period_label"] = PERIOD
    d["scope_note"] = SCOPE
    d.setdefault("layout", {})["intro_hold"] = 2.5     # QC #7：最后一名（#30）也读满 3 s（rank_scroll follow-up 008）
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("ok", len(SOURCE_LINE), len(SCOPE))


if __name__ == "__main__":
    main()
