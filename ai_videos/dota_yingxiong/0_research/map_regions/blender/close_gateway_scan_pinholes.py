"""Cap small degree-two scan holes with local UV charts; preserve large openings."""
from pathlib import Path
import bpy,bmesh,json,sys,numpy as np,argparse
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
parser=argparse.ArgumentParser();parser.add_argument('--source',default='r05');parser.add_argument('--revision',default='r06');parser.add_argument('--weld',action='store_true');args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m303_*/model_3d'));out=folder/args.revision;out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/args.source/'authoring.blend'));ob=bpy.data.objects['Gateway_merchant_body'];bm=bmesh.new();bm.from_mesh(ob.data);before_weld={'vertices':len(bm.verts),'boundary_edges':sum(e.is_boundary for e in bm.edges)}
if args.weld:bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.000001);print('COINCIDENT_VERTEX_WELD',before_weld,'TO',len(bm.verts),sum(e.is_boundary for e in bm.edges),flush=True)
remaining={e for e in bm.edges if e.is_boundary};before=len(remaining);groups=[]
while remaining:
 first=remaining.pop();stack=[first];part=[first]
 while stack:
  edge=stack.pop()
  for v in edge.verts:
   for e in v.link_edges:
    if e in remaining:remaining.remove(e);stack.append(e);part.append(e)
 groups.append(part)
print('BOUNDARIES',before,'COMPONENTS',len(groups),flush=True);uv=bm.loops.layers.uv.active;floatlayers=[bm.verts.layers.float.get(k) for k in ['ScalpHair','BeardStubble','Eyebrows']];floatlayers=[x for x in floatlayers if x is not None];filled=[]
for part in groups:
 if len(part)>96 or len(part)<3:continue
 vs={v for e in part for v in e.verts};dim=np.ptp(np.array([tuple(v.co) for v in vs]),axis=0)
 if max(dim)>.012:continue
 adjacency={v:[] for v in vs}
 for e in part:
  for v in e.verts:adjacency[v].append(e)
 if any(len(edges)!=2 for edges in adjacency.values()):continue
 first=part[0];start=first.verts[0];current=start;edge=first;order=[];charts=[];normals=[];material=first.link_faces[0].material_index
 for _ in range(len(part)):
  other=edge.other_vert(current);face=edge.link_faces[0];a=next(l for l in face.loops if l.vert==current);b=next(l for l in face.loops if l.vert==other);avg=sum((l[uv].uv for l in face.loops),Vector((0,0)))/len(face.loops);charts.append((a[uv].uv.copy(),b[uv].uv.copy(),avg));normals.append(face.normal.copy());order.append(current);current=other;edge=next(e for e in adjacency[current] if e!=edge)
 if current!=start:continue
 centre=bm.verts.new(sum((v.co for v in order),Vector())/len(order));normal=sum(normals,Vector()).normalized()
 for layer in floatlayers:centre[layer]=sum(v[layer] for v in order)/len(order)
 for j,a in enumerate(order):
  b=order[(j+1)%len(order)];seq=[centre,a,b] if (a.co-centre.co).cross(b.co-centre.co).dot(normal)>=0 else [centre,b,a];face=bm.faces.new(seq);face.smooth=True;face.material_index=material;ua,ub,uc=charts[j];mid=(ua+ub)*.5;centeruv=mid+(uc-mid)*.1
  for loop in face.loops:loop[uv].uv=centeruv if loop.vert==centre else ua if loop.vert==a else ub
 filled.append({'edges':len(part),'dimensions_m':dim.tolist(),'centre':list(centre.co)})
bm.normal_update();after=sum(e.is_boundary for e in bm.edges);bm.to_mesh(ob.data);bm.free();ob.data.update();print('LOCAL_CAPS',len(filled),'BOUNDARIES_AFTER',after,flush=True)
scene=bpy.context.scene;scene['production_status']='LOCAL_SCAN_PINHOLE_REPAIR_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));(out/'authoring.json').write_text(json.dumps({'asset_id':'m303','revision':args.revision,'source':args.source,'status':'author_trial_pending_view','coincident_vertex_weld':{'enabled':args.weld,'distance_m':.000001,'before':before_weld},'microhole_repair':{'boundary_edges_before':before,'boundary_edges_after':after,'simple_loops_capped':len(filled),'maximum_loop_extent_m':.012,'uv_method':'Per-edge adjacent chart projection; no interpolation across UV islands','hair_mask_method':'Average boundary vertex attributes at new fan centres','loops':filled},'remaining':['Verify black marks were geometric holes rather than baked albedo','Preserve nostrils, mouth and ear openings','Face/skin and eye realism','Independent review']},indent=2),encoding='utf-8')
scene.cycles.device='CPU';scene.cycles.samples=32;scene.render.threads_mode='FIXED';scene.render.threads=6
for name,loc,target,scale in [('face_detail',(0,-2,1.7),(0,0,1.7),.38),('face_side',(1.3,-2,1.7),(0,0,1.7),.38),('author_preview',(4,-6,2),(0,0,.925),2.37)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
