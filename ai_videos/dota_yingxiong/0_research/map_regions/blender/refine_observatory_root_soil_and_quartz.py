"""Correct r46 author-visible material and soil-footprint problems before QC."""
from pathlib import Path
import bpy,json,sys,math,random
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg23_*/model_3d'));out=folder/'r47';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r46/authoring.blend'));coll=bpy.data.collections['ASSET_bg23'];rng=random.Random(2347)
soil=bpy.data.objects['Continuous_root_soil_bed']
for v in soil.data.vertices:
 a=math.atan2(v.co.y,v.co.x);wall=2.39/math.cos((a+math.pi/8)%(math.pi/4)-math.pi/8);r=math.hypot(v.co.x,v.co.y);rad=wall+(r-wall)*1.6
 v.co.x=rad*math.cos(a);v.co.y=rad*math.sin(a)
 if v.co.z>0:v.co.z*=1.3
soil.data.update()
mat=bpy.data.materials['Weathered_connected_root_bark_r46'];nt=mat.node_tree;bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');old=bs.inputs['Base Color'].links[0].from_socket
tint=nt.nodes.new('ShaderNodeMixRGB');tint.blend_type='MULTIPLY';tint.inputs[0].default_value=1;tint.inputs[2].default_value=(1.26,1.02,.73,1);nt.links.new(old,tint.inputs[1]);nt.links.new(tint.outputs[0],bs.inputs['Base Color'])
# Break the cylindrical silhouette into gentle longitudinal ridges without pointed stubs.
for ob in coll.objects:
 if not ob.name.startswith(('Continuous_forest_primary_root','Continuous_forest_branch')):continue
 for j in range(len(ob.data.vertices)//16):
  ring=[ob.data.vertices[j*16+k] for k in range(16)];center=sum((v.co for v in ring),Vector())/16
  for k,v in enumerate(ring):
   d=v.co-center;v.co=center+d*(1+.10*math.sin(k*math.tau/16*3+j*.12)+.04*math.sin(j*.49+k))
 ob.data.update()
for mat in bpy.data.materials:
 if not mat.name.startswith('Inset_quartz_amethyst_'):continue
 nt=mat.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.75,.70,.83,1);bs.inputs['Transmission Weight'].default_value=.9;bs.inputs['Roughness'].default_value=.15;bs.inputs['IOR'].default_value=1.54
 for node in nt.nodes:
  if node.type=='VOLUME_ABSORPTION':node.inputs['Color'].default_value=(.60,.16,.80,1);node.inputs['Density'].default_value=4
 noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=240;noise.inputs['Detail'].default_value=2;bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.00015;bump.inputs['Strength'].default_value=.12;nt.links.new(noise.outputs['Fac'],bump.inputs['Height']);nt.links.new(bump.outputs['Normal'],bs.inputs['Normal'])
# Retain patch gaps instead of creating a level, uniform band of ivy.
hidden=0
for ob in coll.objects:
 if not ob.name.startswith('Clustered_wall_contact_ivy'):continue
 p=ob.location;angle=math.atan2(p.y,p.x);mask=math.sin(angle*21+p.z*8)+.55*math.cos(angle*37-p.z*13)
 if mask>.55:ob.hide_render=True;ob.hide_viewport=True;hidden+=1
scene=bpy.context.scene;scene['production_status']='R47_GROUND_AND_QUARTZ_AUTHOR_TRIAL';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
report=json.loads((folder/'r46/authoring.json').read_text());report.update(revision='r47',source='r46',status='author_trial_pending_view',r47_changes={'soil_radial_extension':1.6,'soil_positive_relief_scale':1.3,'roots':'Warm photographic bark multiplication and irregular longitudinal profile','quartz':'90% transmission, IOR 1.54, purple volume absorption, microscopic surface texture','ivy_leaves_hidden_for_patch_gaps':hidden});(out/'authoring.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('R47_SAVED',flush=True)
scene.cycles.device='CPU';scene.cycles.samples=48;scene.render.threads_mode='FIXED';scene.render.threads=6
for name,loc,target,scale in [('root_detail',(6,-7,3),(1.25,-.9,.35),3.8),('perspective_preview',(9,-14,7.5),(0,0,2.5),6.9)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
