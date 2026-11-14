"""把总装里个别资产的外部库改指向新版本库，另存新总装（follow-up 298）。

用法：blender -b -P remap_asset_libraries.py -- --src <总装> --dst <新总装> --map bg16=lod_libraries/m1_recolor_v001/bg16/bg16.blend [...]
--map 的路径相对 map_3d 目录。只改库路径，不动摆放与其他资产。
"""
from pathlib import Path
import argparse, json, sys
import bpy

DRAMA = Path(__file__).resolve().parents[3]
OUT = next(DRAMA.glob('2_*')) / 'background/map_3d'
p = argparse.ArgumentParser()
p.add_argument('--src', required=True)
p.add_argument('--dst', required=True)
p.add_argument('--map', nargs='+', required=True)
args = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
dest = OUT / args.dst
if dest.exists():
    raise FileExistsError(dest)
wanted = {}
for item in args.map:
    aid, rel = item.split('=', 1)
    target = (OUT / rel).resolve()
    if not target.exists():
        raise FileNotFoundError(target)
    wanted[aid] = target

bpy.ops.wm.open_mainfile(filepath=str(OUT / args.src))
done = {}
for aid, target in wanted.items():
    coll = bpy.data.collections.get(f'ASSET_{aid}')
    if not (coll and coll.library):
        raise RuntimeError(('资产不是外部库集合', aid))
    lib = coll.library
    before = bpy.path.abspath(lib.filepath)
    lib.filepath = str(target)
    done[aid] = {'before': before, 'after': str(target)}
bpy.ops.wm.save_as_mainfile(filepath=str(dest), relative_remap=True)
(OUT / f'{dest.stem}_report.json').write_text(json.dumps({
    'followup': 298, 'source': args.src, 'file': dest.name, 'remapped': done,
    'note': '只改库路径；重新打开后才加载新库内容',
}, ensure_ascii=False, indent=2), encoding='utf-8')
print('REMAP_SAVED', dest, flush=True)
