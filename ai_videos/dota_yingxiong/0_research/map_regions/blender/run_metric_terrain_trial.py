"""Wait for whole-map memory slot, then author/render metric terrain trial."""
from pathlib import Path
import subprocess,argparse
from map_render_slot import map_render_slot
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];OUT=next(ROOT.glob('2_*'))/'background/map_3d';AUDIT=ROOT.parents[1]/'.audit/adhoc_agents/2026-10-27/dota-local-3d-287'
parser=argparse.ArgumentParser();parser.add_argument('--revision',default='v032',choices=['v032','v033']);args=parser.parse_args()
with map_render_slot(OUT):
 with (AUDIT/f'environment.{args.revision}.author.log').open('w',encoding='utf-8') as log:subprocess.run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','--factory-startup','--background','--threads','8','--python-exit-code','1','--python',str(HERE/'apply_unified_metric_terrain.py'),'--','--revision',args.revision],stdout=log,stderr=subprocess.STDOUT,check=True,creationflags=subprocess.CREATE_NO_WINDOW)
print('METRIC_TERRAIN_TRIAL_RENDERED',flush=True)
