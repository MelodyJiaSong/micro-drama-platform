# -*- coding: utf-8 -*-
"""出图引擎分工（2026-10-17 用户定调，ai_video_management follow-up 270 不用即梦、275 改为 ElevenLabs 优先；
文档见 `.agents/skills/ai-videos-pipeline/resources/assets.md`「出图服务」）。出图工具都从这里读引擎顺序，不各写各的。

| 图 | auto 顺序 | 说明 |
|---|---|---|
| 所有图片（人物、换装、道具、物件、装备、背景、plate、变体、镜头图） | ElevenLabs → Codex 内置出图 | ElevenLabs（`gpt-image-2.5-sunburst`，`tools/image_fetch.py`）默认；**额度 / 套餐不够**才换 Codex（`tools/codex_image.py`，ChatGPT 订阅额度） |
| 即梦 | **不出图** | 即梦只用于视频；图片一律不用即梦，也不作失败回退 |

`--engine auto`：ElevenLabs 只在额度 / 套餐不够（`fallback_ok`）时换 Codex；别的失败（审核拦截、参数错、超时）照实报出来，不换家。
**显式 `--engine X` ＝ 只用 X**（X 只能是 codex / elevenlabs），失败就报出来、重跑续。
结果未知的收费请求不重提（各适配器自己保证）；换下一家只在明确失败后。
收费提交前的兜底在 `tools/service_request.py`：即梦的图片操作不论归属一律拒绝（`reject_dreamina_image`）。
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
DREAMINA = "dreamina"   # 只用于视频；出图器拿它比较时一律视为禁用
AUTO = "auto"
CHOICES = (AUTO, CODEX, ELEVENLABS)
AUTO_ORDER = (ELEVENLABS, CODEX)
SCENE_ORDER = AUTO_ORDER
SCENE_MODEL = "gpt-image-2.5-sunburst"  # 2026-10-03 官方文档 / ElevenLabs schema 已核实；后续调用核对最新型号
NO_DREAMINA = "图片禁止 Dreamina（即梦只用于视频，follow-up 270）；使用 ElevenLabs 或 Codex 内置出图"
# ElevenLabs 额度 / 套餐不够的报错（quota_exceeded、402、credits 不足）；只有这类失败才换 Codex（follow-up 275）
NO_QUOTA = re.compile(r"quota|credit|insufficient|payment|\b402\b|套餐不够|额度", re.I)


def scene_choice(override: str = AUTO) -> list[str]:
    """scene/bg（含 plate）的引擎顺序：与所有图片相同，ElevenLabs → Codex。"""
    return order(override)


def is_scene(target: Path | str, prompt: str = "") -> bool:
    """scene/bg 归属（scenes / background 目录或 bg 路由键）；出图器用它分流，不再决定能否用即梦。"""
    path = Path(target)
    first_line = prompt.strip().splitlines()[0] if prompt.strip() else ""
    environment = BACKGROUND_DIR_NAME in path.parts or (SCENES_DIR_NAME in path.parts and "episodes" not in path.parts)
    return bool(environment or re.match(r"^bg\d+(?:-\d+)?(?:_|\b)", path.stem)
                or re.match(r"^bg\d+(?:-\d+)?(?:_|\b)", first_line))


def reject_dreamina_image(target: Path | str | None = None, prompt: str = "") -> None:
    """收费提交前兜底：即梦出图一律拒绝，不看归属。"""
    raise ValueError(NO_DREAMINA)


reject_dreamina_scene = reject_dreamina_image   # 旧名：原先只拒 scene/bg，现在所有图片都拒


def order(override: str = AUTO, *, target: Path | str | None = None, prompt: str = "",
          dreamina_ok: bool = True) -> list[str]:
    """本张图依次尝试的引擎：auto ＝ ElevenLabs → Codex（换家见 `fallback_ok`）；显式点名只用那一家；点名即梦直接报错。
    `target` / `prompt` / `dreamina_ok` 保留给旧调用方，不再影响结果。"""
    if override == DREAMINA:
        raise ValueError(NO_DREAMINA)
    if override not in CHOICES:
        raise ValueError(f"未知引擎 {override}；可选 {', '.join(CHOICES)}")
    return list(AUTO_ORDER) if override == AUTO else [override]


def fallback_ok(engine: str, err: BaseException | str) -> bool:
    """auto 顺序里这一家失败后能不能换下一家：ElevenLabs 只在额度 / 套餐不够时换 Codex（follow-up 275）。"""
    return engine != ELEVENLABS or bool(NO_QUOTA.search(str(err)))
