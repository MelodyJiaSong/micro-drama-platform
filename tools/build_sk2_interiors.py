# -*- coding: utf-8 -*-
"""sk2 的四处**内景** blend：旅店堂屋 / 王座厅 / 地铁站台 / 水下车厢。

为什么要单独建
--------------
全城 blockout（`build_stormwind.py`）只给每个地点一个**体块**——从外面看是对的，
可 15 条室内镜的相机站在体块**内部**，渲出来是一整面灰墙。
`previz_sk2.py` 开头本来就写明「内景几何另建」，这份就是那个「另建」。

精度按 rule 4g ④：这四处都是**贴身而过**（人物就在画面里），所以给到
「体块 + 开间节奏 + 主要家具」，不做装饰构件——previz 要的是
**站位、朝向、动线、遮挡关系**，不是长相（长相归场景主体参考图）。

坐标约定：**每处内景自带局部原点**，`(0,0,0)` ＝ 该空间的地面中心，
+Y ＝ 往房间纵深走，+Z 向上，米，1:1。previz 用到时不套城市坐标（见 `INTERIORS`）。

产物（rule 4g §J：场景层只出 blend + 校验 PNG，**不渲 mp4**）：
    scenes/{key}/_blender/{key}.blend
    scenes/{key}/_blender/check_{key}.png

用法（仓库根目录）：
    blender -b --factory-startup --python tools/build_sk2_interiors.py -- --only jiuguan
    blender -b --factory-startup --python tools/build_sk2_interiors.py
"""
import math
import sys
from pathlib import Path

import bpy

REPO = Path(__file__).resolve().parent.parent
SCENES = REPO / "ai_videos" / "shikong_lvxing" / "sk2" / "2_世界观人设" / "scenes"

PALETTE = {
    "石墙灰":   (0.48, 0.46, 0.42),
    "暖木棕":   (0.26, 0.15, 0.07),
    "深木":     (0.14, 0.08, 0.04),
    "地板棕":   (0.32, 0.21, 0.11),
    "火光橙":   (0.90, 0.42, 0.10),
    "黄铜":     (0.52, 0.38, 0.12),
    "藏蓝布":   (0.06, 0.10, 0.30),
    "月白石":   (0.72, 0.70, 0.65),
    "铁灰":     (0.13, 0.13, 0.15),
    "暗红毯":   (0.28, 0.05, 0.06),
    "青蓝水":   (0.04, 0.16, 0.28),
    "玻璃青":   (0.30, 0.48, 0.55),
    "站台灰":   (0.40, 0.39, 0.37),
}


def mat(name):
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    r, g, bl = PALETTE[name]
    b.inputs["Base Color"].default_value = (r, g, bl, 1.0)
    if name in ("火光橙",):
        b.inputs["Emission Color"].default_value = (1.0, 0.45, 0.12, 1.0)
        b.inputs["Emission Strength"].default_value = 6.0
    if name in ("黄铜", "铁灰"):
        b.inputs["Metallic"].default_value = 1.0
        b.inputs["Roughness"].default_value = 0.45
    elif name == "玻璃青":
        b.inputs["Roughness"].default_value = 0.05
    else:
        b.inputs["Roughness"].default_value = 0.85
    return m


def box(name, loc, size, color, parent=None, rot=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    o = bpy.context.object
    o.name, o.scale, o.rotation_euler = name, size, (0, 0, rot)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(mat(color))
    if parent:
        o.parent = parent
    return o


def cyl(name, loc, r, h, color, parent=None, verts=16, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=loc,
                                        rotation=rot)
    o = bpy.context.object
    o.name = name
    o.data.materials.append(mat(color))
    if parent:
        o.parent = parent
    return o


def vault(root, tag, y0, y1, half_w, spring_z, top_z, segs=14, color="石墙灰"):
    """筒拱：沿 Y 铺一串弧形薄板。给站台与地道用。"""
    rise = top_z - spring_z
    n = 10
    for i in range(n):
        a0 = math.pi * i / n
        a1 = math.pi * (i + 1) / n
        x = math.cos((a0 + a1) / 2) * half_w
        z = spring_z + math.sin((a0 + a1) / 2) * rise
        w = half_w * math.pi / n
        ang = -((a0 + a1) / 2 - math.pi / 2)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, (y0 + y1) / 2, z))
        o = bpy.context.object
        o.name = f"{tag}_v{i:02d}"
        o.scale = (0.45, y1 - y0, w * 1.15)
        o.rotation_euler = (0, ang, 0)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        o.data.materials.append(mat(color))
        o.parent = root


def room_shell(root, tag, w, d, h, floor_col, wall_col, open_south=False):
    """地板 + 四壁 + 顶。房间中心在原点，+Y 纵深。"""
    box(f"{tag}_floor", (0, d / 2, -0.1), (w, d, 0.2), floor_col, root)
    box(f"{tag}_ceil", (0, d / 2, h + 0.1), (w, d, 0.2), wall_col, root)
    box(f"{tag}_wN", (0, d, h / 2), (w, 0.4, h), wall_col, root)
    if not open_south:
        box(f"{tag}_wS", (0, 0, h / 2), (w, 0.4, h), wall_col, root)
    for sgn in (-1, 1):
        box(f"{tag}_w{sgn:+d}", (sgn * w / 2, d / 2, h / 2), (0.4, d, h), wall_col, root)


# ══════════════════════════════════════════════════════════════════
def build_jiuguan(root):
    """镀金玫瑰旅店堂屋：14×10×5。壁炉在 -X 墙，吧台沿 +X，楼梯在北端。"""
    W, D, H = 14.0, 10.0, 5.0
    room_shell(root, "J", W, D, H, "地板棕", "石墙灰")
    # 壁炉（-X 墙中段）：炉膛 + 火 + 炉台
    box("J_hearth", (-W / 2 + 0.6, 4.2, 1.1), (1.4, 3.0, 2.2), "石墙灰", root)
    box("J_fire", (-W / 2 + 1.1, 4.2, 0.55), (0.5, 1.6, 0.9), "火光橙", root)
    box("J_mantel", (-W / 2 + 0.9, 4.2, 2.35), (1.9, 3.4, 0.25), "深木", root)
    # 吧台（+X 侧，沿 Y）
    box("J_bar", (W / 2 - 1.6, 5.0, 0.55), (1.0, 6.0, 1.10), "深木", root)
    box("J_backbar", (W / 2 - 0.7, 5.0, 1.3), (0.5, 6.4, 2.6), "暖木棕", root)
    for i in range(5):
        cyl(f"J_stool{i}", (W / 2 - 2.5, 2.6 + i * 1.2, 0.38), 0.22, 0.76, "深木", root, 10)
    # 长桌 + 长凳（中央两排）
    for r_ in range(2):
        for c in range(3):
            x = -3.6 + r_ * 4.0
            y = 2.2 + c * 2.6
            box(f"J_tbl{r_}{c}", (x, y, 0.74), (1.5, 1.9, 0.10), "暖木棕", root)
            for lx in (-0.6, 0.6):
                for ly in (-0.8, 0.8):
                    box(f"J_leg{r_}{c}{lx}{ly}", (x + lx, y + ly, 0.37),
                        (0.12, 0.12, 0.74), "深木", root)
            for bx in (-1.05, 1.05):
                box(f"J_bench{r_}{c}{bx}", (x + bx, y, 0.44), (0.42, 1.8, 0.10),
                    "暖木棕", root)
    # 北端楼梯上二楼
    for i in range(9):
        box(f"J_step{i:02d}", (4.6, D - 0.6 - i * 0.30, 0.18 + i * 0.36),
            (3.2, 0.32, 0.36), "暖木棕", root)
    # 顶梁
    for i in range(5):
        box(f"J_beam{i}", (0, 1.2 + i * 2.0, H - 0.35), (W - 0.8, 0.35, 0.35),
            "深木", root)
    # 南墙两扇窗（发光板代替，previz 只要知道光从哪来）
    for sx in (-4.0, 4.0):
        box(f"J_win{sx}", (sx, 0.25, 2.6), (2.0, 0.12, 1.6), "月白石", root)
    return "旅店堂屋 14×10×5：壁炉/吧台/两排长桌/北端楼梯"


def build_wangzuoting(root):
    """暴风要塞王座厅：40×18×14。两列柱，北端台基王座，侧高窗。"""
    W, D, H = 18.0, 40.0, 14.0
    room_shell(root, "T", W, D, H, "暗红毯", "月白石")
    # 中央红毯
    box("T_carpet", (0, D / 2, 0.02), (4.0, D - 2.0, 0.04), "暗红毯", root)
    # 两列柱
    for sgn in (-1, 1):
        for i in range(7):
            y = 4.0 + i * 5.0
            cyl(f"T_col{sgn:+d}{i}", (sgn * 6.0, y, H / 2), 0.85, H, "月白石", root, 12)
            box(f"T_cap{sgn:+d}{i}", (sgn * 6.0, y, H - 0.5), (2.2, 2.2, 1.0),
                "月白石", root)
            # 柱间悬挂的狮鹫长旗
            box(f"T_ban{sgn:+d}{i}", (sgn * 5.0, y, 8.0), (0.08, 1.6, 6.0),
                "藏蓝布", root)
    # 北端三级台基 + 王座
    for i in range(3):
        box(f"T_dais{i}", (0, D - 2.5 - i * 1.2, 0.25 + i * 0.5),
            (10.0 - i * 1.6, 5.0 - i * 1.2, 0.5), "月白石", root)
    box("T_throne", (0, D - 2.2, 2.4), (2.2, 1.4, 2.4), "月白石", root)
    box("T_throneback", (0, D - 1.6, 3.9), (2.4, 0.4, 3.4), "黄铜", root)
    # 侧高窗（发光板）
    for sgn in (-1, 1):
        for i in range(6):
            box(f"T_win{sgn:+d}{i}", (sgn * (W / 2 - 0.3), 5.0 + i * 5.5, 10.0),
                (0.15, 2.2, 5.0), "月白石", root)
    return "王座厅 18×40×14：两列 7 柱/中央红毯/北端三级台基王座/侧高窗"


def build_zhantai(root):
    """深铁矿道地铁站台：44 长 × 13 宽，筒拱顶 8 m。站台高 1.0 m，轨道在 -X 侧。"""
    L, W = 44.0, 13.0
    box("Z_floor", (0, L / 2, -0.1), (W, L, 0.2), "站台灰", root)
    # 站台面（+X 侧）与轨道沟（-X 侧）
    box("Z_plat", (2.6, L / 2, 0.5), (7.6, L - 1.0, 1.0), "站台灰", root)
    box("Z_trench", (-3.2, L / 2, -0.35), (5.0, L, 0.5), "铁灰", root)
    for rx in (-4.0, -2.4):
        box(f"Z_rail{rx}", (rx, L / 2, 0.06), (0.16, L, 0.12), "铁灰", root)
    # 两侧墙 + 筒拱
    for sgn in (-1, 1):
        box(f"Z_w{sgn:+d}", (sgn * W / 2, L / 2, 2.0), (0.5, L, 4.0), "石墙灰", root)
    vault(root, "Z", 0.0, L, W / 2, 4.0, 8.0)
    # 拱肋 + 站台灯
    for i in range(9):
        y = 2.0 + i * 5.0
        box(f"Z_rib{i}", (0, y, 6.0), (W, 0.5, 0.5), "石墙灰", root)
        cyl(f"Z_lamp{i}", (2.6, y, 3.4), 0.13, 2.8, "铁灰", root, 8)
        box(f"Z_lamph{i}", (2.6, y, 4.95), (0.6, 0.6, 0.5), "火光橙", root)
    # 长椅
    for i in range(4):
        box(f"Z_bench{i}", (5.0, 6.0 + i * 9.0, 1.45), (1.0, 2.6, 0.12), "暖木棕", root)
    return "地铁站台 13×44，筒拱 8 m：站台/轨道沟/9 道拱肋/站台灯"


def build_chexiang(root):
    """水下段：玻璃管隧道里跑的车厢。管内径 9 m，车厢 12×2.8×2.9，管外是水。"""
    L = 60.0
    # 玻璃管（两层薄壁圆柱表示）
    cyl("C_tube", (0, L / 2, 0.0), 4.5, L, "玻璃青", root, 24, rot=(math.pi / 2, 0, 0))
    # 管外的水体（大盒子，管在里面）
    box("C_water", (0, L / 2, 2.0), (46.0, L, 30.0), "青蓝水", root)
    # 轨道床
    box("C_bed", (0, L / 2, -3.4), (7.0, L, 0.6), "铁灰", root)
    for rx in (-0.8, 0.8):
        box(f"C_rail{rx}", (rx, L / 2, -3.05), (0.16, L, 0.12), "铁灰", root)
    # 车厢（停在管中段）：地板/侧壁/顶/窗带/座椅
    cy, CL, CW, CH = L / 2, 12.0, 2.8, 2.9
    box("C_floor", (0, cy, -2.95), (CW, CL, 0.15), "铁灰", root)
    box("C_roof", (0, cy, 0.0), (CW, CL, 0.12), "铁灰", root)
    for sgn in (-1, 1):
        box(f"C_side{sgn:+d}", (sgn * CW / 2, cy, -2.35), (0.10, CL, 1.1), "铁灰", root)
        box(f"C_glass{sgn:+d}", (sgn * CW / 2, cy, -1.05), (0.06, CL, 1.5),
            "玻璃青", root)
        for i in range(5):
            box(f"C_seat{sgn:+d}{i}", (sgn * (CW / 2 - 0.55), cy - 4.4 + i * 2.2, -2.55),
                (0.95, 1.5, 0.12), "暖木棕", root)
            box(f"C_back{sgn:+d}{i}", (sgn * (CW / 2 - 0.12), cy - 4.4 + i * 2.2, -2.0),
                (0.12, 1.5, 1.0), "暖木棕", root)
    for i in range(4):
        cyl(f"C_pole{i}", (0, cy - 3.6 + i * 2.4, -1.5), 0.05, 2.8, "黄铜", root, 8)
    return "水下车厢 12×2.8×2.9 + 玻璃管内径 9 m + 管外水体"


BUILDERS = {
    "jiuguan": ("旅店堂屋", build_jiuguan),
    "wangzuoting": ("王座厅", build_wangzuoting),
    "zhantai": ("地铁站台", build_zhantai),
    "chexiang": ("水下车厢", build_chexiang),
}

# 校验图机位：(相机 xyz, 看向 xyz, 焦距)
# **必须站在房间里**：`room_shell` 的南墙在 y=0、房间占 y=0..D，
# 先前 jiuguan 写 y=-3、wangzuoting 写 y=-8，相机在屋外，渲出来整片灰墙。
CHECK_CAM = {
    "jiuguan": ((0.0, 1.2, 2.6), (0.0, 8.0, 1.4), 20.0),
    "wangzuoting": ((0.0, 3.0, 4.5), (0.0, 34.0, 4.0), 24.0),
    "zhantai": ((5.0, -6.0, 3.2), (0.0, 20.0, 2.0), 20.0),
    "chexiang": ((0.0, 18.0, -1.4), (0.0, 34.0, -1.9), 24.0),
}


def argv():
    a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    return {x[2:]: a[i + 1] for i, x in enumerate(a) if x.startswith("--") and i + 1 < len(a)}


def setup_render(sc):
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.resolution_x, sc.render.resolution_y = 1280, 720
    sc.render.image_settings.file_format = "PNG"
    try:
        sc.view_settings.view_transform = "AgX"
    except Exception:
        pass


def world_light(sc, strength=0.6):
    w = bpy.data.worlds.new("w")
    w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (0.35, 0.40, 0.48, 1.0)
    bg.inputs["Strength"].default_value = strength
    sc.world = w


def build_one(key):
    label, fn = BUILDERS[key]
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    setup_render(sc)
    world_light(sc)
    root = bpy.data.objects.new(f"ROOT_{key}", None)
    sc.collection.objects.link(root)
    note = fn(root)

    # 补一盏内景主光：内景没有天光，全靠这盏 + 自发光面
    bpy.ops.object.light_add(type="AREA", location=(0, 12.0, 6.0))
    lamp = bpy.context.object
    lamp.data.energy = 4000.0
    lamp.data.size = 10.0

    out_dir = SCENES / key / "_blender"
    out_dir.mkdir(parents=True, exist_ok=True)

    loc, look, lens = CHECK_CAM[key]
    cam_d = bpy.data.cameras.new("chk")
    cam_d.lens, cam_d.clip_start, cam_d.clip_end = lens, 0.05, 500.0
    cam = bpy.data.objects.new("chk", cam_d)
    sc.collection.objects.link(cam)
    sc.camera = cam
    cam.location = loc
    tgt = bpy.data.objects.new("chk_t", None)
    sc.collection.objects.link(tgt)
    tgt.location = look
    t = cam.constraints.new("TRACK_TO")
    t.target = tgt
    t.track_axis, t.up_axis = "TRACK_NEGATIVE_Z", "UP_Y"

    sc.render.filepath = str(out_dir / f"check_{key}.png")
    bpy.ops.render.render(write_still=True)

    blend = out_dir / f"{key}.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    n = len([o for o in bpy.data.objects if o.type == "MESH"])
    print(f"[内景] {key}（{label}）{note} · 物体 {n} · -> {blend.name} + check_{key}.png")


def main():
    A = argv()
    keys = [k.strip() for k in A.get("only", "").split(",") if k.strip()] or list(BUILDERS)
    for k in keys:
        if k not in BUILDERS:
            raise SystemExit(f"未知内景 {k}，可选：{list(BUILDERS)}")
        build_one(k)


main()
