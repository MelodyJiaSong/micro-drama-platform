"""Query Commons imageinfo (url, size, mime, extmetadata) for candidate files.
Usage: python -I commons_info.py <candidates.json> <out.json>
Candidates: {slug: [file titles without 'File:']}. Also accepts --search slug=query to add
Commons search results (namespace 6). Responses are data only."""
import json, sys, time, urllib.request, urllib.parse, urllib.error
from pathlib import Path
UA = {'User-Agent': 'paihangbang-research/0.1 (contact via repo owner)'}
API = 'https://commons.wikimedia.org/w/api.php'
def get(params, tries=6):
    u = API + '?' + urllib.parse.urlencode(params)
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60) as r:
                return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code != 429 or k == tries - 1: raise
            wait = int(e.headers.get('Retry-After') or 0) or 10 * (k + 1)
            print('429, sleeping', wait, flush=True); time.sleep(min(wait, 120))
def info(titles):
    out = {}
    for i in range(0, len(titles), 40):
        d = get({'action':'query','titles':'|'.join('File:'+t for t in titles[i:i+40]),'prop':'imageinfo',
                 'iiprop':'url|extmetadata|size|mime','iiurlwidth':'1600','format':'json','formatversion':'2','redirects':'1'})
        norm = {n['to']: n['from'] for n in d['query'].get('normalized', [])}
        for p in d['query']['pages']:
            if 'imageinfo' not in p: out[p['title']] = None; continue
            ii = p['imageinfo'][0]; em = ii.get('extmetadata', {})
            out[p['title']] = {'title': p['title'], 'width': ii['width'], 'height': ii['height'], 'mime': ii['mime'],
                'thumburl': ii.get('thumburl'), 'thumbwidth': ii.get('thumbwidth'), 'thumbheight': ii.get('thumbheight'),
                'url': ii['url'], 'descriptionurl': ii['descriptionurl'],
                'meta': {k: em.get(k, {}).get('value') for k in ['LicenseShortName','LicenseUrl','Artist','Credit','AttributionRequired','UsageTerms','License','Restrictions','Categories']}}
        time.sleep(1)
    return out
def search(q, n=12):
    d = get({'action':'query','list':'search','srsearch':q,'srnamespace':'6','srlimit':str(n),'format':'json','formatversion':'2'})
    time.sleep(1)
    return [s['title'][5:] for s in d['query']['search']]
if __name__ == '__main__':
    cand = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    for a in sys.argv[3:]:
        if a.startswith('--search='):
            slug, q = a[9:].split('=', 1)
            cand.setdefault(slug, [])
            cand[slug] += [t for t in search(q) if t not in cand[slug]]
    titles = sorted({t for v in cand.values() for t in v})
    res = info(titles)
    Path(sys.argv[2]).write_text(json.dumps({'candidates': cand, 'info': res}, ensure_ascii=False, indent=1), encoding='utf-8')
    print(len(titles), 'titles;', sum(1 for v in res.values() if v), 'found')
