from pathlib import Path
import requests,json,hashlib,concurrent.futures,datetime
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d/environment_sources';dest=OUT/'bark_brown_02';dest.mkdir(exist_ok=True);data=json.loads((OUT/'bark_brown_02_files.json').read_text());jobs=[data[k]['4k'][fmt] for k,fmt in [('Diffuse','jpg'),('Displacement','png'),('Rough','jpg')]]
def fetch(entry):
 p=dest/entry['url'].rsplit('/',1)[-1]
 if not p.exists():
  r=requests.get(entry['url'],timeout=(20,120));r.raise_for_status();assert hashlib.md5(r.content).hexdigest()==entry['md5'];p.write_bytes(r.content)
 assert hashlib.md5(p.read_bytes()).hexdigest()==entry['md5']
 return dict(entry,path=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:records=list(pool.map(fetch,jobs))
(dest/'provenance.json').write_text(json.dumps({'at':datetime.datetime.now().astimezone().isoformat(),'source':'https://polyhaven.com/a/bark_brown_02','license':'CC0','license_url':'https://polyhaven.com/license','files':records},indent=2),encoding='utf-8');print('VERIFIED',len(records),flush=True)
