"""Inspect welded shoulder boundaries and fill only local open skin loops."""
from pathlib import Path
import bpy,bmesh,json,sys,numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m4_Ghoul/model_3d'));out=folder/'r18';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r17/authoring.blend'));coll=bpy.data.collections['ASSET_m4'];ob=next(o for o in coll.objects if o.type=='MESH' and len(o.data.polygons)>100000);me=ob.data
bm=bmesh.new();bm.from_mesh(me);before=len(bm.verts);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.000002);welded=before-len(bm.verts);uv=bm.loops.layers.uv.active
boundaries=[e for e in bm.edges if e.is_boundary];seen=set();records=[];filled=0
for edge in boundaries:
 if edge in seen:continue
 stack=[edge];component=[]
 while stack:
  e=stack.pop()
  if e in seen:continue
  seen.add(e);component.append(e)
  for v in e.verts:stack.extend(x for x in v.link_edges if x.is_boundary and x not in seen)
 verts={v for e in component for v in e.verts};co=np.array([tuple(v.co) for v in verts]);center=co.mean(0);extent=np.ptp(co,axis=0)
 # Restrict to small open loops in either shoulder. Do not cap eyes/mouth,
 # clothing hems, shoulder spike tips or the main scalp boundary.
 closed=all(sum(e in component for e in v.link_edges)==2 for v in verts)
 eligible=closed and len(component)<=180 and center[2]>1.13 and abs(center[0])>.14 and max(extent)<.12
 if not eligible:continue
 uv_values={v:next((l[uv].uv.copy() for l in v.link_loops),None) for v in verts} if uv else {}
 result=bmesh.ops.holes_fill(bm,edges=component,sides=0);faces=result.get('faces',[])
 for f in faces:
  f.material_index=0;f.smooth=True
  if uv:
   for loop in f.loops:
    if uv_values.get(loop.vert) is not None:loop[uv].uv=uv_values[loop.vert]
 filled+=len(faces);records.append({'edges':len(component),'center':center.tolist(),'extent':extent.tolist(),'new_faces':len(faces)})
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.update()
report={'revision':'r18','status':'author_preview_pending','source':'r17','welded_duplicate_vertices':welded,'boundary_edges_before_patch':len(boundaries),'shoulder_loops_filled':records,'filled_faces':filled,'remaining':['Rendered dark creases may be folds or shading rather than open topology','Cloth ends and hair silhouette still need refinement']}
print(json.dumps(report),flush=True);scene=bpy.context.scene;scene.cycles.samples=24;scene.render.resolution_x=900;scene.render.resolution_y=900;scene.camera.data.ortho_scale=.57;scene.camera.location=(0,-2,1.2);look_at(scene.camera,(0,-.38,1.04));bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));(out/'authoring.json').write_text(json.dumps(report,indent=2),encoding='utf-8');scene.render.filepath=str(out/'face_preview.png');bpy.ops.render.render(write_still=True)
