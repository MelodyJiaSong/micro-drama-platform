from __future__ import annotations

import re
from pathlib import Path

REFERENCE_MODE = "character_reference_mode"
UPLOAD_MODE = "uploads"
CHARACTER_PATTERN = r"[cm]\d+_[A-Za-z0-9_]+"
VOICE_PATTERN = r"[a-z]{2,3}-[mfx]-[a-z0-9-]+"
REFERENCE_USAGE = "每个角色的三张视图只锁同一人的长相与服装，不代表三个人，不锁姿势；声音参考只锁对应角色音色，不复述声样内容；只演本镜台词，未发声角色不说话"


def audio_sample(root: Path) -> Path:
    named = root / "views" / f"{root.name}_audio.mp3"
    legacy = root / "views" / "views.mp3"
    hits = [p for p in (named, legacy) if p.is_file()]
    if len(hits) > 1:
        raise ValueError(f"{root.name}声样MP3不唯一")
    return hits[0] if hits else named


class CharacterReferences:
    def __init__(self, drama: Path, card: str, views: Path | None = None) -> None:
        if re.fullmatch(CHARACTER_PATTERN, card) is None:
            raise ValueError(f"无效人物卡键：{card}")
        roots = list(drama.glob(f"2_*/characters/{card}"))
        if len(roots) != 1:
            raise ValueError(f"{card}人物卡目录不唯一或缺失")
        self.card = card
        self.root = roots[0]
        self.views = views or self.root / "views"
        if not self.views.resolve().is_relative_to(self.root.resolve()):
            raise ValueError(f"{card}视图不属于该角色目录")

    def voice_id(self, required: bool = True) -> str:
        text = (self.root / f"{self.card}.md").read_text(encoding="utf-8")
        ids = set(re.findall(r"\bvoice_id\b(?:[*` \t]*)(?:[（(][^\n）)]*[）)])?[*` \t]*[:：|=][*` \t]*([A-Za-z][A-Za-z0-9_-]+)", text))
        if not ids and not required:
            return ""
        if len(ids) != 1:
            raise ValueError(f"{self.card}voice_id缺失或不唯一：{sorted(ids)}")
        return ids.pop()

    def files(self, voiced: bool = False, combined: bool = False) -> list[tuple[str, Path, str]]:
        numbered = [self.views / f"views{i}.png" for i in (1, 2, 3)]
        named = [self.views / f"{self.card}_{side}.png" for side in ("front", "side", "back")]
        prefix = self.views.name.split("_", 1)[0]
        outfit_named = [self.views / f"{prefix}_{side}.png" for side in ("front", "side", "back")]
        outfit = [self.views / f"{prefix}-{i}_{side}.png" for i, side in enumerate(("正面", "侧面", "背面"), 1)]
        candidates = [paths for paths in (numbered, named, outfit_named, outfit) if all(p.is_file() for p in paths)]
        if len(candidates) != 1:
            raise ValueError(f"{self.card}需要唯一完整的三张视图：{self.views}")
        result = [(f"{self.card}视图{i}", path, "人物三面视图")
                  for i, path in enumerate(candidates[0], 1)]
        if combined:
            stem = self.card if self.views.name == 'views' else prefix
            sheet = self.views / f'{stem}_views.png'
            if not sheet.is_file():
                raise ValueError(f'{self.card}三视图合图缺失：{sheet}')
            import hashlib
            import json
            from PIL import Image
            with Image.open(sheet) as image:
                recorded = json.loads(image.info.get('character_sheet_sources', '[]'))
            expected = [{'role': role, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
                        for role, path in zip(('front', 'side', 'back'), candidates[0])]
            if recorded != expected:
                raise ValueError(f'{self.card}三视图合图与源图不一致，须重新合成：{sheet}')
            result = [(f'{self.card}三视图', sheet, '人物三视图合图')]
        if voiced:
            audio = audio_sample(self.root)
            if not audio.is_file():
                raise ValueError(f"{self.card}声样MP3缺失或不唯一")
            self.voice_id()
            result.append((f"{self.card}声音", audio, "声音音频"))
        return result

    @staticmethod
    def usage(voices: dict[str, str], combined: bool = False) -> str:
        binding = "、".join(f"{card}声音＝{speaker}" for card, speaker in voices.items())
        usage = REFERENCE_USAGE
        if combined:
            usage = usage.replace('三张视图', '三视图合图').replace('不代表三个人', '三格按front/side/back源文件顺序合成，实际角度以图为准，不保证严格正交，是同一人的不同角度，不代表三个人')
        return usage + ("；音色对应：" + binding if binding else "")
