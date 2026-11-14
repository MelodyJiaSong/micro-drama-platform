from pathlib import Path
import bpy,json
root=Path(__file__).resolve().parents[3];folder=next(root.glob('2_*'))/'background/map_3d/environment_sources/blender_human_base_meshes'
with bpy.data.libraries.load(str(folder/'realistic_skull.blend'),link=False) as (src,dst):
 print('COLLECTIONS',src.collections,flush=True);dst.objects=src.objects
for o in dst.objects:
 if not o:continue
 bpy.context.scene.collection.objects.link(o)
 print(json.dumps({'name':o.name,'type':o.type,'location':list(o.location),'rotation':list(o.rotation_euler),'dimensions':list(o.dimensions),'faces':len(o.data.polygons) if o.type=='MESH' else None,'modifiers':[(m.name,m.type) for m in o.modifiers],'asset_description':o.asset_data.description if o.asset_data else None}),flush=True)
