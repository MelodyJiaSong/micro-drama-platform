# -*- coding: utf-8 -*-
"""rank_scroll publish 生成 publish.md 后的人工补写（标题、描述开头、标签、置顶评论开头）。用法：python -I _build/fix_publish.py"""
from pathlib import Path

EP = Path(__file__).resolve().parent.parent
p = EP / "publish.md"
s = p.read_text(encoding="utf-8")

TITLE = "Most Visited Countries in the World | Top 50 (2026)"
s = s.replace("Most Visited Countries in the World | Top 50 (year)\n", f"{TITLE}\n", 1)

INTRO_OLD = "Every number on screen is sourced and cross-checked. Which one surprised you? Tell us in the comments!\n"
INTRO_NEW = ("Which countries really get the most foreign visitors? 50 countries ranked by international tourist arrivals "
             "(overnight visitors) in 2024, from UN Tourism and national statistics offices. Each card shows the change "
             "vs 2019, the last year before the pandemic (same series), so you can see who has recovered and who hasn't.\n"
             "Every number on screen is sourced. Surprised that China is missing, or that Greece isn't 40 million? "
             "The small notes on each card and the text below explain why. Which one surprised you? Tell us in the comments!\n")
assert INTRO_OLD in s
s = s.replace(INTRO_OLD, INTRO_NEW, 1)

HASH_OLD = "#MostVisitedCountriesInTheWorld #Top50 #Ranking #DataComparison"
HASH_NEW = "#MostVisitedCountries #Travel #Tourism #Top50 #Ranking"
s = s.replace(HASH_OLD, HASH_NEW, 1)

if "## Tags" not in s:
    s = s.replace("## Upload checklist", "## Tags\n\nmost visited countries, most visited countries in the world, most visited countries 2026, "
                  "tourism ranking, international tourist arrivals, UN Tourism, top 50 countries, travel statistics, world tourism rankings, "
                  "tourist arrivals by country, top travel destinations, data comparison\n\n## Upload checklist", 1)
import re
m = re.search(r"## Description（\d+ / 5000 字符）\n\n```text\n(.*?)```", s, re.S)
s = s.replace(m.group(0), m.group(0).replace(re.search(r"（\d+ / 5000", m.group(0)).group(0), f"（{len(m.group(1))} / 5000"), 1)
p.write_text(s, encoding="utf-8")
print("title", len(TITLE), "chars; description intro updated")
