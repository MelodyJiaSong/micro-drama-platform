"""Remove four ray-identified reconstruction wires; preserve the bone plates."""
from pathlib import Path
import bpy,bmesh,json,sys,argparse
from mathutils import Vector,kdtree
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
parser=argparse.ArgumentParser();parser.add_argument('--revision',default='r05');parser.add_argument('--groups',nargs='+',type=int,default=[975590,1452231,1980591,2022153]);args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m26_Thunder_Lizard/model_3d'));out=folder/args.revision;out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r04/authoring.blend'));coll=bpy.data.collections['ASSET_m26'];ob=max((o for o in coll.all_objects if not o.hide_render and o.type=='MESH'),key=lambda o:len(o.data.polygons))
groups=json.loads((folder/'wire_component_faces_r04.json').read_text());chosen=args.groups;ids=set(i for g in chosen for i in groups[str(g)])
archive=ob.copy();archive.data=ob.data;archive.name='Archive_r04_before_verified_wire_removal';coll.objects.link(archive);archive.hide_render=True;archive.hide_viewport=True;ob.data=ob.data.copy()
bm=bmesh.new();bm.from_mesh(ob.data);bm.faces.ensure_lookup_table();bm.verts.ensure_lookup_table();uvlayer=bm.loops.layers.uv.active
seedverts={v for i in ids for v in bm.faces[i].verts};kd=kdtree.KDTree(len(seedverts))
for i,v in enumerate(seedverts):kd.insert(ob.matrix_world@v.co,i)
kd.balance();coords=[ob.matrix_world@v.co for v in seedverts];low=Vector(tuple(min(p[j] for p in coords)-.012 for j in range(3)));high=Vector(tuple(max(p[j] for p in coords)+.012 for j in range(3)))
removed=[]
for f in bm.faces:
 p=ob.matrix_world@f.calc_center_median()
 if all(low[j]<=p[j]<=high[j] for j in range(3)) and (f.index in ids or kd.find(p)[2]<.009):removed.append(f)
print('VERIFIED_WIRE_FACES',len(ids),'WITH_LOCAL_DARK_EDGE_MARGIN',len(removed),flush=True)
removedset=set(removed);cutedges={e for f in removed for e in f.edges if any(q not in removedset for q in e.link_faces)}
bmesh.ops.delete(bm,geom=removed,context='FACES')
pending={e for e in cutedges if e.is_valid and e.is_boundary};filled=[];unfilled=[]
while pending:
 part=[];stack=[pending.pop()]
 while stack:
  e=stack.pop();part.append(e)
  for v in e.verts:
   for q in v.link_edges:
    if q in pending:pending.remove(q);stack.append(q)
 verts={v for e in part for v in e.verts};adj={v:[] for v in verts}
 for e in part:
  a,b=e.verts;adj[a].append(b);adj[b].append(a)
 points=[ob.matrix_world@v.co for v in verts];diam=max(max(p[j] for p in points)-min(p[j] for p in points) for j in range(3))
 if not all(len(a)==2 for a in adj.values()) or diam>.055:unfilled.append({'edges':len(part),'diameter_m':diam});continue
 first=next(iter(verts));order=[first];prev=None;cur=first
 while True:
  nxt=next(v for v in adj[cur] if v!=prev)
  if nxt==first:break
  order.append(nxt);prev,cur=cur,nxt
  if len(order)>len(verts):raise RuntimeError('Non-simple cut boundary')
 centre=bm.verts.new(sum((v.co for v in order),Vector())/len(order))
 for j,a in enumerate(order):
  b=order[(j+1)%len(order)];edge=next(e for e in a.link_edges if b in e.verts);adjacent=edge.link_faces[0];normal=adjacent.normal.copy();source={loop.vert:loop[uvlayer].uv.copy() for loop in adjacent.loops};ua,ub=source[a],source[b];uc=sum(source.values(),Vector((0,0)))/len(source);mid=(ua+ub)*.5;cu=mid+(uc-mid)*.1
  seq=[centre,a,b] if (a.co-centre.co).cross(b.co-centre.co).dot(normal)>=0 else [centre,b,a];face=bm.faces.new(seq);face.material_index=adjacent.material_index;face.smooth=True
  for loop in face.loops:loop[uvlayer].uv=cu if loop.vert==centre else source[loop.vert]
 filled.append({'edges':len(part),'diameter_m':diam})
loose=[v for v in bm.verts if not v.link_faces]
if loose:bmesh.ops.delete(bm,geom=loose,context='VERTS')
bm.normal_update();boundaries=sum(e.is_boundary for e in bm.edges);bm.to_mesh(ob.data);bm.free();ob.data.update()
scene=bpy.context.scene;scene.cycles.samples=48;scene['production_status']='AUTHOR_TRIAL_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
report=json.loads((folder/'r04/authoring.json').read_text());report.update(revision=args.revision,source='r04',wire_removal={'evidence':'wire_component_probe_r04.json: actual back-render ray hits and neutral connected patches; r05 near/far images checked before expanded selection','selected_groups':chosen,'selected_white_faces':len(ids),'removed_faces_including_9mm_margin':len(removed),'closed_new_cuts':filled,'unclosed_new_cuts':unfilled,'remaining_boundary_edges':boundaries,'scope':'Explicit neutral wire/fragment groups on upper back. Ivory plate tips and unverified tail geometry retained.'},remaining=['Remaining wires and fragments','Head texture and large mesh cracks','Independent review']);(out/'authoring.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report['wire_removal']),flush=True)
for name,loc,target,scale in [('back_detail',(1,-4,4),(.1,0,1.8),2.3),('far_back_detail',(-1,4,4),(.1,0,1.8),2.3),('author_preview',(6,-8,4.3),(0,0,1.2),5.8)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
