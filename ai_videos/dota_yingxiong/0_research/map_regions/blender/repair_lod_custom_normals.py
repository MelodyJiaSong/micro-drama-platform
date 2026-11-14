"""Test whether stale imported split normals cause the decimation shading failure."""
from pathlib import Path
import bpy,json,hashlib
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';source=OUT/'lod_libraries/overview_v002/m304';dest=OUT/'lod_libraries/overview_v003/m304';dest.mkdir(parents=True,exist_ok=True);blend=dest/'m304.blend'
if blend.exists():raise FileExistsError(blend)
bpy.ops.wm.read_factory_settings(use_empty=True)
with bpy.data.libraries.load(str(source/'m304.blend'),link=False) as (src,dst):dst.collections=['ASSET_m304']
coll=dst.collections[0];bpy.context.scene.collection.children.link(coll);changes=[]
for ob in coll.all_objects:
 if ob.type!='MESH' or ob.hide_render:continue
 mesh=ob.data;before=mesh.has_custom_normals;attrs=[a.name for a in mesh.attributes];bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob
 if before:bpy.ops.mesh.customdata_custom_splitnormals_clear()
 changes.append({'object':ob.name,'had_custom_normals':before,'has_custom_normals_after':mesh.has_custom_normals,'attributes_before':attrs,'attributes_after':[a.name for a in mesh.attributes]})
bpy.data.libraries.write(str(blend),{coll},path_remap='ABSOLUTE',fake_user=True,compress=True);report=json.loads((source/'lod_report.json').read_text());report.update(output=str(blend),output_sha256=hashlib.sha256(blend.read_bytes()).hexdigest(),custom_normal_repair=changes,status='custom_normal_diagnostic_pending_comparison');(dest/'lod_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('NORMAL_DIAGNOSTIC',json.dumps(changes),flush=True)
