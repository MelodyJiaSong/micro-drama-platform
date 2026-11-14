"""Measure soles against host geometry and expose them above the front railing."""
from pathlib import Path
import bpy,json,numpy as np,sys
from mathutils import Vector,Matrix
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';bpy.ops.wm.open_mainfile(filepath=str(OUT/'side_shop_merchant_fit_v001.blend'));unit=bpy.data.objects['m309_on_right_shop_platform'];host=bpy.data.objects['geometry_0'];inverse=host.matrix_world.inverted();points=[]
for ob in unit.instance_collection.all_objects:
 if ob.type!='MESH' or ob.hide_render:continue
 co=np.empty(len(ob.data.vertices)*3,np.float32);ob.data.vertices.foreach_get('co',co);co=co.reshape(-1,3);mat=np.array(unit.matrix_world@Matrix.Translation(-unit.instance_collection.instance_offset)@ob.matrix_world);world=co@mat[:3,:3].T+mat[:3,3];points.append(world)
world=np.concatenate(points);low=world[world[:,2]<world[:,2].min()+.015];indices=np.unique(np.round(low[:,:2]/.01),axis=0,return_index=True)[1];samples=[]
for point in low[indices]:
 origin=Vector(point)+Vector((0,0,.12));hit,p,n,face=host.ray_cast(inverse@origin,inverse.to_3x3()@Vector((0,0,-1)))
 if hit:samples.append({'sole':point.tolist(),'floor':list(host.matrix_world@p),'vertical_clearance_m':float(point[2]-(host.matrix_world@p).z)})
report={'status':'measured_contact_author_view_pending','samples':samples,'clearance_range_m':[min(s['vertical_clearance_m'] for s in samples),max(s['vertical_clearance_m'] for s in samples)],'local_anchor':list(unit.location),'source_blend':'side_shop_merchant_fit_v001.blend','warning':'Lowest 15mm of sole vertices sampled; not full body collision audit'};(OUT/'side_shop_merchant_contact_probe.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k!='samples'}),flush=True)
scene=bpy.context.scene;scene.camera.location=(1.5,-5,7);look_at(scene.camera,(1.5,-1,3.1));scene.camera.data.ortho_scale=1.9;scene.cycles.device='CPU';scene.cycles.samples=24;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.render.filepath=str(OUT/'side_shop_merchant_fit_v001_feet.png');bpy.ops.render.render(write_still=True)
