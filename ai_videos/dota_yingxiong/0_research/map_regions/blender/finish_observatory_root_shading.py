"""Correct dark linear scan remapping and soften the orderly root trajectories."""
from pathlib import Path
import bpy,json,sys,math
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg23_*/model_3d'));out=folder/'r25';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r24/authoring.blend'));coll=bpy.data.collections['ASSET_bg23'];mat=bpy.data.materials['Pale_living_aerial_root_bark']
for n in mat.node_tree.nodes:
 if n.type=='VALTORGB':n.color_ramp.elements[0].position=.008;n.color_ramp.elements[0].color=(.075,.05,.027,1);n.color_ramp.elements[1].position=.16;n.color_ramp.elements[1].color=(.40,.29,.17,1)
roots=0
for ob in coll.objects:
 if not ob.name.startswith(('Woven_pale_primary_root','Connected_crossing_rootlet','Interwoven_circumferential_root')):continue
 me=ob.data;points=[sum((me.vertices[j*14+k].co for k in range(14)),Vector())/14 for j in range(len(me.vertices)//14)]
 for j,p in enumerate(points):
  r=math.hypot(p.x,p.y);weight=max(0,min(1,(r-2.37)/.28));dx=.07*math.sin(p.x*5.7+p.y*2.9)+.025*math.sin(p.y*11);dy=.07*math.sin(p.y*6.1-p.x*3.3)+.025*math.cos(p.x*10);dz=.025*math.sin(p.x*9+p.y*7)*max(0,min(1,p.z/.05));delta=Vector((dx,dy,dz))*weight
  for k in range(14):me.vertices[j*14+k].co+=delta
 me.update();roots+=1
scene=bpy.context.scene;scene.cycles.samples=48;scene.cycles.device='CPU';scene.render.threads_mode='FIXED';scene.render.threads=8;scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene.camera.location=(9,-14,7.5);scene.camera.data.ortho_scale=6.7;look_at(scene.camera,(0,0,2.4));scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'bg23','revision':'r25','source':'r24','status':'author_preview_not_accepted','changes':['Remap linear scanned albedo to pale warm root bark','Small spatially coherent root bends preserve coincident branch attachment coordinates'],'roots':roots,'remaining':['Appearance of roots against ground','Multi-angle independent review']},indent=2),encoding='utf-8')
scene.render.filepath=str(out/'perspective_preview.png');bpy.ops.render.render(write_still=True)
scene.camera.location=(6,-7,3);scene.camera.data.ortho_scale=3.8;look_at(scene.camera,(1.25,-.9,.35));scene.render.filepath=str(out/'root_detail.png');bpy.ops.render.render(write_still=True)
