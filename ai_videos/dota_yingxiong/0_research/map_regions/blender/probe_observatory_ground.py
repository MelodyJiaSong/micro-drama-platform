from pathlib import Path
import bpy,json
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg23_*/model_3d'))
bpy.ops.wm.open_mainfile(filepath=str(folder/'r46/authoring.blend'))
rows=[]
for o in bpy.data.objects:
 if o.name not in ['Studio_floor','Continuous_root_soil_bed','Asset_metre_calibration'] and not o.name.startswith('Irregular_root_soil_collar'):continue
 p=[o.matrix_world@Vector(c) for c in o.bound_box] if o.type=='MESH' else [o.matrix_world.translation]
 rows.append({'name':o.name,'hide_render':o.hide_render,'world_min':[min(v[k] for v in p) for k in range(3)],'world_max':[max(v[k] for v in p) for k in range(3)],'location':list(o.location),'scale':list(o.scale),'materials':[m.name for m in o.data.materials] if o.type=='MESH' else []})
(folder/'r46/ground_probe.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');print(json.dumps(rows),flush=True)
