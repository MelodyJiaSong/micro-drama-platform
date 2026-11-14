"""Repair reviewed r19 surface and crown defects without remeshing the body."""
from pathlib import Path
import bpy,json,sys,math
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m1_Treant/model_3d'));out=folder/'r20';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r19/authoring.blend'));coll=bpy.data.collections['ASSET_m1']
body=max((o for o in coll.all_objects if o.type=='MESH'),key=lambda o:len(o.data.polygons))
wood=next(m for m in bpy.data.materials if m.name.startswith('Continuous_scanned_furrowed_bark')).copy();wood.name='Unified_scanned_bark_r20'
anchor=bpy.data.objects.new('Shared_world_bark_coordinates',None);coll.objects.link(anchor)
for n in wood.node_tree.nodes:
 if n.type=='TEX_COORD':n.object=anchor
 elif n.type=='VECT_MATH' and n.operation=='MULTIPLY':n.inputs[1].default_value=(2.8,2.8,1.45)
 elif n.type=='MIX_RGB' and n.blend_type=='MULTIPLY':n.inputs[2].default_value=(.21,.22,.19,1)
 elif n.type=='BUMP':n.inputs['Distance'].default_value=.012;n.inputs['Strength'].default_value=.85
 elif n.type=='BSDF_PRINCIPLED':n.inputs['Specular IOR Level'].default_value=.13
wood_count=0
for ob in coll.objects:
 if ob==body or ob.name.startswith(('Native_crown_branch','Attached_foliage_twig','Connected_supplementary_petiole','Scanned_leaf_petiole','Wood_inside_spurious')):
  ob.data.materials.clear();ob.data.materials.append(wood);wood_count+=1
knot=next(o for o in coll.objects if o.name.startswith('Wood_inside_spurious'))
knot.location.y+=.025;knot.scale.y*=.30
# The actual shader receives a dark green / plum palette; reduce the white specular leaf backs.
leafmats=[m for m in bpy.data.materials if m.name.startswith('Scanned_dark_living_maple')]
for i,mat in enumerate(leafmats):
 nt=mat.node_tree;n,l=nt.nodes,nt.links;bs=next(n for n in n if n.type=='BSDF_PRINCIPLED');color=next(n for n in n if n.type=='TEX_IMAGE' and n.image and 'Color' in n.image.name)
 gray=n.new('ShaderNodeRGBToBW');l.new(color.outputs['Color'],gray.inputs[0]);ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.08;ramp.color_ramp.elements[1].position=.75
 purple=i%3==2
 ramp.color_ramp.elements[0].color=(.003,.0015,.004,1) if purple else (.002,.004,.001,1)
 ramp.color_ramp.elements[1].color=(.038,.010,.030,1) if purple else (.012,.040,.009,1)
 l.new(gray.outputs[0],ramp.inputs[0]);l.new(ramp.outputs[0],bs.inputs['Base Color'])
 for socket in ['Roughness','Specular IOR Level','Subsurface Weight']:
  for link in list(bs.inputs[socket].links):l.remove(link)
 bs.inputs['Roughness'].default_value=.84;bs.inputs['Specular IOR Level'].default_value=.035;bs.inputs['Subsurface Weight'].default_value=.015
 for node in n:
  if node.type=='NORMAL_MAP':node.inputs['Strength'].default_value=.35
  elif node.type=='BSDF_TRANSLUCENT':l.new(ramp.outputs[0],node.inputs['Color'])
  elif node.type=='MIX_SHADER':node.inputs[0].default_value=.035
bpy.context.view_layer.update()
prefixes=('Scanned_maple_leaf_','Supplementary_scanned_maple_leaf','Attached_foliage_twig','Connected_supplementary_petiole','Scanned_leaf_petiole','Native_crown_branch')
def crown_point(p):
 radius=math.hypot(p.x,p.y);droop=.14*min(1,max(0,(radius-.12)/.30))
 return Vector((p.x*1.15,p.y*1.24,1.40+(p.z-1.40)*.94-droop))
for ob in coll.objects:
 if not ob.name.startswith(prefixes):continue
 # Transform vertices in world space; shared leaf meshes are copied before deformation.
 ob.data=ob.data.copy();world=ob.matrix_world.copy();inv=world.inverted()
 if ob.type=='MESH':
  for v in ob.data.vertices:v.co=inv@crown_point(world@v.co)
 elif ob.type=='CURVE':
  for spline in ob.data.splines:
   for p in spline.points:
    result=inv@crown_point(world@p.co.xyz);p.co=(*result,p.co.w)
   for p in spline.bezier_points:
    p.co=inv@crown_point(world@p.co);p.handle_left=inv@crown_point(world@p.handle_left);p.handle_right=inv@crown_point(world@p.handle_right)
bpy.context.view_layer.update();top=max((o.matrix_world@Vector(c)).z for o in coll.objects if o.type in ['MESH','CURVE'] for c in o.bound_box)
scale=1.9/top
for ob in coll.objects:
 if ob==anchor:continue
 ob.location*=scale;ob.scale*=scale
scene=bpy.context.scene;scene.cycles.device='CPU';scene.cycles.samples=64;scene.render.threads_mode='FIXED';scene.render.threads=8;scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED'
scene.camera.location=(0,-6,1.25);scene.camera.data.ortho_scale=2.25;look_at(scene.camera,(0,0,.95))
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'m1','revision':'r20','source':'r19','status':'author_preview_not_accepted','changes':['Shared scanned bark and world coordinates across trunk, branches and recessed central fill','Dark green and plum leaf palette with low specular and translucency','Broader drooping outer leaf crown','Normalize stature to 1.9m'],'wood_objects':wood_count,'remaining':['Author visual inspection','Branch connections and head cavity','Full independent review']},indent=2),encoding='utf-8')
scene.render.filepath=str(out/'author_preview.png');bpy.ops.render.render(write_still=True)
scene.camera.data.ortho_scale=.9;scene.camera.location=(.4,-3,1.9);look_at(scene.camera,(0,0,1.55));scene.render.filepath=str(out/'crown_detail.png');bpy.ops.render.render(write_still=True)
