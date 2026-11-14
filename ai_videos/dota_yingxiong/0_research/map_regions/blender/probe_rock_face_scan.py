"""Inspect the available rock-face scan's axes before any cliff placement."""
from pathlib import Path
import bpy,json,sys,numpy as np
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';source=OUT/'environment_sources/rock_face_02/rock_face_02_2k.blend';dest=OUT/'rock_face_scan_diagnosis';dest.mkdir(exist_ok=True)
for ob in list(bpy.data.objects):bpy.data.objects.remove(ob,do_unlink=True)
with bpy.data.libraries.load(str(source),link=False) as (src,dst):dst.objects=list(src.objects)
meshes=[o for o in dst.objects if o and o.type=='MESH'];ob=max(meshes,key=lambda o:len(o.data.polygons));bpy.context.scene.collection.objects.link(ob);ob.hide_render=False;ob.hide_viewport=False;bpy.context.view_layer.update();points=np.array([tuple(ob.matrix_world@Vector(v)) for v in ob.bound_box]);lo,hi=points.min(0),points.max(0);center=Vector((lo+hi)/2);span=float(np.max(hi-lo));report={'source':str(source.relative_to(ROOT)),'available_meshes':[{'name':o.name,'faces':len(o.data.polygons)} for o in meshes],'selected':ob.name,'bounds_m':[lo.tolist(),hi.tolist()],'dimensions_m':(hi-lo).tolist(),'transform':list(map(list,ob.matrix_world))};(dest/'probe.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report),flush=True)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=24;scene.render.resolution_x=900;scene.render.resolution_y=900;scene.render.resolution_percentage=100;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.world=bpy.data.worlds.new('Scan_probe_world');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.45,.45,.45,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.6
for name,offset,power,size in [('Key',(-4,-6,7),1400,5),('Rim',(4,2,5),1000,4)]:
 data=bpy.data.lights.new(name,'AREA');data.energy=power;data.shape='DISK';data.size=size;light=bpy.data.objects.new(name,data);scene.collection.objects.link(light);light.location=center+Vector(offset);look_at(light,center)
data=bpy.data.cameras.new('Scan_camera');camera=bpy.data.objects.new('Scan_camera',data);scene.collection.objects.link(camera);scene.camera=camera;data.type='ORTHO';data.ortho_scale=span*1.3
for name,offset in [('front',(0,-2,1)),('side',(2,0,1))]:
 camera.location=center+Vector(offset)*span;look_at(camera,center);scene.render.filepath=str(dest/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
