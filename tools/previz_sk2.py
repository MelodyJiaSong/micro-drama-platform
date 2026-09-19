# -*- coding: utf-8 -*-
"""sk2 逐镜 previz —— 从整城 blend 里摆机位、出白模动画 mp4。

用法（仓库根目录）：
    blender -b --factory-startup --python tools/previz_sk2.py
    blender -b --factory-startup --python tools/previz_sk2.py -- --only S21,S30
    blender -b --factory-startup --python tools/previz_sk2.py -- --fps 10 --res 1280

产物：`5_6_分镜与prompt/shots/shotNN/shotNN_previz.mp4`

设计
----
· **机位从镜表的数据算出来，不手摆**（rule 4h ②：`previz_config` 是 3D 层唯一真相）。
  本片的「唯一真相」就是 `tools/gen_shots_sk2.py` 的 `SHOTS` 表——previz 直接 import 它，
  所以**改镜表 → 重跑 previz，两边永远同步**，不存在手摆机位与镜表对不上的漂移。
· **距离由 `subj_frac`（人占画高）反解**：一个 1.75 m 的人要在画面里占 f 的高度，
  相机到他的距离 d = (1.75 / f) / (2·tan(vfov/2))。起幅与落幅各解一次，中间线性推拉——
  这样 previz 的取景与 shot md 的 `景别档:` 是**同一套数**，可以逐镜对账。
· **机位标签决定高度与俯仰**（低机位 / 平机位 / 高机位俯拍 / 仰拍 / 航拍…），
  相邻镜机位标签不同是景别档铁律的一半，previz 因此能一眼看出接缝成不成立。
· 只渲**布局层灰模**（workbench，`color_type=OBJECT`，不吃材质），符合 rule 4h。

注意
----
· 城市 blend 由 `tools/build_stormwind.py` 确定性生成；**先跑它，再跑本文件**。
· 室内镜（王座厅 / 旅店 / 酒馆 / 地铁）在整城 blend 里只有体块，previz 只对机位与运镜负责，
  内景几何另建（rule 4g §J：场景层只出 blend + 校验 PNG，只有 shot previz 出 mp4）。
"""
from __future__ import annotations

import importlib.util
import math
import os
import sys

import shutil
import subprocess
import tempfile

import bpy

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DRAMA = os.path.join(REPO, "ai_videos", "shikong_lvxing", "sk2")
A = os.path.join(DRAMA, "2_世界观人设")
BLEND = os.path.join(A, "scenes", "stormwind", "_blender", "stormwind.blend")
SHOTS_DIR = os.path.join(DRAMA, "5_6_分镜与prompt", "shots")

HUMAN_H = 1.75          # 用来把 subj_frac 反解成距离
VFOV = math.radians(28)  # 约等于 50mm 全画幅的竖向视角
CITY_SCALE = 0.5
SAFE_BACK = 12.0        # 相机在街心离锚点的后退量（单位＝缩放后的米），保证不进街墙
FFMPEG = shutil.which("ffmpeg") or "C:/Users/light/AppData/Local/Microsoft/WinGet/Packages/yt-dlp.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-N-125365-g9a01c1cb6a-win64-gpl/bin/ffmpeg.exe"


def load_shots():
    spec = importlib.util.spec_from_file_location("g", os.path.join(REPO, "tools", "gen_shots_sk2.py"))
    g = importlib.util.module_from_spec(spec)
    sys.argv = [sys.argv[0]]        # 屏蔽 blender 的参数，别让生成器的 argparse 吃到
    spec.loader.exec_module(g)
    return g.SHOTS, g.BG_NAME


# 场景锚点（与 build_stormwind.py 同一套，米，原点＝城门；此处已含 0.5 比例）
ANCHORS = {k: tuple(c * CITY_SCALE for c in v) for k, v in {
    "bg0": (-129.5, 318.0, 0.0),      # 全城中心（航拍用）
    "bg1": (0.0, 0.0, 0.0),           # 英雄谷
    "bg2": (-112.8, 141.1, -0.3),     # 贸易区
    "bg3": (41.4, 292.6, 4.3),        # 旧城区
    "bg4": (-164.1, 600.0, 1.6),      # 矮人区
    "bg5": (-112.0, 578.0, 1.6),      # 地铁站台（矮人区东侧）
    "bg6": (-112.0, 520.0, -6.0),     # 水下段（隧道内，地下）
    "bg7": (-342.6, 442.8, 12.3),     # 教堂广场
    "bg8": (-559.5, 273.1, -3.0),     # 花园区月亮井
    "bg9": (-465.2, 102.1, 22.2),     # 法师区
    "bg10": (-57.5, 636.5, 26.7),     # 王座厅（要塞北端）
    "bg11": (-318.5, 199.4, 4.2),     # 运河（监狱一带）
    "bg12": (-112.8, 141.1, -0.3),    # 旅店（贸易区内）
}.items()}


# 逛单路线顺序（＝ outline 的一日动线）。相机按「进入该地点的行进方向」站位，
# 也就是**站在街上顺着街轴看**。城变密之后这条是必须的：早先用固定世界方位角退到
# 景别要求的距离，会把相机退进第二三排房子里，渲出来整片灰（2026-09-19 实测 shot04）。
ROUTE = ["bg1", "bg2", "bg12", "bg11", "bg3", "bg10", "bg4", "bg5", "bg6",
         "bg7", "bg8", "bg9"]


# ── 路径机位（shot_id → 关键帧） ──────────────────────────────────
# `cam_rig()` 给的是**与地理无关的通用轨道**：所有「航拍」镜一律「高 26 m、俯角 12°、
# 从 220 m 外推到 120 m」。S01 要的却是一条具体航线——沿引道北飞、穿过城门洞、出洞进英雄谷，
# 通用轨道只会在屋顶上空斜着平移，全程一个状态，门也没有、穿越也没有（2026-09-19 用户指出）。
# 有路径的镜走路径，**没有路径的镜维持原行为一个字不动**。
# 关键帧 = (t 秒, (相机 x,y,z), (视线目标 x,y,z))，写 **build 坐标**（米，未缩放），
# 函数内部统一乘 CITY_SCALE。t 与 `gen_shots_sk2.py` 里该镜的 `动作:` 时间轴逐拍对齐（rule 4h ②）。
#
# 门洞净空：x ±6 / y ±8 / z 0–9（见 build_stormwind.py 的 GATE_* 常量）。
# 穿门那几帧相机固定在 x=0、z≈5，前后各留一帧确保整段都在净空里。
PATHS = {
    # S01（25 s）：0–9s 掠过林间大道 / 9–16s 穿过城门洞 / 16–25s 出洞，巨像从两侧掠过
    "S01": [
        (0.0,  (0.0, -175.0, 20.0), (0.0,   25.0, 13.0)),   # 引道南端上空，树冠高度，朝北看城门
        (9.0,  (0.0,  -38.0,  5.2), (0.0,   40.0,  5.0)),   # 逼近城门，已降到门洞净高以内
        (12.5, (0.0,   -2.0,  4.8), (0.0,   60.0,  4.8)),   # **在门洞之内**（|y|<8）
        (16.0, (0.0,   14.0,  5.4), (-20.0, 40.0,  6.0)),   # 刚穿出，开始转上入城主路
        (25.0, (-55.0,  69.0, 14.0), (-112.0, 140.0, 6.0)),  # 英雄谷内继续北行，高度回升
    ],
    # S02（28 s）：0–18s 拔高后退城区依次入画 / 18–28s 回落到石桥头高度
    # t=0 必须与 S01 末帧**逐字相同**（`衔接: 承接 shot01 末帧`）
    "S02": [
        (0.0,  (-55.0,   69.0,  14.0), (-112.0, 140.0,   6.0)),
        (6.0,  (40.0,   -60.0,  90.0), (-120.0, 260.0,  20.0)),
        (12.0, (180.0,  120.0, 200.0), (-160.0, 330.0,  20.0)),
        (18.0, (60.0,   520.0, 230.0), (-200.0, 330.0,  20.0)),
        (23.0, (-80.0,  240.0, 120.0), (-60.0,   60.0,  10.0)),
        (28.0, (-31.0,   39.0,   7.0), (2.0,    -22.0,   6.0)),  # 石桥头高度，回望城门
    ],
}


def street_heading(bg):
    """进入该地点的行进方向（弧度）。相机站在这个方向的反向，朝目标看。"""
    if bg not in ROUTE:
        return math.radians(200.0)
    i = ROUTE.index(bg)
    if i == 0:
        # 路线起点没有「来路」：行进方向＝朝下一站（朝城里），
        # 取反会让相机朝城外看，画面里一栋楼都没有（2026-09-19 实测 shot04）
        a, b = ANCHORS.get(bg), ANCHORS.get(ROUTE[1])
    else:
        a, b = ANCHORS.get(ROUTE[i - 1]), ANCHORS.get(bg)
    if not a or not b or (abs(a[0] - b[0]) < 1e-6 and abs(a[1] - b[1]) < 1e-6):
        return math.radians(200.0)
    return math.atan2(b[1] - a[1], b[0] - a[0])


def cam_rig(tag):
    """机位标签 → (相机高度 m, 俯仰角 deg, 方位偏移 deg)。正俯仰＝俯拍。"""
    t = tag
    if "航拍" in t:
        return (26.0, 12.0, 0.0) if "低空" in t else (48.0, 26.0, 20.0)
    if "仰拍" in t:
        return (1.2, 0.0, 0.0)   # 仰角由 TrackTo 的目标高度给，不靠压低相机
    if "高机位" in t or "俯瞰" in t or "俯拍" in t:
        return (9.0, 34.0, 25.0)
    if "低机位" in t or "贴轨" in t or "水面" in t:
        return (1.0, 0.0, 0.0)   # 「低」是相对人眼低，不是贴地；再低地面就整个落出画框
    if "侧机位" in t or "侧向" in t:
        return (1.6, 0.0, 70.0)
    if "手持" in t:
        return (1.55, 2.0, 15.0)
    if "环绕" in t:
        return (1.6, 4.0, 0.0)
    return (1.6, 0.0, 0.0)             # 平机位正对


def dist_for(frac):
    """人占画高 frac → 相机到主体的距离（米）。"""
    frac = max(0.02, min(0.95, frac))
    return (HUMAN_H / frac) / (2.0 * math.tan(VFOV / 2.0))


# Seedance 对上传的参考视频有像素数下限：**宽 × 高 ≥ 409600**（＝640×640）。
# 原先的 720×404 只有 290880，整批 previz 传上去全被拒（用户 2026-09-19 实测报错）。
# 1280×720 ＝ 921600，既过线又是精确 16:9，留足余量。
MIN_PIXELS = 409_600


def setup_scene(fps, res):
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_WORKBENCH"
    # 宽高都必须是偶数：libx264 的 yuv420p 不吃奇数边（720→405 会整批编码失败）
    rx = res - (res % 2)
    ry = int(res * 9 / 16)
    ry -= ry % 2
    if rx * ry < MIN_PIXELS:
        raise SystemExit(
            f"[previz] 分辨率闸门未过：{rx}x{ry} = {rx * ry} < {MIN_PIXELS}。"
            f"Seedance 拒收低于 409600 像素的参考视频；--res 至少给 1280。")
    sc.render.resolution_x, sc.render.resolution_y = rx, ry
    sc.render.fps = fps
    # Blender 5.1 这个构建不带 ffmpeg 输出，改出 PNG 序列后用系统 ffmpeg 编码
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    try:
        sh = sc.display.shading
        sh.light = "STUDIO"
        sh.color_type = "OBJECT"       # 不吃材质，纯灰模（rule 4h）
        sh.show_shadows = True
        sh.show_cavity = True
    except Exception:
        pass
    return sc



def clear_of_geometry(sc, cam_loc, tgt_loc):
    """相机到目标之间有没有实体挡着。返回 True ＝ 通视。"""
    import mathutils
    d = mathutils.Vector(tgt_loc) - mathutils.Vector(cam_loc)
    dist = d.length
    if dist < 1e-6:
        return False
    dg = bpy.context.evaluated_depsgraph_get()
    hit, _loc, _n, _i, _o, _m = sc.ray_cast(
        dg, mathutils.Vector(cam_loc), d.normalized(), distance=dist - 0.5)
    return not hit


def find_clear_cam(sc, base_loc, tgt_loc, heading):
    """在街心附近找一个能看见目标的机位。

    密城里按公式算出来的位置常常正对着一栋楼（2026-09-19 实测：贸易区那一镜
    正中杵着一整面墙）。这里按「先抬高、再左右挪、最后后退」的顺序试，
    第一个通视的就用——**几何自己回答，不靠猜**。
    """
    x, y, z = base_loc
    if clear_of_geometry(sc, (x, y, z), tgt_loc):
        return (x, y, z)
    nx, ny = -math.sin(heading), math.cos(heading)      # 街的法向
    for dz in (0.0, 2.0, 5.0, 9.0, 14.0, 20.0):
        for side in (0.0, 3.0, -3.0, 6.0, -6.0, 9.0, -9.0):
            for back in (0.0, 4.0, 8.0, -4.0):
                cx = x + nx * side - math.cos(heading) * back
                cy = y + ny * side - math.sin(heading) * back
                cz = z + dz
                if clear_of_geometry(sc, (cx, cy, cz), tgt_loc):
                    return (cx, cy, cz)
    return (x, y, z + 26.0)      # 全挡住就升到屋顶之上


def new_camera(name, sc):
    cam_d = bpy.data.cameras.new(name)
    cam_d.sensor_fit = "VERTICAL"
    cam_d.sensor_height = 24.0
    cam_d.lens_unit = "MILLIMETERS"
    cam_d.lens = (24.0 / 2.0) / math.tan(VFOV / 2.0)
    cam_d.clip_start = 0.05
    cam_d.clip_end = 6000.0
    cam = bpy.data.objects.new(name, cam_d)
    sc.collection.objects.link(cam)
    return cam, cam_d


def make_path_camera(sh, sc, path):
    """按 PATHS 的关键帧飞：相机与视线目标各自打关键帧，TrackTo 负责朝向。"""
    cam, _cam_d = new_camera(f"cam_{sh['id']}", sc)
    tgt = bpy.data.objects.new(f"tgt_{sh['id']}", None)
    sc.collection.objects.link(tgt)
    con = cam.constraints.new("TRACK_TO")
    con.target = tgt
    con.track_axis, con.up_axis = "TRACK_NEGATIVE_Z", "UP_Y"
    d = max(1e-6, float(sh["d"]))
    span = sc.frame_end - sc.frame_start
    for t, c, l in path:
        f = sc.frame_start + int(round(min(1.0, max(0.0, t / d)) * span))
        cam.location = tuple(v * CITY_SCALE for v in c)
        cam.keyframe_insert("location", frame=f)
        tgt.location = tuple(v * CITY_SCALE for v in l)
        tgt.keyframe_insert("location", frame=f)
    sc.camera = cam
    return cam


def make_camera(sh, sc):
    path = PATHS.get(sh["id"])
    if path:
        return make_path_camera(sh, sc, path)
    bg = sh["bg"]
    target = ANCHORS.get(bg, (0.0, 0.0, 0.0))
    h, pitch, yaw_off = cam_rig(sh["jbcam"])
    f0, f1 = sh["sf"]
    # 航拍镜没有「人」，用固定的远近替代
    if "航拍" in sh["jbcam"] or bg == "bg0":
        d0, d1 = 220.0, 120.0
    else:
        # dist_for() 按真人 1.75 m 解出真实距离，城市是 0.5 比例，距离要同比缩
        d0, d1 = dist_for(f0) * CITY_SCALE, dist_for(f1) * CITY_SCALE
        # 街是有宽度的：退得太远一定穿进两侧街墙。超限就压回来——
        # previz 的景别以能看清站位为准，不为了凑 subj_frac 把相机塞进楼里。
        d0, d1 = min(d0, 26.0), min(d1, 26.0)

    # 街景模型：**相机站在街心锚点，视线目标放在街道前方**。
    # 先前的做法是把相机退到目标后方，城一变密就退进街墙里（整片灰），
    # 且看不出街的纵深。站在街上顺着街看，两侧街墙才会向远处收进去。
    heading = street_heading(bg)
    ground_shot = not ("航拍" in sh["jbcam"] or bg == "bg0")

    # 远裁剪面拉到 6000：地面是大块四边形，四个顶点全在默认 100 m 之外时整块会被裁掉，
    # 画面就只剩近处建筑悬在黑里。裁剪面设置在 new_camera() 里。
    cam, cam_d = new_camera(f"cam_{sh['id']}", sc)

    # 空物体做视线目标，相机 TrackTo 它
    tgt = bpy.data.objects.new(f"tgt_{sh['id']}", None)
    look_h = 14.0 if "仰拍" in sh["jbcam"] else 1.2      # 仰拍看高处，其余看人的胸口
    if ground_shot:
        # 目标 ＝ 街道前方一段距离处（被摄主体站的位置）
        ahead = 16.0
        tgt.location = (target[0] + math.cos(heading) * ahead,
                        target[1] + math.sin(heading) * ahead,
                        max(0.0, target[2]) + look_h)
    else:
        tgt.location = (target[0], target[1], target[2] + look_h)
    sc.collection.objects.link(tgt)
    con = cam.constraints.new("TRACK_TO")
    con.target = tgt
    con.track_axis, con.up_axis = "TRACK_NEGATIVE_Z", "UP_Y"

    # 站在「来路」上朝目标看：heading 是行进方向，相机在它的反向（+180°）
    base_yaw = street_heading(bg) + math.pi + math.radians(yaw_off)

    def place(frame, d, yaw_extra=0.0):
        if ground_shot:
            # **站定 + 变焦**，不推拉。密城里沿街轴推拉一定会撞进建筑
            # （2026-09-19 实测：落幅那几帧整片灰＝相机在墙里）。
            # 相机固定在街心的安全位，用 angle_y 完成景别变化——
            # 好处是景别与 subj_frac 能精确对上，而不是靠距离估。
            z = max(0.0, target[2]) + max(1.0, h)
            base = (target[0] - math.cos(heading) * SAFE_BACK,
                    target[1] - math.sin(heading) * SAFE_BACK, z)
            cam.location = find_clear_cam(sc, base, tgt.location, heading)
            cam.keyframe_insert("location", frame=frame)
            # 人在 target 处，相机到他的距离 ＝ SAFE_BACK + ahead
            dist = SAFE_BACK + 16.0
            frac = max(0.02, min(0.95, HUMAN_H * CITY_SCALE / max(1e-6, d)))
            fov = 2.0 * math.atan(HUMAN_H * CITY_SCALE / (2.0 * dist * frac))
            fov = max(math.radians(8), min(math.radians(70), fov))
            # angle_y 不可打关键帧，改驱动焦距：lens = (sensor_h/2) / tan(fov/2)
            cam_d.lens = (cam_d.sensor_height / 2.0) / math.tan(fov / 2.0)
            cam_d.keyframe_insert("lens", frame=frame)
            return
        yaw = base_yaw + math.radians(yaw_extra)
        # 俯角才抬高相机；**仰角不许把相机压到地下**（负 pitch × 长距离会算出负高度，
        # 实测 39 m 距离下相机落到 -2.2 m，画面只剩悬空屋顶）。朝向由 TrackTo 负责，
        # 这里只管站位高度。
        rise = d * math.tan(math.radians(pitch)) if pitch > 0 else 0.0
        z = max(target[2] + 1.0, target[2] + h + rise)
        cam.location = (target[0] + math.cos(yaw) * d,
                        target[1] + math.sin(yaw) * d, z)
        cam.keyframe_insert("location", frame=frame)

    n = sc.frame_end
    if ground_shot:
        # 地面镜：把 subj_frac 直接喂给 place（它内部换算成 FOV）
        place(1, HUMAN_H * CITY_SCALE / max(0.02, f0))
        place(n, HUMAN_H * CITY_SCALE / max(0.02, f1))
        sc.camera = cam
        return cam
    if "环绕" in sh["jbcam"]:
        for k in range(0, 5):
            place(1 + int((n - 1) * k / 4), d0 + (d1 - d0) * k / 4, yaw_extra=k * 90 / 4)
    else:
        place(1, d0)
        place(n, d1)
    # Blender 5.1 的 Action 走 slot/layer，没有 .fcurves；默认插值已是 BEZIER，无需再设
    sc.camera = cam
    return cam


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    only = ""
    fps, res = 10, 1280
    for i, a in enumerate(argv):
        if a == "--only" and i + 1 < len(argv):
            only = argv[i + 1]
        if a == "--fps" and i + 1 < len(argv):
            fps = int(argv[i + 1])
        if a == "--res" and i + 1 < len(argv):
            res = int(argv[i + 1])

    shots, bgname = load_shots()
    if only:
        keep = {x.strip().upper() for x in only.split(",")}
        shots = [s for s in shots if s["id"] in keep]

    done = 0
    skip_existing = "--fresh" not in argv
    for sh in shots:
        d0 = os.path.join(SHOTS_DIR, sh["id"].lower().replace("s", "shot"))
        mp4_0 = os.path.join(d0, f"{os.path.basename(d0)}_previz.mp4")
        if skip_existing and os.path.isfile(mp4_0) and os.path.getsize(mp4_0) > 5000:
            print(f"[previz] {sh['id']} 已存在，跳过")
            continue
        bpy.ops.wm.open_mainfile(filepath=BLEND)
        sc = setup_scene(fps, res)
        sc.frame_start = 1
        sc.frame_end = max(8, int(sh["d"] * fps))
        make_camera(sh, sc)
        d = os.path.join(SHOTS_DIR, sh["id"].lower().replace("s", "shot"))
        os.makedirs(d, exist_ok=True)
        tmp = tempfile.mkdtemp(prefix="previz_")
        sc.render.filepath = os.path.join(tmp, "f_")
        bpy.ops.render.render(animation=True)
        mp4 = os.path.join(d, f"{os.path.basename(d)}_previz.mp4")
        cmd = [FFMPEG, "-y", "-loglevel", "error", "-framerate", str(fps),
               "-start_number", "1",          # Blender 从 f_0001.png 开始写
               "-i", os.path.join(tmp, "f_%04d.png"),
               "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "23", mp4]
        try:
            subprocess.run(cmd, check=True)
        except Exception as e:
            print(f"[previz] ffmpeg 失败 {sh['id']}: {e}")
        shutil.rmtree(tmp, ignore_errors=True)
        done += 1
        print(f"[previz] {sh['id']} {bgname[sh['bg']]} {sh['d']}s "
              f"{sh['jbcam']} sf={sh['sf']} -> {os.path.basename(d)}_previz.mp4")
    print(f"[previz] 完成 {done} 镜")


main()
