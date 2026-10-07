"""Compose canonical character references without resizing or repainting."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, PngImagePlugin

ROLES = ('front', 'side', 'back')


def compose(folder: Path, prefix: str) -> dict:
    paths = [folder / f'{prefix}_{role}.png' for role in ROLES]
    sources = [{'role': role, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
               for role, path in zip(ROLES, paths)]
    images = []
    for path in paths:
        with Image.open(path) as image:
            images.append(image.convert('RGB'))
    height = max(image.height for image in images)
    width = max(image.width for image in images)
    result = Image.new('RGB', (width * 3, height), (128, 128, 128))
    boxes = []
    for i, image in enumerate(images):
        x, y = i * width + (width - image.width) // 2, (height - image.height) // 2
        result.paste(image, (x, y))
        boxes.append((x, y, x + image.width, y + image.height))
    info = PngImagePlugin.PngInfo()
    info.add_text('character_sheet_sources', json.dumps(sources, sort_keys=True))
    output = folder / f'{prefix}_views.png'
    if output.exists():
        with Image.open(output) as saved:
            if saved.size == result.size and saved.convert('RGB').tobytes() == result.tobytes() and saved.info.get('character_sheet_sources') == json.dumps(sources, sort_keys=True):
                return {'path': str(output), 'size': result.size, 'sources': sources, 'status': 'current'}
    result.save(output, pnginfo=info)
    with Image.open(output) as saved:
        for image, box in zip(images, boxes):
            assert saved.crop(box).tobytes() == image.tobytes(), output
    return {'path': str(output), 'size': result.size, 'sources': sources, 'status': 'built'}


def build(drama: Path) -> list[dict]:
    roots = list(drama.glob('2_*/characters'))
    if len(roots) != 1:
        raise ValueError('人物资产根目录缺失或不唯一')
    rows = []
    for character in sorted(roots[0].iterdir()):
        if not character.is_dir():
            continue
        if (character / 'views').is_dir():
            rows.append(compose(character / 'views', character.name))
        for folder in sorted(character.iterdir()):
            if folder.is_dir() and folder.name.startswith(character.name.split('_', 1)[0] + '-'):
                prefix = folder.name.split('_', 1)[0]
                rows.append(compose(folder, prefix))
    return rows


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('drama', type=Path)
    args = parser.parse_args()
    rows = build(args.drama)
    print(json.dumps(rows, ensure_ascii=False, indent=2))
