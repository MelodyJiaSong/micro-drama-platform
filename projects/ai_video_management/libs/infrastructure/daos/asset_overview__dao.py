"""资产总览的原始读数（follow-up 293）：路径都是仓库相对路径。"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AssetFolderDao:
    kind: str                         # characters / background / props
    folder: str                       # c24_Anti_Mage
    path: str                         # 资产目录
    group: str                        # 分组目录（`近卫_sentinel`、`大陆/区`），没有分组为空串；系列共享的前缀 `_series`
    card: str                         # `{目录}.md`，不在为空串
    title: str                        # 卡首个 `# ` 行
    meta: list[str]                   # 标题前的 `> ` 引用行（键、状态）
    images: list[str]                 # 目录顶层的图片
    videos: list[tuple[str, float]]   # 目录顶层的视频与 mtime
