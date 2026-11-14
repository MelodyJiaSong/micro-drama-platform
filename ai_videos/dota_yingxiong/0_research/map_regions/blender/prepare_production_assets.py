from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


DRAMA = Path(__file__).resolve().parents[3]
WORLD = next(DRAMA.glob('2_*'))
OUTPUT = WORLD / 'background' / 'map_3d'


def reference(path: Path) -> dict:
    return {
        'path': path.relative_to(DRAMA).as_posix(),
        'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def inventory() -> dict:
    assets = []
    directories = list((WORLD / 'background').glob('*/bg*'))
    for path in (WORLD / 'characters').glob('*/m*'):
        match = re.match(r'm(\d+)_', path.name)
        if match and (int(match[1]) < 100 or 300 <= int(match[1]) < 400):
            directories.append(path)
    for path in directories:
        if not path.is_dir():
            continue
        kind = 'building' if path.name.startswith('bg') else 'npc'
        views = {}
        for direction in ('front', 'side', 'back'):
            source = path / 'views' / f'{path.name}_{direction}.png'
            if source.is_file():
                views[direction] = reference(source)
        if kind == 'building' and not views:
            continue
        card = path / f'{path.name}.md'
        anchor = path / f'{path.name}.png'
        if not card.exists():
            raise FileNotFoundError(card)
        text = card.read_text(encoding='utf-8')
        scale_lines = [line for line in text.splitlines()
                       if any(term in line for term in ('尺度：', '身高', '体型 / 年龄 / 种族'))]
        model_dir = path / 'model_3d'
        assets.append({
            'id': path.name.split('_')[0],
            'name': path.name,
            'kind': kind,
            'directory': path.relative_to(DRAMA).as_posix(),
            'card': reference(card),
            'anchor': reference(anchor) if anchor.is_file() else None,
            'views': views,
            'scale_evidence': scale_lines,
            'model_directory': model_dir.relative_to(DRAMA).as_posix(),
            'status': 'queued' if anchor.is_file() or views else 'missing_reference',
            'review': 'not_reviewed',
        })
    assets.sort(key=lambda a: (a['kind'], int(re.search(r'\d+', a['id'])[0])))
    sources = [DRAMA / '0_research' / p for p in (
        'base_layout_refs/base_layout_manifest.json',
        'base_layout_refs/terrain_samples.json',
        'map_regions/map_features.json',
        'map_regions/navigation/tree_positions.json',
        'map_regions/navigation/war3map.doo',
        'map_regions/blender/common.json',
    )]
    return {
        'schema': 1,
        'followups': [287, 288],
        'title': 'DotA 6.83d 精细三维地图与静态 NPC',
        'status': 'in_progress',
        'vision': '宏大绚丽的战场上，比记忆里更真实、更立体的英雄，放出比记忆里更绚丽的技能。',
        'scope': {
            'include': ['全部单体建筑', '商人', '兵线小兵', '野怪与肉山', '地形水面', '树木岩石及地图固定物'],
            'exclude': ['英雄', '召唤物', '骨骼绑定', '动画'],
            'hyper3d': False,
            'dinov3_exception': '用户明确允许，仅限本次任务；follow-up 288',
            'noncommercial_dependencies': '禁止用于本任务；使用前核实实际执行链',
        },
        'coordinate_system': {'east': '+X', 'north': '+Y', 'up': '+Z', 'units': 'metres',
                              'scale_source': '0_research/map_regions/blender/common.json:units_per_m'},
        'map_sources': [reference(p) for p in sources],
        'delivery': ['完整地图 .blend', '每个资产独立模型及材质', '全图及地面机位渲染', '逐资产来源与验收清单'],
        'quality_gate': ['轮廓与三视图一致', '真实厚度及背面', '尺度接地与原版位置', '材质无明显投影拉伸',
                         '地面机位观感', '独立审阅后才能标为完成'],
        'assets': assets,
    }


if __name__ == '__main__':
    OUTPUT.mkdir(parents=True, exist_ok=True)
    target = OUTPUT / 'asset_manifest.json'
    if target.exists():
        raise SystemExit(f'已有清单，禁止覆盖进度：{target}')
    data = inventory()
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(target)
    print({kind: sum(a['kind'] == kind for a in data['assets']) for kind in ('building', 'npc')})
    print('缺参考：', [a['id'] for a in data['assets'] if a['status'] == 'missing_reference'])
