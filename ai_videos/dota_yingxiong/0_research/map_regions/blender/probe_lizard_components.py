"""Read-only seam-aware component diagnosis in the correctly scaled lizard."""
from pathlib import Path
import bpy,bmesh,json,numpy as np
from mathutils import Matrix
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m26_Thunder_Lizard/model_3d'))
bpy.ops.wm.open_mainfile(filepath=str(folder/'r01/inspection/m26_r01.blend'));ob=next(o for o in bpy.data.collections['ASSET_m26'].objects if o.type=='MESH');bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.000001);bm.verts.ensure_lookup_table();bm.verts.index_update()
factor=5/ob.dimensions.x;mat=np.array(Matrix.Scale(factor,4)@ob.matrix_world);seen=set();rows=[]
for v in bm.verts:
 if v.index in seen:continue
 stack=[v];seen.add(v.index);part=[]
 while stack:
  q=stack.pop();part.append(tuple(q.co))
  for e in q.link_edges:
   n=e.other_vert(q)
   if n.index not in seen:seen.add(n.index);stack.append(n)
 p=np.array(part);p=p@mat[:3,:3].T+mat[:3,3];rows.append({'vertices':len(p),'min':p.min(axis=0).tolist(),'max':p.max(axis=0).tolist(),'center':p.mean(axis=0).tolist(),'dimensions':np.ptp(p,axis=0).tolist()})
bm.free();rows.sort(key=lambda r:-r['vertices']);(folder/'components_at_5m.json').write_text(json.dumps({'components':rows,'scale_correction':factor},indent=2),encoding='utf-8');print(json.dumps({'count':len(rows),'largest':rows[:30]}),flush=True)
