from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

SCENES_DIR_NAME = "scenes"
BACKGROUND_DIR_NAME = "background"
SCENE_ID_RE = re.compile(r"s([1-9]\d*)\Z")
SHOT_ID_RE = re.compile(r"st([1-9]\d*)\Z")
# 镜组 (follow-up 331): consecutive shots of one scene generated in one call; `g2` within a scene, `ep1_s1_g2` in full.
GROUP_ID_RE = re.compile(r"g([1-9]\d*)\Z")
GROUP_KEY_RE = re.compile(r"ep([1-9]\d*)_s([1-9]\d*)_g([1-9]\d*)\Z")
GROUPS_DIR_NAME = "groups"
EPISODE_ID_RE = re.compile(r"ep(\d+)\Z", re.I)
SHOT_KEY_RE = re.compile(r"(?<![a-z0-9])ep([1-9]\d*)_s([1-9]\d*)_st([1-9]\d*)(?![a-z0-9])", re.I)
SHOT_KEY_HINT_RE = re.compile(r"(?<![a-z0-9])ep\d+_s(?!hot)\d*", re.I)


@dataclass(frozen=True)
class ShotKey:
    episode: int
    scene: int
    shot: int

    @property
    def value(self) -> str:
        return f"ep{self.episode}_s{self.scene}_st{self.shot}"

    def folder(self, episode: Path) -> Path:
        return episode / SCENES_DIR_NAME / f"s{self.scene}" / "shots" / f"st{self.shot}"


def shot_key(episode: str, scene: str, shot: str) -> ShotKey:
    ep, sc, st = EPISODE_ID_RE.fullmatch(episode), SCENE_ID_RE.fullmatch(scene), SHOT_ID_RE.fullmatch(shot)
    if ep is None or sc is None or st is None or int(ep[1]) < 1:
        raise ValueError("无效的集、场次或镜头编号")
    return ShotKey(int(ep[1]), int(sc[1]), int(st[1]))


def group_key(episode: str, scene: str, group: str) -> str:
    """`ep1_s1_g2`: the 镜组 key; its folder is `scenes/s1/groups/g2/`."""
    ep, sc, g = EPISODE_ID_RE.fullmatch(episode), SCENE_ID_RE.fullmatch(scene), GROUP_ID_RE.fullmatch(group)
    if ep is None or sc is None or g is None or int(ep[1]) < 1:
        raise ValueError("无效的集、场次或镜组编号")
    return f"ep{int(ep[1])}_s{int(sc[1])}_g{int(g[1])}"


def first_shot_key(name: str) -> ShotKey | None:
    match = SHOT_KEY_RE.search(name)
    hint = SHOT_KEY_HINT_RE.search(name)
    if match is None or (hint is not None and hint.start() != match.start()):
        return None
    return ShotKey(*(int(n) for n in match.groups()))


def folder_shot_key(folder: Path) -> ShotKey | None:
    if folder.parent.name != "shots" or folder.parent.parent.parent.name != SCENES_DIR_NAME:
        return None
    try:
        return shot_key(folder.parents[3].name, folder.parent.parent.name, folder.name)
    except ValueError:
        return None


def shot_identity(folder: Path) -> str:
    key = folder_shot_key(folder)
    return key.value if key else folder.name
