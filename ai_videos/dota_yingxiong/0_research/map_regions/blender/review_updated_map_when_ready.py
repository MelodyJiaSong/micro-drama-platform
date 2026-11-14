"""Complete the five-view environment inspection once a selected draft is rendered."""
from pathlib import Path
import argparse,json,subprocess,sys,time,datetime
from map_render_slot import map_render_slot
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];OUT=next(ROOT.glob('2_*'))/'background/map_3d';BLENDER='C:/Program Files/Blender Foundation/Blender 5.2/blender.exe'
p=argparse.ArgumentParser();p.add_argument('--environment',required=True);p.add_argument('--attempt',default='01');args=p.parse_args();receipt=OUT/(Path(args.environment).stem+'_whole_map_review_job.json');deadline=time.monotonic()+6*3600
prior=json.loads(receipt.read_text(encoding='utf-8')) if receipt.exists() else None
job={'at':datetime.datetime.now().astimezone().isoformat(),'environment':args.environment,'status':'waiting_for_complete_draft','attempt':args.attempt,'previous_attempt':prior}
def save():receipt.write_text(json.dumps(job,indent=2),encoding='utf-8')
save()
while time.monotonic()<deadline:
    state=json.loads((OUT/'draft_refresh_state.json').read_text(encoding='utf-8'));drafts=[d for d in state['drafts'] if d.get('environment')==args.environment]
    if drafts:break
    time.sleep(10)
else:raise TimeoutError('Selected map environment was not assembled')
blend=drafts[-1]['file'];stem=Path(blend).stem;job.update(status='waiting_for_map_render_slot',blend=blend);save()
with map_render_slot(OUT):
    job['status']='rendering_three_supplemental_views';save()
    try:
        # Each camera gets a fresh process so evaluated geometry and texture caches are released.
        for camera in ['Mid_River','Sentinel_Base','Scourge_Base']:
            if (OUT/(stem+'_'+camera+'.png')).exists():continue
            job['camera']=camera;save()
            with (OUT/(stem+'_supplemental_'+args.attempt+'_'+camera+'.log')).open('w',encoding='utf-8') as log:subprocess.run([BLENDER,'--factory-startup','--background','--threads','8','--python-exit-code','1','--python',str(HERE/'render_map_check.py'),'--','--blend',blend,'--cameras',camera],stdout=log,stderr=subprocess.STDOUT,check=True,creationflags=subprocess.CREATE_NO_WINDOW)
    except Exception as exc:
        job.update(status='render_failed',error=str(exc));save();raise
job['status']='independent_environment_review';save()
with (OUT/(stem+'_environment_review_process.log')).open('w',encoding='utf-8') as log:subprocess.run([sys.executable,'-X','utf8',str(HERE/'review_map_environment.py'),'--blend',blend],stdout=log,stderr=subprocess.STDOUT,check=True,creationflags=subprocess.CREATE_NO_WINDOW)
result=json.loads((OUT/(stem+'_environment_review.json')).read_text(encoding='utf-8'));job.update(status='review_finished_not_final_map_acceptance',verdict=result.get('verdict'),blockers=len(result.get('blockers',[])),completed_at=datetime.datetime.now().astimezone().isoformat());save();print(json.dumps(job),flush=True)
