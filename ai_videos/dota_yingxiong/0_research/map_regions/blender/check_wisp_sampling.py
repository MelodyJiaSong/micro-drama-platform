"""Check whether denoising turns subpixel luminous dust into a smoke trail."""
from pathlib import Path
import bpy,json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m306_*/model_3d'));out=folder/'r22';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r21/authoring.blend'));scene=bpy.context.scene
scene.cycles.use_denoising=False;scene.cycles.samples=96;scene.cycles.transparent_max_bounces=64
coll=bpy.data.collections['ASSET_m306']
removed=[]
for o in list(coll.objects):
 if o.hide_render or (o.type=='LIGHT' and o.data.energy==0):removed.append(o.name);bpy.data.objects.remove(o,do_unlink=True)
scene.render.resolution_x=900;scene.render.resolution_y=900
bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'revision':'r22','source':'r21','status':'sampling_diagnosis','changes':['Denoising disabled at 96 samples; transparent bounces increased to 64','Hidden historical objects and zero-energy lamps removed'],'removed_objects':removed,'remaining':['Compare side and close images before changing optical geometry']},indent=2),encoding='utf-8')
for name,loc,target,scale in [('side_sampling',(4,0,1.65),(0,0,.65),1.65),('close_preview',(1.1,-1.6,1.25),(0,.05,1),.72)]:
 scene.camera.data.ortho_scale=scale;scene.camera.location=loc;look_at(scene.camera,target);scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
