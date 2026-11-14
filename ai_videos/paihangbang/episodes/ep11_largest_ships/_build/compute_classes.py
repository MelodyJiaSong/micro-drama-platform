# 由 VesselFinder GT≥160k 全量清单（按 GT 区间抓取）+ 船级定义，算每个船级的成员、最大 GT、代表船、首年
import json, re, sys
sys.path.insert(0, '.')
from classes_def import CLASSES
fleet = json.load(open('vf_fleet_gt160_bands.json', encoding='utf-8'))
def norm(n): return re.sub(r'\s+', ' ', n.upper().replace('Ü','U').replace('İ','I')).strip()
out = []
used = {}
for c in CLASSES:
    rx = re.compile(c['members'])
    mem = []
    for x in fleet:
        n = norm(x['name'])
        if not rx.search(n): continue
        if c.get('type_') and x['type'] != c['type_']: continue
        if not c.get('type_') and c['kind'] == 'Container ship' and x['type'] != 'Container Ship': continue
        if c['kind'] == 'Cruise ship' and x['type'] != 'Passenger (Cruise) Ship': continue
        if c.get('size') and not x['size'].startswith(c['size']): continue
        if c.get('size_prefix') and not x['size'].startswith(c['size_prefix']): continue
        if c.get('gt_min') and int(x['gt']) < c['gt_min']: continue
        if c.get('gt_max') and int(x['gt']) > c['gt_max']: continue
        if c.get('size_min_dwt') and not (x['dwt'].isdigit() and int(x['dwt']) >= c['size_min_dwt'] and x['type']=='Bulk Carrier'): continue
        if c.get('dwt_range') and not (x['dwt'].isdigit() and c['dwt_range'][0] <= int(x['dwt']) <= c['dwt_range'][1]): continue
        if c.get('year_min') and int(x['year']) < c['year_min']: continue
        if n in c.get('exclude', ()): continue
        mem.append(x)
        used.setdefault(x['imo'], []).append(c['key'])
    mem.sort(key=lambda x: (-int(x['gt']), int(x['year']), int(x['imo'])))
    rep = mem[0] if mem else None
    first = min((int(x['year']) for x in mem), default=None)
    out.append({**{k: c[k] for k in ('key','name','kind','operator','iso')}, 'n': len(mem), 'max_gt': int(rep['gt']) if rep else 0,
                'rep': rep, 'first_year': first, 'last_year': max((int(x['year']) for x in mem), default=None),
                'members': [[x['imo'], x['name'], x['year'], x['gt'], x['size']] for x in mem]})
dups = {k: v for k, v in used.items() if len(v) > 1}
print('dup members:', dups)
out.sort(key=lambda c: -c['max_gt'])
for i, c in enumerate(out, 1):
    r = c['rep']
    print(f"{i:2d} {c['max_gt']:>7,} {c['name'][:34]:34s} n={c['n']:2d} {c['first_year']}-{c['last_year']} rep={r['name'] if r else '-'} {r['size'] if r else ''}")
json.dump(out, open('classes_computed.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
# 未归类的大船（≥170,618 GT，非海工固定装置）
assigned = set(used)
print('--- unassigned >= 170,619 GT (non-offshore):')
for x in fleet:
    if int(x['gt']) > 170618 and x['imo'] not in assigned and x['type'] not in ('Offshore Support Vessel','FSO'):
        print('  ', x['imo'], x['name'], x['type'], x['year'], x['gt'], x['size'])
