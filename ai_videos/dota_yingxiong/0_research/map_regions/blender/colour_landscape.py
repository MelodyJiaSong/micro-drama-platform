"""Set living grass albedo and retain the separate blighted biome."""
from pathlib import Path
import bpy,math,json
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';dest=OUT/'environment_v008.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v007.blend'))
nt=bpy.data.materials['Continuous_ground'].node_tree
for n in list(nt.nodes):
    if n.type!='TEX_IMAGE':continue
    name=n.image.name
    tint=(.22,.58,.12,1) if name in ['grass_ground_diff_2k.jpg','leafy_grass_diff_2k.jpg'] else (.55,.47,.37,1) if name=='brown_mud_02_diff_2k.jpg' else None
    if tint:
        old=[link.to_socket for link in n.outputs[0].links];mix=nt.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=tint;nt.links.new(n.outputs[0],mix.inputs[1])
        for socket in old:nt.links.new(mix.outputs[0],socket)
for node in bpy.context.scene.world.node_tree.nodes:
    if node.type=='TEX_SKY':node.sun_elevation=math.radians(42);node.air_density=1
bpy.context.scene['production_status']='ENVIRONMENT V008 CANDIDATE; living grass/blight colour separation'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest))
(OUT/'environment_v008_report.json').write_text(json.dumps({'file':dest.name,'status':'candidate_pending_review','changes':['Living grass shader calibration','Dirt reflectance calibration','Neutral daylight sun elevation 42 degrees'],'source':'environment_v007.blend','source_textures':'textures/sources.json'},indent=2))
