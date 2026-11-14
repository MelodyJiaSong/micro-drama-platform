"""Acquire the official CC0 Blender base-mesh bundle for anatomical components."""
from pathlib import Path
import requests,zipfile,json,hashlib,datetime,concurrent.futures
ROOT=Path(__file__).resolve().parents[3];out=next(ROOT.glob('2_*'))/'background/map_3d/environment_sources/blender_human_base_meshes';out.mkdir(parents=True,exist_ok=True)
url='https://download.blender.org/demo/asset-bundles/human-base-meshes/human-base-meshes-bundle-v1.2.0.zip';target=out/'human-base-meshes-bundle-v1.2.0.zip';log=out/'provenance.json'
prior=json.loads(log.read_text(encoding='utf-8')) if log.exists() else None
record={'source':url,'license':'CC0','license_evidence':'https://commons.wikimedia.org/wiki/File:Skull_-_Realistic_by_Paul_Kotelevets,_Tonatiuh_de_San_Juli%C3%A1n_(CC0).stl','purpose':'Detailed skull geometry for the approved Scourge tower skull ring; anatomy component only','requested_at':datetime.datetime.now().astimezone().isoformat(),'status':'requested','prior_attempt':prior}
log.write_text(json.dumps(record,indent=2),encoding='utf-8')
if not target.exists():
 # A normal streamed GET stalled after headers. Verified range requests are
 # supported; save each independent part and validate Content-Range before join.
 total=49674480;chunk=1024*1024;parts=out/'parts';parts.mkdir(exist_ok=True)
 def fetch(start):
  end=min(start+chunk,total)-1;p=parts/f'{start:09d}.bin'
  if p.exists() and p.stat().st_size==end-start+1:return p
  r=requests.get(url+f'?range_start={start}',headers={'Range':f'bytes={start}-{end}'},timeout=90);r.raise_for_status()
  if r.status_code!=206 or r.headers.get('Content-Range')!=f'bytes {start}-{end}/{total}' or len(r.content)!=end-start+1:raise ValueError('Invalid range response')
  p.write_bytes(r.content);print('PART',start,len(r.content),flush=True);return p
 try:
  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:pieces=list(pool.map(fetch,range(0,total,chunk)))
  with target.with_suffix('.part').open('wb') as f:
   for piece in pieces:f.write(piece.read_bytes())
  with zipfile.ZipFile(target.with_suffix('.part')) as z:
   bad=z.testzip()
   if bad:raise ValueError('CRC mismatch: '+bad)
  target.with_suffix('.part').replace(target)
 except Exception as exc:
  record.update(status='download_failed',error=str(exc));log.write_text(json.dumps(record,indent=2),encoding='utf-8');raise
with zipfile.ZipFile(target) as z:
 names=z.namelist()
 for name in names:
  p=(out/name).resolve()
  if not p.is_relative_to(out.resolve()):raise ValueError(name)
 z.extractall(out)
record.update(status='downloaded',bytes=target.stat().st_size,sha256=hashlib.sha256(target.read_bytes()).hexdigest(),members=names);log.write_text(json.dumps(record,indent=2),encoding='utf-8')
print('\n'.join(names))
