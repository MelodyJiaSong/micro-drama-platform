"""Repair the measured hook gap and the four visible r28 review defects."""
from pathlib import Path
import bpy,json,sys,math
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg23_*/model_3d'));out=folder/'r29';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r28/authoring.blend'));coll=bpy.data.collections['ASSET_bg23'];parent=bpy.data.objects['Asset_metre_calibration'];bronze=bpy.data.materials['Cast_bronze_with_verdigris'];brass=bpy.data.materials['Polished_worn_brass']
def box(name,loc,size,mat):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);ob=bpy.context.object
 for c in list(ob.users_collection):c.objects.unlink(ob)
 coll.objects.link(ob);ob.parent=parent;ob.name=name;ob.scale=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);ob.data.materials.append(mat);b=ob.modifiers.new('Cast_edge_radius','BEVEL');b.width=.006;b.segments=3;return ob
# Probe: globe cradle centre (1.20,.95,4.685), hook stem (1.20,1.27,4.680).
# A physical rearward cantilever under the globe bridges the 32cm offset.
box('Hook_to_globe_cradle_structural_bracket',(1.20,1.105,4.68),(.115,.39,.075),bronze)
for y in [.96,1.265]:
 box('Bracket_cast_attachment_lug',(1.20,y,4.68),(.15,.075,.115),bronze)
 bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,radius=.023,location=(1.20,y,4.747));ob=bpy.context.object
 for c in list(ob.users_collection):c.objects.unlink(ob)
 coll.objects.link(ob);ob.parent=parent;ob.name='Bracket_visible_rivet';ob.scale.z=.35;ob.data.materials.append(brass)
soil=bpy.data.objects.get('Irregular_root_soil_collar')
if soil:soil.hide_render=True;soil.hide_viewport=True
mat=bpy.data.materials['Tileable_root_bark_actual_scale'];nt=mat.node_tree;n,l=nt.nodes,nt.links;bs=next(q for q in n if q.type=='BSDF_PRINCIPLED');tex=next(q for q in n if q.type=='TEX_IMAGE' and q.image and '_diff_' in q.image.name);gray=n.new('ShaderNodeRGBToBW');l.new(tex.outputs['Color'],gray.inputs[0]);ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.015;ramp.color_ramp.elements[0].color=(.055,.050,.038,1);ramp.color_ramp.elements[1].position=.45;ramp.color_ramp.elements[1].color=(.25,.23,.18,1);l.new(gray.outputs[0],ramp.inputs[0]);l.new(ramp.outputs[0],bs.inputs['Base Color']);bs.inputs['Specular IOR Level'].default_value=.12
def warp(p):
 t=max(0,min(1,(p.z+.03)/.30));p.z-=.22*t*t*(3-2*t)
 if p.y<-2.25 and abs(p.x)<.86:p.x=math.copysign(.86+(abs(p.x)/.86)*.08,p.x)
 return p
changed=[]
for ob in coll.objects:
 if ob.hide_render:continue
 if ob.type=='MESH' and ob.name.startswith(('Woven_pale_primary_root','Connected_crossing_rootlet','Interwoven_circumferential_root')):
  me=ob.data
  if ob.name.startswith('Woven_pale_primary_root'):
   for j in range(len(me.vertices)//14):
    center=sum((me.vertices[j*14+k].co for k in range(14)),Vector())/14
    for k in range(14):v=me.vertices[j*14+k];v.co=center+(v.co-center)*.66
  for v in me.vertices:v.co=warp(v.co)
  me.update();changed.append(ob.name)
 elif ob.type=='CURVE' and ob.name.startswith('Fine_feeder_root'):
  for sp in ob.data.splines:
   for p in sp.points:p.co=(*warp(p.co.xyz),p.co.w)
 elif ob.name.startswith('Dense_base_fern_skirt'):ob.scale*=.82
scene=bpy.context.scene;scene.cycles.samples=48;scene.cycles.device='CPU';scene.render.threads_mode='FIXED';scene.render.threads=8;scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'bg23','revision':'r29','source':'r28','status':'author_preview_not_accepted','changes':['Measured 32cm rearward hook gap bridged by cast bracket with attachment lugs and visible rivets','Hide rejected hard-edged soil collar','Lower root web below crystal openings and keep entrance corridor clear','Thinner primary roots with pale gray-brown scanned bark; expose more root network'],'root_meshes_changed':len(changed),'bracket_end_centres_parent':[[1.2,.95,4.685],[1.2,1.27,4.68]],'remaining':['Side-view hook support contact','Root/crystal/stair clearance','Natural root colour and ground transition','Independent review']},indent=2),encoding='utf-8')
for name,loc,target,scale in [('perspective_preview',(9,-14,7.5),(0,0,2.5),6.9),('root_detail',(6,-7,3),(1.25,-.9,.35),3.8),('hook_side_detail',(8,1.0,4.55),(1.1,1.0,4.45),1.5)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
