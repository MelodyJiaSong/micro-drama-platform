"""Address stable r21 review defects: branch taper, leaf sheen, lichen and eye folds."""
from pathlib import Path
import bpy,json,sys,numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m1_Treant/model_3d'));out=folder/'r22';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r21/authoring.blend'));coll=bpy.data.collections['ASSET_m1'];body=max((o for o in coll.objects if o.type=='MESH'),key=lambda o:len(o.data.polygons));mat=body.data.materials[0];nt=mat.node_tree;n,l=nt.nodes,nt.links;bs=next(q for q in n if q.type=='BSDF_PRINCIPLED');tc=next(q for q in n if q.type=='TEX_COORD');color=next(q for q in n if q.type=='TEX_IMAGE' and q.image and '_diff_' in q.image.name)
gray=n.new('ShaderNodeRGBToBW');l.new(color.outputs['Color'],gray.inputs[0]);bark=n.new('ShaderNodeValToRGB');bark.color_ramp.elements[0].position=.01;bark.color_ramp.elements[0].color=(.009,.010,.007,1);bark.color_ramp.elements[1].position=.45;bark.color_ramp.elements[1].color=(.055,.052,.043,1);l.new(gray.outputs[0],bark.inputs[0])
def noise(scale,offset=(0,0,0)):
 add=n.new('ShaderNodeVectorMath');add.operation='ADD';add.inputs[1].default_value=offset;l.new(tc.outputs['Object'],add.inputs[0]);node=n.new('ShaderNodeTexNoise');node.inputs['Scale'].default_value=scale;node.inputs['Detail'].default_value=4;l.new(add.outputs[0],node.inputs['Vector']);return node.outputs['Fac']
def threshold(value,lo,hi):
 node=n.new('ShaderNodeMapRange');node.clamp=True;node.interpolation_type='SMOOTHSTEP';node.inputs['From Min'].default_value=lo;node.inputs['From Max'].default_value=hi;l.new(value,node.inputs['Value']);return node.outputs[0]
def product(a,b):
 node=n.new('ShaderNodeMath');node.operation='MULTIPLY';l.new(a,node.inputs[0]);l.new(b,node.inputs[1]);return node.outputs[0]
def layer(base,mask,color):
 node=n.new('ShaderNodeMixRGB');l.new(mask,node.inputs[0]);l.new(base,node.inputs[1]);node.inputs[2].default_value=(*color,1);return node.outputs[0]
fine=noise(220);lichen=product(threshold(noise(12),.39,.57),threshold(fine,.38,.57));surface=layer(bark.outputs[0],lichen,(.26,.29,.23));moss=product(threshold(noise(18,(1.7,-.6,3.1)),.53,.67),threshold(noise(140),.35,.55));surface=layer(surface,moss,(.018,.033,.006));l.new(surface,bs.inputs['Base Color'])
bump=n.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.0016;bump.inputs['Strength'].default_value=.55;l.new(fine,bump.inputs['Height'])
if bs.inputs['Normal'].is_linked:l.new(bs.inputs['Normal'].links[0].from_socket,bump.inputs['Normal'])
l.new(bump.outputs[0],bs.inputs['Normal'])
# A single green palette with subtle purple backfaces avoids separate magenta confetti.
for mat in [m for m in bpy.data.materials if m.name.startswith('Scanned_dark_living_maple')]:
 nt=mat.node_tree;n,l=nt.nodes,nt.links;leaf=next(q for q in n if q.type=='BSDF_PRINCIPLED');ramp=next(q for q in n if q.type=='VALTORGB');ramp.color_ramp.elements[0].position=.03;ramp.color_ramp.elements[0].color=(.002,.004,.001,1);ramp.color_ramp.elements[1].position=.55;ramp.color_ramp.elements[1].color=(.018,.030,.008,1)
 geo=n.new('ShaderNodeNewGeometry');back=n.new('ShaderNodeMixRGB');back.blend_type='MULTIPLY';back.inputs[0].default_value=1;back.inputs[2].default_value=(1.1,.75,1.2,1);l.new(ramp.outputs[0],back.inputs[1]);mix=n.new('ShaderNodeMixRGB');l.new(geo.outputs['Backfacing'],mix.inputs[0]);l.new(ramp.outputs[0],mix.inputs[1]);l.new(back.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],leaf.inputs['Base Color'])
 leaf.inputs['Roughness'].default_value=.52;leaf.inputs['Specular IOR Level'].default_value=.14;leaf.inputs['Coat Weight'].default_value=.10;leaf.inputs['Coat Roughness'].default_value=.30;leaf.inputs['Coat Tint'].default_value=(.65,.58,.78,1)
 for node in n:
  if node.type=='NORMAL_MAP':node.inputs['Strength'].default_value=.9
  elif node.type=='BSDF_TRANSLUCENT':l.new(mix.outputs[0],node.inputs['Color'])
tapered=0
for ob in coll.objects:
 if ob.type!='CURVE':continue
 if ob.name.startswith('Native_crown_branch'):
  for spline in ob.data.splines:
   points=spline.points if spline.type!='BEZIER' else spline.bezier_points
   for j,p in enumerate(points):t=j/max(1,len(points)-1);p.radius=1.5*(1-t)**1.25+.045
  tapered+=1
 elif ob.name.startswith('Attached_foliage_twig'):
  ob.data.bevel_depth=.0032
  for spline in ob.data.splines:
   points=spline.points if spline.type!='BEZIER' else spline.bezier_points
   for j,p in enumerate(points):p.radius=1-j/max(1,len(points)-1)*.85
# Sculpt shallow bark folds over the existing carved sockets; retain the eyes and topology.
me=body.data;co=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',co);co=co.reshape(-1,3);matrix=np.array(body.matrix_world,dtype=np.float32);world=co@matrix[:3,:3].T+matrix[:3,3];eyes=[o for o in coll.objects if o.name.startswith('Recessed_eye_dark_wood')];amount=np.zeros(len(co),np.float32)
for eye in eyes:
 px,py,pz=eye.matrix_world.translation;front=np.clip((py-world[:,1]-.005)/.025,0,1);brow=np.exp(-((world[:,0]-px)/.045)**2-((world[:,2]-pz-.022)/.018)**2);amount+=.014*brow*front
world[:,1]-=amount;co=(world-matrix[:3,3])@np.linalg.inv(matrix[:3,:3]).T;me.vertices.foreach_set('co',co.ravel());me.update()
scene=bpy.context.scene;scene.cycles.samples=64;scene.cycles.device='CPU';scene.render.threads_mode='FIXED';scene.render.threads=8;scene.camera.location=(0,-6,1.25);scene.camera.data.ortho_scale=2.25;look_at(scene.camera,(0,0,.95));scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'m1','revision':'r22','source':'r21','status':'author_preview_not_accepted','changes':['Taper seven main branches and smaller twigs','Dark green leaves with subtle backface colour and varied wet sheen','Cool dark bark, broader pale lichen and patchy wet moss','Small bark eyebrow relief around current eye sockets'],'tapered_main_branches':tapered,'remaining':['Crown clustering and exposed head shape','Leaf/branch connections','Independent multi-angle review'],'review_direction_note':'r19 requested crown closer to eyes; r21 requests exposed head forks. Original design re-viewed; prioritize stable material and branch defects before another crown relocation.'},indent=2),encoding='utf-8');print('BARK_BRANCH_REPAIR_SAVED',flush=True)
scene.render.filepath=str(out/'author_preview.png');bpy.ops.render.render(write_still=True)
scene.camera.data.ortho_scale=.9;scene.camera.location=(.4,-3,1.9);look_at(scene.camera,(0,0,1.55));scene.render.filepath=str(out/'crown_detail.png');bpy.ops.render.render(write_still=True)
