"""人物卡「样片与正片」的读模型（follow-up 286）。视频都是仓库相对路径，经 /api/media 播放。"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ReelClipQdto:
    """一条视频：人物视频，或技能的一条草稿 / 正式条（generation.json 有才带生成信息）。"""
    id: str                           # 生成目录名 `{YYYYMMDD-HHMMSS}_{sid8}`；人物视频为文件名
    video: str
    stage: str                        # turntable / draft / final
    submit_id: str = ""               # 前 8 位
    credits: float | None = None
    generated_at: str = ""            # generation.json 的 downloaded_at，没有就从目录名的时间戳得出
    duration: float | None = None     # generation.json 的 duration_s；没有由播放器读
    resolution: str = ""
    review_status: str = ""


@dataclass(frozen=True)
class SkillReelQdto:
    key: str                          # k651
    title: str                        # 狂战士的怒吼 · Berserker's Call
    path: str
    card: str
    icon: str
    peak: str
    final: ReelClipQdto | None        # 最新的正式条＝当前正片
    finals: list[ReelClipQdto] = field(default_factory=list)
    drafts: list[ReelClipQdto] = field(default_factory=list)   # 新的在前


@dataclass(frozen=True)
class ReelCutQdto:
    """一版剪辑拼接成片（人物目录 demo/ 或集级 edit/{draft,final}/cut_v{N}.json）。"""
    version: int
    stage: str
    episode: str                      # 集目录名；人物目录 demo/ 的为 demo
    path: str
    video: str
    duration: float | None
    note: str = ""
    status: str = ""
    phase: str = ""
    error: str = ""
    own: bool = False                 # 在人物目录 demo/ 下（follow-up 288），排在各集剪辑前


@dataclass(frozen=True)
class CharacterReelQdto:
    name: str
    path: str
    turntable: ReelClipQdto | None
    skills: list[SkillReelQdto] = field(default_factory=list)          # 按技能键（Q W E R）
    cuts: dict[str, list[ReelCutQdto]] = field(default_factory=dict)   # draft / final → 按版本号
    watch: list[str] = field(default_factory=list)                     # 这些目录变了就重取
