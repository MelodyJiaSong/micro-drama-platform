from pathlib import Path
import bpy,json
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg23_*/model_3d'))/'r28';bpy.ops.wm.open_mainfile(filepath=str(folder/'authoring.blend'));parent=bpy.data.objects['Asset_metre_calibration'];out=[]
for o in bpy.data.objects:
 if o.hide_render or not (o.name.startswith(('High_open_question_mark_hook','Sphere_cast_cradle','Wide_flat_cast_support','Irregular_root_soil_collar')) or o.name=='Studio_floor'):continue
 mat=parent.matrix_world.inverted()@o.matrix_world;coords=[mat@Vector(c) for c in o.bound_box];r={'name':o.name,'bounds_parent':[[min(p[i] for p in coords),max(p[i] for p in coords)] for i in range(3)],'location':list(o.location)}
 if o.type=='MESH' and o.name.startswith(('High_open','Wide_flat')):r['first_four_parent']=[list(mat@v.co) for v in o.data.vertices[:4]]
 out.append(r)
(folder/'connection_probe.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out),flush=True)
