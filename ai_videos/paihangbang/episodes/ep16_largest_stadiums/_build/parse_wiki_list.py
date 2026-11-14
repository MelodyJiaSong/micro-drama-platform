# -*- coding: utf-8 -*-
"""解析 Wikipedia「List of stadiums by capacity」wikitext → _build/raw/wiki_candidates.json（只作候选与交叉核对）。"""
import json, re, sys
from pathlib import Path
B = Path(__file__).parent
t = json.loads((B / "raw/wiki_list_stadiums_by_capacity.json").read_text(encoding="utf-8"))["parse"]["wikitext"]
def clean(s):
    s = re.sub(r"<ref[^>]*/>", "", s); s = re.sub(r"<ref[^>]*>.*?</ref>", "", s, flags=re.S)
    s = re.sub(r"\{\{[Ff]lag(?:icon|country)?\|([^}|]+)[^}]*\}\}", r"\1", s)
    s = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]+)\]\]", r"\1", s)
    s = re.sub(r"\{\{[^}]*\}\}", "", s); s = re.sub(r"<[^>]+>", " ", s); s = s.replace("'''", "").replace("''", "")
    return " ".join(s.split())
rows = []
for block in t.split("\n|-")[1:]:
    cells = re.split(r"\n\||\|\|", block.split("\n|}")[0])
    cells = [c for c in cells if c.strip()]
    if len(cells) < 4: continue
    name = clean(cells[0]); cap = clean(cells[1])
    m = re.search(r"[\d,]{5,}", cap)
    if not m: continue
    rows.append({"stadium": name, "capacity": int(m.group(0).replace(",", "")), "cap_raw": cap[:60], "city": clean(cells[2]), "country": clean(cells[3]),
                 "sport": clean(cells[6]) if len(cells) > 6 else ""})
rows.sort(key=lambda r: -r["capacity"])
(B / "raw/wiki_candidates.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
for i, r in enumerate(rows[:90], 1):
    print(i, r["capacity"], r["stadium"], "|", r["city"], "|", r["country"], "|", r["sport"][:40])
