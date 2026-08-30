"""建《对抗熵增》的 previz 资产：F80 车体白模 + 三份场景主档。

用法（仓库根目录）：
    blender -b --factory-startup --python tools/build_duikang_assets.py -- all
    blender -b --factory-startup --python tools/build_duikang_assets.py -- f80
    blender -b --factory-startup --python tools/build_duikang_assets.py -- entropy_city

坐标约定（与 build_previz.py 一致）：
    +X 画右，-X 画左，+Y 画深处，Z 高度。车头朝 +Y。

产物一律是**灰模 blockout**，只承载几何：
    - 场景：广场/街道/高架/隧道的相对位置与尺度，遮挡关系，参照物高度。
    - F80：车体外形（本片的唯一例外——产品即长相，见 previz_plan §五）。
    材质、光色、细节一律不做，交 Seedance。

场景四板的相对位置一次定死（entropy_city）：
    广场在原点 → 主街沿 +Y 伸出 → 高架在更远的 +Y 横跨 → 隧道沿 -Y 伸出。
    于是「第Ⅱ幕冲出广场的方向」与「第Ⅴ幕驶回广场的方向」天然一致（shot16 ↔ shot56）。
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import bmesh
import bpy
from mathutils import Vector

REPO = Path(__file__).resolve().parent.parent
PROJECT = "duikang_shangzeng"
SCENES = REPO / "ai_videos" / PROJECT / "2_世界观人设" / "scenes"
PROPS = REPO / "ai_videos" / PROJECT / "2_世界观人设" / "props"


# ---------------------------------------------------------------- 基础工具

def wipe() -> None:
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob, do_unlink=True)
    for me in list(bpy.data.meshes):
        bpy.data.meshes.remove(me)


def grey(name: str, v: float = 0.45):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = False
    m.diffuse_color = (v, v, v, 1.0)
    return m


def box(name: str, size, loc, mat=None):
    """size=(X宽, Y纵深, Z高)；loc 为底面中心。"""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(loc[0], loc[1], loc[2] + size[2] / 2))
    ob = bpy.context.object
    ob.name = name
    ob.scale = Vector(size)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    ob.data.materials.append(mat or grey("previz_grey"))
    return ob


def cylinder(name: str, r: float, depth: float, loc, axis: str = "X", mat=None):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, vertices=24, location=loc)
    ob = bpy.context.object
    ob.name = name
    if axis == "X":
        ob.rotation_euler = (0.0, math.radians(90), 0.0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    ob.data.materials.append(mat or grey("previz_grey"))
    return ob


def save(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(path))
    print(f"  写出 {path.relative_to(REPO)}")


def join_all(name: str):
    obs = [o for o in bpy.data.objects if o.type == "MESH"]
    bpy.ops.object.select_all(action="DESELECT")
    for o in obs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = obs[0]
    if len(obs) > 1:
        bpy.ops.object.join()
    ob = bpy.context.view_layer.objects.active
    ob.name = name
    return ob


# ---------------------------------------------------------------- F80 车体白模

# 沿 Y 的横截面站位：(y, 最大半宽, 底面 z, 顶面 z)
# 数据源：f80_ferrari.md 事实表 —— 4.84 长 × 2.06 宽 × 1.14 高，轴距 2.67。
F80_STATIONS = [
    (+2.42, 0.55, 0.12, 0.40),   # 车头尖端（极窄、方正）
    (+2.05, 0.82, 0.10, 0.52),
    (+1.60, 1.00, 0.09, 0.64),   # 前轴前缘
    (+1.34, 1.03, 0.09, 0.70),   # 前轴
    (+0.95, 1.03, 0.10, 0.80),   # 前轮正后方的竖向导流开口所在站
    (+0.55, 1.02, 0.11, 0.98),   # 前风挡根部
    (-0.10, 0.97, 0.13, 1.14),   # 座舱最高点（泪滴形）
    (-0.70, 1.01, 0.14, 1.06),
    (-1.20, 1.03, 0.15, 0.94),   # 后轮拱饱满外鼓
    (-1.60, 1.03, 0.16, 0.86),   # 后轴
    (-2.10, 0.99, 0.24, 0.80),
    (-2.42, 0.90, 0.34, 0.74),   # 车尾
]


def f80_profile(hw: float, zb: float, zt: float):
    """双面坡（dihedral）横截面：底窄、腰最宽、顶收。返回 6 个 (x, z)。"""
    zm = zb + (zt - zb) * 0.38
    return [
        (-hw * 0.74, zb), (-hw, zm), (-hw * 0.78, zt),
        (+hw * 0.78, zt), (+hw, zm), (+hw * 0.74, zb),
    ]


def build_f80() -> None:
    wipe()
    m = grey("f80_white", 0.62)

    # —— 车体：沿 Y 放样 12 个横截面
    me = bpy.data.meshes.new("F80_BODY")
    bm = bmesh.new()
    rings = []
    for y, hw, zb, zt in F80_STATIONS:
        ring = [bm.verts.new((x, y, z)) for x, z in f80_profile(hw, zb, zt)]
        rings.append(ring)
    bm.verts.ensure_lookup_table()
    n = len(rings[0])
    for a, b in zip(rings, rings[1:]):
        for i in range(n):
            j = (i + 1) % n
            bm.faces.new((a[i], a[j], b[j], b[i]))
    bm.faces.new(list(reversed(rings[0])))   # 封车头
    bm.faces.new(rings[-1])                  # 封车尾
    bm.normal_update()
    bm.to_mesh(me)
    bm.free()
    body = bpy.data.objects.new("F80_BODY", me)
    bpy.context.collection.objects.link(body)
    body.data.materials.append(m)

    # —— 四轮（轴沿 X）。轮心落在前后轴站位上，轴距 2.67 ≈ 1.34-(-1.33)
    for sx in (-1, 1):
        for y in (1.34, -1.33):
            cylinder(f"F80_WHEEL_{'R' if sx > 0 else 'L'}_{'F' if y > 0 else 'B'}",
                     r=0.36, depth=0.34, loc=(sx * 0.87, y, 0.36), axis="X", mat=m)

    # —— 车头横贯黑条（F80 最易被画丢的识别特征，白模里做成一道凸唇）
    box("F80_NOSE_BAR", (1.30, 0.10, 0.07), (0.0, 2.38, 0.26), m)

    # —— 前轮正后方的笔直竖向导流开口（左右各一，做成外凸薄片好读）
    for sx in (-1, 1):
        box(f"F80_DUCT_{'R' if sx > 0 else 'L'}", (0.05, 0.14, 0.52),
            (sx * 1.02, 0.95, 0.14), m)

    # —— 主动式尾翼 + 两根支柱
    box("F80_WING", (1.62, 0.26, 0.05), (0.0, -2.16, 1.00), m)
    for sx in (-1, 1):
        box(f"F80_WING_PYLON_{'R' if sx > 0 else 'L'}", (0.07, 0.18, 0.24),
            (sx * 0.62, -2.16, 0.78), m)

    # —— 巨型扩散器（车尾下缘上翘）
    diff = box("F80_DIFFUSER", (1.72, 0.62, 0.26), (0.0, -2.18, 0.06), m)
    diff.rotation_euler = (math.radians(-13), 0.0, 0.0)
    bpy.ops.object.select_all(action="DESELECT")
    diff.select_set(True)
    bpy.context.view_layer.objects.active = diff
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

    ob = join_all("F80_WHITEMODEL")
    d = ob.dimensions
    print(f"  F80 白模包围盒：X {d.x:.2f} × Y {d.y:.2f} × Z {d.z:.2f}  "
          f"（目标 2.06 × 4.84 × 1.14）")
    save(PROPS / "f80_ferrari" / "f80_ferrari.blend")


# ---------------------------------------------------------------- 场景

def build_entropy_city() -> None:
    """四板一体：广场(原点) → 主街(+Y) → 高架(更远 +Y) → 隧道(-Y)。"""
    wipe()
    g = grey("city_grey", 0.42)
    gd = grey("city_dark", 0.28)

    # bg1_广场：60×60 铺地，中央偏画左有铜马台座
    box("BG1_PLAZA_GROUND", (60, 60, 0.2), (0, 0, -0.2), g)
    box("BG1_PLINTH", (2.2, 2.2, 1.20), (-9.0, 6.0, 0.0), gd)          # 铜马台座
    for i, (x, y, w, d, h) in enumerate([
        (-26, 20, 14, 16, 34), (26, 18, 16, 14, 42), (-24, -18, 12, 18, 26),
        (25, -20, 14, 16, 30), (0, 30, 22, 10, 20),
    ]):
        box(f"BG1_TOWER_{i}", (w, d, h), (x, y, 0.0), g)

    # bg2_主街：14m 宽，沿 +Y 从 y=40 到 y=200；两侧商铺 + 广告屏
    box("BG2_ROAD", (14, 160, 0.2), (0, 120, -0.2), gd)
    for k in range(10):
        y = 46 + k * 16
        for sx in (-1, 1):
            box(f"BG2_SHOP_{k}_{'R' if sx > 0 else 'L'}",
                (10, 14, 9 + (k % 3) * 4), (sx * 12, y, 0.0), g)
        if k % 3 == 0:
            box(f"BG2_SCREEN_{k}", (0.4, 6, 4), (-7.2, y, 6.0), gd)     # 广告屏
    box("BG2_SIGN_ARCH", (16, 0.6, 1.2), (0, 120, 11.0), gd)

    # bg3_高架：z=9，16m 宽，沿 X 横跨，在 y=260
    box("BG3_DECK", (120, 16, 0.6), (0, 260, 9.0), gd)
    for sx in (-1, 1):
        box(f"BG3_PARAPET_{'R' if sx > 0 else 'L'}", (120, 0.5, 1.1), (0, 260 + sx * 7.8, 9.6), g)
    for i in range(5):
        box(f"BG3_PIER_{i}", (3, 3, 9), (-48 + i * 24, 260, 0.0), g)

    # bg4_隧道：12m 宽 7m 高，沿 -Y 从 y=-40 到 y=-160
    box("BG4_TUNNEL_ROAD", (12, 120, 0.2), (0, -100, -0.2), gd)
    box("BG4_TUNNEL_CEIL", (13, 120, 0.5), (0, -100, 7.0), g)
    for sx in (-1, 1):
        box(f"BG4_TUNNEL_WALL_{'R' if sx > 0 else 'L'}", (0.6, 120, 7), (sx * 6.5, -100, 0.0), g)
    for k in range(15):                                                  # 顶部条形灯
        box(f"BG4_LAMP_{k}", (2.4, 0.5, 0.2), (0, -44 - k * 8, 6.8), gd)

    save(SCENES / "entropy_city" / "entropy_city.blend")
    print("  四板相对位置：广场(0,0) → 主街(+Y 40..200) → 高架(+Y 260) → 隧道(-Y -40..-160)")


def build_medieval_road() -> None:
    wipe()
    g = grey("med_grey", 0.48)
    gd = grey("med_dark", 0.32)
    box("MED_ROAD", (9, 160, 0.2), (0, 60, -0.2), gd)                    # 石板路，9m 宽
    for k in range(14):
        y = -10 + k * 12
        for sx in (-1, 1):
            h = 7 + (k % 3) * 2.5
            box(f"MED_HOUSE_{k}_{'R' if sx > 0 else 'L'}", (8, 10, h), (sx * 8.5, y, 0.0), g)
            box(f"MED_EAVE_{k}_{'R' if sx > 0 else 'L'}", (9.4, 10.6, 0.4),
                (sx * 8.2, y, h), gd)                                     # 出檐
    # 城门拱：跨在路上
    for sx in (-1, 1):
        box(f"MED_GATE_PIER_{'R' if sx > 0 else 'L'}", (3, 3, 11), (sx * 6, 96, 0.0), g)
    box("MED_GATE_TOP", (15, 3, 3), (0, 96, 11.0), g)
    box("MED_WELL", (2.2, 2.2, 1.0), (-6.5, 30, 0.0), gd)                # 水井（时代对照物）
    box("MED_CART", (1.4, 2.6, 1.3), (5.6, 46, 0.0), gd)                 # 木轮马车
    save(SCENES / "medieval_road" / "medieval_road.blend")


def build_ice_plain() -> None:
    wipe()
    g = grey("ice_grey", 0.72)
    gd = grey("ice_dark", 0.38)
    box("ICE_SHEET", (600, 600, 0.2), (0, 120, -0.2), g)                 # 一望无际的冻湖
    # 远处低矮雪丘（尺度参照物）
    for i, (x, y, w, d, h) in enumerate([
        (-120, 300, 90, 40, 12), (110, 340, 120, 50, 16), (-40, 420, 160, 60, 20),
        (200, 260, 70, 30, 9), (-230, 380, 100, 45, 14),
    ]):
        box(f"ICE_MOUND_{i}", (w, d, h), (x, y, 0.0), g)
    # 稀疏枯树剪影
    for i, (x, y) in enumerate([(-38, 90), (44, 150), (-60, 210), (70, 260), (-15, 320)]):
        box(f"ICE_TREE_{i}", (0.5, 0.5, 6.0), (x, y, 0.0), gd)
    save(SCENES / "ice_plain" / "ice_plain.blend")


# ---------------------------------------------------------------- 入口

BUILDERS = {
    "f80": build_f80,
    "entropy_city": build_entropy_city,
    "medieval_road": build_medieval_road,
    "ice_plain": build_ice_plain,
}

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["all"]
targets = list(BUILDERS) if argv[0] == "all" else argv
for t in targets:
    if t not in BUILDERS:
        raise SystemExit(f"不认识的目标「{t}」；可用＝{'/'.join(BUILDERS)}/all")
    print(f"[assets] 建 {t}")
    BUILDERS[t]()
print("[assets] 完成")
