"""Apply downloaded CC0 scanned materials and pack them into the working scene."""
import json
from pathlib import Path
import bpy

ROOT=Path(__file__).resolve().parents[3]
OUT=next(ROOT.glob('2_*'))/'background/map_3d'
TEX=OUT/'textures'
dest=OUT/'environment_v005.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v004.blend'))
sources=json.loads((TEX/'sources.json').read_text())
files={(r['asset'],r['map']):TEX/r['path'] for r in sources}


def sampled(nt,asset,coord,scale=0.5,box=False):
    n,l=nt.nodes,nt.links
    mapping=n.new('ShaderNodeVectorMath');mapping.operation='SCALE';mapping.inputs[3].default_value=scale;l.new(coord,mapping.inputs[0])
    output={}
    for kind in ('Diffuse','Rough','Displacement'):
        node=n.new('ShaderNodeTexImage');node.image=bpy.data.images.load(str(files[(asset,kind)]),check_existing=True)
        if kind!='Diffuse':node.image.colorspace_settings.name='Non-Color'
        if box:node.projection='BOX';node.projection_blend=.28
        l.new(mapping.outputs['Vector'],node.inputs['Vector']);output[kind]=node.outputs['Color']
    return output


def mix(nt,a,b,factor):
    node=nt.nodes.new('ShaderNodeMixRGB');nt.links.new(a,node.inputs[1]);nt.links.new(b,node.inputs[2]);nt.links.new(factor,node.inputs[0]);return node.outputs[0]


terrain=bpy.data.materials['Continuous_ground'];nt=terrain.node_tree;n,l=nt.nodes,nt.links;n.clear()
out=n.new('ShaderNodeOutputMaterial');bsdf=n.new('ShaderNodeBsdfPrincipled');l.new(bsdf.outputs[0],out.inputs['Surface'])
tc=n.new('ShaderNodeTexCoord');coord=tc.outputs['Object']
soil=sampled(nt,'brown_mud_02',coord,.45,True)
forest=sampled(nt,'forest_ground_04',coord,.4,True)
rock=sampled(nt,'rocky_terrain',coord,.27,True)
moss=sampled(nt,'mossy_rock',coord,.36,True)
# Separate low-frequency biome masks from metre-scale scanned texture.
def attr(name):
    node=n.new('ShaderNodeAttribute');node.attribute_name=name;return node.outputs['Fac']
grass,blight,cliff,paving=attr('Grass'),attr('Blight'),attr('Rock'),attr('Paving')
green=n.new('ShaderNodeMixRGB');green.blend_type='MULTIPLY';green.inputs[0].default_value=.62;green.inputs[2].default_value=(.40,.67,.20,1);l.new(forest['Diffuse'],green.inputs[1])
ash=n.new('ShaderNodeHueSaturation');ash.inputs['Saturation'].default_value=.25;ash.inputs['Value'].default_value=.34;l.new(rock['Diffuse'],ash.inputs['Color'])
color=mix(nt,soil['Diffuse'],green.outputs[0],grass);color=mix(nt,color,ash.outputs[0],blight);color=mix(nt,color,moss['Diffuse'],cliff)
l.new(color,bsdf.inputs['Base Color'])
rough=mix(nt,soil['Rough'],forest['Rough'],grass);rough=mix(nt,rough,moss['Rough'],cliff);l.new(rough,bsdf.inputs['Roughness'])
height=mix(nt,soil['Displacement'],forest['Displacement'],grass);height=mix(nt,height,moss['Displacement'],cliff)
bump=n.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.11;bump.inputs['Strength'].default_value=.8;l.new(height,bump.inputs['Height']);l.new(bump.outputs['Normal'],bsdf.inputs['Normal'])

for material_name,asset,scale in [('Grey_limestone','mossy_rock',.55),('Basalt','rocky_terrain',.6)]:
    mat=bpy.data.materials[material_name];nt=mat.node_tree;n,l=nt.nodes,nt.links;bs=n.get('Principled BSDF');tc=n.new('ShaderNodeTexCoord')
    maps=sampled(nt,asset,tc.outputs['Object'],scale,True)
    dark=n.new('ShaderNodeMixRGB');dark.blend_type='MULTIPLY';dark.inputs[0].default_value=1;dark.inputs[2].default_value=(.38,.40,.38,1);l.new(maps['Diffuse'],dark.inputs[1]);l.new(dark.outputs[0],bs.inputs['Base Color']);l.new(maps['Rough'],bs.inputs['Roughness'])
    bump=n.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.08;bump.inputs['Strength'].default_value=.8;l.new(maps['Displacement'],bump.inputs['Height']);l.new(bump.outputs[0],bs.inputs['Normal'])
for obj in bpy.data.collections['07_Cliff_Relief'].objects:
    obj.scale.x*=1.7;obj.scale.y*=1.5;obj.scale.z*=2.4;obj.location.z-=1.0
for node in bpy.data.materials['Low_density_day_haze'].node_tree.nodes:
    if node.type=='VOLUME_SCATTER':node.inputs['Density'].default_value=.00010
# Add a useful eye-level inspection camera, not only the overhead view.
from mathutils import Vector
cam=bpy.data.cameras.new('River_Eye_Level');obj=bpy.data.objects.new('River_Eye_Level',cam);bpy.context.scene.collection.objects.link(obj)
obj.location=(-31,-56,1.5);obj.rotation_euler=(Vector((15,12,-2))-obj.location).to_track_quat('-Z','Y').to_euler();cam.lens=28;cam.clip_end=2500
bpy.context.scene['production_status']='ENVIRONMENT V005 CANDIDATE; scanned ground materials; final review pending'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest))
(OUT/'environment_v005_report.json').write_text(json.dumps({'file':dest.name,'packed_maps':len(sources),'license':'CC0','source_manifest':'textures/sources.json','status':'candidate_pending_review'},indent=2),encoding='utf-8')
print('SAVED',dest,flush=True)
