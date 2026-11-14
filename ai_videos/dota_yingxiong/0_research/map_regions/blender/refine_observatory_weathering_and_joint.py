"""Respond to r41 review with a visible cast joint, textured stone and forest growth."""
from pathlib import Path
import bpy,json,sys,math,random,numpy as np
from mathutils import Vector
from mathutils.geometry import closest_point_on_tri
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at,material
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));OUT=WORLD/'background/map_3d';folder=next(WORLD.glob('background/*/bg23_*/model_3d'));out=folder/'r42';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r41/authoring.blend'));coll=bpy.data.collections['ASSET_bg23'];parent=bpy.data.objects['Asset_metre_calibration'];rng=random.Random(2342)
def adopt(ob,name,mat):
 for c in list(ob.users_collection):c.objects.unlink(ob)
 coll.objects.link(ob);ob.name=name;ob.parent=parent;ob.data.materials.append(mat);return ob
# Keep the scanned bark's colour and fine relief instead of flattening it into pale grey.
bark=bpy.data.materials['Tileable_root_bark_actual_scale'];nt=bark.node_tree;n,l=nt.nodes,nt.links;bs=next(q for q in n if q.type=='BSDF_PRINCIPLED');tex=next(q for q in n if q.type=='TEX_IMAGE' and q.image and '_diff_' in q.image.name)
tint=n.new('ShaderNodeMixRGB');tint.blend_type='MULTIPLY';tint.inputs[0].default_value=1;tint.inputs[2].default_value=(1.15,.78,.48,1);l.new(tex.outputs['Color'],tint.inputs[1]);l.new(tint.outputs[0],bs.inputs['Base Color']);bs.inputs['Roughness'].default_value=.9;bs.inputs['Specular IOR Level'].default_value=.12
for node in n:
 if node.type=='BUMP':node.inputs['Distance'].default_value=.004;node.inputs['Strength'].default_value=.85
roots=0
for ob in coll.objects:
 if ob.hide_render or ob.type!='MESH' or not ob.name.startswith(('Woven_pale_primary_root','Connected_crossing_rootlet','Interwoven_circumferential_root')):continue
 count=len(ob.data.vertices)//14
 for j in range(count):
  vs=[ob.data.vertices[j*14+k] for k in range(14)];centre=sum((v.co for v in vs),Vector())/14
  for k,v in enumerate(vs):
   delta=v.co-centre
   if delta.length>1e-6:v.co+=delta.normalized()*(.0022*math.sin(k*2.9+j*.16)+.001*math.sin(k*5.1-j*.09))
 ob.data.update();roots+=1
# Restore a continuous low soil volume under roots; fade only its outer edge.
soil=material('Forest_root_soil_continuous',(.07,.045,.02),.93);nt=soil.node_tree;n,l=nt.nodes,nt.links;bs=n.get('Principled BSDF');tc=n.new('ShaderNodeTexCoord');scale=n.new('ShaderNodeVectorMath');scale.operation='SCALE';scale.inputs[3].default_value=2.5;l.new(tc.outputs['Object'],scale.inputs[0]);tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(next((OUT/'textures').glob('brown_mud_02_diff_2k.*'))),check_existing=True);tex.projection='BOX';tex.projection_blend=.3;l.new(scale.outputs[0],tex.inputs[0]);tint=n.new('ShaderNodeMixRGB');tint.blend_type='MULTIPLY';tint.inputs[0].default_value=1;tint.inputs[2].default_value=(.36,.31,.23,1);l.new(tex.outputs[0],tint.inputs[1]);l.new(tint.outputs[0],bs.inputs['Base Color']);attr=n.new('ShaderNodeAttribute');attr.attribute_name='Root_ground_fade';l.new(attr.outputs['Fac'],bs.inputs['Alpha']);soil.surface_render_method='DITHERED'
verts=[];faces=[];fade=[]
for i in range(257):
 a=i/256*math.tau;wall=2.39/math.cos((a+math.pi/8)%(math.pi/4)-math.pi/8)
 for j in range(13):
  t=j/12;r=wall-.08+t*(.90+.14*math.sin(a*7)+.08*math.cos(a*19));z=.018+.07*math.sin(math.pi*t)**1.5+.012*math.sin(a*29+t*8)*math.sin(math.pi*t)-.055*t**7
  if math.sin(a)<-.93:z=-.10
  verts.append((r*math.cos(a),r*math.sin(a),z));q=max(0,min(1,(t-.70)/.30));fade.append(1-q*q*(3-2*q))
for i in range(256):
 for j in range(12):k=i*13+j;faces.append((k,k+1,k+14,k+13))
mesh=bpy.data.meshes.new('Continuous_root_soil_bed');mesh.from_pydata(verts,[],faces);mesh.update();ob=bpy.data.objects.new(mesh.name,mesh);coll.objects.link(ob);ob.parent=parent;mesh.materials.append(soil);mesh.attributes.new('Root_ground_fade','FLOAT','POINT').data.foreach_set('value',np.array(fade,np.float32))
for p in mesh.polygons:p.use_smooth=True
for ob in coll.objects:
 if ob.name.startswith('Small_irregular_root_soil_hummock'):ob.hide_render=True
 if not ob.hide_render and ob.name.startswith('Irregular_fern_root_margin'):ob.scale*=1.6
# Stone grain, pitting and dirt at a physical scale, with lower saturation.
stone=bpy.data.materials['Grey_cyan_carved_stone'];nt=stone.node_tree;n,l=nt.nodes,nt.links;bs=next(q for q in n if q.type=='BSDF_PRINCIPLED');geo=n.new('ShaderNodeNewGeometry');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=24;noise.inputs['Detail'].default_value=5;l.new(geo.outputs['Position'],noise.inputs[0]);ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.055,.071,.050,1);ramp.color_ramp.elements[1].color=(.24,.27,.22,1);l.new(noise.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],bs.inputs['Base Color']);pore=n.new('ShaderNodeTexNoise');pore.inputs['Scale'].default_value=420;pore.inputs['Detail'].default_value=3;l.new(geo.outputs['Position'],pore.inputs[0]);bump=n.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.0015;bump.inputs['Strength'].default_value=.65;l.new(pore.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs['Normal'],bs.inputs['Normal']);bs.inputs['Roughness'].default_value=.88
leaf_count=0
for ob in list(coll.objects):
 if not ob.hide_render and ob.name.startswith('Wall_attached_ivy_leaf'):
  ob.scale*=2.1;leaf_count+=1
# Small moss tufts on the cornice, with shared mesh and irregular gaps.
moss=material('Damp_cornice_moss',(.028,.045,.008),.98);mv=[];mf=[]
for k in range(7):
 a=k*math.tau/7;xx=.025*math.cos(a);yy=.025*math.sin(a);h=rng.uniform(.025,.065);b=len(mv);mv.extend([(xx-.009,yy,0),(xx+.009,yy,0),(xx+.012,yy+.006,h*.55),(xx,yy+.012,h)]);mf.append((b,b+1,b+2,b+3))
mm=bpy.data.meshes.new('Moss_tuft_shared');mm.from_pydata(mv,[],mf);mm.materials.append(moss);moss_count=0
for i in range(420):
 a=rng.random()*math.tau
 if rng.random()<.25:continue
 r=2.42/math.cos((a+math.pi/8)%(math.pi/4)-math.pi/8)+rng.uniform(-.025,.04);ob=bpy.data.objects.new('Cornice_moss_tuft',mm);coll.objects.link(ob);ob.parent=parent;ob.location=(r*math.cos(a),r*math.sin(a),2.585+rng.uniform(-.015,.012));ob.rotation_euler.z=a;ob.scale=(rng.uniform(.7,1.5),)*3;moss_count+=1
# Widen the readable clearance and add a real riveted block at the cast joint.
bpy.context.view_layer.update();inverse=parent.matrix_world.inverted();ball=max((o for o in coll.objects if not o.hide_render and o.name.startswith('Reference_mirror_sphere')),key=lambda o:o.matrix_world.translation.z);center=inverse@ball.matrix_world.translation;radius=max((inverse@ball.matrix_world@v.co-center).length for v in ball.data.vertices);hook=bpy.data.objects['Continuous_flat_question_hook'];hook.data.calc_loop_triangles();shift=0
def gap():return min((closest_point_on_tri(center,*[hook.data.vertices[i].co for i in tri.vertices])-center).length-radius for tri in hook.data.loop_triangles)
while gap()<.085 and shift<.32:
 for v in hook.data.vertices:v.co.y+=.02
 shift+=.02
bpy.data.objects['Question_hook_terminal_ball'].location.y+=shift;hook.data.update();bronze=bpy.data.materials['Cast_bronze_with_verdigris'];joint=center+Vector((0,shift*.5,-radius-.13));bpy.ops.mesh.primitive_cube_add(size=1,location=joint);clamp=adopt(bpy.context.object,'Riveted_cast_hook_joint',bronze);clamp.scale=(.25,max(.20,shift+.10),.20);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);be=clamp.modifiers.new('Cast_joint_rounding','BEVEL');be.width=.018;be.segments=4
for sign in [-1,1]:
 for dz in [-.055,.055]:
  loc=joint+Vector((sign*.075,-max(.20,shift+.10)/2-.006,dz));bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=.019,location=loc);rivet=adopt(bpy.context.object,'Hook_joint_rivet',bronze);rivet.scale=(1,.4,1)
scene=bpy.context.scene;scene['production_status']='OBSERVATORY_R42_AUTHOR_TRIAL';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));report={'asset_id':'bg23','revision':'r42','source':'r41','status':'author_trial_pending_view','roots_with_geometric_bark':roots,'root_colour':'Direct photographic bark multiplied by warm tone; no pale grayscale remap','soil':'Continuous volumetric low bed and larger ferns','ivy_leaves_enlarged':leaf_count,'moss_tufts':moss_count,'hook_rear_shift_parent_m':shift,'hook_minimum_globe_gap_parent_m':gap(),'hook_joint':'Bevelled cast block with four front rivets','remaining':['Root wood and soil appearance','Joint placement and load path','Stone grain','Ivy overlap and moss scale','Independent review']};(out/'authoring.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('R42_SAVED',json.dumps(report),flush=True)
scene.cycles.device='CPU';scene.cycles.samples=32;scene.render.threads_mode='FIXED';scene.render.threads=6
for name,loc,target,scale in [('root_detail',(6,-7,3),(1.25,-.9,.35),3.8),('hook_side_detail',(8,1,4.55),(1.1,1,4.45),1.5),('perspective_preview',(9,-14,7.5),(0,0,2.5),6.9)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
