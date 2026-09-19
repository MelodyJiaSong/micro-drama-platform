# -*- coding: utf-8 -*-
"""Render three validation stills of `london.blend`.

`ai_video.md` rule 4h: 出了模型必须先渲一眼再往下做 —— 别拿没看过的几何去做 previz.
These are check renders, not deliverables: flat lighting, fast samples, no look.

Run:
    "<blender>" -b --factory-startup --python tools/check_london.py
"""
from __future__ import annotations

import math
from pathlib import Path

import bpy
from mathutils import Vector

REPO = Path(__file__).resolve().parent.parent
SCENE = REPO / "ai_videos" / "shikong_lvxing" / "sk3" / "2_世界观人设" / "scenes" / "london"
BLEND = SCENE / "_blender" / "london.blend"
OUT = SCENE / "_blender" / "check"

# (名, 相机位置, 看向哪, 焦距) —— 覆盖航拍、桥、布丁巷三档精度
VIEWS = [
    # 航拍：从东南方河面上空回看全城，河、桥、圣保罗必须同时在画里
    ("aerial_southeast", (620, -640, 300), (-180, 80, 30), 32.0),
    # 低空掠河（shot01 的那条路径）
    ("river_low", (520, -150, 22), (-400, -140, 30), 28.0),
    # 圣保罗：航拍最容易画废的一处，单独确认「顶是平的」
    ("st_pauls", (-250, -20, 90), (-430, 150, 40), 50.0),
    # 街面在 z=BANK_Z=3.0，桥面顶在 3.6 —— 视平线 ＝ 面 + 1.6 m。
    # 初版把相机放在 z=1.7，直接埋进地板下面，渲出来是一片灰。
    ("bridge_deck", (-80, -290, 5.2), (-80, -60, 5.2), 35.0),
    # 巷内朝北看（一镜到底的起幅）；巷心 x=61.6
    ("pudding_lane", (61.6, -96, 4.6), (61.6, -46, 6.5), 24.0),
    # 抬头：确认顶部只剩一条缝（jetty 四层累计外挑）
    ("pudding_lane_up", (61.6, -90, 4.6), (61.6, -88, 20.0), 20.0),
]


def look_at(cam, target) -> None:
    d = Vector(target) - cam.location
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def main() -> None:
    bpy.ops.wm.open_mainfile(filepath=str(BLEND))
    sc = bpy.context.scene

    sun = bpy.data.objects.new("check_sun", bpy.data.lights.new("check_sun", "SUN"))
    sun.data.energy = 3.0
    sun.rotation_euler = (math.radians(55), 0, math.radians(35))
    sc.collection.objects.link(sun)
    if sc.world is None:
        sc.world = bpy.data.worlds.new("W")
    sc.world.use_nodes = True
    bg = sc.world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs[0].default_value = (0.55, 0.58, 0.62, 1.0)
        bg.inputs[1].default_value = 1.2

    cam_data = bpy.data.cameras.new("check_cam")
    cam = bpy.data.objects.new("check_cam", cam_data)
    sc.collection.objects.link(cam)
    sc.camera = cam

    sc.render.engine = "BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in [
        i.identifier for i in sc.render.bl_rna.properties["engine"].enum_items
    ] else sc.render.engine
    sc.render.resolution_x, sc.render.resolution_y = 1280, 720
    sc.render.image_settings.file_format = "PNG"
    OUT.mkdir(parents=True, exist_ok=True)

    for name, loc, tgt, lens in VIEWS:
        cam.location = Vector(loc)
        cam_data.lens = lens
        look_at(cam, tgt)
        sc.render.filepath = str(OUT / ("check_%s.png" % name))
        bpy.ops.render.render(write_still=True)
        print("[check] %s" % sc.render.filepath)


if __name__ == "__main__":
    main()
