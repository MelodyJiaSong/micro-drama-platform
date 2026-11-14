# -*- coding: utf-8 -*-
"""解析 Wikipedia「List of river systems by length」(revid 见 raw/wp_list.json) 主表 → raw/wp_rows.json（只作交叉核对）。"""
import json, re
from pathlib import Path
R = Path(__file__).parent / "raw"
w = (R / "wp_list.wikitext").read_text(encoding="utf-8")
t = w[w.find('{|class="wikitable sortable'):]
t = t[:t.find('\n|}')]
COL = {"#ccccff": "Africa", "#ffffaa": "Asia", "#ccff66": "Australia", "#ffc0cb": "Europe", "#ccffff": "North America", "#ffd39b": "South America"}

def strip_refs(s):
    s = re.sub(r"<ref[^>]*/>", "", s)
    s = re.sub(r"<ref[^>]*>.*?</ref>", "", s, flags=re.S)
    s = re.sub(r"\{\{refn.*", "", s, flags=re.S) if "{{refn" in s else s
    return s

def refs(s):
    return re.findall(r"<ref(?: name=\"?([^\">/]+)\"?)?\s*/?>(.*?)(?:</ref>|$)", s, flags=re.S)

def plain(s):
    s = strip_refs(s)
    s = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\{\{[^}]*\}\}", "", s)
    return re.sub(r"\s+", " ", s).strip()

rows = []
for blk in t.split("\n|-")[1:]:
    lines = blk.strip("\n").split("\n")
    head = next((l for l in lines if re.match(r'!\s*scope="row"', l)), None)
    if not head:
        continue
    m = re.search(r"background-color:(#\w+)", head); cont = COL.get(m.group(1).lower(), "?") if m else "?"
    rank = re.sub(r"[^\d=]", "", head.split("|")[-1])
    cells, cur = [], None
    for l in lines[lines.index(head) + 1:]:
        if l.startswith("|"):
            if cur is not None: cells.append(cur)
            cur = l[1:]
        elif cur is not None:
            cur += "\n" + l
    if cur is not None: cells.append(cur)
    if len(cells) < 7: continue
    def nums(c):
        main = strip_refs(c.split("<br")[0]); alt = re.findall(r"\(([\d,\.]+)\)", strip_refs(c))
        mm = re.search(r"[\d,\.]+", main.replace("~", ""))
        return (float(mm.group(0).replace(",", "")) if mm else None, alt)
    km, km_alt = nums(cells[1])
    rows.append({"rank": rank, "continent_colour": cont, "river": plain(cells[0]), "km": km, "km_alt": km_alt,
                 "km_raw": cells[1][:600], "basin_km2": plain(cells[3])[:40], "outflow": plain(cells[5]),
                 "countries": plain(cells[6])})
(R / "wp_rows.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
for r in rows[:75]:
    print(r["rank"], r["continent_colour"][:4], r["km"], r["km_alt"], "|", r["river"][:60], "|", r["outflow"][:25], "|", r["countries"][:70])
