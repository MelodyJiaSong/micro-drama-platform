"""在总装底稿里按区域放贴地机位出检查图；只读打开，不保存 blend。

用法：blender -b -P render_region_eye.py -- --blend assembly_working_v022_lod_v004.blend --region M1
机位规则见 battlefield.md §3 侧拍统一轴：东南侧望西北，近卫在画左、天灾在画右。
"""
from pathlib import Path
import argparse, json, math, sys
import bpy
from mathutils import Vector

DRAMA = Path(__file__).resolve().parents[3]
OUT = next(DRAMA.glob('2_*')) / 'background/map_3d'
# 区域 → 机位目标（米，总装坐标 = 6.83d 游戏坐标 / 20）与各机位相对目标的水平偏移、离地高度、焦距
REGIONS = {
    'M1': {
        'target': (-82.0, -96.0),  # 近卫中路一塔 (-75.2,-91.2) 与塔前兵线之间
        # sun: (高度角, 天空 sun_rotation) 弧度；原场景 (0.733, 5.105) 太阳在西北，东南机位全逆光。
        # 侧拍改为上午低角度、从机位身后偏左打来；只用于本次渲染，不保存。
        'views': {
            'side_SE': {'offset': (16.0, -16.0), 'height': 1.7, 'lens': 35, 'sun': (0.45, 1.75)},
            'low_SE': {'offset': (9.0, -9.0), 'height': 0.5, 'lens': 28, 'sun': (0.45, 1.75)},
            'wide_SE': {'offset': (40.0, -40.0), 'height': 28.0, 'lens': 30, 'sun': (0.45, 1.75)},
            # bg4 卡：视点在土路右侧路肩、一人高，顺着土路从西南望向东北，阳光从画面右后方
            # demo 侧拍（battlefield §4.2 bg4-2）：垂直兵道从东南望西北，英雄在画左、天灾从画右来；上午日光东偏南
            'demo_side': {'target': (-73.5, -73.2), 'offset': (16.4, -11.4), 'height': 1.6, 'lens': 28, 'sun': (0.5, 1.35)},
            'lane_SW': {'offset': (-24.0, -26.0), 'height': 1.7, 'lens': 35, 'look_offset': (6.0, 6.0), 'sun': (0.45, 3.4)},
        },
    },
    # 近卫基地（vlog 第 1 集，follow-up 314）：泉水 (-364.8,-360) → 东侧密室 bg23、奇迹古树 bg22 → 北侧 8 商人一排（面朝南）→ 世界之树 bg2 (-281.6,-307.2)
    # 机位一人高（vlog 自拍视角）；sun_rotation 按 compass ≈ 315 + (r − 5.105)·53.6 取顺光
    'B1': {
        'target': (-345.0, -345.0),
        'views': {
            'fountain_NE': {'target': (-364.8, -360.0), 'offset': (13.0, 9.0), 'height': 1.7, 'lens': 28, 'sun': (0.55, 0.1)},
            'shops_S': {'target': (-339.0, -360.0), 'offset': (2.0, -24.0), 'height': 1.7, 'lens': 28, 'look_z': 4.0, 'sun': (0.6, 2.6)},
            'merchants_S': {'target': (-350.0, -330.0), 'offset': (3.0, -16.0), 'height': 1.7, 'lens': 28, 'sun': (0.6, 2.6)},
            'worldtree_SW': {'target': (-281.6, -307.2), 'offset': (-26.0, -32.0), 'height': 1.7, 'lens': 24, 'look_z': 14.0, 'sun': (0.5, 3.4)},
            'base_drone_SE': {'target': (-320.0, -320.0), 'offset': (55.0, -60.0), 'height': 60.0, 'lens': 30, 'sun': (0.6, 2.6)},
        },
    },
}

p = argparse.ArgumentParser()
p.add_argument('--blend', default='assembly_working_v022_lod_v004.blend')
p.add_argument('--region', default='M1')
p.add_argument('--views', default='')
p.add_argument('--samples', type=int, default=24)
args = p.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [])
cfg = REGIONS[args.region]

bpy.ops.wm.open_mainfile(filepath=str(OUT / args.blend))
scene = bpy.context.scene
depsgraph = bpy.context.evaluated_depsgraph_get()


terrain = bpy.data.objects['Terrain_683d']


def ground_z(x, y):
    # 只对地形求高：场景里的 Atmosphere_volume、树冠都会先挡住射线
    inv = terrain.matrix_world.inverted()
    origin = inv @ Vector((x, y, 500.0))
    direction = (inv.to_3x3() @ Vector((0, 0, -1))).normalized()
    hit, loc, *_ = terrain.evaluated_get(depsgraph).ray_cast(origin, direction)
    if not hit:
        raise RuntimeError(('no ground under', x, y))
    return (terrain.matrix_world @ loc).z


scene.cycles.device = 'CPU'
scene.cycles.samples = args.samples
scene.cycles.use_denoising = True
scene.cycles.debug_use_compact_bvh = True
scene.cycles.texture_limit_render = '2048'
scene.render.resolution_x = 1600
scene.render.resolution_y = 900
dest = OUT / 'regions' / args.region
dest.mkdir(parents=True, exist_ok=True)
tx, ty = cfg['target']
tz = ground_z(tx, ty)
sky = next(n for n in scene.world.node_tree.nodes if n.type == 'TEX_SKY')
scene_sun = (sky.sun_elevation, sky.sun_rotation)
records = {}
names = [v for v in args.views.split(',') if v] or list(cfg['views'])
for name in names:
    v = cfg['views'][name]
    vx, vy = v.get('target', (tx, ty))
    cx, cy = vx + v['offset'][0], vy + v['offset'][1]
    cam_loc = Vector((cx, cy, ground_z(cx, cy) + v['height']))
    lx, ly = vx + v.get('look_offset', (0, 0))[0], vy + v.get('look_offset', (0, 0))[1]
    look = Vector((lx, ly, ground_z(lx, ly) + v.get('look_z', 1.5)))
    sky.sun_elevation, sky.sun_rotation = v.get('sun', scene_sun)
    data = bpy.data.cameras.new(f'REGION_{args.region}_{name}')
    data.lens = v['lens']
    data.clip_end = 3000
    cam = bpy.data.objects.new(data.name, data)
    scene.collection.objects.link(cam)
    cam.location = cam_loc
    cam.rotation_euler = (look - cam_loc).to_track_quat('-Z', 'Y').to_euler()
    scene.camera = cam
    file = dest / f'{Path(args.blend).stem}_{args.region}_{name}.png'
    scene.render.filepath = str(file)
    bpy.ops.render.render(write_still=True)
    records[name] = {'file': file.name, 'camera': list(cam_loc), 'look_at': list(look), 'lens': v['lens'],
                     'sun_elevation_rotation': [sky.sun_elevation, sky.sun_rotation], 'scene_sun': list(scene_sun)}
    print('RENDERED', file, flush=True)
(dest / f'{Path(args.blend).stem}_{args.region}_cameras.json').write_text(
    json.dumps({'blend': args.blend, 'region': args.region, 'samples': args.samples, 'views': records,
                'note': '只读检查渲染，未保存 blend'}, ensure_ascii=False, indent=2), encoding='utf-8')
