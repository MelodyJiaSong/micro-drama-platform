# -*- coding: utf-8 -*-
"""出图引擎分工（`ai_video.md` rule 4l，2026-09-25 用户定调）。出图工具都从这里读首选引擎，不各写各的。

| 图 | 首选 | 理由 |
|---|---|---|
| 所有 scene/bg：世界锚点、场景锚点、plate、变体、shot 背景 | 最新 GPT 图像模型或 ElevenLabs | 2026-10-03 用户要求；禁止 Dreamina 及失败回退 |
| 非场景第一张锚点：角色立绘（从文字长出一个完整主体） | ElevenLabs | 贵，但复杂图出得好 |
| 挂了锚点的非场景派生图：角色 / 物件的侧背视图与状态变体；简单单物件 | 即梦 | 便宜，有参考图或主体简单时够用 |
| props 与装备（equipment）的正 / 侧 / 背三视图 | **只用即梦** | 用户点名（follow-up 017 / 022）；显式 dreamina，失败不退 |
| 装备里蓝档及以上的武器 | **只用 ElevenLabs** | 用户点名（follow-up 027 定、029 收紧到蓝档）；逐件判定在 `equipment_lib.Config.engine_for` |

非场景 `--engine auto`：首选失败（审核拦截、超时、即梦 1600 字硬限）再退另一家；**显式 `--engine X` ＝ 只用 X**，
失败就报出来、重跑续（用户点名「用即梦出」时不许悄悄花 ElevenLabs）。复杂物件的第一张图用 `--engine elevenlabs`。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from projects.ai_video_management.libs.common.production_key import BACKGROUND_DIR_NAME, SCENES_DIR_NAME

ELEVENLABS = "elevenlabs"
DREAMINA = "dreamina"
AUTO = "auto"
CHOICES = (AUTO, DREAMINA, ELEVENLABS)
SCENE_MODEL = "gpt-image-2.5-sunburst"  # 2026-10-03 官方文档 / ElevenLabs schema 已核实；后续调用核对最新型号


def scene_choice(override: str = AUTO) -> str:
    """scene/bg（含 plate）只用最新 GPT 图像模型或 ElevenLabs，禁止即梦及失败回退。"""
    if override not in (AUTO, ELEVENLABS):
        raise ValueError("scene/bg 图片禁止 Dreamina；使用最新 GPT 图像模型或 ElevenLabs")
    return ELEVENLABS


def reject_dreamina_scene(target: Path | str, prompt: str = "") -> None:
    """收费提交前兜底，既识别 scenes 归属，也识别独立 bg 路由键；不影响 bgm / 人物 / 道具。"""
    path = Path(target)
    first_line = prompt.strip().splitlines()[0] if prompt.strip() else ""
    environment = BACKGROUND_DIR_NAME in path.parts or (SCENES_DIR_NAME in path.parts and "episodes" not in path.parts)
    if environment or re.match(r"^bg\d+(?:-\d+)?(?:_|\b)", path.stem) or re.match(r"^bg\d+(?:-\d+)?(?:_|\b)", first_line):
        raise ValueError("scene/bg 图片禁止 Dreamina；使用最新 GPT 图像模型或 ElevenLabs")


def first_choice(anchor: bool, override: str = AUTO) -> str:
    """`anchor`：这张图是不是该主体的第一张锚点。`override` 是命令行 `--engine`，非 auto 时照它。"""
    if override != AUTO:
        return override
    return ELEVENLABS if anchor else DREAMINA


def other(engine: str) -> str:
    return DREAMINA if engine == ELEVENLABS else ELEVENLABS
