"""Address r38 root, frieze and mismatched round-hook review findings."""
from pathlib import Path
import bpy,json,sys,math,numpy as np
from mathutils import Vector,kdtree
from mathutils.geometry import closest_point_on_tri
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg23_*/model_3d'));out=folder/'r39';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r38/authoring.blend'));coll=bpy.data.collections['ASSET_bg23'];parent=bpy.data.objects['Asset_metre_calibration'];inverse=parent.matrix_world.inverted();bpy.context.view_layer.update()
ball=max((o for o in coll.objects if not o.hide_render and o.name.startswith('Reference_mirror_sphere')),key=lambda o:o.matrix_world.translation.z);center=inverse@ball.matrix_world.translation;radius=max((inverse@ball.matrix_world@v.co-center).length for v in ball.data.vertices)
start=center+Vector((0,0,-radius-.12));arc_center=center+Vector((0,radius+.10,.25));arc=[arc_center+Vector((.43*math.cos(a),0,.43*math.sin(a))) for a in np.linspace(0,math.radians(158),121)];b=start+Vector((.35,.08,.04));c=arc[0]+Vector((0,0,-.27));stem=[(1-t)**3*start+3*(1-t)**2*t*b+3*(1-t)*t*t*c+t**3*arc[0] for t in map(float,np.linspace(0,1,65))];points=stem+arc[1:];vertices=[];faces=[]
for j,p in enumerate(points):
 d=(points[min(j+1,len(points)-1)]-points[max(j-1,0)]).normalized();u=Vector((0,1,0));u=(u-d*u.dot(d)).normalized();v=d.cross(u).normalized()
 for a,b in [(-1,-1),(1,-1),(1,1),(-1,1)]:vertices.append(tuple(p+u*a*.045/2+v*b*.15/2))
for j in range(len(points)-1):
 for k in range(4):faces.append((j*4+k,j*4+(k+1)%4,(j+1)*4+(k+1)%4,(j+1)*4+k))
faces.extend([(3,2,1,0),tuple((len(points)-1)*4+k for k in range(4))]);me=bpy.data.meshes.new('Continuous_flat_question_hook');me.from_pydata(vertices,[],faces);me.update();hook=bpy.data.objects.new(me.name,me);coll.objects.link(hook);hook.parent=parent;me.materials.append(bpy.data.materials['Cast_bronze_with_verdigris']);be=hook.modifiers.new('Rounded_cast_edges','BEVEL');be.width=.004;be.segments=3
bpy.data.objects['Continuous_round_hook_and_cradle_return'].hide_render=True;bpy.data.objects['Continuous_round_hook_and_cradle_return'].hide_viewport=True;terminal=bpy.data.objects['Question_hook_terminal_ball'];terminal.location=points[-1];bpy.context.view_layer.update();me.calc_loop_triangles();gap=min((closest_point_on_tri(center,*[Vector(vertices[i]) for i in tri.vertices])-center).length-radius for tri in me.loop_triangles);assert gap>.005,('hook intersects globe',gap)
# Raise the root crown into a continuous taper, retaining buried distal tips.
primary=[];paths=[]
for ob in coll.objects:
 if ob.hide_render or not ob.name.startswith('Woven_pale_primary_root'):continue
 count=len(ob.data.vertices)//14;path=[]
 for j in range(count):
  vs=[ob.data.vertices[j*14+k] for k in range(14)];centre=sum((v.co for v in vs),Vector())/14;t=j/(count-1);new=centre.copy();new.z=.27*(1-t)**1.7+.035*math.sin(t*math.pi)-.105*t**5
  for v in vs:v.co=new+(v.co-centre)*(1.15-.1*t)
  primary.append(new);path.append(new)
 ob.data.update();paths.append(path)
tree=kdtree.KDTree(len(primary))
for i,p in enumerate(primary):tree.insert((p.x,p.y,0),i)
tree.balance()
for ob in coll.objects:
 if ob.hide_render or ob.type!='MESH' or not ob.name.startswith(('Connected_crossing_rootlet','Interwoven_circumferential_root')):continue
 count=len(ob.data.vertices)//14;origin=sum((ob.data.vertices[k].co for k in range(14)),Vector())/14;start=primary[tree.find((origin.x,origin.y,0))[1]]
 for j in range(count):
  vs=[ob.data.vertices[j*14+k] for k in range(14)];centre=sum((v.co for v in vs),Vector())/14;t=j/(count-1);new=centre.copy()
  if ob.name.startswith('Connected'):new.x+=(start.x-origin.x)*(1-t)**2;new.y+=(start.y-origin.y)*(1-t)**2;new.z=start.z*(1-t)+.025*math.sin(t*math.pi)-.08*t**5
  else:new.z=.04*math.sin(t*math.pi)-.065*(abs(t-.5)*2)**6
  for v in vs:v.co=new+(v.co-centre)
 ob.data.update()
for ob in coll.objects:
 if ob.hide_render or not ob.name.startswith('Small_irregular_root_soil_hummock'):continue
 centre=sum((v.co for v in ob.data.vertices),Vector())/len(ob.data.vertices)
 for v in ob.data.vertices:v.co.x=centre.x+(v.co.x-centre.x)*1.5;v.co.y=centre.y+(v.co.y-centre.y)*1.5;v.co.z=v.co.z*.32-.008
 ob.data.update()
bark=bpy.data.materials['Tileable_root_bark_actual_scale'];nt=bark.node_tree;bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');tex=next(n for n in nt.nodes if n.type=='TEX_IMAGE' and n.image and '_diff_' in n.image.name);gray=nt.nodes.new('ShaderNodeRGBToBW');nt.links.new(tex.outputs['Color'],gray.inputs[0]);ramp=nt.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.015;ramp.color_ramp.elements[0].color=(.06,.045,.030,1);ramp.color_ramp.elements[1].position=.30;ramp.color_ramp.elements[1].color=(.30,.245,.17,1);nt.links.new(gray.outputs[0],ramp.inputs[0]);nt.links.new(ramp.outputs[0],bs.inputs['Base Color'])
# Broaden the actual engraved grooves; preserve the closed two-layer topology.
def segment(x,z,a,b):
 dx,dz=b[0]-a[0],b[1]-a[1];t=max(0,min(1,((x-a[0])*dx+(z-a[1])*dz)/(dx*dx+dz*dz)));return math.hypot(x-a[0]-t*dx,z-a[1]-t*dz)
bands=sorted((o for o in coll.objects if o.name.startswith('Restored_closed_engraved_frieze') and not o.hide_render),key=lambda o:o.name)
for side,ob in enumerate(bands):
 phi=-math.pi/2+side*math.pi/4;n=Vector((math.cos(phi),math.sin(phi),0));tangent=Vector((-n.y,n.x,0))
 for v in list(ob.data.vertices)[:421*65]:
  x=v.co.dot(tangent);z=v.co.z;d=min(abs(z-2.378),abs(z-2.574))
  for center_x in [-.63,0,.63]:d=min(d,abs(math.hypot(x-center_x,z-2.476)-.067))
  for center_x in [-.315,.315]:
   p=[(center_x-.104,2.476),(center_x,2.536),(center_x+.104,2.476),(center_x,2.416),(center_x-.104,2.476)];d=min(d,*(segment(x,z,a,b) for a,b in zip(p,p[1:])))
  depth=.014*max(0,1-d/.010);v.co+=n*((2.42-depth)-v.co.dot(n))
 ob.data.update()
mat=bpy.data.materials['Grey_cyan_carved_stone'];nt=mat.node_tree;bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=55;ramp=nt.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.15,.20,.20,1);ramp.color_ramp.elements[1].color=(.35,.41,.40,1);nt.links.new(noise.outputs['Fac'],ramp.inputs[0]);nt.links.new(ramp.outputs[0],bs.inputs['Base Color']);bs.inputs['Roughness'].default_value=.82
report={'asset_id':'bg23','revision':'r39','source':'r38','status':'author_trial_pending_view','hook':{'section_parent_m':[.15,.045],'minimum_globe_gap_parent_m':gap,'method':'Flat band starts on existing support below cradle, continues behind globe into open hook'},'roots':{'primary_count':len(paths),'crown_height_parent_m':.27,'buried_tip_depth_parent_m':.105,'colour':'Single scanned-bark grayscale remap to medium pale brown'},'frieze':{'bands':len(bands),'carving_depth_parent_m':.014,'groove_half_width_parent_m':.010},'remaining':['Root contact and bark plausibility','Flat hook support connection','Frieze mid-distance readability','Independent review']}
scene=bpy.context.scene;scene['production_status']='REFERENCE_CAST_ROOT_FRIEZE_AUTHOR_TRIAL';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));(out/'authoring.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('SAVED',json.dumps(report),flush=True)
scene.cycles.device='CPU';scene.cycles.samples=32;scene.render.threads_mode='FIXED';scene.render.threads=6
for name,loc,target,scale in [('root_detail',(6,-7,3),(1.25,-.9,.35),3.8),('hook_side_detail',(8,1.0,4.55),(1.1,1.0,4.45),1.5),('perspective_preview',(9,-14,7.5),(0,0,2.5),6.9)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
