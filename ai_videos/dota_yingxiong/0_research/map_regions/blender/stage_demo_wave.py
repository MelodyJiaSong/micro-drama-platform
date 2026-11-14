"""在区域里摆 demo 编成：英雄占位＋来兵（follow-up 298，按 battlefield.md §2.2、§4.2）。

只加新对象（集合 DEMO_<region>），不动原有摆放；另存新总装。
坐标为总装米制（= 6.83d 游戏坐标 / 20），朝向约定：模型正面 −Y，rotation_z=θ 时朝 (sinθ, −cosθ)。
用法：blender -b -P stage_demo_wave.py -- --src <总装> --dst <新总装> --region M1
"""
from pathlib import Path
import argparse, json, math, sys
import bpy
from mathutils import Vector

DRAMA = Path(__file__).resolve().parents[3]
OUT = next(DRAMA.glob('2_*')) / 'background/map_3d'

# M1：兵道在塔西侧约 5–10 m，自西南斜向东北（Paving 属性 5 m 网格实测）。
# 以 lane_origin 为路上 t=0，沿 lane_dir 前进 t 米，lateral 为垂直路向（正值偏东南）。
STAGES = {
    'M1': {
        'lane_origin': (-87.7, -93.7),  # 塔 (-75.2,-91.2) 西南侧的路心
        'lane_dir': (0.57, 0.82),
        # 塔在路上 t≈9.2、东南侧 8.8 m；英雄放在 t=16，塔在其身后右侧，东南侧拍不被塔挡
        'hero': {'t': 16.0, 'lateral': 0.0, 'height': 1.8},
        # 天灾常规波：4 食尸鬼 + 2 亡灵法师，自东北沿路过来，面朝英雄；常规不带绞肉车
        'units': [
            ('m4', 27.0, -1.6), ('m4', 27.5, 1.4), ('m4', 29.5, -0.2), ('m4', 30.0, 2.6),
            ('m5', 34.0, -1.0), ('m5', 34.5, 1.8),
        ],
    },
}

p = argparse.ArgumentParser()
p.add_argument('--src', required=True)
p.add_argument('--dst', required=True)
p.add_argument('--region', default='M1')
args = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
cfg = STAGES[args.region]
dest = OUT / args.dst
if dest.exists():
    raise FileExistsError(dest)

bpy.ops.wm.open_mainfile(filepath=str(OUT / args.src))
scene = bpy.context.scene
depsgraph = bpy.context.evaluated_depsgraph_get()
terrain = bpy.data.objects['Terrain_683d']


def ground_z(x, y):
    inv = terrain.matrix_world.inverted()
    hit, loc, *_ = terrain.evaluated_get(depsgraph).ray_cast(inv @ Vector((x, y, 500.0)), (inv.to_3x3() @ Vector((0, 0, -1))).normalized())
    if not hit:
        raise RuntimeError(('no ground under', x, y))
    return (terrain.matrix_world @ loc).z


ox, oy = cfg['lane_origin']
dx, dy = cfg['lane_dir']
n = math.hypot(dx, dy); dx, dy = dx / n, dy / n
px, py = dy, -dx  # 垂直路向，指向东南


def lane_point(t, lateral):
    x, y = ox + dx * t + px * lateral, oy + dy * t + py * lateral
    return Vector((x, y, ground_z(x, y)))


facing_ne = math.atan2(dx, -dy)  # 朝 (dx,dy)：sinθ=dx、−cosθ=dy
facing_sw = facing_ne + math.pi

name = f'DEMO_{args.region}'
if name in bpy.data.collections:
    raise RuntimeError(('已有演示集合', name))
coll = bpy.data.collections.new(name)
scene.collection.children.link(coll)
records = []

# 英雄占位：灰色胶囊＋朝向楔块，只标站位与朝向，不代表造型
h = cfg['hero']
hero_loc = lane_point(h['t'], h['lateral'])
mat = bpy.data.materials.new('DEMO_hero_placeholder')
mat.use_nodes = True
next(nd for nd in mat.node_tree.nodes if nd.type == 'BSDF_PRINCIPLED').inputs['Base Color'].default_value = (0.55, 0.55, 0.58, 1)
radius = 0.28
bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=h['height'] - 2 * radius, location=hero_loc + Vector((0, 0, h['height'] / 2)))
body = bpy.context.active_object
bpy.ops.mesh.primitive_uv_sphere_add(radius=radius * 1.05, location=hero_loc + Vector((0, 0, h['height'] - radius)))
head = bpy.context.active_object
bpy.ops.mesh.primitive_cone_add(radius1=0.12, depth=0.35, location=(0, 0, 0))
nose = bpy.context.active_object
nose.rotation_euler = (math.pi / 2, 0, facing_ne)  # 锥尖（+Z）转到 −Y 再按朝向旋转，指向英雄正面
nose.location = hero_loc + Vector((dx * radius * 1.4, dy * radius * 1.4, h['height'] - radius))
for ob in (body, head, nose):
    ob.data.materials.append(mat)
    for c in ob.users_collection:
        c.objects.unlink(ob)
    coll.objects.link(ob)
body.name, head.name, nose.name = f'{name}_hero_body', f'{name}_hero_head', f'{name}_hero_facing'
records.append({'object': 'hero_placeholder', 'location': list(hero_loc), 'facing_deg': math.degrees(facing_ne), 'height_m': h['height']})

for i, (aid, t, lateral) in enumerate(cfg['units']):
    src = bpy.data.collections.get(f'ASSET_{aid}')
    if not src:
        raise RuntimeError(('总装里没有该资产集合', aid))
    ob = bpy.data.objects.new(f'{name}_{aid}_{i}', None)
    ob.instance_type = 'COLLECTION'
    ob.instance_collection = src
    ob.location = lane_point(t, lateral)
    ob.rotation_euler = (0, 0, facing_sw)
    coll.objects.link(ob)
    records.append({'object': ob.name, 'asset': aid, 'lane_t': t, 'lateral': lateral, 'location': list(ob.location), 'facing_deg': math.degrees(facing_sw)})

scene[f'demo_stage_{args.region}'] = 'followup 298: battlefield §4.2 常规波（4 食尸鬼+2 亡灵法师）＋英雄占位'
bpy.ops.wm.save_as_mainfile(filepath=str(dest), relative_remap=True)
stage_dir = OUT / 'regions' / args.region
stage_dir.mkdir(parents=True, exist_ok=True)
(stage_dir / f'{dest.stem}_demo_stage.json').write_text(json.dumps({
    'followup': 298, 'source': args.src, 'file': dest.name, 'region': args.region,
    'basis': 'battlefield.md §2.2 常规波、§4.2 近卫英雄 demo：天灾自东北沿路来、英雄面朝东北、古树塔在身后',
    'lane_origin': cfg['lane_origin'], 'lane_dir': [dx, dy], 'objects': records,
    'note': '英雄为灰色占位，只标站位与朝向；近卫友军沿用总装原有塔前兵线',
}, ensure_ascii=False, indent=2), encoding='utf-8')
print('STAGE_SAVED', dest, flush=True)
