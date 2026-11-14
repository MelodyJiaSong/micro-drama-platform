"""Read-only sampled geometry-to-terrain contact check for instanced rocks."""
from pathlib import Path
import bpy,json,numpy as np
from mathutils import Matrix
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v026.blend'));me=bpy.data.objects['Terrain_683d'].data;co=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',co);z=co.reshape(1025,1025,3)[:,:,2]
def height(x,y):
 u,v=np.clip((x+409.6)/.8,0,1023.999),np.clip((y+409.6)/.8,0,1023.999);i,j=u.astype(int),v.astype(int);a,b=u-i,v-j;return (z[j,i]*(1-a)+z[j,i+1]*a)*(1-b)+(z[j+1,i]*(1-a)+z[j+1,i+1]*a)*b
cache={};rows=[];checked=0
for cname in ['07_Cliff_Relief','09_Ground_Stones','17_River_bank_detail']:
 for ob in bpy.data.collections[cname].objects:
  if ob.hide_render or ob.instance_type!='COLLECTION' or not ob.instance_collection:continue
  lib=ob.instance_collection
  if lib.name not in cache:
   points=[]
   for src in lib.all_objects:
    if src.hide_render or src.type!='MESH':continue
    p=np.empty(len(src.data.vertices)*3,np.float32);src.data.vertices.foreach_get('co',p);p=p.reshape(-1,3);p=p[::max(1,len(p)//1536)];m=np.array(src.matrix_world);points.append(p@m[:3,:3].T+m[:3,3]-np.array(lib.instance_offset))
   cache[lib.name]=np.concatenate(points) if points else np.zeros((0,3))
  p=cache[lib.name]
  if not len(p):continue
  m=np.array(ob.matrix_world);p=p@m[:3,:3].T+m[:3,3];gap=float(np.min(p[:,2]-height(p[:,0],p[:,1])));checked+=1
  if gap>.025:rows.append({'object':ob.name,'collection':cname,'prototype':lib.name,'location':list(ob.location),'minimum_sampled_gap_m':gap})
rows.sort(key=lambda r:-r['minimum_sampled_gap_m']);report={'status':'sampled_geometry_diagnosis_not_full_collision_proof','environment':'environment_v026.blend','checked_instances':checked,'floating_candidates':rows,'sampling':'Every mesh in each instance prototype, at most approximately 1536 evenly indexed vertices per mesh; compare to bilinear 0.8m terrain heights','warning':'Sampling can overestimate a small gap; inspect large gaps before moving. Cliff rocks intentionally buried are not changed.'};(OUT/'rock_contact_probe_v026.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps({'checked':checked,'floating_candidates':len(rows),'largest':rows[:15]}),flush=True)
