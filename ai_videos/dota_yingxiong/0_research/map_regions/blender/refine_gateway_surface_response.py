"""Correct proven scalp reflection and inspect orbital seams and gaze."""
from pathlib import Path
import bpy,numpy as np,json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m303_*/model_3d'));out=folder/'r05';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r04/authoring.blend'));body=bpy.data.objects['Gateway_merchant_body'];me=body.data
if me.has_custom_normals:me.normals_split_custom_set([(0,0,0)]*len(me.loops))
co=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',co);co=co.reshape(-1,3)
for cx in [-.0494,.03458]:
 weight=np.exp(-((co[:,0]-cx)/.018)**2-((co[:,2]-1.6582)/.014)**2)*np.clip((-.025-co[:,1])/.04,0,1);co[:,2]+=.003*weight
me.vertices.foreach_set('co',co.ravel());me.update()
for mat in me.materials:
 nt=mat.node_tree;bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');attr=nt.nodes.new('ShaderNodeAttribute');attr.attribute_name='ScalpHair';remap=nt.nodes.new('ShaderNodeMapRange');remap.inputs['To Min'].default_value=.28;remap.inputs['To Max'].default_value=.025;nt.links.new(attr.outputs['Fac'],remap.inputs['Value']);nt.links.new(remap.outputs[0],bs.inputs['Specular IOR Level'])
for name in ['Buzzcut_individual_hairs','Stubble_individual_hairs','Brows_individual_hairs']:
 for mat in bpy.data.objects[name].data.materials:
  bs=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED');bs.inputs['Specular IOR Level'].default_value=.03
for ob in bpy.data.collections['ASSET_m303'].all_objects:
 if ob.name.startswith(('Iris_','Pupil_')):ob.location.z-=.003
patch=bpy.data.objects['MPFB_orbital_skin_patches'];pc=np.empty(len(patch.data.vertices)*3,np.float32);patch.data.vertices.foreach_get('co',pc);pc=pc.reshape(-1,3);d=np.minimum(*[np.sqrt(((pc[:,0]-cx)/.034)**2+((pc[:,2]-1.73)/.028)**2) for cx in [-.0494,.02394]]);t=np.clip((d-.86)/.30,0,1);pc[:,1]+=.0014*t*t*(3-2*t);patch.data.vertices.foreach_set('co',pc.ravel());patch.data.update()
scene=bpy.context.scene;scene['production_status']='SCALP_REFLECTANCE_AND_FACE_AUTHOR_TRIAL_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'m303','revision':'r05','source':'r04','status':'author_trial_pending_view','evidence':'r04 hair_albedo_control.png confirms base colour black; standard lighting renders gray','changes':['Scalp-only Specular IOR Level .025; skin remains .28; matte hair curves .03','Clear source custom normals after deformation','Move irises/pupils down 3mm within fitted eye volumes','Inset outer orbital patch edge by up to 1.4mm','Lift mouth corners smoothly by 3mm'],'remaining':['Source mesh holes','Skin seam continuity','Eyes and natural expression','Independent review']},indent=2),encoding='utf-8')
scene.cycles.device='CPU';scene.cycles.samples=32;scene.render.threads_mode='FIXED';scene.render.threads=6
for name,loc in [('face_detail',(0,-2,1.7)),('face_side',(1.3,-2,1.7))]:
 scene.camera.location=loc;look_at(scene.camera,(0,0,1.7));scene.camera.data.ortho_scale=.38;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
