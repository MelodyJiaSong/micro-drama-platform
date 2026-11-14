"""Inspect physical connected pieces in exactly the instances hit by the river-view probe."""
from pathlib import Path
import bpy,bmesh,json,numpy as np
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v026.blend'))
me=bpy.data.objects['Terrain_683d'].data;co=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',co);z=co.reshape(1025,1025,3)[:,:,2]
def height(x,y):
 u,v=np.clip((x+409.6)/.8,0,1023.999),np.clip((y+409.6)/.8,0,1023.999);i,j=u.astype(int),v.astype(int);a,b=u-i,v-j;return (z[j,i]*(1-a)+z[j,i+1]*a)*(1-b)+(z[j+1,i]*(1-a)+z[j+1,i+1]*a)*b
hits=json.loads((OUT/'river_visible_detail_probe.json').read_text());unique={}
for h in hits:unique.setdefault((h['object'],json.dumps(h['matrix'])),h)
cache={};rows=[]
for h in unique.values():
 name=h['object'];ob=bpy.data.objects[name]
 if name not in cache:
  bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.00001);bm.verts.ensure_lookup_table();seen=set();parts=[]
  for v in bm.verts:
   if v.index in seen:continue
   stack=[v];seen.add(v.index);part=[]
   while stack:
    q=stack.pop();part.append(tuple(q.co))
    for e in q.link_edges:
     n=e.other_vert(q)
     if n.index not in seen:seen.add(n.index);stack.append(n)
   parts.append(np.array(part))
  cache[name]=parts;bm.free()
 m=np.array(h['matrix']);components=[]
 for idx,p in enumerate(cache[name]):
  p=p@m[:3,:3].T+m[:3,3];gap=p[:,2]-height(p[:,0],p[:,1]);components.append({'component':idx,'vertices':len(p),'min_gap_m':float(gap.min()),'max_gap_m':float(gap.max()),'dimensions_m':np.ptp(p,axis=0).tolist(),'minimum_xyz':p.min(axis=0).tolist()})
 rows.append({'object':name,'pixel':h['pixel'],'matrix':h['matrix'],'components':sorted(components,key=lambda r:-r['vertices'])})
(OUT/'visible_rock_component_probe_v026.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');print(json.dumps(rows),flush=True)
