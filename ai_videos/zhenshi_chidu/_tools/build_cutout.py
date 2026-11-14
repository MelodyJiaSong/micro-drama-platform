"""真实尺度 · 2.5D 整集场景（ep01 第 2 版，用户 2026-11-07 选 B）：主体是 Codex 侧面参考图的抠像平面，
按肩线像素精确缩放；真实草原环境（Poly Haven CC0 HDRI + 地面贴图）、太阳投影、接触阴影。

    blender -b --python ai_videos/zhenshi_chidu/_tools/build_cutout.py -- <集目录>

读 data.json 与 assets/cutouts/cutouts.json（_tools/cutouts.py 产出）；节奏、镜头构图与 build_ep.py 相同
（exec 进来复用 _shot/_key/_project 与时长常量），所以 timeline 时长不变、配乐不用重拼。
产出：scene/ep.blend、_build/timeline.json、scale_check.json。渲染仍用 render_ep.py。

几何约定：
- 抠像平面立在 y=0（动物中线），宽 = 像素宽 × 米/像素，米/像素 = 肩高 ÷ (剪影底行 − 肩顶行)；平面底边对齐剪影底行 → 蹄底 z=0。
- 人同样是抠像平面：剪影总高（发顶到鞋底）= 1.75 m，站在动物身后 0.85 m（同一纵深，透视比例一致）。
- 合影：同一批平面的副本，五排前小后大，长焦远机位（约 600 m，前后排透视差 ≤ 约 2%），带天空。
- 钩子：日落 HDRI 逆光，平面发光强度置 0 = 黑色剪影（render_ep.py 切换）。
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import bpy
import numpy as np
from mathutils import Vector

TOOLS = Path(__file__).resolve().parent
REPO = TOOLS.parents[2]
SHARED = TOOLS.parent / "_shared"
exec(compile((TOOLS / "scene_lineup.py").read_text(encoding="utf-8"), str(TOOLS / "scene_lineup.py"), "exec"))
exec(compile((TOOLS / "build_ep.py").read_text(encoding="utf-8"), str(TOOLS / "build_ep.py"), "exec"))
SCENE_ENV = TOOLS / "scene_env.py"     # 第 3 版精细环境（远景板 + 中景树 + 3D 草），在 build() 里 exec

HDRI_DAY = SHARED / "hdri" / "mpumalanga_veld_8k.hdr"   # 135 mm 下 4k 的远景树木成像素块
HDRI_HOOK = SHARED / "hdri" / "plains_sunset_4k.hdr"     # 第 4 轮审片：Safari Sunset 那一面是灰白雾天，不像日落
GROUND_TEX = SHARED / "tex" / "grass_ground"
SUN_DAY_DIR = Vector((-0.85, -0.35, 0.0))     # 第 3 版：太阳在左前方（与远景板一致从左照），草被照亮呈金黄；原 (−0.80, 0.40)      # 太阳灯在左侧略偏后：影子朝相机右前方落下（平视时身后的地面看不见，影子要落在前面才看得到）
U_VIEW_DAY = 0.90        # 列队相机（看 +y）对着 HDRI 的哪一列：背光一侧的蓝天与远方平缓地平线（0.10 的台地方向天空过曝成白）
U_VIEW_GROUP = 0.955     # 合影视角只有约 2.6°：对着空旷的远方地平线，避免近处树被放大成一团
SUN_HOOK_DIR = Vector((0.04, 1.0, 0.0))       # 钩子逆光：太阳在剪影背后
GROUP_DIST = 600.0
SUN_ELEV_DEG = 40.0      # 太阳灯仰角固定：HDRI 里的太阳太低，30 个平面的影子会横扫整片地面
FSTOP = 2.8              # 列队长焦景深：主体（y=0）清楚，远处地面与天际线柔化，像长焦实拍
PITCH_DEG = 0.0          # 覆盖 build_ep：平视，地平线在画面正中，天空占上半；竖线不汇聚
HORIZON_FROM_TOP = 0.50  # 合影：平视，地平线在画面正中，大个子的上半身衬在天空上


# ---------- 材质与平面 ----------

def _cut_material(key: str, png: Path) -> bpy.types.Material:
    img = bpy.data.images.load(str(png), check_existing=True)
    img.alpha_mode = "STRAIGHT"
    m = bpy.data.materials.new("cut_" + key)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.interpolation = "Cubic"
    tex.extension = "CLIP"
    em = nt.nodes.new("ShaderNodeEmission")
    val = nt.nodes.new("ShaderNodeValue")
    val.name = val.label = "cut_strength"          # render_ep.py 钩子段置 0 → 黑剪影
    val.outputs[0].default_value = 1.0
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(tex.outputs["Color"], em.inputs["Color"])
    nt.links.new(val.outputs[0], em.inputs["Strength"])
    nt.links.new(tex.outputs["Alpha"], mix.inputs["Fac"])
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    for attr, v in (("surface_render_method", "DITHERED"), ("blend_method", "HASHED"), ("use_transparent_shadow", True)):
        try:
            setattr(m, attr, v)
        except (AttributeError, TypeError):
            pass
    return m


def _cut_plane(name: str, key: str, info: dict, mpp: float) -> bpy.types.Object:
    """原点在底边中点；平面在 XZ 面内，正对 −y 方向的相机。"""
    w_px, h_px = info["size"]
    w, h = w_px * mpp, h_px * mpp
    z0 = -(h_px - 1 - info["bottom"]) * mpp
    me = bpy.data.meshes.new(name)
    me.from_pydata([(-w / 2, 0, z0), (w / 2, 0, z0), (w / 2, 0, z0 + h), (-w / 2, 0, z0 + h)], [], [(0, 1, 2, 3)])
    uv = me.uv_layers.new(name="UVMap")
    for li, co in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]):
        uv.data[li].uv = co
    me.materials.append(_cut_material(key, REPO / info["png"]))
    ob = bpy.data.objects.new(name, me)
    _link(ob)
    ob["mpp"] = mpp
    ob["px_w"] = w_px
    # 平面剪影不投影：侧光下一张竖直平面的影子被压成贴地细线，相邻动物的连成横贯全画面的黑线（第 3 版成片自查发现）；
    # 接地感由 _blob 的柔和接触阴影提供
    ob.visible_shadow = False
    return ob


def _blob(name: str, cx: float, length: float, depth: float = 1.0, alpha: float = 0.6) -> bpy.types.Object:
    """接触阴影：脚下一块径向渐变的半透明黑。"""
    me = bpy.data.meshes.new(name)
    me.from_pydata([(-0.5, -0.5, 0), (0.5, -0.5, 0), (0.5, 0.5, 0), (-0.5, 0.5, 0)], [], [(0, 1, 2, 3)])
    ob = bpy.data.objects.new(name, me)
    ob.location = (cx, 0.0, 0.004)
    ob.scale = (length * 1.05, depth, 1)
    m = bpy.data.materials.get("contact_shadow")
    if m is None:
        m = bpy.data.materials.new("contact_shadow")
        m.use_nodes = True
        nt = m.node_tree
        nt.nodes.clear()
        tc = nt.nodes.new("ShaderNodeTexCoord")
        sub = nt.nodes.new("ShaderNodeVectorMath")
        sub.operation = "SUBTRACT"
        sub.inputs[1].default_value = (0.5, 0.5, 0.0)
        ln = nt.nodes.new("ShaderNodeVectorMath")
        ln.operation = "LENGTH"
        mr = nt.nodes.new("ShaderNodeMapRange")
        mr.inputs["From Min"].default_value = 0.0
        mr.inputs["From Max"].default_value = 0.5
        mr.inputs["To Min"].default_value = alpha
        mr.inputs["To Max"].default_value = 0.0
        pw = nt.nodes.new("ShaderNodeMath")
        pw.operation = "POWER"
        pw.inputs[1].default_value = 1.6
        tr = nt.nodes.new("ShaderNodeBsdfTransparent")
        dk = nt.nodes.new("ShaderNodeEmission")
        dk.inputs["Color"].default_value = (0, 0, 0, 1)
        mix = nt.nodes.new("ShaderNodeMixShader")
        out = nt.nodes.new("ShaderNodeOutputMaterial")
        nt.links.new(tc.outputs["Generated"], sub.inputs[0])
        nt.links.new(sub.outputs[0], ln.inputs[0])
        nt.links.new(ln.outputs["Value"], mr.inputs["Value"])
        nt.links.new(mr.outputs["Result"], pw.inputs[0])
        nt.links.new(pw.outputs[0], mix.inputs["Fac"])
        nt.links.new(tr.outputs[0], mix.inputs[1])
        nt.links.new(dk.outputs[0], mix.inputs[2])
        nt.links.new(mix.outputs[0], out.inputs["Surface"])
        for attr, v in (("surface_render_method", "BLENDED"), ("blend_method", "BLEND")):
            try:
                setattr(m, attr, v)
            except (AttributeError, TypeError):
                pass
        try:
            m.shadow_method = "NONE"
        except (AttributeError, TypeError):
            pass
    me.materials.append(m)
    try:
        ob.visible_shadow = False
    except AttributeError:
        pass
    _link(ob)
    return ob


# ---------- 环境 ----------

def _hdri_sun(img: bpy.types.Image) -> Vector:
    """HDRI 里最亮像素 → 世界方向（Blender 等距柱状投影：u = 0.5 − atan2(y, −x)/2π，v = 0.5 + 仰角/π）。"""
    w, h = img.size
    px = np.empty(w * h * 4, dtype=np.float32)
    img.pixels.foreach_get(px)
    lum = px.reshape(h, w, 4)[:, :, :3].sum(axis=2)
    j, i = np.unravel_index(int(np.argmax(lum)), lum.shape)
    u, v = (i + 0.5) / w, (j + 0.5) / h
    a = (0.5 - u) * 2 * math.pi
    el = (v - 0.5) * math.pi
    return Vector((-math.cos(a) * math.cos(el), math.sin(a) * math.cos(el), math.sin(el)))


def theta_for_u(u: float) -> float:
    """映射节点绕 Z 的角度，使看 +y 方向的相机对着 HDRI 第 u 列。"""
    a = (0.5 - u) * 2 * math.pi
    return math.pi / 2 - a


def make_world(name: str, hdr: Path, sun_target: Vector | None, strength: float,
               u_view: float | None = None) -> tuple[bpy.types.World, Vector]:
    """HDRI 世界：给 u_view 时让相机正对那一列，否则绕 Z 旋转使 HDRI 里的太阳落到 sun_target 方位。返回 (世界, 太阳的世界方向)。"""
    img = bpy.data.images.load(str(hdr), check_existing=True)
    d_img = _hdri_sun(img)
    if u_view is not None:
        theta = theta_for_u(u_view)
    else:
        theta = math.atan2(d_img.y, d_img.x) - math.atan2(sun_target.y, sun_target.x)
    w = bpy.data.worlds.get(name) or bpy.data.worlds.new(name)
    w.use_nodes = True
    nt = w.node_tree
    nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Rotation"].default_value[2] = theta
    env = nt.nodes.new("ShaderNodeTexEnvironment")
    env.image = img
    env.interpolation = "Cubic"     # 长焦放大 HDRI：线性插值出像素块
    bg = nt.nodes.new("ShaderNodeBackground")
    bg.inputs["Strength"].default_value = strength
    out = nt.nodes.new("ShaderNodeOutputWorld")
    nt.links.new(tc.outputs["Generated"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], env.inputs["Vector"])
    nt.links.new(env.outputs["Color"], bg.inputs["Color"])
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])
    c, s = math.cos(-theta), math.sin(-theta)
    d_w = Vector((c * d_img.x - s * d_img.y, s * d_img.x + c * d_img.y, d_img.z))
    w["sun_dir"] = list(d_w)
    w["hdri"] = hdr.name
    w.use_fake_user = True          # 钩子用的世界平时没挂在场景上，存盘会被丢
    return w, d_w


def make_sun(name: str, d_w: Vector, energy: float) -> bpy.types.Object:
    ld = bpy.data.lights.new(name, "SUN")
    ld.energy = energy
    ld.angle = math.radians(1.5)
    ob = bpy.data.objects.new(name, ld)
    bpy.context.scene.collection.objects.link(ob)
    hz = Vector((d_w.x, d_w.y, 0.0)).normalized()
    el = math.radians(SUN_ELEV_DEG) if d_w.z < math.sin(math.radians(SUN_ELEV_DEG)) and name == "sun_day" else math.asin(max(-1, min(1, d_w.z)))
    d = Vector((hz.x * math.cos(el), hz.y * math.cos(el), math.sin(el)))
    ob.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
    return ob


HAZE = (0.30, 0.20, 0.06, 1)        # 列队：远处地面淡到树林根部的暗橄榄色，地平线不再是亮地对暗树的硬边
HAZE_GROUP = (0.47, 0.50, 0.52, 1)  # 合影：对着空旷远方，淡到地平线处的浅灰蓝
PARALLAX_D = 400.0                  # 远景视差：相机每横移 PARALLAX_D 米，HDRI 转 1 弧度（远处树林约在 400 m 外）


def ground_material(name: str = "ground_veld", fade_min: float = 150.0, fade_max: float = 900.0,
                    haze_color: tuple = HAZE) -> bpy.types.Material:
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sc = nt.nodes.new("ShaderNodeVectorMath")
    sc.operation = "SCALE"
    sc.inputs["Scale"].default_value = 1 / 2.51          # 贴图实际 2.51 m 见方
    nt.links.new(geo.outputs["Position"], sc.inputs[0])

    def tex(fn: str, non_color: bool):
        t = nt.nodes.new("ShaderNodeTexImage")
        t.image = bpy.data.images.load(str(GROUND_TEX / fn), check_existing=True)
        if non_color:
            t.image.colorspace_settings.name = "Non-Color"
        nt.links.new(sc.outputs[0], t.inputs["Vector"])
        return t
    diff = tex("grass_ground_diff_2k.jpg", False)
    rough = tex("grass_ground_rough_2k.jpg", True)
    nor = tex("grass_ground_nor_gl_2k.jpg", True)
    hsv = nt.nodes.new("ShaderNodeHueSaturation")       # 往草原的干黄调：色相略偏黄、提一点亮度
    hsv.inputs["Hue"].default_value = 0.47           # 第 3 版：调成与远景板一致的金黄草原色
    hsv.inputs["Saturation"].default_value = 1.35
    hsv.inputs["Value"].default_value = 1.45
    nt.links.new(diff.outputs["Color"], hsv.inputs["Color"])
    # 大尺度明暗起伏，打散 2.5 m 贴图的重复
    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 0.035
    nt.links.new(geo.outputs["Position"], noise.inputs["Vector"])
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs["To Min"].default_value = 0.78
    mr.inputs["To Max"].default_value = 1.12
    nt.links.new(noise.outputs["Fac"], mr.inputs["Value"])
    mul = nt.nodes.new("ShaderNodeMix")
    mul.data_type = "RGBA"
    mul.blend_type = "MULTIPLY"
    mul.inputs["Factor"].default_value = 1.0
    nt.links.new(hsv.outputs["Color"], mul.inputs[6])
    nt.links.new(mr.outputs["Result"], mul.inputs[7])
    # 远处淡到平均色：掠射角下贴图会出摩尔纹（ep01 第 3 轮审片）
    cam = nt.nodes.new("ShaderNodeCameraData")
    fade = nt.nodes.new("ShaderNodeMapRange")
    fade.inputs["From Min"].default_value = fade_min
    fade.inputs["From Max"].default_value = fade_max
    nt.links.new(cam.outputs["View Distance"], fade.inputs["Value"])
    avg = nt.nodes.new("ShaderNodeMix")
    avg.data_type = "RGBA"
    nt.links.new(fade.outputs["Result"], avg.inputs["Factor"])
    nt.links.new(mul.outputs[2], avg.inputs[6])
    avg.inputs[7].default_value = (0.30, 0.21, 0.08, 1)
    haze = nt.nodes.new("ShaderNodeMapRange")
    haze.inputs["From Min"].default_value = 300.0
    haze.inputs["From Max"].default_value = 4000.0
    nt.links.new(cam.outputs["View Distance"], haze.inputs["Value"])
    hz = nt.nodes.new("ShaderNodeMix")
    hz.data_type = "RGBA"
    nt.links.new(haze.outputs["Result"], hz.inputs["Factor"])
    nt.links.new(avg.outputs[2], hz.inputs[6])
    hz.inputs[7].default_value = haze_color
    emis = nt.nodes.new("ShaderNodeMath")              # 雾是自发光的「空气」：远处不靠太阳照亮
    emis.operation = "MULTIPLY"
    emis.inputs[1].default_value = 1.0
    nt.links.new(haze.outputs["Result"], emis.inputs[0])
    nt.links.new(avg.outputs[2], bsdf.inputs["Base Color"])
    nt.links.new(hz.outputs[2], bsdf.inputs["Emission Color"])
    nt.links.new(emis.outputs[0], bsdf.inputs["Emission Strength"])
    nt.links.new(rough.outputs["Color"], bsdf.inputs["Roughness"])
    nm = nt.nodes.new("ShaderNodeNormalMap")
    nm.inputs["Strength"].default_value = 0.6
    nt.links.new(nor.outputs["Color"], nm.inputs["Color"])
    nt.links.new(nm.outputs["Normal"], bsdf.inputs["Normal"])
    bsdf.inputs["Specular IOR Level"].default_value = 0.2
    return m


def make_ground(name: str, cx: float, size: float, mat: bpy.types.Material) -> bpy.types.Object:
    me = bpy.data.meshes.new(name)
    s = size / 2
    me.from_pydata([(-s, -s, 0), (s, -s, 0), (s, s, 0), (-s, s, 0)], [], [(0, 1, 2, 3)])
    me.materials.append(mat)
    ob = bpy.data.objects.new(name, me)
    ob.location = (cx, s * 0.8, 0)          # 大部分铺在相机前方
    _link(ob)
    return ob


# ---------- 主流程 ----------

def build(ep: Path) -> dict:
    data = json.loads((ep / "data.json").read_text(encoding="utf-8"))
    cuts = json.loads((ep / "assets" / "cutouts" / "cutouts.json").read_text(encoding="utf-8"))
    man_info = cuts["human"]
    scene = bpy.context.scene
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    scene.render.fps = FPS
    scene.render.resolution_x, scene.render.resolution_y = 1920, 1080
    engine = _engine_eevee()
    scene.view_settings.view_transform = "Standard"     # 抠像是照片：显示即原色，不经 AgX 压缩
    scene.view_settings.look = "None"
    scene.view_settings.exposure = 0.0
    try:
        scene.eevee.use_shadows = True
        scene.eevee.shadow_ray_count = 2
    except AttributeError:
        pass

    w_day, _ = make_world("world_day", HDRI_DAY, None, 1.0, u_view=U_VIEW_DAY)
    w_day["theta_lineup"] = theta_for_u(U_VIEW_DAY)
    w_day["theta_group"] = theta_for_u(U_VIEW_GROUP)      # render_ep.py 合影段切换
    w_day["parallax_d"] = PARALLAX_D                       # render_ep.py 列队段按相机 x 逐帧转 HDRI
    sun_day = SUN_DAY_DIR
    w_hook, sun_hook = make_world("world_hook", HDRI_HOOK, SUN_HOOK_DIR, 1.0)
    scene.world = w_day
    make_sun("sun_day", sun_day, 3.5)
    sh = make_sun("sun_hook", sun_hook, 2.0)
    sh.hide_render = True

    order = list(reversed(data["items"]))
    man_mpp = 1.75 / (man_info["bottom"] - man_info["head_top"])
    subjects = []
    x, prev_len = 0.0, 0.0
    for it in order:
        key = it["model"]["key"]
        info = cuts[key]
        mpp = it["dims"]["height_m"] / (info["bottom"] - info["shoulder_top"])
        obj = _cut_plane(f"subj_{key}", key, info, mpp)
        length = info["size"][0] * mpp
        x += (max(prev_len, length) * 0.6 + 1.6) if subjects else 0.0
        obj.location = (x + length / 2, 0.0, 0.0)
        man = _cut_plane(f"human_{key}", "human", man_info, man_mpp)
        man_w = man_info["size"][0] * man_mpp
        man.location = (x - 0.85, 0.0, 0.0)      # 人中线在动物尾端后 0.85 m（同 build_ep）
        obj["marker_x"] = x + info["shoulder_col"] * mpp
        _blob(f"blob_{key}", x + length / 2, length, depth=4.0)          # 平视下地面纵深被压扁：阴影要够深才看得见
        _blob(f"blob_human_{key}", man.location.x, man_w * 1.2, 2.0)
        x += length
        prev_len = length
        subjects.append((it, obj, man))
    bpy.context.view_layer.update()
    gmat = ground_material()
    make_ground("ground", x / 2, 12000.0, gmat)
    env_cfg = ep / "assets" / "cutouts" / "env.json"
    if env_cfg.exists():
        exec(compile(SCENE_ENV.read_text(encoding="utf-8"), str(SCENE_ENV), "exec"), globals())
        cfg = json.loads(env_cfg.read_text(encoding="utf-8"))
        cut_dir = ep / "assets" / "cutouts"
        build_env(0.0, x, ep, {"plate": REPO / cfg["plate"], "plate_horizon": cfg["plate_horizon"],
                                "trees": [cut_dir / f for f in cfg["trees"]], "bushes": [cut_dir / f for f in cfg["bushes"]]})

    # 比例机检：由平面的世界坐标与像素标定反算肩高、蹄底高度、人高
    rows = []
    for it, obj, man in subjects:
        info = cuts[it["model"]["key"]]
        lo, hi = world_bbox(obj)
        mpp_w = (hi.z - lo.z) / info["size"][1]
        shoulder_z = lo.z + (info["size"][1] - 1 - info["shoulder_top"]) * mpp_w
        foot_z = lo.z + (info["size"][1] - 1 - info["bottom"]) * mpp_w
        mlo, mhi = world_bbox(man)
        mmpp = (mhi.z - mlo.z) / man_info["size"][1]
        man_h = (man_info["bottom"] - man_info["head_top"]) * mmpp
        err = abs(shoulder_z - foot_z - it["dims"]["height_m"]) / it["dims"]["height_m"]
        rows.append({"key": it["model"]["key"], "expected_height_m": it["dims"]["height_m"],
                     "measured_height_m": round(shoulder_z - foot_z, 4), "error": round(err, 5),
                     "grounded": abs(foot_z) < 0.01, "human_height_m": round(man_h, 4),
                     "human_ok": abs(man_h - 1.75) / 1.75 <= 0.01,
                     "pass": err <= TOLERANCE and abs(foot_z) < 0.01 and abs(man_h - 1.75) / 1.75 <= 0.01})
    check = {"tolerance": TOLERANCE, "method": "cutout pixels (shoulder row, sole row) × metres per pixel",
             "all_pass": all(r["pass"] for r in rows), "items": rows}
    (ep / "scale_check.json").write_text(json.dumps(check, ensure_ascii=False, indent=2), encoding="utf-8")

    # 相机：列队（与 build_ep.build_episode 相同的节奏与构图）
    cam = bpy.data.objects.new("Camera", bpy.data.cameras.new("Camera"))
    scene.collection.objects.link(cam)
    scene.camera = cam
    cam.data.lens = LENS_MM
    cam.data.clip_end = 8000
    cam.data.dof.use_dof = True
    cam.data.dof.aperture_fstop = FSTOP
    f = 1
    timeline = {"fps": FPS, "segments": {}, "items": [], "insights": [], "mode": "cutout"}
    ins_after = {i["after_rank"]: n for n, i in enumerate(data["insights"])}
    n = len(subjects)
    for i, (it, obj, man) in enumerate(subjects):
        lo, hi = world_bbox(obj)
        mlo, mhi = world_bbox(man)
        eye, rot = _shot(cam, min(lo.x, mlo.x), max(hi.x, mhi.x), max(hi.z - lo.z, (mhi.z - mlo.z) * 1.22), 0.0)
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
        cam.data.dof.focus_distance = -eye.y          # 平视看 +y：到主体平面（y=0）的距离
        cam.data.dof.keyframe_insert("focus_distance", frame=f)
        cam.data.dof.keyframe_insert("focus_distance", frame=c)
        scene.frame_set(a)
        man_head = _project(cam, Vector(((mlo.x + mhi.x) / 2, 0.0, mhi.z + 0.12)))
        mx = obj["marker_x"]
        timeline["items"].append({
            "data_index": data["items"].index(it), "key": it["model"]["key"], "rank": it["rank"], "name": it["name"],
            "label": [a, b], "static": [f, c], "man_label_xy": man_head,
            "marker": {"base": _project(cam, Vector((mx, 0.0, 0.0))), "top": _project(cam, Vector((mx, 0.0, it["dims"]["height_m"])))},
        })
        f = c + int(MOVE_S * FPS) if i < n - 1 else c
    lineup_end = f
    timeline["segments"]["lineup"] = [1, lineup_end]

    # 钩子：冠军与亚军的剪影，日落逆光
    top = subjects[-2:]
    x0 = min(min(world_bbox(o)[0].x, world_bbox(m)[0].x) for _, o, m in top)
    x1 = max(world_bbox(o)[1].x for _, o, _ in top)
    h = max(world_bbox(o)[1].z for _, o, _ in top)
    hook_cam = bpy.data.objects.new("cam_hook", bpy.data.cameras.new("cam_hook"))
    scene.collection.objects.link(hook_cam)
    hook_cam.data.lens = LENS_MM
    hook_cam.data.clip_end = 8000
    hook_cam.data.shift_y = 0.3 * 1080 / 1920
    vis_h = h / 0.52
    dist = max(vis_h / 2 / math.tan(hook_cam.data.angle_y / 2), (x1 - x0 + 2) / 2 / math.tan(hook_cam.data.angle_x / 2))
    e0 = Vector(((x0 + x1) / 2, -dist, 0.02))
    r0 = Vector((math.pi / 2, 0.0, 0.0))
    hook_start = lineup_end + 1
    _key(hook_cam, e0, r0, hook_start)
    _key(hook_cam, e0 + Vector((0.0, dist * 0.05, 0.0)), r0, hook_start + int(HOOK_S * FPS) - 1)
    timeline["segments"]["hook"] = [hook_start, hook_start + int(HOOK_S * FPS) - 1]

    # 合影：五排（前小后大），长焦远机位，带天空
    grp = bpy.data.collections.new("Group")
    scene.collection.children.link(grp)
    rows_ = [subjects[i:i + 6] for i in range(0, len(subjects), 6)]
    row_gap = 2.6
    placed, widest = [], 0.0
    GX = 20000.0
    for t, row in enumerate(rows_):
        lens = [world_bbox(o)[1].x - world_bbox(o)[0].x for _, o, _ in row]
        step = sum(lens) / len(lens) * 0.62      # 前后交错重叠，合影更紧凑、个头更大
        span = step * (len(row) - 1) + lens[-1]
        widest = max(widest, span)
        for j, (it, o, _) in enumerate(row):
            dup = o.copy()
            dup.name = f"grp_{it['model']['key']}"
            grp.objects.link(dup)
            dup.location = (GX - span / 2 + step * j + lens[j] / 2, t * row_gap + (j % 2) * 0.6, 0.0)
            b = _blob(f"grp_blob_{it['model']['key']}", dup.location.x, lens[j])
            for c_ in list(b.users_collection):
                c_.objects.unlink(b)
            grp.objects.link(b)
            b.location.y = dup.location.y
            placed.append(dup)
    bpy.context.view_layer.update()
    front_lo = min(world_bbox(o)[0].x for o in placed[:len(rows_[0])])
    gman = subjects[0][2].copy()
    gman.name = "grp_human"
    grp.objects.link(gman)
    # 人放在全体最左侧之外（第 6 轮审片：夹在牦牛和斑马之间只露上半身，观众找不到）
    all_lo = min(world_bbox(o)[0].x for o in placed)
    gman.location = (min(front_lo - 0.9, all_lo - 1.2), -0.3, 0.0)
    gg = make_ground("grp_ground", GX, 6000.0, gmat)   # 第 3 版：与列队同一种金色草地（原单独的浅灰材质发白）
    for c_ in list(gg.users_collection):
        c_.objects.unlink(gg)
    grp.objects.link(gg)
    gcam = bpy.data.objects.new("cam_group", bpy.data.cameras.new("cam_group"))
    scene.collection.objects.link(gcam)
    gcam.data.clip_end = 20000
    hmax = max(world_bbox(o)[1].z for o in placed)
    depth_c = row_gap * (len(rows_) - 1) / 2
    # 取景框住「人 + 全体」并以其中点居中，两侧各留约 3 m（第 8 轮审片：镜头缓推时人和标签贴到左缘 10–15 px）
    bpy.context.view_layer.update()
    span_lo = world_bbox(gman)[0].x
    span_hi = max(world_bbox(o)[1].x for o in placed)
    vis_w = (span_hi - span_lo + 4.0) / 0.92
    gcam.data.lens = 36 * GROUP_DIST / vis_w
    vis_h = vis_w * 9 / 16
    half_v = math.atan(vis_h / 2 / GROUP_DIST)
    p = math.atan((0.5 - HORIZON_FROM_TOP) * 2 * math.tan(half_v))   # 俯角：地平线落在上方 30%
    fwd = Vector((0, math.cos(p), -math.sin(p)))
    # 前排脚底放在离底 17% 处：沿屏幕竖向从画面中心下移 0.33 × 可视高（第 3 版：少露前景地面）
    up = Vector((0, math.sin(p), math.cos(p)))
    front = Vector(((span_lo + span_hi) / 2, 0.0, 0.0))
    tgt = front + up * (vis_h * 0.33)
    gcam.location = tgt - fwd * GROUP_DIST
    gcam.rotation_euler = (math.pi / 2 - p, 0, 0)
    g0 = hook_start + int(HOOK_S * FPS)
    g1 = g0 + int(GROUP_S * FPS) - 1
    lens0 = gcam.data.lens
    gcam.data.lens = lens0 / 1.05
    gcam.data.keyframe_insert("lens", frame=g0)
    gcam.data.lens = lens0
    gcam.data.keyframe_insert("lens", frame=g1)
    timeline["segments"]["group"] = [g0, g1]
    if env_cfg.exists():          # 第 3 版：合影也放同一套精细环境（按合影相机视野摆）
        scene.frame_set(g1)
        build_group_env(GX, gcam, row_gap * (len(rows_) - 1) + 0.6, grp,
                        {"plate": REPO / cfg["plate"], "plate_horizon": cfg["plate_horizon"],
                         "trees": [cut_dir / f for f in cfg["trees"]], "bushes": [cut_dir / f for f in cfg["bushes"]]})
    gl = []
    for fr in (g0, g1):
        scene.frame_set(fr)
        gm_lo, gm_hi = world_bbox(gman)
        gl.append(_project(gcam, Vector(((gm_lo.x + gm_hi.x) / 2, gman.location.y, gm_hi.z + 0.12))))
    timeline["group_man_label_xy"] = gl
    timeline["group_perspective_error"] = round(row_gap * (len(rows_) - 1) / GROUP_DIST, 4)
    timeline["sources_s"] = SOURCES_S
    timeline["engine"] = engine
    scene.frame_start, scene.frame_end = 1, g1

    (ep / "_build").mkdir(exist_ok=True)
    (ep / "_build" / "timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=1), encoding="utf-8")
    (ep / "scene").mkdir(exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(ep / "scene" / "ep.blend"))
    return {"scale_check_all_pass": check["all_pass"], "lineup_frames": lineup_end, "length_m": round(x, 1)}


if __name__ == "__main__" or "--" in sys.argv:
    EP = Path(sys.argv[sys.argv.index("--") + 1]).resolve()
    print("[build_cutout]", build(EP))
