# -*- coding: utf-8 -*-
"""暴风城**入城段**的彩色高精场景：城门 + 英雄谷 + 北端屏墙。

形制唯一出处
------------
`ai_videos/shikong_lvxing/sk2/2_世界观人设/scenes/stormwind/_gate_research/gate_spec.md`
（2026-09-20 调研，14 张 Vanilla 参考图逐张版本判定）。**改形制先改那份规格书，再改这里。**

与 `build_stormwind.py` 的分工（rule 4g ④「几何精度按镜头接近度分级」）
------------------------------------------------------------------
那个建的是**全城 blockout**（灰盒子，给 42 条街景 previz 定机位）；
本文件建的是**一个地点的高精彩色场景**——S01–S07 是贴身穿过城门的 hero 镜，
「贴身而过 ＝ 真立面」，blockout 精度在这里不够看。
共用坐标约定：**原点 ＝ 城门正中，+Y 进城（北），+Z 向上，米，1:1 不缩放**。

第一版（`build_gate_scene.py.v1`）错在哪 —— 五条，全部推翻
----------------------------------------------------------
① **门上方加了实心过梁** —— 真实是两座圆塔之间的**豁口**，只有一对 12 m 木门扇，
   上方什么都没有。有过梁，「穿过城门」就变成了「钻隧道」。
② **水面放在城外** —— 真实是**门内**英雄谷两侧各一片水，引道是两片水之间的石堤；
   城外只有土路草地与两侧土黄陡岩。方向整个反了。
③ **12 尊雕像沿全程排开** —— 真实是 **5 尊挤在北端 30 m 内**、本体 15 m 高。
   「前段空旷石堤 → 尽头五像压顶」的节奏被摊平抹掉。
④ **塔只有 2 座、灰棱锥帽** —— 真实 **4 座**：内侧 2 座高瘦圆塔配**蓝色肋纹锥顶**，
   外侧 2 座矮粗堡塔配**蜜色木甲板顶**。丢了蓝锥顶就丢了暴风城第一识别特征。
⑤ **北端什么都没有** —— 真实是**三拱屏墙 + 图拉扬方台 + 大阶梯 + 蓝瓦半木大屋**，
   那是从城外望进来的视线尽头。

雕像从哪来
----------
**不是脚本建的**。`ai_video.md` §28 实测：Rodin 的 text-only 做不了整身着装人像
（出来是躺倒的光滑坨）。走 rule 4d 的「图先行」：纯文字出我们自己的三视图锚点图 →
那三张喂 image-to-3D → `whitemodel_normalize.py` 归一 → 本文件 import。
**权利人的官方图绝不上传生成模型**（`divergence #108`）。
`STATUES` 里 `mesh` 为 None 的先放占位柱，场景照样能渲、能看节奏。

用法（仓库根目录）：
    blender -b --factory-startup --python tools/build_gate_scene.py -- --out <绝对路径>.blend
    blender -b --factory-startup --python tools/build_gate_scene.py -- --out x.blend --check <目录>
"""
import math
import sys
from pathlib import Path

import bpy

# ══ 数值表：逐条对应 gate_spec.md §3。`实测` ＝ 两组独立量测，`估` ＝ 单组或比例外推 ══
ROAD_W = 8.0                              # 主路净宽                     实测
WALK_W = 2.5                              # 单侧人行道（人字砖）         估
KERB_H = 0.30                             # 路缘石高                     估
BAL_H, BAL_T = 1.0, 0.5                   # 外缘矮石栏 高 / 厚           估
LAMP_H, LAMP_GAP = 4.3, 12.0              # 街灯全高 / 间距              实测 / 估

GATE_W = 10.0                             # 门洞净宽                     实测
DOOR_W, DOOR_H, DOOR_T = 5.0, 12.0, 0.5   # 单扇门 宽/高/厚              实测
IN_TOWER_D, IN_TOWER_Z = 8.0, 18.0        # 内侧高塔 直径 / 雉堞顶标高   估
CONE_H, CONE_D = 6.5, 8.8                 # 蓝锥顶 高 / 底径             估
POLE_H, FLAG_L = 4.0, 3.5                 # 锥尖旗杆 / 燕尾旗            估
OUT_TOWER_D, OUT_CREN_Z, OUT_DECK_Z = 13.0, 13.0, 11.5   # 外堡塔        估
WALL_Z, WALL_T = 11.0, 3.5                # 城墙 垛顶标高 / 厚           估
MER_W, MER_H, MER_GAP = 1.6, 1.1, 1.6     # 方齿 宽/高/齿距              估
LION_W, LION_H, LION_Z = 2.4, 2.2, 5.0    # 塔基狮首石雕                 估
BANNER_W, BANNER_L = 3.2, 8.0             # 外堡大旗                     估
WATER_W, WATER_DZ = 20.0, 2.5             # 门内护城水面 宽 / 低于路面   估

STATUE_H = 15.0                           # 雕像本体高                   实测
PLINTH_D, PLINTH_Z = 10.0, 4.0            # 八角基座 对边径 / 高         估
STATUE_X = 11.0                           # 雕像中心距主路中线           实测
STATUE_Y_S, STATUE_Y_N = 118.0, 136.0     # 南对 / 北对 Y 位             估
TURALYON = (8.0, 6.0, 3.0)                # 图拉扬方台                   估
SCREEN_Y = 148.0                          # 北端屏墙 Y 位                估
ARCH_W, ARCH_H, SCREEN_Z = 12.0, 10.0, 12.0   # 屏墙 拱跨/拱高/垛顶      估
TRADE_Y = 180.6                           # 贸易区南入口（由 GM 坐标算出）

# ══ 配色：逐条对应 gate_spec.md §5。自然色名 → 线性 RGB。
#    「零 hex」是 prompt 的规矩；这里是渲染数值，不进 prompt。 ══
PALETTE = {
    "月白墙石":   (0.74, 0.72, 0.67),   # 受光近象牙白、背光转青灰
    "冷月白":     (0.80, 0.80, 0.78),   # 雕像石材，比墙石更冷更浅
    "暗金":       (0.42, 0.33, 0.11),   # 雕像边饰 / 纹章（**不是素灰石像**）
    "宝蓝锥顶":   (0.10, 0.20, 0.58),   # 饱和群青偏亮
    "深靛暗带":   (0.05, 0.10, 0.34),   # 叠瓦肋纹之间的暗带
    "宝蓝瓦":     (0.13, 0.22, 0.48),   # 屋瓦，比锥顶略淡略灰
    "藏蓝旗":     (0.05, 0.09, 0.30),
    "靛紫旗":     (0.16, 0.10, 0.38),
    "蜜色松木":   (0.52, 0.36, 0.16),   # 外堡甲板 / 门扇顶帽条
    "蓝灰深木":   (0.15, 0.16, 0.19),   # 门板面
    "深铁灰":     (0.06, 0.06, 0.07),
    "琥珀金":     (0.60, 0.40, 0.10),   # 灯笼玻璃
    "暖米白路":   (0.76, 0.72, 0.63),
    "土黄人字砖": (0.40, 0.30, 0.17),
    "青蓝水":     (0.05, 0.18, 0.30),
    "深棕木":     (0.18, 0.11, 0.06),
    "米白灰泥":   (0.72, 0.70, 0.64),
    "黄绿草":     (0.20, 0.26, 0.09),
    "灰白碎石":   (0.55, 0.54, 0.50),
    "土黄岩":     (0.36, 0.30, 0.18),
}

# (编号, 人物, X 侧 ±1, Y, 归一后的 .blend 或 None)
# (编号, 目录名, X 侧 ±1, Y, 面朝南要不要转 180°)
# 归一后的网格**自带基座**（15 m 本体 + 4 m 台 ＝ 19 m，与 gate_spec 一致），
# 所以脚本不再另建基座——否则会叠两层台。
STATUE_DIR = REPO_PROPS = None   # 见 statue_blend()
STATUES = [
    (1, "p23_库德兰像",   -1, STATUE_Y_S),
    (2, "p26_丹娜斯像",   +1, STATUE_Y_S),
    (3, "p24_卡德加像",   -1, STATUE_Y_N),
    (4, "p27_奥蕾莉亚像", +1, STATUE_Y_N),
]
TURALYON_DIR = "p25_图拉扬像"    # 中轴最北，正朝南（全段唯一正朝向）


def argv():
    a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    return {x[2:]: a[i + 1] for i, x in enumerate(a) if x.startswith("--") and i + 1 < len(a)}


def mat(name):
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    r, g, bl = PALETTE[name]
    b.inputs["Base Color"].default_value = (r, g, bl, 1.0)
    if name == "青蓝水":
        b.inputs["Roughness"].default_value = 0.05
    elif name in ("深铁灰", "琥珀金", "暗金"):
        b.inputs["Metallic"].default_value = 1.0
        b.inputs["Roughness"].default_value = 0.4
    else:
        b.inputs["Roughness"].default_value = 0.85
    return m


def box(name, loc, size, color, parent=None, rot=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    o = bpy.context.object
    o.name, o.scale, o.rotation_euler = name, size, (0, 0, rot)
    # 必须显式给 flags：不写会把 location 烘进网格，物体落到 2× 位置（本仓库踩过）
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(mat(color))
    if parent:
        o.parent = parent
    return o


def cyl(name, loc, r, h, color, parent=None, verts=24):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=loc)
    o = bpy.context.object
    o.name = name
    o.data.materials.append(mat(color))
    if parent:
        o.parent = parent
    return o


def cone(name, loc, r, h, color, parent=None, verts=24):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, depth=h, location=loc)
    o = bpy.context.object
    o.name = name
    o.data.materials.append(mat(color))
    if parent:
        o.parent = parent
    return o


def ring_merlons(root, tag, cx, cy, radius, top_z, n=14):
    for i in range(n):
        a = 2 * math.pi * i / n
        box(f"{tag}_mer{i:02d}",
            (cx + math.cos(a) * radius, cy + math.sin(a) * radius, top_z + MER_H / 2),
            (MER_W, MER_W, MER_H), "月白墙石", root, rot=a)


def line_merlons(root, tag, y, x0, x1, top_z, thick):
    i, x = 0, x0
    while x < x1:
        box(f"{tag}_m{i:02d}", (x + MER_W / 2, y, top_z + MER_H / 2),
            (MER_W, thick, MER_H), "月白墙石", root)
        x += MER_W + MER_GAP
        i += 1


def build_terrain(root):
    """门外：灰白碎石小径 + 黄绿草 + 两侧土黄陡岩。门内：石堤与两侧水面。"""
    box("T_grass_out", (0, -110, -0.5), (420, 250, 1.0), "黄绿草", root)
    box("T_path_out", (0, -110, 0.06), (7.0, 250, 0.16), "灰白碎石", root)
    for sgn in (-1, +1):
        box(f"T_cliff_{sgn:+d}", (sgn * 62, -110, 9.0), (26, 250, 20.0), "土黄岩", root)

    # 门内：英雄谷的石堤基面 + 两侧水（**这是 v1 搞反的地方**）
    box("T_valley_base", (0, (TRADE_Y + 30) / 2, -1.2), (150, TRADE_Y + 40, 2.4),
        "月白墙石", root)
    for sgn in (-1, +1):
        # 水的内缘**由雕像基座定，不由路缘定**（2026-09-21，S06 高机位俯拍抓到）：
        # 先前内缘算在 x=8，而基座中心 x=11、对边径 10 → 基座占 6…16，
        # 于是五尊巨像有一半泡在水里。gate_spec 里 `STATUE_X` 是**实测**、
        # 水面宽窄位置是**估**，所以让估的那个让路。外缘保持原位，只把内缘推出去。
        w_in = STATUE_X + PLINTH_D / 2 + 1.0          # 17.0：基座外沿再留 1 m 岸
        w_out = ROAD_W / 2 + WALK_W + BAL_T + WATER_W + 1.0   # 28.0，与原来一致
        box(f"T_water_{sgn:+d}", (sgn * (w_in + w_out) / 2, 66.0, -WATER_DZ / 2),
            (w_out - w_in, 116.0, WATER_DZ), "青蓝水", root)


def build_causeway(root):
    L = TRADE_Y + 24
    box("R_road", (0, L / 2 - 12, 0.10), (ROAD_W, L, 0.20), "暖米白路", root)
    for sgn in (-1, +1):
        box(f"R_walk_{sgn:+d}", (sgn * (ROAD_W / 2 + WALK_W / 2), L / 2 - 12, 0.16),
            (WALK_W, L, 0.32), "土黄人字砖", root)
        box(f"R_kerb_{sgn:+d}", (sgn * (ROAD_W / 2), L / 2 - 12, KERB_H / 2),
            (0.25, L, KERB_H), "月白墙石", root)
        box(f"R_bal_{sgn:+d}", (sgn * (ROAD_W / 2 + WALK_W + BAL_T / 2), L / 2 - 12, BAL_H / 2),
            (BAL_T, L, BAL_H), "月白墙石", root)


def build_gate(root):
    """**门上方什么都没有**——两座圆塔之间的豁口 + 一对 12 m 木门扇（常开外张）。"""
    inner_x = GATE_W / 2 + IN_TOWER_D / 2
    outer_x = inner_x + IN_TOWER_D / 2 + OUT_TOWER_D / 2 + 1.0

    for sgn in (-1, +1):
        tag = "L" if sgn < 0 else "R"
        # 内侧高瘦圆塔：塔身 + 雉堞 + 蓝色肋纹锥顶 + 锥尖旗杆燕尾旗
        cyl(f"G_in_{tag}", (sgn * inner_x, 0, IN_TOWER_Z / 2), IN_TOWER_D / 2,
            IN_TOWER_Z, "月白墙石", root)
        ring_merlons(root, f"G_in_{tag}", sgn * inner_x, 0, IN_TOWER_D / 2 - MER_W / 2,
                     IN_TOWER_Z)
        cz = IN_TOWER_Z + MER_H
        cone(f"G_cone_{tag}", (sgn * inner_x, 0, cz + CONE_H / 2), CONE_D / 2, CONE_H,
             "宝蓝锥顶", root)
        for k in range(8):           # 叠瓦肋纹：锥面压几道深靛暗带
            a = 2 * math.pi * k / 8
            box(f"G_rib_{tag}{k}",
                (sgn * inner_x + math.cos(a) * CONE_D * 0.24,
                 math.sin(a) * CONE_D * 0.24, cz + CONE_H * 0.42),
                (0.22, 0.22, CONE_H * 0.78), "深靛暗带", root, rot=a)
        pz = cz + CONE_H
        cyl(f"G_pole_{tag}", (sgn * inner_x, 0, pz + POLE_H / 2), 0.12, POLE_H,
            "深铁灰", root, verts=8)
        box(f"G_pennant_{tag}", (sgn * inner_x + FLAG_L / 2, 0, pz + POLE_H - 0.9),
            (FLAG_L, 0.06, 1.3), "靛紫旗", root)

        # 外侧矮粗堡塔：塔身 + 蜜色木甲板 + 雉堞 + 蓝底金狮大旗 + 塔基狮首
        cyl(f"G_out_{tag}", (sgn * outer_x, 0, OUT_CREN_Z / 2), OUT_TOWER_D / 2,
            OUT_CREN_Z, "月白墙石", root)
        cyl(f"G_deck_{tag}", (sgn * outer_x, 0, OUT_DECK_Z), OUT_TOWER_D / 2 - 0.6,
            0.4, "蜜色松木", root)
        ring_merlons(root, f"G_out_{tag}", sgn * outer_x, 0, OUT_TOWER_D / 2 - MER_W / 2,
                     OUT_CREN_Z, n=18)
        by = -OUT_TOWER_D / 2 - 0.2
        box(f"G_banner_{tag}", (sgn * outer_x, by, OUT_CREN_Z - BANNER_L / 2),
            (BANNER_W, 0.12, BANNER_L), "藏蓝旗", root)
        box(f"G_lionemb_{tag}", (sgn * outer_x, by - 0.1, OUT_CREN_Z - BANNER_L / 2),
            (BANNER_W * 0.48, 0.06, BANNER_L * 0.30), "暗金", root)
        box(f"G_lionhead_{tag}", (sgn * outer_x, by - 0.3, LION_Z),
            (LION_W, 1.0, LION_H), "月白墙石", root)

        # 门扇：常开外张，绕门洞边铰接转出约 65°
        ang = math.radians(65) * (1 if sgn > 0 else -1)
        hinge = sgn * GATE_W / 2
        box(f"G_door_{tag}",
            (hinge + sgn * math.cos(ang) * DOOR_W / 2,
             -abs(math.sin(ang)) * DOOR_W / 2, DOOR_H / 2),
            (DOOR_W, DOOR_T, DOOR_H), "蓝灰深木", root, rot=ang)

        # 两侧城墙从外堡塔接出去；**门洞上方不封**
        x0, x1 = sgn * (outer_x + OUT_TOWER_D / 2), sgn * 210.0
        xa, xb = min(x0, x1), max(x0, x1)
        box(f"G_wall_{tag}", ((xa + xb) / 2, 0, WALL_Z / 2), (xb - xa, WALL_T, WALL_Z),
            "月白墙石", root)
        line_merlons(root, f"G_wall_{tag}", 0.0, xa, xb, WALL_Z, WALL_T)


def humanoid(name, loc, height, color, parent=None, yaw=0.0):
    """粗人形替身。previz 只需要**体量、姿态、朝向**，不需要长相。

    为什么不用方柱：15 m 的素白方板读起来是**墙**，不是巨像——
    2026-09-20 排 S03 机位时连试六组构图全被白板占满，换成人形后才判得出来。
    **占位物的形状会影响构图判断，所以占位物也要像那个东西。**
    """
    h = height
    parts = []
    parts.append(cyl(f"{name}_leg", (loc[0], loc[1], loc[2] + h * 0.26),
                     h * 0.10, h * 0.52, color, parent, verts=10))
    parts.append(box(f"{name}_torso", (loc[0], loc[1], loc[2] + h * 0.68),
                     (h * 0.24, h * 0.14, h * 0.36), color, parent))
    parts.append(box(f"{name}_head", (loc[0], loc[1], loc[2] + h * 0.92),
                     (h * 0.13, h * 0.13, h * 0.13), color, parent))
    # 一条斜举的手臂 + 一件持物，让剪影一眼看出是「人像」而不是柱子
    parts.append(box(f"{name}_arm", (loc[0] + h * 0.20, loc[1], loc[2] + h * 0.72),
                     (h * 0.30, h * 0.08, h * 0.08), color, parent, rot=0.0))
    parts.append(box(f"{name}_prop", (loc[0] + h * 0.34, loc[1], loc[2] + h * 0.86),
                     (h * 0.06, h * 0.06, h * 0.34), color, parent))
    for p in parts:
        p.rotation_euler = (0, 0, yaw)
    return parts


def statue_blend(dirname):
    """归一后的 .blend 路径。`build_sk2_whitemodels.py --gate` 的产物。"""
    return (Path(__file__).resolve().parent.parent / "ai_videos" / "shikong_lvxing" / "sk2" /
            "2_世界观人设" / "props" / dirname / "whitemodel" / f"{dirname}.blend")


def place_statue(root, tag, dirname, loc, yaw):
    """append 归一网格；缺了就退回人形占位（场景照样能渲、能看节奏）。"""
    b = statue_blend(dirname)
    if b.exists():
        before = set(bpy.data.objects)
        # 归一产物里只有一个网格对象，名字就是目录名
        bpy.ops.wm.append(directory=str(b) + "/Object/", filename=dirname)
        new = [o for o in set(bpy.data.objects) - before if o.type == "MESH"]
        for o in new:
            o.name = f"{tag}_{dirname}"
            o.location = loc
            o.rotation_euler = (0, 0, yaw)
            # **保留 Rodin 的烘焙材质**——它带着盔甲边饰与纹章的暗金。
            # gate_spec §4 把「不是素灰石像、是带金饰的彩石像」列为雕像最重要的一条；
            # 先前 `materials.clear()` 刷成纯冷月白，等于把那条扔了（2026-09-21 实测）。
            if not o.data.materials:
                o.data.materials.append(mat("冷月白"))
            o.parent = root
        return bool(new)
    humanoid(f"{tag}_PH", loc, STATUE_H, "冷月白", root, yaw=yaw)
    return False


def build_statues(root):
    """5 尊挤在北端 30 m 内：南北两对 + 中轴图拉扬。

    网格**自带基座**（15 m 本体 + 4 m 台），所以这里不再另建八角台——
    只补一块侧嵌铭牌（gate_spec §4：铭牌文字本片不需要读清，但**凹槽必须建**，
    它是基座侧面唯一的形体变化）。
    """
    placed = 0
    for idx, dirname, sgn, y in STATUES:
        x = sgn * STATUE_X
        # 东侧那两尊面朝南略偏西、西侧那两尊面朝南略偏东——都转向路心
        yaw = math.radians(-18 if sgn > 0 else 18)
        placed += place_statue(root, f"S{idx}", dirname, (x, y, 0.0), yaw)
        box(f"S{idx}_plaque", (x, y - 3.2, 2.0), (1.6, 0.12, 0.9), "暗金", root)
    ty = (STATUE_Y_S + STATUE_Y_N) / 2 + 14.0        # 中轴最北，贴屏墙前
    placed += place_statue(root, "S5", TURALYON_DIR, (0.0, ty, TURALYON[2]), 0.0)
    box("S5_base", (0, ty, TURALYON[2] / 2), TURALYON, "冷月白", root)
    return placed


def build_screen_and_hall(root):
    """北端：屏墙（中轴墩 + 两侧大圆拱）+ 大阶梯 + 蓝瓦半木大屋 + 远景尖塔群。"""
    box("P_center", (0, SCREEN_Y, SCREEN_Z / 2), (7.0, 5.0, SCREEN_Z), "月白墙石", root)
    line_merlons(root, "P_c", SCREEN_Y, -3.5, 3.5, SCREEN_Z, 5.0)
    for sgn in (-1, +1):
        cx = sgn * (3.5 + ARCH_W / 2)                 # 拱洞中心
        px = sgn * (3.5 + ARCH_W + 6.0)               # 外侧墩中心
        box(f"P_pier_{sgn:+d}", (px, SCREEN_Y, SCREEN_Z / 2), (12.0, 5.0, SCREEN_Z),
            "月白墙石", root)
        line_merlons(root, f"P_{sgn:+d}", SCREEN_Y, px - 6, px + 6, SCREEN_Z, 5.0)
        # 拱洞上方填实（拱洞本身是空的，这是「三拱」的拱）
        box(f"P_lintel_{sgn:+d}", (cx, SCREEN_Y, ARCH_H + (SCREEN_Z - ARCH_H) / 2),
            (ARCH_W, 5.0, SCREEN_Z - ARCH_H), "月白墙石", root)
        line_merlons(root, f"P_a{sgn:+d}", SCREEN_Y, cx - ARCH_W / 2, cx + ARCH_W / 2,
                     SCREEN_Z, 5.0)

    for i in range(10):
        box(f"P_step{i:02d}", (0, SCREEN_Y + 6 + i * 1.4, 0.35 + i * 0.7),
            (26.0, 1.4, 0.7), "月白墙石", root)

    box("H_hall", (0, SCREEN_Y + 36, 9.0), (34.0, 22.0, 18.0), "米白灰泥", root)
    for k in range(5):
        box(f"H_frame{k}", (-15 + k * 7.5, SCREEN_Y + 36 - 11.1, 9.0),
            (0.6, 0.35, 18.0), "深棕木", root)
    cone("H_roof", (0, SCREEN_Y + 36, 18.0 + 6.0), 25.0, 12.0, "宝蓝瓦", root, verts=4)

    # 远景大教堂尖塔群：大气透视下几乎脱色，只要细高成束的轮廓
    for k, (dx, h) in enumerate(((-26, 46), (-10, 58), (8, 52), (24, 40))):
        cyl(f"H_spire{k}", (dx, SCREEN_Y + 100, h / 2), 3.2, h, "月白墙石", root, verts=8)
        cone(f"H_spire{k}_top", (dx, SCREEN_Y + 100, h + 7.0), 4.0, 14.0,
             "宝蓝锥顶", root, verts=8)


def city_tables():
    """从 `build_stormwind.py` **读出**（而不是执行）城区锚点表与运河环。

    为什么不 `import`：那份脚本末尾直接调 `main()`，import 一下会把整座城建出来。
    为什么不抄一份常量进来：抄的那份**一定会漂**（rule 4i ① / CLAUDE.md「一个名字只有一处定义」）
    ——城区位置在两个文件里各写一遍，改了 A 没有任何东西会提醒你改 B，
    而错位只有渲出来才看得见。用 `ast` 取字面量：**单一出处、零执行**。

    坐标口径：`ANCHORS` 是**未缩放**的 build 坐标，原点同为城门正中；
    `build_stormwind.py` 自己在放几何时才乘 `CITY_SCALE`，而 gate_scene 是 1:1，
    所以这里**直接用原值，不要乘任何比例**。
    """
    import ast
    src = (Path(__file__).resolve().parent / "build_stormwind.py").read_text(encoding="utf-8")
    got = {}
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            t = node.targets[0]
            if isinstance(t, ast.Name) and t.id in ("ANCHORS", "CANAL"):
                got[t.id] = ast.literal_eval(node.value)
    missing = {"ANCHORS", "CANAL"} - set(got)
    if missing:
        raise SystemExit(f"build_stormwind.py 里找不到 {missing}——表被改名了？")
    return got["ANCHORS"], got["CANAL"]


# 锚点名 -> (块数, 散布半径 m, 高度区间, 蓝锥顶概率)。**位置不在这里**，位置只在锚点表里。
DISTRICT_BLOCKS = {
    "贸易区南入口":   (26, 95, (11, 26), 0.60),
    "旧城区中心":     (24, 90, (9, 20), 0.50),
    "暴风要塞入口":   (10, 60, (16, 30), 0.70),
    "矮人区水井":     (20, 80, (8, 16), 0.25),    # 矮人区矮而厚，少蓝锥顶
    "割喉小巷":       (8, 45, (8, 15), 0.30),
    "教堂广场入口":   (14, 70, (12, 22), 0.60),
    "花园区中心":     (18, 85, (8, 15), 0.45),
    "法师区水井":     (18, 80, (12, 24), 0.70),
    "监狱入口":       (10, 55, (10, 18), 0.40),
}
# 锚点名 -> (底面 w,d, 主体高, 尖顶高)。三处天际线地标，让拉远的画面认得出是哪座城。
LANDMARKS = [
    ("光明大教堂入口", (46, 70), 46.0, 34.0),
    ("要塞北端", (70, 60), 40.0, 26.0),
    ("巫师圣殿入口", (34, 34), 38.0, 30.0),
]


def convex_hull(pts):
    """单调链凸包，逆时针。给外城墙用——墙只需要一条包住全城的闭合折线。"""
    p = sorted(set(pts))
    if len(p) < 3:
        return p

    def half(seq):
        out = []
        for q in seq:
            while len(out) >= 2:
                (x1, y1), (x2, y2) = out[-2], out[-1]
                if (x2 - x1) * (q[1] - y1) - (y2 - y1) * (q[0] - x1) > 0:
                    break
                out.pop()
            out.append(q)
        return out[:-1]

    return half(p) + half(p[::-1])


def build_distant_city(root):
    """屏墙以北的**远景城市体块**，按真实城区平面布置。

    为什么要有：S02 是「承接 S01 末帧起升后退，八个城区连同运河一圈圈铺开」——
    没有这一层，拉远之后画面里只有草地和天空。
    rule 4g ④「远景＝纯体块」：这里**只给体量、蓝顶分布与运河走向**，不做立面。

    2026-09-21 重写：原先是固定种子的**随机同心环**，渲出来是一片认不出的方块散点
    ——而 S02 这一镜的内容**就是城市平面本身**，平面错了等于这镜没有内容。
    现在城区簇心一律取自 `build_stormwind.py` 的锚点表，运河照它的 `CANAL` 环走。
    """
    import random
    anchors, canal = city_tables()
    rng = random.Random(20260921)     # 固定种子：散布是随机的，簇心不是

    pts = [anchors[k] for k in DISTRICT_BLOCKS if k in anchors]
    xs = [p[0] for p in pts] + [0.0]
    ys = [p[1] for p in pts] + [0.0]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    gw, gd = (max(xs) - min(xs)) + 520, (max(ys) - min(ys)) + 520
    box("D_ground", (cx, cy, -1.4), (gw, gd, 2.0), "黄绿草", root)

    # 运河先铺：锚点环逐段连成水带，后面的房子压在它上面才对
    for i in range(len(canal) - 1):
        a, b = anchors[canal[i]], anchors[canal[i + 1]]
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        seg = math.dist((a[0], a[1]), (b[0], b[1]))
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        box(f"D_canal{i:02d}", (mx, my, -1.0), (seg, 14.0, 2.0), "青蓝水",
            root, rot=ang)

    n = 0
    for name, (cnt, rad, (h0, h1), blue) in DISTRICT_BLOCKS.items():
        ax, ay = anchors[name][0], anchors[name][1]
        for k in range(cnt):
            a = rng.uniform(0, 2 * math.pi)
            r = rad * math.sqrt(rng.random())        # 均匀铺满圆盘，不堆在圆心
            x, y = ax + math.cos(a) * r, ay + math.sin(a) * r
            if y < SCREEN_Y + 28:                    # 别压到英雄谷的精细段上
                continue
            w, d = rng.uniform(16, 32), rng.uniform(16, 32)
            h = rng.uniform(h0, h1)
            box(f"D_{n:03d}", (x, y, h / 2), (w, d, h), "米白灰泥", root,
                rot=rng.uniform(-0.35, 0.35))
            if rng.random() < blue:
                cone(f"D_{n:03d}_sp", (x, y, h + 6.0), max(w, d) * 0.6, 12.0,
                     "宝蓝瓦", root, verts=4)
            n += 1

    # 外城墙：暴风城从空中看最认得出的一条轮廓。取城区锚点的凸包外扩，
    # 不另写一套坐标（同 rule 4i ①）。城门那一段留豁口——精细段已经有真城门了，
    # 再盖一道低墙会把它埋掉。
    hull = convex_hull([(p[0], p[1]) for p in pts])
    hx = sum(p[0] for p in hull) / len(hull)
    hy = sum(p[1] for p in hull) / len(hull)
    for i in range(len(hull)):
        a, b = hull[i], hull[(i + 1) % len(hull)]
        ax, ay = hx + (a[0] - hx) * 1.36, hy + (a[1] - hy) * 1.36
        bx, by = hx + (b[0] - hx) * 1.36, hy + (b[1] - hy) * 1.36
        if ay < SCREEN_Y + 40 and by < SCREEN_Y + 40:
            continue                                  # 南面豁口：让给真城门
        seg = math.dist((ax, ay), (bx, by))
        box(f"D_wall{i:02d}", ((ax + bx) / 2, (ay + by) / 2, 6.0),
            (seg, 5.0, 12.0), "月白墙石", root,
            rot=math.atan2(by - ay, bx - ax))
        cyl(f"D_wtower{i:02d}", (ax, ay, 8.0), 5.0, 16.0, "月白墙石", root, verts=10)
        cone(f"D_wtower{i:02d}_sp", (ax, ay, 16.0 + 3.5), 5.4, 7.0, "宝蓝锥顶",
             root, verts=8)
        n += 2

    for name, (lw, ld), body, spire in LANDMARKS:
        ax, ay = anchors[name][0], anchors[name][1]
        box(f"L_{name}", (ax, ay, body / 2), (lw, ld, body), "月白墙石", root)
        cone(f"L_{name}_sp", (ax, ay, body + spire / 2), max(lw, ld) * 0.5, spire,
             "宝蓝锥顶", root, verts=8)
        n += 1
    return n


def build_lamps(root):
    y, n = 14.0, 0
    while y < SCREEN_Y - 6:
        for sgn in (-1, +1):
            x = sgn * (ROAD_W / 2 + WALK_W * 0.55)
            cyl(f"L{n}_post_{sgn:+d}", (x, y, (LAMP_H - 0.8) / 2), 0.11, LAMP_H - 0.8,
                "深铁灰", root, verts=8)
            box(f"L{n}_base_{sgn:+d}", (x, y, 0.2), (0.6, 0.6, 0.4), "深铁灰", root)
            box(f"L{n}_lantern_{sgn:+d}", (x, y, LAMP_H - 0.55), (0.9, 0.9, 1.1),
                "琥珀金", root)
            cone(f"L{n}_cap_{sgn:+d}", (x, y, LAMP_H + 0.25), 0.62, 0.55, "深铁灰",
                 root, verts=4)
        y += LAMP_GAP
        n += 1
    return n


def setup_world(sc):
    """清晨低角度暖金侧逆光，长影铺在石堤上（shot01 的 `光线:`）。"""
    w = bpy.data.worlds.new("sky")
    w.use_nodes = True
    nt = w.node_tree
    bg = nt.nodes["Background"]
    sky = nt.nodes.new("ShaderNodeTexSky")
    opts = {i.identifier for i in sky.bl_rna.properties["sky_type"].enum_items}
    sky.sky_type = ("MULTIPLE_SCATTERING" if "MULTIPLE_SCATTERING" in opts
                    else ("NISHITA" if "NISHITA" in opts else "HOSEK_WILKIE"))
    for attr, val in (("sun_elevation", math.radians(9.0)),
                      ("sun_rotation", math.radians(240.0)), ("altitude", 200.0)):
        if hasattr(sky, attr):
            setattr(sky, attr, val)
    nt.links.new(sky.outputs[0], bg.inputs[0])
    # 天空只当**补光**：给 1.0 会把对比度冲平，渲出来是「没有投影的平光」——
    # ai_video.md §18 判为「像 CG」的头号特征
    bg.inputs[1].default_value = 0.35
    sc.world = w

    sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
    sun.data.energy = 6.0
    sun.data.angle = math.radians(0.6)
    sun.data.use_shadow = True
    # 阳光阴影走级联，默认只覆盖 200 m 左右；本场景跨 400 m，不拉长远处就没影子
    for attr, val in (("shadow_cascade_max_distance", 600.0),
                      ("shadow_cascade_count", 4), ("shadow_soft_size", 0.8)):
        if hasattr(sun.data, attr):
            setattr(sun.data, attr, val)
    sun.rotation_euler = (math.radians(90 - 9), 0, math.radians(240))
    sc.collection.objects.link(sun)


def setup_render(sc):
    # Blender 5.1 的引擎枚举只有 BLENDER_EEVEE（4.2–4.5 曾叫 BLENDER_EEVEE_NEXT）。
    # 名字猜错会**静默回退 Workbench**：几何照渲，材质与天空全没，看着像「建错了」。
    engines = {i.identifier for i in sc.render.bl_rna.properties["engine"].enum_items}
    for cand in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE", "CYCLES"):
        if cand in engines:
            sc.render.engine = cand
            break
    else:
        raise SystemExit(f"没有可用渲染引擎，只有 {sorted(engines)}")
    ee = getattr(sc, "eevee", None)
    if ee:
        # 只设 5.1 里**实际存在**的属性：`use_gtao` / `taa_render_samples` 已移除，
        # 设了也是静默无效（这类「以为设上了其实没有」最费调试时间）
        for attr, val in (("use_shadows", True), ("use_raytracing", True),
                          ("shadow_ray_count", 4), ("shadow_step_count", 8)):
            if hasattr(ee, attr):
                setattr(ee, attr, val)
    vs = sc.view_settings
    looks = {i.identifier for i in vs.bl_rna.properties["view_transform"].enum_items}
    for cand in ("AgX", "Filmic", "Standard"):
        if cand in looks:
            vs.view_transform = cand
            break
    vs.exposure = -0.2
    print(f"[gate] 渲染引擎 {sc.render.engine} · 影调 {vs.view_transform}")


def render_checks(out_dir: Path):
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y = 1280, 720
    cam_d = bpy.data.cameras.new("chk")
    cam_d.lens, cam_d.clip_end = 28, 4000
    cam = bpy.data.objects.new("chk", cam_d)
    sc.collection.objects.link(cam)
    sc.camera = cam
    tgt = bpy.data.objects.new("chk_t", None)
    sc.collection.objects.link(tgt)
    t = cam.constraints.new("TRACK_TO")
    t.target = tgt
    t.track_axis, t.up_axis = "TRACK_NEGATIVE_Z", "UP_Y"
    shots = [
        ("out_to_gate", (0, -78, 12), (0, 6, 12)),       # 城外望城门
        ("valley_north", (0, 30, 8), (0, 140, 13)),      # 门内顺谷望北端五像
        ("gate_from_in", (0, 66, 16), (0, 0, 14)),       # 谷内回望城门
        ("statues_close", (30, 127, 11), (0, 127, 11)),  # 雕像侧看
    ]
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, loc, look in shots:
        cam.location, tgt.location = loc, look
        sc.render.filepath = str(out_dir / f"check_{name}.png")
        bpy.ops.render.render(write_still=True)
    print(f"[gate] 校验图 {len(shots)} 张 -> {out_dir}")


def main():
    A = argv()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    root = bpy.data.objects.new("GATE_ROOT", None)
    bpy.context.scene.collection.objects.link(root)

    build_terrain(root)
    build_causeway(root)
    build_gate(root)
    n_statue = build_statues(root)
    build_screen_and_hall(root)
    n_city = build_distant_city(root)
    n_lamp = build_lamps(root)
    setup_world(bpy.context.scene)
    setup_render(bpy.context.scene)

    print(f"[gate] 物体 {len(bpy.context.scene.objects)} 个"
          f"（雕像真网格 {n_statue}/5，其余占位；街灯 {n_lamp} 对；远景体块 {n_city} 栋）")
    if "check" in A:
        render_checks(Path(A["check"]))
    if "out" in A:
        p = Path(A["out"])
        p.parent.mkdir(parents=True, exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=str(p))
        print(f"[gate] 已保存 {p}")


main()
