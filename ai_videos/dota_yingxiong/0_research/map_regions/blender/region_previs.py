# -*- coding: utf-8 -*-
"""预演渲染（follow-up 244）：在 region_blockout 的原版数据布局上铺程序材质、水面、分阵营树形与实体代理，
只渲染配置里列出的机位，作为 Codex 重出时的图1（锁住机位、太阳方向与影子、地形水面、物体位置与真实尺度）。
营地不画外框与标桩，改放野怪体块；不出文字标注。

    blender -b --factory-startup --python region_previs.py -- previs.json
"""
from __future__ import annotations

import json
import math
import random
import sys
from pathlib import Path

import bmesh
import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
from region_blockout import MAP_MIN, Builder, load_config, sha256  # noqa: E402

SIDE_COLORS = {  # grass dark / light, dirt, rock
    "sentinel": ((0.10, 0.20, 0.05), (0.26, 0.38, 0.10), (0.33, 0.25, 0.15), (0.36, 0.35, 0.32)),
    "scourge": ((0.07, 0.07, 0.06), (0.20, 0.19, 0.15), (0.17, 0.14, 0.12), (0.22, 0.22, 0.24)),
    "river": ((0.09, 0.17, 0.06), (0.22, 0.30, 0.10), (0.30, 0.25, 0.17), (0.34, 0.33, 0.31)),
}


class Previs(Builder):
    def __init__(self, cfg: dict, root: Path):
        super().__init__(cfg, root)
        self.ramps: dict[str, bpy.types.Node] = {}
        self.rng = random.Random(244)
        self.tree_objs: list[tuple[list, float, float, float, float]] = []

    # ---------- materials ----------
    def noise_mat(self, name: str, a, b, scale: float = 0.08, rough: float = 0.9) -> bpy.types.Material:
        mt = bpy.data.materials.new(name)
        mt.use_nodes = True
        nt = mt.node_tree
        bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
        noise = nt.nodes.new("ShaderNodeTexNoise")
        noise.inputs["Scale"].default_value = scale
        noise.inputs["Detail"].default_value = 8.0
        coord = nt.nodes.new("ShaderNodeTexCoord")
        ramp = nt.nodes.new("ShaderNodeValToRGB")
        ramp.color_ramp.elements[0].color = (*a, 1)
        ramp.color_ramp.elements[1].color = (*b, 1)
        nt.links.new(coord.outputs["Object"], noise.inputs["Vector"])
        nt.links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
        nt.links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
        bsdf.inputs["Roughness"].default_value = rough
        mt.diffuse_color = (*b, 1)
        self.ramps[name] = ramp
        return mt

    def mat(self, name: str) -> bpy.types.Material:
        if name in self.mats:
            return self.mats[name]
        c = SIDE_COLORS["sentinel"]
        made = {"grass": lambda: self.noise_mat("grass", c[0], c[1], 0.05),
                "ramp": lambda: self.noise_mat("ramp", c[2], c[1], 0.08),
                "rock": lambda: self.noise_mat("rock", (0.18, 0.17, 0.16), c[3], 0.3, 0.95)}.get(name)
        if made:
            self.mats[name] = made()
            return self.mats[name]
        return super().mat(name)

    def blighted(self, X: float, Y: float) -> bool:
        return self.blight_at(X, Y) >= 0.5

    def blight_at(self, X: float, Y: float) -> float:
        """原版 w3e 枯萎地标志（0x20）在顶点间双线性插值，0 = 草地，1 = 天灾枯萎地。"""
        t = self.terrain
        fi, fj = (X - MAP_MIN) / 128, (Y - MAP_MIN) / 128
        i, j = int(math.floor(fi)), int(math.floor(fj))
        u, v = fi - i, fj - j
        f = lambda a, b: float(bool(t.flags[max(0, min(t.n - 1, b))][max(0, min(t.n - 1, a))] & 0x20))
        return (f(i, j) * (1 - u) + f(i + 1, j) * u) * (1 - v) + (f(i, j + 1) * (1 - u) + f(i + 1, j + 1) * u) * v

    def build_terrain(self) -> None:
        super().build_terrain()
        mesh = bpy.data.objects["terrain"].data
        vals = [self.blight_at(v.co.x * self.upm + self.cx, v.co.y * self.upm + self.cy) for v in mesh.vertices]
        mesh.attributes.new("blight", "FLOAT", "POINT").data.foreach_set("value", vals)
        for name in ("grass", "ramp"):
            self.blight_mix(self.mats[name], name)

    def blight_mix(self, mt: bpy.types.Material, name: str) -> None:
        """草地 / 坡道颜色与枯萎黑土按顶点属性 + 噪声混合，边界成自然的不规则斑块而不是格子。"""
        nt = mt.node_tree
        bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
        coord = next(n for n in nt.nodes if n.type == "TEX_COORD")
        attr = nt.nodes.new("ShaderNodeAttribute")
        attr.attribute_name = "blight"
        edge = nt.nodes.new("ShaderNodeTexNoise")
        edge.inputs["Scale"].default_value = 0.22
        edge.inputs["Detail"].default_value = 6.0
        nt.links.new(coord.outputs["Object"], edge.inputs["Vector"])
        mad = nt.nodes.new("ShaderNodeMath")
        mad.operation = "MULTIPLY_ADD"
        nt.links.new(edge.outputs["Fac"], mad.inputs[0])
        mad.inputs[1].default_value = 0.6
        nt.links.new(attr.outputs["Fac"], mad.inputs[2])
        thr = nt.nodes.new("ShaderNodeValToRGB")
        thr.color_ramp.elements[0].position, thr.color_ramp.elements[1].position = 0.74, 0.86
        nt.links.new(mad.outputs[0], thr.inputs["Fac"])
        dirt = nt.nodes.new("ShaderNodeTexNoise")
        dirt.inputs["Scale"].default_value = 0.09
        dirt.inputs["Detail"].default_value = 8.0
        nt.links.new(coord.outputs["Object"], dirt.inputs["Vector"])
        dr = nt.nodes.new("ShaderNodeValToRGB")
        dr.color_ramp.elements[0].color = (0.030, 0.026, 0.028, 1)
        dr.color_ramp.elements[1].color = (0.15, 0.13, 0.12, 1)
        nt.links.new(dirt.outputs["Fac"], dr.inputs["Fac"])
        mix = nt.nodes.new("ShaderNodeMix")
        mix.data_type = "RGBA"
        sock = lambda coll, ident: next(x for x in coll if x.identifier == ident)
        nt.links.new(thr.outputs["Color"], sock(mix.inputs, "Factor_Float"))
        nt.links.new(self.ramps[name].outputs["Color"], sock(mix.inputs, "A_Color"))
        nt.links.new(dr.outputs["Color"], sock(mix.inputs, "B_Color"))
        nt.links.new(sock(mix.outputs, "Result_Color"), bsdf.inputs["Base Color"])

    def recolor(self, side: str) -> None:
        g0, g1, d, r = SIDE_COLORS["sentinel"]  # unblighted ground is always Sentinel-type grass; blight has its own material
        for name, (a, b) in {"grass": (g0, g1), "ramp": (d, g1), "rock": ((0.18, 0.17, 0.16), r)}.items():
            ramp = self.ramps.get(name)
            if ramp:
                ramp.color_ramp.elements[0].color = (*a, 1)
                ramp.color_ramp.elements[1].color = (*b, 1)


    def flat(self, name: str, color, rough: float = 0.8) -> str:
        if name not in self.mats:
            mt = bpy.data.materials.new(name)
            mt.use_nodes = True
            bsdf = next(n for n in mt.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
            bsdf.inputs["Base Color"].default_value = (*color, 1)
            bsdf.inputs["Roughness"].default_value = rough
            mt.diffuse_color = (*color, 1)
            self.mats[name] = mt
        return name

    # ---------- water ----------
    def build_water(self) -> None:
        z = (self.cfg["water_level_layer"] - self.cfg["base_layer"]) * self.cfg["level_height_m"]
        half = 16384 / self.upm / 2 + 10
        mesh = bpy.data.meshes.new("water")
        bm = bmesh.new()
        bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=1.0)
        bm.to_mesh(mesh)
        bm.free()
        obj = bpy.data.objects.new("water", mesh)
        span = 16384 / self.upm
        obj.dimensions = (span, span, 0)
        cx, cy = self.m(0, 0)
        obj.location = (cx, cy, z)
        mesh.materials.append(bpy.data.materials.get(self.flat("water_previs", (0.05, 0.16, 0.17), 0.05)))
        self.link(obj, "water")

    # ---------- trees ----------
    def build_trees(self) -> None:
        x0, y0, x1, y1 = self.cfg["terrain_bounds"]
        trees = json.loads(self.sources["trees"].read_text("utf8"))
        self.flat("leaf_a", (0.10, 0.24, 0.06)); self.flat("leaf_b", (0.16, 0.30, 0.08)); self.flat("bark", (0.22, 0.15, 0.09))
        self.flat("conifer", (0.08, 0.12, 0.09)); self.flat("deadwood", (0.62, 0.60, 0.55))
        src = {
            "trunk": self.prim("cyl", "src_trunk", "src", "bark", (0, 0, -999), (0.45, 0.45, 6.5)),
            "crown": self.prim("sphere", "src_crown", "src", "leaf_a", (0, 0, -999), (1, 1, 0.8)),
            "crown2": self.prim("sphere", "src_crown2", "src", "leaf_b", (0, 0, -999), (1, 1, 0.8)),
            "cone": self.prim("cyl", "src_cone", "src", "conifer", (0, 0, -999), (1, 1, 11), r1=3.2, r2=0.2, seg=10),
            "dead": self.prim("cyl", "src_dead", "src", "deadwood", (0, 0, -999), (0.35, 0.35, 9), r1=1, r2=0.4, seg=8),
            "branch": self.prim("cyl", "src_branch", "src", "deadwood", (0, 0, -999), (0.15, 0.15, 3.5), seg=6),
        }
        n = 0
        for d in trees:
            if not (x0 <= d["x"] <= x1 and y0 <= d["y"] <= y1) or d.get("life", 1) <= 0:
                continue
            s = (d["scale"][0] if isinstance(d["scale"], list) else d["scale"]) * (0.85 + 0.3 * self.rng.random())
            mx, my = self.m(d["x"], d["y"])
            gz = self.ground(d["x"], d["y"])
            rnd = random.Random(d["editor_id"])
            objs = []
            if not self.blighted(d["x"], d["y"]):
                objs.append(self.inst(src["trunk"], "trees_broadleaf", (mx, my, gz), s))
                for k in range(3):
                    r = (2.2 + rnd.random() * 1.0) * s
                    ox, oy = rnd.uniform(-1.1, 1.1) * s, rnd.uniform(-1.1, 1.1) * s
                    objs.append(self.inst(src["crown" if k % 2 == 0 else "crown2"], "trees_broadleaf", (mx + ox, my + oy, gz + (6.5 + k * 1.5) * s), r))
                top = gz + 12.5 * s
            elif rnd.random() < 0.72:
                objs.append(self.inst(src["cone"], "trees_scourge", (mx, my, gz), s))
                top = gz + 11 * s
            else:
                objs.append(self.inst(src["dead"], "trees_scourge", (mx, my, gz), s))
                for k in range(3):
                    o = self.inst(src["branch"], "trees_scourge", (mx, my, gz + (4.5 + k * 1.3) * s), s)
                    o.rotation_euler = (math.radians(rnd.uniform(35, 60)), 0, rnd.uniform(0, 2 * math.pi))
                    objs.append(o)
                top = gz + 10 * s
            self.tree_objs.append((objs, mx, my, top, 3.6 * s))
            n += 1
        for o in src.values():
            bpy.data.objects.remove(o)
        self.tree_count = n

    def inst(self, src: bpy.types.Object, coll: str, loc, s: float) -> bpy.types.Object:
        o = bpy.data.objects.new(src.name.replace("src_", ""), src.data)
        o.location = loc
        o.scale = (src.scale.x * s, src.scale.y * s, src.scale.z * s)
        return self.link(o, coll)

    # ---------- entity proxies ----------
    def build_features(self) -> None:
        f = json.loads(self.sources["features"].read_text("utf8"))
        creatures = self.cfg["camp_creatures"]
        base = [(r["x"], r["y"]) for r in json.loads(self.sources["units"].read_text("utf8"))["rows"]]
        for c in f["camps"]:
            groups = creatures.get(c["id"])
            if not groups:
                continue
            mx, my = self.m(*c["spawn"])
            gz = self.ground(*c["spawn"])
            members = [(g, k) for g in groups for k in range(g[3])]
            for i, (g, _k) in enumerate(members):
                label, h, r, _count, color = g
                a = 2 * math.pi * i / len(members) + 0.4
                rad = 0 if len(members) == 1 else 1.6 + r * 1.5
                x, y = mx + rad * math.cos(a), my + rad * math.sin(a)
                m = self.flat(f"cr_{label}", color, 0.7)
                self.prim("cyl", f"{c['id']}_{label}", "camp_creatures", m, (x, y, gz), (r, r, h * 0.72))
                self.prim("sphere", f"{c['id']}_{label}_h", "camp_creatures", m, (x, y, gz + h * 0.82), (r * 0.75, r * 0.75, r * 0.75))
        ro = f["roshan"]
        mx, my = self.m(*ro["spawn"]); gz = self.ground(*ro["spawn"])
        m = self.flat("roshan_stone", (0.30, 0.22, 0.36), 0.85)
        for k, (r, z) in enumerate(((1.5, 1.2), (1.8, 2.6), (1.0, 3.9))):
            self.prim("sphere", f"roshan_{k}", "creatures", m, (mx, my, gz + z), (r * 1.1, r, r))
        for rn in f["runes"]:
            mx, my = self.m(*rn["spawn"]); gz = self.ground(*rn["spawn"])
            m = self.flat("rune_stone", (0.40, 0.42, 0.38), 0.9)
            for k in range(8):
                a = 2 * math.pi * k / 8
                self.prim("sphere", f"rune_{k}", "features", m, (mx + 1.8 * math.cos(a), my + 1.8 * math.sin(a), gz + 0.15), (0.45, 0.45, 0.3))
        for s in f["shops"]:
            mx, my = self.m(*s["spawn"]); gz = self.ground(*s["spawn"])
            if s["kind"] == "secret_shop":
                m = self.flat("robe", (0.16, 0.08, 0.20), 0.7)
                self.prim("cyl", "leragas", "creatures", m, (mx, my, gz), (1, 1, 1.75), r1=0.5, r2=0.18, seg=12)
                self.prim("sphere", "leragas_h", "creatures", self.flat("hood", (0.75, 0.68, 0.50)), (mx, my, gz + 1.9), (0.22, 0.22, 0.22))
            elif s["rawcode"] == "u010":
                wood, straw = self.flat("bamboo", (0.55, 0.45, 0.25)), self.flat("thatch", (0.62, 0.62, 0.25))
                for dx, dy in ((-2, -2), (2, -2), (-2, 2), (2, 2)):
                    self.prim("cyl", "hut_post", "features", wood, (mx + dx, my + dy, gz), (0.15, 0.15, 3.2))
                self.prim("cyl", "hut_floor", "features", wood, (mx, my, gz + 3.0), (3.2, 3.2, 0.3))
                self.prim("cyl", "hut_wall", "features", self.flat("cloth", (0.55, 0.10, 0.12)), (mx, my, gz + 3.3), (2.6, 2.6, 2.0))
                self.prim("cyl", "hut_roof", "features", straw, (mx, my, gz + 5.3), (1, 1, 2.6), r1=3.6, r2=0.2, seg=16)
            else:
                self.prim("box", "lab", "features", self.flat("planks", (0.40, 0.30, 0.20)), (mx, my, gz), (6, 6, 2.2))
                self.prim("box", "lab_top", "features", self.flat("metal", (0.38, 0.40, 0.44), 0.5), (mx, my, gz + 2.2), (4, 4, 2.4))
        tw = {"sentinel": self.flat("treant", (0.18, 0.30, 0.10)), "scourge": self.flat("scourge_metal", (0.30, 0.26, 0.34), 0.6)}
        for t in f["towers"]:
            if any(abs(t["spawn"][0] - bx) < 50 and abs(t["spawn"][1] - by) < 50 for bx, by in base):
                continue
            mx, my = self.m(*t["spawn"]); gz = self.ground(*t["spawn"])
            if t["side"] == "sentinel":
                self.prim("cyl", t["id"], "features", tw["sentinel"], (mx, my, gz), (1, 1, 9), r1=3.5, r2=1.4, seg=14)
            else:
                self.prim("cyl", t["id"], "features", tw["scourge"], (mx, my, gz), (1, 1, 7), r1=5, r2=1.5, seg=8)
                self.prim("sphere", t["id"] + "_c", "features", self.flat("crystal", (0.3, 0.8, 0.4), 0.2), (mx, my, gz + 7.6), (0.9, 0.9, 1.3))

    # ---------- render ----------
    def setup_scene(self) -> None:
        super().setup_scene()
        sc = bpy.context.scene
        for vt in ("AgX", "Filmic", "Standard"):
            try:
                sc.view_settings.view_transform = vt
                break
            except TypeError:
                continue
        bpy.context.scene.world.node_tree.nodes["Background"].inputs[1].default_value = self.cfg["render"].get("sky_strength", 0.35)
        sun = bpy.data.objects["sun"].data
        sun.energy = self.cfg["render"]["sun_energy"]
        sun.angle = math.radians(1.5)

    def clear_sightline(self, c: dict) -> int:
        """藏起挡住机位到注视点视线的树（树顶高过视线、树冠压到视线两侧），其余林子照原版保留。"""
        X, Y, h = c["pos"]
        LX, LY, lh = c["look"]
        ex, ey = self.m(X, Y); ez = self.ground(X, Y) + h
        tx, ty = self.m(LX, LY); tz = self.ground(LX, LY) + lh
        dx, dy = tx - ex, ty - ey
        L2 = dx * dx + dy * dy or 1.0
        hidden = 0
        for objs, mx, my, top, rad in self.tree_objs:
            u = ((mx - ex) * dx + (my - ey) * dy) / L2
            occ = 0.0 < u < 0.92 and math.hypot(ex + u * dx - mx, ey + u * dy - my) < rad + 1.0 and top > ez + u * (tz - ez) - 0.5
            for o in objs:
                o.hide_render = occ
            hidden += occ
        return hidden

    def shot_cameras(self) -> list[dict]:
        planned = {c["id"]: c for r in json.loads(self.sources["region_cameras"].read_text("utf8"))["regions"].values() for c in r["cameras"]}
        s1 = {f"S1_{c['id']}": {**c, "id": f"S1_{c['id']}"} for c in json.loads(self.sources["s1_cameras"].read_text("utf8"))["cameras"]}
        return [planned.get(i) or s1[i] for i in self.cfg["shots"]]


def main() -> None:
    cfg, root = load_config()
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o)
    b = Previs(cfg, root)
    b.setup_scene()
    b.build_terrain()
    b.build_water()
    b.build_trees()
    b.build_units()
    b.build_features()
    b.build_doodads()
    b.build_fences()
    cfg["cameras"] = b.shot_cameras()
    b.sources.pop("region_cameras", None)   # cameras(): only the listed shots
    out_dir = (root / cfg["out_dir"]).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    sc = bpy.context.scene
    proj = {}
    side_of = cfg["side_of"]
    for cam in b.cameras():
        c, obj = cam["cfg"], cam["obj"]
        b.recolor(side_of[c["id"].split("_")[0]])
        cleared = b.clear_sightline(c) if c.get("type") == "persp" else 0
        camp = bpy.data.collections.get("camp_creatures")
        if camp:
            camp.hide_render = c["id"] in cfg.get("empty_shots", [])
        sc.camera = obj
        sc.render.resolution_x, sc.render.resolution_y = c["res"]
        path = out_dir / f"previs_{c['id']}.png"
        sc.render.filepath = str(path)
        bpy.ops.render.render(write_still=True)
        proj[c["id"]] = {"file": path.name, "sha256": sha256(path), "camera": c, "trees_cleared_from_sightline": cleared,
                         "camp_creatures_shown": not (camp and camp.hide_render)}
    (out_dir / "previs_projection.json").write_text(json.dumps({"status": "previs_reference_not_film_art", "follow_up": 244,
        "views": proj, "notes": cfg["notes"]}, ensure_ascii=False, indent=1) + "\n", "utf8")
    print("DONE", out_dir, len(proj))


if __name__ == "__main__":
    main()
