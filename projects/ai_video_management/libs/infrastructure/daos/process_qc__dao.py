"""流程与自检的读取结果：检查登记、缺陷记录、出片结论、日志健康度。"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class QcCheckDao:
    id: str
    stage: str
    kind: str
    gate: bool
    auto: bool
    level: str                 # 仓库级 / 剧级
    when: str = ""
    desc: str = ""
    how: str = ""
    basis: str = ""
    sources: tuple[str, ...] = ()
    perspective: str = ""        # 由哪个视角审：character / director / audience / fidelity


@dataclass(frozen=True)
class QcDefectDao:
    ts: str
    category: str
    caught_by: str
    artifact: str = ""
    followup: str = ""
    note: str = ""


@dataclass(frozen=True)
class QcRenderDao:
    path: str                  # 出片目录（仓库相对路径）
    artifact: str
    verdicts: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class FollowupHealthDao:
    window_days: int
    followups: int
    logged: int
    duplicates: tuple[int, ...]
    pending: int
    last_number: int
