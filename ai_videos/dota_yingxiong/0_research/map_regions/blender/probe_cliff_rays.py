"""Identify the actual geometry under bright northern cliff pixels."""
from pathlib import Path
import bpy,json
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v022.blend'));scene=bpy.context.scene;cam=bpy.data.objects['Map_Overview'];deps=bpy.context.evaluated_depsgraph_get();projection=cam.calc_matrix_camera(deps,x=1000,y=750,scale_x=1,scale_y=1);inv=(projection@cam.matrix_world.inverted()).inverted();rows=[]
for x,y in [(280,62),(320,65),(360,63),(400,65),(440,62),(480,62),(520,65),(105,150)]:
 near=inv@Vector((2*x/1000-1,1-2*y/750,-1,1));far=inv@Vector((2*x/1000-1,1-2*y/750,1,1));origin=near.xyz/near.w;target=far.xyz/far.w;direction=(target-origin).normalized();hits=[]
 for _ in range(8):
  ok,point,normal,index,ob,matrix=scene.ray_cast(deps,origin,direction)
  if not ok:break
  materials=[m.name for m in ob.data.materials if m] if hasattr(ob.data,'materials') else [];hits.append({'object':ob.name,'world_point':list(point),'face':index,'materials':materials,'collections':[c.name for c in ob.users_collection]})
  if ob.name!='Atmosphere_volume':break
  origin=point+direction*.05
 rows.append({'pixel':[x,y],'hits':hits})
(OUT/'cliff_ray_probe.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');print(json.dumps(rows),flush=True)
