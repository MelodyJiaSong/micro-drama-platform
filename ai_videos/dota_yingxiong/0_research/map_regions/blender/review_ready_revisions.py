"""Review explicitly selected manual revisions after their renders are complete."""
from pathlib import Path
import argparse,json,subprocess,sys,time
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];OUT=next(ROOT.glob('2_*'))/'background/map_3d'
p=argparse.ArgumentParser();p.add_argument('revisions',nargs='+');args=p.parse_args();manifest=json.loads((OUT/'asset_manifest.json').read_text(encoding='utf-8'));pending=list(args.revisions);deadline=time.monotonic()+3*3600
while pending:
    progressed=False
    for key in pending[:]:
        asset,revision=key.split(':');a=next(a for a in manifest['assets'] if a['id']==asset);folder=ROOT/a['model_directory']/revision/'inspection';blend=folder/f'{asset}_{revision}.blend'
        if not (folder/'inspection.json').exists() or not blend.exists():continue
        if not (folder/'independent_review.json').exists():
            print('REVIEW',key,flush=True)
            with (folder/'independent_review_process.log').open('w',encoding='utf-8') as log:subprocess.run([sys.executable,'-X','utf8',str(HERE/'review_model_asset.py'),asset,'--revision',revision],stdout=log,stderr=subprocess.STDOUT,check=True,creationflags=subprocess.CREATE_NO_WINDOW)
        pending.remove(key);progressed=True;print('REVIEWED',key,flush=True)
        subprocess.run([sys.executable,'-X','utf8',str(HERE/'asset_status.py')],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
    if time.monotonic()>deadline:raise TimeoutError('Revisions not ready: '+','.join(pending))
    if pending and not progressed:time.sleep(20)
