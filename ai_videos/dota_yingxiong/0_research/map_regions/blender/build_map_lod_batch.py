"""Bounded local Blender worker queue for separate, resumable map LOD libraries."""
from pathlib import Path
import concurrent.futures,subprocess,sys,json,datetime,threading,time,argparse,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];OUT=next(ROOT.glob('2_*'))/'background/map_3d';AUDIT=ROOT.parents[1]/'.audit/adhoc_agents/2026-10-27/dota-local-3d-287';BLENDER='C:/Program Files/Blender Foundation/Blender 5.2/blender.exe'
from map_render_slot import memory_headroom
p=argparse.ArgumentParser();p.add_argument('--version',default='overview_v004');p.add_argument('--workers',type=int,choices=[1,2],default=2);args=p.parse_args();folder=OUT/'lod_libraries'/args.version;folder.mkdir(parents=True,exist_ok=True);trial=json.loads((folder/'m304/comparison_author_check.json').read_text())
if trial.get('status')!='usable_for_map_preview' or not trial.get('coincident_weld') or not trial.get('boundary_protection'):raise ValueError('The boundary-protected decimation trial has not passed its map-preview visual comparison')
statepath=folder/'batch_state.json';source=json.loads((OUT/'assembly_working_v022_report.json').read_text(encoding='utf-8'));lock=threading.Lock();state={'started':datetime.datetime.now().astimezone().isoformat(),'status':'building_map_preview_libraries_not_quality_acceptance','source_map':'assembly_working_v022.blend','workers':args.workers,'assets':{}}
def update(aid,value):
 with lock:
  state['assets'][aid]=value;state['updated']=datetime.datetime.now().astimezone().isoformat();statepath.write_text(json.dumps(state,indent=2),encoding='utf-8')

def bounded_run(command,log):
 child=subprocess.Popen(command,stdout=log,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
 deadline=time.monotonic()+20*60
 while child.poll() is None:
  if time.monotonic()>deadline or memory_headroom()['commit']<6*1024**3:
   child.terminate();child.wait();return 124
  time.sleep(2)
 return child.returncode
def work(aid):
 target=folder/aid;report=target/'lod_report.json'
 if report.exists() and (target/(aid+'.blend')).exists():
  old=json.loads(report.read_text());original=ROOT/source['source_libraries'][aid]
  if hashlib.sha256(original.read_bytes()).hexdigest()!=old['source_sha256'] or hashlib.sha256((target/(aid+'.blend')).read_bytes()).hexdigest()!=old['output_sha256']:
   update(aid,{'status':'existing_candidate_hash_mismatch'});return False
  update(aid,{'status':'existing_candidate','faces':old['visible_unique_faces_after']});return True
 if (target/(aid+'.blend')).exists():update(aid,{'status':'incomplete_output_requires_inspection'});return False
 budget=250000 if aid.startswith('bg') else 120000
 threshold=14 if args.workers==1 else 24
 deadline=time.monotonic()+120
 while min(memory_headroom().values())<threshold*1024**3:
  if time.monotonic()>deadline:
   update(aid,{'status':'skipped_memory_timeout','retry_later':True});return False
  update(aid,{'status':'waiting_memory','required_physical_and_commit_gib':threshold});time.sleep(5)
 update(aid,{'status':'running','face_budget':budget})
 with (AUDIT/f'{aid}.lod.{args.version}.batch.log').open('w',encoding='utf-8') as log:
  result=bounded_run([BLENDER,'--factory-startup','--background','--threads','4','--python-exit-code','1','--python',str(HERE/'build_map_lod_library.py'),'--','--asset',aid,'--face-budget',str(budget),'--version',args.version,'--weld','--protect-boundaries'],log)
 if result or not report.exists():update(aid,{'status':'skipped_timeout_or_memory' if result==124 else 'failed','returncode':result});return False
 old=json.loads(report.read_text())
 if old['changes']:
  update(aid,{'status':'rendering_before_after_comparison','faces_after':old['visible_unique_faces_after']})
  with (AUDIT/f'{aid}.lod.{args.version}.comparison.log').open('w',encoding='utf-8') as log:
   check=bounded_run([BLENDER,'--factory-startup','--background','--threads','4','--python-exit-code','1','--python',str(HERE/'compare_map_lod.py'),'--','--asset',aid,'--version',args.version],log)
  if check:update(aid,{'status':'comparison_skipped_timeout_or_memory' if check==124 else 'comparison_render_failed','returncode':check});return False
 update(aid,{'status':'candidate_pending_visual_check' if old['changes'] else 'geometry_unchanged','faces_before':old['visible_unique_faces_before'],'faces_after':old['visible_unique_faces_after']});print('LOD_READY',aid,old['visible_unique_faces_after'],flush=True);return True
with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
 results=list(pool.map(work,source['source_libraries']))
state['status']='all_preview_libraries_generated_pending_validation' if all(results) else 'some_libraries_failed';state['finished']=datetime.datetime.now().astimezone().isoformat();statepath.write_text(json.dumps(state,indent=2),encoding='utf-8');print(state['status'],flush=True)
