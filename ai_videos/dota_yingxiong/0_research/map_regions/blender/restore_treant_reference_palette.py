"""Replace accumulated paint-like shading and restore a vertically branching crown."""
from pathlib import Path
import bpy,json,sys,numpy as np
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m1_Treant/model_3d'));out=folder/'r25';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r24/authoring.blend'));coll=bpy.data.collections['ASSET_m1'];body=max((o for o in coll.objects if o.type=='MESH'),key=lambda o:len(o.data.polygons));old=body.data.materials[0]
images={}
for node in old.node_tree.nodes:
 if node.type=='TEX_IMAGE' and node.image:
  for key in ['diff','disp','rough']:
   if '_'+key+'_' in node.image.name:images[key]=node.image
assert len(images)==3
mat=bpy.data.materials.new('Reference_dark_bark_local_moss_and_lichen');mat.use_nodes=True;nt=mat.node_tree;n,l=nt.nodes,nt.links;bs=n.get('Principled BSDF');bs.inputs['Specular IOR Level'].default_value=.18
tc=n.new('ShaderNodeTexCoord');tc.object=bpy.data.objects['Shared_world_bark_coordinates'];scale=n.new('ShaderNodeVectorMath');scale.operation='MULTIPLY';scale.inputs[1].default_value=(2.8,2.8,1.45);l.new(tc.outputs['Object'],scale.inputs[0]);textures={}
for key,img in images.items():
 tex=n.new('ShaderNodeTexImage');tex.image=img;tex.projection='BOX';tex.projection_blend=.25;l.new(scale.outputs[0],tex.inputs['Vector']);textures[key]=tex
tint=n.new('ShaderNodeMixRGB');tint.blend_type='MULTIPLY';tint.inputs[0].default_value=1;tint.inputs[2].default_value=(.28,.22,.15,1);l.new(textures['diff'].outputs['Color'],tint.inputs[1])
def noise(freq,offset=(0,0,0)):
 add=n.new('ShaderNodeVectorMath');add.operation='ADD';add.inputs[1].default_value=offset;l.new(tc.outputs['Object'],add.inputs[0]);q=n.new('ShaderNodeTexNoise');q.inputs['Scale'].default_value=freq;q.inputs['Detail'].default_value=5;l.new(add.outputs[0],q.inputs[0]);return q.outputs['Fac']
def ramp(value,lo,hi):
 q=n.new('ShaderNodeMapRange');q.clamp=True;q.interpolation_type='SMOOTHSTEP';q.inputs['From Min'].default_value=lo;q.inputs['From Max'].default_value=hi;l.new(value,q.inputs['Value']);return q.outputs[0]
def mul(a,b):
 q=n.new('ShaderNodeMath');q.operation='MULTIPLY';l.new(a,q.inputs[0]);l.new(b,q.inputs[1]);return q.outputs[0]
def mix(base,mask,color):
 q=n.new('ShaderNodeMixRGB');l.new(base,q.inputs[1]);l.new(mask,q.inputs[0]);q.inputs[2].default_value=(*color,1);return q.outputs[0]
macro=noise(11);fine=noise(175);lichen=mul(ramp(macro,.47,.62),ramp(fine,.51,.60));surface=mix(tint.outputs[0],lichen,(.075,.085,.063));moss=mul(ramp(noise(17,(2,-1,3)),.46,.59),ramp(noise(110),.38,.55));surface=mix(surface,moss,(.008,.021,.0035));l.new(surface,bs.inputs['Base Color'])
bump=n.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.012;bump.inputs['Strength'].default_value=.8;l.new(textures['disp'].outputs['Color'],bump.inputs['Height']);micro=n.new('ShaderNodeBump');micro.inputs['Distance'].default_value=.001;micro.inputs['Strength'].default_value=.42;l.new(fine,micro.inputs['Height']);l.new(bump.outputs[0],micro.inputs['Normal']);l.new(micro.outputs[0],bs.inputs['Normal']);rough=n.new('ShaderNodeMapRange');rough.inputs['To Min'].default_value=.60;rough.inputs['To Max'].default_value=.90;l.new(textures['rough'].outputs['Color'],rough.inputs['Value']);l.new(rough.outputs[0],bs.inputs['Roughness'])
for ob in coll.objects:
 if hasattr(ob.data,'materials'):
  for i,m in enumerate(ob.data.materials):
   if m==old:ob.data.materials[i]=mat
for index,m in enumerate(sorted((m for m in bpy.data.materials if m.name.startswith('Scanned_dark_living_maple')),key=lambda m:m.name)):
 nt=m.node_tree;leaf=next(q for q in nt.nodes if q.type=='BSDF_PRINCIPLED');r=next(q for q in nt.nodes if q.type=='VALTORGB');r.color_ramp.elements[0].color=(.0015,.003,.0007,1);r.color_ramp.elements[1].color=(*[(.010,.021,.005),(.014,.022,.008),(.014,.017,.011)][index%3],1)
 leaf.inputs['Roughness'].default_value=.43;leaf.inputs['Specular IOR Level'].default_value=.22;leaf.inputs['Coat Weight'].default_value=.06;leaf.inputs['Coat Roughness'].default_value=.32;leaf.inputs['Coat Tint'].default_value=(.70,.65,.79,1);leaf.inputs['Subsurface Weight'].default_value=.025
 for q in nt.nodes:
  if q.type=='NORMAL_MAP':q.inputs['Strength'].default_value=.9
prefixes=('Scanned_maple_leaf_','Supplementary_scanned_maple_leaf','Attached_foliage_twig','Connected_supplementary_petiole','Scanned_leaf_petiole','Native_crown_branch')
def warp(p):
 p=p.copy();a=np.clip((p[:,2]-1.45)/.12,0,1);p[:,0]*=1-.10*a;p[:,1]*=1-.06*a;p[:,2]+=.68*np.maximum(0,p[:,2]-1.45);return p
for ob in coll.objects:
 if ob.hide_render or not (ob==body or ob.name.startswith(prefixes)):continue
 matrix=np.array(ob.matrix_world);rot=matrix[:3,:3];trans=matrix[:3,3];inv=np.linalg.inv(rot)
 if ob.type=='MESH':
  co=np.empty(len(ob.data.vertices)*3,np.float32);ob.data.vertices.foreach_get('co',co);co=co.reshape(-1,3);co=(warp(co@rot.T+trans)-trans)@inv.T;ob.data.vertices.foreach_set('co',co.ravel());ob.data.update()
 elif ob.type=='CURVE':
  for sp in ob.data.splines:
   for p in sp.points:p.co=(*((warp(np.array([rot@np.array(p.co[:3])+trans]))[0]-trans)@inv.T),p.co.w)
bpy.context.view_layer.update();top=max((o.matrix_world@Vector(c)).z for o in coll.objects if not o.hide_render and o.type in ['MESH','CURVE'] for c in o.bound_box);factor=1.9/top
for ob in coll.objects:
 if ob.name=='Shared_world_bark_coordinates' or ob.parent in coll.objects[:]:continue
 ob.location*=factor;ob.scale*=factor
scene=bpy.context.scene;scene.cycles.samples=48;scene.cycles.device='CPU';scene.render.threads_mode='FIXED';scene.render.threads=8;scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'m1','revision':'r25','source':'r24','status':'author_preview_not_accepted','changes':['Rebuilt shared wood shader from scanned bark: warm dark brown, fine locally clustered muted lichen and wet green moss','Unified dark olive leaf palette with subtle plum tint and scanned vein normals','Coherent upward crown and upper-fork elongation, normalized to 1.9m'],'normalization_factor':factor,'remaining':['Author visual assessment','Branch connections and leaf shape','Full independent review']},indent=2),encoding='utf-8')
for name,loc,target,scale in [('author_preview',(0,-6,1.25),(0,0,.95),2.25),('crown_detail',(.4,-3,1.9),(0,0,1.53),.95)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
