# -*- coding: utf-8 -*-
"""Look pass for bianjing.blend (sk1 北宋汴京): turns the grey layout city into a renderable, realistic city.

The layout builder `tools/build_bianjing.py` stays the only source of *where* things are. This pass only adds
*what they look like*, deterministically, on top of that layout (sk1 divergence #19):

  · materials   — colours sampled from the scene anchor images (`scenes/bianjing/bg*/bg*-1.png`), surface detail from
                  CC0 Poly Haven PBR maps (`_blender/textures/polyhaven/`, fetched by `tools/polyhaven_fetch.py`),
                  box-projected onto the layout meshes (no UVs needed); a rammed-earth layering patch is cut from bg2-1
  · houses      — every unit box in G_BLOCKS / G_SUBURBS becomes an instance of a procedural Song vernacular house
                  (curved tile or thatch roof, posts, lattice windows, shopfronts); place protos p9 / p10 / p10a and the
                  虹桥 p8 get detailed meshes of the same bounding box
  · trees       — icosphere trees become instanced willows
  · world       — physical sky, low sun from the east (卯时), Cycles render settings, a still camera

Layout meshes that were replaced are kept (hide_render) so QC, previz ground probes and the geometry digest see the same
layout as before. Everything this pass creates carries the custom property `look=1`; `undress()` removes all of it.

Run (repo root):
  blender -b <bianjing.blend> --python tools/look_bianjing.py -- --save
  blender -b <bianjing.blend> --python tools/look_bianjing.py -- --stills all [--samples 96]   # needs a dressed blend
"""
from __future__ import annotations

import argparse
import math
import random
import sys
from dataclasses import dataclass
from pathlib import Path

import bmesh
import bpy
import numpy as np
from mathutils import Matrix, Vector
from mathutils.geometry import convex_hull_2d

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_bianjing as bj  # noqa: E402

TEX = bj.BLENDER_DIR / "textures"
PH = TEX / "polyhaven"
SCENES = bj.BLENDER_DIR.parent
Z = bj.Z_STREET

# ── palette: (image, rect as fractions x0,y0,x1,y1 from top-left, target albedo luminance, saturation kept) ─────────
# The anchors are lit at sunrise, so sampled hue carries warm light; saturation is scaled back to get an albedo.
PALETTE_SRC: dict[str, tuple[str, tuple[float, float, float, float], float, float]] = {
    "roof":    ("bg7_坊巷民居/bg7-1.png",   (0.010, 0.270, 0.165, 0.420), 0.09, 0.4),
    "glazed":  ("bg12_宣德楼/bg12-1.png",  (0.440, 0.222, 0.675, 0.293), 0.06, 1.0),
    "plaster": ("bg7_坊巷民居/bg7-1.png",   (0.940, 0.738, 0.995, 0.853), 0.52, 0.35),
    "rammed":  ("bg2_东水门城门/bg2-1.png", (0.550, 0.418, 0.620, 0.711), 0.28, 0.8),
    "earth":   ("bg7_坊巷民居/bg7-1.png",   (0.350, 0.800, 0.500, 0.933), 0.20, 0.9),
    "water":   ("bg1_虹桥/bg1-1.png",      (0.520, 0.820, 0.660, 0.900), 0.07, 1.9),
    "leaf":    ("bg2_东水门城门/bg2-1.png", (0.010, 0.498, 0.080, 0.622), 0.16, 1.0),
    "red":     ("bg1_虹桥/bg1-1.png",      (0.650, 0.293, 0.750, 0.338), 0.09, 1.2),
    "timber":  ("bg2_东水门城门/bg2-1.png", (0.300, 0.240, 0.525, 0.284), 0.11, 0.6),
    "brick":   ("bg12_宣德楼/bg12-1.png",  (0.260, 0.551, 0.450, 0.622), 0.12, 0.4),
    "stone":   ("bg4_州桥御街/bg4-1.png",   (0.300, 0.560, 0.700, 0.620), 0.26, 0.5),
    "field":   ("bg0_汴京全城/bg0-1.png",   (0.900, 0.550, 0.990, 0.700), 0.15, 2.2),
}
RAMMED_PATCH = ("bg2_东水门城门/bg2-1.png", (0.550, 0.418, 0.620, 0.711))

MAT_NAMES = ("EARTH", "GROUND", "WATER", "RIVERBED", "RAMMED", "PLASTER", "TIMBER", "RED", "BLACK", "ROOF", "ROOF_UV",
             "GLAZED", "BRICK", "STONE", "REED", "WINDOW", "GILT", "LEAF", "BARK", "CLOTH_RED", "CLOTH_BLUE", "INVISIBLE",
             "FIELD", "CLOTH_UNDYED", "SKIN", "BLOSSOM")
M = {n: i for i, n in enumerate(MAT_NAMES)}


def tag(idb) -> None:
    idb["look"] = 1


# ── images and palette ────────────────────────────────────────────────────────────────────────────────────────────
def srgb_to_linear(c: np.ndarray) -> np.ndarray:
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def load_pixels(path: Path) -> tuple[bpy.types.Image, np.ndarray]:
    if not path.is_file():
        raise bj.PlanError(f"look: missing image {path}")
    img = bpy.data.images.load(str(path), check_existing=True)
    w, h = img.size
    px = np.empty(w * h * 4, dtype=np.float32)
    img.pixels.foreach_get(px)
    return img, px.reshape(h, w, 4)


def crop(px: np.ndarray, rect: tuple[float, float, float, float]) -> np.ndarray:
    h, w = px.shape[:2]
    x0, y0, x1, y1 = rect
    return px[int(h * (1 - y1)):int(h * (1 - y0)), int(w * x0):int(w * x1), :3]


def luminance(rgb: np.ndarray) -> np.ndarray:
    return rgb[..., 0] * 0.2126 + rgb[..., 1] * 0.7152 + rgb[..., 2] * 0.0722


def sample_palette() -> dict[str, tuple[float, float, float]]:
    out = {}
    for key, (rel, rect, albedo, sat) in PALETTE_SRC.items():
        img, px = load_pixels(SCENES / rel)
        lin = srgb_to_linear(crop(px, rect).reshape(-1, 3)).mean(axis=0)
        grey = float(luminance(lin))
        lin = grey + (lin - grey) * sat
        lin = np.clip(lin, 1e-4, None) * (albedo / max(1e-4, float(luminance(lin))))
        out[key] = tuple(float(min(1.0, v)) for v in lin)
    return out


def rammed_patch() -> bpy.types.Image:
    """夯层 patch from bg2-1: mirror-tiled in X, cross-faded in Y, luminance-normalised, packed into the blend."""
    rel, rect = RAMMED_PATCH
    _img, px = load_pixels(SCENES / rel)
    c = srgb_to_linear(crop(px, rect))
    c = np.concatenate([c, c[:, ::-1]], axis=1)
    h = c.shape[0]
    k = max(2, h // 6)
    ramp = np.linspace(0.0, 1.0, k)[:, None, None]
    c[:k] = c[:k] * ramp + c[h - k:] * (1 - ramp)
    c = c[:h - k]
    lum = luminance(c)
    c = np.repeat((lum / max(1e-4, float(lum.mean())))[..., None], 3, axis=2) * 0.5
    hh, ww = c.shape[:2]
    rgba = np.concatenate([np.clip(c, 0, 1), np.ones((hh, ww, 1), np.float32)], axis=2)[::-1]
    img = bpy.data.images.new("LOOK_rammed_layers", ww, hh, float_buffer=True)
    img.colorspace_settings.name = "Non-Color"
    img.pixels.foreach_set(rgba.astype(np.float32).ravel())
    img.pack()
    tag(img)
    return img


# ── node helpers ──────────────────────────────────────────────────────────────────────────────────────────────────
class NT:
    def __init__(self, mat: bpy.types.Material) -> None:
        mat.use_nodes = True
        self.t = mat.node_tree
        self.t.nodes.clear()
        self.x = 0

    def n(self, idname: str, **props):
        nd = self.t.nodes.new(idname)
        nd.location = (self.x, 0)
        self.x += 10
        for k, v in props.items():
            setattr(nd, k, v)
        return nd

    def link(self, a, b) -> None:
        self.t.links.new(a, b)

    def math(self, op: str, a, b=None):
        nd = self.n("ShaderNodeMath", operation=op)
        for i, v in enumerate((a, b)):
            if v is None:
                continue
            if isinstance(v, (int, float)):
                nd.inputs[i].default_value = float(v)
            else:
                self.link(v, nd.inputs[i])
        return nd.outputs[0]

    def mix(self, fac, a, b, blend: str = "MIX"):
        nd = self.n("ShaderNodeMix", data_type="RGBA", blend_type=blend)
        for sock, v in ((nd.inputs[0], fac), (nd.inputs[6], a), (nd.inputs[7], b)):
            if isinstance(v, (int, float)):
                sock.default_value = float(v)
            elif isinstance(v, tuple):
                sock.default_value = (*v[:3], 1.0)
            else:
                self.link(v, sock)
        return nd.outputs[2]

    def tex(self, image: bpy.types.Image, vector, box: bool = True, non_color: bool = False):
        nd = self.n("ShaderNodeTexImage", image=image, interpolation="Linear")
        if box:
            nd.projection, nd.projection_blend = "BOX", 0.25
        if non_color:
            image.colorspace_settings.name = "Non-Color"
        self.link(vector, nd.inputs["Vector"])
        return nd

    def coords(self, scale_m: float, uv: bool = False):
        if uv:
            src = self.n("ShaderNodeUVMap", uv_map="UVMap").outputs["UV"]
        else:
            src = self.n("ShaderNodeTexCoord").outputs["Object"]
        mp = self.n("ShaderNodeMapping")
        mp.inputs["Scale"].default_value = (1 / scale_m, 1 / scale_m, 1 / scale_m)
        self.link(src, mp.inputs["Vector"])
        return mp.outputs["Vector"]

    def noise(self, vector, scale: float, detail: float = 3.0):
        nd = self.n("ShaderNodeTexNoise", noise_dimensions="3D")
        nd.inputs["Scale"].default_value = scale
        nd.inputs["Detail"].default_value = detail
        if vector is not None:
            self.link(vector, nd.inputs["Vector"])
        return nd.outputs["Fac"]


@dataclass(frozen=True)
class PBR:
    diff: bpy.types.Image
    rough: bpy.types.Image
    mean_luma: float


PBR_CACHE: dict[str, PBR] = {}


def pbr_maps(asset: str) -> PBR:
    if asset not in PBR_CACHE:
        d, px = load_pixels(PH / asset / f"{asset}_diff_2k.jpg")
        r, _ = load_pixels(PH / asset / f"{asset}_rough_2k.jpg")
        r.colorspace_settings.name = "Non-Color"
        mean = float(luminance(srgb_to_linear(px[::8, ::8, :3])).mean())
        for im in (d, r):
            im.pack()
            tag(im)
        PBR_CACHE[asset] = PBR(d, r, mean)
    return PBR_CACHE[asset]


def pbr_material(name: str, asset: str, tint: tuple[float, float, float], scale_m: float, *, uv: bool = False,
                 bump: float = 0.35, rough_add: float = 0.0, var: float = 0.22, keep_hue: float = 0.15,
                 macro_m: float = 30.0, overlay=None, metallic: float = 0.0) -> bpy.types.Material:
    mat = bpy.data.materials.new(f"LOOK_{name}")
    tag(mat)
    nt = NT(mat)
    maps = pbr_maps(asset)
    vec = nt.coords(scale_m, uv=uv)
    diff = nt.tex(maps.diff, vec, box=not uv)
    rough = nt.tex(maps.rough, vec, box=not uv, non_color=True)
    bw = nt.n("ShaderNodeRGBToBW")
    nt.link(diff.outputs["Color"], bw.inputs["Color"])
    detail = nt.math("DIVIDE", bw.outputs["Val"], max(1e-3, maps.mean_luma))
    col = nt.mix(keep_hue, nt.mix(1.0, tint, detail, "MULTIPLY"), diff.outputs["Color"], "MIX")
    if overlay is not None:
        col = nt.mix(0.55, col, overlay(nt), "MULTIPLY")
    info = nt.n("ShaderNodeObjectInfo")
    macro = nt.noise(nt.coords(macro_m), 1.0, 2.0)
    v = nt.math("ADD", nt.math("MULTIPLY", nt.math("SUBTRACT", info.outputs["Random"], 0.5), var),
                nt.math("MULTIPLY", nt.math("SUBTRACT", macro, 0.5), var))
    hsv = nt.n("ShaderNodeHueSaturation")
    nt.link(col, hsv.inputs["Color"])
    nt.link(nt.math("ADD", v, 1.0), hsv.inputs["Value"])
    bsdf = nt.n("ShaderNodeBsdfPrincipled")
    nt.link(hsv.outputs["Color"], bsdf.inputs["Base Color"])
    nt.link(nt.math("ADD", rough.outputs["Color"], rough_add), bsdf.inputs["Roughness"])
    bsdf.inputs["Metallic"].default_value = metallic
    bmp = nt.n("ShaderNodeBump")
    bmp.inputs["Strength"].default_value = bump
    bmp.inputs["Distance"].default_value = 0.02 * scale_m
    nt.link(bw.outputs["Val"], bmp.inputs["Height"])
    nt.link(bmp.outputs["Normal"], bsdf.inputs["Normal"])
    out = nt.n("ShaderNodeOutputMaterial")
    nt.link(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat


def flat_material(name: str, rgb, rough: float, *, metallic: float = 0.0, var: float = 0.15) -> bpy.types.Material:
    mat = bpy.data.materials.new(f"LOOK_{name}")
    tag(mat)
    nt = NT(mat)
    info = nt.n("ShaderNodeObjectInfo")
    grain = nt.noise(nt.coords(0.4), 1.0, 6.0)
    v = nt.math("ADD", 1.0, nt.math("MULTIPLY", nt.math("ADD", info.outputs["Random"], grain), var))
    hsv = nt.n("ShaderNodeHueSaturation")
    hsv.inputs["Color"].default_value = (*rgb, 1.0)
    nt.link(nt.math("SUBTRACT", v, var), hsv.inputs["Value"])
    bsdf = nt.n("ShaderNodeBsdfPrincipled")
    nt.link(hsv.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metallic
    out = nt.n("ShaderNodeOutputMaterial")
    nt.link(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat


def water_material(rgb) -> bpy.types.Material:
    mat = bpy.data.materials.new("LOOK_WATER")
    tag(mat)
    nt = NT(mat)
    pos = nt.n("ShaderNodeTexCoord").outputs["Object"]
    n1 = nt.noise(pos, 0.9, 4.0)
    n2 = nt.noise(pos, 0.07, 2.0)
    h = nt.math("ADD", n1, nt.math("MULTIPLY", n2, 3.0))
    bmp = nt.n("ShaderNodeBump")
    bmp.inputs["Strength"].default_value = 0.25
    bmp.inputs["Distance"].default_value = 0.08
    nt.link(h, bmp.inputs["Height"])
    lw = nt.n("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = 0.35
    deep = tuple(c * 0.6 for c in rgb)
    col = nt.mix(lw.outputs["Facing"], deep, tuple(min(1.0, c * 2.2) for c in rgb))
    bsdf = nt.n("ShaderNodeBsdfPrincipled")
    nt.link(col, bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.16
    bsdf.inputs["Specular IOR Level"].default_value = 0.35
    nt.link(bmp.outputs["Normal"], bsdf.inputs["Normal"])
    out = nt.n("ShaderNodeOutputMaterial")
    nt.link(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat


def leaf_material(rgb, name: str = "LEAF", fresh=(0.07, 0.15, 0.025), holes_at: float = 0.44) -> bpy.types.Material:
    mat = bpy.data.materials.new(f"LOOK_{name}")
    tag(mat)
    nt = NT(mat)
    pos = nt.n("ShaderNodeTexCoord").outputs["Object"]
    holes = nt.noise(pos, 38.0, 2.0)
    alpha = nt.math("GREATER_THAN", holes, holes_at)
    info = nt.n("ShaderNodeObjectInfo")
    hsv = nt.n("ShaderNodeHueSaturation")
    hsv.inputs["Color"].default_value = (*(0.5 * a + 0.5 * b for a, b in zip(rgb, fresh)), 1.0)
    nt.link(nt.math("ADD", 0.85, nt.math("MULTIPLY", info.outputs["Random"], 0.35)), hsv.inputs["Value"])
    nt.link(nt.math("ADD", 0.48, nt.math("MULTIPLY", info.outputs["Random"], 0.04)), hsv.inputs["Hue"])
    bsdf = nt.n("ShaderNodeBsdfPrincipled")
    nt.link(hsv.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.55
    trans = nt.n("ShaderNodeBsdfTranslucent")
    nt.link(hsv.outputs["Color"], trans.inputs["Color"])
    mix = nt.n("ShaderNodeMixShader")
    mix.inputs[0].default_value = 0.35
    nt.link(bsdf.outputs["BSDF"], mix.inputs[1])
    nt.link(trans.outputs["BSDF"], mix.inputs[2])
    clear = nt.n("ShaderNodeBsdfTransparent")
    cut = nt.n("ShaderNodeMixShader")
    nt.link(alpha, cut.inputs[0])
    nt.link(clear.outputs["BSDF"], cut.inputs[1])
    nt.link(mix.outputs["Shader"], cut.inputs[2])
    out = nt.n("ShaderNodeOutputMaterial")
    nt.link(cut.outputs["Shader"], out.inputs["Surface"])
    return mat


def invisible_material() -> bpy.types.Material:
    mat = bpy.data.materials.new("LOOK_INVISIBLE")
    tag(mat)
    nt = NT(mat)
    clear = nt.n("ShaderNodeBsdfTransparent")
    out = nt.n("ShaderNodeOutputMaterial")
    nt.link(clear.outputs["BSDF"], out.inputs["Surface"])
    return mat


def ground_material(pal: dict, city_quad: list[tuple[float, float]]) -> bpy.types.Material:
    """City interior = packed yellow earth with worn grass; outside the outer wall = spring field patchwork."""
    mat = bpy.data.materials.new("LOOK_GROUND")
    tag(mat)
    nt = NT(mat)
    pos = nt.n("ShaderNodeTexCoord").outputs["Object"]
    sep = nt.n("ShaderNodeSeparateXYZ")
    nt.link(pos, sep.inputs[0])
    px, py = sep.outputs["X"], sep.outputs["Y"]
    inside = None
    for i, (ax, ay) in enumerate(city_quad):
        bx, by = city_quad[(i + 1) % len(city_quad)]
        ln = math.hypot(bx - ax, by - ay)
        d = nt.math("ADD", nt.math("ADD", nt.math("MULTIPLY", py, (bx - ax) / ln), nt.math("MULTIPLY", px, -(by - ay) / ln)),
                    (-(bx - ax) * ay + (by - ay) * ax) / ln)
        inside = d if inside is None else nt.math("MINIMUM", inside, d)
    city = nt.math("MULTIPLY", nt.math("ADD", inside, 80.0), 1 / 160.0)
    city = nt.math("MINIMUM", nt.math("MAXIMUM", city, 0.0), 1.0)

    dirt = pbr_maps("raked_dirt")
    grass = pbr_maps("sparse_grass")
    soil = pbr_maps("farm_soil")
    v4 = nt.coords(4.0)
    dirt_c = nt.tex(dirt.diff, v4).outputs["Color"]
    grass_c = nt.tex(grass.diff, v4).outputs["Color"]
    soil_c = nt.tex(soil.diff, v4).outputs["Color"]

    def tinted(src, mean, rgb):
        bw = nt.n("ShaderNodeRGBToBW")
        nt.link(src, bw.inputs["Color"])
        return nt.mix(1.0, rgb, nt.math("DIVIDE", bw.outputs["Val"], max(1e-3, mean)), "MULTIPLY")

    earth = tinted(dirt_c, dirt.mean_luma, pal["earth"])
    worn = nt.math("GREATER_THAN", nt.noise(nt.coords(40.0), 1.0, 4.0), 0.56)
    city_col = nt.mix(nt.math("MULTIPLY", worn, 0.55), earth, tinted(grass_c, grass.mean_luma, pal["field"]))

    # 田块：长条地块网格（每 420 m 大块里随机横竖），每块一个随机作物色
    big = nt.n("ShaderNodeVectorMath", operation="FLOOR")
    nt.link(nt.coords(420.0), big.inputs[0])
    flip = nt.n("ShaderNodeTexWhiteNoise", noise_dimensions="3D")
    nt.link(big.outputs[0], flip.inputs["Vector"])
    horiz = nt.math("GREATER_THAN", flip.outputs["Value"], 0.5)
    cell_a = nt.n("ShaderNodeMapping")
    cell_a.inputs["Scale"].default_value = (1 / 45.0, 1 / 160.0, 1.0)
    nt.link(pos, cell_a.inputs["Vector"])
    cell_b = nt.n("ShaderNodeMapping")
    cell_b.inputs["Scale"].default_value = (1 / 160.0, 1 / 45.0, 1.0)
    nt.link(pos, cell_b.inputs["Vector"])
    fa = nt.n("ShaderNodeVectorMath", operation="FLOOR")
    nt.link(cell_a.outputs[0], fa.inputs[0])
    fb = nt.n("ShaderNodeVectorMath", operation="FLOOR")
    nt.link(cell_b.outputs[0], fb.inputs[0])
    wa = nt.n("ShaderNodeTexWhiteNoise", noise_dimensions="3D")
    nt.link(fa.outputs[0], wa.inputs["Vector"])
    wb = nt.n("ShaderNodeTexWhiteNoise", noise_dimensions="3D")
    nt.link(fb.outputs[0], wb.inputs["Vector"])
    cell_val = nt.mix(horiz, wa.outputs["Color"], wb.outputs["Color"])
    ramp = nt.n("ShaderNodeValToRGB")
    ramp.color_ramp.interpolation = "CONSTANT"
    fg = pal["field"]
    # bg8：刚返青的麦田为主，少量嫩黄绿与翻耕地
    stops = ((0.0, tuple(c * 1.0 for c in fg)), (0.3, tuple(c * 1.3 for c in fg)),
             (0.65, (fg[0] * 1.5, fg[1] * 1.45, fg[2] * 0.7)), (0.9, (pal["earth"][0] * 0.8, pal["earth"][1] * 0.7, pal["earth"][2] * 0.6)))
    els = ramp.color_ramp.elements
    els[0].position, els[0].color = stops[0][0], (*stops[0][1], 1.0)
    els[1].position, els[1].color = stops[1][0], (*stops[1][1], 1.0)
    for p, c in stops[2:]:
        e = els.new(p)
        e.color = (*c, 1.0)
    sepc = nt.n("ShaderNodeSeparateColor")
    nt.link(cell_val, sepc.inputs[0])
    nt.link(sepc.outputs[0], ramp.inputs["Fac"])
    rows = nt.n("ShaderNodeTexWave", wave_type="BANDS", bands_direction="X")
    rows.inputs["Scale"].default_value = 1.0
    nt.link(nt.coords(1.4), rows.inputs["Vector"])
    field = nt.mix(nt.math("MULTIPLY", rows.outputs["Fac"], 0.18), ramp.outputs["Color"], (0, 0, 0))
    field = nt.mix(0.5, field, tinted(soil_c, soil.mean_luma, (0.5, 0.5, 0.5)), "MULTIPLY")
    field = nt.mix(0.35, field, tinted(grass_c, grass.mean_luma, fg), "MIX")
    col = nt.mix(city, field, city_col)
    macro = nt.noise(nt.coords(400.0), 1.0, 3.0)
    hsv = nt.n("ShaderNodeHueSaturation")
    nt.link(col, hsv.inputs["Color"])
    nt.link(nt.math("ADD", 0.8, nt.math("MULTIPLY", macro, 0.4)), hsv.inputs["Value"])
    bsdf = nt.n("ShaderNodeBsdfPrincipled")
    nt.link(hsv.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.95
    bw = nt.n("ShaderNodeRGBToBW")
    nt.link(dirt_c, bw.inputs["Color"])
    bmp = nt.n("ShaderNodeBump")
    bmp.inputs["Strength"].default_value = 0.4
    bmp.inputs["Distance"].default_value = 0.05
    nt.link(bw.outputs["Val"], bmp.inputs["Height"])
    nt.link(bmp.outputs["Normal"], bsdf.inputs["Normal"])
    out = nt.n("ShaderNodeOutputMaterial")
    nt.link(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat


def build_materials(pal: dict, city_quad: list[tuple[float, float]]) -> list[bpy.types.Material]:
    patch = rammed_patch()

    def layers(nt: NT):
        vec = nt.coords(3.5)
        return nt.tex(patch, vec, box=True, non_color=True).outputs["Color"]

    mats = {
        "EARTH": pbr_material("EARTH", "raked_dirt", pal["earth"], 3.0, bump=0.5, keep_hue=0.1),
        "GROUND": ground_material(pal, city_quad),
        "WATER": water_material(pal["water"]),
        "RIVERBED": flat_material("RIVERBED", tuple(c * 0.5 for c in pal["water"]), 0.9),
        "RAMMED": pbr_material("RAMMED", "excavated_soil_wall", pal["rammed"], 4.0, bump=0.6, keep_hue=0.05, overlay=layers),
        "PLASTER": pbr_material("PLASTER", "white_rough_plaster", pal["plaster"], 2.5, bump=0.25, keep_hue=0.35),
        "TIMBER": pbr_material("TIMBER", "weathered_planks", pal["timber"], 1.5, bump=0.3, keep_hue=0.2),
        # bg1：朱漆发暗、磨损处露木，禁「鲜红新漆」——保留三成木纹原色
        "RED": pbr_material("RED", "weathered_planks", tuple(c * 0.85 for c in pal["red"]), 1.5, bump=0.35, keep_hue=0.3, var=0.2),
        "BLACK": pbr_material("BLACK", "weathered_planks", (0.02, 0.02, 0.02), 1.5, bump=0.2, keep_hue=0.0, var=0.1),
        "ROOF": pbr_material("ROOF", "roof_tiles_14", pal["roof"], 1.2, bump=0.8, keep_hue=0.0),
        "ROOF_UV": pbr_material("ROOF_UV", "roof_tiles_14", pal["roof"], 1.2, uv=True, bump=0.8, keep_hue=0.0),
        "GLAZED": pbr_material("GLAZED", "roof_tiles_14", pal["glazed"], 1.2, bump=0.8, keep_hue=0.0, rough_add=-0.35, var=0.1),
        "BRICK": pbr_material("BRICK", "dark_brick_wall", pal["brick"], 2.0, bump=0.4, keep_hue=0.1),
        "STONE": pbr_material("STONE", "large_sandstone_blocks", pal["stone"], 3.0, bump=0.4, keep_hue=0.15),
        "REED": pbr_material("REED", "reed_roof_04", (0.36, 0.30, 0.19), 2.0, bump=0.6, keep_hue=0.3),
        "WINDOW": flat_material("WINDOW", (0.012, 0.010, 0.008), 0.9, var=0.05),
        "GILT": flat_material("GILT", (0.55, 0.38, 0.12), 0.45, metallic=0.8, var=0.1),
        "LEAF": leaf_material(pal["leaf"]),
        "BARK": pbr_material("BARK", "bark_willow", (0.09, 0.08, 0.07), 1.0, bump=0.8, keep_hue=0.2),
        "CLOTH_RED": flat_material("CLOTH_RED", (0.28, 0.035, 0.03), 0.9),
        "CLOTH_BLUE": flat_material("CLOTH_BLUE", (0.03, 0.05, 0.16), 0.9),
        "INVISIBLE": invisible_material(),
        "FIELD": pbr_material("FIELD", "leafy_grass", pal["field"], 3.0, bump=0.3, keep_hue=0.1),
        "CLOTH_UNDYED": flat_material("CLOTH_UNDYED", (0.40, 0.37, 0.31), 0.9),     # 平民衣本白（麻布泛灰黄）
        "SKIN": flat_material("SKIN", (0.30, 0.19, 0.13), 0.6),
        # bg4：御沟两岸桃李梨杏，白与淡粉的花（不是柳）
        "BLOSSOM": leaf_material((0.80, 0.62, 0.66), "BLOSSOM", fresh=(0.85, 0.80, 0.78), holes_at=0.4),
    }
    return [mats[n] for n in MAT_NAMES]


def set_slots(me: bpy.types.Mesh, mats: list[bpy.types.Material]) -> None:
    me.materials.clear()
    for m in mats:
        me.materials.append(m)


# ── mesh builder with material index + UV ───────────────────────────────────────────────────────────────────────
class MB:
    def __init__(self) -> None:
        self.bm = bmesh.new()
        self.uv = self.bm.loops.layers.uv.new("UVMap")

    def face(self, pts, mat: str, uvs=None) -> None:
        vs = [self.bm.verts.new(Vector(p)) for p in pts]
        f = self.bm.faces.new(vs)
        f.material_index = M[mat]
        if uvs is None:
            n = f.normal
            ax = 0 if abs(n.x) > max(abs(n.y), abs(n.z)) else (1 if abs(n.y) > abs(n.z) else 2)
            uvs = [((p[1], p[2]) if ax == 0 else (p[0], p[2]) if ax == 1 else (p[0], p[1])) for p in pts]
        for lp, uv in zip(f.loops, uvs):
            lp[self.uv].uv = uv

    def box(self, lo, hi, mat: str, skip: str = "") -> None:
        x0, y0, z0 = lo
        x1, y1, z1 = hi
        faces = {
            "b": [(x0, y0, z0), (x0, y1, z0), (x1, y1, z0), (x1, y0, z0)],
            "t": [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)],
            "s": [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)],
            "n": [(x1, y1, z0), (x0, y1, z0), (x0, y1, z1), (x1, y1, z1)],
            "w": [(x0, y1, z0), (x0, y0, z0), (x0, y0, z1), (x0, y1, z1)],
            "e": [(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)],
        }
        for k, pts in faces.items():
            if k not in skip:
                self.face(pts, mat)

    def cbox(self, c, s, mat: str) -> None:
        self.box((c[0] - s[0] / 2, c[1] - s[1] / 2, c[2] - s[2] / 2), (c[0] + s[0] / 2, c[1] + s[1] / 2, c[2] + s[2] / 2), mat)

    def tube(self, pts: list[Vector], radii: list[float], seg: int, mat: str, cap: bool = True) -> None:
        rings = []
        for i, p in enumerate(pts):
            d = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized()
            a = Vector((1, 0, 0)) if abs(d.z) > 0.9 else Vector((0, 0, 1))
            u = d.cross(a).normalized()
            v = d.cross(u)
            rings.append([p + (u * math.cos(2 * math.pi * k / seg) + v * math.sin(2 * math.pi * k / seg)) * radii[i]
                          for k in range(seg)])
        for i in range(len(rings) - 1):
            for k in range(seg):
                j = (k + 1) % seg
                self.face([rings[i][k], rings[i][j], rings[i + 1][j], rings[i + 1][k]], mat,
                          uvs=[(k / seg, i), ((k + 1) / seg, i), ((k + 1) / seg, i + 1), (k / seg, i + 1)])
        if cap:
            self.face(list(reversed(rings[0])), mat)
            self.face(rings[-1], mat)

    def finish(self, name: str, mats: list[bpy.types.Material]) -> bpy.types.Object:
        bmesh.ops.remove_doubles(self.bm, verts=self.bm.verts, dist=1e-5)
        me = bpy.data.meshes.new(name)
        set_slots(me, mats)
        self.bm.to_mesh(me)
        self.bm.free()
        ob = bpy.data.objects.new(name, me)
        tag(ob)
        return ob


# ── Song vernacular house pieces (front = +Y, origin at street level) ───────────────────────────────────────────────
def roof(mb: MB, x0: float, x1: float, yb: float, yf: float, eave: float, ridge: float, *, mat: str = "ROOF_UV",
         over_f: float = 0.8, over_s: float = 0.45, segs: int = 5, thick: float = 0.16, ridge_tiles: bool = True,
         curve: float = 1.45) -> None:
    """悬山 two-slope roof, ridge along X, concave slope (flat at the eave, steep at the ridge)."""
    xa, xb = x0 - over_s, x1 + over_s
    ym = (yb + yf) / 2
    ze = eave - 0.25
    for side, y_edge in ((1, yf + over_f), (-1, yb - over_f)):
        prof = []
        for k in range(segs + 1):
            t = k / segs
            prof.append((y_edge + (ym - y_edge) * t, ze + (ridge - ze) * t ** curve))
        dist = [0.0]
        for a, b in zip(prof, prof[1:]):
            dist.append(dist[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
        for (ya, za), (yb_, zb), da, db in zip(prof, prof[1:], dist, dist[1:]):
            top = [(xa, ya, za), (xb, ya, za), (xb, yb_, zb), (xa, yb_, zb)]
            if side < 0:
                top = [top[1], top[0], top[3], top[2]]
            u = [(xa, dist[-1] - da), (xb, dist[-1] - da), (xb, dist[-1] - db), (xa, dist[-1] - db)]
            if side < 0:
                u = [u[1], u[0], u[3], u[2]]
            mb.face(top, mat, uvs=u)
            bot = [(p[0], p[1], p[2] - thick) for p in reversed(top)]
            mb.face(bot, "TIMBER")
        e = prof[0]
        edge = [(xa, e[0], e[1] - thick), (xb, e[0], e[1] - thick), (xb, e[0], e[1]), (xa, e[0], e[1])]
        mb.face(edge if side > 0 else [edge[1], edge[0], edge[3], edge[2]], "TIMBER")
        for xs, sgn in ((xa, -1), (xb, 1)):
            for (ya, za), (yb_, zb) in zip(prof, prof[1:]):
                q = [(xs, ya, za - thick), (xs, yb_, zb - thick), (xs, yb_, zb), (xs, ya, za)]
                if (sgn > 0) != (side > 0):
                    q = [q[1], q[0], q[3], q[2]]
                mb.face(q, "TIMBER")
    if ridge_tiles:
        mb.box((xa - 0.05, ym - 0.2, ridge - 0.12), (xb + 0.05, ym + 0.2, ridge + 0.28), mat.replace("_UV", ""))
        for xs in (xa, xb):
            mb.box((xs - 0.12, ym - 0.16, ridge + 0.2), (xs + 0.12, ym + 0.16, ridge + 0.62), mat.replace("_UV", ""))


def gable_walls(mb: MB, x0: float, x1: float, yb: float, yf: float, eave: float, ridge: float, wall: str) -> None:
    ym = (yb + yf) / 2
    for xs, sgn in ((x0, -1), (x1, 1)):
        tri = [(xs, yb, eave), (xs, yf, eave), (xs, ym, ridge - 0.35)]
        mb.face(tri if sgn > 0 else list(reversed(tri)), wall)


def lattice(mb: MB, xc: float, y: float, z0: float, w: float, h: float, bars: int = 5) -> None:
    mb.box((xc - w / 2, y - 0.02, z0), (xc + w / 2, y + 0.01, z0 + h), "WINDOW")
    mb.box((xc - w / 2 - 0.08, y, z0 - 0.08), (xc + w / 2 + 0.08, y + 0.06, z0), "TIMBER")
    mb.box((xc - w / 2 - 0.08, y, z0 + h), (xc + w / 2 + 0.08, y + 0.06, z0 + h + 0.08), "TIMBER")
    for k in range(bars + 1):
        x = xc - w / 2 + w * k / bars
        mb.box((x - 0.025, y, z0), (x + 0.025, y + 0.05, z0 + h), "TIMBER")


def unit(mb: MB, x0: float, x1: float, yb: float, yf: float, eave: float, ridge: float, style: str, lod: int,
         rng: random.Random) -> None:
    """One bay-block of a house: plinth, walls, posts, openings, roof. style ∈ tile / shop / thatch / tall."""
    wall = "RAMMED" if style == "thatch" else "PLASTER"
    roof_mat = "REED" if style == "thatch" else "ROOF_UV"
    if lod == 1:
        mb.box((x0, yb, 0.0), (x1, yf, eave), wall)
        gable_walls(mb, x0, x1, yb, yf, eave, ridge, wall)
        roof(mb, x0, x1, yb, yf, eave, ridge, mat=roof_mat, segs=2, ridge_tiles=style != "thatch")
        return
    plinth = 0.0 if style == "thatch" else 0.4
    if plinth:
        mb.box((x0 - 0.05, yb - 0.05, 0.0), (x1 + 0.05, yf + 0.05, plinth), "BRICK")
    top = eave - 0.35
    mb.box((x0 + 0.05, yb + 0.05, plinth), (x1 - 0.05, yf - 0.05, eave), wall, skip="bt")
    gable_walls(mb, x0 + 0.05, x1 - 0.05, yb + 0.05, yf - 0.05, eave, ridge, wall)
    n_bay = max(1, round((x1 - x0) / 3.3))
    for y in (yb, yf):
        for k in range(n_bay + 1):
            x = x0 + 0.12 + (x1 - x0 - 0.24) * k / n_bay
            mb.box((x - 0.12, y - 0.12, plinth), (x + 0.12, y + 0.12, eave), "TIMBER")
        mb.box((x0, y - 0.1, top), (x1, y + 0.1, top + 0.3), "TIMBER")
    for x in (x0, x1):
        mb.box((x - 0.1, yb, top), (x + 0.1, yf, top + 0.3), "TIMBER")
    yfa = yf + 0.07
    if style == "shop":
        w = x1 - x0 - 0.5
        mb.box((x0 + 0.25, yf - 0.02, plinth), (x1 - 0.25, yf + 0.02, min(top, plinth + 2.6)), "WINDOW")
        n_board = int(w / 0.34)
        for k in range(n_board):
            if rng.random() < 0.45:
                continue
            xb = x0 + 0.25 + k * 0.34
            mb.box((xb, yfa - 0.03, plinth + 0.02), (xb + 0.3, yfa + 0.02, plinth + 2.5), "TIMBER")
        aw = min(top, plinth + 2.7)
        mb.face([(x0, yf, aw), (x1, yf, aw), (x1, yf + 1.4, aw - 0.45), (x0, yf + 1.4, aw - 0.45)], "REED")
        mb.face([(x1, yf, aw - 0.06), (x0, yf, aw - 0.06), (x0, yf + 1.4, aw - 0.51), (x1, yf + 1.4, aw - 0.51)], "REED")
        for x in (x0 + 0.15, x1 - 0.15):
            mb.box((x - 0.05, yf + 1.3, 0.0), (x + 0.05, yf + 1.4, aw - 0.45), "TIMBER")
    else:
        dw = 1.2
        dh = min(2.2, top - plinth - 0.2)
        xc = (x0 + x1) / 2 + (rng.uniform(-0.3, 0.3) if x1 - x0 > 4 else 0.0)
        mb.box((xc - dw / 2, yf - 0.02, plinth), (xc + dw / 2, yf + 0.03, plinth + dh), "WINDOW")
        for sx in (-1, 1):
            mb.box((xc + sx * dw / 2 - 0.07, yf, plinth), (xc + sx * dw / 2 + 0.07, yfa, plinth + dh + 0.1), "TIMBER")
        mb.box((xc - dw / 2 - 0.07, yf, plinth + dh), (xc + dw / 2 + 0.07, yfa, plinth + dh + 0.14), "TIMBER")
        if x1 - x0 > 3.2:
            for sx in (-1, 1):
                wx = (xc + x0) / 2 if sx < 0 else (xc + x1) / 2
                if abs(wx - xc) > 1.1:
                    lattice(mb, wx, yfa, plinth + 1.0, min(1.1, abs(wx - xc) * 0.9), 0.8)
        lattice(mb, (x0 + x1) / 2, yb - 0.09, plinth + 1.3, 0.8, 0.6, 3)
    if style == "tall":
        pent = min(3.1, eave * 0.5)
        mb.face([(x0 - 0.2, yf + 0.1, pent), (x1 + 0.2, yf + 0.1, pent), (x1 + 0.2, yf + 1.0, pent - 0.35), (x0 - 0.2, yf + 1.0, pent - 0.35)],
                "ROOF_UV", uvs=[(0, 0.9), (x1 - x0, 0.9), (x1 - x0, 0), (0, 0)])
        mb.box((x0, yf, pent - 0.15), (x1, yf + 0.12, pent), "TIMBER")
        n_win = max(1, int((x1 - x0) / 1.6))
        for k in range(n_win):
            lattice(mb, x0 + (x1 - x0) * (k + 0.5) / n_win, yfa, pent + 0.5, 1.0, 1.0, 4)
    roof(mb, x0, x1, yb, yf, eave, ridge, mat=roof_mat, segs=5, thick=0.35 if style == "thatch" else 0.16,
         ridge_tiles=style != "thatch", curve=1.0 if style == "thatch" else 1.45)


def house_object(name: str, parts: list[tuple[float, float, float, float, float, float]], style: str, lod: int, seed: int,
                 mats: list[bpy.types.Material], extra=None) -> bpy.types.Object:
    rng = random.Random(seed)
    mb = MB()
    for x0, x1, yb, yf, eave, ridge in parts:
        unit(mb, x0, x1, yb, yf, eave, ridge, style, lod, rng)
    if extra:
        extra(mb)
    return mb.finish(name, mats)


def p10_parts() -> list[tuple]:
    B = bj.BAY
    return [(2.0, 2.0 + B, -3.25, 1.75, 2.7, 4.3), (-2.0, -2.0 + B, -3.25, 1.75, 5.0, 6.6), (-6.0, -6.0 + B, -3.25, 1.75, 2.7, 4.3)]


def p9_extra(mb: MB) -> None:
    for x in (-0.9, 3.9):
        mb.tube([Vector((x, 3.65, 0.0)), Vector((x, 3.65, 7.5))], [0.11, 0.09], 8, "TIMBER")
    for z in (2.6, 5.0, 7.4):
        mb.box((-1.1, 3.55, z - 0.1), (4.1, 3.75, z + 0.1), "TIMBER")
    for k, x in enumerate((-0.4, 0.6, 1.6, 2.6, 3.4)):
        mb.box((x - 0.18, 3.5, 2.7 + 0.25 * (k % 2)), (x + 0.18, 3.52, 4.9), "CLOTH_RED" if k % 2 else "CLOTH_BLUE")
    for x in (-3.9, -0.6):
        for y in (-0.65, 2.15):
            mb.box((x - 0.05, y - 0.05, 0.0), (x + 0.05, y + 0.05, 2.5), "TIMBER")
    mb.face([(-4.1, -0.85, 2.6), (-0.4, -0.85, 2.6), (-0.4, 2.35, 2.45), (-4.1, 2.35, 2.45)], "REED")
    mb.face([(-0.4, -0.85, 2.52), (-4.1, -0.85, 2.52), (-4.1, 2.35, 2.37), (-0.4, 2.35, 2.37)], "REED")


def p10_extra(mb: MB) -> None:
    mb.face([(-6.0, 1.75, 2.62), (-2.0, 1.75, 2.62), (-2.0, 3.25, 2.12), (-6.0, 3.25, 2.12)], "REED")
    mb.face([(-2.0, 1.75, 2.56), (-6.0, 1.75, 2.56), (-6.0, 3.25, 2.06), (-2.0, 3.25, 2.06)], "REED")
    for x in (-5.9, -2.1):
        mb.box((x - 0.06, 3.09, 0.0), (x + 0.06, 3.21, 2.12), "TIMBER")


# ── 虹桥 p8: woven timber arch, plank deck, lacquered railing ───────────────────────────────────────────────────────
def bridge_object(mats: list[bpy.types.Material]) -> bpy.types.Object:
    mb = MB()
    hw, foot, arch = bj.BRIDGE_HALF_W, bj.BRIDGE_FOOT, bj.BRIDGE_ARCH_HALF
    dt = bj.deck_top
    for sysk, (nodes_y, z_off) in enumerate((((-12.5, -7.5, -2.5, 2.5, 7.5, 12.5), -0.95),
                                             ((-10.0, -5.0, 0.0, 5.0, 10.0), -1.45))):
        pts_yz = []
        for y in nodes_y:
            yy = max(-arch, min(arch, y))
            spring = abs(y) >= 12.0
            pts_yz.append((y, 0.35 if spring else dt(yy) - DECK_OFF + z_off))
        n_log = 13 if sysk == 0 else 12
        for k in range(n_log):
            x = -hw + 0.3 + (2 * hw - 0.6) * (k + (0.5 if sysk else 0.0)) / (n_log - (0 if sysk else 1))
            for (ya, za), (yb, zb) in zip(pts_yz, pts_yz[1:]):
                mb.tube([Vector((x, ya, za)), Vector((x, yb, zb))], [0.17, 0.17], 7, "RED", cap=False)
        for y, z in pts_yz:
            mb.tube([Vector((-hw - 0.2, y, z + 0.05)), Vector((hw + 0.2, y, z + 0.05))], [0.2, 0.2], 8, "RED")
    step = 0.5
    ys = [-foot + step * i for i in range(int(2 * foot / step) + 1)]
    for ya, yb in zip(ys, ys[1:]):
        za, zb = dt(ya), dt(yb)
        mb.face([(-hw, ya, za), (hw, ya, za), (hw, yb, zb), (-hw, yb, zb)], "TIMBER",
                uvs=[(0, ya), (2 * hw, ya), (2 * hw, yb), (0, yb)])
        for sx in (-1, 1):
            x = sx * hw
            q = [(x, ya, za - 0.45), (x, yb, zb - 0.45), (x, yb, zb), (x, ya, za)]
            mb.face(q if sx > 0 else [q[1], q[0], q[3], q[2]], "RED")
        if abs(ya) < arch:
            mb.face([(hw, ya, za - 0.45), (-hw, ya, za - 0.45), (-hw, yb, zb - 0.45), (hw, yb, zb - 0.45)], "RED")
    for sgn in (-1, 1):
        prof = [(y, dt(y)) for y in ys if abs(y) >= arch - 1e-6 and y * sgn > 0]
        for (ya, za), (yb, zb) in zip(prof, prof[1:]):
            for sx in (-1, 1):
                x = sx * hw
                q = [(x, ya, bj.Z_WATER), (x, yb, bj.Z_WATER), (x, yb, zb - 0.45), (x, ya, za - 0.45)]
                mb.face(q if sx > 0 else [q[1], q[0], q[3], q[2]], "RAMMED")
    for sx in (-1, 1):
        x = sx * (hw - 0.1)
        for i in range(37):
            y = -18.0 + i
            mb.box((x - 0.08, y - 0.08, dt(y)), (x + 0.08, y + 0.08, dt(y) + 1.15), "RED")
        rail = [Vector((x, y, dt(y) + 1.05)) for y in (-18.0 + 0.5 * i for i in range(73))]
        mb.tube(rail, [0.06] * len(rail), 6, "RED")
        mid = [Vector((x, y, dt(y) + 0.55)) for y in (-18.0 + 0.5 * i for i in range(73))]
        mb.tube(mid, [0.04] * len(mid), 6, "RED")
    return mb.finish("LOOK_p8_honqiao", mats)


DECK_OFF = 0.6


# ── shot-layer assets: 纲船 hull, anonymous figures (used by build_bianjing previz when the scene is dressed) ───────
def ensure_mats() -> list[bpy.types.Material] | None:
    """The look material list if this blend has been dressed, else None (shot previz then falls back to boxes)."""
    mats = [bpy.data.materials.get(f"LOOK_{n}") for n in MAT_NAMES]
    return mats if all(mats) else None


def boat_object(name: str, ln: float, wd: float, hh: float, mats: list[bpy.types.Material]) -> bpy.types.Object:
    """平底纲船：origin at the waterline centre, length along X (bow −X), matting cabin amidships, deck at z 1.0."""
    mb = MB()
    n = 16
    secs = []
    for i in range(n + 1):
        u = -1 + 2 * i / n
        x = u * ln / 2
        half = wd / 2 * (1 - 0.45 * abs(u) ** 4)
        zb = -0.6 + 1.1 * abs(u) ** 6
        zg = 1.2 + 0.45 * abs(u) ** 3
        secs.append([(x, -half * 0.85, zb), (x, half * 0.85, zb), (x, half, zg), (x, -half, zg)])
    for a, b in zip(secs, secs[1:]):
        mb.face([a[0], b[0], b[1], a[1]], "TIMBER")
        mb.face([a[1], b[1], b[2], a[2]], "TIMBER")
        mb.face([a[3], b[3], b[0], a[0]], "TIMBER")
        mb.face([(a[3][0], a[3][1] + 0.12, 1.0), (b[3][0], b[3][1] + 0.12, 1.0), (b[2][0], b[2][1] - 0.12, 1.0),
                 (a[2][0], a[2][1] - 0.12, 1.0)], "TIMBER")
    for end in (secs[0], secs[-1]):
        mb.face(end, "TIMBER")
    for s in (-1, 1):
        rail = [Vector((sec[2 if s > 0 else 3][0], sec[2 if s > 0 else 3][1], sec[2][2])) for sec in secs]
        mb.tube(rail, [0.07] * len(rail), 6, "TIMBER")
    x0, x1 = -0.3 * ln, 0.2 * ln
    cw = 0.4 * wd
    mb.box((x0, -cw, 1.0), (x1, -cw + 0.08, hh - 0.4), "TIMBER")
    mb.box((x0, cw - 0.08, 1.0), (x1, cw, hh - 0.4), "TIMBER")
    for xw in np.linspace(x0 + 0.8, x1 - 0.8, max(2, int((x1 - x0) / 1.6))):
        for s in (-1, 1):
            lattice(mb, float(xw), s * (cw + 0.03), 1.7, 0.8, 0.6, 3)
    arc = 10
    for k in range(arc):
        a0, a1 = math.pi * k / arc, math.pi * (k + 1) / arc
        y0, z0 = -math.cos(a0) * (cw + 0.15), hh - 0.4 + math.sin(a0) * 0.55
        y1, z1 = -math.cos(a1) * (cw + 0.15), hh - 0.4 + math.sin(a1) * 0.55
        mb.face([(x0 - 0.2, y0, z0), (x1 + 0.2, y0, z0), (x1 + 0.2, y1, z1), (x0 - 0.2, y1, z1)], "REED",
                uvs=[(0, k * 0.3), (x1 - x0, k * 0.3), (x1 - x0, (k + 1) * 0.3), (0, (k + 1) * 0.3)])
    for s in (-1, 1):
        for k in range(5):
            xs = 0.3 * ln + k * 0.9
            mb.box((xs - 0.35, s * 0.8 - 0.3, 1.0), (xs + 0.35, s * 0.8 + 0.3, 1.45), "REED")
    return mb.finish(name, mats)


def figure_object(name: str, pose: str, mats: list[bpy.types.Material], cloth: str = "CLOTH_UNDYED") -> bpy.types.Object:
    """Anonymous labourer, 1.7 m, feet at origin, facing +Y. pose ∈ walk / haul (both hands forward-down) / pole."""
    mb = MB()
    V = Vector
    mb.tube([V((0, 0, 1.46)), V((0, 0, 1.56)), V((0, 0, 1.66)), V((0, 0, 1.74))], [0.07, 0.105, 0.1, 0.03], 8, "SKIN")
    mb.tube([V((0, -0.01, 1.68)), V((0, -0.01, 1.78))], [0.11, 0.08], 8, "WINDOW")
    mb.tube([V((0, 0, 0.78)), V((0, 0, 1.0)), V((0, 0, 1.22)), V((0, 0, 1.44))], [0.21, 0.18, 0.19, 0.15], 8, cloth)
    for s in (-1, 1):
        mb.tube([V((s * 0.1, 0, 0.84)), V((s * 0.11, 0.02, 0.45)), V((s * 0.12, 0, 0.06))], [0.08, 0.065, 0.055], 6, cloth)
        mb.box((s * 0.12 - 0.05, -0.05, 0.0), (s * 0.12 + 0.05, 0.16, 0.07), "WINDOW")
    arms = {
        "walk": {1: (V((0.25, 0.02, 1.12)), V((0.26, 0.06, 0.86))), -1: (V((-0.25, -0.02, 1.12)), V((-0.26, -0.04, 0.86)))},
        "haul": {1: (V((0.22, 0.28, 1.12)), V((0.12, 0.5, 0.92))), -1: (V((-0.22, 0.28, 1.12)), V((-0.12, 0.5, 0.92)))},
        "pole": {1: (V((0.24, 0.22, 1.25)), V((0.12, 0.35, 1.36))), -1: (V((-0.22, 0.25, 1.05)), V((-0.05, 0.38, 1.02)))},
    }[pose]
    for s in (-1, 1):
        elbow, hand = arms[s]
        mb.tube([V((s * 0.2, 0, 1.4)), elbow, hand], [0.06, 0.05, 0.045], 6, cloth)
        mb.tube([hand, hand + (hand - elbow).normalized() * 0.1], [0.045, 0.035], 6, "SKIN")
    return mb.finish(name, mats)


# ── flowering fruit tree (御街 peach / plum / pear / apricot, bg4) ──────────────────────────────────────────────
def blossom_object(name: str, seed: int, mats: list[bpy.types.Material]) -> bpy.types.Object:
    """Unit tree: height 8 m, crown radius 3.2 m. Short trunk, spreading branches, clusters of petal cards."""
    rng = random.Random(seed)
    mb = MB()
    trunk = [Vector((0, 0, 0)), Vector((rng.uniform(-0.2, 0.2), rng.uniform(-0.2, 0.2), 1.4)), Vector((0, 0, 2.2))]
    mb.tube(trunk, [0.2, 0.15, 0.12], 8, "BARK")
    top = trunk[-1]
    for k in range(7):
        a = 2 * math.pi * k / 7 + rng.uniform(-0.3, 0.3)
        tip = top + Vector((math.cos(a) * rng.uniform(1.8, 2.8), math.sin(a) * rng.uniform(1.8, 2.8), rng.uniform(2.6, 4.6)))
        mb.tube([top, top.lerp(tip, 0.5) + Vector((0, 0, 0.3)), tip], [0.08, 0.05, 0.02], 5, "BARK", cap=False)
        for _ in range(26):
            c = tip.lerp(top, rng.uniform(0.0, 0.55)) + Vector((rng.uniform(-0.9, 0.9), rng.uniform(-0.9, 0.9), rng.uniform(-0.5, 0.7)))
            u = Vector((rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-0.3, 0.3))).normalized() * 0.45
            v = u.cross(Vector((0, 0, 1))).normalized() * 0.45
            mb.face([c - u - v, c + u - v, c + u + v, c - u + v], "BLOSSOM")
    return mb.finish(name, mats)


BLOSSOM_SOURCES = ("C_35_trees_E", "C_35_trees_W", "G_4011_yujie_E", "G_4011_yujie_W")


# ── willow ──────────────────────────────────────────────────────────────────────────────────────────────────────
def willow_object(name: str, seed: int, mats: list[bpy.types.Material]) -> bpy.types.Object:
    """Unit willow: height 8 m, crown radius 3.2 m, trunk base at origin."""
    """bg8：老干粗、开裂、歪斜，截头后萌出一丛细长枝条，长长的柳丝垂到肩高。"""
    rng = random.Random(seed)
    mb = MB()
    lean = Vector((rng.uniform(-1.0, 1.0), rng.uniform(-1.0, 1.0), 0.0))
    trunk = [Vector((0, 0, 0)) + lean * (t * t) + Vector((rng.uniform(-0.1, 0.1), rng.uniform(-0.1, 0.1), 2.9 * t))
             for t in (0, 0.25, 0.5, 0.75, 1.0)]
    mb.tube(trunk, [0.5, 0.4, 0.36, 0.38, 0.34], 10, "BARK")
    top = trunk[-1]
    tips = []
    for k in range(13):
        a = 2 * math.pi * k / 13 + rng.uniform(-0.25, 0.25)
        r = rng.uniform(1.3, 2.8)
        tip = top + Vector((math.cos(a) * r, math.sin(a) * r, rng.uniform(3.4, 5.0)))
        mid = top.lerp(tip, 0.45) + Vector((0, 0, 0.6))
        mb.tube([top, mid, tip], [0.1, 0.05, 0.02], 5, "BARK", cap=False)
        tips.append((top, mid, tip))
    for s in range(300):
        a0, m0, t0 = tips[s % len(tips)]
        t = rng.uniform(0.4, 1.0)
        p = (a0.lerp(m0, t * 2) if t < 0.5 else m0.lerp(t0, (t - 0.5) * 2)) + Vector((rng.uniform(-0.4, 0.4), rng.uniform(-0.4, 0.4), 0))
        length = rng.uniform(2.5, max(2.6, p.z - 1.5))
        out = Vector((p.x, p.y, 0.0))
        out = out.normalized() if out.length > 1e-3 else Vector((1, 0, 0))
        yaw = rng.uniform(0, math.pi)
        side = Vector((math.cos(yaw), math.sin(yaw), 0.0)) * 0.07
        prev = None
        for k in range(6):
            f = k / 5
            q = p + out * (0.35 * math.sin(f * 1.4)) + Vector((0, 0, -length * f))
            if prev is not None:
                mb.face([prev - side * (1 - f + 0.2), prev + side * (1 - f + 0.2), q + side * (1 - f), q - side * (1 - f)], "LEAF")
            prev = q
    return mb.finish(name, mats)


# ── layout parsing (primitive islands are contiguous vertex ranges, see build_bianjing.Batch) ────────────────────────
def islands(me: bpy.types.Mesh) -> tuple[np.ndarray, np.ndarray]:
    nv = len(me.vertices)
    co = np.empty(nv * 3, np.float32)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    ev = np.empty(len(me.edges) * 2, np.int64)
    me.edges.foreach_get("vertices", ev)
    ev = ev.reshape(-1, 2)
    lo, hi = ev.min(axis=1), ev.max(axis=1)
    cover = np.zeros(nv + 1, np.int64)
    np.add.at(cover, lo + 1, 1)
    np.add.at(cover, hi + 1, -1)
    crossed = np.cumsum(cover)[:nv]          # edges with lo < s <= hi: vertex s sits inside some primitive
    starts = np.nonzero(crossed == 0)[0]
    return co, starts


def face_arrays(me: bpy.types.Mesh) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    n = len(me.polygons)
    nrm = np.empty(n * 3, np.float32)
    cen = np.empty(n * 3, np.float32)
    first = np.empty(n, np.int64)
    me.polygons.foreach_get("normal", nrm)
    me.polygons.foreach_get("center", cen)
    me.polygons.foreach_get("loop_start", first)
    lv = np.empty(len(me.loops), np.int64)
    me.loops.foreach_get("vertex_index", lv)
    return nrm.reshape(-1, 3), cen.reshape(-1, 3), lv[first]


@dataclass
class Tree:
    base: Vector
    height: float
    crown: float


def tree_islands(ob: bpy.types.Object) -> tuple[list[Tree], set[int]]:
    """Batch.ball crowns (icosahedron: 12 verts, extents equal in x/y/z) + the trunk cylinder (12 verts, tall and thin)
    right under them → trees (world); returns island ids to hide."""
    co, starts = islands(ob.data)
    sizes = np.diff(np.append(starts, len(co)))
    mw = ob.matrix_world
    trunks: dict[tuple[int, int], tuple[int, float]] = {}
    crowns: list[int] = []
    for i, (s, n) in enumerate(zip(starts, sizes)):
        if n not in (12, 42):
            continue
        pts = co[s:s + n]
        ext = pts.max(axis=0) - pts.min(axis=0)
        if abs(ext[2] - ext[0]) < 0.15 * max(ext[0], 1e-3) and ext[0] > 0.6:
            crowns.append(i)
        elif ext[2] > 2.5 * max(ext[0], ext[1]):
            trunks[(int(round(pts[:, 0].mean() * 10)), int(round(pts[:, 1].mean() * 10)))] = (i, float(pts[:, 2].min()))
    out, hide = [], set()
    for i in crowns:
        s, n = starts[i], sizes[i]
        pts = co[s:s + n]
        c = pts.mean(axis=0)
        r = float((pts[:, 0].max() - pts[:, 0].min()) / 2)
        key = (int(round(c[0] * 10)), int(round(c[1] * 10)))
        tr = trunks.get(key)
        base_z = tr[1] if tr else float(c[2] - r - 2.0)
        if tr:
            hide.add(tr[0])
        hide.add(i)
        w = mw @ Vector((float(c[0]), float(c[1]), base_z))
        out.append(Tree(w, float(c[2]) + r - base_z, r))
    return out, hide


@dataclass
class Unit:
    loc: Vector
    yaw: float
    mirror: bool
    dims: tuple[float, float, float]


def house_units(ob: bpy.types.Object) -> list[Unit]:
    """build_bianjing.house(): an 8-vert box (bottom ring q0..q3 then top ring) optionally followed by a 6-vert roof prism."""
    co, starts = islands(ob.data)
    sizes = np.diff(np.append(starts, len(co)))
    mw = ob.matrix_world
    out: list[Unit] = []
    for idx, (s, n) in enumerate(zip(starts, sizes)):
        if n != 8:
            continue
        q = co[s:s + 4]
        top = float(co[s + 4, 2])
        if idx + 1 < len(starts) and sizes[idx + 1] == 6:
            top = max(top, float(co[starts[idx + 1]:starts[idx + 1] + 6, 2].max()))
        u = Vector((float(q[1, 0] - q[0, 0]), float(q[1, 1] - q[0, 1]), 0.0))
        nvec = Vector((float(q[3, 0] - q[0, 0]), float(q[3, 1] - q[0, 1]), 0.0))
        lx, ly = u.length, nvec.length
        c = Vector((float(q[:, 0].mean()), float(q[:, 1].mean()), float(q[0, 2])))
        mirror = u.cross(nvec).z < 0
        ax = -u if mirror else u
        w = mw @ c
        out.append(Unit(w, math.atan2(ax.y, ax.x) + mw.to_euler().z, mirror, (lx, ly, top - float(q[0, 2]))))
    return out


# ── instancers ──────────────────────────────────────────────────────────────────────────────────────────────────
def instancer(name: str, col: bpy.types.Collection, protos: bpy.types.Collection,
              pts: list[tuple[Vector, float, tuple[float, float, float], int]]) -> bpy.types.Object:
    me = bpy.data.meshes.new(name)
    me.vertices.add(len(pts))
    me.vertices.foreach_set("co", np.array([tuple(p[0]) for p in pts], np.float32).ravel())
    rot = me.attributes.new("look_rot", "FLOAT_VECTOR", "POINT")
    rot.data.foreach_set("vector", np.array([(0.0, 0.0, p[1]) for p in pts], np.float32).ravel())
    scl = me.attributes.new("look_scl", "FLOAT_VECTOR", "POINT")
    scl.data.foreach_set("vector", np.array([p[2] for p in pts], np.float32).ravel())
    pick = me.attributes.new("look_pick", "INT", "POINT")
    pick.data.foreach_set("value", np.array([p[3] for p in pts], np.int32))
    ob = bpy.data.objects.new(name, me)
    tag(ob)
    col.objects.link(ob)
    tree = bpy.data.node_groups.new(f"{name}_GN", "GeometryNodeTree")
    tag(tree)
    tree.interface.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    tree.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    nodes, links = tree.nodes, tree.links
    gi, go = nodes.new("NodeGroupInput"), nodes.new("NodeGroupOutput")
    m2p = nodes.new("GeometryNodeMeshToPoints")
    iop = nodes.new("GeometryNodeInstanceOnPoints")
    ci = nodes.new("GeometryNodeCollectionInfo")
    ci.inputs["Collection"].default_value = protos
    ci.inputs["Separate Children"].default_value = True
    ci.inputs["Reset Children"].default_value = True
    ci.transform_space = "ORIGINAL"
    na = {}
    for key, dt in (("look_rot", "FLOAT_VECTOR"), ("look_scl", "FLOAT_VECTOR"), ("look_pick", "INT")):
        nd = nodes.new("GeometryNodeInputNamedAttribute")
        nd.data_type = dt
        nd.inputs["Name"].default_value = key
        na[key] = nd.outputs["Attribute"]
    er = nodes.new("FunctionNodeEulerToRotation")
    links.new(gi.outputs[0], m2p.inputs["Mesh"])
    links.new(m2p.outputs[0], iop.inputs["Points"])
    links.new(ci.outputs[0], iop.inputs["Instance"])
    iop.inputs["Pick Instance"].default_value = True
    links.new(na["look_pick"], iop.inputs["Instance Index"])
    links.new(na["look_rot"], er.inputs[0])
    links.new(er.outputs[0], iop.inputs["Rotation"])
    links.new(na["look_scl"], iop.inputs["Scale"])
    links.new(iop.outputs[0], go.inputs[0])
    mod = ob.modifiers.new("look_instances", "NODES")
    mod.node_group = tree
    return ob


def proto_collection(name: str, obs: list[bpy.types.Object]) -> bpy.types.Collection:
    col = bpy.data.collections.new(name)
    tag(col)
    for o in sorted(obs, key=lambda o: o.name):
        col.objects.link(o)
    return col


def look_collection(name: str) -> bpy.types.Collection:
    col = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    tag(col)
    if col.name not in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.link(col)
    return col


# ── layout material classification ──────────────────────────────────────────────────────────────────────────────
def classify(ob: bpy.types.Object, mats: list[bpy.types.Material], frame_c: bj.Frame) -> None:
    me = ob.data
    if not len(me.polygons):
        return
    nrm, cen, fv = face_arrays(me)
    nz = nrm[:, 2]
    zc = cen[:, 2]
    col = ob.users_collection[0].name
    name = ob.name
    idx = np.full(len(nz), M["PLASTER"], np.int32)
    up, slope, down = nz > 0.97, (nz > 0.15) & (nz <= 0.97), nz < -0.5
    vert = ~(up | slope | down)

    def generic(wall: str = "PLASTER", roof_m: str = "ROOF", base_z: float = Z + 0.6) -> np.ndarray:
        out = np.full(len(nz), M[wall], np.int32)
        out[up & (zc <= Z + 0.35)] = M["EARTH"]
        out[up & (zc > Z + 0.35) & (zc <= Z + 2.6)] = M["STONE"]
        out[up & (zc > Z + 2.6)] = M[roof_m]
        out[slope] = M[roof_m]
        out[down] = M["TIMBER"]
        out[vert & (zc < base_z)] = M["BRICK"]
        return out

    def gate(wall_top: float) -> np.ndarray:
        out = np.full(len(nz), M["RAMMED"], np.int32)
        hi_ = zc > wall_top + 0.3
        out[hi_ & (up | slope)] = M["ROOF"]
        out[hi_ & vert] = M["RED"]
        out[hi_ & down] = M["TIMBER"]
        return out

    lname = name.lower()
    if col == "G_GROUND":
        idx[:] = M["GROUND"]
    elif "water" in lname:
        idx[:] = M["WATER"]
    elif lname.endswith("_bed") or "_bed_" in lname:
        idx[:] = M["RIVERBED"]
    elif "moat_bridges" in name:
        idx[:] = M["TIMBER"]
    elif col == "G_YARDS" and "garden" in name:
        idx[:] = M["FIELD"]                                     # 菜园 / 空地
    elif col == "G_YARDS" and "yardwalls" in name:
        idx = np.where(up | slope, M["ROOF"], np.where(zc < Z + 0.6, M["BRICK"], M["PLASTER"])).astype(np.int32)   # 院墙：青砖墙根、白灰墙身、瓦顶
    elif col in ("J_GROUND",) or name == "J_114_ridges":
        idx[:] = M["FIELD"]
    elif col.endswith(("_GROUND", "_STREET")) or col == "J_ROAD" or name.startswith("G_40") and "yujie" not in name:
        idx[:] = M["EARTH"]
        if name in ("D_56_stone_bridge",):
            idx[:] = M["STONE"]
        if name == "I_107_plank_bridge":
            idx[:] = M["TIMBER"]
    elif col in ("G_WALL", "B_WALL"):
        idx[:] = M["RAMMED"]
    elif col == "G_GATES":
        idx = gate(Z + bj.WALL_H)
    elif col == "B_GATES":
        idx = gate(Z + bj.WALL_H) if "tower" in name else np.full(len(nz), M["RAMMED" if "madao" in name else "TIMBER"], np.int32)
    elif name.startswith("B_25"):
        idx[:] = M["TIMBER"]
    elif col == "C_ZHOUQIAO":
        idx[:] = M["STONE"]
    elif col in ("C_CHAZI", "D_CHAZI"):
        idx[:] = M["BLACK" if name.startswith("C_34") else "RED"]
    elif col == "C_DITCH":
        idx[:] = np.where(up, M["WATER"], M["STONE"])
    elif col == "C_GALLERY":
        idx = np.where(up & (zc > Z + 3.0), M["ROOF"], np.where(up, M["STONE"], M["TIMBER"])).astype(np.int32)
    elif col in ("A_POLES", "I_FENCE", "E_DOCK") and name != "E_71_quay":
        idx[:] = M["TIMBER"]
    elif name in ("A_12_quay", "E_71_quay", "C_40_well") or col == "F_COURT" and "stones" in name:
        idx[:] = M["STONE"]
    elif name == "A_12_timber_step":
        idx[:] = M["TIMBER"]
    elif col == "I_SHED":
        idx = np.where(slope | up, M["REED"], np.where(vert & (zc > Z + 0.2), M["REED"], M["TIMBER"])).astype(np.int32)
    elif name == "J_115_farms":
        idx = generic("RAMMED", "REED")
    elif name == "J_112_mound" or name == "G_517_lm":
        idx[:] = M["EARTH"]
    elif name in ("G_518_lm", "G_519_lm", "G_520_lm"):
        idx = np.where(up, M["EARTH"], M["BRICK"]).astype(np.int32)
    elif name in ("G_521_lm", "G_522_lm"):
        idx = np.where(slope | up, M["ROOF"], M["BRICK"]).astype(np.int32)
    elif col == "D_DUN":
        idx = np.full(len(nz), M["GILT" if "nails" in name else ("RED" if "leaves" in name else "BRICK")], np.int32)
        if name == "D_51_dun":
            idx[up] = M["STONE"]
    elif col in ("D_MENLOU", "D_QUE"):
        idx = generic("RED", "GLAZED", base_z=Z + 12.3 if col == "D_QUE" else Z + 0.6)
    elif col in ("D_COURT", "D_HALL", "F_GATE") or name in ("F_86_zhengting", "F_87_0_rear_hall", "F_87_1_rear_hall",
                                                              "H_91_east_gate", "H_92_sanmen", "H_93_main_hall", "H_94_zisheng_gate",
                                                              "G_103_palace_halls"):
        idx = generic("RED")
    elif col in ("D_WALL",):
        idx[:] = M["BRICK"]
    elif col == "C_ZHENGDIAN" or name == "C_39_fire_tower":
        idx = generic("TIMBER")
    elif col == "G_STREETS":
        idx = streets_ext(ob, nz, zc, fv, frame_c)
    else:
        idx = generic()
    me.materials.clear()
    set_slots(me, mats)
    me.polygons.foreach_set("material_index", idx.astype(np.int32))
    me["look_slots"] = 1


def streets_ext(ob: bpy.types.Object, nz: np.ndarray, zc: np.ndarray, fv: np.ndarray, fc: bj.Frame) -> np.ndarray:
    """G_4011_yujie_*: 朱 / 黑杈子 posts, 御沟 trees (hidden later), 御廊 floor / columns / roof slab."""
    co, starts = islands(ob.data)
    isl = np.searchsorted(starts, fv, side="right") - 1
    lx = np.array([fc.local(float(c[0]), float(c[1]))[0] for c in co[starts]], np.float32)
    red = float(bj.re.search(rf"x=±({bj.NUM})", bj.row_of("C", 33).where).group(1))
    black = float(bj.re.search(rf"x=±({bj.NUM})", bj.row_of("C", 34).where).group(1))
    sizes = np.diff(np.append(starts, len(co)))
    out = np.full(len(nz), M["TIMBER"], np.int32)
    fl = np.abs(lx[isl])
    small = sizes[isl] == 8
    out[small & (np.abs(fl - red) < 1.0)] = M["RED"]
    out[small & (np.abs(fl - black) < 1.0)] = M["BLACK"]
    out[(nz > 0.97) & (zc > Z + 3.0)] = M["ROOF"]
    out[(nz > 0.97) & (zc <= Z + 0.6)] = M["STONE"]
    return out


# ── hip roofs → curved roofs with brackets; gate tower boxes → timber towers ───────────────────────────────────────
class FrameMB:
    """Draw into an MB inside a rectangle frame: centre c, long axis u, short axis v (unit vectors), z absolute."""

    def __init__(self, mb: MB, c: Vector, u: Vector, v: Vector) -> None:
        self.mb, self.c, self.u, self.v = mb, c, u, v

    def P(self, x: float, y: float, z: float) -> tuple[float, float, float]:
        p = self.c + self.u * x + self.v * y
        return (p.x, p.y, z)

    def box(self, x0: float, x1: float, y0: float, y1: float, z0: float, z1: float, mat: str) -> None:
        P = self.P
        c = {k: P(x, y, z) for k, (x, y, z) in {
            "000": (x0, y0, z0), "100": (x1, y0, z0), "110": (x1, y1, z0), "010": (x0, y1, z0),
            "001": (x0, y0, z1), "101": (x1, y0, z1), "111": (x1, y1, z1), "011": (x0, y1, z1)}.items()}
        for f in (("000", "010", "110", "100"), ("001", "101", "111", "011"), ("000", "100", "101", "001"),
                  ("110", "010", "011", "111"), ("010", "000", "001", "011"), ("100", "110", "111", "101")):
            self.mb.face([c[k] for k in f], mat)


def rect_frame(pts: np.ndarray) -> tuple[Vector, Vector, Vector, float, float]:
    """4 base corners in ring order → centre, long axis, short axis, half long, half short."""
    q = [Vector((float(p[0]), float(p[1]), 0.0)) for p in pts[:4]]
    e1, e2 = q[1] - q[0], q[3] - q[0]
    c = (q[0] + q[2]) / 2
    if e1.length >= e2.length:
        u, v, a, b = e1.normalized(), e2.normalized(), e1.length / 2, e2.length / 2
    else:
        u, v, a, b = e2.normalized(), e1.normalized(), e2.length / 2, e1.length / 2
    return c, u, v, a, b


def curved_hip(fm: FrameMB, a: float, b: float, z0: float, h: float, mat: str) -> None:
    """歇山/庑殿 roof: concave slopes, corner upturn (起翘), hip ridges, main ridge with 鸱吻, eave fascia, soffit."""
    r = max(0.0, a - b)
    up = min(0.45, 0.025 * b + 0.05)      # 场景卡：屋脊平直、檐角只微微起翘，禁「飞檐翘角过甚」（bg1 / bg7 / bg12 / bg13）
    rows, cols = 6, 10

    def surf(t: float, s: float, side: str) -> tuple[float, float, float]:
        # side faces: long (±v) param s∈[-1,1] along u; short (±u) param s along v
        zc = z0 + h * t ** 1.3
        if side in ("+v", "-v"):
            x = s * (a + (r - a) * t)
            y = (b * (1 - t)) * (1 if side == "+v" else -1)
            corner = abs(s)
        else:
            x = (a + (r - a) * t) * (1 if side == "+u" else -1)
            y = s * b * (1 - t)
            corner = abs(s)
        return fm.P(x, y, zc + up * (1 - t) ** 2 * corner ** 4)

    for side in ("+v", "-v", "+u", "-u"):
        grid = [[surf(i / rows, -1 + 2 * j / cols, side) for j in range(cols + 1)] for i in range(rows + 1)]
        flip = side in ("-v", "+u")
        for i in range(rows):
            for j in range(cols):
                q = [grid[i][j], grid[i][j + 1], grid[i + 1][j + 1], grid[i + 1][j]]
                fm.mb.face(list(reversed(q)) if flip else q, mat)
                qd = [(p[0], p[1], p[2] - 0.25) for p in q]
                fm.mb.face(qd if flip else list(reversed(qd)), "TIMBER")
        for j in range(cols):
            e0, e1 = grid[0][j], grid[0][j + 1]
            fm.mb.face([e0, e1, (e1[0], e1[1], e1[2] - 0.35), (e0[0], e0[1], e0[2] - 0.35)], "RED" if mat == "GLAZED" else "TIMBER")
        rid = [Vector(grid[i][0]) for i in range(rows + 1)]
        fm.mb.tube(rid, [0.05 * b + 0.08] * len(rid), 6, mat, cap=False)
    zr = z0 + h
    if r > 0.3:
        fm.box(-r - 0.2, r + 0.2, -0.12 * b - 0.1, 0.12 * b + 0.1, zr - 0.1, zr + 0.1 * h + 0.2, mat)
        for sx in (-1, 1):
            w = 0.06 * b + 0.1
            fm.box(sx * r - w, sx * r + w, -0.05 * b - 0.05, 0.05 * b + 0.05, zr, zr + 0.14 * h + 0.25, mat)
            fm.box(sx * (r - w * 1.6) - w * 0.6, sx * (r - w * 1.6) + w * 0.6, -0.04 * b - 0.04, 0.04 * b + 0.04,
                   zr + 0.1 * h, zr + 0.2 * h + 0.3, mat)
    n_side = max(2, int(2 * (a - 1.0) / 1.15))
    zb = z0 - 0.05
    bracket = "RED" if mat == "GLAZED" else "TIMBER"     # world.md §8：朱漆只四处，普通殿宇斗拱素木
    for sgn in (-1, 1):
        fm.box(-(a - 0.9), a - 0.9, sgn * (b - 0.9) - 0.25, sgn * (b - 0.9) + 0.25, zb - 0.9, zb, "TIMBER")
        for k in range(n_side + 1):
            x = -(a - 0.9) + 2 * (a - 0.9) * k / n_side
            fm.box(x - 0.18, x + 0.18, sgn * (b - 0.9) - 0.5, sgn * (b - 0.9) + 0.5, zb - 0.55, zb - 0.15, bracket)
    n_end = max(1, int(2 * (b - 1.0) / 1.15))
    for sgn in (-1, 1):
        fm.box(sgn * (a - 0.9) - 0.25, sgn * (a - 0.9) + 0.25, -(b - 0.9), b - 0.9, zb - 0.9, zb, "TIMBER")
        for k in range(n_end + 1):
            y = -(b - 0.9) + 2 * (b - 0.9) * k / n_end
            fm.box(sgn * (a - 0.9) - 0.5, sgn * (a - 0.9) + 0.5, y - 0.18, y + 0.18, zb - 0.55, zb - 0.15, bracket)


def timber_tower(fm: FrameMB, a: float, b: float, z0: float, z1: float) -> None:
    """城楼 body on a wall top: plank floor + balcony, lacquered columns, lattice walls with doors, architrave."""
    fm.box(-a - 0.9, a + 0.9, -b - 0.9, b + 0.9, z0, z0 + 0.3, "TIMBER")
    zf = z0 + 0.3
    for sx, sy, lx_, ly_ in ((0, 1, a + 0.9, 0.0), (0, -1, a + 0.9, 0.0), (1, 0, 0.0, b + 0.9), (-1, 0, 0.0, b + 0.9)):
        if sy:
            fm.box(-lx_, lx_, sy * (b + 0.85) - 0.05, sy * (b + 0.85) + 0.05, zf + 0.95, zf + 1.05, "RED")
            for k in range(int(2 * lx_ / 1.2) + 1):
                x = -lx_ + k * 1.2
                fm.box(x - 0.05, x + 0.05, sy * (b + 0.85) - 0.05, sy * (b + 0.85) + 0.05, zf, zf + 1.05, "RED")
        else:
            fm.box(sx * (a + 0.85) - 0.05, sx * (a + 0.85) + 0.05, -ly_, ly_, zf + 0.95, zf + 1.05, "RED")
            for k in range(int(2 * ly_ / 1.2) + 1):
                y = -ly_ + k * 1.2
                fm.box(sx * (a + 0.85) - 0.05, sx * (a + 0.85) + 0.05, y - 0.05, y + 0.05, zf, zf + 1.05, "RED")
    top = z1 - 0.1
    nx, ny = max(2, round(2 * a / 3.6)), max(1, round(2 * b / 3.6))
    for k in range(nx + 1):
        x = -a + 2 * a * k / nx
        for y in (-b, b):
            fm.box(x - 0.2, x + 0.2, y - 0.2, y + 0.2, zf, top, "RED")
    for k in range(1, ny):
        y = -b + 2 * b * k / ny
        for x in (-a, a):
            fm.box(x - 0.2, x + 0.2, y - 0.2, y + 0.2, zf, top, "RED")
    wall_top = top - 0.6
    fm.box(-a + 0.2, a - 0.2, -b + 0.35, b - 0.35, zf, wall_top, "WINDOW")
    for k in range(nx):
        xc = -a + 2 * a * (k + 0.5) / nx
        w = 2 * a / nx - 0.4
        for y in (-b + 0.3, b - 0.3):
            for m in range(9):                      # 直棂窗：只有竖棂（bg2）
                x = xc - w / 2 + w * m / 8
                fm.box(x - 0.04, x + 0.04, y - 0.04, y + 0.04, zf + 0.2, wall_top, "TIMBER")
    fm.box(-a - 0.25, a + 0.25, -b - 0.25, b + 0.25, top - 0.6, top, "RED")


def upgrade_structures(ob: bpy.types.Object, mats: list[bpy.types.Material]) -> int:
    """Replace Batch.hip islands (5 / 6 verts, 4-corner base ring) and, in gate meshes, the tower box under a hip."""
    me = ob.data
    co, starts = islands(me)
    sizes = np.diff(np.append(starts, len(co)))
    _n, _c, fv = face_arrays(me)
    isl_of_face = np.searchsorted(starts, fv, side="right") - 1
    idx = np.empty(len(fv), np.int32)
    me.polygons.foreach_get("material_index", idx)
    col = ob.users_collection[0].name if ob.users_collection else ""
    is_gate = col in ("G_GATES",) or (col == "B_GATES" and "tower" in ob.name)
    mb = MB()
    replaced: list[int] = []
    for i, (s, n) in enumerate(zip(starts, sizes)):
        if n not in (5, 6):
            continue
        pts = co[s:s + n]
        base = pts[:4]
        if np.ptp(base[:, 2]) > 1e-3 or pts[4:, 2].min() <= base[0, 2] + 0.2:
            continue
        c, u, v, a, b = rect_frame(base)
        if b < 1.2:
            continue
        faces_i = np.nonzero(isl_of_face == i)[0]
        cur = MAT_NAMES[int(idx[faces_i[0]])] if len(faces_i) else "ROOF"
        mat = cur if cur in ("GLAZED", "REED") else "ROOF"
        z0 = float(base[0, 2])
        curved_hip(FrameMB(mb, c, u, v), a, b, z0, float(pts[4:, 2].max()) - z0, mat)
        replaced.append(i)
        if is_gate and i > 0 and sizes[i - 1] == 8:
            box = co[starts[i - 1]:starts[i - 1] + 8]
            bc, bu, bv, ba, bb = rect_frame(box[:4])
            zlo, zhi = float(box[:, 2].min()), float(box[:, 2].max())
            if zlo > Z + bj.WALL_H - 1.0 and zhi <= z0 + 0.05:
                timber_tower(FrameMB(mb, bc, bu, bv), ba, bb, zlo, zhi)
                replaced.append(i - 1)
    if not replaced:
        mb.bm.free()
        return 0
    idx[np.isin(isl_of_face, np.array(replaced))] = M["INVISIBLE"]
    me.polygons.foreach_set("material_index", idx)
    up = mb.finish(f"LOOK_up_{ob.name}", mats)
    up.matrix_world = ob.matrix_world.copy()
    look_collection("LOOK_CITY").objects.link(up)
    return len(replaced)


# ── dress / undress ─────────────────────────────────────────────────────────────────────────────────────────────
TREE_OBJECTS = ("A_14_willow_N", "A_14_willow_S", "B_27_trees", "C_35_trees_E", "C_35_trees_W", "E_76_willows",
                "J_113_willows", "J_116_big_willow", "G_20000_suburb_willows")
MIXED_TREE_OBJECTS = ("G_4011_yujie_E", "G_4011_yujie_W", "G_524_lm")


def is_tree_object(ob: bpy.types.Object) -> bool:
    return ob.name.endswith(("_trees", "_willows"))
PLACE_PROTOS = {"p8": "PROTO_p8_PROXY", "p9": "PROTO_p9_PROXY", "p10": "PROTO_p10_PROXY", "p10a": "PROTO_p10a_PROXY"}


def undress() -> None:
    for ob in list(bpy.data.objects):
        if ob.get("look"):
            bpy.data.objects.remove(ob)
        elif ob.get("look_hidden"):
            ob.hide_render = False
            del ob["look_hidden"]
    for me in bpy.data.meshes:
        if me.get("look_slots"):
            me.materials.clear()
            me.polygons.foreach_set("material_index", np.zeros(len(me.polygons), np.int32))
            del me["look_slots"]
    for coll in (bpy.data.collections, bpy.data.materials, bpy.data.node_groups, bpy.data.images, bpy.data.lights,
                 bpy.data.cameras, bpy.data.worlds):
        for idb in list(coll):
            if idb.get("look"):
                coll.remove(idb)
    bpy.data.orphans_purge(do_recursive=True)


def hide(ob: bpy.types.Object) -> None:
    ob.hide_render = True
    ob["look_hidden"] = 1


def city_quad() -> list[tuple[float, float]]:
    ob = bpy.data.objects["G_101_wall_外城"]
    pts = [(v.co.x, v.co.y) for v in ob.data.vertices]
    hull = [pts[i] for i in convex_hull_2d(pts)]
    corners = [max(hull, key=lambda p: sx * p[0] + sy * p[1]) for sx, sy in ((1, -1), (1, 1), (-1, 1), (-1, -1))]
    return corners


def dress(log=print) -> dict[str, int]:
    undress()
    md = bj.PLAN_MD.read_text(encoding="utf-8")
    if not bj.ROWS:
        bj.ROWS[:] = bj.parse_plan(md)
        bj.load_w11()
    pal = sample_palette()
    mats = build_materials(pal, city_quad())
    log("look: palette " + ", ".join(f"{k}=({v[0]:.3f},{v[1]:.3f},{v[2]:.3f})" for k, v in pal.items()))

    frame_c = bj.FRAMES["C"]
    layout = [o for o in bpy.context.scene.objects if o.type == "MESH" and not o.get("look")
              and o.users_collection and o.users_collection[0].name not in ("G_BLOCKS",)]
    for ob in layout:
        classify(ob, mats, frame_c)
    log(f"look: classified {len(layout)} layout meshes")
    skip_up = set(TREE_OBJECTS) | {o.name for o in bpy.data.collections["G_SUBURBS"].objects}
    n_up = sum(upgrade_structures(ob, mats) for ob in layout if ob.name not in skip_up)
    log(f"look: upgraded {n_up} roofs / gate towers")

    counts: dict[str, int] = {}
    # place protos
    for key, cname in PLACE_PROTOS.items():
        col = bpy.data.collections.get(cname)
        if col is None:
            continue
        for o in col.objects:
            if not o.get("look"):
                hide(o)
        if key == "p8":
            det = bridge_object(mats)
        elif key == "p9":
            det = house_object("LOOK_p9_shop", [(-0.5, 3.5, -3.75, 2.25, 5.4, 7.0)], "tall", 2, 9, mats, p9_extra)
        elif key == "p10":
            det = house_object("LOOK_p10_row", p10_parts(), "tile", 2, 10, mats, p10_extra)
        else:
            det = house_object("LOOK_p10a_house", [(-2.0, 2.0, -2.5, 2.5, 2.7, 4.3)], "tile", 2, 11, mats)
        col.objects.link(det)
    # block / suburb house prototypes (pick index ↔ sorted name)
    # follow-up 008：房子大小高低有别——原型按「面宽档 × 层数 × 式样」分，实例只做小幅缩放，不把一种房拉成所有尺寸
    WIDTHS = {"w4": (4.0, 4.5), "w8": (8.0, 7.0), "w12": (12.0, 9.0), "w18": (18.0, 11.0)}   # 面宽档：(面宽, 进深)
    STOREYS = {1: 5.5, 2: 8.5, 3: 12.0}                                                     # 层数：脊高 m
    protos: list[bpy.types.Object] = []
    pick_of: dict[tuple[str, int, int, str], int] = {}
    for wk, (lx, ly) in WIDTHS.items():
        for storey, h in STOREYS.items():
            styles = ("tile", "shop", "thatch") if storey == 1 else ("tall", "shop")
            for st in styles:
                for lod in (1, 2):
                    eave = h * (0.63 if storey == 1 else 0.76)
                    parts = [(-lx / 2, lx / 2, -ly / 2, ly / 2, eave, h)]
                    if wk == "w18" and storey == 1 and st != "thatch":          # 宽屋：明间高、次间低（三段屋面）
                        w3 = lx / 3
                        parts = [(-lx / 2 + w3 * i, -lx / 2 + w3 * (i + 1), -ly / 2, ly / 2, eave * (1.0 if i == 1 else 0.8), h * (1.0 if i == 1 else 0.82))
                                 for i in range(3)]
                    name = f"LOOK_H{len(protos):02d}_{wk}_S{storey}_{st}_L{lod}"
                    protos.append(house_object(name, parts, st, lod, len(protos) * 7 + 3, mats))
                    pick_of[(wk, storey, lod, st)] = len(protos) - 1
    house_protos = proto_collection("LOOK_PROTO_HOUSES", protos)

    def proto_for(d: tuple[float, float, float], lod: int, rng: random.Random, thatch: float, shop: float) -> tuple[int, tuple[float, float, float]]:
        wk = min(WIDTHS, key=lambda k: abs(WIDTHS[k][0] - d[0]))
        storey = 1 if d[2] < 7.0 else (2 if d[2] < 10.5 else 3)
        if storey == 1:
            st = "thatch" if rng.random() < thatch else ("shop" if rng.random() < shop else "tile")
        else:
            st = "shop" if rng.random() < max(shop, 0.4) else "tall"
        lx, ly = WIDTHS[wk]
        return pick_of[(wk, storey, lod, st)], (d[0] / lx, d[1] / ly, d[2] / STOREYS[storey])

    pts = []
    all_units: list[Unit] = []
    for ob in list(bpy.data.collections["G_BLOCKS"].objects):
        level = ob.get("bj_level", "C")
        rng = random.Random(int(ob.get("bj_row", 0)))
        units = house_units(ob)
        all_units.extend(units)
        for u in units:
            # 城内零草顶（bg0 / bg7）；只有贫户小棚（面宽 < 5.5 m 且单层）偶见草顶
            thatch = 0.25 if (u.dims[0] < 5.5 and u.dims[2] < 4.5) else 0.0
            pick, sc = proto_for(u.dims, 2 if level == "B" else 1, rng, thatch, 0.25 if u.dims[1] >= 9.0 else 0.08)
            pts.append((u.loc, u.yaw, ((-1 if u.mirror else 1) * sc[0], sc[1], sc[2]), pick))
        hide(ob)
    for ob in list(bpy.data.collections["G_SUBURBS"].objects):
        if is_tree_object(ob):
            continue
        rng = random.Random(int(ob.get("bj_row", 0)))
        thatch = 0.75 if "hamlet" in ob.name else (0.2 if "guanxiang" in ob.name else 0.3)   # bg8 村舍草顶；关厢多瓦房
        for u in house_units(ob):
            all_units.append(u)
            pick, sc = proto_for(u.dims, 2, rng, thatch, 0.1)
            pts.append((u.loc, u.yaw, ((-1 if u.mirror else 1) * sc[0], sc[1], sc[2]), pick))
        hide(ob)
    looks = look_collection("LOOK_CITY")
    instancer("LOOK_houses", looks, house_protos, pts)
    counts["houses"] = len(pts)

    willows = proto_collection("LOOK_PROTO_WILLOWS", [willow_object(f"LOOK_W{i}_willow", 100 + i, mats) for i in range(5)])
    trees: list[Tree] = []
    blossoms: list[Tree] = []
    suburb_trees = tuple(o.name for c in ("G_SUBURBS", "G_YARDS") if bpy.data.collections.get(c)
                         for o in bpy.data.collections[c].objects if is_tree_object(o) and o.name not in TREE_OBJECTS)
    for name in TREE_OBJECTS + MIXED_TREE_OBJECTS + suburb_trees:
        ob = bpy.data.objects.get(name)
        if ob is None:
            continue
        found, hide_ids = tree_islands(ob)
        (blossoms if name in BLOSSOM_SOURCES else trees).extend(found)
        if name in TREE_OBJECTS or name in suburb_trees:
            hide(ob)
        elif hide_ids:
            co, starts = islands(ob.data)
            _n, _c, fv = face_arrays(ob.data)
            isl = np.searchsorted(starts, fv, side="right") - 1
            idx = np.empty(len(fv), np.int32)
            ob.data.polygons.foreach_get("material_index", idx)
            idx[np.isin(isl, np.array(sorted(hide_ids)))] = M["INVISIBLE"]
            ob.data.polygons.foreach_set("material_index", idx)
    rng = random.Random(7)
    tpts = [(t.base, rng.uniform(0, 2 * math.pi), (t.crown / 3.2 * 1.1, t.crown / 3.2 * 1.1, max(0.5, t.height / 8.0)), rng.randrange(5))
            for t in trees]
    instancer("LOOK_trees", looks, willows, tpts)
    counts["trees"] = len(tpts)
    fruit = proto_collection("LOOK_PROTO_BLOSSOMS", [blossom_object(f"LOOK_B{i}_blossom", 300 + i, mats) for i in range(4)])
    bpts = [(t.base, rng.uniform(0, 2 * math.pi), (t.crown / 3.2 * 1.3, t.crown / 3.2 * 1.3, max(0.5, t.height / 8.0 * 1.2)), rng.randrange(4))
            for t in blossoms]
    instancer("LOOK_blossoms", looks, fruit, bpts)
    counts["blossoms"] = len(bpts)
    counts["people"] = build_people(looks, mats, all_units)
    setup_world()
    log(f"look: {counts}")
    return counts


# ── static townsfolk (follow-up 007: 城里城外到处有人) ───────────────────────────────────────────────────────────
PEOPLE_CLOTH = ("CLOTH_UNDYED", "WINDOW", "CLOTH_BLUE", "CLOTH_UNDYED")     # 平民衣本白 / 皂黑 / 灰青（style_guide §2）


def build_people(col: bpy.types.Collection, mats: list[bpy.types.Material], units: list[Unit]) -> int:
    """W11 街道两侧行人 + 各户门前三三两两。细节 Place 足迹内不放——那里的人由 shot previz 自己编排。
    只进写实渲染：build_bianjing / previz_sk1 的灰模 previz 把 LOOK_people 设为 hide_render。"""
    protos = [figure_object(f"LOOK_P{i}_person", "haul" if i == 3 else "walk", mats, cloth) for i, cloth in enumerate(PEOPLE_CLOTH)]
    pcol = proto_collection("LOOK_PROTO_PEOPLE", protos)
    rng = random.Random(77)
    pts: list[tuple[Vector, float, tuple[float, float, float], int]] = []

    def add(x: float, y: float, z: float, yaw: float) -> None:
        if bj.in_any_place((x, y), 10.0):
            return
        s = rng.uniform(0.92, 1.06)
        pts.append((Vector((x, y, z)), yaw, (s, s, s), rng.randrange(len(protos))))

    for st in bj.load_w11()["street"]:
        sp = [(float(p[0]), float(p[1])) for p in st["points"]]
        wd = float(st["width_m"])
        for (ax, ay), (bx, by) in zip(sp, sp[1:]):
            ln = math.hypot(bx - ax, by - ay)
            if ln < 1.0:
                continue
            tx, ty = (bx - ax) / ln, (by - ay) / ln
            s = 0.0
            while s < ln:
                s += rng.uniform(3.0, 8.0)
                for side in (-1, 1):
                    if rng.random() > 0.55:
                        continue
                    off = rng.uniform(24.0, wd / 2 - 8.0) if wd > 100 else rng.uniform(1.0, max(1.5, wd / 2 - 1.0))   # 御街：御道里无人
                    add(ax + tx * s - ty * side * off, ay + ty * s + tx * side * off, Z + bj.STREET_H,
                        math.atan2(ty, tx) - math.pi / 2 + (math.pi if rng.random() < 0.5 else 0.0))
    for u in units:
        if rng.random() > 0.1:
            continue
        fx, fy = -math.sin(u.yaw), math.cos(u.yaw)
        d = u.dims[1] / 2 + rng.uniform(1.0, 3.5)
        side = rng.uniform(-u.dims[0] / 2, u.dims[0] / 2)
        add(u.loc.x + fx * d + math.cos(u.yaw) * side, u.loc.y + fy * d + math.sin(u.yaw) * side, Z, rng.uniform(0, 2 * math.pi))
    instancer("LOOK_people", col, pcol, pts)
    return len(pts)


def show_people(show: bool) -> None:
    ob = bpy.data.objects.get("LOOK_people")
    if ob is not None:
        ob.hide_render = not show


# ── world, sun, render ──────────────────────────────────────────────────────────────────────────────────────────
SUN_ELEV = 22.0       # 卯时偏晚：14° 时平地几乎只吃蓝天补光、整片发紫灰（2026-09-15 实测），抬到 22° 仍是清晨长影
SUN_AZ = 10.0         # 0 ＝ 正东（+X），逆时针；清明前后日出偏北
# 不用世界体积雾：无限远的太阳穿过无限大的体积会被完全吸收，整张图全黑（2026-09-15 实测）；follow-up 004 本来也要通透无霾
FAR_GROUND_HALF = 1500000.0


def far_ground() -> None:
    """全城地面（G_EXTENT）之外的一圈远郊田野，免得高空机位看见地面尽头。"""
    x0, x1, y0, y1 = bj.G_EXTENT
    r = FAR_GROUND_HALF
    z = Z - 0.02
    verts = [(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z), (-r, -r, z), (r, -r, z), (r, r, z), (-r, r, z)]
    faces = [(4, 5, 1, 0), (5, 6, 2, 1), (6, 7, 3, 2), (7, 4, 0, 3)]
    me = bpy.data.meshes.new("LOOK_far_ground")
    me.from_pydata(verts, [], faces)
    set_slots(me, [bpy.data.materials["LOOK_GROUND"]])
    ob = bpy.data.objects.new("LOOK_far_ground", me)
    tag(ob)
    look_collection("LOOK_CITY").objects.link(ob)


def sun_vector(elev: float, az: float) -> Vector:
    e, a = math.radians(elev), math.radians(az)
    return Vector((math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)))


def setup_world(elev: float = SUN_ELEV, az: float = SUN_AZ) -> None:
    sc = bpy.context.scene
    world = bpy.data.worlds.new("LOOK_WORLD")
    tag(world)
    world.use_nodes = True
    nt = world.node_tree
    nt.nodes.clear()
    sky = nt.nodes.new("ShaderNodeTexSky")
    sky.sky_type = "MULTIPLE_SCATTERING"
    sky.sun_disc = False
    sky.sun_elevation = math.radians(elev)
    sky.sun_rotation = math.radians(90.0 - az)
    sky.altitude = 100.0
    sky.air_density = 1.0
    sky.aerosol_density = 0.4
    sky.ozone_density = 1.0
    bg = nt.nodes.new("ShaderNodeBackground")
    bg.inputs["Strength"].default_value = 0.12
    out = nt.nodes.new("ShaderNodeOutputWorld")
    nt.links.new(sky.outputs["Color"], bg.inputs["Color"])
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])
    sc.world = world
    far_ground()

    light = bpy.data.lights.new("LOOK_SUN", "SUN")
    tag(light)
    light.energy = 4.6
    light.angle = math.radians(0.55)
    light.color = (1.0, 0.84, 0.66)
    sun = bpy.data.objects.new("LOOK_SUN", light)
    tag(sun)
    look_collection("LOOK_CITY").objects.link(sun)
    sun.rotation_euler = (-sun_vector(elev, az)).to_track_quat("-Z", "Y").to_euler()

    sc.render.engine = "CYCLES"
    cy = sc.cycles
    cy.device = "GPU"
    cy.samples = 96
    cy.use_adaptive_sampling = True
    cy.use_denoising = True
    cy.max_bounces = 5
    cy.diffuse_bounces = 3
    cy.glossy_bounces = 3
    cy.transparent_max_bounces = 16
    cy.sample_clamp_indirect = 8.0
    try:
        sc.view_settings.view_transform = "AgX"
        sc.view_settings.look = "AgX - Medium High Contrast"
    except TypeError:
        pass
    sc.view_settings.exposure = -0.4
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1920, 1080, 100


def enable_gpu() -> None:
    prefs = bpy.context.preferences.addons["cycles"].preferences
    for kind in ("OPTIX", "CUDA"):
        try:
            prefs.compute_device_type = kind
            prefs.get_devices()
            if any(d.type == kind for d in prefs.devices):
                for d in prefs.devices:
                    d.use = d.type == kind
                return
        except TypeError:
            continue


# ── stills ──────────────────────────────────────────────────────────────────────────────────────────────────────
def world_of(spec: tuple) -> Vector:
    if spec[0] == "世界":
        return Vector(spec[1:])
    f = bj.FRAMES[spec[1]]
    x, y = f.world(spec[2], spec[3])
    return Vector((x, y, spec[4]))


VIEWS: dict[str, tuple[tuple, tuple, float]] = {
    "01_aerial_city": (("世界", 4700.0, -4300.0, 1900.0), ("世界", 200.0, 700.0, 0.0), 24.0),
    "08_aerial_se_corner": (("世界", 4700.0, -4450.0, 260.0), ("世界", 3300.0, -3000.0, 0.0), 24.0),
    "02_aerial_bianhe_hongqiao": (("Place", "A", 260.0, -60.0, 70.0), ("Place", "A", 0.0, 0.0, 4.0), 28.0),
    "03_hongqiao_river": (("Place", "A", 55.0, -1.0, 3.2), ("Place", "A", 0.0, 0.0, 4.2), 30.0),
    "04_hongqiao_bank": (("Place", "A", -32.0, -16.0, 3.8), ("Place", "A", 0.0, 1.0, 5.2), 26.0),
    "05_dongshuimen": (("Place", "B", 70.0, -26.0, 7.0), ("Place", "B", 0.0, 0.0, 9.0), 26.0),
    "06_yujie_xuandelou": (("世界", 90.0, 1000.0, 10.0), ("世界", 103.0, 1140.0, 32.0), 24.0),
    "07_city_blocks_low": (("世界", -520.0, 160.0, 90.0), ("世界", -140.0, 520.0, 0.0), 28.0),
}


def render_stills(names: list[str], out_dir: Path, samples: int) -> list[Path]:
    enable_gpu()
    sc = bpy.context.scene
    sc.cycles.samples = samples
    cam_data = bpy.data.cameras.new("LOOK_STILL_CAM")
    cam_data.clip_start, cam_data.clip_end, cam_data.sensor_width = 0.1, 2000000.0, 36.0
    cam = bpy.data.objects.new("LOOK_STILL_CAM", cam_data)
    look_collection("LOOK_CITY").objects.link(cam)
    sc.camera = cam
    im = sc.render.image_settings
    if hasattr(im, "media_type"):
        im.media_type = "IMAGE"
    im.file_format = "PNG"
    out = []
    for name in names:
        pos, look, lens = VIEWS[name]
        p, t = world_of(pos), world_of(look)
        cam.location = p
        cam.rotation_euler = (t - p).to_track_quat("-Z", "Y").to_euler()
        cam_data.lens = lens
        cam_data.clip_start = max(0.1, min(5.0, (p.z - Z) / 60.0))
        sc.render.filepath = str(out_dir / f"look_{name}.png")
        bpy.ops.render.render(write_still=True)
        out.append(Path(sc.render.filepath))
        print(f"STILL {sc.render.filepath}")
        sys.stdout.flush()
    bpy.data.objects.remove(cam)
    bpy.data.cameras.remove(cam_data)
    return out


def parse_args() -> argparse.Namespace:
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--save", action="store_true", help="dress the open blend and save it")
    ap.add_argument("--stills", default="", help="comma list of view names, or 'all'")
    ap.add_argument("--samples", type=int, default=96)
    ap.add_argument("--out", default=str(bj.BLENDER_DIR))
    ap.add_argument("--frames", default="", help="render the scene camera (e.g. a shot previz) at these frames with Cycles")
    ap.add_argument("--video", default="", help="render the scene camera's whole frame range with Cycles to this mp4 (blend on disk untouched)")
    ap.add_argument("--video-res", default="1280x720")
    a = ap.parse_args(argv)
    a.out = str(Path(a.out).resolve())    # Blender 把相对路径接到盘符根上（2026-09-15 实测写到了 C:\ai_videos）
    return a


def render_frames(frames: list[int], out_dir: Path, samples: int, prefix: str) -> None:
    """Cycles stills from the blend's own camera (shot previz blends keep their workbench mp4 settings on disk)."""
    show_people(True)
    enable_gpu()
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device, sc.cycles.samples, sc.cycles.use_denoising = "GPU", samples, True
    im = sc.render.image_settings
    if hasattr(im, "media_type"):
        im.media_type = "IMAGE"
    im.file_format = "PNG"
    for f in frames:
        sc.frame_set(f)
        sc.render.filepath = str(out_dir / f"{prefix}_f{f:04d}.png")
        bpy.ops.render.render(write_still=True)
        print(f"FRAME {sc.render.filepath}")
        sys.stdout.flush()


def main() -> int:
    a = parse_args()
    if a.save:
        dress()
        bpy.ops.wm.save_mainfile()
        print(f"LOOK SAVED {bpy.data.filepath}")
    if a.stills:
        names = list(VIEWS) if a.stills == "all" else [s.strip() for s in a.stills.split(",") if s.strip()]
        if not bj.FRAMES:
            bj.ROWS[:] = bj.parse_plan(bj.PLAN_MD.read_text(encoding="utf-8"))
            bj.load_w11()
        render_stills(names, Path(a.out), a.samples)
    if a.frames:
        prefix = Path(bpy.data.filepath).stem.replace("_previz", "") + "_look"
        render_frames([int(v) for v in a.frames.split(",")], Path(a.out), a.samples, prefix)
    if a.video:
        render_video(Path(a.video).resolve(), a.samples, a.video_res)
    return 0


def render_video(out: Path, samples: int, res: str) -> None:
    """写实版镜头视频（不是 previz 参考位用的灰模 mp4）：Cycles 逐帧渲染 → H.264。不存盘，blend 仍是 workbench 设置。"""
    show_people(True)
    enable_gpu()
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device, sc.cycles.samples, sc.cycles.use_denoising = "GPU", samples, True
    sc.cycles.use_adaptive_sampling = True
    sc.render.use_persistent_data = True
    w, h = (int(v) for v in res.lower().split("x"))
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = w, h, 100
    im = sc.render.image_settings
    if hasattr(im, "media_type"):
        im.media_type = "VIDEO"
    im.file_format = "FFMPEG"
    sc.render.ffmpeg.format, sc.render.ffmpeg.codec = "MPEG4", "H264"
    sc.render.ffmpeg.constant_rate_factor = "HIGH"
    sc.render.filepath = str(out)
    bpy.ops.render.render(animation=True)
    print(f"VIDEO {out}")
    sys.stdout.flush()


if __name__ == "__main__":
    import traceback
    try:
        code = main()
    except Exception:
        traceback.print_exc()
        code = 2
    sys.stdout.flush()
    sys.exit(code)
