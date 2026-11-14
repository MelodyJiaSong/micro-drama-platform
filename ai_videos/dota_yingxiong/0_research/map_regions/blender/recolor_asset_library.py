"""按标准 A（follow-up 298：3D 作出片参考，形体／颜色分区／比例对即可）给单图生成模型重分色。

TRELLIS 贴图常见问题：整体发白发灰、叶子偏薄荷青、光照烘进漫反射。
这里不改几何与 UV，只在着色器里按像素色相／饱和度把贴图分成「植被」与「木石」两类，
分别重映射到资产卡的目标色，并把有机物金属度归零。另存新库文件，不改原库。

用法：blender -b -P recolor_asset_library.py -- --asset bg16 --src <库 blend> --profile tree_tower --version m1_recolor_v001
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
import bpy
from mathutils import Vector

DRAMA = Path(__file__).resolve().parents[3]
OUT = next(DRAMA.glob('2_*')) / 'background/map_3d'
REPO = DRAMA.parents[1]

# 目标色来自资产卡与锚点图（RGB 线性近似）
PROFILES = {
    # bg16 近卫防御塔：叶子橄榄绿到深绿、受光黄绿；木头风化灰褐
    'tree_tower': {
        'foliage_hue': (0.15, 0.62),   # 原贴图里被判为植被的色相区间（黄绿→青）
        'foliage_min_sat': 0.10,
        'leaf_hue': 0.22, 'leaf_hue_spread': 0.25, 'leaf_sat': (0.45, 0.75), 'leaf_value': 0.55,
        'wood_tint': (0.36, 0.28, 0.17), 'wood_value': 0.85,
    },
    # m3 投刃车：整车褪成同一浅黄褐，色相分不开；按明度分区——亮部鎏金黄铜、暗部深棕硬木
    'gold_wood': {
        'mode': 'value_split', 'split_percentiles': (22, 38),  # 按本贴图明度分位数定亮暗分界
        'dark_tint': (0.20, 0.11, 0.05), 'bright_tint': (0.95, 0.66, 0.24),
        'bright_metallic': 0.85, 'bright_roughness': 0.38, 'dark_roughness': 0.7,
    },
    # m2 利爪德鲁伊：正面颜色对，侧背褪成米白；只把低饱和偏亮像素压回深棕羽毛色，正面原色不动
    'washed_feather': {
        'mode': 'washed', 'max_sat': 0.20, 'min_value': 0.30,
        'target_tint': (0.36, 0.20, 0.09), 'target_value': 0.75,
    },
}

p = argparse.ArgumentParser()
p.add_argument('--asset', required=True)
p.add_argument('--src', required=True, help='相对仓库根或绝对路径')
p.add_argument('--profile', required=True, choices=PROFILES)
p.add_argument('--version', required=True)
args = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
prof = PROFILES[args.profile]
src = Path(args.src)
src = src if src.is_absolute() else REPO / src
folder = OUT / 'lod_libraries' / args.version / args.asset
folder.mkdir(parents=True, exist_ok=True)
dest = folder / f'{args.asset}.blend'
if dest.exists():
    raise FileExistsError(dest)

bpy.ops.wm.open_mainfile(filepath=str(src))
changed = []
for mat in bpy.data.materials:
    if not mat.use_nodes:
        continue
    nt = mat.node_tree
    bsdf = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    base = bsdf.inputs['Base Color'] if bsdf else None
    if not (base and base.is_linked and base.links[0].from_node.type == 'TEX_IMAGE'):
        continue
    tex = base.links[0].from_node
    N, L = nt.nodes.new, nt.links.new
    hsv = N('ShaderNodeSeparateColor'); hsv.mode = 'HSV'
    L(tex.outputs['Color'], hsv.inputs['Color'])
    h, s, v = hsv.outputs[0], hsv.outputs[1], hsv.outputs[2]

    def math_node(op, a, b=None, clamp=False):
        n = N('ShaderNodeMath'); n.operation = op; n.use_clamp = clamp
        (L(a, n.inputs[0]) if not isinstance(a, (int, float)) else n.inputs[0].__setattr__('default_value', a))
        if b is not None:
            (L(b, n.inputs[1]) if not isinstance(b, (int, float)) else n.inputs[1].__setattr__('default_value', b))
        return n.outputs[0]

    def ramp(x, lo, hi):
        n = N('ShaderNodeMapRange'); n.interpolation_type = 'SMOOTHSTEP'
        L(x, n.inputs['Value']); n.inputs['From Min'].default_value = lo; n.inputs['From Max'].default_value = hi
        return n.outputs['Result']

    def tinted(value_socket, tint, scale=2.2):
        gray = N('ShaderNodeCombineColor'); [L(value_socket, gray.inputs[i]) for i in range(3)]
        out = N('ShaderNodeMixRGB'); out.blend_type = 'MULTIPLY'; out.inputs['Fac'].default_value = 1.0
        out.inputs['Color2'].default_value = (*[c * scale for c in tint], 1.0)
        L(gray.outputs['Color'], out.inputs['Color1'])
        return out.outputs['Color']

    def set_input(name, value=None, socket=None):
        inp = bsdf.inputs[name]
        for link in list(inp.links):
            nt.links.remove(link)
        if socket is not None:
            L(socket, inp)
        else:
            inp.default_value = value

    mode = prof.get('mode', 'foliage_wood')
    if mode == 'value_split':
        import numpy as np
        px = np.empty(len(tex.image.pixels), dtype=np.float32); tex.image.pixels.foreach_get(px)
        px = px.reshape(-1, 4)
        px = px[px[:, 3] > 0.5][:, :3]
        val = px.max(1)  # HSV 明度
        val = val[val > 0.02]  # 去掉 UV 空白
        split = tuple(float(np.percentile(val, q)) for q in prof['split_percentiles'])
        prof = dict(prof, split=split)
        bright = ramp(v, *split)
        mix = N('ShaderNodeMixRGB'); mix.name = 'Recolor_gold_vs_wood'
        L(bright, mix.inputs['Fac'])
        L(tinted(math_node('MULTIPLY', v, 0.9), prof['dark_tint']), mix.inputs['Color1'])
        L(tinted(v, prof['bright_tint'], 1.0), mix.inputs['Color2'])
        L(mix.outputs['Color'], base)
        set_input('Metallic', socket=math_node('MULTIPLY', bright, prof['bright_metallic']))
        rough = N('ShaderNodeMapRange'); L(bright, rough.inputs['Value'])
        rough.inputs['To Min'].default_value, rough.inputs['To Max'].default_value = prof['dark_roughness'], prof['bright_roughness']
        set_input('Roughness', socket=rough.outputs['Result'])
    elif mode == 'washed':
        washed = math_node('MULTIPLY', math_node('SUBTRACT', 1.0, ramp(s, prof['max_sat'] - 0.06, prof['max_sat'] + 0.04)),
                           ramp(v, prof['min_value'] - 0.05, prof['min_value'] + 0.1), clamp=True)
        mix = N('ShaderNodeMixRGB'); mix.name = 'Recolor_restore_washed'
        L(washed, mix.inputs['Fac']); L(tex.outputs['Color'], mix.inputs['Color1'])
        L(tinted(math_node('MULTIPLY', v, prof['target_value']), prof['target_tint']), mix.inputs['Color2'])
        L(mix.outputs['Color'], base)
    else:
        lo, hi = prof['foliage_hue']
        in_hue = math_node('MULTIPLY', ramp(h, lo - 0.04, lo + 0.04), math_node('SUBTRACT', 1.0, ramp(h, hi - 0.04, hi + 0.04)))
        foliage = math_node('MULTIPLY', in_hue, ramp(s, prof['foliage_min_sat'] - 0.05, prof['foliage_min_sat'] + 0.08), clamp=True)

        # 植被：色相压到绿区，饱和度抬高，明度随原贴图
        centre = (lo + hi) / 2
        leaf_h = math_node('ADD', math_node('MULTIPLY', math_node('SUBTRACT', h, centre), prof['leaf_hue_spread']), prof['leaf_hue'])
        leaf_s = N('ShaderNodeMapRange'); L(s, leaf_s.inputs['Value'])
        leaf_s.inputs['To Min'].default_value, leaf_s.inputs['To Max'].default_value = prof['leaf_sat']
        leaf_v = math_node('MULTIPLY', v, prof['leaf_value'])
        leaf = N('ShaderNodeCombineColor'); leaf.mode = 'HSV'
        L(leaf_h, leaf.inputs[0]); L(leaf_s.outputs['Result'], leaf.inputs[1]); L(leaf_v, leaf.inputs[2])

        # 木石：去掉原色偏，按明度乘目标灰褐
        wood_v = math_node('MULTIPLY', v, prof['wood_value'])
        wood = N('ShaderNodeMixRGB'); wood.blend_type = 'MULTIPLY'; wood.inputs['Fac'].default_value = 1.0
        wood.inputs['Color2'].default_value = (*[c * 2.2 for c in prof['wood_tint']], 1.0)
        gray = N('ShaderNodeCombineColor'); [L(wood_v, gray.inputs[i]) for i in range(3)]
        L(gray.outputs['Color'], wood.inputs['Color1'])

        mix = N('ShaderNodeMixRGB'); mix.name = 'Recolor_foliage_vs_wood'
        L(foliage, mix.inputs['Fac']); L(wood.outputs['Color'], mix.inputs['Color1']); L(leaf.outputs['Color'], mix.inputs['Color2'])
        L(mix.outputs['Color'], base)
        met = bsdf.inputs['Metallic']
        for link in list(met.links):
            nt.links.remove(link)
        met.default_value = 0.0
    changed.append(mat.name)

if not changed:
    raise RuntimeError('没有可重着色的材质')

# 单体检查图：南／东／透视，工作室布光
scene = bpy.context.scene
# 库文件里的资产集合通常没挂在场景上；检查渲染时临时挂上，保存前摘掉
temp_links = [c for c in bpy.data.collections if c.name.startswith('ASSET_') and c.name not in scene.collection.children]
for c in temp_links:
    scene.collection.children.link(c)
asset_coll = bpy.data.collections[f'ASSET_{args.asset}']
objs = [o for o in asset_coll.all_objects if o.type == 'MESH']
hidden = [o for o in scene.objects if o.name not in asset_coll.all_objects and not o.hide_render]
for o in hidden:
    o.hide_render = True
# 用求值后的网格算范围：库内存的 bound_box／顶点与实际渲染尺寸可能不一致（bg16 记 1 m、渲染约 9 m）
dg = bpy.context.evaluated_depsgraph_get()
pts = []
for o in objs:
    ev = o.evaluated_get(dg)
    me = ev.to_mesh()
    pts += [ev.matrix_world @ v.co for i, v in enumerate(me.vertices) if i % 20 == 0]
    ev.to_mesh_clear()
lo_v = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
hi_v = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
centre_v, size = (lo_v + hi_v) / 2, max(hi_v - lo_v)
if not scene.world:
    scene.world = bpy.data.worlds.new('Check')
scene.world.use_nodes = True
bg = next(n for n in scene.world.node_tree.nodes if n.type == 'BACKGROUND')
bg.inputs['Strength'].default_value = 0.6
sun = bpy.data.objects.new('Check_sun', bpy.data.lights.new('Check_sun', 'SUN'))
sun.data.energy = 3.5; sun.rotation_euler = (math.radians(50), 0, math.radians(35)); scene.collection.objects.link(sun)
scene.render.engine = 'CYCLES'; scene.cycles.device = 'CPU'; scene.cycles.samples = 24; scene.cycles.use_denoising = True
scene.render.resolution_x = scene.render.resolution_y = 900
cam = bpy.data.objects.new('Check_cam', bpy.data.cameras.new('Check_cam')); scene.collection.objects.link(cam); scene.camera = cam
renders = []
for name, d in {'south': (0, -1, 0.25), 'east': (1, 0, 0.25), 'perspective': (0.7, -0.7, 0.45)}.items():
    cam.location = centre_v + Vector(d).normalized() * size * 2.1
    cam.rotation_euler = (centre_v - cam.location).to_track_quat('-Z', 'Y').to_euler()
    f = folder / f'recolor_{name}.png'; scene.render.filepath = str(f)
    bpy.ops.render.render(write_still=True); renders.append(f.name)
# 检查用的相机与灯不进库
for ob in (cam, sun):
    bpy.data.objects.remove(ob, do_unlink=True)
for c in temp_links:
    scene.collection.children.unlink(c)
for o in hidden:
    o.hide_render = False
bpy.ops.wm.save_as_mainfile(filepath=str(dest), relative_remap=True)
sha = lambda f: hashlib.sha256(Path(f).read_bytes()).hexdigest()
(folder / 'recolor_report.json').write_text(json.dumps({
    'followup': 298, 'asset': args.asset, 'profile': args.profile, 'params': prof,
    'source': str(src.relative_to(REPO)) if src.is_relative_to(REPO) else str(src), 'source_sha256': sha(src),
    'output': str(dest.relative_to(REPO)), 'output_sha256': sha(dest), 'materials': changed,
    'unchanged': ['几何', 'UV', '原贴图像素', '原库文件'], 'renders': renders,
    'standard': 'A：出片参考，颜色分区与资产卡一致即可；不等于精模验收',
}, ensure_ascii=False, indent=2), encoding='utf-8')
print('RECOLOR_SAVED', dest, flush=True)
