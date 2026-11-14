"""Reduce waxy crown highlights and put scanned bark on connecting branches."""
from pathlib import Path
import bpy,json,sys,math
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));folder=next(WORLD.glob('characters/*/m1_Treant/model_3d'));out=folder/'r12';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r10/authoring.blend'));coll=bpy.data.collections['ASSET_m1']
for mat in bpy.data.materials:
 if not mat.name.startswith('Living_maple_lamina_'):continue
 bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.72;bs.inputs['Specular IOR Level'].default_value=.12;bs.inputs['Coat Weight'].default_value=0;bs.inputs['Subsurface Weight'].default_value=.02
mat=bpy.data.materials['Connected_branch_rough_brown_bark'];nt=mat.node_tree;bs=nt.nodes.get('Principled BSDF');tc=nt.nodes.new('ShaderNodeTexCoord');scale=nt.nodes.new('ShaderNodeVectorMath');scale.operation='MULTIPLY';scale.inputs[1].default_value=(8,8,2);nt.links.new(tc.outputs['Object'],scale.inputs[0]);tex=nt.nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(WORLD/'background/map_3d/environment_sources/tree_small_02/textures/tree_small_02_diff_2k.jpg'),check_existing=True);tex.projection='BOX';tex.projection_blend=.3;nt.links.new(scale.outputs[0],tex.inputs['Vector']);tint=nt.nodes.new('ShaderNodeMixRGB');tint.blend_type='MULTIPLY';tint.inputs[0].default_value=1;tint.inputs[2].default_value=(.40,.34,.23,1);nt.links.new(tex.outputs['Color'],tint.inputs[1]);nt.links.new(tint.outputs[0],bs.inputs['Base Color'])
bs.inputs['Specular IOR Level'].default_value=.18
for ob in list(coll.objects):
 if ob.type=='CURVE' and ob.name.startswith('Native_crown_branch'):
  sp=ob.data.splines[0];start=Vector(sp.points[0].co[:3]);end=Vector(sp.points[-1].co[:3]);mid=start.lerp(end,.5)
  # Curve path receives asymmetry without breaking the branch endpoints.
  sp.points[1].co=(*(mid+Vector((.018*math.sin(end.x*30),.012*math.cos(end.z*20),.014))),1)
scene=bpy.context.scene;scene.cycles.samples=64;scene.cycles.device='CPU';scene.camera.location=(0,-6,1.25);scene.camera.data.ortho_scale=2.25;look_at(scene.camera,(0,0,.95));scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'m1','revision':'r12','source':'r10','status':'author_preview_not_accepted','changes':['Reduced leaf specular highlight and coat','Scanned bark reflectance on connected branches','Small branch curvature variation'],'remaining':['Author visual check','Cut crown transitions','Source torso texture distortion','Full independent review']},indent=2),encoding='utf-8')
scene.render.filepath=str(out/'author_preview.png');bpy.ops.render.render(write_still=True)
scene.camera.data.ortho_scale=.9;scene.camera.location=(.4,-3,1.9);look_at(scene.camera,(0,0,1.57));scene.render.filepath=str(out/'crown_detail.png');bpy.ops.render.render(write_still=True)
