"""Export a separate map-preview LOD; preserve authored source and inspect deviation."""
from pathlib import Path
import bpy,bmesh,json,argparse,sys,time,hashlib,numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d'
p=argparse.ArgumentParser();p.add_argument('--asset',required=True);p.add_argument('--face-budget',type=int,default=120000);p.add_argument('--version',default='overview_v001');p.add_argument('--weld',action='store_true');p.add_argument('--protect-boundaries',action='store_true');args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
if args.protect_boundaries and not args.weld:raise ValueError('Boundary protection needs the welded topology')
report=json.loads((OUT/'assembly_working_v022_report.json').read_text(encoding='utf-8'));source=Path(report['source_libraries'][args.asset])
if not source.is_absolute():source=ROOT/source
assert source.is_file(),source
source_hash=hashlib.sha256(source.read_bytes()).hexdigest();dest=OUT/'lod_libraries'/args.version/args.asset;dest.mkdir(parents=True,exist_ok=True);blend=dest/(args.asset+'.blend')
if blend.exists():raise FileExistsError(blend)
with bpy.data.libraries.load(str(source),link=False) as (src,dst):dst.collections=['ASSET_'+args.asset]
coll=dst.collections[0];bpy.context.scene.collection.children.link(coll)
meshes={o.data.as_pointer():o for o in coll.all_objects if o.type=='MESH' and not o.hide_render};dense=[o for o in meshes.values() if len(o.data.polygons)>5000];total=sum(len(o.data.polygons) for o in dense);fixed=sum(len(o.data.polygons) for o in meshes.values() if o not in dense);ratio=min(1,max(10000,args.face_budget-fixed)/max(total,1));changes=[]
print('LOD_START',args.asset,'faces',total+fixed,'ratio',ratio,flush=True)
for ob in dense:
 if ratio>=.999:continue
 start=time.monotonic();mesh=ob.data;weld=None;protected=[]
 # Apply once to a private copy, then restore sharing for all original instances.
 # Blender refuses modifier_apply while the mesh has multiple object users.
 shared_users=[o for o in bpy.data.objects if o.type=='MESH' and o.data==mesh]
 if mesh.users>1:
  ob.data=mesh.copy();mesh=ob.data
 if args.weld:
  original_vertices=len(mesh.vertices);bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6);bm.verts.index_update()
  if args.protect_boundaries:protected=sorted({v.index for e in bm.edges if not e.is_manifold for v in e.verts})
  bm.to_mesh(mesh);bm.free();mesh.update();weld={'distance_local':1e-6,'vertices_merged':original_vertices-len(mesh.vertices),'remaining_vertices':len(mesh.vertices),'protected_boundary_or_nonmanifold_vertices':len(protected)};print('COINCIDENT_WELD',json.dumps(weld),flush=True)
 mesh.calc_loop_triangles();positions=np.empty(len(mesh.vertices)*3,np.float32);mesh.vertices.foreach_get('co',positions);positions=positions.reshape(-1,3);triangles=np.empty(len(mesh.loop_triangles)*3,np.int32);mesh.loop_triangles.foreach_get('vertices',triangles);triangles=triangles.reshape(-1,3)
 tree=BVHTree.FromPolygons(positions,triangles,all_triangles=True);before=len(mesh.polygons);rng=np.random.default_rng(633);sample_idx=rng.choice(len(triangles),min(4000,len(triangles)),replace=False);source_samples=positions[triangles[sample_idx]].mean(1);del positions,triangles
 bpy.ops.object.select_all(action='DESELECT');ob.hide_set(False);ob.select_set(True);bpy.context.view_layer.objects.active=ob
 modifier=ob.modifiers.new('Map_preview_only_mesh_reduction','DECIMATE');modifier.decimate_type='COLLAPSE';modifier.ratio=ratio;modifier.use_collapse_triangulate=True
 if args.protect_boundaries:
  # Blender's collapse implementation skips edges with a zero-weight endpoint:
  # https://github.com/blender/blender/blob/main/source/blender/bmesh/tools/bmesh_decimate_collapse.cc
  group=ob.vertex_groups.new(name='Map_LOD_safe_interior');group.add(list(range(len(mesh.vertices))),1.0,'REPLACE');group.remove(protected);modifier.vertex_group=group.name;modifier.vertex_group_factor=1
 bpy.ops.object.modifier_apply(modifier=modifier.name)
 mesh=ob.data
 if mesh.has_custom_normals:bpy.ops.mesh.customdata_custom_splitnormals_clear()
 for shared_ob in shared_users:
  if shared_ob!=ob:shared_ob.data=ob.data
 mesh=ob.data;mesh.calc_loop_triangles();positions=np.empty(len(mesh.vertices)*3,np.float32);mesh.vertices.foreach_get('co',positions);positions=positions.reshape(-1,3);triangles=np.empty(len(mesh.loop_triangles)*3,np.int32);mesh.loop_triangles.foreach_get('vertices',triangles);triangles=triangles.reshape(-1,3);low_tree=BVHTree.FromPolygons(positions,triangles,all_triangles=True);sample_idx=rng.choice(len(triangles),min(4000,len(triangles)),replace=False);low_samples=positions[triangles[sample_idx]].mean(1)
 source_to_low=np.array([low_tree.find_nearest(Vector(x))[3] for x in source_samples]);low_to_source=np.array([tree.find_nearest(Vector(x))[3] for x in low_samples]);scale=max(ob.matrix_world.to_scale());distances=np.concatenate([source_to_low,low_to_source])*scale
 row={'object':ob.name,'coincident_weld':weld,'faces_before':before,'faces_after':len(mesh.polygons),'uv_layers_after':len(mesh.uv_layers),'surface_samples_each_direction':len(sample_idx),'sampled_symmetric_distance_world_m_quantiles':np.quantile(distances,[.5,.9,.99,1]).tolist(),'quantiles':[.5,.9,.99,1],'elapsed_seconds':round(time.monotonic()-start,2)};changes.append(row);print('LOD_MESH',json.dumps(row),flush=True);del tree,low_tree,positions,triangles
bpy.data.libraries.write(str(blend),{coll},path_remap='ABSOLUTE',fake_user=True,compress=True)
result={'status':'map_preview_LOD_pending_visual_comparison_not_asset_acceptance','asset':args.asset,'source':str(source),'source_sha256':source_hash,'output':str(blend),'output_sha256':hashlib.sha256(blend.read_bytes()).hexdigest(),'face_budget':args.face_budget,'visible_unique_faces_before':total+fixed,'visible_unique_faces_after':sum(len(o.data.polygons) for o in meshes.values()),'changes':changes,'limitations':['Sampled distance is not an exact Hausdorff bound.','No new normal bake; original UV and materials retained through decimation.','Use only map overview/working preview, not close asset acceptance.','Original source files unchanged.']}
(dest/'lod_report.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print('LOD_LIBRARY_SAVED',args.asset,flush=True)
