"""Measured hook clearance, a continuous cast return, and localized root-soil contacts."""
from pathlib import Path
import bpy,json,sys,math,random
from mathutils import Vector
from mathutils.geometry import closest_point_on_tri
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg23_*/model_3d'));out=folder/'r33';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r32/authoring.blend'));coll=bpy.data.collections['ASSET_bg23'];parent=bpy.data.objects['Asset_metre_calibration'];bronze=bpy.data.materials['Cast_bronze_with_verdigris'];old=bpy.data.objects['Rounded_spatial_question_mark_hook'];me=old.data;count=len(me.vertices)//16;hook=[sum((me.vertices[j*16+k].co for k in range(16)),Vector())/16+Vector((0,.20,0)) for j in range(count)];old.hide_render=True;old.hide_viewport=True;bpy.data.objects['Continuous_cast_hook_cradle_return'].hide_render=True;bpy.data.objects['Continuous_cast_hook_cradle_return'].hide_viewport=True;bpy.data.objects['Question_hook_terminal_ball'].location.y+=.20
start=Vector((1.20,1.02,4.61));end=hook[0];direction=(hook[1]-hook[0]).normalized();b=start+Vector((0,.07,-.18));c=end-direction*.20;return_points=[]
for j in range(65):t=j/64;return_points.append((1-t)**3*start+3*(1-t)**2*t*b+3*(1-t)*t*t*c+t**3*end)
points=return_points+hook[1:];radii=[.060-(.060-.052)*j/64 for j in range(65)]+[.052]*(len(hook)-1);verts=[];faces=[];u=None;previous=None
for j,p in enumerate(points):
 tangent=(points[min(j+1,len(points)-1)]-points[max(j-1,0)]).normalized()
 if previous is None:u=tangent.cross(Vector((1,0,0))).normalized()
 else:u=previous.rotation_difference(tangent)@u;u=(u-tangent*u.dot(tangent)).normalized()
 v=tangent.cross(u).normalized()
 for k in range(20):a=k*math.tau/20;verts.append(tuple(p+radii[j]*(u*math.cos(a)+v*math.sin(a))))
 previous=tangent
for j in range(len(points)-1):
 for k in range(20):faces.append((j*20+k,j*20+(k+1)%20,(j+1)*20+(k+1)%20,(j+1)*20+k))
faces.extend([tuple(range(19,-1,-1)),tuple((len(points)-1)*20+k for k in range(20))]);mesh=bpy.data.meshes.new('Continuous_round_casting');mesh.from_pydata(verts,[],faces);ob=bpy.data.objects.new('Continuous_round_hook_and_cradle_return',mesh);coll.objects.link(ob);ob.parent=parent;mesh.materials.append(bronze)
for f in mesh.polygons:f.use_smooth=True
bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=.105,depth=.12,location=(1.20,.95,4.61));socket=bpy.context.object
for col in list(socket.users_collection):col.objects.unlink(socket)
coll.objects.link(socket);socket.parent=parent;socket.name='Cast_round_to_flat_cradle_socket';socket.data.materials.append(bronze);be=socket.modifiers.new('Cast_socket_edge_rounding','BEVEL');be.width=.012;be.segments=4
bark=bpy.data.materials['Tileable_root_bark_actual_scale']
for node in bark.node_tree.nodes:
 if node.type=='VALTORGB' and abs(node.color_ramp.elements[1].position-.45)<.001:node.color_ramp.elements[0].color=(.065,.050,.032,1);node.color_ramp.elements[1].color=(.31,.25,.17,1)
raised=0
for root in coll.objects:
 if root.hide_render:continue
 if root.name.startswith('Fine_feeder_root') and root.type=='CURVE':
  root.data.bevel_depth*=1.3
  for sp in root.data.splines:
   for p in sp.points:
    if p.co.z>-.02:p.co.z+=.012
  raised+=1
# Small non-planar soil hummocks fade geometrically below the studio/map ground,
# instead of reintroducing the rejected continuous dark collar.
soil=bpy.data.materials.new('Localized_root_soil');soil.use_nodes=True;nt=soil.node_tree;n,l=nt.nodes,nt.links;bs=n.get('Principled BSDF');bs.inputs['Roughness'].default_value=.94;tc=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='SCALE';mapping.inputs[3].default_value=2.5;l.new(tc.outputs['Object'],mapping.inputs[0]);tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(next((next(ROOT.glob('2_*'))/'background/map_3d/textures').glob('forest_ground_04_diff_2k.*'))),check_existing=True);tex.projection='BOX';tex.projection_blend=.3;l.new(mapping.outputs[0],tex.inputs['Vector']);tint=n.new('ShaderNodeMixRGB');tint.blend_type='MULTIPLY';tint.inputs[0].default_value=1;tint.inputs[2].default_value=(.34,.32,.25,1);l.new(tex.outputs[0],tint.inputs[1]);l.new(tint.outputs[0],bs.inputs['Base Color']);noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=90;l.new(tc.outputs['Object'],noise.inputs['Vector']);bump=n.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.006;bump.inputs['Strength'].default_value=.45;l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],bs.inputs['Normal']);rng=random.Random(2333);mounds=0
for i,root in enumerate(o for o in coll.objects if not o.hide_render and o.name.startswith('Woven_pale_primary_root')):
 if i%2:continue
 count=len(root.data.vertices)//14;centre=sum((root.data.vertices[min(count-1,22)*14+k].co for k in range(14)),Vector())/14;radius=rng.uniform(.18,.29);phase=rng.random()*math.tau;vv=[];ff=[]
 for j in range(9):
  t=j/8
  for k in range(32):
   a=k*math.tau/32;r=radius*t*(1+.16*math.sin(a*3+phase)+.09*math.sin(a*7));zz=.035*(1-t*t)**2-.012*t**5+.004*math.sin(a*5)*math.sin(t*math.pi);vv.append((centre.x+r*math.cos(a),centre.y+r*math.sin(a),zz))
 for j in range(8):
  for k in range(32):ff.append((j*32+k,j*32+(k+1)%32,(j+1)*32+(k+1)%32,(j+1)*32+k))
 mm=bpy.data.meshes.new('Small_irregular_root_soil_hummock');mm.from_pydata(vv,[],ff);mo=bpy.data.objects.new('Small_irregular_root_soil_hummock',mm);coll.objects.link(mo);mo.parent=parent;mm.materials.append(soil)
 for f in mm.polygons:f.use_smooth=True
 mounds+=1
bpy.context.view_layer.update();ball=max((o for o in coll.objects if not o.hide_render and o.name.startswith('Reference_mirror_sphere')),key=lambda o:o.matrix_world.translation.z);center=ball.matrix_world.translation;radius=max((ball.matrix_world@v.co-center).length for v in ball.data.vertices);mesh.calc_loop_triangles();world=[ob.matrix_world@v.co for v in mesh.vertices];gaps=[];hookgaps=[]
for tri in mesh.loop_triangles:
 gap=(closest_point_on_tri(center,*[world[i] for i in tri.vertices])-center).length-radius;gaps.append(gap)
 if min(tri.vertices)>=64*20:hookgaps.append(gap)
assert min(gaps)>0,(min(gaps),'sphere intersection');assert min(hookgaps)>.04,min(hookgaps)
scene=bpy.context.scene;scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED';scene.cycles.samples=48;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));report=json.loads((folder/'r32/authoring.json').read_text());report.update(revision='r33',source='r32',changes=['Move the hook rearward 20cm in parent space; measured against the actual sphere','One continuously framed mesh and tangent-matched curved return with a cast round-to-flat socket','Intermediate pale grey-brown bark; raise fine feeder network and add localized soil hummocks'],hook_clearance_m={'entire_round_casting':min(gaps),'upper_hook_only':min(hookgaps)},prior_verified_intersection_m=.001474359,raised_feeder_roots=raised,localized_soil_mounds=mounds,remaining=['Root-soil naturalness and network visibility','Support joint appearance','Chrome reflections versus matte control','Independent review']);(out/'authoring.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('HOOK_CLEARANCE',report['hook_clearance_m'],flush=True)
for name,loc,target,scale in [('hook_side_detail',(8,1.0,4.55),(1.1,1.0,4.45),1.5),('root_detail',(6,-7,3),(1.25,-.9,.35),3.8),('perspective_preview',(9,-14,7.5),(0,0,2.5),6.9)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
