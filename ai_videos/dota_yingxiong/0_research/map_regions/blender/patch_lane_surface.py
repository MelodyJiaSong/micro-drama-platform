"""兵道路面从白砂岩石块改为夯土（follow-up 298）。

设定（battlefield.md 兵道行、bg4 卡）：近卫侧土黄夯土路，天灾侧黑褐泥路。
原 Paving 分支 = white_sandstone 贴图 × 灰色，读成水泥／石板路。
这里把该分支的颜色换成 brown_mud 贴图 × (按 Blight 在土黄与黑褐之间混) × 低频踩痕噪声；
遮罩、其他地表、粗糙度与法线不动。只另存新文件，不改源 blend。

用法：blender -b -P patch_lane_surface.py -- --src assembly_working_v022_lod_v004.blend --dst <新文件名>
"""
from pathlib import Path
import argparse, json, sys
import bpy

DRAMA = Path(__file__).resolve().parents[3]
OUT = next(DRAMA.glob('2_*')) / 'background/map_3d'
p = argparse.ArgumentParser()
p.add_argument('--src', default='assembly_working_v022_lod_v004.blend')
p.add_argument('--dst', required=True)
args = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
dest = OUT / args.dst
if dest.exists():
    raise FileExistsError(dest)

SENTINEL_EARTH = (0.42, 0.33, 0.20, 1.0)  # 土黄夯土（乘在 brown_mud 漫反射上）
SCOURGE_MUD = (0.16, 0.12, 0.09, 1.0)     # 黑褐泥

bpy.ops.wm.open_mainfile(filepath=str(OUT / args.src))
mat = bpy.data.materials['Continuous_ground']
if mat.library:
    mat = mat.make_local()
nt = mat.node_tree
nodes, links = nt.nodes, nt.links
sand = nodes['Image Texture.013']
tint = nodes['Mix (Legacy).010']  # sand × 灰
if not (sand.image and 'sandstone' in sand.image.name):
    raise RuntimeError(('Paving 分支结构已变，停止', sand.image.name if sand.image else None))
mud_img = next(n.image for n in nodes if n.type == 'TEX_IMAGE' and n.image and n.image.name.startswith('brown_mud_02_diff'))
sand.image = mud_img  # 同一组坐标（Vector Math.004，0.5 缩放）采样泥土

side = nodes.new('ShaderNodeAttribute'); side.attribute_name = 'Blight'; side.name = 'Lane_side_blight'
side_mix = nodes.new('ShaderNodeMixRGB'); side_mix.name = 'Lane_earth_by_side'
side_mix.inputs['Color1'].default_value = SENTINEL_EARTH
side_mix.inputs['Color2'].default_value = SCOURGE_MUD
links.new(side.outputs['Fac'], side_mix.inputs['Fac'])

coord = nodes.new('ShaderNodeTexCoord')
wear = nodes.new('ShaderNodeTexNoise'); wear.name = 'Lane_wear_noise'
wear.inputs['Scale'].default_value = 0.35
wear.inputs['Detail'].default_value = 6.0
links.new(coord.outputs['Object'], wear.inputs['Vector'])
wear_ramp = nodes.new('ShaderNodeMapRange'); wear_ramp.name = 'Lane_wear_range'
wear_ramp.inputs['From Min'].default_value = 0.35
wear_ramp.inputs['From Max'].default_value = 0.65
wear_ramp.inputs['To Min'].default_value = 0.75
wear_ramp.inputs['To Max'].default_value = 1.15
links.new(wear.outputs['Fac'], wear_ramp.inputs['Value'])
wear_mul = nodes.new('ShaderNodeMixRGB'); wear_mul.blend_type = 'MULTIPLY'; wear_mul.name = 'Lane_wear_apply'
wear_mul.inputs['Fac'].default_value = 1.0
links.new(side_mix.outputs['Color'], wear_mul.inputs['Color1'])
links.new(wear_ramp.outputs['Result'], wear_mul.inputs['Color2'])
# 原来 Color2 是固定灰；改接 土色 × 踩痕
links.new(wear_mul.outputs['Color'], tint.inputs['Color2'])

bpy.context.scene['lane_surface_patch'] = 'followup 298: Paving sandstone → packed earth (sentinel yellow / scourge black-brown)'
bpy.ops.wm.save_as_mainfile(filepath=str(dest), relative_remap=True)
(OUT / f'{dest.stem}_report.json').write_text(json.dumps({
    'followup': 298, 'source': args.src, 'file': dest.name,
    'change': 'Continuous_ground 材质 Paving 分支：white_sandstone → brown_mud × 按 Blight 混合的土黄/黑褐 × 踩痕噪声',
    'sentinel_earth': SENTINEL_EARTH, 'scourge_mud': SCOURGE_MUD,
    'unchanged': ['遮罩与混合权重', '其他地表层', '粗糙度与法线', '所有模型与摆放'],
    'status': 'DRAFT_REFERENCE_FOR_VIDEO（用户 298 定标准 A：3D 作出片参考）',
}, ensure_ascii=False, indent=2), encoding='utf-8')
print('LANE_PATCH_SAVED', dest, flush=True)
