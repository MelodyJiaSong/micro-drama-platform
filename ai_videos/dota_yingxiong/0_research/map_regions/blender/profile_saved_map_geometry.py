"""Read-only map resource inventory; does not evaluate geometry or render."""
from pathlib import Path
import bpy,json,collections,sys,argparse
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d'
p=argparse.ArgumentParser();p.add_argument('--blend',default='assembly_working_v022.blend');args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []);source=OUT/args.blend
bpy.ops.wm.open_mainfile(filepath=str(source))
print('MAP_LOADED',len(bpy.data.meshes),len(bpy.data.images),flush=True)
rows=[];by_mesh=collections.defaultdict(list)
for ob in bpy.data.objects:
 if ob.type=='MESH':by_mesh[ob.data.as_pointer()].append(ob)
for mesh in bpy.data.meshes:
 objects=by_mesh[mesh.as_pointer()]
 rows.append({'name':mesh.name,'vertices':len(mesh.vertices),'edges':len(mesh.edges),'faces':len(mesh.polygons),'corners':len(mesh.loops),'uv_layers':len(mesh.uv_layers),'library':mesh.library.filepath if mesh.library else None,'objects':[o.name for o in objects],'all_objects_render_hidden':all(o.hide_render for o in objects),'estimated_base_buffers_mib':round((len(mesh.vertices)*24+len(mesh.edges)*8+len(mesh.polygons)*16+len(mesh.loops)*(8+len(mesh.uv_layers)*8))/1024**2,2)})
rows.sort(key=lambda r:r['estimated_base_buffers_mib'],reverse=True)
print('MESH_INVENTORY_DONE',flush=True)
# Image.size/is_float can decode packed pixels. Never load all full-resolution
# texture buffers merely to profile a memory-constrained scene.
images=[{'name':im.name,'filepath':im.filepath,'users':im.users,'pixels_already_loaded':im.has_data,'packed_bytes':sum(p.packed_file.size for p in im.packed_files)} for im in bpy.data.images]
report={'purpose':'Read-only inventory, approximate storage only; not Cycles peak allocation measurement. Hidden archive geometry is included in blend data but should not enter render BVH. Image dimensions deliberately omitted to avoid decoding full-resolution pixels.','source':args.blend,'meshes':rows,'images':images,'total_unique_vertices':sum(r['vertices'] for r in rows),'total_unique_faces':sum(r['faces'] for r in rows),'estimated_base_buffers_gib':round(sum(r['estimated_base_buffers_mib'] for r in rows)/1024,3),'total_packed_image_gib':round(sum(r['packed_bytes'] for r in images)/1024**3,3)}
(OUT/(source.stem+'_resource_inventory.json')).write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k not in ['meshes','images']}),flush=True);print('TOP_MESHES',json.dumps(rows[:12]),flush=True)
