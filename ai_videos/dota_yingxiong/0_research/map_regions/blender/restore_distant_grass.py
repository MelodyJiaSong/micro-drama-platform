"""Retain near soil and account for grass culled beyond the camera LOD radius."""
from pathlib import Path
import bpy,json
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';dest=OUT/'environment_v016.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v015.blend'));nt=bpy.data.materials['Continuous_ground'].node_tree;changed=[]
for n in list(nt.nodes):
 if n.type!='MIX_RGB' or n.blend_type!='MULTIPLY' or not n.inputs[1].is_linked:continue
 source=n.inputs[1].links[0].from_node
 if source.type!='TEX_IMAGE' or not source.image or source.image.name!='grass_ground_diff_2k.jpg':continue
 camera=nt.nodes.new('ShaderNodeCameraData');distance=nt.nodes.new('ShaderNodeMapRange');distance.interpolation_type='SMOOTHSTEP';distance.clamp=True;distance.inputs['From Min'].default_value=60;distance.inputs['From Max'].default_value=140;nt.links.new(camera.outputs['View Distance'],distance.inputs['Value'])
 tint=nt.nodes.new('ShaderNodeMixRGB');tint.name='Grass_colour_beyond_geometry_LOD';tint.inputs[1].default_value=n.inputs[2].default_value;tint.inputs[2].default_value=(.14,.36,.055,1);nt.links.new(distance.outputs['Result'],tint.inputs[0]);nt.links.new(tint.outputs[0],n.inputs[2]);changed.append(n.name)
assert changed,'Grass material branch not found'
scene=bpy.context.scene;scene['production_status']='ENVIRONMENT V016 CANDIDATE; grass LOD colour pending visual review';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest))
report={'file':dest.name,'source':'environment_v015.blend','status':'candidate_pending_visual_inspection','geometry_and_navigation_changed':False,'changes':['Grass albedo smoothly includes distant grass coverage from 60 to 140 m camera distance; near soil and forest leaf litter unchanged'],'nodes':changed,'independent_review':False}
(OUT/'environment_v016_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
scene.cycles.device='CPU';scene.cycles.samples=32;scene.cycles.use_denoising=True;scene.render.resolution_x=1200;scene.render.resolution_y=900
for name in ['Map_Overview','Sentinel_Merchant_Ground_Eye']:
 camera=bpy.data.objects.get(name)
 if not camera:raise KeyError(name)
 scene.camera=camera;scene.render.filepath=str(OUT/f'environment_v016_{name}.png');bpy.ops.render.render(write_still=True)
