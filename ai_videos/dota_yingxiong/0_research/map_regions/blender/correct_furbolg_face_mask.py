"""Undo false leather tint on the original head without another anatomical warp."""
from pathlib import Path
import bpy,json,sys,numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m21_Polar_Furbolg/model_3d'));out=folder/'r10';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r03/authoring.blend'));coll=bpy.data.collections['ASSET_m21'];body=max((o for o in coll.objects if o.type=='MESH'),key=lambda o:len(o.data.polygons));me=body.data
co=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',co);co=co.reshape(-1,3);old=np.empty(len(co),np.float32);me.attributes['LeatherCoverage'].data.foreach_get('value',old)
def smooth(x,a,b):
 t=np.clip((x-a)/(b-a),0,1);return t*t*(3-2*t)
head=(1-smooth(np.abs(co[:,0]),.16,.26))*(1-smooth(co[:,1],-.41,-.30))*smooth(co[:,2],1.43,1.50)*(1-smooth(co[:,2],1.71,1.82))
new=old*(1-head);me.attributes['LeatherCoverage'].data.foreach_set('value',new);me.update();changed=int(np.sum(old-new>.05));assert changed>50,changed
scene=bpy.context.scene;scene.cycles.device='CPU';scene.cycles.samples=48;scene.render.threads_mode='FIXED';scene.render.threads=8;scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'m21','revision':'r10','source':'r03','status':'author_preview_not_accepted','diagnosis':'Height-based leather mask included forehead above the original narrow face exclusion','change':'Soft spatial exclusion restores original head albedo; source head/neck geometry and groom unchanged','vertices_with_material_mask_correction':changed,'remaining':['Face appearance and exact hood boundary','All r03 geometry and proportion blockers remain','Not a complete repair']},indent=2),encoding='utf-8')
for name,loc,target,scale in [('author_preview',(6,-7,3),(0,0,1.15),2.9),('face_detail',(.5,-3,1.8),(0,-.40,1.61),.72)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
