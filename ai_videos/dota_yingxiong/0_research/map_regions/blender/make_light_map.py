"""给总装做“轻量查看版”：外部库与本地重网格减面、贴图降分辨率，另存新库与新总装（follow-up 299）。

只用于在界面里快速打开看布局；出检查图、精修仍用原总装。原库、原总装不动。
两步：
  1) 库：blender -b -P make_light_map.py -- libs --src <总装> [--only 序号,序号]
     每个外部库 → lod_libraries/light_v001/<库名>/<库名>.blend
  2) 总装：blender -b -P make_light_map.py -- map --src <总装> --dst <轻量总装>
     库路径改指 light_v001，本地重网格减面、本地贴图降分辨率
"""
from pathlib import Path
import argparse, json, sys
import bpy

DRAMA = Path(__file__).resolve().parents[3]
OUT = next(DRAMA.glob('2_*')) / 'background/map_3d'
LIGHT = OUT / 'lod_libraries/light_v001'
MAX_FACES_PER_LIB = 60000   # 每个库（一个资产）总面数上限
MAX_FACES_LOCAL = 150000    # 总装本地单个网格上限；地形单列
TERRAIN_FACES = 262144
TEX_MAX = 1024

p = argparse.ArgumentParser()
p.add_argument('step', choices=['libs', 'map'])
p.add_argument('--src', required=True)
p.add_argument('--dst')
p.add_argument('--only', default='')
args = p.parse_args(sys.argv[sys.argv.index('--') + 1:])


def lib_key(path):
    # 同名库（例如两个 bg16.blend）加上级目录区分
    path = Path(path)
    return path.stem if path.parent.name != path.stem else f'{path.parent.parent.name}_{path.stem}'


def decimate(mesh, ratio):
    # 临时物体求值减面，再把所有使用者换到新网格；UV、材质随网格保留
    ob = bpy.data.objects.new('_light_tmp', mesh)
    bpy.context.scene.collection.objects.link(ob)
    mod = ob.modifiers.new('light', 'DECIMATE')
    mod.ratio = max(ratio, 0.002)
    new = bpy.data.meshes.new_from_object(ob.evaluated_get(bpy.context.evaluated_depsgraph_get()))
    bpy.data.objects.remove(ob)
    new.name = mesh.name
    mesh.user_remap(new)
    bpy.data.meshes.remove(mesh)
    return len(new.polygons)


def shrink_images(images):
    n = 0
    for img in images:
        if img.source != 'FILE':
            continue
        w, h = img.size  # 读文件头；缺失贴图为 0×0，跳过
        if max(w, h) <= TEX_MAX:
            continue
        s = TEX_MAX / max(w, h)
        img.scale(max(1, int(w * s)), max(1, int(h * s)))
        img.pack()  # 降分辨率后的像素打包进轻量库，不回写原贴图文件
        n += 1
    return n


def faces(meshes):
    return sum(len(m.polygons) for m in meshes)


if args.step == 'libs':
    bpy.ops.wm.open_mainfile(filepath=str(OUT / args.src))
    libs = [bpy.path.abspath(l.filepath) for l in bpy.data.libraries]
    only = {int(i) for i in args.only.split(',') if i}
    for i, lib in enumerate(libs):
        if only and i not in only:
            continue
        key = lib_key(lib)
        dest = LIGHT / key / f'{key}.blend'
        if dest.exists():
            print('SKIP', i, key, flush=True)
            continue
        bpy.ops.wm.open_mainfile(filepath=lib)
        meshes = [m for m in bpy.data.meshes if not m.library and m.users]
        before = faces(meshes)
        ratio = min(1.0, MAX_FACES_PER_LIB / max(before, 1))
        after = before
        if ratio < 1.0:
            after = sum(decimate(m, ratio) for m in meshes)
        shrunk = shrink_images([im for im in bpy.data.images if not im.library])
        dest.parent.mkdir(parents=True, exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=str(dest), relative_remap=True, compress=True)
        (dest.parent / 'light_report.json').write_text(json.dumps({
            'followup': 299, 'source': lib, 'faces_before': before, 'faces_after': after,
            'images_shrunk_to': TEX_MAX, 'images_shrunk': shrunk, 'note': '轻量查看版，不用于出检查图',
        }, ensure_ascii=False, indent=2), encoding='utf-8')
        print('LIB_DONE', i, key, before, after, shrunk, flush=True)
else:
    dest = OUT / args.dst
    if dest.exists():
        raise FileExistsError(dest)
    bpy.ops.wm.open_mainfile(filepath=str(OUT / args.src))
    remapped, missing = {}, []
    for lib in bpy.data.libraries:
        src = bpy.path.abspath(lib.filepath)
        key = lib_key(src)
        light = LIGHT / key / f'{key}.blend'
        if not light.exists():
            missing.append(src)
            continue
        lib.filepath = str(light)
        remapped[key] = src
    if missing:
        raise RuntimeError(('轻量库未生成', missing))
    local = []
    for m in [m for m in bpy.data.meshes if not m.library and m.users]:
        n = len(m.polygons)
        cap = TERRAIN_FACES if m.name == 'Terrain_683d' else MAX_FACES_LOCAL
        if n > cap:
            local.append({'mesh': m.name, 'before': n, 'after': decimate(m, cap / n)})
    shrunk = shrink_images([im for im in bpy.data.images if not im.library])
    scene = bpy.context.scene
    scene.render.use_simplify = True
    scene[f'light_view'] = 'followup 299: 轻量查看版，只看布局；出图与精修用原总装'
    bpy.ops.wm.save_as_mainfile(filepath=str(dest), relative_remap=True, compress=True)
    (OUT / f'{dest.stem}_report.json').write_text(json.dumps({
        'followup': 299, 'source': args.src, 'file': dest.name, 'libraries': remapped,
        'local_decimated': local, 'local_images_shrunk': shrunk, 'tex_max': TEX_MAX,
        'max_faces_per_lib': MAX_FACES_PER_LIB,
    }, ensure_ascii=False, indent=2), encoding='utf-8')
    print('MAP_SAVED', dest, flush=True)
