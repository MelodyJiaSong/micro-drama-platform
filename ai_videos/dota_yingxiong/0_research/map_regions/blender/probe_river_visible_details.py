from pathlib import Path
import bpy,json
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v026.blend'));scene=bpy.context.scene;camera=bpy.data.objects['River_Eye_Level'];scene.camera=camera;scene.render.resolution_x=1200;scene.render.resolution_y=900;deps=bpy.context.evaluated_depsgraph_get();frame=camera.data.view_frame(scene=scene);left,right=min(v.x for v in frame),max(v.x for v in frame);bottom,top=min(v.y for v in frame),max(v.y for v in frame);rows=[]
for py in range(465,531,3):
 for px in range(735,856,3):
  local=Vector((left+(right-left)*px/1200,top-(top-bottom)*py/900,frame[0].z));origin=camera.matrix_world.translation;direction=(camera.matrix_world@local-origin).normalized();hit,pos,normal,face,ob,matrix=scene.ray_cast(deps,origin,direction)
  if hit and ob and ob.name not in ['Terrain_683d','River_surface','Continuous_outer_land']:
   rows.append({'pixel':[px,py],'point':list(pos),'object':ob.name,'collections':[c.name for c in ob.users_collection],'matrix':[[float(v) for v in row] for row in matrix]})
(OUT/'river_visible_detail_probe.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');print(json.dumps(rows[:30]),flush=True)
