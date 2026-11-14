import sys; sys.stdout.reconfigure(encoding="utf-8")
import json,sys
from pathlib import Path
d=json.load(open('../data.json',encoding='utf-8'))
for i in map(int,sys.argv[1:]):
    it=d['items'][i]; p=Path('reselect/cand')/f"{i:02d}_{Path(it['image']).stem}"/'meta.json'
    print('==',i,it['name'])
    for c in json.load(open(p,encoding='utf-8')):
        print(f"  {c['id']:4} {c.get('w')}x{c.get('h')} {c['licence'][:28]:28} | {c['author'][:18]:18} | {c['why'][:110]} | {c['page_url'][:80]}")
