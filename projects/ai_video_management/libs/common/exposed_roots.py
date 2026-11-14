"""网页可访问的顶层目录：唯一定义，ExposedTree 与 SafeResolver 都从这里读。

`ai_videos/` 是短剧制作产物；`edu_videos/` 是教学视频（follow-up 339，单集预览页审片用）。
"""
from __future__ import annotations

EXPOSED_TOP_LEVEL: frozenset[str] = frozenset({"ai_videos", "edu_videos"})
