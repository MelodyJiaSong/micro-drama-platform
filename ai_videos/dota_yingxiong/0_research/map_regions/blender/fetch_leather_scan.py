"""Download one CC0 leather scan with source hashes for the Furbolg cape repair."""
from pathlib import Path
import requests,json,hashlib,datetime,time
ROOT=Path(__file__).resolve().parents[3];out=next(ROOT.glob('2_*'))/'background/map_3d/environment_sources/brown_leather';out.mkdir(exist_ok=True)
log=out/'provenance.json';record={'asset':'brown_leather','source':'https://polyhaven.com/a/brown_leather','author':'Rob Tuytel','license':'CC0','license_evidence':'https://polyhaven.com/license','physical_height_m':.4,'at':datetime.datetime.now().astimezone().isoformat(),'status':'requested','files':[]}
if log.exists():
 previous=json.loads(log.read_text(encoding='utf-8'));record['previous_runs']=previous.get('previous_runs',[])+[{k:v for k,v in previous.items() if k!='previous_runs'}]
log.write_text(json.dumps(record,indent=2),encoding='utf-8');headers={'User-Agent':'DotaLocalAssetBuild/1.0'}
meta=out/'files.json'
if meta.exists():data=json.loads(meta.read_text(encoding='utf-8'))
else:
 response=requests.get('https://api.polyhaven.com/files/brown_leather',headers=headers,timeout=40);response.raise_for_status();data=response.json();meta.write_text(json.dumps(data,indent=2),encoding='utf-8')
for kind,fmt in [('Diffuse','jpg'),('Rough','jpg'),('nor_gl','png'),('Displacement','png')]:
 entry=data[kind]['4k'][fmt];path=out/entry['url'].rsplit('/',1)[-1];row={'kind':kind,'path':path.name,'url':entry['url'],'source_md5':entry['md5'],'status':'requested'};record['files'].append(row);log.write_text(json.dumps(record,indent=2),encoding='utf-8')
 if not path.exists():
  row['attempts']=[]
  for attempt in range(3):
   try:
    response=requests.get(entry['url'],headers=headers,timeout=(20,45));response.raise_for_status();content=response.content;assert hashlib.md5(content).hexdigest()==entry['md5'];path.write_bytes(content);row['attempts'].append({'attempt':attempt+1,'status':'downloaded'});break
   except Exception as exc:
    row['attempts'].append({'attempt':attempt+1,'status':'failed','error':str(exc)});log.write_text(json.dumps(record,indent=2),encoding='utf-8');print('DOWNLOAD_RETRY',kind,attempt+1,type(exc).__name__,flush=True)
    if attempt==2:raise
    time.sleep(2)
 content=path.read_bytes();assert hashlib.md5(content).hexdigest()==entry['md5'];row.update(status='downloaded_hash_verified',bytes=len(content),sha256=hashlib.sha256(content).hexdigest());log.write_text(json.dumps(record,indent=2),encoding='utf-8');print(kind,len(content),flush=True)
record['status']='downloaded_hash_verified';log.write_text(json.dumps(record,indent=2),encoding='utf-8')
