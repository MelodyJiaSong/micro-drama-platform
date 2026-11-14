"""用 CPU 渲染当前地图底稿，避免抢占本地建模显存。"""
from pathlib import Path
import argparse
import json
import sys
import bpy

DRAMA = Path(__file__).resolve().parents[3]
OUT = next(DRAMA.glob('2_*')) / 'background/map_3d'
parser = argparse.ArgumentParser()
parser.add_argument('--blend', default='foundation_v002.blend')
parser.add_argument('--cameras',default='Map_Overview,Mid_River')
parser.add_argument('--texture-limit',choices=['512','1024','2048'],default='2048')
args = parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
bpy.ops.wm.open_mainfile(filepath=str(OUT / args.blend))
scene = bpy.context.scene
scene.cycles.device = 'CPU'
scene.cycles.samples = 16
scene.cycles.use_denoising = True
scene.render.threads_mode = 'FIXED'
scene.render.threads = 8
scene.render.resolution_x = 1200
scene.render.resolution_y = 900
scene.cycles.debug_use_compact_bvh = True
scene.render.use_simplify = True
scene.cycles.texture_limit_render = args.texture_limit
scene.render.simplify_subdivision_render = 6
# Limit preview texture sampling without changing source pixels or mesh geometry.
overrides={'compact_bvh':True,'texture_limit_render':args.texture_limit,'geometry_simplification':False,'camera_culling':False,'source_blend_unchanged':True,'purpose':'1200x900 map inspection; close asset renders retain original maps'}
for name in args.cameras.split(','):
    scene.camera = bpy.data.objects[name]
    scene.render.filepath = str(OUT / f'{Path(args.blend).stem}_{name}.png')
    bpy.ops.render.render(write_still=True)
    (OUT / f'{Path(args.blend).stem}_{name}_render_settings.json').write_text(json.dumps(overrides,indent=2),encoding='utf-8')
    print('RENDERED', scene.render.filepath, flush=True)
