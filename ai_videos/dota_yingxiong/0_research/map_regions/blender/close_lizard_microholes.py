"""Cap only small simple boundary loops, preserving the creature's detailed surface."""
from pathlib import Path
import bpy,bmesh,json,sys,numpy as np,argparse
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
parser=argparse.ArgumentParser();parser.add_argument('--revision',default='r03');parser.add_argument('--source',default='r02');parser.add_argument('--cap-uv-seams',action='store_true');args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []);assert args.revision in ['r03','r04'];assert args.source in ['r02','r03']
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m26_Thunder_Lizard/model_3d'));out=folder/args.revision;out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/args.source/'authoring.blend'));coll=bpy.data.collections['ASSET_m26'];ob=next(o for o in coll.objects if o.type=='MESH' and not o.hide_render)
if args.source=='r02':
 source=ob.copy();source.data=ob.data.copy();coll.objects.link(source);source.name='Archive_lizard_before_hole_caps';source.hide_render=True;source.hide_viewport=True
bm=bmesh.new();bm.from_mesh(ob.data);edges=set(e for e in bm.edges if e.is_boundary);before=len(edges);groups=[]
while edges:
 first=edges.pop();stack=[first];part=[first]
 while stack:
  edge=stack.pop()
  for v in edge.verts:
   for neighbor in v.link_edges:
    if neighbor in edges:edges.remove(neighbor);stack.append(neighbor);part.append(neighbor)
 groups.append(part)
print('BOUNDARY_COMPONENTS',len(groups),before,flush=True)
filled=[];selected_groups=[]
for part in groups:
 if len(part)>128:continue
 vertices={v for e in part for v in e.verts};points=np.array([tuple(ob.matrix_world@v.co) for v in vertices]);dimensions=np.ptp(points,axis=0)
 if max(dimensions)>.045:continue
 degree={v:0 for v in vertices}
 for e in part:
  for v in e.verts:degree[v]+=1
 if any(n!=2 for n in degree.values()):continue
 selected_groups.append((part,dimensions))
print('SELECTED_LOCAL_CAPS',len(selected_groups),flush=True)
# Blender's generic fill operator stalled on thousands of tiny loops. These
# already-validated degree-two boundaries can be capped locally without a
# global fill/nearest-surface transfer over the 2.8M-face body.
newfaces=[];uvlayer=bm.loops.layers.uv.active;skipped_uv=0;projected_uv=0
for part,dimensions in selected_groups:
 edge=part[0];start=edge.verts[0];current=start;order=[];used=set();texcoords=[];normals=[];edge_uvs=[]
 while edge not in used:
  used.add(edge);order.append(current);face=edge.link_faces[0];loop=next(q for q in face.loops if q.vert==current);texcoords.append(loop[uvlayer].uv.copy());normals.append(face.normal.copy());nextv=edge.other_vert(current);edge_uvs.append((loop[uvlayer].uv.copy(),next(q[uvlayer].uv.copy() for q in face.loops if q.vert==nextv),sum((q[uvlayer].uv for q in face.loops),Vector((0,0)))/len(face.loops)));candidates=[q for q in nextv.link_edges if q in part and q!=edge]
  current=nextv
  if current==start:break
  edge=candidates[0]
 if current!=start or len(order)!=len(part) or len(order)<3:continue
 uvs=np.array([tuple(q) for q in texcoords])
 seam=np.max(np.ptp(uvs,axis=0))>.12
 if seam and not args.cap_uv_seams:skipped_uv+=1;continue
 if seam:projected_uv+=1
 centre=bm.verts.new(sum((v.co for v in order),Vector())/len(order));centre_uv=sum(texcoords,Vector((0,0)))/len(order);normal=sum(normals,Vector()).normalized()
 for j,a in enumerate(order):
  k=(j+1)%len(order);b=order[k];sequence=[centre,a,b] if (a.co-centre.co).cross(b.co-centre.co).dot(normal)>=0 else [centre,b,a];face=bm.faces.new(sequence);face.smooth=True;face.material_index=part[0].link_faces[0].material_index
  ua,ub,uc=edge_uvs[j];local_mid=(ua+ub)*.5;local_center=local_mid+(uc-local_mid)*.10
  for loop in face.loops:
   if seam:loop[uvlayer].uv=local_center if loop.vert==centre else ua if loop.vert==a else ub
   else:loop[uvlayer].uv=centre_uv if loop.vert==centre else texcoords[j] if loop.vert==a else texcoords[k]
  newfaces.append(face)
 filled.append({'boundary_edges':len(part),'dimensions_m':dimensions.tolist()})
print('LOCAL_TRIANGLE_CAPS_CREATED',len(filled),'UV_SEAMS_SKIPPED',skipped_uv,flush=True)
bm.normal_update();after=sum(e.is_boundary for e in bm.edges);bm.to_mesh(ob.data);bm.free();ob.data.update();print('LOCAL_CAP_GEOMETRY_DONE',before,after,flush=True)
for p in ob.data.polygons:p.use_smooth=True
for mat in ob.data.materials:
 for node in mat.node_tree.nodes:
  if node.type=='HUE_SAT':node.inputs['Hue'].default_value=.545;node.inputs['Saturation'].default_value=1.15;node.inputs['Value'].default_value=.70
scene=bpy.context.scene;scene.cycles.samples=48;scene['production_status']='AUTHOR_TRIAL_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));report=json.loads((folder/args.source/'authoring.json').read_text());report.update(revision=args.revision,source=args.source,status='author_trial_pending_view',microhole_repair={'boundary_edges_before':before,'boundary_edges_after':after,'simple_loops_capped':len(filled),'maximum_loop_diameter_limit_m':.045,'uv_transfer':'Local triangle fan preserves boundary UVs; optional seam caps project each tiny triangle into its own adjacent source chart, avoiding interpolation across atlas islands','uv_seam_loops_skipped':skipped_uv,'uv_seam_loops_locally_projected':projected_uv,'filled_loops':filled},remaining=['Remaining connected arc wires','Head texture and eye fidelity','Large boundaries intentionally untouched','Independent review']);(out/'authoring.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('MICROHOLES_CAPPED',len(filled),before,after,flush=True)
for name,loc,target,scale in [('head_detail',(5,-3,2.4),(1.65,0,1.05),1.9),('back_detail',(1,-4,4),(.1,0,1.8),2.3),('author_preview',(6,-8,4.3),(0,0,1.2),5.8)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
