"""Serialize the prepared outer boundary correction with existing map jobs."""
from pathlib import Path
import subprocess
from map_render_slot import map_render_slot
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];OUT=next(ROOT.glob('2_*'))/'background/map_3d';AUDIT=ROOT.parents[1]/'.audit/adhoc_agents/2026-10-27/dota-local-3d-287'
with map_render_slot(OUT,minimum_gib=64):
 with (AUDIT/'environment.v035.author.log').open('w',encoding='utf-8') as log:subprocess.run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','--factory-startup','--background','--threads','8','--python-exit-code','1','--python',str(HERE/'synchronize_outer_land_boundary.py'),'--','--source','v033'],stdout=log,stderr=subprocess.STDOUT,check=True,creationflags=subprocess.CREATE_NO_WINDOW)
print('OUTER_BOUNDARY_TRIAL_RENDERED',flush=True)
