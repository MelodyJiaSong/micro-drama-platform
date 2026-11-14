from pathlib import Path
import bpy,numpy as np,json,sys
from mathutils import Vector,Matrix
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m16_Ogre/model_3d'));out=folder/'r01/diagnostics';out.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r01/inspection/m16_r01.blend'));body=max((o for o in bpy.data.collections['ASSET_m16'].all_objects if o.type=='MESH'),key=lambda o:len(o.data.polygons));bpy.context.view_layer.update();body.data.transform(body.matrix_world);body.parent=None;body.matrix_world=Matrix.Identity(4)
co=np.empty(len(body.data.vertices)*3,np.float32);body.data.vertices.foreach_get('co',co);co=co.reshape(-1,3);rows=[]
for lo in np.arange(2.2,2.81,.05):
 a=co[(co[:,2]>lo)&(co[:,2]<lo+.05)]
 rows.append({'z':float(lo),'bounds':[a.min(0).tolist(),a.max(0).tolist()],'frontmost_samples':a[np.argsort(a[:,1])[:8]].tolist()})
(out/'face_world_coordinates.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
rays=[]
for z in [2.515,2.530,2.545,2.560,2.575]:
 for x in [-.40,-.38,-.36,-.34,-.32,-.30,-.28]:
  hit,pt,n,index=body.ray_cast(Vector((x,-3,z)),Vector((0,1,0)))
  if hit:rays.append({'x':x,'z':z,'y':pt.y,'normal':list(n)})
(out/'left_tusk_rays.json').write_text(json.dumps(rays,indent=2),encoding='utf-8')
if '--rays-only' in sys.argv:sys.exit(0)
scene=bpy.context.scene;scene.cycles.samples=32;scene.cycles.device='CPU';scene.camera.data.ortho_scale=1.30;scene.camera.location=(0,-4,2.5);look_at(scene.camera,(0,0,2.5));scene.render.filepath=str(out/'face_front.png');bpy.ops.render.render(write_still=True)
