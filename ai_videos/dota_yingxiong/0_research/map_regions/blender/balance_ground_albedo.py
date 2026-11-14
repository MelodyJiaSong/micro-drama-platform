"""Restore scanned soil/grass colour and reduce oversized shader bump relief."""
from pathlib import Path
import bpy,json,sys
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';dest=OUT/'environment_v014.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v013.blend'));nt=bpy.data.materials['Continuous_ground'].node_tree;changed=[]
for n in nt.nodes:
 if n.type=='MIX_RGB' and n.blend_type=='MULTIPLY' and n.inputs[1].is_linked:
  source=n.inputs[1].links[0].from_node
  if source.type=='TEX_IMAGE' and source.image and source.image.name in ['grass_ground_diff_2k.jpg','leafy_grass_diff_2k.jpg']:
   changed.append({'node':n.name,'old_factor':n.inputs[0].default_value,'old_tint':list(n.inputs[2].default_value)})
   n.inputs[0].default_value=.28;n.inputs[2].default_value=(.75,.95,.62,1)
 if n.type=='BUMP' and n.inputs['Distance'].default_value>.11:
  changed.append({'node':n.name,'old_bump_distance':n.inputs['Distance'].default_value});n.inputs['Distance'].default_value=.028
assert len(changed)>=2,changed
scene=bpy.context.scene;scene['production_status']='ENVIRONMENT V014 CANDIDATE; soil albedo correction pending visual review'
data=bpy.data.cameras.new('Sentinel_Merchant_Ground_Eye');camera=bpy.data.objects.new(data.name,data);scene.collection.objects.link(camera);camera.location=(-355.7,-326.8,5.508);look_at(camera,(-356.8,-324.75,4.578));data.lens=48;data.clip_start=.02;data.clip_end=3000
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest))
(OUT/'environment_v014_report.json').write_text(json.dumps({'file':dest.name,'source':'environment_v013.blend','status':'candidate_pending_visual_inspection','changes':changed,'geometry_and_navigation_changed':False,'reason':'Actual-map close-up showed pale green clay-like soil; restore more original scanned ground reflectance'},indent=2),encoding='utf-8')
scene.camera=camera;scene.cycles.device='CPU';scene.cycles.samples=32;scene.cycles.use_denoising=True;scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene.render.filepath=str(OUT/'environment_v014_Merchant_Ground.png');bpy.ops.render.render(write_still=True)
