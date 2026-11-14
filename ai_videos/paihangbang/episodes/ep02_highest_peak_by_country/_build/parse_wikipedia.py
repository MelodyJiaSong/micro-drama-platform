"""Parse Wikipedia 'List of elevation extremes by country' wikitext into JSON rows.
Input: raw/wp_elevation_extremes_2026-11-03.json (untrusted data, parsed only).
Output: wp_rows.json  [{code, country_cell, highest_point, elev_m}]
"""
import json, re, sys
from pathlib import Path
here = Path(__file__).parent
w = json.loads((here/'raw'/'wp_elevation_extremes_2026-11-03.json').read_text(encoding='utf-8'))['parse']['wikitext']
table = w.split('\n{|', 1)[1].split('\n|}', 1)[0]  # table end must be at line start
rows = re.split(r'\n\|-[^\n]*\n', table)
out = []
for r in rows[1:]:
    # cells start with '|' at line start
    cells = re.split(r'\n\|', '\n'+r.strip())
    cells = [c for c in cells if c.strip()]
    if len(cells) < 2: continue
    c0 = cells[0].strip()
    m = re.match(r'\{\{([A-Z]{3})\}\}', c0)
    code = m.group(1) if m else None
    hp = cells[1]
    em = re.search(r'\{\{epi/moft\|([-\d.,]+)', hp)
    elev = float(em.group(1).replace(',','')) if em else None
    name_part = hp.split('{{epi/moft')[0]
    name_part = re.sub(r'<ref[^>]*/>|<ref.*?</ref>', '', name_part, flags=re.S)
    name_part = re.sub(r'\{\{efn.*?\}\}', '', name_part, flags=re.S)
    links = re.findall(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]', name_part)
    out.append({'code': code, 'country_cell': c0[:80], 'highest_point_raw': name_part.strip()[:200],
                'links': [l[0] for l in links], 'elev_m': elev})
(here/'wp_rows.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
print(len(out))
