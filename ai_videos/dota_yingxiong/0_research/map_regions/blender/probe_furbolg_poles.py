"""Read-only connected tip measurements for the authored Furbolg roof poles."""
from pathlib import Path
import bpy,numpy as np,json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m21_Polar_Furbolg/model_3d'));out=folder/'r03'
bpy.ops.wm.open_mainfile(filepath=str(out/'authoring.blend'));body=max((o for o in bpy.data.collections['ASSET_m21'].objects if o.type=='MESH'),key=lambda o:len(o.data.polygons));me=body.data
co=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',co);co=co.reshape(-1,3);edges=np.empty(len(me.edges)*2,np.int32);me.edges.foreach_get('vertices',edges);edges=edges.reshape(-1,2)
results={}
for cut in [1.96,2.02,2.08,2.14]:
 selected=co[:,2]>cut;part=edges[selected[edges].all(axis=1)];parent={int(i):int(i) for i in np.flatnonzero(selected)}
 def root(i):
  while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
  return i
 for a,b in part:
  a,b=root(int(a)),root(int(b))
  if a!=b:parent[a]=b
 groups={}
 for i in parent:groups.setdefault(root(i),[]).append(i)
 rows=[]
 for members in groups.values():
  if len(members)<40:continue
  points=co[members];rows.append({'vertices':len(members),'min':points.min(axis=0).tolist(),'max':points.max(axis=0).tolist(),'centre':points.mean(axis=0).tolist()})
 results[str(cut)]=sorted(rows,key=lambda x:-x['vertices'])[:12]
(out/'pole_components.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(json.dumps(results),flush=True)
scene=bpy.context.scene;scene.cycles.samples=24;scene.cycles.device='CPU';scene.render.threads_mode='FIXED';scene.render.threads=6;scene.camera.location=(3,4,3.2);scene.camera.data.ortho_scale=1.5;look_at(scene.camera,(0,.1,1.8));scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene.render.filepath=str(out/'roof_poles_probe.png');bpy.ops.render.render(write_still=True)
