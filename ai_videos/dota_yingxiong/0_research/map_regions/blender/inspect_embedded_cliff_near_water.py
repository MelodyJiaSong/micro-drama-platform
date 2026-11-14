"""Inspect the closest local rock patch from the existing river camera side."""
from pathlib import Path
import bpy,json,numpy as np,sys
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v038.blend'))
scene=bpy.context.scene;camera=bpy.data.objects['River_Eye_Level'];original=camera.location.copy()
report=json.loads((OUT/'environment_v038_report.json').read_text())
rows=sorted(report['patches'],key=lambda r:(Vector((*r['anchor'],original.z))-original).length)
evidence=[]
for index,row in enumerate(rows[:2]):
    ob=bpy.data.objects[row['object']]
    target=Vector((*row['anchor'],sum(row['z_range'])/2))
    toward=Vector((original.x-target.x,original.y-target.y,0)).normalized()
    camera.location=target+toward*16+Vector((0,0,3))
    look_at(camera,target);camera.data.type='PERSP';camera.data.lens=42
    scene.camera=camera;scene.cycles.device='CPU';scene.cycles.samples=24;scene.cycles.use_denoising=True
    scene.render.threads_mode='FIXED';scene.render.threads=6;scene.render.resolution_x=1200;scene.render.resolution_y=900
    scene.render.use_border=False;scene.render.use_crop_to_border=False;scene.render.use_simplify=True;scene.cycles.texture_limit_render='2048'
    path=OUT/f'environment_v038_Rock_River_Close_{index+1}.png';scene.render.filepath=str(path)
    bpy.ops.render.render(write_still=True)
    evidence.append({'image':path.name,'object':ob.name,'target':list(target),'camera':list(camera.location),'scene_geometry_visibility_unchanged':True})
(OUT/'environment_v038_close_cameras.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
