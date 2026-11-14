"""Resume a guarded map preview after the LOD worker queue completes successfully."""
from pathlib import Path
import sys,json,time,subprocess,datetime
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];OUT=next(ROOT.glob('2_*'))/'background/map_3d';BLENDER='C:/Program Files/Blender Foundation/Blender 5.2/blender.exe'
from map_render_slot import map_render_slot,memory_headroom
VERSION='overview_v004';NAME='assembly_working_v022_lod_v004.blend';statefile=OUT/'lod_libraries'/VERSION/'map_preview_state.json';batchfile=statefile.parent/'batch_state.json';state={'status':'waiting_for_lod_batch','map':NAME,'lod_version':VERSION,'quality':'DRAFT_PREVIEW_NOT_ACCEPTED'}
def update(status,**kwargs):
 state.update(status=status,at=datetime.datetime.now().astimezone().isoformat(),**kwargs);statefile.write_text(json.dumps(state,indent=2),encoding='utf-8');print(status,flush=True)
def run(script,args,logname,minimum=40):
 with map_render_slot(OUT,minimum_gib=minimum,timeout=120), (OUT/logname).open('w',encoding='utf-8') as log:
  child=subprocess.Popen([BLENDER,'--factory-startup','--background','--threads','8','--python-exit-code','1','--python',str(HERE/script),'--']+args,stdout=log,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
  update('running_'+script,child_pid=child.pid)
  deadline=time.monotonic()+20*60
  while child.poll() is None:
   if time.monotonic()>deadline:
    child.terminate();child.wait();raise TimeoutError('Owned map step exceeded 20 minutes; preserve outputs and skip')
   if memory_headroom()['commit']<6*1024**3:
    child.terminate();child.wait();raise RuntimeError('Stopped this owned Blender worker because available commit fell below 6 GiB')
   time.sleep(3)
  if child.returncode:raise subprocess.CalledProcessError(child.returncode,script)
update('waiting_for_lod_batch');deadline=time.monotonic()+120
try:
 while time.monotonic()<deadline:
  try:batch=json.loads(batchfile.read_text(encoding='utf-8'))
  except (FileNotFoundError,json.JSONDecodeError):time.sleep(20);continue
  if batch['status']=='some_libraries_failed':raise RuntimeError('LOD batch contains failed/incomplete outputs; map not remapped')
  if batch['status']=='all_preview_libraries_generated_pending_validation':break
  time.sleep(20)
 else:raise TimeoutError('LOD batch not ready within watcher window')
 if not (OUT/NAME).exists():run('save_map_with_lod_libraries.py',['--version',VERSION,'--output',NAME],Path(NAME).stem+'_save.log')
 if not (OUT/(Path(NAME).stem+'_report.json')).exists():raise RuntimeError('Saved map exists without its remapping report')
 run('profile_saved_map_geometry.py',['--blend',NAME],Path(NAME).stem+'_profile.log',minimum=32)
 inventory=json.loads((OUT/(Path(NAME).stem+'_resource_inventory.json')).read_text());report=json.loads((OUT/(Path(NAME).stem+'_report.json')).read_text());actual={str(Path(r['library']).resolve()).casefold() for r in inventory['meshes'] if r['library']};expected={str((ROOT/relative).resolve()).casefold() for relative in report['source_libraries'].values()}
 if not actual.issubset(expected):raise RuntimeError('Reloaded map still contains unexpected high-resolution asset libraries')
 update('lod_reopened_and_inventoried',unique_faces=inventory['total_unique_faces'],base_buffer_estimate_gib=inventory['estimated_base_buffers_gib'])
 for camera in ['Map_Overview','Sentinel_Forest_Eye']:
  try:
   if not (OUT/(Path(NAME).stem+'_'+camera+'.png')).exists():run('render_map_check.py',['--blend',NAME,'--cameras',camera,'--texture-limit','1024'],Path(NAME).stem+'_'+camera+'_render.log')
  except (TimeoutError,subprocess.CalledProcessError) as exc:
   state.setdefault('skipped_steps',[]).append({'camera':camera,'reason':str(exc)})
   update('camera_skipped_continuing')
 subprocess.run([sys.executable,'-X','utf8',str(HERE/'audit_map_asset_coverage.py'),'--blend',NAME],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
 update('partial_preview_with_skipped_steps' if state.get('skipped_steps') else 'preview_images_ready_for_author_and_independent_review',child_pid=None)
except Exception as exc:
 update('stopped_with_artifacts_preserved',error=str(exc));raise
