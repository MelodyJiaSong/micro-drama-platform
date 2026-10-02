# -*- coding: utf-8 -*-
"""出图引擎分工（`ai_video.md` rule 4l，2026-09-25 用户定调）。出图工具都从这里读首选引擎，不各写各的。

| 图 | 首选 | 理由 |
|---|---|---|
| 第一张锚点：世界锚点、bg 锚点、角色立绘（从文字长出一个完整主体） | ElevenLabs | 贵，但复杂图出得好 |
| 挂了锚点的派生图：plate、角色 / 物件的侧背视图与状态变体；简单单物件 | 即梦 | 便宜，有参考图或主体简单时够用 |
| props 与装备（equipment）的正 / 侧 / 背三视图 | **只用即梦** | 用户点名（follow-up 017 / 022）；显式 dreamina，失败不退 |
| 装备里蓝档及以上的武器 | **只用 ElevenLabs** | 用户点名（follow-up 027 定、029 收紧到蓝档）；逐件判定在 `equipment_lib.Config.engine_for` |

`--engine auto`：首选失败（审核拦截、超时、即梦 1600 字硬限）再退另一家；**显式 `--engine X` ＝ 只用 X**，
失败就报出来、重跑续（用户点名「用即梦出」时不许悄悄花 ElevenLabs）。复杂物件的第一张图用 `--engine elevenlabs`。
"""
from __future__ import annotations

ELEVENLABS = "elevenlabs"
DREAMINA = "dreamina"
AUTO = "auto"
CHOICES = (AUTO, DREAMINA, ELEVENLABS)


def first_choice(anchor: bool, override: str = AUTO) -> str:
    """`anchor`：这张图是不是该主体的第一张锚点。`override` 是命令行 `--engine`，非 auto 时照它。"""
    if override != AUTO:
        return override
    return ELEVENLABS if anchor else DREAMINA


def other(engine: str) -> str:
    return DREAMINA if engine == ELEVENLABS else ELEVENLABS
