from pathlib import Path
import bpy,json,numpy as np
ROOT=Path(__file__).resolve().parents[3];source=next(ROOT.glob('2_*'))/'background/map_3d/environment_sources/blender_human_base_meshes/realistic_skull.blend'
with bpy.data.libraries.load(str(source),link=False) as (src,dst):dst.objects=['Skull - Realistic']
o=dst.objects[0];me=o.data;v=np.array([p.co[:] for p in me.vertices]);parent=list(range(len(v)))
def find(x):
 while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
 return x
for edge in me.edges:
 a,b=map(find,edge.vertices);parent[a]=b
groups={}
for i in range(len(v)):groups.setdefault(find(i),[]).append(i)
lo,hi=v.min(0),v.max(0)
for key,ids in sorted(groups.items(),key=lambda kv:-len(kv[1])):
 vv=(v[ids]-lo)/(hi-lo)
 print(json.dumps({'component':key,'vertices':len(ids),'min_normalized':vv.min(0).tolist(),'max_normalized':vv.max(0).tolist(),'center_normalized':vv.mean(0).tolist()}),flush=True)
