"""Run two prepared author trials after the exclusive map/environment jobs."""
from pathlib import Path
import time,subprocess
from map_render_slot import map_render_slot,alive
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];OUT=next(ROOT.glob('2_*'))/'background/map_3d';AUDIT=ROOT.parents[1]/'.audit/adhoc_agents/2026-10-27/dota-local-3d-287';deadline=time.monotonic()+3*3600
while alive(31044):
 if time.monotonic()>deadline:raise TimeoutError('Cliff trial still running')
 time.sleep(15)
if not (OUT/'environment_v034_Map_Overview.png').exists():raise RuntimeError('Cliff trial incomplete; inspect before continuing')
for script,logname in [('patch_gateway_measured_holes.py','gateway.r10.author'),('refine_observatory_flat_cast_and_roots.py','observatory.r39.author')]:
 with map_render_slot(OUT,minimum_gib=32):
  with (AUDIT/(logname+'.log')).open('w',encoding='utf-8') as log:subprocess.run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','--factory-startup','--background','--threads','6','--python-exit-code','1','--python',str(HERE/script)],stdout=log,stderr=subprocess.STDOUT,check=True,creationflags=subprocess.CREATE_NO_WINDOW)
 print('AUTHOR_TRIAL_FINISHED',script,flush=True)
