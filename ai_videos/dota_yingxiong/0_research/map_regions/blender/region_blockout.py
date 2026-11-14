# -*- coding: utf-8 -*-
"""DotA 6.83d 区域三维布局（technical layout，不是成片场景）。

    blender -b --factory-startup --python region_blockout.py -- <区域配置.json>

只读原版数据：w3e 顶点层/坡道标志（terrain_samples.json）、树位（tree_positions.json）、
基地实例坐标（base_layout_manifest.json）、放置物（war3map.doo）。坐标按配置的
units_per_m 换算为米，北 = +Y、东 = +X；高差按 level_height_m（每个悬崖层）换算。
产物：.blend、各机位干净渲染、projection.json（每个对象在每个机位的像素位置）。
"""
from __future__ import annotations

import hashlib
import json
import math
import struct
import sys
from pathlib import Path

import bmesh
import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

TILE = 128.0
MAP_MIN = -8192.0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_config() -> tuple[dict, Path]:
    """区域配置可写 "extends": "common.json"：公共的尺度、材质、体块只在公共配置里定义一次。"""
    path = Path(sys.argv[sys.argv.index("--") + 1]).resolve()
    cfg = json.loads(path.read_text("utf8"))
    if "extends" in cfg:
        base = json.loads((path.parent / cfg.pop("extends")).read_text("utf8"))
        for k, v in cfg.items():
            base[k] = {**base[k], **v} if isinstance(v, dict) and isinstance(base.get(k), dict) else v
        cfg = base
    return cfg, path.parent


def read_doodads(path: Path) -> list[dict]:
    raw = path.read_bytes()
    magic, version, sub, count = struct.unpack_from("<4siii", raw)
    assert magic == b"W3do" and version in (7, 8), (magic, version, sub)
    off, out = 16, []
    for _ in range(count):
        did, _var, x, y, z, ang, sx, sy, sz = struct.unpack_from("<4si3ff3f", raw, off)
        off += 36
        flags, life = raw[off], raw[off + 1]
        off += 2
        if version >= 8:
            _table, sets = struct.unpack_from("<ii", raw, off)
            off += 8
            for _s in range(sets):
                (n,) = struct.unpack_from("<i", raw, off)
                off += 4 + n * 8
        (editor,) = struct.unpack_from("<i", raw, off)
        off += 4
        out.append({"id": did.decode("latin-1"), "x": x, "y": y, "z": z, "angle": ang,
                    "scale": sx, "flags": flags, "life": life, "editor_id": editor})
    return out


class Terrain:
    """w3e 顶点 → 连续高度：同层平面，四角全带坡道标志的格线性过渡，其余跨层格画成陡坎。"""

    def __init__(self, samples: dict, base_layer: int, level_m: float):
        self.layers = samples["cliff_layers"]
        self.flags = samples["flags"]
        self.n = samples["width"]
        self.base, self.level_m = base_layer, level_m

    def _corner(self, i: int, j: int) -> tuple[int, bool]:
        i, j = max(0, min(self.n - 1, i)), max(0, min(self.n - 1, j))
        return self.layers[j][i], bool(self.flags[j][i] & 16)

    def tile_kind(self, X: float, Y: float) -> str:
        i, j = int((X - MAP_MIN) // TILE), int((Y - MAP_MIN) // TILE)
        c = [self._corner(i, j), self._corner(i + 1, j), self._corner(i, j + 1), self._corner(i + 1, j + 1)]
        if len({l for l, _ in c}) == 1:
            return "flat"
        return "ramp" if all(r for _, r in c) else "cliff"

    def level(self, X: float, Y: float) -> float:
        fi, fj = (X - MAP_MIN) / TILE, (Y - MAP_MIN) / TILE
        i, j = int(math.floor(fi)), int(math.floor(fj))
        u, v = fi - i, fj - j
        (a, ra), (b, rb), (c, rc), (d, rd) = (self._corner(i, j), self._corner(i + 1, j),
                                              self._corner(i, j + 1), self._corner(i + 1, j + 1))
        if a == b == c == d:
            return float(a)
        if not (ra and rb and rc and rd):
            sharpen = lambda t: min(1.0, max(0.0, (t - 0.5) * 5.0 + 0.5))
            u, v = sharpen(u), sharpen(v)
        return (a * (1 - u) + b * u) * (1 - v) + (c * (1 - u) + d * u) * v

    def z(self, X: float, Y: float) -> float:
        return (self.level(X, Y) - self.base) * self.level_m


class Builder:
    def __init__(self, cfg: dict, root: Path):
        self.cfg, self.root = cfg, root
        self.upm = cfg["units_per_m"]
        b = cfg["overhead_bounds"]
        self.cx, self.cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
        src = {k: (root / v).resolve() for k, v in cfg["sources"].items()}
        self.sources = src
        self.terrain = Terrain(json.loads(src["terrain"].read_text("utf8")), cfg["base_layer"], cfg["level_height_m"])
        self.mats: dict[str, bpy.types.Material] = {}
        self.anchors: dict[str, tuple[float, float, float, str]] = {}

    # ---------- helpers ----------
    def m(self, X: float, Y: float) -> tuple[float, float]:
        return (X - self.cx) / self.upm, (Y - self.cy) / self.upm

    def ground(self, X: float, Y: float) -> float:
        return self.terrain.z(X, Y)

    def mat(self, name: str) -> bpy.types.Material:
        if name in self.mats:
            return self.mats[name]
        spec = self.cfg["materials"][name]
        mt = bpy.data.materials.new(name)
        mt.use_nodes = True
        bsdf = next(n for n in mt.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
        bsdf.inputs["Base Color"].default_value = (*spec["color"], 1.0)
        bsdf.inputs["Roughness"].default_value = spec.get("roughness", 0.8)
        if spec.get("emission"):
            bsdf.inputs["Emission Color"].default_value = (*spec["color"], 1.0)
            bsdf.inputs["Emission Strength"].default_value = spec["emission"]
        mt.diffuse_color = (*spec["color"], 1.0)
        self.mats[name] = mt
        return mt

    def link(self, obj: bpy.types.Object, coll: str) -> bpy.types.Object:
        c = bpy.data.collections.get(coll) or bpy.data.collections.new(coll)
        if c.name not in bpy.context.scene.collection.children:
            bpy.context.scene.collection.children.link(c)
        c.objects.link(obj)
        return obj

    def prim(self, kind: str, name: str, coll: str, mat: str, loc, scale, rot_z: float = 0.0, **kw) -> bpy.types.Object:
        mesh = bpy.data.meshes.new(name)
        bm = bmesh.new()
        if kind == "cyl":
            bmesh.ops.create_cone(bm, cap_ends=True, segments=kw.get("seg", 24), radius1=kw.get("r1", 1.0),
                                  radius2=kw.get("r2", 1.0), depth=1.0)
            bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, 0.5))
        elif kind == "box":
            bmesh.ops.create_cube(bm, size=1.0)
            bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, 0.5))
        elif kind == "sphere":
            bmesh.ops.create_uvsphere(bm, u_segments=20, v_segments=12, radius=1.0)
        bm.to_mesh(mesh)
        bm.free()
        obj = bpy.data.objects.new(name, mesh)
        obj.location, obj.scale, obj.rotation_euler = loc, scale, (0, 0, rot_z)
        mesh.materials.append(self.mat(mat))
        for poly in mesh.polygons:
            poly.use_smooth = kind in ("cyl", "sphere", "torus")
        return self.link(obj, coll)

    # ---------- terrain ----------
    def build_terrain(self) -> None:
        x0, y0, x1, y1 = self.cfg["terrain_bounds"]
        step = self.cfg["terrain_step"]
        nx, ny = int((x1 - x0) / step) + 1, int((y1 - y0) / step) + 1
        bm = bmesh.new()
        grid = []
        for j in range(ny):
            row = []
            for i in range(nx):
                X, Y = x0 + i * step, y0 + j * step
                mx, my = self.m(X, Y)
                row.append(bm.verts.new((mx, my, self.ground(X, Y))))
            grid.append(row)
        for j in range(ny - 1):
            for i in range(nx - 1):
                f = bm.faces.new((grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]))
                f.normal_update()
                ramp = self.terrain.tile_kind(x0 + (i + 0.5) * step, y0 + (j + 0.5) * step) == "ramp"
                f.material_index = 2 if f.normal.z < 0.75 else (1 if ramp else 0)
        mesh = bpy.data.meshes.new("terrain")
        bm.to_mesh(mesh)
        bm.free()
        for name in ("grass", "ramp", "rock"):
            mesh.materials.append(self.mat(name))
        self.link(bpy.data.objects.new("terrain", mesh), "terrain")

    # ---------- trees ----------
    def build_trees(self) -> None:
        x0, y0, x1, y1 = self.cfg["terrain_bounds"]
        trees = json.loads(self.sources["trees"].read_text("utf8"))
        t = self.cfg["tree"]
        trunk = self.prim("cyl", "tree_trunk_src", "trees", "trunk", (0, 0, -999), (t["trunk_r"], t["trunk_r"], t["trunk_h"]))
        crown = self.prim("cyl", "tree_crown_src", "trees", "canopy", (0, 0, -999), (1, 1, t["crown_h"]), r1=t["crown_r"], r2=t["crown_r"] * 0.15, seg=10)
        n = 0
        for d in trees:
            if not (x0 <= d["x"] <= x1 and y0 <= d["y"] <= y1) or d.get("life", 1) <= 0:
                continue
            s = d["scale"][0] if isinstance(d["scale"], list) else d["scale"]
            mx, my = self.m(d["x"], d["y"])
            gz = self.ground(d["x"], d["y"])
            for src, z0 in ((trunk, 0.0), (crown, t["crown_base"])):
                o = bpy.data.objects.new(f"{src.name[:-4]}_{d['editor_id']}", src.data)
                o.location = (mx, my, gz + z0 * s)
                o.scale = (src.scale.x * s, src.scale.y * s, src.scale.z * s)
                self.link(o, "trees")
            n += 1
        bpy.data.objects.remove(trunk)
        bpy.data.objects.remove(crown)
        self.tree_count = n

    # ---------- units & doodads ----------
    def anchor(self, key: str, X: float, Y: float, h: float, label: str) -> None:
        mx, my = self.m(X, Y)
        self.anchors[key] = (mx, my, self.ground(X, Y) + h, label)

    def build_units(self) -> None:
        x0, y0, x1, y1 = self.cfg["terrain_bounds"]
        rows = json.loads(self.sources["units"].read_text("utf8"))["rows"]
        shapes = self.cfg["shapes"]
        for r in rows:
            if not (x0 <= r["x"] <= x1 and y0 <= r["y"] <= y1):
                continue
            key = f"{r['faction']}:{r['instance_id']}"
            spec = shapes.get(r["asset_id"]) or shapes[r["category"]]
            mx, my = self.m(r["x"], r["y"])
            gz = self.ground(r["x"], r["y"])
            top = 0.0
            for k, part in enumerate(spec["parts"]):
                z = gz + part.get("z", 0.0)
                ox, oy = part.get("offset", [0, 0])
                sc = part["size"]
                kw = {k2: part[k2] for k2 in ("r1", "r2", "seg") if k2 in part}
                self.prim(part["kind"], f"{key}_{k}", spec.get("coll", r["category"]), part["mat"],
                          (mx + ox, my + oy, z), sc, math.radians(part.get("rot", 0)), **kw)
                top = max(top, part.get("z", 0.0) + (sc[2] if part["kind"] != "sphere" else sc[2]))
            self.anchor(key, r["x"], r["y"], min(top, spec.get("label_h", top)), f"{r['asset_id']} {r['name']}")

    def build_features(self) -> None:
        """map_features.json 的营地（占位区外框＋刷新点）、肉山、神符、商店与基地外的塔。"""
        if "features" not in self.sources:
            return
        x0, y0, x1, y1 = self.cfg["terrain_bounds"]
        f = json.loads(self.sources["features"].read_text("utf8"))
        shapes = self.cfg["feature_shapes"]
        base = [(r["x"], r["y"]) for r in json.loads(self.sources["units"].read_text("utf8"))["rows"]]
        points = [(c, "camp") for c in f["camps"]] + [(f["roshan"], "roshan")] + [(r, "rune") for r in f["runes"]]             + [(s, s["kind"]) for s in f["shops"]] + [(t, f"tower_{t['side']}") for t in f["towers"]
                                                      if not any(abs(t["spawn"][0] - bx) < 50 and abs(t["spawn"][1] - by) < 50 for bx, by in base)]
        for item, kind in points:
            X, Y = item["spawn"]
            if not (x0 <= X <= x1 and y0 <= Y <= y1):
                continue
            spec = shapes[kind]
            mx, my = self.m(X, Y)
            gz = self.ground(X, Y)
            mat = spec.get("mat_by_size", {}).get(item.get("size", ""), None)
            for k, part in enumerate(spec["parts"]):
                kw = {k2: part[k2] for k2 in ("r1", "r2", "seg") if k2 in part}
                self.prim(part["kind"], f"{item['id']}_{k}", "features", mat or part["mat"], (mx, my, gz + part.get("z", 0.0)), part["size"], **kw)
            if kind == "camp":
                ax0, ay0, ax1, ay1 = item["area"]
                corners = [(ax0, ay0), (ax1, ay0), (ax1, ay1), (ax0, ay1), (ax0, ay0)]
                for (pX, pY), (qX, qY) in zip(corners, corners[1:]):
                    a, b = Vector((*self.m(pX, pY), 0)), Vector((*self.m(qX, qY), 0))
                    mid = (a + b) / 2
                    gzm = self.ground((pX + qX) / 2, (pY + qY) / 2)
                    self.prim("box", f"{item['id']}_area", "features", mat or spec["parts"][0]["mat"], (mid.x, mid.y, gzm + 0.1),
                              ((b - a).length + 0.8, 0.8, 0.35), math.atan2(b.y - a.y, b.x - a.x))
            label = f"{item['id']} {item['name']}" if kind in ("camp", "roshan") else item["name"]
            self.anchor(item["id"], X, Y, spec.get("label_h", 2.0), label)

    def build_doodads(self) -> None:
        x0, y0, x1, y1 = self.cfg["terrain_bounds"]
        dd = self.cfg["doodads"]
        self.doodads = [d for d in read_doodads(self.sources["doodads"]) if d["id"] in dd and x0 <= d["x"] <= x1 and y0 <= d["y"] <= y1]
        for d in self.doodads:
            spec = dd[d["id"]]
            mx, my = self.m(d["x"], d["y"])
            gz = self.ground(d["x"], d["y"])
            for k, part in enumerate(spec["parts"]):
                kw = {k2: part[k2] for k2 in ("r1", "r2", "seg") if k2 in part}
                rot = math.degrees(d["angle"]) + part.get("rot", 0) if spec.get("use_angle") else part.get("rot", 0)
                self.prim(part["kind"], f"{d['id']}_{d['editor_id']}_{k}", "doodads", part["mat"],
                          (mx, my, gz + part.get("z", 0.0)), part["size"], math.radians(rot), **kw)
            if spec.get("label"):
                self.anchor(f"{d['id']}#{d['editor_id']}", d["x"], d["y"], spec.get("label_h", 1.0), spec["label"])

    def build_fences(self) -> None:
        for k, line in enumerate(self.cfg.get("fences", [])):
            pts = [Vector((*self.m(X, Y), 0)) for X, Y in line["points"]]
            for a, b in zip(pts, pts[1:]):
                n = max(1, int((b - a).length / line["post_spacing_m"]))
                for s in range(n + 1):
                    p = a.lerp(b, s / n)
                    X, Y = p.x * self.upm + self.cx, p.y * self.upm + self.cy
                    self.prim("box", f"fence{k}_post", "fences", "wood", (p.x, p.y, self.ground(X, Y)), (0.25, 0.25, line["h"]))
                mid = (a + b) / 2
                Xm, Ym = mid.x * self.upm + self.cx, mid.y * self.upm + self.cy
                ang = math.atan2(b.y - a.y, b.x - a.x)
                for hz in (0.45, 0.85):
                    self.prim("box", f"fence{k}_rail", "fences", "wood", (mid.x, mid.y, self.ground(Xm, Ym) + line["h"] * hz),
                              ((b - a).length, 0.12, 0.12), ang)

    # ---------- scene ----------
    def setup_scene(self) -> None:
        sc = bpy.context.scene
        try:
            sc.render.engine = self.cfg["render"]["engine"]
        except TypeError as e:
            print("engine fallback:", e)
            sc.render.engine = "CYCLES"
        if sc.render.engine == "CYCLES":
            sc.cycles.samples = 32
        world = bpy.data.worlds.new("sky")
        world.use_nodes = True
        bg = next(n for n in world.node_tree.nodes if n.type == "BACKGROUND")
        bg.inputs[0].default_value = (*self.cfg["render"]["sky"], 1)
        bg.inputs[1].default_value = 0.9
        sc.world = world
        sun = bpy.data.lights.new("sun", "SUN")
        sun.energy = self.cfg["render"]["sun_energy"]
        sun.angle = math.radians(2)
        so = bpy.data.objects.new("sun", sun)
        el, az = (math.radians(a) for a in self.cfg["render"]["sun_elev_az"])
        so.rotation_euler = (math.pi / 2 - el, 0, az)
        self.link(so, "lights")
        sc.view_settings.view_transform = "Standard"

    def region_cameras(self) -> list[dict]:
        """每个拍摄区一台正交相机，范围直接取 map_regions.json 的 original_reference.map_bounds（地图百分比，北上）。"""
        if "region_manifest" not in self.sources:
            return []
        out = []
        for r in json.loads(self.sources["region_manifest"].read_text("utf8"))["regions"]:
            b = r["original_reference"]["map_bounds"]
            X = lambda p: MAP_MIN + p * 163.84
            Y = lambda p: -MAP_MIN - p * 163.84
            w, h = b[2] - b[0], b[3] - b[1]
            res = [1200, round(1200 * h / w)] if w >= h else [round(1200 * w / h), 1200]
            out.append({"id": r["id"], "type": "ortho", "res": res, "bounds": [X(b[0]), Y(b[3]), X(b[2]), Y(b[1])]})
        return out

    def cameras(self) -> list[dict]:
        out = []
        planned = []
        if "region_cameras" in self.sources:
            planned = [c for r in json.loads(self.sources["region_cameras"].read_text("utf8"))["regions"].values() for c in r["cameras"]]
        for cam in self.cfg.get("cameras", []) + self.region_cameras() + planned:
            data = bpy.data.cameras.new(cam["id"])
            obj = bpy.data.objects.new(f"cam_{cam['id']}", data)
            self.link(obj, "cameras")
            res = cam["res"]
            if cam["type"] == "ortho":
                b = cam.get("bounds", self.cfg["overhead_bounds"])
                data.type = "ORTHO"
                w_m, h_m = (b[2] - b[0]) / self.upm, (b[3] - b[1]) / self.upm
                data.ortho_scale = max(w_m, h_m * res[0] / res[1])
                obj.location = (*self.m((b[0] + b[2]) / 2, (b[1] + b[3]) / 2), 400)
                obj.rotation_euler = (0, 0, 0)
                data.clip_end = 1000
            else:
                X, Y, h = cam["pos"]
                LX, LY, lh = cam["look"]
                eye = Vector((*self.m(X, Y), self.ground(X, Y) + h))
                tgt = Vector((*self.m(LX, LY), self.ground(LX, LY) + lh))
                obj.location = eye
                obj.rotation_euler = (tgt - eye).to_track_quat("-Z", "Y").to_euler()
                data.lens = cam["lens_mm"]
                data.sensor_width = 36
                data.clip_end = 2000
            out.append({"cfg": cam, "obj": obj})
        return out

    def render(self, out_dir: Path) -> dict:
        sc = bpy.context.scene
        proj = {}
        for cam in self.cameras():
            c, obj = cam["cfg"], cam["obj"]
            sc.camera = obj
            sc.render.resolution_x, sc.render.resolution_y = c["res"]
            sc.render.resolution_percentage = 100
            path = out_dir / f"layout_{c['id']}.png"
            sc.render.filepath = str(path)
            bpy.ops.render.render(write_still=True)
            pts = {}
            for key, (x, y, z, label) in self.anchors.items():
                v = world_to_camera_view(sc, obj, Vector((x, y, z)))
                if 0 <= v.x <= 1 and 0 <= v.y <= 1 and v.z > 0:
                    pts[key] = {"px": [round(v.x * c["res"][0], 1), round((1 - v.y) * c["res"][1], 1)], "label": label}
            proj[c["id"]] = {"file": path.name, "sha256": sha256(path), "res": c["res"], "camera": c,
                             "location_m": list(obj.location), "points": pts}
        return proj


def main() -> None:
    cfg, root = load_config()
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o)
    b = Builder(cfg, root)
    b.setup_scene()
    b.build_terrain()
    b.build_trees()
    b.build_units()
    b.build_features()
    b.build_doodads()
    b.build_fences()
    out_dir = (root / cfg["out_dir"]).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    proj = b.render(out_dir)
    blend = out_dir / cfg["blend_name"]
    bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    manifest = {
        "status": "technical_layout_not_film_art",
        "region": cfg["region"],
        "config": {"file": Path(sys.argv[sys.argv.index("--") + 1]).name, "sha256": sha256(Path(sys.argv[sys.argv.index("--") + 1]))},
        "sources": {k: {"file": str(v), "sha256": sha256(v)} for k, v in b.sources.items()},
        "units_per_m": cfg["units_per_m"], "level_height_m": cfg["level_height_m"],
        "overhead_bounds": cfg["overhead_bounds"], "origin_world": [b.cx, b.cy],
        "tree_count": b.tree_count, "doodads": len(b.doodads), "blend": blend.name,
        "views": proj, "notes": cfg["notes"],
    }
    (out_dir / "layout_projection.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", "utf8")
    print("DONE", out_dir)


if __name__ == "__main__":
    main()
