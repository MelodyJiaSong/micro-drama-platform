from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class CutEventQdto:
    """时间线上的一段：某镜某一条的入出点（可带与画面不同的声音区间），或缺镜占位。"""
    shot: str
    start: float                      # 在本版成片里的起点（秒）
    duration: float
    placeholder: bool = False
    take: str = ""
    cut_in: float | None = None
    cut_out: float | None = None
    audio_in: float | None = None     # 只有 J/L 剪辑（声音区间与画面不同）时才有
    audio_out: float | None = None
    reason: str = ""
    notes: list[str] = field(default_factory=list)
    text: list[str] = field(default_factory=list)   # 占位卡上写的分镜与台词


@dataclass(frozen=True)
class CutVersionQdto:
    """一版剪辑决定与它渲染出的片子（follow-up 269）。"""
    version: int
    stage: str                        # draft / final
    phase: str                        # 初接 / 粗剪 / 精剪 / 锁片
    status: str                       # 草稿 / 批准
    path: str                         # 剪辑决定 JSON 的仓库相对路径
    approved_by: str | None = None
    made_by: str = ""
    base_version: int | None = None
    video: str = ""                   # 干净版；没渲染或文件不在就是空
    labeled_video: str = ""           # 左上角烧了镜号 · 条 · 入出点的版本
    duration: float = 0.0
    rendered_at: str = ""
    shots: int = 0
    placeholders: int = 0
    events: list[CutEventQdto] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    violations: list[dict[str, Any]] = field(default_factory=list)
    error: str = ""


@dataclass(frozen=True)
class SceneCutsQdto:
    scene: str
    label: str
    draft: list[CutVersionQdto] = field(default_factory=list)   # 新的版本在前
    final: list[CutVersionQdto] = field(default_factory=list)


@dataclass(frozen=True)
class JoinSegmentQdto:
    """集级成片里的一场：接的是哪一版场剪辑、在成片里从哪儿开始。"""
    scene: str
    cut_version: int
    start: float
    duration: float


@dataclass(frozen=True)
class JoinTransitionQdto:
    """两场之间的转场（菜单见 libs/common/scene_cut.py）；at ＝ 下一场在成片里开始的时刻。"""
    from_scene: str
    to_scene: str
    type: str
    name: str
    duration: float
    at: float
    audio_j: float | None = None      # 下一场声音先进几秒
    audio_l: float | None = None      # 上一场声音拖后几秒
    reason: str = ""


@dataclass(frozen=True)
class EpisodeJoinQdto:
    """一版集级剪辑（follow-up 278）：把各场接起来的成片、转场、独立审稿结论。"""
    version: int
    stage: str
    phase: str
    status: str
    path: str
    approved_by: str | None = None
    base_version: int | None = None
    video: str = ""
    duration: float = 0.0
    rendered_at: str = ""
    head: str = ""
    tail: str = ""
    segments: list[JoinSegmentQdto] = field(default_factory=list)
    transitions: list[JoinTransitionQdto] = field(default_factory=list)
    review_verdict: str = ""          # 独立审稿结论；审的不是这版成片（sha 不符）时为空，review_stale 为真
    review_stale: bool = False
    review_items: list[str] = field(default_factory=list)
    changes: list[str] = field(default_factory=list)
    note: str = ""
    error: str = ""


@dataclass(frozen=True)
class GalleryEntryQdto:
    start: float
    label: str


@dataclass(frozen=True)
class GalleryQdto:
    """两场交界的转场样片（tools/episode_cut.py gallery）。"""
    from_scene: str
    to_scene: str
    video: str
    entries: list[GalleryEntryQdto] = field(default_factory=list)


@dataclass(frozen=True)
class EpisodeCutsQdto:
    episode_path: str
    scenes: list[SceneCutsQdto] = field(default_factory=list)   # 分镜顺序，每场都列（没剪的列表为空）
    joined: dict[str, list[EpisodeJoinQdto]] = field(default_factory=dict)   # 阶段 → 集级剪辑，新的版本在前
    galleries: dict[str, list[GalleryQdto]] = field(default_factory=dict)   # 阶段 → 转场样片
