import re, html, time, urllib.request, json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
D = Path(__file__).parent / 'raw' / 'ilec'
ids = dict(Baikal='ASI-27', Tanganyika='AFR-06', Caspian='ASI-222', Malawi='AFR-13', IssykKul='ASI-55', GreatSlave='NAM-276', Crater='NAM-227',
  Matano='ASI-301', GeneralCarrera='SAM-265', Toba='ASI-10', Tahoe='NAM-02', Kivu='AFR-223', NahuelHuapi='SAM-02', OHiggins='SAM-266',
  Mjosa='EUR-32', Van='ASI-251', Poso='ASI-319', Fagnano='SAM-270', GreatBear='NAM-30', Manapouri='OCE-208', Como='EUR-208', TeAnau='OCE-209',
  Tazawa='ASI-244', Khantayskoye='ASI-221', Wakatipu='OCE-210', Superior='NAM-04', Argentino='SAM-269', Viedma='SAM-268', Hawea='OCE-212',
  Maggiore='EUR-05', Garda='EUR-218', Geneva='EUR-07', Ohrid='EUR-278', DeadSea='ASI-209', Titicaca='SAM-04')
UA = {'User-Agent': 'Mozilla/5.0'}
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read().decode('utf-8', 'replace')
out = {}
for name, lid in ids.items():
    dl = D / f'dl_{lid}.html'
    if not dl.exists(): dl.write_text(get(f'https://wldb.ilec.or.jp/Lake/{lid}/datalist'), encoding='utf-8'); time.sleep(0.5)
    m = re.search(r'href="(https://wldb.ilec.or.jp/Display/html/\d+)"', dl.read_text(encoding='utf-8'))
    if not m: out[name] = {'id': lid, 'err': 'no databook'}; print(name, 'no databook'); continue
    url = m.group(1); f = D / (url.rsplit('/', 1)[1] + '.html')
    if not f.exists(): f.write_text(get(url), encoding='utf-8'); time.sleep(0.5)
    t = f.read_text(encoding='utf-8')
    row = {'id': lid, 'url': url}
    for k in ['Maximum depth', 'Mean depth', 'Surface area', 'Altitude', 'Volume']:
        mm = re.search(k + r'[^<]*</TD>\s*<TD>([^<]*)', t, re.I)
        if mm: row[k] = html.unescape(mm.group(1)).strip()
    loc = re.sub(r'<[^>]+>', ' ', t); loc = re.sub(r'\s+', ' ', html.unescape(loc))
    i = loc.find('A. LOCATION'); row['location'] = loc[i:i+260] if i >= 0 else ''
    out[name] = row
    print(name, lid, url, row.get('Maximum depth'), row.get('Surface area'), '|', row['location'][:200])
json.dump(out, open(D / 'ilec_summary.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
