"""真实尺度 · 整集场景（bible §2.2 / §2.3）：由 data.json 生成列队、镜头动画、全体合影与钩子镜头，写 timeline.json。

在 Blender 里运行（MCP 或 `blender --background --python`），先 exec scene_lineup.py，再 exec 本文件：
    build_episode(r"<集目录>")
产出：<集目录>/scene/ep.blend、_build/timeline.json、scale_check.json（bible §7 第 2、3 条）。
渲染由 render_ep.py 按 timeline.json 分段完成；叠加由 compose.py 完成。
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import bpy
from mathutils import Vector

FPS = 30
HOOK_S = 7.0
TITLE_S = 3.0
HOLD_S = 4.5
TOP_HOLD_S = 6.75        # 前 5 名 ×1.5（bible §2.2）
MOVE_S = 2.0
INSIGHT_S = 4.5
GROUP_S = 10.0
SOURCES_S = 15.0         # 来源卡兼片尾推荐位（bible §2.2：15–20 s）
FILL = 0.53              # 主体（或人）高度占画面高（0.58 时长颈鹿头顶、角尖离上沿仅 10–20 px，ep01 第 2 轮审片）
WIDTH_FILL = 0.78
GROUND_FROM_TOP = 0.66   # 地面线在画面中的高度（自上而下）；下方留给标签卡
PITCH_DEG = 2.0
LENS_MM = 135              # 长焦远机位：主体近侧 / 角尖离中线 ±0.6 m 时透视放大 ≤ 约 2.5%（35 mm 时达 11%）
REPO = Path(__file__).resolve().parents[3] if "__file__" in globals() else Path(r"C:\workspace\micro-drama-platform")


def _engine_eevee() -> str:
    items = [i.identifier for i in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items]
    for cand in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
        try:
            bpy.context.scene.render.engine = cand
            return cand
        except TypeError:
            continue
    return items[0]


def _world_and_sun() -> None:
    """内置天空纹理 + 太阳光（不引入外部 HDRI，许可零风险）。"""
    scene = bpy.context.scene
    world = scene.world or bpy.data.worlds.new("World")
    scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputWorld")
    bg = nt.nodes.new("ShaderNodeBackground")
    sky = nt.nodes.new("ShaderNodeTexSky")
    try:
        sky.sun_elevation = math.radians(40)
        sky.sun_rotation = math.radians(200)
    except AttributeError:
        pass
    bg.inputs["Strength"].default_value = 0.3
    nt.links.new(sky.outputs["Color"], bg.inputs["Color"])
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])
    for o in [o for o in scene.objects if o.type == "LIGHT"]:
        bpy.data.objects.remove(o, do_unlink=True)
    sun_data = bpy.data.lights.new("sun", "SUN")
    sun_data.energy = 3.2
    sun_data.angle = math.radians(2.0)
    sun = bpy.data.objects.new("sun", sun_data)
    scene.collection.objects.link(sun)
    sun.rotation_euler = (math.radians(42), 0.0, math.radians(-35))   # 从左前上方照，影子落到右后方
    vs = scene.view_settings
    for lk in ("AgX - Punchy", "AgX - Medium High Contrast"):
        try:
            vs.look = lk
            break
        except TypeError:
            continue
    vs.exposure = -0.3


def _shot(cam, x0: float, x1: float, h: float, depth: float) -> tuple[Vector, Vector]:
    fov_y, fov_x = cam.data.angle_y, cam.data.angle_x
    dist_h = (h / FILL / 2) / math.tan(fov_y / 2)
    dist_w = ((x1 - x0) / WIDTH_FILL / 2) / math.tan(fov_x / 2)
    dist = max(dist_h, dist_w) + depth / 2
    vis_h = 2 * (dist - depth / 2) * math.tan(fov_y / 2)
    tz = (GROUND_FROM_TOP - 0.5) * vis_h
    target = Vector(((x0 + x1) / 2, 0.0, tz))
    p = math.radians(PITCH_DEG)
    eye = target + Vector((0.0, -dist * math.cos(p), dist * math.sin(p)))
    rot = Vector((math.pi / 2 - p, 0.0, 0.0))
    return eye, rot


def _key(cam, eye, rot, frame) -> None:
    cam.location = eye
    cam.rotation_euler = rot
    cam.keyframe_insert("location", frame=frame)
    cam.keyframe_insert("rotation_euler", frame=frame)


def _project(cam, p: Vector) -> list[int]:
    from bpy_extras.object_utils import world_to_camera_view
    scene = bpy.context.scene
    co = world_to_camera_view(scene, cam, p)
    return [round(co.x * scene.render.resolution_x), round((1 - co.y) * scene.render.resolution_y)]


def build_episode(ep_dir: str, require_all: bool = True) -> dict:
    ep = Path(ep_dir)
    data = json.loads((ep / "data.json").read_text(encoding="utf-8"))
    scene = bpy.context.scene
    _clear()
    for nm in ("cam_hook", "cam_group", "sun"):
        if nm in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects[nm], do_unlink=True)
    for c in ("Group",):
        old = bpy.data.collections.get(c)
        if old:
            for o in list(old.objects):
                bpy.data.objects.remove(o, do_unlink=True)
    scene.render.fps = FPS
    scene.render.resolution_x, scene.render.resolution_y = 1920, 1080
    engine = _engine_eevee()
    _world_and_sun()

    missing = [it["name"] for it in data["items"] if not it.get("model")]
    if missing and require_all:
        raise ValueError(f"缺模型：{missing}")
    order = [it for it in reversed(data["items"]) if it.get("model")]   # 从小到大登场，冠军最后
    subjects = []
    x, prev_len = 0.0, 0.0
    for idx_rev, it in enumerate(order):
        m = it["model"]
        imp = dict(m["import"], key=m["key"], model_path=str(REPO / m["path"]))
        obj = import_model(imp)
        lo, hi = world_bbox(obj)
        k = it["dims"]["height_m"] / ((hi.z - lo.z) * m["landmark_ratio"])
        obj.scale = obj.scale * k
        bpy.context.view_layer.update()
        lo, hi = world_bbox(obj)
        length = hi.x - lo.x
        x += (max(prev_len, length) * 0.6 + 1.6) if subjects else 0.0
        obj.location += Vector((x - lo.x, -(lo.y + hi.y) / 2, -lo.z))
        bpy.context.view_layer.update()
        lo, hi = world_bbox(obj)
        # 人与动物中线同一纵深（y=0）：透视下两者缩放一致，画面比例才真（站在动物身后 0.85 m 处，不前不后）
        man = _human(f"human_{m['key']}")
        bpy.context.view_layer.update()
        mlo, mhi = world_bbox(man)
        man.location += Vector((x - 0.85 - (mlo.x + mhi.x) / 2, -(mlo.y + mhi.y) / 2, -mlo.z))
        frac = m.get("landmark_x_frac")
        marker_x = lo.x + frac * (hi.x - lo.x) if frac is not None else None
        obj["marker_x"] = marker_x if marker_x is not None else -1e9
        x += length
        prev_len = length
        subjects.append((it, obj, man))
    bpy.context.view_layer.update()
    depth = max(world_bbox(o)[1].y - world_bbox(o)[0].y for _, o, _ in subjects)
    _ground(x, depth)

    # 比例机检（bible §7 第 2、3 条）
    check = scale_check([(dict(key=it["model"]["key"], height_m=it["dims"]["height_m"],
                               landmark_ratio=it["model"]["landmark_ratio"]), o) for it, o, _ in subjects],
                        str(ep / "scale_check.json"))

    # 相机：列队
    cam = bpy.data.objects.get("Camera") or bpy.data.objects.new("Camera", bpy.data.cameras.new("Camera"))
    if cam.name not in scene.collection.all_objects:
        scene.collection.objects.link(cam)
    scene.camera = cam
    cam.data.type = "PERSP"
    cam.data.lens = LENS_MM
    cam.data.clip_end = 5000
    cam.animation_data_clear()
    f = 1
    timeline = {"fps": FPS, "segments": {}, "items": [], "insights": []}
    ins_after = {i["after_rank"]: n for n, i in enumerate(data["insights"])}
    n = len(subjects)
    lineup_start = f
    for i, (it, obj, man) in enumerate(subjects):
        lo, hi = world_bbox(obj)
        mlo, mhi = world_bbox(man)
        eye, rot = _shot(cam, min(lo.x, mlo.x), max(hi.x, mhi.x), max(hi.z - lo.z, (mhi.z - mlo.z) * 1.22), hi.y - lo.y)  # 人头顶留出标签位
        hold = TOP_HOLD_S if i >= n - 5 else HOLD_S
        a = f
        if i == 0:
            timeline["title"] = [a, a + int(TITLE_S * FPS)]
            a += int(TITLE_S * FPS)
        b = a + int(hold * FPS)
        c = b
        if it["rank"] in ins_after and i < n - 1:
            c = b + int(INSIGHT_S * FPS)
            timeline["insights"].append({"index": ins_after[it["rank"]], "frames": [b, c]})
        _key(cam, eye, rot, f)
        _key(cam, eye, rot, c)
        cam.data.keyframe_insert("lens", frame=f)
        bpy.context.scene.frame_set(a)
        man_head = _project(cam, Vector(((mlo.x + mhi.x) / 2, 0.0, mhi.z + 0.12)))
        mx = obj.get("marker_x", -1e9)
        marker = None if mx < -1e8 else {   # 肩高标线：在动物中线纵深（y=0）上投影，合成时画成 2D 线
            "base": _project(cam, Vector((mx, 0.0, 0.0))),
            "top": _project(cam, Vector((mx, 0.0, it["dims"]["height_m"])))}
        timeline["items"].append({
            "data_index": data["items"].index(it), "key": it["model"]["key"], "rank": it["rank"], "name": it["name"],
            "label": [a, b], "static": [f, c], "man_label_xy": man_head, "marker": marker,
        })
        f = c + int(MOVE_S * FPS) if i < n - 1 else c
    lineup_end = f
    timeline["segments"]["lineup"] = [lineup_start, lineup_end]
    # 关键帧默认贝塞尔（自动钳制句柄）：静止段两端同值 → 移动段自然缓入缓出

    # 钩子：冠军与前几名的剪影（材质覆盖成黑色，在渲染脚本里切换）
    top = subjects[-2:]
    x0 = min(min(world_bbox(o)[0].x, world_bbox(m)[0].x) for _, o, m in top)
    x1 = max(world_bbox(o)[1].x for _, o, _ in top)
    h = max(world_bbox(o)[1].z for _, o, _ in top)
    hook_cam = bpy.data.objects.new("cam_hook", bpy.data.cameras.new("cam_hook"))
    scene.collection.objects.link(hook_cam)
    hook_cam.data.lens = LENS_MM
    hook_cam.data.clip_end = 5000
    # 低机位平视 + 镜头上移（shift_y）：地平线压到画面下方 80% 处，剪影衬在夕阳天空上
    hook_cam.data.shift_y = 0.3 * 1080 / 1920
    vis_h = h / 0.52
    dist = max(vis_h / 2 / math.tan(hook_cam.data.angle_y / 2), (x1 - x0 + 2) / 2 / math.tan(hook_cam.data.angle_x / 2))
    e0 = Vector(((x0 + x1) / 2, -dist, 0.02))   # 机位贴地：地平线 = 脚底线，剪影完整露出（0.4 m 时人只露 1.35 m，长颈鹿看着像 5.8 m）
    r0 = Vector((math.pi / 2, 0.0, 0.0))
    e1 = e0 + Vector((0.0, dist * 0.05, 0.0))
    hook_start = lineup_end + 1
    _key(hook_cam, e0, r0, hook_start)
    _key(hook_cam, e1, r0, hook_start + int(HOOK_S * FPS) - 1)
    timeline["segments"]["hook"] = [hook_start, hook_start + int(HOOK_S * FPS) - 1]

    # 全体合影：按名次分三排（小的在前、大的在后），正交相机保证真实比例
    grp = bpy.data.collections.get("Group") or bpy.data.collections.new("Group")
    if grp.name not in scene.collection.children:
        scene.collection.children.link(grp)
    # 五排合影站位（小的在前、大的在后），正交相机俯拍：没有透视，前后排比例完全真实；地面 1 m 格当尺子
    rows = [subjects[i:i + 6] for i in range(0, len(subjects), 6)]
    row_gap = 2.6
    widest = 0.0
    placed = []
    for t, row in enumerate(rows):
        lens = [world_bbox(o)[1].x - world_bbox(o)[0].x for _, o, _ in row]
        step = sum(lens) / len(lens) * 0.9
        span = step * (len(row) - 1) + lens[-1]
        xs = [-span / 2 + step * j for j in range(len(row))]
        widest = max(widest, span)
        for j, (it, o, _) in enumerate(row):
            dup = o.copy()
            dup.name = f"grp_{it['model']['key']}"
            grp.objects.link(dup)
            lo, hi = world_bbox(o)
            dup.location = o.location + Vector((xs[j] - lo.x + 20000, t * row_gap + (j % 2) * 0.6 - (lo.y + hi.y) / 2, 0))
            placed.append(dup)
    tpl = bpy.data.objects.get(HUMAN_TEMPLATE)
    gman = tpl.copy()
    gman.name = "grp_human"
    gman.hide_render = False
    grp.objects.link(gman)
    bpy.context.view_layer.update()                 # 副本刚改位置，先刷新世界矩阵再量
    front_lo = min(world_bbox(o)[0].x for o in placed[:len(rows[0])])
    gman.location = (front_lo - 0.9, -0.3, 0)      # 紧挨第一排最左一只
    gplane = bpy.data.objects["ground"].copy()
    gplane.name = "grp_ground"
    gplane.location = (20000, 0, 0)
    grp.objects.link(gplane)
    gcam = bpy.data.objects.new("cam_group", bpy.data.cameras.new("cam_group"))
    scene.collection.objects.link(gcam)
    gcam.data.type = "ORTHO"
    gcam.data.clip_end = 5000
    p = math.radians(15)
    depth_rows = row_gap * (len(rows) - 1)
    hmax = max(world_bbox(o)[1].z for o in placed)
    vis_h_needed = depth_rows * math.sin(p) + hmax * math.cos(p) + 1.0
    s0 = max((widest + 3.0) / 0.92, vis_h_needed / 0.84 * 16 / 9)
    vis_h = s0 * 9 / 16
    # 画面竖向：前排脚底放在离底 20% 处
    front = Vector((20000, -0.5, 0.0))
    up = Vector((0, math.sin(p), math.cos(p)))       # 相机屏幕「上」方向
    fwd = Vector((0, math.cos(p), -math.sin(p)))     # 视线方向
    tgt = front + up * (vis_h * 0.30)
    gcam.location = tgt - fwd * 300
    gcam.rotation_euler = (math.pi / 2 - p, 0, 0)
    g0 = hook_start + int(HOOK_S * FPS)
    g1 = g0 + int(GROUP_S * FPS) - 1
    gcam.data.ortho_scale = s0 * 1.05
    gcam.data.keyframe_insert("ortho_scale", frame=g0)
    gcam.data.ortho_scale = s0
    gcam.data.keyframe_insert("ortho_scale", frame=g1)
    timeline["segments"]["group"] = [g0, g1]
    gl = []
    for fr in (g0, g1):
        scene.frame_set(fr)
        gm_lo, gm_hi = world_bbox(gman)
        gl.append(_project(gcam, Vector(((gm_lo.x + gm_hi.x) / 2, (gm_lo.y + gm_hi.y) / 2, gm_hi.z + 0.12))))
    timeline["group_man_label_xy"] = gl     # 合影首帧、末帧的人头顶位置（正交缩放期间线性插值）
    timeline["sources_s"] = SOURCES_S
    timeline["engine"] = engine
    scene.frame_start, scene.frame_end = 1, g1

    (ep / "_build").mkdir(exist_ok=True)
    (ep / "_build" / "timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=1), encoding="utf-8")
    (ep / "scene").mkdir(exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(ep / "scene" / "ep.blend"))
    return {"scale_check_all_pass": check["all_pass"], "lineup_frames": lineup_end, "length_m": x}
