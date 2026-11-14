"""Download small Commons thumbnails and build labelled contact sheets for visual review.
Usage: python -I preview_sheet.py <titles.json: [[label, file title], ...]> <out_dir>
Downloads are untrusted image data, opened only with Pillow."""
import json, sys, time, io, urllib.request, urllib.parse, urllib.error
from pathlib import Path
from PIL import Image, ImageDraw
UA = {'User-Agent': 'paihangbang-research/0.1 (contact via repo owner)'}
def fetch(u, tries=6):
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60) as r: return r.read()
        except urllib.error.HTTPError as e:
            if e.code != 429 or k == tries-1: raise
            time.sleep(min(int(e.headers.get('Retry-After') or 0) or 10*(k+1), 120))
items = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
titles = [t for _, t in items]; thumbs = {}
for i in range(0, len(titles), 40):
    q = {'action':'query','titles':'|'.join('File:'+t for t in titles[i:i+40]),'prop':'imageinfo','iiprop':'url','iiurlwidth':'360','format':'json','formatversion':'2'}
    d = json.loads(fetch('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(q)))
    norm = {n['to']: n['from'] for n in d['query'].get('normalized', [])}
    for p in d['query']['pages']:
        if 'imageinfo' in p: thumbs[norm.get(p['title'], p['title'])[5:]] = p['imageinfo'][0]['thumburl']
    time.sleep(1)
tiles = []
for label, t in items:
    u = thumbs.get(t)
    if not u: print('no thumb', t); continue
    try:
        im = Image.open(io.BytesIO(fetch(u))).convert('RGB')
    except Exception as e:
        print('fail', t, e); continue
    im.thumbnail((360, 240)); tile = Image.new('RGB', (360, 270), 'white'); tile.paste(im, ((360-im.width)//2, 0))
    ImageDraw.Draw(tile).text((4, 248), label[:58], fill='black'); tiles.append(tile); time.sleep(0.5)
for s in range(0, len(tiles), 12):
    sheet = Image.new('RGB', (360*4, 270*3), 'gray')
    for k, tl in enumerate(tiles[s:s+12]): sheet.paste(tl, ((k % 4)*360, (k//4)*270))
    sheet.save(out/f'sheet_{s//12+1:02d}.jpg', quality=85)
print(len(tiles), 'tiles')
