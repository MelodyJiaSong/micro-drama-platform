"""Fetch CC0 environment sources with manifests and checksum verification."""
from pathlib import Path
import requests, json, hashlib, concurrent.futures, time

ROOT=Path(__file__).resolve().parents[3]
OUT=next(ROOT.glob('2_*'))/'background/map_3d/environment_sources'
OUT.mkdir(parents=True,exist_ok=True)
ASSETS=['tree_small_02','fir_tree_01','rock_face_02','coast_rocks_02','grass_medium_01','dead_tree_trunk_02','island_tree_01','jacaranda_tree','fern_02','shrub_02','flower_heliophila','flower_ursinia','tree_stump_01','boulder_01','brass_pot_01']
HEADERS={'User-Agent':'DotaLocalAssetBuild/1.0'}

def fetch(job):
    path,entry=job
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists() and hashlib.md5(path.read_bytes()).hexdigest()==entry['md5']:
        return {'path':str(path.relative_to(OUT)),**entry,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    for attempt in range(3):
        try:
            r=requests.get(entry['url'],headers=HEADERS,timeout=(30,120));r.raise_for_status()
            if hashlib.md5(r.content).hexdigest()!=entry['md5']:raise ValueError('Checksum mismatch '+str(path))
            path.write_bytes(r.content)
            print('FETCHED',path.name,len(r.content),flush=True)
            return {'path':str(path.relative_to(OUT)),**entry,'sha256':hashlib.sha256(r.content).hexdigest()}
        except Exception:
            if attempt==2:raise
            time.sleep(2)

jobs=[]
for asset in ASSETS:
    meta=OUT/(asset+'_files.json')
    if meta.exists():data=json.loads(meta.read_text())
    else:
        r=requests.get('https://api.polyhaven.com/files/'+asset,headers=HEADERS,timeout=40);r.raise_for_status();data=r.json();meta.write_text(json.dumps(data,indent=2))
    entry=dict(data['blend']['2k']['blend']);includes=entry.pop('include',{})
    jobs.append((OUT/asset/entry['url'].rsplit('/',1)[-1],entry))
    jobs.extend((OUT/asset/p,e) for p,e in includes.items())
(OUT/'download_plan.json').write_text(json.dumps({'license':'CC0','license_url':'https://polyhaven.com/license','jobs':[{'path':str(p.relative_to(OUT)),**e} for p,e in jobs]},indent=2))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    records=list(pool.map(fetch,jobs))
(OUT/'sources.json').write_text(json.dumps({'license':'CC0','license_url':'https://polyhaven.com/license','files':records},indent=2))
print('VERIFIED',len(records),flush=True)
