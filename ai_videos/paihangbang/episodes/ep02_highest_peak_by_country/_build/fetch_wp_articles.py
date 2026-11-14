"""Fetch enwiki sitelinks for candidate peaks (Wikidata wbgetentities), then the
article wikitext + short description (Wikipedia API). Facts only; no text reused.
Writes raw/wp_articles_2026-11-03.json. Polite: batched, 1 s sleeps."""
import json, time, urllib.request, urllib.parse
from pathlib import Path
here = Path(__file__).parent
UA = {'User-Agent': 'paihangbang-research/0.1 (contact via repo owner)'}
def get(url, params):
    u = url + '?' + urllib.parse.urlencode(params)
    with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60) as r:
        return json.loads(r.read().decode('utf-8'))
meta = json.loads((here/'raw'/'wikidata_peaks_meta_2026-11-03.json').read_text(encoding='utf-8'))
qids = sorted({b['p']['value'].split('/')[-1] for b in meta['results']['bindings']})
sitelinks = {}
for i in range(0, len(qids), 50):
    d = get('https://www.wikidata.org/w/api.php', {'action':'wbgetentities','ids':'|'.join(qids[i:i+50]),
            'props':'sitelinks|labels','sitefilter':'enwiki','languages':'en','format':'json'})
    for q, e in d['entities'].items():
        sitelinks[q] = {'enwiki': e.get('sitelinks',{}).get('enwiki',{}).get('title'),
                        'label': e.get('labels',{}).get('en',{}).get('value')}
    time.sleep(1)
titles = [v['enwiki'] for v in sitelinks.values() if v['enwiki']]
pages = {}
for i in range(0, len(titles), 20):
    d = get('https://en.wikipedia.org/w/api.php', {'action':'query','titles':'|'.join(titles[i:i+20]),
            'prop':'revisions|description','rvprop':'content|ids','rvslots':'main','format':'json','formatversion':'2','redirects':'1'})
    for p in d['query']['pages']:
        pages[p['title']] = {'description': p.get('description'),
                             'revid': p['revisions'][0]['revid'] if p.get('revisions') else None,
                             'wikitext': p['revisions'][0]['slots']['main']['content'] if p.get('revisions') else ''}
    time.sleep(1)
(here/'raw'/'wp_articles_2026-11-03.json').write_text(json.dumps({'sitelinks':sitelinks,'pages':pages}, ensure_ascii=False), encoding='utf-8')
print(len(sitelinks), len(pages))
