"""Version a retained AI model with verified normal repair; no generation call."""
import argparse,json,hashlib,shutil,datetime
from pathlib import Path
import local_mesh as lm
from check_glb_normals import repair_exported_normals
p=argparse.ArgumentParser();p.add_argument('asset');p.add_argument('--source',required=True);p.add_argument('--revision',required=True);args=p.parse_args()
manifest=json.loads(lm.MANIFEST.read_text(encoding='utf-8'));asset=next(a for a in manifest['assets'] if a['id']==args.asset);folder=lm.DRAMA/asset['model_directory'];source=next((folder/args.source).glob('*_pbr_*.glb'));destdir=folder/args.revision
destdir.mkdir(exist_ok=True);dest=destdir/(args.asset+'_'+args.revision+'_pbr_normal_corrected.glb')
if dest.exists():raise FileExistsError(dest)
original_sha=hashlib.sha256(source.read_bytes()).hexdigest();shutil.copy2(source,dest);result=repair_exported_normals(dest)
report={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source':str(source),'source_sha256':original_sha,'output':dest.name,'output_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'generation_requests':0,'images_changed':False,'geometry_positions_changed':False,'repair':result}
(destdir/'normal_repair.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps({'asset':args.asset,'revision':args.revision,'applied':result['applied'],'output':str(dest)},ensure_ascii=False))
