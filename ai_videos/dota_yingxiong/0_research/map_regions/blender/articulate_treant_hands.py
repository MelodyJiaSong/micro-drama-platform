"""Clean residual crown fragments and author three separated tapered wooden digits."""
from pathlib import Path
import bpy,bmesh,json,math,sys,numpy as np,argparse
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from build_production_map import surface
parser=argparse.ArgumentParser();parser.add_argument('--revision',default='r07');parser.add_argument('--source',default='r05');args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));folder=next(WORLD.glob('characters/*/m1_Treant/model_3d'));out=folder/args.revision;out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/args.source/'authoring.blend'));coll=bpy.data.collections['ASSET_m1'];body=max((o for o in coll.objects if o.type=='MESH'),key=lambda o:len(o.data.polygons));retained_material=body.data.materials[0]
with bpy.data.libraries.load(str(folder/'r01/inspection/m1_r01.blend'),link=False) as (src,dst):dst.objects=['geometry_0']
native=dst.objects[0];bpy.context.scene.collection.objects.link(native);ancestor=native.parent
while ancestor:
 if not ancestor.users_collection:bpy.context.scene.collection.objects.link(ancestor)
 ancestor=ancestor.parent
bpy.context.view_layer.update();mesh=native.data.copy();mesh.transform(native.matrix_world);mesh.materials.clear();mesh.materials.append(retained_material);body.data=mesh;bpy.data.objects.remove(native,do_unlink=True)
co=np.empty(len(body.data.vertices)*3,np.float32);body.data.vertices.foreach_get('co',co);co=co.reshape(-1,3)
assert abs(float(co[:,2].max())-1.9)<.02,co[:,2].max()
wrists={}
for side in [-1,1]:
 selected=co[(co[:,0]*side>.23)&(co[:,2]>.445)&(co[:,2]<.475)]
 if len(selected)<5:raise RuntimeError('Cannot locate wrist '+str(side))
 wrists[side]=Vector(selected.mean(0))
bm=bmesh.new();bm.from_mesh(body.data);remove=[v for v in bm.verts if v.co.z>1.60 or (v.co.z>1.37 and math.hypot(v.co.x,v.co.y)>.18) or (v.co.z>1.29 and math.hypot(v.co.x,v.co.y)>.27) or (.14<v.co.z<.45 and abs(v.co.x)>.23)];bmesh.ops.delete(bm,geom=remove,context='VERTS');bm.to_mesh(body.data);bm.free();body.data.update()
if body.data.has_custom_normals:body.data.normals_split_custom_set([(0,0,0)]*len(body.data.loops))
wood=surface('Treant_finger_ridged_bark',(.018,.012,.006),(.065,.043,.022),50,.88,.0025)
nt=wood.node_tree;bs=nt.nodes.get('Principled BSDF');tc=nt.nodes.new('ShaderNodeTexCoord');scale=nt.nodes.new('ShaderNodeVectorMath');scale.operation='MULTIPLY';scale.inputs[1].default_value=(6,6,1.6);nt.links.new(tc.outputs['Object'],scale.inputs[0]);tex=nt.nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(WORLD/'background/map_3d/environment_sources/tree_small_02/textures/tree_small_02_diff_2k.jpg'),check_existing=True);tex.projection='BOX';tex.projection_blend=.3;nt.links.new(scale.outputs[0],tex.inputs['Vector']);nt.links.new(tex.outputs['Color'],bs.inputs['Base Color'])
mul=nt.nodes.new('ShaderNodeMixRGB');mul.blend_type='MULTIPLY';mul.inputs[0].default_value=1;mul.inputs[2].default_value=(.35,.38,.25,1);nt.links.new(tex.outputs['Color'],mul.inputs[1]);nt.links.new(mul.outputs[0],bs.inputs['Base Color'])
for ob in coll.objects:
 if ob.name.startswith(('Treant_primary_crown_branch','Treant_crown_branch','Treant_leaf_twig','Maple_petioles_and_midvein','Individual_curved_lobed_leaves')):ob.location.z-=.08
 if ob.type=='CURVE' and ob.name.startswith(('Treant_primary_crown_branch','Treant_crown_branch','Treant_leaf_twig')):ob.data.materials.clear();ob.data.materials.append(wood)
created=[]
def curve(name,pts,radius,radii):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=12;cu.bevel_depth=radius;cu.bevel_resolution=3;cu.use_fill_caps=True;sp=cu.splines.new('BEZIER');sp.bezier_points.add(len(pts)-1)
 for p,co,r in zip(sp.bezier_points,pts,radii):p.co=co;p.handle_left_type='AUTO';p.handle_right_type='AUTO';p.radius=r
 ob=bpy.data.objects.new(name,cu);coll.objects.link(ob);cu.materials.append(wood);created.append(ob)
for side,wrist in wrists.items():
 palm=wrist+Vector((side*.015,0,-.055));curve('Treant_wooden_palm',[wrist+Vector((0,0,.04)),wrist,palm],.048,[1.1,1,.78])
 for digit in range(3):
  spread=(digit-1)*.032;start=palm+Vector((side*spread,0,.02));tip=start+Vector((side*spread*.45,-.035,-(.225 if digit==1 else .195)))
  curve('Treant_separate_wooden_digit',[start,start+Vector((side*spread*.7,-.035,-.06)),tip+Vector((side*.015,-.04,.055)),tip],.020,[1,.90,.63,.06])
bpy.ops.object.select_all(action='DESELECT')
for ob in created:ob.select_set(True)
bpy.context.view_layer.objects.active=created[0];bpy.ops.object.convert(target='MESH');bpy.ops.object.join();hand=bpy.context.object;hand.name='Continuous_bark_hands_three_curved_digits';remesh=hand.modifiers.new('Organic_palm_digit_union','REMESH');remesh.mode='VOXEL';remesh.voxel_size=.0015;remesh.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=remesh.name);smooth=hand.modifiers.new('Subtle_knuckle_blending','SMOOTH');smooth.factor=.35;smooth.iterations=2;bpy.ops.object.modifier_apply(modifier=smooth.name);texture=bpy.data.textures.new('Wood_finger_surface_relief',type='CLOUDS');texture.noise_scale=.012;disp=hand.modifiers.new('Physical_bark_roughness','DISPLACE');disp.texture=texture;disp.strength=.002;disp.mid_level=.5
scene=bpy.context.scene;scene.cycles.samples=48;scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'m1','revision':args.revision,'source':args.source,'status':'author_preview_not_accepted','changes':['Removed residual lateral crown fragments','Three separate curved wood digits on each hand','Voxel-unioned palms with scanned bark and physical surface relief'],'wrist_positions':{str(k):list(v) for k,v in wrists.items()},'remaining':['Wrist joins and mesh boundaries','Lichen volume and bark detail','Eyes and crown realism','Full multi-angle review']},indent=2),encoding='utf-8');scene.render.filepath=str(out/'author_preview.png');bpy.ops.render.render(write_still=True)
