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
· 只渲**布局层灰模**（workbench，`color_type=SINGLE`，不吃材质与显示色），符合 rule 4h。

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
# 相机在街心沿街轴后退量的**上限**（缩放后的米）。实际退多少由 `street_axis()`
# 实测的净空决定，退不动就不退。
#
# 2026-09-21 定案：那 42 条地面 previz 渲成满屏屋顶，根因**不是**这个常数，
# 也不是先前猜的「锚点落在建筑体内」（八方向射线实测净空 bg1 3.0 m ｜ bg2 5.7 ｜
# bg3 5.6 ｜ bg4 4.5 ｜ bg7 3.3 ｜ bg9 6.9，锚点全在开阔街面上）。
# 根因是 `street_heading()` 给的**不是街的方向**——它是「上一站锚点 → 本站锚点」的
# 城市级直线方位角，横穿整座城，与该锚点脚下那条街的走向没有任何关系。
# 于是「沿 heading 后退 12 m」等于朝一个任意方向平移 12 m，街半宽只有 3–6 m，
# 必然进旁边的房子；`find_clear_cam()` 随即按顺序抬高、最后 `z+26` 升到屋顶之上。
# 修法：街的方向**由几何自己回答**（`street_axis()` 扫射线找真正通的那条轴），
# 后退量与前视距离都取实测净空，`dist` 也改成量出来的而不是假设的。
SAFE_BACK_MAX = 12.0

# 入城段七镜**不归本文件管**：它们由 `tools/previz_gate_sk2.py` 在查证过形制的
# `gate_scene.blend` 上手排机位，并直接装进 shots/shotNN/。
# 本文件如果也去渲它们，会用全城 blockout（城门段已证实差五处形制）的结果
# **覆盖掉那七条好的**，而且两个文件同名、只有内容不同，覆盖了也看不出来。
GATE_SHOTS = {"S01", "S02", "S03", "S04", "S05", "S06", "S07"}

# ── 内景：这些 bg 不在整城 blend 里，各有自己的 1:1 blend ──────────────
# 全城 blockout 只给每个地点一个**体块**，而这 15 条镜的相机站在体块**内部**，
# 渲出来是一整面灰墙。内景几何由 `tools/build_sk2_interiors.py` 确定性生成。
# **内景是 1:1，整城是 0.5**——所以凡是把真人身高换算成场景尺寸的地方，
# 比例都必须按镜取（`scale_of()`），不能再无脑乘 CITY_SCALE。
INTERIORS = {
    "bg12": "jiuguan",        # 镀金玫瑰旅店堂屋
    "bg10": "wangzuoting",    # 暴风要塞王座厅
    "bg5":  "zhantai",        # 深铁矿道地铁站台
    "bg6":  "chexiang",       # 水下段车厢
}
# 内景里**人站在哪**。室外镜的被摄点可以取「街轴前方 N 米」——那是一条有纵深的街，
# 看过去是街景；室内照搬这条就会把镜头指到一面白墙上（实测 S12 旅店：满屏墙皮）。
# 室内必须显式指定被摄点，让它落在这个空间真正的视觉重心上。
INTERIOR_SUBJECT = {
    "bg12": (-3.4, 4.6, 0.0),     # 壁炉前的长桌边
    "bg10": (0.0, 26.0, 0.0),     # 王座厅中央红毯，背后是台基王座
    "bg5":  (4.6, 24.0, 1.0),     # 站台面上，背后是拱顶与站台灯
    "bg6":  (0.0, 30.0, -2.85),   # 车厢内，背后是玻璃与水
}

# 内景的局部锚点（该 blend 自己的坐标，不套城市坐标）
INTERIOR_ANCHOR = {
    "bg12": (0.0, 4.5, 0.0),      # 堂屋中央
    "bg10": (0.0, 20.0, 0.0),     # 王座厅中段红毯上
    "bg5":  (4.6, 20.0, 1.0),     # 站台面中段。**避开 x=2.6 那排灯柱**——
                                  # 锚点落在柱子内部时八方向净空全是 0.1 m，街轴直接失效
    "bg6":  (0.0, 30.0, -2.85),   # 车厢内地板
}


def scale_of(bg):
    """该镜所在 blend 的比例：内景 1:1，整城 0.5。"""
    return 1.0 if bg in INTERIORS else CITY_SCALE


def blend_of(bg):
    """该镜要打开哪个 blend。"""
    if bg in INTERIORS:
        return os.path.join(A, "scenes", INTERIORS[bg], "_blender",
                            f"{INTERIORS[bg]}.blend")
    return BLEND


def anchor_of(bg):
    """该镜的锚点（已按各自 blend 的坐标系给出）。"""
    if bg in INTERIORS:
        return INTERIOR_ANCHOR[bg]
    return ANCHORS.get(bg, (0.0, 0.0, 0.0))

# 这条街装不下这个景别的镜：逐条记下来，跑完一次性列出（见 place() 里的 need_w 判定）
IMPOSSIBLE = []
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
        # 落地前两拍走**入城主路中轴线**（横向 0，巨像在 ±13.5 m 外），
        # 既不会蹭到巨像，又让末帧是「夹道巨像 + 远处城门楼」而不是贴着墙面的一块灰
        (26.0, (-87.0,  109.0,  30.0), (-25.0,   22.0,  10.0)),
        (28.0, (-69.0,   86.0,   8.0), (-3.0,     4.0,  10.0)),  # 石桥头高度，回望城门
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
        sh.color_type = "SINGLE"       # 单一灰：OBJECT 会吃物体显示色，
                                       # 深色内景（铁灰/水）会渲成一团黑（rule 4h）
        sh.single_color = (0.72, 0.72, 0.72)   # SINGLE 必须同时给色，不给就还是默认的暗色
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


def street_axis(sc, at, z, hint):
    """在锚点脚下**量出**这条街的真实走向，以及前后各能走多远。

    返回 `(轴向弧度, 前方净空 m, 后方净空 m)`。

    为什么不能用 `street_heading()`：那是「上一站 → 本站」的城市级直线方位角
    （见 SAFE_BACK_MAX 上方的定案），横穿整座城，跟脚下这条街无关。
    街的走向只有几何知道，所以在锚点处每 10° 打一条水平射线问「这个方向能走多远」，
    **一条街的特征是正反两头都通**，于是按 `min(正向, 反向)` 给每条轴打分。
    同分时取与 `hint`（行进方向）夹角小的那条，保证相机仍然朝着城里看，
    不会掉头朝城外——那是 2026-09-19 shot04 踩过的坑。
    """
    import mathutils
    dg = bpy.context.evaluated_depsgraph_get()
    o = mathutils.Vector((at[0], at[1], z))
    probe = 80.0

    def run(a):
        d = mathutils.Vector((math.cos(a), math.sin(a), 0.0))
        hit, loc, _n, _i, _ob, _m = sc.ray_cast(dg, o, d, distance=probe)
        return (mathutils.Vector(loc) - o).length if hit else probe

    step = math.radians(10.0)
    free = {k: run(k * step) for k in range(36)}
    best, best_score = None, -1.0
    for k in range(36):
        fwd, bwd = free[k], free[(k + 18) % 36]
        # 轴得分＝两头里较窄的一头；同分时偏向与 hint 同向的那条
        score = min(fwd, bwd) - 0.001 * abs(((k * step - hint + math.pi) % (2 * math.pi)) - math.pi)
        if score > best_score:
            best, best_score = k, score
    a = best * step
    return a, free[best], free[(best + 18) % 36]


def cam_clearance(sc, loc, n=12, probe=30.0):
    """相机**四周**最近的障碍有多远（水平一圈射线取最小）。

    为什么不能只看「到目标通视」：贴着墙站也是通视的——视线沿街射出去畅通无阻，
    可画框的一小半是那堵墙。2026-09-21 实测，S04/S05 修好街轴之后依然满屏灰墙，
    病根就在这里：`clear_of_geometry()` 回答的是「看得见吗」，
    而取景要问的是「**站得开吗**」。
    """
    import mathutils
    dg = bpy.context.evaluated_depsgraph_get()
    o = mathutils.Vector(loc)
    best = probe
    for k in range(n):
        a = 2 * math.pi * k / n
        d = mathutils.Vector((math.cos(a), math.sin(a), 0.0))
        hit, p, _nn, _i, _ob, _m = sc.ray_cast(dg, o, d, distance=probe)
        if hit:
            best = min(best, (mathutils.Vector(p) - o).length)
    return best


def lateral_room(sc, loc, heading, probe=60.0):
    """垂直于视轴的**左右可用宽度**（左净空 ＋ 右净空）。

    `cam_clearance()` 回答的是「四周最近的障碍有多远」，那是**站得开不开**的问题；
    取景要问的是另一个问题——**画框左右能铺多宽**。两者不能混用：
    ① 画框只往左右铺，**正前方与正后方的障碍不占画幅宽**（街尽头那堵墙不限制取景宽度）；
    ② 左右两边往往不对称（人站在街的一侧），用「2 × 最小值」会把宽的那边也按窄的算。
    实测差距很大：地铁站台按 2×min 算是 3.3 m，按左右实测是整条隧道的 13 m。
    """
    import mathutils
    dg = bpy.context.evaluated_depsgraph_get()
    o = mathutils.Vector(loc)
    total = 0.0
    for sgn in (1.0, -1.0):
        d = mathutils.Vector((-math.sin(heading) * sgn, math.cos(heading) * sgn, 0.0))
        start, travelled = o.copy(), 0.0
        for _ in range(6):          # 最多穿 6 层透明件，够用且不会死循环
            hit, p, _n, _i, ob, _m = sc.ray_cast(dg, start, d, distance=probe - travelled)
            if not hit:
                travelled = probe
                break
            step = (mathutils.Vector(p) - start).length
            travelled += step
            # **窗户不是墙**：玻璃挡光线投射，却不挡取景——车厢侧窗被算成障碍时，
            # 水下段的可用画幅宽只剩 2.7 m（车厢内宽），而这几镜拍的正是
            # 窗外的隧道与水体。遇到透明件就穿过去接着量。
            if any(k in ob.name for k in ("glass", "玻璃", "_win", "C_glass")):
                start = mathutils.Vector(p) + d * 0.05
                travelled += 0.05
                continue
            break
        total += min(travelled, probe)
    return total


def find_clear_cam(sc, base_loc, tgt_loc, heading, ground=True):
    """在街心附近找一个能看见目标的机位。

    密城里按公式算出来的位置常常正对着一栋楼（2026-09-19 实测：贸易区那一镜
    正中杵着一整面墙）。这里按「先抬高、再左右挪、最后后退」的顺序试，
    第一个通视的就用——**几何自己回答，不靠猜**。

    ⚠️ **已知缺陷，未修（2026-09-20）**：密城里街心几乎必然被挡，于是本函数的第一反应
    是把相机抬高（兜底更是 `z+26` 升到屋顶之上）——**42 条地面镜因此全渲成满屏屋顶斜面**。
    试过把顺序改成「左右 → 后退 → 才轻微抬」并去掉升空兜底，结果**更差**：
    相机贴死在墙里、整片灰（S16/S17 实测 σ=1）。
    说明真正的病灶不在搜索顺序，而在**基准机位本身就落在建筑体内**——
    很可能是街心锚点与 `build_infill()` 街区填充块的坐标关系不对。
    在查清之前保留升空行为：**屋顶视角虽然构图不对，至少还看得见几何**。
    修的时候应当先验证「街心锚点是否真的落在开阔街面上」，而不是继续调这个搜索。
    """
    x, y, z = base_loc
    # **先量头顶有多高**：本函数会为了找通视位置往上抬，而「抬到屋顶外面」
    # 在空旷度上永远赢过屋里任何位置（外面净空＝探针上限），
    # 于是每条室内镜都被抬穿天花板（2026-09-21 实测 S12：画面是天花板背面）。
    # 有顶就把抬升量卡在净空以内；露天则不限。
    import mathutils as _mu
    _dg = bpy.context.evaluated_depsgraph_get()
    _hit, _p, *_ = sc.ray_cast(_dg, _mu.Vector((x, y, z)), _mu.Vector((0, 0, 1)),
                               distance=60.0)
    head_room = ((_mu.Vector(_p) - _mu.Vector((x, y, z))).length - 0.6) if _hit else 1e9
    nx, ny = -math.sin(heading), math.cos(heading)      # 街的法向
    # 通视 **且** 站得开才算数（见 cam_clearance 的注释）。
    #
    # 顺序很要紧：**本来就站得住的机位，一步都不要挪**。
    # 先前这里无条件挑「最宽敞的候选」，结果室内镜全被抬到近天花板——
    # 家具之间的眼高位置净空当然不如头顶那片空气大，于是它次次选头顶
    # （实测 S12：5 m 层高的旅店里相机站到 3.6 m，画面是天花板与墙的夹角）。
    # 空旷度只用来在**被挡之后**的候选里排序，不能用来否决一个本来就合格的机位。
    MIN_ROOM = 1.5
    if clear_of_geometry(sc, (x, y, z), tgt_loc) and cam_clearance(sc, (x, y, z)) >= MIN_ROOM:
        return (x, y, z)
    best, best_room = None, -1.0
    for dz in (0.0, 2.0, 5.0, 9.0, 14.0, 20.0):
        if dz > head_room:
            continue
        for side in (0.0, 3.0, -3.0, 6.0, -6.0, 9.0, -9.0):
            for back in (0.0, 4.0, 8.0, -4.0):
                c = (x + nx * side - math.cos(heading) * back,
                     y + ny * side - math.sin(heading) * back, z + dz)
                if not clear_of_geometry(sc, c, tgt_loc):
                    continue
                room = cam_clearance(sc, c)
                if room > best_room:
                    best, best_room = c, room
        # **抬升是最后手段**：这一层里只要找到站得开的就收手，不去更高处比空旷
        if best is not None and best_room >= MIN_ROOM:
            return best
    if best is not None:
        return best
    # 全挡住才升到屋顶之上。**必须喊出来**：这 42 条镜之所以能一路错到成品，
    # 就是因为这条兜底是静默的——渲出来是「屋顶视角」，日志里却一片祥和。
    print(f"[previz] ⚠ 街心到目标全程被挡，升空兜底 @ {x:.1f},{y:.1f}")
    return (x, y, z + min(26.0, max(0.0, head_room)))


def make_proxy(sc, x, y, z, scale, heading):
    """被摄点上的 1.75 m 人形替身：腿 + 躯干 + 头 + 朝向标。

    previz 只要**尺度、站位、朝向**三件事，不要长相（长相归参考图）。
    比例按所在 blend 走：整城 0.5、内景 1:1。
    """
    H = HUMAN_H * scale
    parts = []
    bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=0.11 * scale,
                                        depth=0.49 * H, location=(0, 0, 0.25 * H))
    parts.append(bpy.context.object)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.66 * H))
    o = bpy.context.object
    o.scale = (0.24 * H, 0.14 * H, 0.35 * H)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    parts.append(o)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.066 * H, location=(0, 0, 0.92 * H))
    parts.append(bpy.context.object)
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.055 * H, depth=0.15 * H,
                                    location=(0, 0.11 * H, 0.74 * H))
    parts.append(bpy.context.object)

    root = bpy.data.objects.new("PROXY", None)
    sc.collection.objects.link(root)
    for p in parts:
        p.parent = root
    root.location = (x, y, z)
    root.rotation_euler = (0, 0, heading + math.pi)   # 面朝来路（也就是面朝相机）
    return root


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
    target = anchor_of(bg)
    SC = scale_of(bg)          # 内景 1:1、整城 0.5——凡真人尺寸换算都按这个
    h, pitch, yaw_off = cam_rig(sh["jbcam"])
    f0, f1 = sh["sf"]
    # 航拍镜没有「人」，用固定的远近替代
    if "航拍" in sh["jbcam"] or bg == "bg0":
        d0, d1 = 220.0, 120.0
    else:
        # dist_for() 按真人 1.75 m 解出真实距离，城市是 0.5 比例，距离要同比缩
        d0, d1 = dist_for(f0) * SC, dist_for(f1) * SC
        # 街是有宽度的：退得太远一定穿进两侧街墙。超限就压回来——
        # previz 的景别以能看清站位为准，不为了凑 subj_frac 把相机塞进楼里。
        d0, d1 = min(d0, 26.0), min(d1, 26.0)

    # 街景模型：**相机站在街心锚点，视线目标放在街道前方**。
    # 先前的做法是把相机退到目标后方，城一变密就退进街墙里（整片灰），
    # 且看不出街的纵深。站在街上顺着街看，两侧街墙才会向远处收进去。
    ground_shot = not ("航拍" in sh["jbcam"] or bg == "bg0")
    heading = street_heading(bg)
    look_h = 14.0 if "仰拍" in sh["jbcam"] else 1.2      # 仰拍看高处，其余看人的胸口
    back, fwd_room = 0.0, 16.0
    if ground_shot:
        # 街的走向与前后净空都**量出来**，不猜（见 SAFE_BACK_MAX 上方的定案）。
        # 高度取**看向点的高度**，不取眼高：实测 S20 眼高 1.6 的射线从王座厅台基上方
        # 掠过、报 20 m 通畅，而看向点在 z=1.2 正好埋进三级台基里，
        # 于是通视判定必然失败、升空兜底把相机捅穿了 14 m 高的屋顶。
        heading, f_room, b_room = street_axis(sc, target, max(0.0, target[2]) + look_h,
                                              street_heading(bg))
        fwd_room = max(4.0, min(16.0, f_room - 2.0))
        back = max(0.0, min(SAFE_BACK_MAX, b_room - 2.0))
        print(f"[previz] {sh['id']} {bg} 街轴 {math.degrees(heading):6.1f}° "
              f"前 {f_room:.1f}m 后 {b_room:.1f}m → 退 {back:.1f} 看前 {fwd_room:.1f}")

    # 远裁剪面拉到 6000：地面是大块四边形，四个顶点全在默认 100 m 之外时整块会被裁掉，
    # 画面就只剩近处建筑悬在黑里。裁剪面设置在 new_camera() 里。
    cam, cam_d = new_camera(f"cam_{sh['id']}", sc)

    # 空物体做视线目标，相机 TrackTo 它
    tgt = bpy.data.objects.new(f"tgt_{sh['id']}", None)
    if ground_shot:
        # 目标 ＝ 被摄主体站的位置。室内用显式被摄点（见 INTERIOR_SUBJECT），
        # 室外取「街轴前方 fwd_room 米」——距离取实测净空，不写死 16，
        # 街短的地方写死会把被摄点放到墙里去。
        ahead = fwd_room
        if bg in INTERIOR_SUBJECT:
            sx, sy, sz = INTERIOR_SUBJECT[bg]
            subj_xy = (sx, sy, sz)
            ahead = max(2.0, math.dist((sx, sy), (target[0], target[1])))
        else:
            # **被摄点要站在街上最开阔的那一段**，不是「能走多远走多远」。
            # 先前取 `fwd_room`（＝净空减 2 m），等于把人贴在前方那堵墙根下，
            # 于是他身边的可用画幅宽只剩 2–3 m——远景当然摆不出来，
            # 而这会被误读成「镜表的景别写得太贪」。实测：贸易区 2.9 m、旧城区 2.6 m。
            # 沿街轴采样，挑周围最空的那一点；同样空旷时取靠前的，画面才有纵深。
            z_probe = max(0.0, target[2]) + 1.6
            best_t, best_room = 2.0, -1.0
            for t in (2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 16.0):
                if t > fwd_room:
                    break
                px = target[0] + math.cos(heading) * t
                py = target[1] + math.sin(heading) * t
                r = cam_clearance(sc, (px, py, z_probe))
                if r >= best_room - 0.15:        # 并列时偏向更远（画面有纵深）
                    best_t, best_room = t, max(r, best_room)
            ahead = best_t
            subj_xy = (target[0] + math.cos(heading) * ahead,
                       target[1] + math.sin(heading) * ahead,
                       max(0.0, target[2]))
        tgt.location = (subj_xy[0], subj_xy[1], subj_xy[2] + look_h)
    else:
        tgt.location = (target[0], target[1], target[2] + look_h)
    sc.collection.objects.link(tgt)
    con = cam.constraints.new("TRACK_TO")
    con.target = tgt
    con.track_axis, con.up_axis = "TRACK_NEGATIVE_Z", "UP_Y"

    # **被摄点上放一个人形替身**（rule 4h ①：previz 锁的是站位与动作时刻表）。
    # 先前 44 条 previz 里一个人都没有，于是「人占画高」全是纸上算出来的数字，
    # 画面里根本没有可对照的东西——景别对没对上，看片子的人无从判断。
    if ground_shot:
        make_proxy(sc, tgt.location[0], tgt.location[1],
                   tgt.location[2] - look_h, SC, heading)

    # 站在「来路」上朝目标看：heading 是行进方向，相机在它的反向（+180°）
    base_yaw = street_heading(bg) + math.pi + math.radians(yaw_off)

    def place(frame, d, yaw_extra=0.0):
        if ground_shot:
            # **先用距离凑景别，焦距只当兜底**。
            # 原来是「站定 + 变焦」：相机钉在街心的安全位，全靠 FOV 变景别。
            # 那条规则在远景上没问题，在近景上会出灾难——实测 S12（旅店近景 0.9）
            # 被摆成「站在 11.8 m 外用 9° 长焦怼一个点」，画面里只有一块墙皮，
            # 人和房间全都没了。真实近景是**走过去拍**，不是隔着屋子拉长焦。
            # 所以：算出该景别对应的距离，退不到那么远就退到街允许的最远，
            # 剩下的差额才交给 FOV 补（下面那段 fov 计算不变，景别照样精确）。
            z = max(0.0, target[2]) + max(1.0, h)
            frac_want = max(0.02, min(0.95, HUMAN_H * SC / max(1e-6, d)))
            d_want = dist_for(frac_want) * SC
            d_use = max(1.0 * SC, min(d_want, back + ahead))
            base = (tgt.location[0] - math.cos(heading) * d_use,
                    tgt.location[1] - math.sin(heading) * d_use, z)
            cam.location = find_clear_cam(sc, base, tgt.location, heading, ground=ground_shot)
            cam.keyframe_insert("location", frame=frame)
            # **量出来的距离**，不是假设的。find_clear_cam 有权把相机挪走，
            # 先前这里写死 `SAFE_BACK + 16`，相机一被挪动景别就对不上了。
            dist = max(1.0, math.dist(cam.location, tgt.location))
            frac = max(0.02, min(0.95, HUMAN_H * SC / max(1e-6, d)))
            fov = 2.0 * math.atan(HUMAN_H * SC / (2.0 * dist * frac))
            # 这个景别，**相机退得到那个位置吗**？退不到就点名喊出来。
            #
            # 2026-09-22 更正：先前这里问的是「画幅比房间宽吗」，**那个问题问错了**。
            # 画幅比房间宽根本不是失败——墙会把画框填满，那正是室内远景该有的样子
            # （一个人很小、整间屋子都在画面里）。按那个口径判，18 m 宽的王座厅
            # 会被判成「装不下远景」，于是逼着把「高机位俯瞰」的落幅改成 0.80 近景，
            # 数值合规了、和分镜写的「俯瞰」正好相反。
            # 真正的物理限制只有一条：**要让人只占画高的 frac，相机必须退到 d 远，
            # 而它背后未必有那么长的地方**。退不到就只能改景别、换地点或换镜头。
            # 退不远就换广角——这是**现场真会做的事**，不是失败。
            # 唯一真正做不到的情形是：退到头之后镜头得广到开始变形。
            # （这条判据换过三次，前两次都问错了问题：
            #  「画幅比房间宽吗」——墙填满画框正是室内远景的样子，不是失败；
            #  「退得到那么远吗」——退不到就换广角，画面照样成立。
            #  真正的物理下限只有镜头角度。）
            MAX_FOV = math.radians(75.0)        # 再广就是鱼眼感，人会被拉变形
            if fov > MAX_FOV:
                need_d = dist_for(frac) * SC
                IMPOSSIBLE.append(
                    f"{sh['id']} {bg} 人占画高 {frac:.2f}：退到头（{(back + ahead) / SC:.0f} m）"
                    f"仍需 {math.degrees(fov):.0f}° 广角（应退到 {need_d / SC:.0f} m）")
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
        place(1, HUMAN_H * SC / max(0.02, f0))
        place(n, HUMAN_H * SC / max(0.02, f1))
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
        if sh["id"] in GATE_SHOTS:
            print(f"[previz] {sh['id']} 归 previz_gate_sk2.py（入城段），跳过")
            continue
        d0 = os.path.join(SHOTS_DIR, sh["id"].lower().replace("s", "shot"))
        mp4_0 = os.path.join(d0, f"{os.path.basename(d0)}_previz.mp4")
        if skip_existing and os.path.isfile(mp4_0) and os.path.getsize(mp4_0) > 5000:
            print(f"[previz] {sh['id']} 已存在，跳过")
            continue
        bpy.ops.wm.open_mainfile(filepath=blend_of(sh['bg']))
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
    if IMPOSSIBLE:
        # 不是渲染失败，是**镜表要的景别这个地方做不出来**：
        # 相机已经退到底，还得上 75° 以上的超广角，人会被拉变形。
        # 逐条点名，交给排镜去改 subj_frac、换地点或接受畸变。
        print(f"[previz] ⚠ {len(IMPOSSIBLE)} 处景别在现场做不出来（退到头还得上超广角）：")
        for line in dict.fromkeys(IMPOSSIBLE):
            print(f"    · {line}")


main()
