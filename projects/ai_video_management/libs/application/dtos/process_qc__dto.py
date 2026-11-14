"""流程与自检的查询结果：仓库级总览与单部剧的明细，两层分开返回、不混。"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ProcessQcRepoQdto:
    stages: list[str]
    checks: list[dict[str, Any]]              # 仓库级检查（对所有剧生效）
    dramas: list[dict[str, Any]]              # 各剧体检汇总


@dataclass(frozen=True)
class ProcessQcDramaQdto:
    drama: str
    spec: str
    enabled: bool                             # 本剧有剧级登记表＝已启用自检闸门
    stages: list[str]
    drama_checks: list[dict[str, Any]]        # 本剧自己的检查
    repo_checks: list[dict[str, Any]]         # 继承自仓库级
    defects: list[dict[str, Any]]
    escapes: list[dict[str, Any]]
    escape_rate: float | None
    renders: list[dict[str, Any]]
    renders_total: int
    followup: dict[str, Any]
