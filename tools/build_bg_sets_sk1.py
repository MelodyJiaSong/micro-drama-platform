# -*- coding: utf-8 -*-
"""每个 bg 主体一份 3D 体块集 —— `bg{N}_set.blend`（2026-09-21 用户定调）。

**2026-09-25 起不再导出 `_set.glb`**：GLB 只装单个物体（一栋建筑 / 一件器物），多物体的体块集只以 blend 存在。
已出过的 `_set.glb` 不回溯删除（规则变更只对新改的产物生效）。

用户的话：「每一个 scene 的 bg，你应该为它建立 either 一个 3d glb file 或者一个含多于一个
object 的 blender file」。所以本文件的产物契约是硬的：**每个 bg 一份、每份 ≥ 2 个 object**，
不满足直接 raise（闸门从最终产物回读——`bpy.data.objects` 数完再写盘）。

它是什么、不是什么（rule 4g / 4d，别踩回老坑）：
  · **是**「这个地点由哪几块体量组成」的三维速记：地面、墙、屋、树、水、船、塔各是一个 object，
    位置与尺寸来自该主体卡的「锁定描述符 / 空间结构」。给 previz 摆机位、给分镜判遮挡与纵深用。
  · **不是**出图参考。rule 4d ① 白纸黑字：**绝不拿 blockout / 白模 / 灰模渲图当出图参考**，
    那会把画面质量上限锁死在方盒子水平。图仍然由 `bg{N}-1.png` 那条「图先行」的链子出。
  · **不是**几何真相的第二个出处。全城几何仍然只有 `_blender/bianjing.blend`（由
    `tools/build_bianjing.py` 从 W11 + city_plan 生成）；本文件出的是**主体尺度的局部体块集**，
    坐标是主体局部坐标（原点＝该主体的取景中心），不参与全城对位。
  · bg0 / bg16（全城俯瞰本身）不另建：它们的三维就是 `bianjing.blend`，
    落一份 `bg{N}_set.link.json` 指过去（rule 4b-B 的指针写法），不复制 82 MB。

改体块 ＝ 改本文件的 `SETS` 表重跑，不手改 blend（rule 4h ④）。

Run（仓库根目录）：
  blender -b --factory-startup --python tools/build_bg_sets_sk1.py
  blender -b --factory-startup --python tools/build_bg_sets_sk1.py -- --only bg19 bg20
  python tools/build_bg_sets_sk1.py --check          # 不开 Blender，只核对产物是否齐、object 数够不够
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCENES = REPO / "ai_videos" / "shikong_lvxing" / "sk1" / "2_世界观人设" / "scenes" / "bianjing"
CITY_BLEND = SCENES / "_blender" / "bianjing.blend"
MIN_OBJECTS = 2

# ══════════════════════════════════════════════════════════════════════════════
# 体块表：每个 bg 一串 item。`kind` 决定形状，其余是尺寸与位置（米，主体局部坐标）。
#   ground  地坪         (w, d)
#   water   水面         (w, d, z)
#   house   屋           (x, y, w, d, h, roof: gable|hip|flat, yaw)
#   shed    草棚 / 席棚   (x, y, w, d, h, yaw)
#   wall    墙 / 夯土台   (x, y, w, d, h, yaw)
#   tower   塔           (x, y, r, h, tiers)
#   tree    树           (x, y, h)
#   boat    平底船       (x, y, l, w, yaw)
#   bridge  桥           (x, y, l, w, h, yaw)
#   deck    埠头 / 跳板   (x, y, w, d, h, yaw)
#   post    杆 / 桩 / 幡  (x, y, h)
#   block   通用体块     (x, y, w, d, h, yaw)
# ══════════════════════════════════════════════════════════════════════════════
def row(x0: float, y: float, n: int, dx: float, w: float, d: float, h: float,
        roof: str = "gable", yaw: float = 0.0, kind: str = "house") -> list[tuple]:
    """一排房：关厢与河街都是「沿路一层进深」，一排就是一个 item 生成器。"""
    return [(kind, x0 + i * dx, y, w, d, h, roof, yaw) for i in range(n)]


SETS: dict[str, dict] = {
    "bg1_虹桥": {"note": "无柱木拱桥 + 两岸脚店与席棚", "items": [
        ("water", 120.0, 60.0, 0.0),
        ("bridge", 0.0, 0.0, 22.0, 8.0, 5.6, 0.0),
        ("post", -11.0, 5.0, 9.0), ("post", 11.0, 5.0, 9.0),
        *row(-30.0, 22.0, 3, 14.0, 11.0, 7.0, 4.5, "gable"),
        *row(-24.0, -22.0, 2, 14.0, 11.0, 7.0, 4.5, "gable"),
        ("shed", -4.0, 16.0, 6.0, 4.0, 2.6, 0.0),
        ("boat", -34.0, 0.0, 18.0, 4.5, 8.0),
        ("tree", -44.0, 20.0, 8.0), ("tree", 40.0, -20.0, 8.0),
    ]},
    "bg2_东水门城门": {"note": "跨河夯土城台 + 两岸旱门 + 城楼 + 拐子城", "items": [
        ("water", 160.0, 40.0, -2.0),
        ("wall", 0.0, 22.0, 34.0, 16.0, 11.0, 0.0),
        ("wall", 0.0, -22.0, 34.0, 16.0, 11.0, 0.0),
        ("house", 0.0, 22.0, 16.0, 10.0, 6.0, "hip", 0.0),
        ("block", -30.0, 30.0, 60.0, 5.0, 4.0, 0.0),
        ("block", -30.0, -30.0, 60.0, 5.0, 4.0, 0.0),
        ("boat", -40.0, 0.0, 18.0, 4.5, 0.0),
        ("tree", -55.0, 34.0, 8.0), ("tree", 40.0, -34.0, 8.0),
    ]},
    "bg3_汴河码头": {"note": "仓廒长排 + 石岸 + 跳板 + 三条纲船", "items": [
        ("water", 160.0, 50.0, -2.0),
        *row(-60.0, 40.0, 5, 26.0, 22.0, 14.0, 7.5, "gable"),
        ("deck", -30.0, 16.0, 70.0, 6.0, 0.6, 0.0),
        ("boat", -30.0, 6.0, 18.0, 4.5, 0.0), ("boat", 0.0, 6.0, 18.0, 4.5, 0.0),
        ("boat", 30.0, 6.0, 18.0, 4.5, 0.0),
        ("deck", -30.0, 10.0, 6.0, 1.2, 0.4, 20.0),
        ("tree", -70.0, 26.0, 7.0),
    ]},
    "bg4_州桥御街": {"note": "御街 + 朱漆杈子两列 + 两侧廊庑 + 御沟", "items": [
        ("ground", 200.0, 120.0),
        *row(-70.0, 46.0, 6, 24.0, 20.0, 9.0, 5.5, "gable"),
        *row(-70.0, -46.0, 6, 24.0, 20.0, 9.0, 5.5, "gable"),
        ("block", -60.0, 26.0, 1.0, 1.0, 1.6, 0.0), ("block", -20.0, 26.0, 1.0, 1.0, 1.6, 0.0),
        ("block", 20.0, 26.0, 1.0, 1.0, 1.6, 0.0), ("block", -60.0, -26.0, 1.0, 1.0, 1.6, 0.0),
        ("block", -20.0, -26.0, 1.0, 1.0, 1.6, 0.0), ("block", 20.0, -26.0, 1.0, 1.0, 1.6, 0.0),
        ("bridge", 60.0, 0.0, 24.0, 20.0, 1.2, 0.0),
    ]},
    "bg5_正店酒楼": {"note": "三层主楼 + 彩楼欢门 + 邻铺", "items": [
        ("ground", 90.0, 60.0),
        ("house", 0.0, 12.0, 24.0, 16.0, 13.0, "hip", 0.0),
        ("house", -26.0, 10.0, 14.0, 12.0, 7.0, "gable", 0.0),
        ("house", 26.0, 10.0, 14.0, 12.0, 7.0, "gable", 0.0),
        ("block", 0.0, 2.0, 12.0, 1.0, 8.0, 0.0),
        ("post", -6.0, 2.0, 8.5), ("post", 6.0, 2.0, 8.5),
        ("shed", -14.0, 0.0, 6.0, 3.0, 2.6, 0.0),
    ]},
    "bg6_瓦子勾栏": {"note": "大看棚三座 + 栅栏 + 摊", "items": [
        ("ground", 120.0, 90.0),
        ("shed", -22.0, 10.0, 26.0, 20.0, 8.0, 0.0),
        ("shed", 14.0, 16.0, 20.0, 16.0, 7.0, 0.0),
        ("shed", 6.0, -18.0, 18.0, 14.0, 6.5, 0.0),
        ("block", -40.0, -6.0, 1.0, 40.0, 1.8, 0.0),
        ("shed", -34.0, -24.0, 5.0, 3.0, 2.4, 0.0),
        ("tree", 40.0, -30.0, 9.0),
    ]},
    "bg7_坊巷民居": {"note": "两排坊巷 + 井台 + 客店门脸", "items": [
        ("ground", 100.0, 70.0),
        *row(-40.0, 14.0, 5, 18.0, 15.0, 11.0, 5.0, "gable"),
        *row(-40.0, -14.0, 5, 18.0, 15.0, 11.0, 5.0, "gable"),
        ("block", -6.0, 0.0, 2.4, 2.4, 0.8, 0.0),
        ("house", 30.0, 16.0, 18.0, 13.0, 7.5, "hip", 0.0),
        ("tree", 42.0, -18.0, 7.0),
    ]},
    "bg8_郊外清明踏青路": {"note": "黄土大路 + 田埂 + 柳 + 轿", "items": [
        ("ground", 180.0, 120.0),
        ("block", 0.0, 0.0, 180.0, 9.0, 0.15, 0.0),
        ("tree", -60.0, 9.0, 9.0), ("tree", -20.0, 10.0, 9.0),
        ("tree", 20.0, 9.0, 9.0), ("tree", 60.0, 10.0, 9.0),
        ("block", -10.0, -2.0, 2.2, 1.6, 2.0, 0.0),
        ("house", 55.0, -34.0, 12.0, 9.0, 4.2, "gable", 0.0),
    ]},
    "bg9_今日州桥遗址": {"note": "当代考古坑 + 探方 + 现代楼体块", "items": [
        ("ground", 120.0, 90.0),
        ("block", 0.0, 0.0, 40.0, 26.0, -6.0, 0.0),
        ("block", -8.0, 0.0, 14.0, 8.0, 0.8, 0.0),
        ("block", 10.0, 4.0, 10.0, 6.0, 0.5, 0.0),
        ("house", -46.0, 34.0, 26.0, 18.0, 22.0, "flat", 0.0),
        ("house", 42.0, 36.0, 22.0, 16.0, 18.0, "flat", 0.0),
    ]},
    "bg10_赵太丞家": {"note": "三进医铺门面 + 立招 + 街", "items": [
        ("ground", 70.0, 50.0),
        ("house", 0.0, 10.0, 16.0, 12.0, 7.0, "gable", 0.0),
        ("house", 0.0, 26.0, 16.0, 12.0, 6.0, "gable", 0.0),
        ("house", 0.0, 40.0, 16.0, 12.0, 6.0, "gable", 0.0),
        ("post", -6.0, 2.5, 4.2), ("post", 6.0, 2.5, 4.2),
        ("shed", 0.0, 3.0, 12.0, 2.5, 3.0, 0.0),
    ]},
    "bg11_开封府": {"note": "府门 + 两侧廊房 + 正厅 + 月台", "items": [
        ("ground", 140.0, 120.0),
        ("house", 0.0, -30.0, 22.0, 12.0, 9.0, "hip", 0.0),
        ("block", -30.0, -30.0, 38.0, 6.0, 5.0, 0.0),
        ("block", 30.0, -30.0, 38.0, 6.0, 5.0, 0.0),
        ("block", 0.0, 10.0, 34.0, 20.0, 1.2, 0.0),
        ("house", 0.0, 10.0, 30.0, 16.0, 12.0, "hip", 0.0),
        ("house", -32.0, 6.0, 10.0, 24.0, 6.0, "gable", 0.0),
        ("house", 32.0, 6.0, 10.0, 24.0, 6.0, "gable", 0.0),
    ]},
    "bg12_宣德楼": {"note": "五门洞墩台 + 朵楼 + 阙亭 + 殿庭", "items": [
        ("ground", 220.0, 160.0),
        ("wall", 0.0, 0.0, 90.0, 20.0, 14.0, 0.0),
        ("house", 0.0, 0.0, 46.0, 14.0, 12.0, "hip", 0.0),
        ("house", -34.0, 0.0, 14.0, 12.0, 8.0, "hip", 0.0),
        ("house", 34.0, 0.0, 14.0, 12.0, 8.0, "hip", 0.0),
        ("block", -52.0, -26.0, 10.0, 10.0, 10.0, 0.0),
        ("block", 52.0, -26.0, 10.0, 10.0, 10.0, 0.0),
        ("block", 0.0, 46.0, 60.0, 34.0, 2.0, 0.0),
        ("house", 0.0, 50.0, 46.0, 24.0, 16.0, "hip", 0.0),
    ]},
    "bg13_相国寺": {"note": "寺门 + 大殿 + 两廊 + 书市摊", "items": [
        ("ground", 180.0, 140.0),
        ("house", 0.0, -40.0, 26.0, 12.0, 10.0, "hip", 0.0),
        ("house", 0.0, 20.0, 40.0, 26.0, 18.0, "hip", 0.0),
        ("block", -40.0, -10.0, 8.0, 60.0, 5.0, 0.0),
        ("block", 40.0, -10.0, 8.0, 60.0, 5.0, 0.0),
        ("shed", -20.0, -26.0, 6.0, 3.0, 2.4, 0.0),
        ("shed", -8.0, -26.0, 6.0, 3.0, 2.4, 0.0),
        ("shed", 6.0, -26.0, 6.0, 3.0, 2.4, 0.0),
        ("tree", -48.0, -34.0, 11.0), ("tree", 48.0, -34.0, 11.0),
    ]},
    "bg14_客店房间夜": {"note": "内景：四壁 + 床榻 + 桌凳 + 直棂窗 + 油灯", "items": [
        ("ground", 5.0, 4.2),
        ("block", 0.0, 2.1, 5.0, 0.2, 2.8, 0.0),
        ("block", 0.0, -2.1, 5.0, 0.2, 2.8, 0.0),
        ("block", -2.5, 0.0, 0.2, 4.2, 2.8, 0.0),
        ("block", 2.5, 0.0, 0.2, 4.2, 2.8, 0.0),
        ("block", -1.4, 1.2, 1.9, 0.9, 0.5, 0.0),
        ("block", 1.4, -1.0, 1.1, 0.7, 0.75, 0.0),
        ("block", 0.9, -1.6, 0.4, 0.4, 0.45, 0.0),
        ("post", 1.5, -1.0, 0.22),
    ]},
    "bg15_园林雅集": {"note": "池 + 廊 + 亭 + 柳 + 栏杆", "items": [
        ("ground", 120.0, 90.0),
        ("water", 60.0, 40.0, -0.4),
        ("house", -34.0, 16.0, 10.0, 10.0, 5.0, "hip", 0.0),
        ("block", -10.0, 24.0, 40.0, 4.0, 3.2, 0.0),
        ("block", 0.0, -22.0, 40.0, 0.6, 0.9, 0.0),
        ("tree", -40.0, -10.0, 10.0), ("tree", 34.0, 12.0, 10.0),
        ("tree", 10.0, 28.0, 9.0),
    ]},
    "bg17_州桥夜市": {"note": "低平石桥 + 两侧摊位 + 街", "items": [
        ("ground", 140.0, 80.0),
        ("bridge", 0.0, 0.0, 26.0, 20.0, 1.2, 0.0),
        ("water", 140.0, 12.0, -1.8),
        *row(-46.0, 18.0, 5, 14.0, 5.0, 3.0, 2.4, "flat", 0.0, "shed"),
        *row(-46.0, -18.0, 5, 14.0, 5.0, 3.0, 2.4, "flat", 0.0, "shed"),
        ("house", 40.0, 26.0, 16.0, 12.0, 7.0, "gable", 0.0),
    ]},
    # ── 本轮新建的五个主体（follow-up 028）────────────────────────────────────
    "bg18_繁塔": {"note": "九层砖塔 + 寺院院落 + 老树 + 屋海", "items": [
        ("ground", 200.0, 160.0),
        ("tower", 0.0, 0.0, 9.0, 76.0, 9),
        ("block", 0.0, 0.0, 26.0, 26.0, 1.2, 0.0),
        ("block", -30.0, 0.0, 1.0, 70.0, 2.4, 0.0),
        ("block", 30.0, 0.0, 1.0, 70.0, 2.4, 0.0),
        ("house", 0.0, 26.0, 20.0, 12.0, 8.0, "hip", 0.0),
        ("house", -18.0, -22.0, 14.0, 9.0, 5.5, "gable", 0.0),
        ("tree", -24.0, 14.0, 14.0), ("tree", 24.0, -14.0, 13.0),
        *row(-80.0, 62.0, 5, 30.0, 12.0, 8.0, 4.5, "gable"),
        *row(-80.0, -62.0, 5, 30.0, 12.0, 8.0, 4.5, "gable"),
    ]},
    "bg19_东水门外关厢": {"note": "河岸土路 + 两排关厢屋舍 + 草棚 + 白墙朱门 + 柳 + 护龙河", "items": [
        ("ground", 300.0, 160.0),
        ("water", 300.0, 26.0, -2.5),
        ("block", 0.0, 22.0, 300.0, 9.0, 0.15, 0.0),
        *row(-120.0, 36.0, 7, 26.0, 13.0, 8.0, 4.6, "gable"),
        *row(-108.0, 54.0, 5, 30.0, 11.0, 7.0, 4.2, "gable"),
        ("shed", -66.0, 36.0, 7.0, 5.0, 3.0, 0.0),
        ("shed", 18.0, 36.0, 7.0, 5.0, 3.0, 0.0),
        ("shed", 74.0, 54.0, 8.0, 6.0, 3.2, 0.0),
        ("block", -150.0, 30.0, 4.0, 60.0, 2.2, 0.0),
        ("tree", -96.0, 14.0, 9.0), ("tree", -40.0, 14.0, 9.0),
        ("tree", 22.0, 14.0, 9.0), ("tree", 86.0, 14.0, 9.0),
        ("tree", -150.0, 44.0, 8.0),
        ("boat", 60.0, -4.0, 14.0, 4.0, 4.0),
    ]},
    "bg20_城内汴河河街": {"note": "两岸连续铺面 + 席棚 + 小埠头 + 纲船 + 柳", "items": [
        ("ground", 300.0, 180.0),
        ("water", 300.0, 30.0, -2.0),
        *row(-120.0, 30.0, 9, 22.0, 17.0, 11.0, 5.2, "gable"),
        *row(-114.0, -32.0, 8, 24.0, 16.0, 10.0, 4.8, "gable"),
        ("house", 40.0, 30.0, 17.0, 11.0, 8.6, "gable", 0.0),
        ("shed", -54.0, 21.0, 9.0, 4.0, 3.2, 0.0),
        ("shed", 18.0, 21.0, 9.0, 4.0, 3.2, 0.0),
        ("post", -8.0, 20.0, 6.5), ("post", 4.0, 20.0, 6.5),
        ("deck", -30.0, 14.0, 8.0, 6.0, 1.0, 0.0),
        ("boat", -30.0, 4.0, 18.0, 4.5, 4.0), ("boat", 26.0, 2.0, 18.0, 4.5, 3.0),
        ("tree", -80.0, 17.0, 8.0), ("tree", 62.0, 17.0, 8.0),
    ]},
    "bg21_迎祥池": {"note": "开阔池 + 夹岸垂杨 + 平桥 + 拱桥 + 亭 + 水榭", "items": [
        ("ground", 260.0, 200.0),
        ("water", 180.0, 140.0, -0.5),
        ("bridge", -20.0, 0.0, 60.0, 2.4, 0.4, 90.0),
        ("bridge", 40.0, 34.0, 22.0, 3.0, 3.2, 0.0),
        ("house", 78.0, 10.0, 6.0, 6.0, 4.4, "hip", 0.0),
        ("house", 70.0, -40.0, 9.0, 7.0, 4.0, "hip", 0.0),
        ("deck", 70.0, -33.0, 9.0, 4.0, 0.5, 0.0),
        *[("tree", -95.0 + i * 38.0, 78.0, 9.0) for i in range(6)],
        *[("tree", -95.0 + i * 38.0, -78.0, 9.0) for i in range(6)],
        ("boat", -60.0, -50.0, 9.0, 2.4, 15.0),
    ]},
    "bg22_里城东墙门": {"note": "里城夯土墙 + 旧宋门城台城楼 + 角门子 + 河缺口 + 纲船", "items": [
        ("ground", 300.0, 200.0),
        ("water", 60.0, 300.0, -2.5),
        ("wall", 0.0, 60.0, 16.0, 120.0, 9.0, 0.0),
        ("wall", 0.0, -60.0, 16.0, 120.0, 9.0, 0.0),
        ("wall", 0.0, 120.0, 26.0, 22.0, 11.0, 0.0),
        ("house", 0.0, 120.0, 14.0, 10.0, 6.0, "hip", 0.0),
        ("block", 14.0, 112.0, 14.0, 5.0, 5.0, 0.0),
        ("wall", 0.0, -118.0, 20.0, 16.0, 8.0, 0.0),
        ("house", 0.0, -118.0, 8.0, 6.0, 3.4, "gable", 0.0),
        ("boat", -6.0, 10.0, 18.0, 4.5, 80.0),
        ("tree", -28.0, 96.0, 8.0), ("tree", -28.0, -96.0, 8.0),
        ("block", -40.0, 0.0, 6.0, 260.0, 0.15, 0.0),
    ]},
}

# 全城俯瞰本身：三维就是 bianjing.blend，落指针不复制（rule 4b-B）
LINKED = {
    "bg0_汴京全城": "本主体就是全城俯瞰，它的三维 ＝ `_blender/bianjing.blend`（`tools/build_bianjing.py` 生成）。"
                    "复制一份 82 MB 的副本只会漂（rule 4i ①），所以这里只落指针。",
    "bg16_汴京全城五更": "同 bg0：全城俯瞰的五更态，几何不变、只有光变，三维仍是 `_blender/bianjing.blend`。",
}


# ══════════════════════════════════════════════════════════════════════════════
# Blender 侧
# ══════════════════════════════════════════════════════════════════════════════
def build() -> None:
    import bpy
    from mathutils import Vector  # noqa: F401

    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    only = set(argv[argv.index("--only") + 1:]) if "--only" in argv else set()

    def clear() -> None:
        bpy.ops.wm.read_factory_settings(use_empty=True)

    def mesh(name: str, verts: list, faces: list) -> "bpy.types.Object":
        me = bpy.data.meshes.new(name)
        me.from_pydata(verts, [], faces)
        me.update()
        ob = bpy.data.objects.new(name, me)
        bpy.context.scene.collection.objects.link(ob)
        return ob

    def box(name: str, cx: float, cy: float, w: float, d: float, z0: float, z1: float,
            yaw: float = 0.0) -> "bpy.types.Object":
        hw, hd = w / 2, d / 2
        a = math.radians(yaw)
        ca, sa = math.cos(a), math.sin(a)
        pts = [(-hw, -hd), (hw, -hd), (hw, hd), (-hw, hd)]
        pts = [(cx + px * ca - py * sa, cy + px * sa + py * ca) for px, py in pts]
        verts = [(x, y, z0) for x, y in pts] + [(x, y, z1) for x, y in pts]
        faces = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
        return mesh(name, verts, faces)

    def roofed(name: str, cx: float, cy: float, w: float, d: float, h: float,
               roof: str, yaw: float) -> list:
        """墙身 + 屋面 ＝ 两个 object：屋顶单独成件，previz 判遮挡时最要紧的就是它。"""
        wall_h = h * 0.62 if roof != "flat" else h
        out = [box(f"{name}_wall", cx, cy, w, d, 0.0, wall_h, yaw)]
        if roof == "flat":
            return out
        a = math.radians(yaw)
        ca, sa = math.cos(a), math.sin(a)
        hw, hd = w / 2 * 1.12, d / 2 * 1.12          # 出檐
        def P(px, py, pz):
            return (cx + px * ca - py * sa, cy + px * sa + py * ca, pz)
        if roof == "gable":
            verts = [P(-hw, -hd, wall_h), P(hw, -hd, wall_h), P(hw, hd, wall_h), P(-hw, hd, wall_h),
                     P(-hw, 0.0, h), P(hw, 0.0, h)]
            faces = [(0, 1, 5, 4), (3, 2, 5, 4), (0, 4, 3), (1, 2, 5), (0, 1, 2, 3)]
        else:                                        # hip
            verts = [P(-hw, -hd, wall_h), P(hw, -hd, wall_h), P(hw, hd, wall_h), P(-hw, hd, wall_h),
                     P(-hw * 0.35, 0.0, h), P(hw * 0.35, 0.0, h)]
            faces = [(0, 1, 5, 4), (3, 2, 5, 4), (0, 4, 3), (1, 2, 5), (0, 1, 2, 3)]
        out.append(mesh(f"{name}_roof", verts, faces))
        return out

    def cyl(name: str, cx: float, cy: float, r: float, z0: float, z1: float, seg: int = 12):
        verts = ([(cx + r * math.cos(2 * math.pi * i / seg), cy + r * math.sin(2 * math.pi * i / seg), z0)
                  for i in range(seg)]
                 + [(cx + r * math.cos(2 * math.pi * i / seg), cy + r * math.sin(2 * math.pi * i / seg), z1)
                    for i in range(seg)])
        faces = [(i, (i + 1) % seg, seg + (i + 1) % seg, seg + i) for i in range(seg)]
        faces += [tuple(range(seg - 1, -1, -1)), tuple(range(seg, 2 * seg))]
        return mesh(name, verts, faces)

    def ball(name: str, cx: float, cy: float, cz: float, r: float):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=(cx, cy, cz), segments=12, ring_count=8)
        ob = bpy.context.active_object
        ob.name = name
        ob.data.name = name          # glTF 导出用的是 mesh 名，只改 object 名会在 glb 里留下 Sphere.001
        return ob

    def emit(key: str, items: list) -> int:
        n = 0
        for i, it in enumerate(items):
            kind = it[0]
            tag = f"{key.split('_')[0]}_{kind}{i:02d}"
            if kind == "ground":
                box(tag, 0.0, 0.0, it[1], it[2], -0.2, 0.0)
            elif kind == "water":
                box(tag, 0.0, 0.0, it[1], it[2], it[3] - 0.3, it[3])
            elif kind in ("house",):
                roofed(tag, it[1], it[2], it[3], it[4], it[5], it[6], it[7])
                n += 1
            elif kind == "shed":
                box(tag, it[1], it[2], it[3], it[4], it[5] - 0.25, it[5])
                for s in (-1, 1):
                    cyl(f"{tag}_post{s}", it[1] + s * it[3] / 2 * 0.9, it[2], 0.09, 0.0, it[5])
                n += 2
            elif kind in ("wall", "block"):
                box(tag, it[1], it[2], it[3], it[4], 0.0, it[5], it[6] if len(it) > 6 else 0.0)
            elif kind == "tower":
                for t in range(it[5]):
                    z0 = it[4] * t / it[5]
                    r = it[3] * (1.0 - 0.45 * t / it[5])
                    cyl(f"{tag}_tier{t}", it[1], it[2], r, z0, z0 + it[4] / it[5] * 0.86, 6)
                    cyl(f"{tag}_eave{t}", it[1], it[2], r * 1.22, z0 + it[4] / it[5] * 0.86,
                        z0 + it[4] / it[5], 6)
                cyl(f"{tag}_finial", it[1], it[2], it[3] * 0.12, it[4], it[4] + it[4] * 0.08, 6)
                n += it[5] * 2
            elif kind == "tree":
                cyl(f"{tag}_trunk", it[1], it[2], max(0.12, it[3] * 0.045), 0.0, it[3] * 0.55)
                ball(f"{tag}_crown", it[1], it[2], it[3] * 0.78, it[3] * 0.34)
                n += 1
            elif kind == "boat":
                box(tag, it[1], it[2], it[3], it[4], -0.6, 0.7, it[5])
                box(f"{tag}_cabin", it[1], it[2], it[3] * 0.4, it[4] * 0.8, 0.7, 2.1, it[5])
                n += 1
            elif kind == "bridge":
                box(tag, it[1], it[2], it[3], it[4], it[5] - 0.5, it[5], it[6] if len(it) > 6 else 0.0)
            elif kind == "deck":
                box(tag, it[1], it[2], it[3], it[4], 0.0, it[5], it[6] if len(it) > 6 else 0.0)
            elif kind == "post":
                cyl(tag, it[1], it[2], 0.11, 0.0, it[3])
            else:
                raise SystemExit(f"{key}：不认识的体块类型 {kind}")
            n += 1
        return n

    made = []
    for key, spec in SETS.items():
        stem = key.split("_")[0]
        if only and stem not in only and key not in only:
            continue
        folder = SCENES / key
        if not folder.is_dir():
            raise SystemExit(f"{folder} 不存在——体块表里的 bg 必须有主体卡目录")
        clear()
        emit(key, spec["items"])
        obs = [o for o in bpy.data.objects if o.type == "MESH"]
        if len(obs) < MIN_OBJECTS:
            raise SystemExit(f"{key}：只生成了 {len(obs)} 个 object，契约要求 ≥ {MIN_OBJECTS}")
        blend = folder / f"{stem}_set.blend"
        bpy.ops.wm.save_as_mainfile(filepath=str(blend))
        print(f"✅ {key}：{len(obs)} objects → {blend.name}")
        made.append((key, len(obs)))

    for key, why in LINKED.items():
        folder = SCENES / key
        if only and key.split("_")[0] not in only and key not in only:
            continue
        if not folder.is_dir():
            continue
        (folder / f"{key.split('_')[0]}_set.link.json").write_text(
            json.dumps({"target": "../_blender/bianjing.blend", "note": why},
                       ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"✅ {key}：指针 → _blender/bianjing.blend")
    print(f"共 {len(made)} 份体块集，{len(LINKED)} 份指针")


def check() -> int:
    """不开 Blender 的产物核对：每个 bg 目录要么有 `_set.blend`，要么有 `_set.link.json`。"""
    bad = []
    for folder in sorted(SCENES.glob("bg*_*")):
        if not folder.is_dir():
            continue
        stem = folder.name.split("_")[0]
        has_set = (folder / f"{stem}_set.blend").is_file()
        has_link = (folder / f"{stem}_set.link.json").is_file()
        mark = "✅" if (has_set or has_link) else "❌"
        if not (has_set or has_link):
            bad.append(folder.name)
        kb = ((folder / f"{stem}_set.blend").stat().st_size // 1024) if has_set else 0
        print(f"{mark} {folder.name}" + (f"  blend {kb} KB" if has_set else ("  → 指针" if has_link else "  缺 3D")))
    if bad:
        print(f"\n缺 3D 的 bg（{len(bad)}）：{'、'.join(bad)}")
        return 1
    print("\n每个 bg 都有 3D（blend 或指针）")
    return 0


if __name__ == "__main__":
    if "--check" in sys.argv and "bpy" not in sys.modules:
        try:
            import bpy  # noqa: F401
        except ModuleNotFoundError:
            sys.stdout.reconfigure(encoding="utf-8")
            raise SystemExit(check())
    build()
