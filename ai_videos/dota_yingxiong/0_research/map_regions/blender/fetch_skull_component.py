"""Download only the CC0 skull component from Blender's official asset repo."""
from pathlib import Path
import requests,json,hashlib,datetime,concurrent.futures,time
root=Path(__file__).resolve().parents[3];out=next(root.glob('2_*'))/'background/map_3d/environment_sources/blender_human_base_meshes';out.mkdir(parents=True,exist_ok=True)
api='https://projects.blender.org/api/v1/repos/blender/blender-assets/contents/publish/online/base_meshes/human_base_meshes__realistic-skull.blend'
r=requests.get(api,timeout=30);r.raise_for_status();metadata=r.json();(out/'skull_repository_metadata.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
record={'source':metadata['download_url'],'repository_blob_sha':metadata['sha'],'license':'CC0','license_evidence':'https://developer.blender.org/docs/release_notes/3.6/asset_bundles/','status':'requested','at':datetime.datetime.now().astimezone().isoformat()};log=out/'skull_provenance.json';log.write_text(json.dumps(record,indent=2),encoding='utf-8')
try:
 r=requests.get(metadata['download_url'],timeout=90);r.raise_for_status();content=r.content
 if content.startswith(b'version https://git-lfs.github.com'):
  fields=dict(line.split(' ',1) for line in content.decode().splitlines());oid=fields['oid'].split(':',1)[1];size=int(fields['size'])
  batch=requests.post('https://projects.blender.org/blender/blender-assets.git/info/lfs/objects/batch',json={'operation':'download','transfers':['basic'],'objects':[{'oid':oid,'size':size}]},headers={'Accept':'application/vnd.git-lfs+json'},timeout=30);batch.raise_for_status()
  action=batch.json()['objects'][0]['actions']['download'];parts=out/'skull_parts';parts.mkdir(exist_ok=True);chunk=262144
  def part(start):
   end=min(size,start+chunk)-1;p=parts/f'{start:09d}.bin'
   if p.exists() and p.stat().st_size==end-start+1:return p
   for attempt in range(4):
    try:
     headers=dict(action.get('header',{}));headers['Range']=f'bytes={start}-{end}'
     href=action['href']
     # Public LFS endpoint has no signed query; give each range a distinct URL
     # so an intermediary cannot reuse a stalled response for another range.
     if '?' not in href:href+=f'?range_start={start}&attempt={attempt}'
     r=requests.get(href,headers=headers,timeout=25);r.raise_for_status()
     if r.status_code!=206 or r.headers.get('Content-Range')!=f'bytes {start}-{end}/{size}' or len(r.content)!=end-start+1:raise ValueError('Invalid partial content')
     p.write_bytes(r.content);print('PART',start,flush=True);return p
    except Exception:
     if attempt==3:raise
     time.sleep(2)
  with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:pieces=list(pool.map(part,range(0,size,chunk)))
  content=b''.join(p.read_bytes() for p in pieces)
  if len(content)!=size or hashlib.sha256(content).hexdigest()!=oid:raise ValueError('Git LFS size or SHA256 mismatch')
  record.update(lfs_sha256=oid,lfs_size=size)
 if not (content.startswith(b'BLENDER') or content[:4]==bytes.fromhex('28b52ffd')):raise ValueError('Unexpected Blender header: '+repr(content[:30]))
 target=out/'realistic_skull.blend';target.write_bytes(content)
 record.update(status='downloaded',bytes=len(content),sha256=hashlib.sha256(content).hexdigest());print(json.dumps(record),flush=True)
except Exception as exc:record.update(status='failed',error=str(exc));raise
finally:log.write_text(json.dumps(record,indent=2),encoding='utf-8')
