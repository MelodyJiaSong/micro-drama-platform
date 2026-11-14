"""Parse the main table of Wikipedia 'List of tallest buildings' wikitext (data only).

Usage: python -I 02_parse_wikipedia.py <raw/wp_tallest.json> <out wp_list.json>
"""
import json
import re
import sys


def link_target(s):
    m = re.search(r"\[\[([^\]|#]+)(?:[^\]]*)\]\]", s)
    return m.group(1).strip() if m else None


def link_text(s):
    s = re.sub(r"'''?", "", s)
    m = re.search(r"\[\[([^\]]+)\]\]", s)
    if not m:
        return s.strip()
    inner = m.group(1)
    return inner.split("|")[-1].strip()


def main(src, dst):
    w = json.load(open(src, encoding="utf-8"))["parse"]["wikitext"]
    start = w.find('{| class="sortable wikitable sticky-header-multi')
    end = w.find("\n|}", start)
    table = w[start:end]
    rows = re.split(r"\n\|-[^\n]*", table)
    out = []
    for r in rows:
        lines = [l for l in r.split("\n") if l.startswith("|") and not l.startswith("|}")]
        cells = []
        for l in lines:
            # a cell line may be "| a || b"; style prefixes "style=.. | value"
            for c in re.split(r"\|\|", l[1:]):
                cells.append(c.strip())
        if len(cells) < 9:
            continue
        rank_txt = re.sub(r"[^0-9=]", "", cells[0])
        if not rank_txt:
            continue
        hm = re.search(r"\{\{cvt\|([0-9.,]+)\|m", cells[2])
        img = re.search(r"\[\[File:([^|\]]+)", cells[4])
        country = re.search(r"\{\{[Ff]lag(?:country)?\|([^}|]+)", cells[6])
        year = re.search(r"(\d{4})", cells[7])
        floors = re.match(r"\s*(\d+)", cells[3])
        out.append({
            "wp_rank": rank_txt,
            "article": link_target(cells[1]),
            "name": link_text(cells[1]),
            "height_m": float(hm.group(1).replace(",", "")) if hm else None,
            "floors": int(floors.group(1)) if floors else None,
            "image": img.group(1).strip() if img else None,
            "city": link_text(cells[5]),
            "country": country.group(1).strip() if country else cells[6],
            "year": int(year.group(1)) if year else None,
        })
    json.dump(out, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(out), "rows")
    for o in out[:70]:
        print(o["wp_rank"], o["name"], "|", o["article"], o["height_m"], o["floors"], o["city"], o["country"], o["year"], o["image"])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
