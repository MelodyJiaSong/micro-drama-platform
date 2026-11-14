from pathlib import Path
import bpy,json
root=Path(__file__).resolve().parents[3];folder=next(next(root.glob('2_*')).glob('characters/*/m306_*/model_3d'))
bpy.ops.wm.open_mainfile(filepath=str(folder/'r21/authoring.blend'))
for o in bpy.data.collections['ASSET_m306'].objects:
 if o.hide_render:continue
 print(json.dumps({'name':o.name,'type':o.type,'location':list(o.location),'scale':list(o.scale),'materials':[s.material.name for s in o.material_slots if s.material],'dimensions':list(o.dimensions)}))
