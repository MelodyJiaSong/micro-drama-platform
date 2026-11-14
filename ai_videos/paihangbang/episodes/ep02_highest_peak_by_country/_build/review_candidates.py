"""Print licence / size verdicts for each candidate. Usage: python -I review_candidates.py <commons_info.json>"""
import json, sys, re, html
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
def plain(s):
    if s is None: return ''
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', s))).strip()
def licence_ok(lic):
    l = (lic or '').lower()
    if not l: return False
    if 'nc' in re.split(r'[\s\-]', l) or 'nd' in re.split(r'[\s\-]', l): return False
    if l in ('public domain', 'pd', 'cc0') or l.startswith('pd') or l.startswith('cc0') or 'public domain' in l: return True
    if l.startswith('cc by'): return True
    return False
d = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
for slug, titles in d['candidates'].items():
    print('##', slug)
    for t in titles:
        i = d['info'].get('File:' + t)
        if not i: print('   MISSING', t); continue
        m = i['meta']; r = i['width'] / i['height']
        ok = licence_ok(m['LicenseShortName'])
        print('  ', 'OK ' if ok else 'BAD', f"{i['width']}x{i['height']} r={r:.2f}", i['mime'].split('/')[-1], '|', m['LicenseShortName'], '|', plain(m['Artist'])[:50], '|', t[:90])
