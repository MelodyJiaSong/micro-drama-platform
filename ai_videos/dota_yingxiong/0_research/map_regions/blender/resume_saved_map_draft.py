"""Resume a saved draft's inspection in isolated camera processes after OOM."""
from pathlib import Path
import argparse,json,subprocess,sys,datetime
from map_render_slot import map_render_slot
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];OUT=next(ROOT.glob('2_*'))/'background/map_3d';BLENDER='C:/Program Files/Blender Foundation/Blender 5.2/blender.exe'
p=argparse.ArgumentParser();p.add_argument('--blend',required=True);p.add_argument('--environment',required=True);p.add_argument('--minimum-gib',type=float,default=88);p.add_argument('--texture-limit',choices=['512','1024','2048'],default='2048');args=p.parse_args();assert Path(args.blend).name==args.blend;stem=Path(args.blend).stem;report=json.loads((OUT/(stem+'_report.json')).read_text(encoding='utf-8'));statefile=OUT/'draft_refresh_state.json'
def update(**values):
 state=json.loads(statefile.read_text(encoding='utf-8'));assert state.get('active_file')==args.blend,state.get('active_file');state.update(values);statefile.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8');return state
update(status='waiting_to_resume_saved_draft',resume_settings={'minimum_free_gib':args.minimum_gib,'texture_limit':args.texture_limit,'isolated_camera_processes':True})
for camera in ['Map_Overview','Sentinel_Forest_Eye']:
 if (OUT/f'{stem}_{camera}.png').exists():continue
 with map_render_slot(OUT,minimum_gib=args.minimum_gib):
  update(status='rendering_draft',resume_camera=camera)
  with (OUT/f'{stem}_retry01_{camera}.log').open('w',encoding='utf-8') as log:
   result=subprocess.run([BLENDER,'--factory-startup','--background','--threads','8','--python-exit-code','1','--python',str(HERE/'render_map_check.py'),'--','--blend',args.blend,'--cameras',camera,'--texture-limit',args.texture_limit],stdout=log,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
  if result.returncode:update(status='saved_draft_render_failed',failed_camera=camera,returncode=result.returncode);raise RuntimeError(f'{camera} render failed')
state=update(status='all_families_assembled_as_draft_quality_review_still_required',active_environment=args.environment)
if not any(d['file']==args.blend for d in state['drafts']):state['drafts'].append({'file':args.blend,'families':report['asset_library_count'],'environment':args.environment,'at':datetime.datetime.now().astimezone().isoformat(),'acceptance':'DRAFT_NOT_RELEASED','recovery':'Preserved saved assembly; cameras rendered in isolated processes after initial OOM'})
statefile.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8');subprocess.run([sys.executable,'-X','utf8',str(HERE/'audit_map_asset_coverage.py'),'--blend',args.blend],check=True);print('SAVED_DRAFT_INSPECTION_RECOVERED',args.blend,flush=True)
