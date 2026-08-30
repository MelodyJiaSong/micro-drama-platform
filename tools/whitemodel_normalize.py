"""白模归一化 + 验收闸门。任何来源的网格进来，出去都是可用的 {name}.blend。

用法（仓库根目录）：
    blender -b --factory-startup --python tools/whitemodel_normalize.py -- \
        --src  <raw.glb|.obj|.fbx|.stl|.ply|.blend>   \
        --spec <object.toml>                          \
        --out  <目标 .blend>
    # 只验收不写盘（对已有白模做体检）：--qc-only --src 现有.blend

为什么要有这个闸门
------------------
白模的来源是可换的——image-to-3D（Rodin / Hunyuan3D / Tripo…）、素材市场买的高模、
脚本 blockout、手工建的。**pipeline 不该在这些来源之间二选一，它应该接受任何一个，
只要过同一道闸门。** genericity 来自闸门，不来自来源。

而质量不稳的真正来源从来不是"选了哪家 vendor"，是"拿到网格之后那一段"：
四步归一化（朝向/尺寸/原点/清材质）过去写在每个 object 的 Prompt 5 散文里、
由人按文字手动执行，漏一步没人发现；验收清单靠人眼看。**这里把两件事都变成代码。**

四步归一化
----------
① 朝向  —— 按 spec 的 [几何].源朝向 → 目标朝向 旋转（默认目标：前 +Y、上 +Z）
② 尺寸  —— 默认**等比**缩放到 spec 声明的包围盒。等比而非逐轴拉伸，是为了让
           "生成出来的网格比例对不对"仍然是一个可被验收发现的问题；逐轴拉伸会把
           这个缺陷抹平成永远通过。需要精确贴合时用 --fit stretch。
③ 原点  —— 落在底面中心（接地平面），不是几何中心
④ 材质  —— 无条件全剥。白模只承载几何，不承载长相与材质；image-to-3D 的产物
           自带烤死的贴图与颜色，正是必须被剥掉的东西。

验收（可证伪，不是"你看看对不对"）
----------------------------------
包围盒读数 / 原点位置 / 材质残留 / 松散块数，加上 spec 里逐条声明的识别特征探针：

  类型 = "占位"     区域内是否有几何 —— 尾翼在不在、扩散器在不在、车头黑条在不在
  类型 = "截面对比"  两个带之间的截面宽度关系 —— 后轮拱是否外鼓于车身中段、
                     座舱是否向上收窄成泪滴

薄结构（尾翼、扩散器叶片、器物细部）是 image-to-3D 最不稳的地方，换哪家都一样。
闸门治不好生成，但能**发现**——挂了就报出来，再决定重生成还是脚本补件。

QC 不通过 → 退出码 1。这是闸门，不是报告。
"""
from __future__ import annotations

import argparse
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

import bpy
from mathutils import Matrix, Vector

REPO = Path(__file__).resolve().parent.parent

AXES: dict[str, Vector] = {
    "+X": Vector((1, 0, 0)), "-X": Vector((-1, 0, 0)),
    "+Y": Vector((0, 1, 0)), "-Y": Vector((0, -1, 0)),
    "+Z": Vector((0, 0, 1)), "-Z": Vector((0, 0, -1)),
}

IMPORTERS: dict[str, str] = {
    ".glb": "gltf", ".gltf": "gltf", ".obj": "obj", ".fbx": "fbx",
    ".stl": "stl", ".ply": "ply", ".blend": "blend",
}


def die(msg: str) -> None:
    print(f"\n[whitemodel] ✗ {msg}", file=sys.stderr)
    sys.exit(2)


# ---------------------------------------------------------------- 导入

def wipe_scene() -> None:
    bpy.ops.wm.read_factory_settings(use_empty=True)


def import_source(src: Path) -> list[bpy.types.Object]:
    """把任意来源的网格读进空场景。返回导入的 MESH 物体。"""
    ext = src.suffix.lower()
    kind = IMPORTERS.get(ext)
    if kind is None:
        die(f"不支持的来源格式 {ext}；支持 {sorted(IMPORTERS)}")

    if kind == "blend":
        with bpy.data.libraries.load(str(src), link=False) as (_src, _dst):
            _dst.objects = list(_src.objects)
        linked = {o.name for o in bpy.context.collection.objects}
        for ob in bpy.data.objects:
            if ob.name not in linked:
                bpy.context.collection.objects.link(ob)
    elif kind == "gltf":
        bpy.ops.import_scene.gltf(filepath=str(src))
    elif kind == "obj":
        bpy.ops.wm.obj_import(filepath=str(src))
    elif kind == "fbx":
        bpy.ops.import_scene.fbx(filepath=str(src))
    elif kind == "stl":
        bpy.ops.wm.stl_import(filepath=str(src))
    elif kind == "ply":
        bpy.ops.wm.ply_import(filepath=str(src))

    meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    if not meshes:
        die(f"{src} 里没有 MESH 物体")
    return meshes


def join_meshes(meshes: list[bpy.types.Object], name: str) -> bpy.types.Object:
    """合成单一物体。previz 与转盘都把 object 当一个整体摆放，多块会各自跑偏。"""
    bpy.ops.object.select_all(action="DESELECT")
    for ob in meshes:
        ob.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    if len(meshes) > 1:
        bpy.ops.object.join()
    ob = bpy.context.view_layer.objects.active
    ob.name = name
    ob.data.name = name
    return ob


# ---------------------------------------------------------------- 四步归一化

def world_bounds(ob: bpy.types.Object) -> tuple[Vector, Vector]:
    bpy.context.view_layer.update()
    pts = [ob.matrix_world @ Vector(c) for c in ob.bound_box]
    lo = Vector((min(p[i] for p in pts) for i in range(3)))
    hi = Vector((max(p[i] for p in pts) for i in range(3)))
    return lo, hi


def basis(forward: Vector, up: Vector) -> Matrix:
    """由 前/上 两轴建正交基。列序 (右, 前, 上)。"""
    f = forward.normalized()
    u = up.normalized()
    u = (u - f * u.dot(f)).normalized()          # 正交化，容忍 spec 写得不严格
    r = f.cross(u)
    return Matrix((
        (r.x, f.x, u.x),
        (r.y, f.y, u.y),
        (r.z, f.z, u.z),
    ))


def step_orient(ob: bpy.types.Object, src_f: str, src_u: str,
                tgt_f: str, tgt_u: str) -> None:
    for k in (src_f, src_u, tgt_f, tgt_u):
        if k not in AXES:
            die(f"未知轴「{k}」；可用 {sorted(AXES)}")
    rot = basis(AXES[tgt_f], AXES[tgt_u]) @ basis(AXES[src_f], AXES[src_u]).transposed()
    ob.matrix_world = rot.to_4x4() @ ob.matrix_world
    apply_transform(ob)


def step_scale(ob: bpy.types.Object, target: Vector, fit: str) -> tuple[Vector, Vector]:
    """缩放到声明包围盒。返回 (缩放前实测尺寸, 逐轴比例因子)。"""
    lo, hi = world_bounds(ob)
    dims = hi - lo
    if min(dims) <= 1e-9:
        die(f"来源包围盒退化：{tuple(round(d, 4) for d in dims)}")
    ratios = Vector((target[i] / dims[i] for i in range(3)))
    if fit == "stretch":
        ob.scale = ratios
    else:
        if fit == "cover":
            s = max(ratios)
        elif fit == "mean":
            s = sum(ratios) / 3.0
        else:                       # uniform：按最长的声明轴定标，
            longest = max(range(3), key=lambda i: target[i])   # 其余两轴的偏差
            s = ratios[longest]                                # 留给验收去发现
        ob.scale = Vector((s, s, s))
    apply_transform(ob)
    return dims, ratios


def step_origin(ob: bpy.types.Object) -> None:
    """原点落底面中心（轮胎接地平面），不是几何中心。"""
    lo, hi = world_bounds(ob)
    ground = Vector(((lo.x + hi.x) / 2.0, (lo.y + hi.y) / 2.0, lo.z))
    ob.data.transform(Matrix.Translation(-ground))
    ob.matrix_world = Matrix.Translation(Vector((0.0, 0.0, 0.0)))
    bpy.context.view_layer.update()


def step_strip_materials(ob: bpy.types.Object) -> int:
    n = len(ob.data.materials)
    ob.data.materials.clear()
    for img in list(bpy.data.images):
        if img.users == 0:
            bpy.data.images.remove(img)
    return n


def apply_transform(ob: bpy.types.Object) -> None:
    bpy.ops.object.select_all(action="DESELECT")
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


# ---------------------------------------------------------------- 验收探针

@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    fatal: bool = True


def local_verts(ob: bpy.types.Object) -> list[Vector]:
    return [v.co.copy() for v in ob.data.vertices]


def norm_coords(verts: list[Vector], lo: Vector, hi: Vector) -> list[Vector]:
    """归一化到包围盒 0..1，让 spec 里的区域声明与真实尺寸解耦。"""
    span = Vector((max(hi[i] - lo[i], 1e-9) for i in range(3)))
    return [Vector(((v[i] - lo[i]) / span[i] for i in range(3))) for v in verts]


def probe_occupancy(nv: list[Vector], spec: dict,
                    faces: list[tuple[Vector, float]] | None = None) -> Check:
    """声明区域内是否有几何。

    默认判据是**面积占比**而不是顶点数，因为顶点数是密度相关的：
    一个 320 顶点的脚本 blockout 与一个十万顶点的 image-to-3D 网格，
    描述同一个结构时顶点数差三个数量级，绝无可能共用一个绝对阈值——
    而闸门的意义正是"同一份验收清单能验任何来源的网格"。
    面积占比是密度无关的：一块用 2 个三角形描述的扩散器底板，
    与用 2000 个三角形描述的同一块板，面积占比相同。
    `最少顶点` 保留为可选的绝对下限，二者都声明时须同时满足。
    """
    box = spec.get("区域", {})
    rx = box.get("x", [0.0, 1.0])
    ry = box.get("y", [0.0, 1.0])
    rz = box.get("z", [0.0, 1.0])

    def inside(v: Vector) -> bool:
        return (rx[0] <= v.x <= rx[1] and ry[0] <= v.y <= ry[1]
                and rz[0] <= v.z <= rz[1])

    n = sum(1 for v in nv if inside(v))
    bits = [f"顶点 {n}"]
    ok = True

    need_v = spec.get("最少顶点")
    if need_v is not None:
        ok = ok and n >= int(need_v)
        bits[-1] += f"/≥{int(need_v)}"

    need_a = spec.get("最少面积占比")
    if need_a is not None and faces:
        total = sum(a for _, a in faces) or 1e-9
        got = sum(a for c, a in faces if inside(c)) / total
        ok = ok and got >= float(need_a)
        bits.append(f"面积占比 {got * 100:.2f}%/≥{float(need_a) * 100:.2f}%")

    if need_v is None and need_a is None:
        ok = n >= 8
        bits[-1] += "/≥8(默认)"

    return Check(
        name=str(spec.get("名称", "占位")),
        ok=ok,
        detail=f"区域内 {'  '.join(bits)}  x{rx} y{ry} z{rz}",
    )


def probe_section(nv: list[Vector], spec: dict, dims: Vector) -> Check:
    """两个带之间的截面尺寸关系。管"外鼓/收窄"这类没有硬边、占位探针测不到的特征。"""
    axis = {"x": 0, "y": 1, "z": 2}
    meas = axis[str(spec.get("测量轴", "x")).lower()]
    band = axis[str(spec.get("分带轴", "y")).lower()]
    ba = spec.get("带A", [0.0, 0.2])
    bb = spec.get("带B", [0.4, 0.6])
    rel = str(spec.get("关系", "A > B"))
    min_gap = float(spec.get("最小差", 0.0))
    # 第三轴限定（可选）。没有它，突出于主体的附件会把主体自身的鼓凹信号淹掉——
    # 例如量"后轮拱是否外鼓于车身中段"时，两个带量到的都是外凸的轮子而非车身。
    third = ({0, 1, 2} - {meas, band}).pop()
    lim = spec.get("限定", [0.0, 1.0])

    def extent(band_range: list[float]) -> tuple[float, int]:
        vals = [v[meas] for v in nv
                if band_range[0] <= v[band] <= band_range[1]
                and lim[0] <= v[third] <= lim[1]]
        return ((max(vals) - min(vals)) * dims[meas] if vals else 0.0), len(vals)

    (ea, na), (eb, nb) = extent(ba), extent(bb)
    # 空带必须判失败，不能当 0 宽度参与比较——否则 "A > B" 在 B 空时平凡成立，
    # 探针会给出假通过。空带说明带的范围划错了（或该结构根本不存在），两者都该报出来。
    if na == 0 or nb == 0:
        empty = "带A" if na == 0 else ("带B" if nb else "带A+带B")
        return Check(
            name=str(spec.get("名称", "截面对比")),
            ok=False,
            detail=f"{empty} 区间内无几何（A {na} 点 / B {nb} 点）——"
                   f"带范围划错，或该结构不存在",
        )
    # 方向由**哪一侧在前**决定，不能只看有没有 ">"——"A > B" 与 "B > A" 都含 ">"。
    lhs = rel.replace(" ", "")[:1].upper()
    bigger_is_a = (lhs == "A") == (">" in rel)
    gap = ea - eb if bigger_is_a else eb - ea
    # 上界（可选）。有些特征要判的不是"A 明显大于 B"，而是"A 不该比 B 大太多"——
    # 例如"轮拱必须包住轮子"：轮心高度的车宽若远大于轮子正上方的车宽，
    # 说明轮子是外凸地贴在车身上、根本没有轮拱。这类缺陷只有上界能表达。
    max_gap = spec.get("最大差")
    if max_gap is not None:
        return Check(
            name=str(spec.get("名称", "截面对比")),
            ok=gap <= float(max_gap),
            detail=f"带A {ea:.3f}m 带B {eb:.3f}m  差 {gap:+.3f}m / 上限 ≤{float(max_gap):.3f}m ({rel})",
        )
    return Check(
        name=str(spec.get("名称", "截面对比")),
        ok=gap >= min_gap,
        detail=f"带A {ea:.3f}m 带B {eb:.3f}m  差 {gap:+.3f}m / 需要 ≥{min_gap:.3f}m ({rel})",
    )


def loose_parts(ob: bpy.types.Object) -> int:
    """松散块数。image-to-3D 常把薄件甩成独立碎块或干脆丢掉，块数是廉价的健康信号。"""
    seen: set[int] = set()
    adj: dict[int, list[int]] = {}
    for e in ob.data.edges:
        a, b = e.vertices
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    parts = 0
    for start in range(len(ob.data.vertices)):
        if start in seen:
            continue
        parts += 1
        stack = [start]
        seen.add(start)
        while stack:
            cur = stack.pop()
            for nxt in adj.get(cur, ()):
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
    return parts


# ---------------------------------------------------------------- 主流程

def parse_args() -> argparse.Namespace:
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser(description="白模归一化 + 验收闸门")
    ap.add_argument("--src", required=True, help="来源网格（glb/gltf/obj/fbx/stl/ply/blend）")
    ap.add_argument("--spec", required=True, help="object.toml")
    ap.add_argument("--out", help="目标 .blend；--qc-only 时可省")
    ap.add_argument("--fit", default="uniform",
                    choices=("uniform", "stretch", "cover", "mean"),
                    help="uniform=按最长轴等比（默认，保留比例缺陷以便验收发现）；"
                         "stretch=逐轴精确贴合")
    ap.add_argument("--qc-only", action="store_true", help="只体检，不归一化不写盘")
    # 源朝向每换一版生成网格就可能不同，改 toml 太重——命令行覆盖，toml 里那个值当默认。
    ap.add_argument("--src-forward", help="覆盖 spec 的 [几何].源朝向.前，如 +Y / -Z")
    ap.add_argument("--src-up", help="覆盖 spec 的 [几何].源朝向.上")
    return ap.parse_args(argv)


def resolve(p: str) -> Path:
    q = Path(p)
    return q if q.is_absolute() else (REPO / q).resolve()


def main() -> None:
    args = parse_args()
    src, spec_path = resolve(args.src), resolve(args.spec)
    if not src.is_file():
        die(f"来源不存在：{src}")
    if not spec_path.is_file():
        die(f"spec 不存在：{spec_path}")
    spec = tomllib.loads(spec_path.read_text(encoding="utf-8"))

    obj_spec = spec.get("对象", {})
    geo = spec.get("几何", {})
    name = str(obj_spec.get("名称") or src.stem)
    target = Vector([float(x) for x in geo.get("尺寸", (1, 1, 1))])
    tol = float(geo.get("容差", 0.05))
    src_f = args.src_forward or str(geo.get("源朝向", {}).get("前", "+Y"))
    src_u = args.src_up or str(geo.get("源朝向", {}).get("上", "+Z"))
    tgt_f = str(geo.get("目标朝向", {}).get("前", "+Y"))
    tgt_u = str(geo.get("目标朝向", {}).get("上", "+Z"))

    wipe_scene()
    ob = join_meshes(import_source(src), name)

    n_mat = 0
    raw_dims = ratios = Vector((0, 0, 0))
    if not args.qc_only:
        step_orient(ob, src_f, src_u, tgt_f, tgt_u)
        raw_dims, ratios = step_scale(ob, target, args.fit)
        step_origin(ob)
        n_mat = step_strip_materials(ob)

    lo, hi = world_bounds(ob)
    dims = hi - lo
    # 探针在**局部坐标**的包围盒里归一化：spec 的区域声明因此与摆放和尺寸都无关，
    # 同一份验收清单能复用到重生成的任何一版网格上。
    verts = local_verts(ob)
    l_lo = Vector((min(v[i] for v in verts) for i in range(3)))
    l_hi = Vector((max(v[i] for v in verts) for i in range(3)))
    nv = norm_coords(verts, l_lo, l_hi)
    # 面质心（归一化坐标）+ 面积，供密度无关的面积占比判据用
    _span = Vector((max(l_hi[i] - l_lo[i], 1e-9) for i in range(3)))
    faces = [
        (Vector(((f.center[i] - l_lo[i]) / _span[i] for i in range(3))), f.area)
        for f in ob.data.polygons
    ]

    checks: list[Check] = []

    dev = [abs(dims[i] - target[i]) / max(target[i], 1e-9) for i in range(3)]
    checks.append(Check(
        "包围盒",
        max(dev) <= tol,
        f"实测 {dims.x:.3f} × {dims.y:.3f} × {dims.z:.3f} m  / "
        f"声明 {target.x:.3f} × {target.y:.3f} × {target.z:.3f} m  "
        f"最大偏差 {max(dev) * 100:.1f}% / 容差 {tol * 100:.0f}%",
    ))

    checks.append(Check(
        "原点在接地面",
        abs(lo.z) <= 1e-3 and abs((lo.x + hi.x) / 2) <= 1e-3 and abs((lo.y + hi.y) / 2) <= 1e-3,
        f"底面 z={lo.z:+.4f}  中心 xy=({(lo.x + hi.x) / 2:+.4f}, {(lo.y + hi.y) / 2:+.4f})",
    ))

    checks.append(Check(
        "无材质残留",
        len(ob.data.materials) == 0,
        f"剩余 {len(ob.data.materials)} 个（本次剥掉 {n_mat} 个）",
    ))

    parts = loose_parts(ob)
    checks.append(Check(
        "松散块数",
        parts <= int(geo.get("最多松散块", 40)),
        f"{parts} 块 / 上限 {int(geo.get('最多松散块', 40))}",
        fatal=False,
    ))

    for item in spec.get("验收", []):
        kind = str(item.get("类型", "占位"))
        if kind == "占位":
            checks.append(probe_occupancy(nv, item, faces))
        elif kind == "截面对比":
            checks.append(probe_section(nv, item, dims))
        else:
            checks.append(Check(str(item.get("名称", "?")), False,
                                f"未知验收类型「{kind}」"))

    print("\n" + "=" * 72)
    print(f"[whitemodel] {name}   来源 {src.name}   fit={args.fit}"
          f"{'   (QC ONLY)' if args.qc_only else ''}")
    print(f"  面数 {len(ob.data.polygons)}   顶点 {len(ob.data.vertices)}")
    if not args.qc_only and args.fit != "stretch":
        print(f"  来源比例体检：逐轴需要的比例因子 "
              f"{ratios.x:.3f} / {ratios.y:.3f} / {ratios.z:.3f} "
              f"—— 三者越接近，说明生成网格的比例越贴合声明")
    print("=" * 72)

    bad = 0
    for c in checks:
        mark = "✓" if c.ok else ("✗" if c.fatal else "!")
        print(f"  {mark} {c.name:<16} {c.detail}")
        if not c.ok and c.fatal:
            bad += 1

    if not args.qc_only:
        if not args.out:
            die("缺 --out")
        out = resolve(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=str(out))
        print(f"\n  写出 {out}")

    print("=" * 72)
    if bad:
        print(f"[whitemodel] ✗ 验收未通过：{bad} 项硬失败。"
              f"重生成、或用脚本补件后再过一遍。\n")
        sys.exit(1)
    print("[whitemodel] ✓ 全部通过\n")


if __name__ == "__main__":
    main()
