"""Read-only evaluated geometry probe for the visible roof/frieze separation."""
from pathlib import Path
import bpy,json
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3]
folder=next(next(ROOT.glob('2_*')).glob('background/*/bg23_*/model_3d'))/'r27'
bpy.ops.wm.open_mainfile(filepath=str(folder/'authoring.blend'))
parent=bpy.data.objects['Asset_metre_calibration'];dg=bpy.context.evaluated_depsgraph_get();rows=[]
for ob in bpy.data.collections['ASSET_bg23'].objects:
 if ob.hide_render or not ob.name.startswith(('Cast_bronze_dome','Mitered_continuous_frieze','Continuous_lime_backing')):continue
 ev=ob.evaluated_get(dg);me=ev.to_mesh();m=parent.matrix_world.inverted()@ev.matrix_world
 coords=[m@v.co for v in me.vertices]
 rows.append({'name':ob.name,'vertices':len(coords),'faces':len(me.polygons),'bounds_local':[[min(c[i] for c in coords),max(c[i] for c in coords)] for i in range(3)] if coords else None,'materials':[x.name if x else None for x in me.materials]})
 ev.to_mesh_clear()
(folder/'roof_contact_probe.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
print(json.dumps([r for r in rows if not r['name'].startswith('Continuous_lime_backing')]),flush=True)
