"""Version and inspect pre-fix exports without replacing their originals."""
from pathlib import Path
import json, subprocess, sys, datetime
import local_mesh as lm
HERE=Path(__file__).resolve().parent
BLENDER='C:/Program Files/Blender Foundation/Blender 5.2/blender.exe'
manifest=json.loads(lm.MANIFEST.read_text(encoding='utf-8'))
heights=json.loads((lm.MANIFEST.parent/'model_calibration.json').read_text(encoding='utf-8'))['heights']
jobs=[('m300','r08','r16','authored'),('m4','r14','r15','authored'),('bg2','r06','r07','preview'),('bg3','r04','r05','preview'),('bg15','r08','r09','preview'),('bg16','r01','r02','raw'),('bg17','r01','r02','raw'),('bg18','r01','r02','raw'),('bg19','r01','r02','raw')]
state={'started_at':datetime.datetime.now().astimezone().isoformat(),'status':'running','results':[]}
report=lm.MANIFEST.parent/'legacy_normal_repairs.json'
def run(script,arguments,log,blender=False):
    command=([BLENDER,'--factory-startup','--background','--threads','8','--python-exit-code','1','--python',str(HERE/script),'--'] if blender else [sys.executable,'-X','utf8',str(HERE/script)])+arguments
    with log.open('w',encoding='utf-8') as stream:subprocess.run(command,stdout=stream,stderr=subprocess.STDOUT,check=True,creationflags=subprocess.CREATE_NO_WINDOW)
def save():report.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
for asset,source,revision,kind in jobs:
    a=next(a for a in manifest['assets'] if a['id']==asset);folder=lm.DRAMA/a['model_directory']/revision;folder.mkdir(exist_ok=True)
    state['active_asset']=asset;save();print('REPAIR',asset,revision,flush=True)
    try:
        if kind=='raw':
            if not (folder/'normal_repair.json').exists():run('repair_model_export.py',[asset,'--source',source,'--revision',revision],folder/'repair.log')
            if not (folder/'inspection'/f'{asset}_{revision}.blend').exists():run('inspect_model.py',[asset,'--revision',revision,'--height',str(heights[asset]),'--samples','16'],folder/'inspection.log',True)
        else:
            if not (folder/'authoring.blend').exists():run('repair_authored_normals.py',[asset,'--source',source,'--revision',revision]+(['--authoring-source'] if kind=='preview' else []),folder/'repair.log',True)
            if not (folder/'inspection'/f'{asset}_{revision}.blend').exists():run('render_authored_asset.py',[asset,'--revision',revision,'--base-revision',source],folder/'inspection.log',True)
        state['results'].append({'asset':asset,'revision':revision,'status':'candidate_pending_review'})
    except Exception as e:
        state['results'].append({'asset':asset,'revision':revision,'status':'failed','error':str(e)})
    save();print(state['results'][-1],flush=True)
    subprocess.run([sys.executable,'-X','utf8',str(HERE/'asset_status.py')],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
state['status']='finished_candidates_not_accepted';state['finished_at']=datetime.datetime.now().astimezone().isoformat();save()
