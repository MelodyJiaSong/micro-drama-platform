"""排行榜预览的读模型（follow-up 320）。路径都是仓库相对路径，经 /api/media 播放；文件不在为空串 / None。"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class RankVideoQdto:
    name: str
    path: str
    label: str
    risk: bool                        # `_with-risk-images` 版
    music: bool | None                # manifest 或文件名判断；无 manifest 又看不出为 None
    duration_s: float | None
    complete: bool = True             # 有 moov 才能播；渲染中的文件为 False
    recommended: bool = False


@dataclass(frozen=True)
class RankImageStatsQdto:
    items: int = 0
    with_image: int = 0               # 主图文件在盘上
    missing: int = 0                  # 写了主图但文件不在，或没写主图
    risk: int = 0                     # 有 image_risk
    alt: int = 0                      # 有 image_alt
    ai: int = 0                       # 主图或替代图许可为 AI-generated


@dataclass(frozen=True)
class RankImageQdto:
    path: str                         # 仓库相对；文件不在为空串
    declared: str                     # data.json 里写的相对路径
    licence: str = ""
    author: str = ""
    source: str = ""                  # 来源页 URL
    ai: bool = False


@dataclass(frozen=True)
class RankPersonQdto:
    """公司卡的创始人（契约 v1.3 `person`，follow-up 321）。"""
    name: str
    role: str = ""
    image: RankImageQdto | None = None
    image_risk: str = ""
    credit: str = ""


@dataclass(frozen=True)
class RankItemQdto:
    rank: int                         # 列表期（mode=list）为出场序号，不是名次
    name: str
    subtitle: str
    country_iso2: str
    country_name: str
    flag: str                         # `_assets/flags/<iso2>.png`；不在为空串
    value_display: str
    badge: str
    image: RankImageQdto | None
    image_alt: RankImageQdto | None
    image_risk: str
    # 以下为契约 v1.3/v1.4 的可选字段（follow-up 321）；没写为空串 / None
    corner: str = ""                  # 卡片右上角标签，如 EST. 2015
    logo: RankImageQdto | None = None
    logo_bg: str = ""                 # 只收 #rgb / #rrggbb(aa)
    person: RankPersonQdto | None = None
    image_alt_credit: str = ""
    secondary_display: str = ""
    notes: str = ""


@dataclass(frozen=True)
class RankInsightQdto:
    after_rank: int | None
    text: str


@dataclass(frozen=True)
class RankDocQdto:
    path: str                         # 文件不在为空串
    text: str = ""


@dataclass(frozen=True)
class RankEpisodeCardQdto:
    key: str                          # ep02_highest_peak_by_country
    number: int | None
    path: str
    title: str
    n: int
    champion: str
    duration_s: float | None
    thumbnail: str
    verdict: str                      # qc.md 最新结论一行；没有为空串
    music: bool | None                # 任一成片有配乐为 True
    videos: int
    stats: RankImageStatsQdto
    error: str = ""
    # follow-up 321：列表期不排名，champion 置空，改给首个 / 末个与排列依据
    mode: str = "rank"                # rank / list
    first: str = ""
    last: str = ""
    list_order: str = ""              # 列表期的排列依据，如「成立年份」；看不出为空串


@dataclass(frozen=True)
class RankEpisodeQdto:
    card: RankEpisodeCardQdto
    kicker: str
    theme: str
    metric_label: str
    period_label: str
    source_line: str
    scope_note: str
    videos: list[RankVideoQdto] = field(default_factory=list)
    verdict_excerpt: str = ""         # qc.md 最新结论起约 30 行
    qc: RankDocQdto = field(default_factory=lambda: RankDocQdto(""))
    publish: RankDocQdto = field(default_factory=lambda: RankDocQdto(""))
    handoff: RankDocQdto = field(default_factory=lambda: RankDocQdto(""))
    items: list[RankItemQdto] = field(default_factory=list)
    insights: list[RankInsightQdto] = field(default_factory=list)


@dataclass(frozen=True)
class RankSeriesQdto:
    path: str
    focus: list[int] = field(default_factory=list)     # 重点展示的期号
    episodes: list[RankEpisodeCardQdto] = field(default_factory=list)


@dataclass(frozen=True)
class RankPreviewQdto:
    kind: str                         # series / episode
    series: RankSeriesQdto | None = None
    episode: RankEpisodeQdto | None = None
