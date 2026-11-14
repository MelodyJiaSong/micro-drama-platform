"""Unobstructed diagnostic camera; retain all camp/environment geometry."""
from pathlib import Path
import bpy,json,sys
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'camp_K8_RAO_v001.blend'))
units=[o for o in bpy.data.collections['10_Neutral_Camps'].objects if o.get('camp')=='K8'];assert len(units)==3
center=sum((o.location for o in units),Vector())/3;scene=bpy.context.scene;camera=scene.camera
camera.location=center+Vector((0,-1,26));look_at(camera,center);camera.data.type='ORTHO';camera.data.ortho_scale=17
scene.cycles.device='CPU';scene.cycles.samples=24;scene.cycles.use_denoising=True;scene.cycles.debug_use_compact_bvh=True;scene.render.use_simplify=True;scene.cycles.texture_limit_render='2048';scene.render.threads_mode='FIXED';scene.render.threads=6;scene.render.resolution_x=1200;scene.render.resolution_y=1000
scene.render.filepath=str(OUT/'camp_K8_RAO_v001_overhead.png');bpy.ops.render.render(write_still=True)
(OUT/'camp_K8_RAO_v001_camera_check.json').write_text(json.dumps({'status':'author_view_pending','geometry_changed':False,'original_view':'Rejected for tree occlusion; not evidence of visual placement acceptance','camera':list(camera.location),'units':[{'name':o.name,'rawcode':o.get('rawcode'),'position':list(o.location),'scale':list(o.scale)} for o in units]},indent=2),encoding='utf-8')
print('OVERHEAD_SAVED',flush=True)
