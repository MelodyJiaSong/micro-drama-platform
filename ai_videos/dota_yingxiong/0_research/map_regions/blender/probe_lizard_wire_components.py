"""Read-only colour-connected wire diagnosis; never delete ivory dorsal plates."""
from pathlib import Path
import bpy,numpy as np,json,sys
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m26_Thunder_Lizard/model_3d'))
bpy.ops.wm.open_mainfile(filepath=str(folder/'r04/authoring.blend'));scene=bpy.context.scene
ob=max((o for o in bpy.data.collections['ASSET_m26'].all_objects if not o.hide_render and o.type=='MESH'),key=lambda o:len(o.data.polygons));me=ob.data
co=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',co);co=co.reshape(-1,3);matrix=np.array(ob.matrix_world);world=co@matrix[:3,:3].T+matrix[:3,3]
indices=np.empty(len(me.loops),np.int32);me.loops.foreach_get('vertex_index',indices);starts=np.empty(len(me.polygons),np.int32);counts=np.empty(len(me.polygons),np.int32);me.polygons.foreach_get('loop_start',starts);me.polygons.foreach_get('loop_total',counts);pos=np.add.reduceat(world[indices],starts)/counts[:,None]
uv=np.empty(len(me.loops)*2,np.float32);me.uv_layers.active.data.foreach_get('uv',uv);uv=np.add.reduceat(uv.reshape(-1,2),starts)/counts[:,None];im=bpy.data.images['Image_0'];pix=np.empty(len(im.pixels),np.float32);im.pixels.foreach_get(pix);pix=pix.reshape(im.size[1],im.size[0],4);ij=np.mod(np.floor(uv*np.array(im.size)).astype(int),np.array(im.size));rgb=pix[ij[:,1],ij[:,0],:3]
region=(pos[:,0]<1.3)&(pos[:,0]>-1.8)&(np.abs(pos[:,1])<.7)&(pos[:,2]>1.1)
mask=region&(rgb.max(axis=1)>.38)&(rgb.min(axis=1)>rgb.max(axis=1)*.72)
selected=np.flatnonzero(mask);parents={int(i):int(i) for i in selected};owners={}
def find(i):
 while parents[i]!=i:parents[i]=parents[parents[i]];i=parents[i]
 return i
for i in selected:
 i=int(i)
 for v in indices[starts[i]:starts[i]+counts[i]]:
  v=int(v)
  if v in owners:parents[find(i)]=find(owners[v])
  else:owners[v]=i
groups={}
for i in selected:groups.setdefault(find(int(i)),[]).append(int(i))
camera=scene.camera;camera.location=(1,-4,4);look_at(camera,(.1,0,1.8));camera.data.ortho_scale=2.3;scene.render.resolution_x=scene.render.resolution_y=960;bpy.context.view_layer.update()
frame=camera.data.view_frame(scene=scene);left,right=min(v.x for v in frame),max(v.x for v in frame);bottom,top=min(v.y for v in frame),max(v.y for v in frame);direction=camera.matrix_world.to_quaternion()@Vector((0,0,-1));inv=ob.matrix_world.inverted();hits=[]
for x,y in [(309,585),(324,604),(485,478),(496,466),(749,340),(772,349),(764,362),(904,551),(906,567),(618,409),(664,407)]:
 origin=camera.matrix_world@Vector((left+(right-left)*(x+.5)/960,top-(top-bottom)*(y+.5)/960,0));hit,p,n,index=ob.ray_cast(inv@origin,(inv.to_3x3()@direction).normalized())
 if hit:hits.append({'pixel':[x,y],'face':index,'point':list(ob.matrix_world@p),'rgb':rgb[index].tolist(),'group':find(index) if index in parents else None})
rows=[];face_groups={}
for key,ids in groups.items():
 if len(ids)<5:continue
 pp=pos[ids];rows.append({'id':key,'faces':len(ids),'bounds':[pp.min(axis=0).tolist(),pp.max(axis=0).tolist()],'centre':pp.mean(axis=0).tolist(),'rgb':np.median(rgb[ids],axis=0).tolist(),'seed_pixels':[h['pixel'] for h in hits if h['group']==key]});face_groups[str(key)]=ids
rows.sort(key=lambda r:(not bool(r['seed_pixels']),-r['faces']))
(folder/'wire_component_probe_r04.json').write_text(json.dumps({'asset_object':ob.name,'candidate_faces':len(selected),'groups':rows,'hits':hits},indent=2),encoding='utf-8')
(folder/'wire_component_faces_r04.json').write_text(json.dumps(face_groups),encoding='utf-8')
print(json.dumps({'hits':hits,'seeded_groups':[r for r in rows if r['seed_pixels']],'largest_other_groups':rows[:10]}),flush=True)
