"""Locate visible discontinuities on the actual 1000px author preview."""
from pathlib import Path
import bpy,json
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m21_Polar_Furbolg/model_3d'));bpy.ops.wm.open_mainfile(filepath=str(folder/'r05/authoring.blend'));scene=bpy.context.scene;camera=scene.camera;deps=bpy.context.evaluated_depsgraph_get();frame=camera.data.view_frame(scene=scene);left=min(v.x for v in frame);right=max(v.x for v in frame);low=min(v.y for v in frame);high=max(v.y for v in frame);result=[]
for px,py in [(600,380),(560,370),(460,355),(630,390),(350,410),(410,420),(650,440),(550,320)]:
 origin=camera.matrix_world@Vector((left+(right-left)*px/1000,high-(high-low)*py/1000,0));direction=camera.matrix_world.to_quaternion()@Vector((0,0,-1));hit,pos,normal,face,obj,matrix=scene.ray_cast(deps,origin,direction)
 item={'pixel':[px,py],'hit':hit,'point':list(pos),'object':obj.name if obj else None,'face':face}
 if hit and obj.type=='MESH' and 0<=face<len(obj.data.polygons):
  ids=obj.data.polygons[face].vertices; item['material_slot']=obj.data.polygons[face].material_index; item['materials']=[m.name if m else None for m in obj.data.materials]
  item['attributes']={name:sum(obj.data.attributes[name].data[i].value for i in ids)/len(ids) for name in ['LeatherCoverage','FurCoverage'] if obj.data.attributes.get(name)}
 result.append(item)
(folder/'r05/cape_boundary_probe.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result),flush=True)
