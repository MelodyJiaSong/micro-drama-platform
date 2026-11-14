"""Blender + MPFB: build a cast of rigged characters (game_engine rig) into one .blend.
blender -b -P make_cast.py -- cast.json out.blend [preview_dir]
cast.json: [{"name","gender","age","height","muscle","weight","outfit":"riley"|"tunic",
             "tunic_len":"knee"|"ankle","colors":{...},"hair":"long01"|..., "props":["basket","amphora2"]}]
Every object of a character is prefixed with name; rig is "<name>_rig".
"""
import bpy, sys, json, math, importlib, os
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
CAST = json.load(open(argv[0], encoding="utf-8"))
OUT = argv[1]
PREV = argv[2] if len(argv) > 2 else None
HS = importlib.import_module("bl_ext.blender_org.mpfb.services.humanservice").HumanService
TS = importlib.import_module("bl_ext.blender_org.mpfb.services.targetservice").TargetService
ASSETS = os.path.join(os.environ["APPDATA"], "Blender Foundation", "Blender", "5.1", "extensions", ".user",
                      "blender_org", "mpfb", "data")

for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)

def mat(name, rgb, rough=0.85, sheen=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = (*rgb, 1)
    b.inputs["Roughness"].default_value = rough
    # subtle fabric noise so flat colours do not look plastic
    nt = m.node_tree
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 180
    mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"; mix.blend_type = "MULTIPLY"
    ins = [x for x in mix.inputs if x.type == "RGBA"]; outs = [x for x in mix.outputs if x.type == "RGBA"]
    fac = next(x for x in mix.inputs if x.name == "Factor" and x.type == "VALUE")
    fac.default_value = 0.18
    ins[0].default_value = (*rgb, 1)
    nt.links.new(nz.outputs["Color"], ins[1])
    nt.links.new(outs[0], b.inputs["Base Color"])
    bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.15
    nt.links.new(nz.outputs["Fac"], bump.inputs["Height"]); nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    return m

def skin_mat(name, rgb):
    m = mat(name, rgb, 0.55)
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    try:
        b.inputs["Subsurface Weight"].default_value = 0.15
        b.inputs["Subsurface Radius"].default_value = (1.0, 0.4, 0.25)
    except Exception:
        pass
    return m

def bone_parent(obj, rig, bone, loc=(0, 0, 0), rot=(0, 0, 0)):
    obj.parent = rig; obj.parent_type = "BONE"; obj.parent_bone = bone
    obj.location = loc; obj.rotation_euler = rot

def tube(name, rig, top, bot, r_top, r_bot, color, sy=0.78):
    bpy.ops.mesh.primitive_cone_add(vertices=28, radius1=r_bot, radius2=r_top, depth=top - bot,
                                    end_fill_type="NOTHING", location=(0, 0, (top + bot) / 2))
    o = bpy.context.active_object; o.name = name; o.scale = (1, sy, 1)
    bpy.ops.object.transform_apply(scale=True)
    # gentle folds
    bpy.ops.object.modifier_add(type="SUBSURF"); o.modifiers[-1].levels = 2
    bpy.ops.object.modifier_add(type="DISPLACE")
    tx = bpy.data.textures.new(name + "_folds", "CLOUDS"); tx.noise_scale = 0.06
    o.modifiers[-1].texture = tx; o.modifiers[-1].strength = 0.012
    o.data.materials.append(mat(name, color, 0.95))
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True); rig.select_set(True); bpy.context.view_layer.objects.active = rig
    bpy.ops.object.parent_set(type="ARMATURE_AUTO")
    return o

def fitted_top(nm, body, H, color):
    """copy of the (shape-keyed) body: keep torso + upper arms, inflate -> short-sleeved tunic top"""
    dg = bpy.context.evaluated_depsgraph_get()
    ev = body.evaluated_get(dg)
    me = bpy.data.meshes.new_from_object(ev, preserve_all_data_layers=True, depsgraph=dg)
    o = bpy.data.objects.new(nm + "_top", me); bpy.context.collection.objects.link(o)
    o.matrix_world = body.matrix_world.copy()
    import bmesh
    bm = bmesh.new(); bm.from_mesh(me)
    kill = []
    for v in bm.verts:
        z = v.co.z
        # shoulder line: arms leave the torso around |x| ~ 0.2 H/1.67; keep sleeves to ~ |x| < 0.30
        if z < H * 0.50 or z > H * 0.835 or abs(v.co.x) > 0.29 * H / 1.67:
            kill.append(v)
    bmesh.ops.delete(bm, geom=kill, context="VERTS")
    for v in bm.verts:
        v.co += v.normal * 0.014
    bm.to_mesh(me); bm.free()
    o.data.materials.clear(); o.data.materials.append(mat(nm + "_topm", color, 0.95))
    # keep body weights: vertex groups survive new_from_object; add armature modifier to the same rig
    rig = body.parent
    o.parent = rig
    m = o.modifiers.new("arm", "ARMATURE"); m.object = rig
    sub = o.modifiers.new("sub", "SUBSURF"); sub.levels = 1
    return o

def lathe(name, profile, color):
    """profile: list of (r, z) bottom->top; returns object."""
    me = bpy.data.meshes.new(name)
    verts = [(r, 0, z) for r, z in profile]
    edges = [(i, i + 1) for i in range(len(verts) - 1)]
    me.from_pydata(verts, edges, [])
    o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o)
    sc = o.modifiers.new("lathe", "SCREW"); sc.steps = 24; sc.render_steps = 24; sc.use_smooth_shade = True
    o.modifiers.new("sub", "SUBSURF").levels = 1
    o.data.materials.append(mat(name, color, 0.8))
    return o

for c in CAST:
    nm = c["name"]
    macro = TS.get_default_macro_info_dict()
    for k in ("gender", "age", "height", "muscle", "weight", "proportions"):
        if k in c:
            macro[k] = c[k]
    body = HS.create_human(scale=0.1, macro_detail_dict=macro)
    body.name = nm + "_body"
    HS.add_builtin_rig(body, "game_engine", import_weights=True)
    rig = body.parent if body.parent and body.parent.type == "ARMATURE" else \
        next(o for o in bpy.data.objects if o.type == "ARMATURE" and not o.name.endswith("_rig"))
    rig.name = nm + "_rig"
    dg = bpy.context.evaluated_depsgraph_get()
    ev = body.evaluated_get(dg); em = ev.to_mesh()
    H = max((body.matrix_world @ v.co).z for v in em.vertices)
    ev.to_mesh_clear()
    print(nm, "height", round(H, 3))
    col = c.get("colors", {})
    body.data.materials.clear(); body.data.materials.append(skin_mat(nm + "_skin", col.get("skin", (0.55, 0.38, 0.28))))

    def add_asset(kind, aname):
        f = os.path.join(ASSETS, kind, aname, aname + ".mhclo")
        before = set(bpy.data.objects)
        HS.add_mhclo_asset(f, body, asset_type="Hair" if kind == "hair" else "Clothes", subdiv_levels=0)
        new = [o for o in bpy.data.objects if o not in before]
        for o in new:
            o.name = f"{nm}_{aname}"
        return new

    if c.get("outfit") == "riley":
        for o in add_asset("clothes", "female_casualsuit01"):
            # split top / trousers by height: faces above the waist get the shirt colour
            shirt = mat(nm + "_shirt", col.get("shirt", (0.78, 0.68, 0.55)), 0.95)
            pants = mat(nm + "_pants", col.get("pants", (0.42, 0.33, 0.22)), 0.9)
            o.data.materials.clear(); o.data.materials.append(shirt); o.data.materials.append(pants)
            waist = H * 0.555
            for p in o.data.polygons:
                p.material_index = 0 if (o.matrix_world @ p.center).z > waist else 1
        for o in add_asset("clothes", "shoes03"):
            o.data.materials.clear(); o.data.materials.append(mat(nm + "_boots", col.get("boots", (0.20, 0.12, 0.07)), 0.7))
    else:
        L = {"knee": 0.27, "ankle": 0.07, "calf": 0.17}[c.get("tunic_len", "knee")]
        fitted_top(nm, body, H, col.get("tunic", (0.72, 0.66, 0.55)))
        tube(nm + "_tunic", rig, H * 0.60, H * L, 0.19 * H / 1.67, 0.26 * H / 1.67,
             col.get("tunic", (0.72, 0.66, 0.55)), 0.80)
        if c.get("belt", True):
            tube(nm + "_belt", rig, H * 0.60, H * 0.575, 0.165 * H / 1.67, 0.17 * H / 1.67, (0.30, 0.20, 0.12), 0.8)
        for o in add_asset("clothes", c.get("shoes", "shoes01")):
            o.data.materials.clear(); o.data.materials.append(mat(nm + "_sandal", (0.35, 0.22, 0.12), 0.8))
    if c.get("hair"):
        for o in add_asset("hair", c["hair"]):
            hm = mat(nm + "_hair", col.get("hair", (0.12, 0.08, 0.05)), 0.6)
            # keep MPFB alpha texture if present: just tint base colour
            if o.data.materials:
                try:
                    old = o.data.materials[0]
                    tex = next((n for n in old.node_tree.nodes if n.type == "TEX_IMAGE"), None)
                    if tex is not None:
                        b = next(n for n in hm.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
                        t2 = hm.node_tree.nodes.new("ShaderNodeTexImage"); t2.image = tex.image
                        hm.node_tree.links.new(t2.outputs["Alpha"], b.inputs["Alpha"])
                        try: hm.surface_render_method = "DITHERED"
                        except Exception: hm.blend_method = "HASHED"
                except Exception as e:
                    print("hair alpha", e)
                o.data.materials.clear()
            o.data.materials.append(hm)
    pb = rig.data.bones
    def follow(o, bone, offset):
        o.parent = None
        cl = o.constraints.new("COPY_LOCATION"); cl.target = rig; cl.subtarget = bone
        cl.head_tail = 1.0 if bone == "head" else 0.5
        cr = o.constraints.new("COPY_ROTATION"); cr.target = rig
        o.location = offset
        cl.use_offset = True
    for prop in c.get("props", []):
        if prop == "basket":
            b = lathe(nm + "_basket", [(0.0, 0.0), (0.12, 0.0), (0.18, 0.10), (0.19, 0.12)], (0.48, 0.34, 0.18))
            follow(b, "head", (0, 0, -0.01))
            # bread loaves inside
            for k in range(4):
                bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=(0.06 * math.cos(k * 1.6), 0.06 * math.sin(k * 1.6), 0.10))
                bl = bpy.context.active_object; bl.scale = (1, 1, 0.6); bl.name = f"{nm}_loaf{k}"
                bl.data.materials.append(mat(f"{nm}_loafm", (0.38, 0.22, 0.10), 0.7))
                bl.parent = b
        if prop == "amphora2":
            prof = [(0.0, 0.0), (0.03, 0.0), (0.09, 0.10), (0.12, 0.26), (0.10, 0.40), (0.045, 0.50), (0.04, 0.60), (0.055, 0.62)]
            for side, bn in ((1, "hand_l"), (-1, "hand_r")):
                a2 = lathe(f"{nm}_amphora_{'l' if side > 0 else 'r'}", prof, (0.62, 0.34, 0.20))
                follow(a2, bn, (0, 0, -0.30))
    if c.get("hair_cap"):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.105 * H / 1.67)
        h = bpy.context.active_object; h.name = nm + "_cap"
        h.data.materials.append(mat(nm + "_cap", c["hair_cap"], 0.9))
        bone_parent(h, rig, "head", loc=(0, -rig.data.bones["head"].length * 0.55, 0.0))
    rig["cast_name"] = nm

bpy.context.scene.render.fps = 24
if PREV:
    import math as m
    sc = bpy.context.scene
    try: sc.render.engine = "BLENDER_EEVEE_NEXT"
    except TypeError: sc.render.engine = "BLENDER_EEVEE"
    sc.render.resolution_x, sc.render.resolution_y = 1600, 640
    rigs = [o for o in bpy.data.objects if o.type == "ARMATURE"]
    for i, r in enumerate(rigs):
        r.location.x = (i - (len(rigs) - 1) / 2) * 0.9
    cd = bpy.data.cameras.new("pc"); cd.type = "ORTHO"; cd.ortho_scale = max(5.6, 0.9 * len(rigs) + 0.8)
    cam = bpy.data.objects.new("pc", cd); sc.collection.objects.link(cam); sc.camera = cam
    for k, ang in enumerate((180, 0)):
        a = m.radians(ang)
        cam.location = (m.sin(a) * -8, m.cos(a) * -8 * -1 if ang == 0 else 8, 0.9)
        cam.location = (0, 8 if ang == 180 else -8, 0.9)
        cam.rotation_euler = (m.radians(90), 0, m.radians(ang))
        sun = bpy.data.objects.get("psun") or bpy.data.objects.new("psun", bpy.data.lights.new("psun", "SUN"))
        if sun.name not in sc.collection.objects: sc.collection.objects.link(sun)
        sun.data.energy = 3; sun.rotation_euler = (0.9, 0.3, m.radians(ang) + 0.6)
        if sc.world is None: sc.world = bpy.data.worlds.new("w")
        sc.render.filepath = f"{PREV}/cast_{'back' if ang == 180 else 'front'}.png"
        bpy.ops.render.render(write_still=True)
    for r in rigs: r.location.x = 0
    for o in (cam, bpy.data.objects.get("psun")): bpy.data.objects.remove(o)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("SAVED", OUT)
