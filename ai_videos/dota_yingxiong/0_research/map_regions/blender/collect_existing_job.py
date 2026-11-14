"""Collect and inspect a recorded request; never submit another generation."""
import argparse,json,subprocess,time,sys
from pathlib import Path
import local_mesh as lm
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('asset');p.add_argument('--revision',required=True);args=p.parse_args()
manifest=json.loads(lm.MANIFEST.read_text(encoding='utf-8'));asset=next(a for a in manifest['assets'] if a['id']==args.asset)
folder=lm.DRAMA/asset['model_directory']/args.revision
request=json.loads((folder/'generation.json').read_text(encoding='utf-8'));prompt=request['prompt_id']
while request['status'] not in ['generated_pending_review','failed']:
    if lm.api('/history/'+prompt).get(prompt):
        lm.status(args.asset,args.revision);request=json.loads((folder/'generation.json').read_text(encoding='utf-8'))
    else:
        q=lm.api('/queue')
        if not any(r[1]==prompt for r in q['queue_running']+q['queue_pending']):raise RuntimeError('Recorded job not found in queue or history')
        time.sleep(20)
if request['status']=='failed':raise RuntimeError('Generation failed; receipt retained')
dest=folder/'inspection'/f'{args.asset}_{args.revision}.blend'
if not dest.exists():
    heights=json.loads((lm.MANIFEST.parent/'model_calibration.json').read_text(encoding='utf-8'))['heights']
    with (folder/'inspection.log').open('w',encoding='utf-8') as log:
        subprocess.run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','--factory-startup','--background','--python-exit-code','1','--python',str(HERE/'inspect_model.py'),'--',args.asset,'--revision',args.revision,'--height',str(heights[args.asset]),'--samples','24'],stdout=log,stderr=subprocess.STDOUT,check=True,creationflags=subprocess.CREATE_NO_WINDOW)
print('CANDIDATE_SAVED',str(dest),flush=True)
if not (folder/'inspection/independent_review.json').exists():
    subprocess.run([sys.executable,'-X','utf8',str(HERE/'review_model_asset.py'),args.asset,'--revision',args.revision],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
