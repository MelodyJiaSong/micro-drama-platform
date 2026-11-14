"""真实尺度 · 分段渲染（bible §8：量产期无界面批量渲染）。

    blender -b <集目录>/scene/ep.blend --python ai_videos/zhenshi_chidu/_tools/render_ep.py -- <集目录> <段> [--draft]
段：lineup | hook | group。读 _build/timeline.json；输出 _build/frames/<段>/NNNNN.jpg（段内从 0 编号）。
列队段镜头静止的区间只渲染第一帧、其余复制（画面不动，结果逐像素相同）。已存在的帧跳过（可续跑）。
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import bpy

argv = sys.argv[sys.argv.index("--") + 1:]
EP = Path(argv[0]).resolve()
SEG = argv[1]
DRAFT = "--draft" in argv
ONLY = None   # --only 0,120,240：只渲染段内这些帧（试看），输出到 frames/<段>_test/
if "--only" in argv:
    ONLY = [int(v) for v in argv[argv.index("--only") + 1].split(",")]
# --still <段内帧> <宽>x<高> <中心x> <视野宽> <视野顶> <输出.png>：封面静帧（covers.py 调用）。
# 视野用原 1920×1080 画面的像素坐标给出（可超出原画面，如竖版向上多露天空）；同一相机位置，只改焦距与平移，比例不变。
STILL = None
if "--still" in argv:
    i_ = argv.index("--still")
    ow_, oh_ = (int(v) for v in argv[i_ + 2].split("x"))
    STILL = {"f": int(argv[i_ + 1]), "size": (ow_, oh_), "cx": float(argv[i_ + 3]), "w": float(argv[i_ + 4]),
             "top": float(argv[i_ + 5]), "out": str(Path(argv[i_ + 6]).resolve())}   # 绝对路径：Blender 把相对路径解析到盘符根
    ONLY = [STILL["f"]]
tl = json.loads((EP / "_build" / "timeline.json").read_text(encoding="utf-8"))
scene = bpy.context.scene
vl = scene.view_layers[0]


def layer(name: str):
    def walk(lc):
        if lc.collection.name == name:
            return lc
        for ch in lc.children:
            r = walk(ch)
            if r:
                return r
    return walk(vl.layer_collection)


for cand in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
    try:
        scene.render.engine = cand
        break
    except TypeError:
        pass
try:
    scene.eevee.taa_render_samples = 16 if DRAFT else 32     # 第 3 版 3D 草地：48 时 21 s/帧
except AttributeError:
    pass
scene.render.resolution_x, scene.render.resolution_y = 1920, 1080
scene.render.resolution_percentage = 50 if DRAFT else 100
scene.render.image_settings.file_format = "JPEG"
scene.render.image_settings.quality = 93

lineup_lc, group_lc = layer("TrueScale"), layer("Group")
lineup_lc.exclude = SEG == "group"
group_lc.exclude = SEG != "group"
scene.camera = bpy.data.objects[{"lineup": "Camera", "hook": "cam_hook", "group": "cam_group"}[SEG]]

CUTOUT = tl.get("mode") == "cutout"
if CUTOUT:
    # 2.5D（build_cutout.py）：白天 / 日落两套 HDRI 世界与太阳；钩子把抠像的发光强度置 0 = 黑剪影
    hook = SEG == "hook"
    scene.world = bpy.data.worlds["world_hook" if hook else "world_day"]
    if not hook:     # 合影镜头视角窄：转到空旷的地平线
        wd = scene.world
        mp = next(n for n in wd.node_tree.nodes if n.type == "MAPPING")
        mp.inputs["Rotation"].default_value[2] = wd["theta_group" if SEG == "group" else "theta_lineup"]
    gnd = bpy.data.materials.get("ground_veld")   # 钩子逆光：近处地面压暗
    if gnd:
        b_ = next(n for n in gnd.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
        b_.inputs["Base Color"].default_value = (0.03, 0.025, 0.02, 1)
        if hook:
            for l in list(b_.inputs["Base Color"].links):
                gnd.node_tree.links.remove(l)
    bpy.data.objects["sun_day"].hide_render = hook
    bpy.data.objects["sun_hook"].hide_render = not hook
    for m in bpy.data.materials:
        if m.name.startswith("cut_") and m.node_tree and "cut_strength" in m.node_tree.nodes:
            m.node_tree.nodes["cut_strength"].outputs[0].default_value = 0.0 if hook else 1.0
    for o in bpy.data.objects:
        if o.name.startswith(("blob_", "grp_blob_", "scatter_", "env_")):   # 钩子：机位贴地 2 cm，草会挡住一切；日落天空不要远景板
            o.hide_render = hook
elif SEG == "hook":
    mat = bpy.data.materials.new("silhouette")
    mat.use_nodes = True
    b = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = (0.0, 0.0, 0.0, 1)
    b.inputs["Roughness"].default_value = 1.0
    b.inputs["Specular IOR Level"].default_value = 0.0
    vl.material_override = mat
    nt = scene.world.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputWorld")
    bg = nt.nodes.new("ShaderNodeBackground")
    coord = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    nt.links.new(coord.outputs["Generated"], sep.inputs[0])   # 世界的 Generated = 视线方向；Z 即仰角正弦
    nt.links.new(sep.outputs["Z"], ramp.inputs["Fac"])
    ramp.color_ramp.elements[0].position = 0.0      # 地平线：橙
    ramp.color_ramp.elements[0].color = (1.0, 0.42, 0.10, 1)
    ramp.color_ramp.elements[1].position = 0.13     # 画面顶部（135 mm 竖向视角约 10°，顶边仰角约 8°，sin≈0.14）：深蓝紫
    ramp.color_ramp.elements[1].color = (0.10, 0.10, 0.30, 1)
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = 1.0
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])

a, b = tl["segments"][SEG]
out_dir = EP / "_build" / "frames" / (SEG + ("_test" if ONLY else ""))
out_dir.mkdir(parents=True, exist_ok=True)
static = {}
static_starts = {it["static"][0] for it in tl["items"]}
if SEG == "lineup":
    for it in tl["items"]:
        s0, s1 = it["static"]
        for f in range(s0 + 1, s1 + 1):
            static[f] = s0
PARALLAX = None
if CUTOUT and SEG == "lineup":
    # 远景视差（第 4 轮审片：横移时背景纹丝不动）：HDRI 随相机 x 转动，相当于远景在约 parallax_d 米外
    wd = bpy.data.worlds["world_day"]
    PARALLAX = (next(n for n in wd.node_tree.nodes if n.type == "MAPPING"), wd["theta_lineup"], wd["parallax_d"])
    scene.frame_set(a)
    CAM_X0 = scene.camera.matrix_world.translation.x
for f in range(a, b + 1):
    if ONLY is not None and (f - a) not in ONLY:
        continue
    dst = out_dir / f"{f - a:05d}.jpg"
    if STILL:
        scene.frame_set(f)
        if PARALLAX:
            mp_, th0, dd = PARALLAX
            mp_.inputs["Rotation"].default_value[2] = th0 - (scene.camera.matrix_world.translation.x - CAM_X0) / dd
        scene.eevee.taa_render_samples = 64
        cam = scene.camera.data
        cam.animation_data_clear()        # 合影相机焦距有关键帧：清掉，否则渲染时按动画值覆盖下面的改动（当前帧的值已求出）
        ow, oh = STILL["size"]
        wpx = STILL["w"]
        hpx = wpx * oh / ow
        big = wpx      # HORIZONTAL 适配时平移以画面宽为单位（实测：按长边算时竖版窗口偏 25%）
        sx0, sy0 = cam.shift_x * 1920, cam.shift_y * 1920       # 原画面横版、AUTO 适配：平移以宽为单位
        cam.sensor_fit = "HORIZONTAL"
        cam.lens = cam.lens * 1920 / wpx
        cam.shift_x = (sx0 + STILL["cx"] - 960) / big
        cam.shift_y = (sy0 - (STILL["top"] + hpx / 2 - 540)) / big
        scene.render.resolution_x, scene.render.resolution_y, scene.render.resolution_percentage = ow, oh, 100
        scene.render.image_settings.file_format = "PNG"
        scene.render.filepath = STILL["out"]
        bpy.ops.render.render(write_still=True)
        print("[render] still", STILL["out"], flush=True)
        break
    if dst.exists():
        continue
    if f in static:
        src = out_dir / f"{static[f] - a:05d}.jpg"
        if src.exists():
            shutil.copyfile(src, dst)
            continue
    scene.frame_set(f)
    if CUTOUT and SEG == "lineup" and not DRAFT:   # 横移帧在运动中：16 采样足够；静止帧（只渲一次、要停 4.5 s）用 32
        scene.eevee.taa_render_samples = 32 if f in static_starts else 16
    if PARALLAX:
        mp_, th0, dd = PARALLAX
        mp_.inputs["Rotation"].default_value[2] = th0 - (scene.camera.matrix_world.translation.x - CAM_X0) / dd
    scene.render.filepath = str(dst)
    bpy.ops.render.render(write_still=True)
    print(f"[render] {SEG} {f - a}/{b - a}", flush=True)
print("[render] done", SEG)
