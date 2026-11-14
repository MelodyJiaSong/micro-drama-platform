"""Let the pending map previews finish before starting the next large trial."""
from pathlib import Path
import json,time,subprocess
from map_render_slot import map_render_slot
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];OUT=next(ROOT.glob('2_*'))/'background/map_3d';AUDIT=ROOT.parents[1]/'.audit/adhoc_agents/2026-10-27/dota-local-3d-287';deadline=time.monotonic()+3*3600
while time.monotonic()<deadline:
 state=json.loads((OUT/'draft_refresh_state.json').read_text(encoding='utf-8'))
 if state.get('active_file')!='assembly_working_v021.blend':raise RuntimeError('Map job changed; do not compete with another job')
 if state['status']=='all_families_assembled_as_draft_quality_review_still_required':break
 if 'failed' in state['status']:raise RuntimeError('Map render failed; preserve memory for diagnosis')
 time.sleep(15)
else:raise TimeoutError('Map previews still pending')
with map_render_slot(OUT,minimum_gib=64):
 with (AUDIT/'environment.v034.author.log').open('w',encoding='utf-8') as log:subprocess.run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','--factory-startup','--background','--threads','8','--python-exit-code','1','--python',str(HERE/'apply_cliff_surface_relief.py')],stdout=log,stderr=subprocess.STDOUT,check=True,creationflags=subprocess.CREATE_NO_WINDOW)
print('CLIFF_RELIEF_TRIAL_RENDERED',flush=True)
