"""Create versioned map drafts as locally generated candidate libraries grow."""
from pathlib import Path
import json,time,subprocess,sys,datetime,argparse
import local_mesh as lm
from map_render_slot import map_render_slot
HERE=Path(__file__).resolve().parent;OUT=lm.MANIFEST.parent;BLENDER='C:/Program Files/Blender Foundation/Blender 5.2/blender.exe'
parser=argparse.ArgumentParser();parser.add_argument('--environment',default='environment_v013.blend');parser.add_argument('--force-once',action='store_true',help='Reassemble changed asset revisions or placement logic even when family count is unchanged');parser.add_argument('--render-minimum-gib',type=float,default=88);parser.add_argument('--texture-limit',choices=['512','1024','2048'],default='2048');args=parser.parse_args()
if not (OUT/args.environment).is_file():raise FileNotFoundError(args.environment)
statefile=OUT/'draft_refresh_state.json';deadline=time.monotonic()+24*3600
state=json.loads(statefile.read_text(encoding='utf-8')) if statefile.exists() else {'drafts':[]}
state.setdefault('runs',[]).append({'at':datetime.datetime.now().astimezone().isoformat(),'environment':args.environment,'force_once':args.force_once,'render_minimum_gib':args.render_minimum_gib,'preview_texture_limit':args.texture_limit})
state.update(status='waiting_for_current_repairs',active_environment=args.environment)
def save():statefile.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
def run(script,script_args,log):
 with map_render_slot(OUT,minimum_gib=args.render_minimum_gib if script=='render_map_check.py' else 64),log.open('w',encoding='utf-8') as stream:subprocess.run([BLENDER,'--factory-startup','--background','--threads','8','--python-exit-code','1','--python',str(HERE/script),'--']+script_args,stdout=stream,stderr=subprocess.STDOUT,check=True,creationflags=subprocess.CREATE_NO_WINDOW)
save();manifest=json.loads(lm.MANIFEST.read_text(encoding='utf-8'));wisp=next(a for a in manifest['assets'] if a['id']=='m306');last=state['drafts'][-1] if state['drafts'] else {};last_count=last.get('families',0);last_environment=last.get('environment','environment_v013.blend')
while time.monotonic()<deadline:
 try:
  repairs=json.loads((OUT/'legacy_normal_repairs.json').read_text(encoding='utf-8'))
  if repairs['status']!='finished_candidates_not_accepted' or not (lm.DRAMA/wisp['model_directory']/'r17/inspection/inspection.json').exists():time.sleep(30);continue
  subprocess.run([sys.executable,'-X','utf8',str(HERE/'asset_status.py')],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
  current=json.loads((OUT/'current_status.json').read_text(encoding='utf-8'));count=current['families_with_candidates'];batch=json.loads((OUT/'batch_full_models_v1.json').read_text(encoding='utf-8'));batch_done=batch['status']=='candidates_generated_pending_review'
  if args.force_once or last_count==0 or count>=last_count+5 or args.environment!=last_environment or (batch_done and count>last_count):
   versions=[int(p.stem.rsplit('v',1)[1]) for p in OUT.glob('assembly_working_v*.blend')];name=f'assembly_working_v{max(versions,default=0)+1:03d}.blend';state.update(status='assembling_draft',active_file=name);save();print('ASSEMBLE',name,count,flush=True)
   run('assemble_map.py',['--environment',args.environment,'--output',name,'--draft'],OUT/(Path(name).stem+'_assembly.log'))
   state['status']='rendering_draft';save()
   # A fresh process for each view avoids retained BVH/image memory, as verified
   # by the successful v020 recovery after the combined render ran out of RAM.
   for camera in ['Map_Overview','Sentinel_Forest_Eye']:
    run('render_map_check.py',['--blend',name,'--cameras',camera,'--texture-limit',args.texture_limit],OUT/(Path(name).stem+'_'+camera+'_render.log'))
   state['drafts'].append({'file':name,'families':count,'environment':args.environment,'at':datetime.datetime.now().astimezone().isoformat(),'acceptance':'DRAFT_NOT_RELEASED'});last_count=count;last_environment=args.environment;args.force_once=False;state['status']='waiting_for_more_candidates';save();print('DRAFT_RENDERED',name,flush=True)
  if batch_done and count==current['total_asset_families']:
   state['status']='all_families_assembled_as_draft_quality_review_still_required';save();break
  if batch['status'].startswith('blocked'):
   state['status']='generation_scheduler_blocked_drafts_preserved';save();break
 except json.JSONDecodeError:
  time.sleep(10);continue
 except subprocess.CalledProcessError as exc:
  state.update(status='draft_job_failed_artifacts_preserved',last_error={'returncode':exc.returncode,'command':exc.cmd});save();raise
 time.sleep(60)
else:state['status']='watch_deadline_reached_not_complete';save()
