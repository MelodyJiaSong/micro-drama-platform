"""人物卡的样片与正片（follow-up 286）：人物视频、各技能的草稿与正式条、接进了这个人物素材的剪辑成片。只读。

人物目录 `characters/[{分组}/]{卡}/`：`{卡}_turntable.mp4` 是人物视频；`skills/k{号}_{名}/` 每个技能一张卡，
`{目录}.md` 首个 `# ` 行是技能名，`icon/{键}_icon*.png` 图标，`{目录}_peak.png`（没有就取版本号最大的
`{目录}_peak_v{N}.png`）峰值图，`drafts/` 与 `renders/` 的每条生成由 `ShotRendersReader` 读（同镜头生成记录）。
成片（`SceneCutReader` 读）：人物目录 `demo/edit/{draft,final}/cut_v{N}.json` 全算（follow-up 288，没有分集的剧把英雄 demo 放这里）；
`{剧}/episodes/ep*/edit/{draft,final}/cut_v{N}.json` 任一 `events[].clip` 在人物目录下才算；没有 `episodes/` 的剧照常。
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from libs.common import drama_ref
from libs.common.asset_group import is_character_name
from libs.common.safe_resolve import SafeResolver
from libs.domain.errors.character_video__error import NotCharacterCardDirError
from libs.infrastructure.daos.character_reel__dao import CharacterReelDao, SkillCardDao
from libs.infrastructure.readers.scene_cut__reader import SceneCutReader
from libs.infrastructure.readers.shot_renders__reader import DRAFTS, RENDERS, ShotRendersReader

CHARACTERS = "characters"
SKILLS = "skills"
EPISODES = "episodes"
DEMO = "demo"
TURNTABLE_SUFFIX = "_turntable.mp4"
SKILL_DIR_RE = re.compile(r"^k(\d+)_.+$")
PEAK_VERSION_RE = re.compile(r"_peak_v(\d+)\.png$")
TITLE_RE = re.compile(r"^# (.+)$", re.M)


class CharacterReelReader:
    def __init__(self, repo_root: Path) -> None:
        self.root = repo_root
        self.resolver = SafeResolver(repo_root)
        self.renders = ShotRendersReader(repo_root)
        self.cuts = SceneCutReader(repo_root)

    def _rel(self, path: Path) -> str:
        return path.relative_to(self.root).as_posix()

    def _file(self, path: Path) -> str:
        return self._rel(path) if path.is_file() and not path.is_symlink() else ""

    def card_dir(self, rel: str) -> tuple[Path, str]:
        """(人物目录, 剧根的仓库相对路径)；不是 `characters/[{分组}/]{卡}` 抛 NotCharacterCardDirError。"""
        norm = rel.strip().rstrip("/")
        parts = norm.split("/")
        resolved = self.resolver.resolve(norm)
        depth = drama_ref.asset_root_depth(self.root, parts)
        if resolved is None or depth is None or not resolved.is_dir() or not is_character_name(parts[-1]):
            raise NotCharacterCardDirError(f"不是人物卡目录：{rel}")
        inside = parts[depth:-1]
        if not (inside[-1:] == [CHARACTERS] or (len(inside) >= 2 and inside[-2] == CHARACTERS and not is_character_name(inside[-1]))):
            raise NotCharacterCardDirError(f"不在 characters/ 下：{rel}")
        return resolved, "/".join(parts[:depth])

    def read(self, rel: str) -> CharacterReelDao:
        folder, drama = self.card_dir(rel)
        prefix = self._rel(folder) + "/"
        return CharacterReelDao(folder.name, self._rel(folder), drama, self._file(folder / f"{folder.name}{TURNTABLE_SUFFIX}"),
                                self._skills(folder / SKILLS), self._cuts(folder, drama, prefix))

    def _skills(self, skills: Path) -> list[SkillCardDao]:
        if not skills.is_dir() or skills.is_symlink():
            return []
        out = []
        for entry in skills.iterdir():
            match = SKILL_DIR_RE.match(entry.name)
            if not match or not entry.is_dir() or entry.is_symlink():
                continue
            card = entry / f"{entry.name}.md"
            text = card.read_text(encoding="utf-8") if card.is_file() else ""
            title = TITLE_RE.search(text)
            key = f"k{match.group(1)}"
            icons = sorted(p for p in (entry / "icon").glob(f"{key}_icon*.png") if p.is_file()) if (entry / "icon").is_dir() else []
            out.append(SkillCardDao(key, int(match.group(1)), self._rel(entry), title.group(1).strip() if title else entry.name,
                                    self._file(card), self._rel(icons[0]) if icons else "", self._peak(entry),
                                    self.renders.takes(entry / DRAFTS), self.renders.takes(entry / RENDERS)))
        return sorted(out, key=lambda s: s.number)

    def _peak(self, skill: Path) -> str:
        exact = self._file(skill / f"{skill.name}_peak.png")
        if exact:
            return exact
        versions = [(int(m.group(1)), p) for p in skill.glob(f"{skill.name}_peak_v*.png") if (m := PEAK_VERSION_RE.search(p.name))]
        return self._rel(max(versions)[1]) if versions else ""

    def _cuts(self, folder: Path, drama: str, prefix: str) -> dict[str, list[dict[str, Any]]]:
        """人物目录 demo/ 的剪辑在前（带 `_own`），再接各集里用到这个人物素材的剪辑。"""
        out: dict[str, list[dict[str, Any]]] = {}
        demo = folder / DEMO
        if demo.is_dir() and not demo.is_symlink():
            for stage, found in self.cuts.cuts(self._rel(demo), None).items():
                out.setdefault(stage, []).extend({**c, "_episode": DEMO, "_own": True} for c in found)
        episodes = self.root / drama / EPISODES
        for episode in sorted(episodes.iterdir()) if episodes.is_dir() else []:
            if not episode.is_dir() or episode.is_symlink() or episode.name.startswith((".", "_")):
                continue
            for stage, found in self.cuts.cuts(self._rel(episode), None).items():
                mine = [{**c, "_episode": episode.name} for c in found if _uses(c, prefix)]
                out.setdefault(stage, []).extend(mine)
        return out

    def exists(self, rel: str) -> bool:
        return self.cuts.exists(rel)


def _uses(cut: dict[str, Any], prefix: str) -> bool:
    events = cut.get("events")
    return isinstance(events, list) and any(isinstance(e, dict) and isinstance(e.get("clip"), str) and e["clip"].startswith(prefix)
                                            for e in events)
