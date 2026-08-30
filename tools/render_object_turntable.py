"""从白模 .blend 渲一套 object 多角度参考盘（静帧 ×8 + 10s 转盘 MP4）。

用法（仓库根目录）：
    blender -b --factory-startup --python tools/render_object_turntable.py -- \
        --blend ai_videos/duikang_shangzeng/2_世界观人设/props/f80_ferrari/f80_ferrari.blend \
        --out   ai_videos/duikang_shangzeng/2_世界观人设/props/f80_ferrari/whitemodel \
        --name  f80_ferrari
    # 只渲静帧（快）：加 --stills-only

对齐 ai_video.md rule 12.5 的**人物** 7s turntable 契约，改造为 **object 10s 版**：
    人物 3 个静止落点（0°/90°/180°）→ object 5 个（0°/45°/90°/135°/180°）。
    车的身份比人脸分布在更多视角上：前四分之三看肩线、正侧看比例、
    后四分之三看轮拱与尾翼——少一个角度，模型就会自己编一个。

**跨角度 framing 恒定**是这套盘能当 reference 用的前提：
    同一焦距、同一相机距离、同一主体居中、同一光位，只有方位角在变。
    任何一项跟着角度变，模型就会把"变化"也学进去。

产物：
    {out}/angles/{name}_{tag}.png     ×8   → Seedance 图像参考位（结构锁）
    {out}/{name}_turntable.mp4        10s  → Seedance reference_video 位（形体锁）
    {out}/{name}_turntable_frames/    PNG 序列（无 FFMPEG 构建时的退路）
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

REPO = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- 契约常量
#
# 10s 转盘时刻表：5 个静止落点 + 4 段旋转。抽帧时间戳锁在静止落点的中点——
# 与人物 turntable 的 (front 1.0 / side 3.5 / back 6.0) 同构。
#
#   0.0-1.5s  静止 0°     正面
#   1.5-2.2s  转到 45°
#   2.2-3.5s  静止 45°    前四分之三   ← 主参考
#   3.5-4.2s  转到 90°
#   4.2-5.5s  静止 90°    正侧
#   5.5-6.2s  转到 135°
#   6.2-7.5s  静止 135°   后四分之三
#   7.5-8.2s  转到 180°
#   8.2-10.0s 静止 180°   正后
TURNTABLE_SCHEDULE = [
    # (t_start, t_end, azimuth_deg, is_static)
    (0.0, 1.5, 0.0, True),
    (1.5, 2.2, 45.0, False),
    (2.2, 3.5, 45.0, True),
    (3.5, 4.2, 90.0, False),
    (4.2, 5.5, 90.0, True),
    (5.5, 6.2, 135.0, False),
    (6.2, 7.5, 135.0, True),
    (7.5, 8.2, 180.0, False),
    (8.2, 10.0, 180.0, True),
]

# 下游抽帧契约：静止落点的中点。改这里必须同步改 f80_ferrari.md §3。
CANONICAL_VIEWS = [
    ("front",     0.0,  0.75, "正面 0°"),
    ("front3q",  45.0,  2.85, "前四分之三 45°  ← 主参考"),
    ("side",     90.0,  4.85, "正侧 90°"),
    ("rear3q",  135.0,  6.85, "后四分之三 135°"),
    ("rear",    180.0,  9.10, "正后 180°"),
]

# 另外两个不在转盘上的角度（转盘只绕水平一圈，这两个要单独渲）
EXTRA_VIEWS = [
    ("top",   45.0, 78.0, "顶视俯拍 — 无人机镜用"),
    ("low3q", 40.0,  4.0, "贴地前四分之三 — 速度镜用"),
]

TURNTABLE_SEC = 10.0
ELEV_DEG = 8.0      # 转盘的固定俯角：略高于车顶，能同时看到车顶面与侧面
FOCAL_MM = 85.0     # 长焦压缩，减少透视畸变——参考图要的是比例真实，不是空间感


def parse_args() -> argparse.Namespace:
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--blend", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--fps", type=int, default=25)
    ap.add_argument("--res", default="1920x1080")
    ap.add_argument("--stills-only", action="store_true")
    return ap.parse_args(argv)


def clay_material(name: str, v: float) -> bpy.types.Material:
    """节点化灰模材质。

    必须走节点：`use_nodes=False` + `diffuse_color` 只是**视口显示色**，
    Workbench 认、EEVEE 不认——EEVEE 会退回默认近白表面，于是车、地面、背景
    渲成同一片白，剪影彻底读不出来。灰模的明度是可读性的一部分，不能碰运气。
    """
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (v, v, v * 1.02, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.65
    if "Specular IOR Level" in bsdf.inputs:
        bsdf.inputs["Specular IOR Level"].default_value = 0.2   # 压高光，别在灰模上造假亮斑
    return m


def strip_and_clay(objects) -> int:
    """无条件剥掉源档材质，换成统一灰模。

    白模只承载几何，不承载长相与材质——所以渲染器不该相信源档的材质。
    这条对将来换 image-to-3D 生成的网格尤其重要：那类模型自带烤死的贴图与颜色，
    正是必须被剥掉的东西。
    """
    clay = clay_material("TT_CLAY", 0.62)
    n = 0
    for ob in objects:
        if ob.type != "MESH":
            continue
        ob.data.materials.clear()
        ob.data.materials.append(clay)
        n += 1
    return n


def setup_world_and_lights(radius: float) -> None:
    """中性灰无缝背景 + 三点布光。跨所有角度恒定。"""
    w = bpy.data.worlds.new("TT_WORLD")
    w.use_nodes = True                      # 同上：非节点世界色 EEVEE 不读
    _bg = w.node_tree.nodes.get("Background")
    # 背景压到明显低于灰模（灰模 0.62）。原来背景/地面/模型三者明度几乎相同，
    # 剪影融进背景——白模最该被看清的东西反而看不见。
    _bg.inputs[0].default_value = (0.13, 0.14, 0.17, 1.0)
    _bg.inputs[1].default_value = 1.0
    bpy.context.scene.world = w

    # 无缝地面（cyc wall 的简化：一块大灰板，避免地平线切割主体）
    bpy.ops.mesh.primitive_plane_add(size=radius * 400, location=(0, 0, 0))
    ground = bpy.context.object
    ground.name = "TT_GROUND"
    ground.data.materials.append(clay_material("TT_GROUND_MAT", 0.16))  # 地面压深，托出接地阴影

    # 主:补 由 2.5:1 拉到 5.6:1。补光太强＝平光，灰模在平光下读不出曲面往哪拐。
    for tag, rot, energy in [
        ("KEY",  (math.radians(40), 0.0, math.radians(40)),  5.0),
        ("FILL", (math.radians(62), 0.0, math.radians(-75)), 0.9),
        ("RIM",  (math.radians(72), 0.0, math.radians(190)), 3.0),
    ]:
        li = bpy.data.lights.new(f"TT_{tag}", type="SUN")
        li.energy = energy
        li.angle = math.radians(6)
        ob = bpy.data.objects.new(f"TT_{tag}", li)
        ob.rotation_euler = rot
        bpy.context.collection.objects.link(ob)


def place_camera(cam, subject_center: Vector, dist: float, azim_deg: float, elev_deg: float) -> None:
    """把相机放在球面上并对准主体中心。距离与焦距全程不变——这是参考盘的命门。"""
    a, e = math.radians(azim_deg), math.radians(elev_deg)
    cam.location = subject_center + Vector((
        dist * math.cos(e) * math.sin(a),
        -dist * math.cos(e) * math.cos(a),
        dist * math.sin(e),
    ))
    d = (subject_center - cam.location).normalized()
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def main() -> None:
    args = parse_args()
    blend = (REPO / args.blend).resolve() if not Path(args.blend).is_absolute() else Path(args.blend)
    out = (REPO / args.out).resolve() if not Path(args.out).is_absolute() else Path(args.out)
    if not blend.is_file():
        raise SystemExit(f"白模档不存在：{blend}")

    bpy.ops.wm.open_mainfile(filepath=str(blend))
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    if not meshes:
        raise SystemExit(f"{blend} 里没有 MESH 物体")

    # 主体包围盒 → 中心与外接半径
    lo = Vector((1e9, 1e9, 1e9))
    hi = Vector((-1e9, -1e9, -1e9))
    for o in meshes:
        for c in o.bound_box:
            p = o.matrix_world @ Vector(c)
            lo = Vector((min(lo[i], p[i]) for i in range(3)))
            hi = Vector((max(hi[i], p[i]) for i in range(3)))
    center = (lo + hi) / 2.0
    dims = hi - lo
    radius = max(dims) / 2.0
    print(f"  主体包围盒 X {dims.x:.2f} × Y {dims.y:.2f} × Z {dims.z:.2f}，外接半径 {radius:.2f}")

    n_clay = strip_and_clay(meshes)
    print(f"  灰模化：剥掉源档材质，{n_clay} 件网格换成统一灰模")

    setup_world_and_lights(radius)

    scene = bpy.context.scene
    W, H = (int(x) for x in args.res.lower().split("x"))
    scene.render.resolution_x, scene.render.resolution_y = W, H
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = False
    # Blender 5.x 的枚举只有 "BLENDER_EEVEE"（"..._NEXT" 这个名字在 4.2 之后已撤销）。
    # 回退目标必须仍是 EEVEE——落到 Workbench 会静默丢掉 AO 与 Freestyle
    # （Workbench 不支持 Freestyle），白模就又渲回一片平灰。
    for _eng in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
        try:
            scene.render.engine = _eng
            break
        except TypeError:
            continue
    else:
        raise SystemExit("找不到 EEVEE 引擎；Workbench 不支持 Freestyle，不能当回退")

    # 形状可读性：与 tools/previz/build_previz.py 同一套配置，保持两处白模观感一致。
    # 白模只承载几何——所以几何必须被渲得看得见，否则形状信息在渲染这一步就丢了。
    if scene.render.engine.startswith("BLENDER_EEVEE"):
        scene.eevee.use_raytracing = True
        scene.eevee.use_fast_gi = True
        scene.eevee.fast_gi_method = "AMBIENT_OCCLUSION_ONLY"
        scene.eevee.fast_gi_distance = 0.6
        scene.eevee.fast_gi_ray_count = 4
        scene.eevee.fast_gi_step_count = 12
        scene.eevee.taa_render_samples = max(scene.eevee.taa_render_samples, 48)
    # Freestyle 只对低面数灰模有价值：粗模靠描边才读得出转折，
    # 高面数网格靠 AO+三点光就够，且 Freestyle 在生成网格的非流形拓扑上会崩
    # （Blender 5.1: FEdgeSmooth.normal_left）。按面数自动决定开不开。
    _dense = sum(len(o.data.polygons) for o in bpy.context.scene.objects if o.type == "MESH")
    scene.render.use_freestyle = _dense < 200000
    print(f"  Freestyle: {'开' if scene.render.use_freestyle else '关（%d 面，高面数靠 AO 读型面）' % _dense}")
    scene.render.line_thickness_mode = "ABSOLUTE"
    scene.render.line_thickness = 1.0
    _fs = bpy.context.view_layer.freestyle_settings
    for _ls in list(_fs.linesets):
        _fs.linesets.remove(_ls)
    _ls = _fs.linesets.new("TT_FORM")
    _ls.select_silhouette = True
    _ls.select_border = True
    _ls.select_crease = True
    _ls.select_ridge_valley = True
    _ls.select_contour = False
    _fs.crease_angle = math.radians(130)
    _ls.linestyle.color = (0.05, 0.05, 0.06)
    _ls.linestyle.thickness = 1.4

    cam_data = bpy.data.cameras.new("TT_CAM")
    cam_data.lens = FOCAL_MM
    cam = bpy.data.objects.new("TT_CAM", cam_data)
    scene.collection.objects.link(cam)
    scene.camera = cam

    # 相机距离：主体最长边在画宽里占 target_frac，全角度恒定。
    # 恒定距离意味着正面视角看起来比正侧小——这是**对的**：真实转盘就是这样，
    # 模型要学的是「这台车从各个角度分别是什么样」，不是「每个角度都填满画面」。
    sensor = cam_data.sensor_width               # 36mm，sensor_fit=AUTO 作用于长边
    target_frac = 0.78
    subject_extent = max(dims.x, dims.y)
    dist = subject_extent * FOCAL_MM / (sensor * target_frac)
    print(f"  相机距离锁定 {dist:.2f}m，焦距 {FOCAL_MM:.0f}mm（全角度恒定）")

    # ---- 静帧 ×8
    angles_dir = out / "angles"
    angles_dir.mkdir(parents=True, exist_ok=True)
    for tag, azim, _t, note in CANONICAL_VIEWS:
        place_camera(cam, center, dist, azim, ELEV_DEG)
        scene.render.filepath = str(angles_dir / f"{args.name}_{tag}.png")
        bpy.ops.render.render(write_still=True)
        print(f"  ✓ {tag:8s} {note}")
    for tag, azim, elev, note in EXTRA_VIEWS:
        place_camera(cam, center, dist, azim, elev)
        scene.render.filepath = str(angles_dir / f"{args.name}_{tag}.png")
        bpy.ops.render.render(write_still=True)
        print(f"  ✓ {tag:8s} {note}")

    if args.stills_only:
        print("  --stills-only：跳过转盘视频")
        return

    # ---- 10s 转盘：按 TURNTABLE_SCHEDULE 打关键帧（静止段前后两帧同角度＝真静止）
    fps = args.fps
    scene.render.fps = fps
    scene.frame_start = 1
    scene.frame_end = int(TURNTABLE_SEC * fps)
    cam.animation_data_clear()
    for t0, t1, azim0, is_static in TURNTABLE_SCHEDULE:
        if is_static:
            steps = [(t0, azim0), (t1, azim0)]
        else:
            # 旋转段：相机走的是圆弧，但关键帧之间是直线插值——两帧之间会切一条弦，
            # 相机在段中点离主体更近（45° 一步误差约 7.6%）。每 15° 补一帧压掉它。
            prev = TURNTABLE_SCHEDULE[TURNTABLE_SCHEDULE.index((t0, t1, azim0, is_static)) - 1]
            a_from = prev[2]
            n = max(1, int(round(abs(azim0 - a_from) / 15.0)))
            steps = [(t0 + (t1 - t0) * i / n, a_from + (azim0 - a_from) * i / n)
                     for i in range(n + 1)]
        for t, azim in steps:
            place_camera(cam, center, dist, azim, ELEV_DEG)
            f = max(1, int(round(t * fps)) + 1)
            cam.keyframe_insert("location", frame=f)
            cam.keyframe_insert("rotation_euler", frame=f)

    # Blender 4.4+ / 5.x 的 slotted actions 移除了 action.fcurves，改走 layers→strips→channelbags
    def _fcurves(action):
        if hasattr(action, "fcurves"):
            return list(action.fcurves)
        out = []
        for layer in getattr(action, "layers", []):
            for strip in getattr(layer, "strips", []):
                for cb in getattr(strip, "channelbags", []):
                    out.extend(cb.fcurves)
        return out

    for fc in _fcurves(cam.animation_data.action):
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"

    frames_dir = out / f"{args.name}_turntable_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = str(frames_dir / "f_")
    bpy.ops.render.render(animation=True)
    n = len(list(frames_dir.glob("*.png")))
    print(f"  ✓ 转盘 PNG 序列 {n} 帧 → {frames_dir.relative_to(REPO)}")
    print(f"    合成 MP4：ffmpeg -framerate {fps} -i \"{frames_dir}/f_%04d.png\" "
          f"-c:v libx264 -pix_fmt yuv420p \"{out}/{args.name}_turntable.mp4\"")

    print("\n  下游抽帧契约（静止落点中点，与人物 turntable 同构）：")
    for tag, azim, t, note in CANONICAL_VIEWS:
        print(f"    {tag:8s} t={t:.2f}s  方位角 {azim:5.1f}°  {note}")


main()
