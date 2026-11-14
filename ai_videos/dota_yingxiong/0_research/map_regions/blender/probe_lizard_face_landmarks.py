"""Read actual side-face geometry before adding the absent eye anatomy."""
from pathlib import Path
import bpy,json,sys
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m26_*/model_3d/r09'));bpy.ops.wm.open_mainfile(filepath=str(folder/'authoring.blend'));body=bpy.data.objects['Closed_lizard_surface_3mm'];rows=[]
for sign in [-1,1]:
 for x in [1.65,1.75,1.85,1.95,2.05]:
  for z in [.90,1.0,1.1,1.2]:
   hit,p,n,face=body.ray_cast(Vector((x,sign*3,z)),Vector((0,-sign,0)))
   if hit:rows.append({'side':sign,'xz':[x,z],'point':list(p),'normal':list(n),'face':face})
(folder/'head_side_ray_probe.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');print('SIDE_RAYS_SAVED',flush=True)
scene=bpy.context.scene;scene.camera.location=(1.85,-5,1.1);look_at(scene.camera,(1.85,0,1.1));scene.camera.data.ortho_scale=1.5;scene.cycles.device='CPU';scene.cycles.samples=20;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.render.resolution_x=scene.render.resolution_y=1000;scene.render.filepath=str(folder/'head_side_diagnosis.png');bpy.ops.render.render(write_still=True)
