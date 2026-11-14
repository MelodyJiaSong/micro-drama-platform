"""Address r34's three material/structure blockers with actual relief and roots."""
from pathlib import Path
import bpy,json,math,random,sys
from mathutils import Vector,kdtree
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg23_*/model_3d'));out=folder/'r35';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r34/inspection/bg23_r34.blend'));coll=bpy.data.collections['ASSET_bg23'];parent=bpy.data.objects['Asset_metre_calibration'];rng=random.Random(2335);primary=[];stats={'blocks':0,'recessed_backing':0,'primary_roots':0,'rootlets':0,'bronze_relief_curves':0}
for ob in coll.objects:
 if ob.hide_render or ob.type!='MESH':continue
 if ob.name.startswith(('Staggered_limestone_block','Continuous_lime_backing')):
  center=sum((v.co for v in ob.data.vertices),Vector())/len(ob.data.vertices);angle=round(math.atan2(center.y,center.x)/(math.pi/4))*math.pi/4;n=Vector((math.cos(angle),math.sin(angle),0));dots=[v.co.dot(n) for v in ob.data.vertices];limit=(min(dots)+max(dots))*.5
  shift=rng.uniform(.016,.046) if ob.name.startswith('Staggered') else -.055
  for v in ob.data.vertices:
   if v.co.dot(n)>limit:v.co+=n*shift
  for mod in ob.modifiers:
   if mod.type=='BEVEL':mod.width=rng.uniform(.011,.019);mod.segments=3
  ob.data.update();stats['blocks' if ob.name.startswith('Staggered') else 'recessed_backing']+=1
 if ob.name.startswith('Woven_pale_primary_root'):
  count=len(ob.data.vertices)//14
  for j in range(count):
   vertices=[ob.data.vertices[j*14+k] for k in range(14)];center=sum((v.co for v in vertices),Vector())/14;t=j/(count-1);target=.59*(1-t)**3+.075*(1-t**5)-.08*t**8;new=Vector((center.x,center.y,target));factor=1.65-.35*t
   for v in vertices:v.co=new+(v.co-center)*factor
   primary.append(new)
  ob.data.update();stats['primary_roots']+=1
tree=kdtree.KDTree(len(primary))
for i,p in enumerate(primary):tree.insert(Vector((p.x,p.y,0)),i)
tree.balance()
for ob in coll.objects:
 if ob.hide_render or ob.type!='MESH':continue
 if ob.name.startswith(('Connected_crossing_rootlet','Interwoven_circumferential_root')):
  count=len(ob.data.vertices)//14;first=sum((ob.data.vertices[k].co for k in range(14)),Vector())/14;start=primary[tree.find(Vector((first.x,first.y,0)))[1]].z
  for j in range(count):
   vertices=[ob.data.vertices[j*14+k] for k in range(14)];center=sum((v.co for v in vertices),Vector())/14;t=j/(count-1)
   target=start*(1-t)+.065*math.sin(t*math.pi)-.06*t**7 if ob.name.startswith('Connected') else .10*math.sin(t*math.pi)+.03*math.sin(t*12)**2-.035*(abs(t-.5)*2)**8
   new=Vector((center.x,center.y,target))
   for v in vertices:v.co=new+(v.co-center)*1.35
  ob.data.update();stats['rootlets']+=1
 elif ob.name.startswith('Small_irregular_root_soil_hummock'):
  for v in ob.data.vertices:
   if v.co.z>0:v.co.z*=2.8
  ob.data.update()
# Final-node remapping preserves bark texture at its verified physical scale.
rootmats={m for ob in coll.objects if not ob.hide_render and ob.name.startswith(('Woven_pale','Connected_crossing','Interwoven_circumferential','Fine_feeder')) for m in ob.data.materials if m}
for mat in rootmats:
 nt=mat.node_tree;bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');source=bs.inputs['Base Color'].links[0].from_socket;gray=nt.nodes.new('ShaderNodeRGBToBW');nt.links.new(source,gray.inputs[0]);ramp=nt.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.015;ramp.color_ramp.elements[0].color=(.17,.135,.09,1);ramp.color_ramp.elements[1].position=.25;ramp.color_ramp.elements[1].color=(.58,.48,.32,1);nt.links.new(gray.outputs[0],ramp.inputs[0]);nt.links.new(ramp.outputs[0],bs.inputs['Base Color']);bs.inputs['Specular IOR Level'].default_value=.12
for name in ['Weathered_white_limestone','Limestone_capstones']:
 mat=bpy.data.materials.get(name)
 if not mat:continue
 nt=mat.node_tree;bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');source=bs.inputs['Base Color'].links[0].from_socket if bs.inputs['Base Color'].is_linked else None
 if source:
  hsv=nt.nodes.new('ShaderNodeHueSaturation');hsv.inputs['Saturation'].default_value=.40;hsv.inputs['Value'].default_value=1.12;nt.links.new(source,hsv.inputs['Color']);mix=nt.nodes.new('ShaderNodeMixRGB');mix.inputs[0].default_value=.16;mix.inputs[2].default_value=(.66,.60,.48,1);nt.links.new(hsv.outputs[0],mix.inputs[1]);nt.links.new(mix.outputs[0],bs.inputs['Base Color'])
 bs.inputs['Specular IOR Level'].default_value=.16
# Share the bronze alloy with the dome: the relief is cast into the same metal,
# with a broader rounded section, instead of a saturated gold wire overlay.
bronze=bpy.data.materials['Cast_bronze_with_verdigris'];cu=bpy.data.curves.new('Broader_cast_relief_profile','CURVE');cu.dimensions='2D';sp=cu.splines.new('POLY');sp.points.add(31);sp.use_cyclic_u=True
for k,p in enumerate(sp.points):a=k*math.tau/32;p.co=(.022*math.cos(a),.009*math.sin(a),0,1)
profile=bpy.data.objects.new('Hidden_broader_cast_profile',cu);coll.objects.link(profile);profile.hide_render=True
for ob in coll.objects:
 if ob.hide_render or ob.type!='CURVE' or not ob.name.startswith(('Concentric_cast_relief','Cast_spiral_relief','Fine_cast_volute')):continue
 ob.data.materials.clear();ob.data.materials.append(bronze);ob.data.bevel_mode='OBJECT';ob.data.bevel_object=profile;ob.data.twist_mode='Z_UP';stats['bronze_relief_curves']+=1
scene=bpy.context.scene;scene['production_status']='R34_THREE_BLOCKER_REPAIR_AUTHOR_TRIAL_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));(out/'authoring.json').write_text(json.dumps({'asset_id':'bg23','revision':'r35','source':'r34 inspection','status':'author_trial_pending_view','changes':stats,'masonry':'Actual outer stone faces advanced 16–46mm; lime backing recessed 55mm; 11–19mm worn bevels; cream limestone tint','roots':'Primary collar begins at 0.665m parent height, thicker branching sections, pale textured bark and visible local soil mounds','roof':'Existing spirals and rings retain shape; same bronze alloy as dome with broader 22x9mm half-section','remaining':['Root crossing and ground contact','Raised relief casting readability','Stone joint depth and material naturalness','Independent review']},indent=2),encoding='utf-8');print('THREE_BLOCKER_REPAIR_SAVED',json.dumps(stats),flush=True)
scene.cycles.device='CPU';scene.cycles.samples=32;scene.render.threads_mode='FIXED';scene.render.threads=6
for name,loc,target,scale in [('root_detail',(6,-7,3),(1.25,-.9,.35),3.8),('roof_detail',(4,-6,8),(0,0,3),5.7),('perspective_preview',(9,-14,7.5),(0,0,2.5),6.9)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
