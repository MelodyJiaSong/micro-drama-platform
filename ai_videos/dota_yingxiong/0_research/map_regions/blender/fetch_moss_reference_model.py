"""Fetch one CC0 moss model without rewriting the existing environment manifests."""
from pathlib import Path
import requests,json,hashlib,datetime
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d/environment_sources/moss_01';OUT.mkdir(exist_ok=True)
headers={'User-Agent':'DotaLocalAssetBuild/1.0'}
meta=requests.get('https://api.polyhaven.com/files/moss_01',headers=headers,timeout=40);meta.raise_for_status();data=meta.json();(OUT/'files_metadata.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
entry=dict(data['blend']['2k']['blend']);includes=entry.pop('include',{});jobs=[(OUT/entry['url'].rsplit('/',1)[-1],entry)]+[(OUT/p,e) for p,e in includes.items()]
plan={'at':datetime.datetime.now().astimezone().isoformat(),'asset':'moss_01','source':'https://polyhaven.com/a/moss_01','license':'CC0','license_url':'https://polyhaven.com/license','status':'download_planned','jobs':[{'path':str(p.relative_to(OUT)),**e} for p,e in jobs]};(OUT/'provenance.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
records=[]
for p,e in jobs:
 p.parent.mkdir(exist_ok=True,parents=True)
 if not p.exists() or hashlib.md5(p.read_bytes()).hexdigest()!=e['md5']:
  r=requests.get(e['url'],headers=headers,timeout=(30,120));r.raise_for_status();assert hashlib.md5(r.content).hexdigest()==e['md5'];p.write_bytes(r.content)
 records.append({'path':str(p.relative_to(OUT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'md5':e['md5']});print('FETCHED_VERIFIED',p.name,flush=True)
plan.update(status='downloaded_checksum_verified',files=records);(OUT/'provenance.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
