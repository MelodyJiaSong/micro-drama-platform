"""真实尺度 · 精细环境（ep01 第 3 版，用户 2026-11-08：「后面的场景太粗糙了应该做一个精细的场景，可以用图片或者 blender 来做」）。

由 build_cutout.py exec 进来使用（依赖其中的 _link、_cut_material、REPO、SHARED）。四层：
1. 远景板：Codex 生成的草原地平线照片，竖在 5 km 外（地平线行对准相机高度）；合影另放一块缩小的。
2. 中景：Codex 生成的金合欢 / 灌木抠像平面，散在 40–700 m，横移时有真实视差。
3. 近景：Poly Haven CC0 草（几何节点散布）：动物前方与脚下只铺 2–15 cm 的短草（不挡视线到蹄底），
   身后铺放大的干草丛（0.3–1 m）与零星石块。
4. 主体（build_cutout.py）。
"""
from __future__ import annotations

import json
import math
import random

import bpy
from mathutils import Vector

MODELS = SHARED / "models"  # noqa: F821  (exec 环境里有 SHARED)
GRASS_TINT = (0.42, 1.1, 1.35)    # 色相 / 饱和 / 明度：把绿草调成旱季草原的枯黄
DRY_TINT = (0.48, 1.35, 1.3)      # Poly Haven dry_diff 偏灰：再往金黄调


def _src_collection(name: str, model: str, keep=lambda n: True, tint: tuple | None = GRASS_TINT) -> bpy.types.Collection:
    """导入 glTF 到一个不挂进场景的集合（只作几何节点实例源，自身不渲染）。"""
    col = bpy.data.collections.get(name)
    if col:
        return col
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(MODELS / model / f"{model}.gltf"))
    new = [o for o in bpy.data.objects if o not in before]
    col = bpy.data.collections.new(name)
    for o in new:
        for c in list(o.users_collection):
            c.objects.unlink(o)
        if o.type == "MESH" and keep(o.name):
            o.location = (0, 0, 0)
            o.rotation_euler = (0, 0, 0)
            o.parent = None
            col.objects.link(o)
        else:
            bpy.data.objects.remove(o, do_unlink=True)
    tex_dir = MODELS / model / "textures"
    for o in col.objects:
        for sl in o.material_slots:
            m = sl.material
            if not m or m.get("fixed"):
                continue
            nt = m.node_tree
            b = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None)
            link = b and next(iter(b.inputs["Base Color"].links), None)
            # glTF 的 1k 颜色贴图是 JPG、没有透明：草叶间的暗底被渲成实心块（第 3 版首测全黑）。单独接 Poly Haven 的 Alpha 图
            alpha = sorted(tex_dir.glob("*_alpha_2k.jpg"))
            if b and alpha:
                ta = nt.nodes.new("ShaderNodeTexImage")
                ta.image = bpy.data.images.load(str(alpha[0]), check_existing=True)
                ta.image.colorspace_settings.name = "Non-Color"
                for l in list(b.inputs["Alpha"].links):
                    nt.links.remove(l)
                uvsrc = next((n for n in nt.nodes if n.type == "TEX_IMAGE" and n is not ta), None)
                if uvsrc and uvsrc.inputs["Vector"].links:
                    nt.links.new(uvsrc.inputs["Vector"].links[0].from_socket, ta.inputs["Vector"])
                nt.links.new(ta.outputs["Color"], b.inputs["Alpha"])
            # 旱季：有 dry_diff（Poly Haven 枯草色）就换上；没有就用色相偏移调黄
            dry = sorted(tex_dir.glob("*_dry_diff_2k.jpg"))
            if link and dry:
                link.from_node.image = bpy.data.images.load(str(dry[0]), check_existing=True)
                if tint:
                    hsv = nt.nodes.new("ShaderNodeHueSaturation")
                    hsv.inputs["Hue"].default_value, hsv.inputs["Saturation"].default_value, hsv.inputs["Value"].default_value = DRY_TINT
                    nt.links.new(link.from_socket, hsv.inputs["Color"])
                    nt.links.new(hsv.outputs["Color"], b.inputs["Base Color"])
            elif link and tint:
                hsv = nt.nodes.new("ShaderNodeHueSaturation")
                hsv.inputs["Hue"].default_value, hsv.inputs["Saturation"].default_value, hsv.inputs["Value"].default_value = tint
                nt.links.new(link.from_socket, hsv.inputs["Color"])
                nt.links.new(hsv.outputs["Color"], b.inputs["Base Color"])
            for attr, v in (("surface_render_method", "DITHERED"), ("blend_method", "HASHED")):
                try:
                    setattr(m, attr, v)
                except (AttributeError, TypeError):
                    pass
            m["fixed"] = True
    return col


def _region(name: str, x0: float, x1: float, y0: float, y1: float) -> bpy.types.Object:
    me = bpy.data.meshes.new(name)
    me.from_pydata([(x0, y0, 0), (x1, y0, 0), (x1, y1, 0), (x0, y1, 0)], [], [(0, 1, 2, 3)])
    ob = bpy.data.objects.new(name, me)
    _link(ob)  # noqa: F821
    return ob


def scatter(name: str, region: tuple, src: bpy.types.Collection, density: float, smin: float, smax: float,
            seed: int = 0, patch: float = 0.6, cast_shadow: bool = True) -> bpy.types.Object:
    """几何节点：区域面上随机撒点 → 随机挑实例、随机朝向与缩放；patch>0 时用噪声做成一片一片的疏密。"""
    ob = _region(name, *region)
    ng = bpy.data.node_groups.new(name + "_gn", "GeometryNodeTree")
    ng.interface.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    N = ng.nodes
    L = ng.links
    gi, go = N.new("NodeGroupInput"), N.new("NodeGroupOutput")
    dist = N.new("GeometryNodeDistributePointsOnFaces")
    dist.distribute_method = "RANDOM"
    dist.inputs["Seed"].default_value = seed
    pos = N.new("GeometryNodeInputPosition")
    noise = N.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 0.08
    noise.inputs["Detail"].default_value = 3.0
    mr = N.new("ShaderNodeMapRange")
    mr.inputs["From Min"].default_value = 0.35
    mr.inputs["From Max"].default_value = 0.65
    mr.inputs["To Min"].default_value = density * (1 - patch)
    mr.inputs["To Max"].default_value = density
    L.new(pos.outputs[0], noise.inputs["Vector"])
    L.new(noise.outputs["Fac"], mr.inputs["Value"])
    L.new(gi.outputs[0], dist.inputs["Mesh"])
    L.new(mr.outputs["Result"], dist.inputs["Density"])
    ci = N.new("GeometryNodeCollectionInfo")
    ci.inputs["Collection"].default_value = src
    ci.inputs["Separate Children"].default_value = True
    ci.inputs["Reset Children"].default_value = True
    inst = N.new("GeometryNodeInstanceOnPoints")
    inst.inputs["Pick Instance"].default_value = True
    ri = N.new("FunctionNodeRandomValue")
    ri.data_type = "INT"
    ri.inputs["Min"].default_value = 0
    ri.inputs["Max"].default_value = len(src.objects) - 1
    ri.inputs["Seed"].default_value = seed + 1
    rr = N.new("FunctionNodeRandomValue")
    rr.data_type = "FLOAT_VECTOR"
    rr.inputs[0].default_value = (0, 0, 0)
    rr.inputs[1].default_value = (0, 0, 6.283)
    rr.inputs["Seed"].default_value = seed + 2
    rs = N.new("FunctionNodeRandomValue")
    rs.data_type = "FLOAT"
    rs.inputs["Min"].default_value = smin
    rs.inputs["Max"].default_value = smax
    rs.inputs["Seed"].default_value = seed + 3
    L.new(dist.outputs["Points"], inst.inputs["Points"])
    L.new(ci.outputs[0], inst.inputs["Instance"])
    L.new(next(o for o in ri.outputs if o.type == "INT" and o.enabled), inst.inputs["Instance Index"])
    L.new(next(o for o in rr.outputs if o.type == "VECTOR" and o.enabled), inst.inputs["Rotation"])
    L.new(next(o for o in rs.outputs if o.type == "VALUE" and o.enabled), inst.inputs["Scale"])
    L.new(inst.outputs[0], go.inputs[0])
    mod = ob.modifiers.new("scatter", "NODES")
    mod.node_group = ng
    ob["scatter"] = True
    if not cast_shadow:               # 短草的影子在画面里看不出，却占大半阴影计算
        ob.visible_shadow = False
    return ob


def billboard(name: str, png, height_m: float, x: float, y: float, strength: float = 1.0) -> bpy.types.Object:
    """抠像平面（树、灌木）：与主体同一种材质，底边落地，正对 −y。"""
    img = bpy.data.images.load(str(png), check_existing=True)
    w_px, h_px = img.size
    a = img.pixels[:]
    # 剪影底行：自下而上找第一行有不透明像素（裁切后应接近 0）
    bottom = 0
    for r in range(h_px):
        if any(a[(r * w_px + c) * 4 + 3] > 0.5 for c in range(0, w_px, 4)):
            bottom = r
            break
    mpp = height_m / h_px
    w = w_px * mpp
    z0 = -bottom * mpp
    me = bpy.data.meshes.new(name)
    me.from_pydata([(-w / 2, 0, z0), (w / 2, 0, z0), (w / 2, 0, z0 + height_m), (-w / 2, 0, z0 + height_m)], [], [(0, 1, 2, 3)])
    uv = me.uv_layers.new(name="UVMap")
    for li, co in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]):
        uv.data[li].uv = co
    key = "env_" + png.stem
    m = bpy.data.materials.get("cut_" + key) or _cut_material(key, png)  # noqa: F821
    m.node_tree.nodes["cut_strength"].outputs[0].default_value = strength
    me.materials.append(m)
    ob = bpy.data.objects.new(name, me)
    ob.location = (x, y, 0)
    ob.visible_shadow = False    # 同主体：竖直平面的影子会被压成贴地细线
    _link(ob)  # noqa: F821
    return ob


def plate(name: str, png, cx: float, y: float, width_m: float, horizon_from_top: float, horizon_z: float) -> bpy.types.Object:
    """远景板：照片竖在远处，照片里的地平线行对准 horizon_z（相机高度附近）。不投影、不受光。"""
    img = bpy.data.images.load(str(png), check_existing=True)
    w_px, h_px = img.size
    h = width_m * h_px / w_px
    top = horizon_z + horizon_from_top * h
    me = bpy.data.meshes.new(name)
    me.from_pydata([(-width_m / 2, 0, top - h), (width_m / 2, 0, top - h), (width_m / 2, 0, top), (-width_m / 2, 0, top)], [], [(0, 1, 2, 3)])
    uv = me.uv_layers.new(name="UVMap")
    for li, co in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]):
        uv.data[li].uv = co
    m = bpy.data.materials.new("plate_" + name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.interpolation = "Cubic"
    tex.extension = "EXTEND"
    em = nt.nodes.new("ShaderNodeEmission")
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(tex.outputs["Color"], em.inputs["Color"])
    nt.links.new(em.outputs[0], out.inputs["Surface"])
    me.materials.append(m)
    ob = bpy.data.objects.new(name, me)
    ob.location = (cx, y, 0)
    try:
        ob.visible_shadow = False
        ob.visible_diffuse = False
        ob.visible_glossy = False
    except AttributeError:
        pass
    _link(ob)  # noqa: F821
    return ob


def build_env(x_lo: float, x_hi: float, ep_dir, env: dict, cx_group: float | None = None, group_half: float = 0.0) -> None:
    """env：{"plate": png, "plate_horizon": 地平线行比例, "trees": [png...], "bushes": [png...]}。"""
    short = _src_collection("src_grass_short", "grass_bermuda_01")
    flat = _src_collection("src_grass_flat", "grass_bermuda_01",
                           keep=lambda n: any(k in n for k in ("dead", "flattened", "small")))   # ≤ 6 cm
    tall = _src_collection("src_grass_tall", "grass_medium_02")
    tall1 = _src_collection("src_grass_tall1", "grass_medium_01",
                            keep=lambda n: any(k in n for k in ("large", "mid", "tall")))
    rocks = _src_collection("src_rocks", "moon_rock_02", tint=None)
    xa, xb = x_lo - 40, x_hi + 40
    # 动物前方与脚下：相机只有 0.6–2 m 高、视线贴地，前方 25 m 内只铺贴地的枯草与压伏草（≤ 6 cm），蹄底不被挡；
    # 更近相机处（−25 m 以外）才用 bermuda 全部变体（≤ 15 cm），在景深里虚成前景
    scatter("scatter_flat_front", (xa, xb, -25.0, 1.2), flat, 45.0, 0.8, 1.0, seed=11, patch=0.5, cast_shadow=False)
    scatter("scatter_short_front", (xa, xb, -90.0, -25.0), short, 14.0, 0.7, 1.1, seed=12, patch=0.5, cast_shadow=False)
    # 身后：放大的干草丛（0.3–1 m）、两套模型混合，零星石块
    # 渲染量（第 3 版测速 21 s/帧 → 削减）：平视下 40 m 外的草被近处挡住、又在景深里，只铺到 40 m
    # 身后草丛从紧贴主体平面处（y=0.05）开始：原从 1.2 m 起，草带前沿在画面上是一条直边，像站在草坪边上（第 6 轮审片）
    scatter("scatter_tall_back_a", (xa, xb, 0.05, 40.0), tall, 1.8, 1.4, 2.6, seed=21, patch=0.75)
    scatter("scatter_tall_back_b", (xa, xb, 0.05, 40.0), tall1, 1.6, 1.8, 3.2, seed=31, patch=0.75)
    scatter("scatter_short_back", (xa, xb, 0.05, 30.0), short, 10.0, 0.8, 1.3, seed=41, patch=0.4, cast_shadow=False)
    # 前景草丛（第 6 轮审片：画面下 1/3 只有贴地小苗，像平涂泥地）。列队相机俯仰固定，相机高 ÷ 到主体距离恒为 0.0284，
    # 所以 y 处（主体前方 −y 米）的草只要矮于 0.0284 × (−y) 就挡不到蹄底；下面按 0.0256（留 10%）分三段给最高草高。
    # 草矮，只能靠密度盖住地面（首试 0.6–0.8 株/m² 在长焦景深下几乎看不出）
    scatter("scatter_fg_far_a", (xa, xb, -60.0, -18.0), tall, 3.0, 0.9, 1.1, seed=13, patch=0.6, cast_shadow=False)     # ≤ 0.44 m
    scatter("scatter_fg_far_b", (xa, xb, -60.0, -18.0), tall1, 3.0, 1.0, 1.4, seed=14, patch=0.6, cast_shadow=False)   # ≤ 0.45 m
    scatter("scatter_fg_mid_a", (xa, xb, -18.0, -8.0), tall, 5.0, 0.45, 0.5, seed=15, patch=0.6, cast_shadow=False)    # ≤ 0.20 m
    scatter("scatter_fg_mid_b", (xa, xb, -18.0, -8.0), tall1, 6.0, 0.55, 0.7, seed=16, patch=0.6, cast_shadow=False)   # ≤ 0.22 m
    scatter("scatter_fg_near", (xa, xb, -8.0, -3.0), short, 20.0, 0.5, 0.55, seed=17, patch=0.5, cast_shadow=False)     # ≤ 0.08 m
    scatter("scatter_rocks", (xa, xb, 2.0, 40.0), rocks, 0.02, 0.6, 2.0, seed=51, patch=0.2)
    rnd = random.Random(7)
    # 中景：树 40–700 m、灌木 20–200 m；x 范围随距离放宽（远处的要覆盖更宽的视野）
    for i in range(70):
        y = rnd.uniform(60, 700)
        spread = 0.14 * (y + 60)
        png = rnd.choice(env["trees"])
        billboard(f"env_tree_{i:02d}", png, rnd.uniform(4.5, 9.0), rnd.uniform(x_lo - spread, x_hi + spread), y)
    for i in range(90):
        y = rnd.uniform(20, 220)
        spread = 0.14 * (y + 60)
        billboard(f"env_bush_{i:02d}", rnd.choice(env["bushes"]), rnd.uniform(0.9, 2.2), rnd.uniform(x_lo - spread, x_hi + spread), y)
    # 远景板：5 km 外，宽度覆盖整个横移范围加两侧视野
    plate("env_plate", env["plate"], (x_lo + x_hi) / 2, 5000.0, (x_hi - x_lo) + 1700.0, env["plate_horizon"], 1.0)


def _warm_copy(src: bpy.types.Collection, name: str, hue: float = 0.505, sat_mul: float = 1.8, val_mul: float = 1.35) -> bpy.types.Collection:
    """合影专用的暖色草：复制实例源与材质，只调色相 / 饱和 / 明度（第 7 轮审片：合影近处枯草灰褐、远景板草原金黄，两层色调发闷）。
    列队仍用原材质，不受影响。"""
    col = bpy.data.collections.get(name)
    if col:
        return col
    col = bpy.data.collections.new(name)
    for o in src.objects:
        c = o.copy()
        c.data = o.data.copy()
        for i, m in enumerate(c.data.materials):
            if not m:
                continue
            m2 = m.copy()
            for n in m2.node_tree.nodes:
                if n.type == "HUE_SAT":
                    n.inputs["Hue"].default_value = hue
                    n.inputs["Saturation"].default_value *= sat_mul
                    n.inputs["Value"].default_value *= val_mul
            c.data.materials[i] = m2
        col.objects.link(c)
    return col


def build_group_env(gx: float, cam: bpy.types.Object, row_depth: float, coll: bpy.types.Collection, env: dict) -> None:
    """合影环境：同一套草、树、远景板，按合影相机（约 600 m、超长焦、视角约 2.5°）的视野重新摆，挂进 Group 集合。"""
    # 暖色实例源要在记录 before 之前建：函数末尾会把新对象全部挪进 Group 集合，实例源被挪走就成了空集合（草全消失）
    short = _warm_copy(bpy.data.collections["src_grass_short"], "src_grp_grass_short")
    flat = _warm_copy(bpy.data.collections["src_grass_flat"], "src_grp_grass_flat")
    tall = _warm_copy(bpy.data.collections["src_grass_tall"], "src_grp_grass_tall")
    tall1 = _warm_copy(bpy.data.collections["src_grass_tall1"], "src_grp_grass_tall1")
    before = set(bpy.data.objects)
    half = 45.0
    # 机位一侧：画面下部是离相机约 340–600 m 的地面，掠射角约 1.5°，地面贴图被压成一片平色（第 3 版首片发现）。
    # 铺草把它变成长焦下层层压缩的草地；草高不挡前排蹄子：y 处的草高须 < 相机高 ×（−y）/ 600。
    cam_y = cam.location.y
    y_near = cam_y + 240.0                   # 画面下沿约在相机前 340 m，留余量
    # 草高从机位一侧到脚线逐段降低（第 7 轮审片：原来只有「高草 → 矮草 → 贴地草」三档，脚线处有一条水平硬边，上下两层颜色像台阶）。
    # 每段最高草高 h 只能铺到 y = −h / r，r = 0.9 × 相机高 ÷ 到前排距离，保证不挡前排蹄底
    r = 0.9 * cam.location.z / (-cam_y)
    y_of = lambda h: -h / r              # noqa: E731
    region = lambda y0, y1: (gx - half, gx + half, y0, y1)   # noqa: E731
    bands = [  # (最高草高, tall 缩放, tall1 缩放, 密度)：tall 原高 ≤ 0.40 m，tall1 ≤ 0.32 m
        (0.68, (1.0, 1.7), (1.2, 2.0), (2.2, 1.6)),
        (0.34, (0.6, 0.85), (0.7, 1.05), (2.5, 2.0)),
        (0.18, (0.35, 0.45), (0.4, 0.55), (3.0, 3.0)),
    ]
    y0 = y_near
    for k, (h, sa, sb, (da, db)) in enumerate(bands):
        y1 = y_of(h)
        scatter(f"grp_scatter_front_tall_a{k}", region(y0, y1), tall, da, *sa, seed=93 + k, patch=0.3, cast_shadow=False)
        scatter(f"grp_scatter_front_tall_b{k}", region(y0, y1), tall1, db, *sb, seed=96 + k, patch=0.3, cast_shadow=False)
        y0 = y1
    y_short = y_of(0.18)                 # short 原高 ≤ 0.15 m，缩放 ≤ 1.2
    y_small = y_of(0.09)
    scatter("grp_scatter_front_short", region(y_near, y_short), short, 8.0, 0.9, 1.2, seed=91, patch=0.3, cast_shadow=False)
    scatter("grp_scatter_front_small", region(y_short, y_small), short, 15.0, 0.5, 0.6, seed=92, patch=0.3, cast_shadow=False)
    scatter("grp_scatter_flat", region(y_small, row_depth + 1.0), flat, 30.0, 0.8, 1.0, seed=61, patch=0.5, cast_shadow=False)
    print("group front grass: cam_y %.1f cam_z %.2f bands %s small until %.1f" % (cam_y, cam.location.z, [round(y_of(b[0]), 1) for b in bands], y_small))
    # 合影机位远（约 600 m）、几乎平视：草要一直铺到远景板，否则中间露出一条光地面（第 3 版首测发白）
    y_plate = row_depth + 260.0
    scatter("grp_scatter_tall_a", (gx - half, gx + half, row_depth + 1.5, y_plate), tall, 1.4, 1.4, 2.6, seed=71, patch=0.75)
    scatter("grp_scatter_tall_b", (gx - half, gx + half, row_depth + 1.5, y_plate), tall1, 1.2, 1.8, 3.2, seed=81, patch=0.75)
    cam_z = cam.location.z
    tan_h = math.tan(cam.data.angle_x / 2)
    rnd = random.Random(17)
    for i in range(14):                 # 树别抢戏：少、靠后
        y = rnd.uniform(row_depth + 150, y_plate - 10)
        half_w = (y - cam_y) * tan_h * 1.2
        billboard(f"grp_env_tree_{i:02d}", rnd.choice(env["trees"]), rnd.uniform(4.5, 9.0), gx + rnd.uniform(-half_w, half_w), y)
    for i in range(30):
        y = rnd.uniform(row_depth + 25, y_plate - 20)
        half_w = (y - cam_y) * tan_h * 1.2
        billboard(f"grp_env_bush_{i:02d}", rnd.choice(env["bushes"]), rnd.uniform(0.9, 2.2), gx + rnd.uniform(-half_w, half_w), y)
    w_plate = (y_plate - cam_y) * tan_h * 2 * 1.6
    plate("grp_env_plate", env["plate"], gx, y_plate, w_plate, env["plate_horizon"], cam_z)
    for o in set(bpy.data.objects) - before:
        for c in list(o.users_collection):
            c.objects.unlink(o)
        coll.objects.link(o)
