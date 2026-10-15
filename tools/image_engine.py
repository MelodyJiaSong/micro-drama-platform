# -*- coding: utf-8 -*-
"""出图引擎分工（2026-10-11 用户定调，follow-up 238；文档见 `.agents/skills/ai-videos-pipeline/resources/assets.md`「出图服务」）。
出图工具都从这里读引擎顺序，不各写各的。

| 图 | auto 顺序 | 说明 |
|---|---|---|
| 所有图片（人物、换装、道具、装备、背景） | Codex 内置出图 → ElevenLabs → 即梦 | Codex 画质最高（`tools/codex_image.py`，ChatGPT 订阅额度）；即梦是最低选项，前面都不行才用 |
| scene/bg：世界锚点、场景锚点、plate、变体、shot 背景 | Codex → ElevenLabs，**不用即梦** | 2026-10-03 用户要求，禁止即梦及失败回退到即梦 |

`--engine auto`：按顺序一家失败（审核拦截、超时、未登录、额度不足）再换下一家；即梦 1600 字硬限超了就跳过即梦。
**显式 `--engine X` ＝ 只用 X**，失败就报出来、重跑续（用户点名「用即梦出」时不许悄悄换别家）。
结果未知的收费请求不重提（各适配器自己保证）；换下一家只在明确失败后。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from projects.ai_video_management.libs.common.production_key import BACKGROUND_DIR_NAME, SCENES_DIR_NAME

CODEX = "codex"
ELEVENLABS = "elevenlabs"
DREAMINA = "dreamina"
AUTO = "auto"
CHOICES = (AUTO, CODEX, ELEVENLABS, DREAMINA)
AUTO_ORDER = (CODEX, ELEVENLABS, DREAMINA)   # 即梦永远最后
SCENE_ORDER = (CODEX, ELEVENLABS)
SCENE_MODEL = "gpt-image-2.5-sunburst"  # 2026-10-03 官方文档 / ElevenLabs schema 已核实；后续调用核对最新型号


def scene_choice(override: str = AUTO) -> list[str]:
    """scene/bg（含 plate）的引擎顺序：Codex → ElevenLabs，禁止即梦及失败回退。"""
    if override == DREAMINA or override not in CHOICES:
        raise ValueError("scene/bg 图片禁止 Dreamina；使用 Codex 内置出图（最新 GPT 图像）或 ElevenLabs")
    return list(SCENE_ORDER) if override == AUTO else [override]


def is_scene(target: Path | str, prompt: str = "") -> bool:
    try:
        reject_dreamina_scene(target, prompt)
    except ValueError:
        return True
    return False


def reject_dreamina_scene(target: Path | str, prompt: str = "") -> None:
    """收费提交前兜底，既识别 scenes 归属，也识别独立 bg 路由键；不影响 bgm / 人物 / 道具。"""
    path = Path(target)
    first_line = prompt.strip().splitlines()[0] if prompt.strip() else ""
    environment = BACKGROUND_DIR_NAME in path.parts or (SCENES_DIR_NAME in path.parts and "episodes" not in path.parts)
    if environment or re.match(r"^bg\d+(?:-\d+)?(?:_|\b)", path.stem) or re.match(r"^bg\d+(?:-\d+)?(?:_|\b)", first_line):
        raise ValueError("scene/bg 图片禁止 Dreamina；使用最新 GPT 图像模型或 ElevenLabs")


def order(override: str = AUTO, *, target: Path | str | None = None, prompt: str = "",
          dreamina_ok: bool = True) -> list[str]:
    """本张图依次尝试的引擎。`target` 是 scene/bg 时去掉即梦（显式点名即梦直接报错）；
    `dreamina_ok=False`（如超即梦字数硬限）时 auto 里去掉即梦。"""
    if override not in CHOICES:
        raise ValueError(f"未知引擎 {override}；可选 {', '.join(CHOICES)}")
    if target is not None and is_scene(target, prompt):
        return scene_choice(override)
    if override != AUTO:
        return [override]
    return [e for e in AUTO_ORDER if dreamina_ok or e != DREAMINA]
