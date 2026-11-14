"""Remove a demonstrated tube-frame flip without changing the hook centre line."""
from pathlib import Path
import bpy,json,sys,math
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg23_*/model_3d'));out=folder/'r32';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r31/authoring.blend'));repaired=[]
for name,radius in [('Rounded_spatial_question_mark_hook',.052),('Continuous_cast_hook_cradle_return',.055)]:
 ob=bpy.data.objects[name];me=ob.data;count=len(me.vertices)//16;centres=[sum((me.vertices[j*16+k].co for k in range(16)),Vector())/16 for j in range(count)];previous_t=None;u=None
 for j,p in enumerate(centres):
  tangent=(centres[min(j+1,count-1)]-centres[max(j-1,0)]).normalized()
  if previous_t is None:
   u=tangent.cross(Vector((0,1,0)))
   if u.length<.01:u=tangent.cross(Vector((1,0,0)))
   u.normalize()
  else:u=previous_t.rotation_difference(tangent)@u;u=(u-tangent*u.dot(tangent)).normalized()
  v=tangent.cross(u).normalized()
  for k in range(16):a=k*math.tau/16;me.vertices[j*16+k].co=p+radius*(u*math.cos(a)+v*math.sin(a))
  previous_t=tangent
 me.update();repaired.append(name)
scene=bpy.context.scene;scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));report=json.loads((folder/'r31/authoring.json').read_text());report.update(revision='r32',source='r31',diagnosis='r31 hook side preview revealed a pinched slit at the vertical tangent; independent cross(Z) frames flipped sign there',frame_repair='Parallel transport of ring basis vectors through vertical tangents',repaired_meshes=repaired);(out/'authoring.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
for name,loc,target,scale in [('hook_side_detail',(8,1.0,4.55),(1.1,1.0,4.45),1.5),('perspective_preview',(9,-14,7.5),(0,0,2.5),6.9)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
