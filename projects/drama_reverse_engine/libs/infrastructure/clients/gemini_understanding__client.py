from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any

import httpx

from libs.common.vocab import CAMERA_ANGLES, CAMERA_MOVES, SHOT_SIZES
from libs.infrastructure.daos.shotanalysis__dao import (
    EpisodeUnderstandingDao,
    ShotAnalysisDao,
    SpeakerAssignmentDao,
)

_BASE = "https://generativelanguage.googleapis.com"
_MODEL = "gemini-2.5-pro"


def snap_to_vocab(value: str, vocab: tuple[str, ...], default: str) -> str:
    return value if value in vocab else default


def _character_name(entry: Any) -> str:
    # models sometimes return character OBJECTS ({"name": ..., "desc": ...}) despite
    # the string-array contract; the descriptor pipeline keys on bare names
    if isinstance(entry, dict):
        return str(entry.get("name") or entry.get("角色") or "").strip()
    return str(entry).strip()


def parse_episode_json(data: dict[str, Any]) -> EpisodeUnderstandingDao:
    return EpisodeUnderstandingDao(
        narrative=str(data.get("narrative", "")),
        beats=tuple(str(b) for b in data.get("beats", [])),
        emotion_curve=str(data.get("emotion_curve", "")),
        character_continuity={str(k): str(v) for k, v in data.get("character_continuity", {}).items()},
        speaker_assignments=tuple(
            SpeakerAssignmentDao(
                line_index=int(a["line_index"]), speaker=str(a.get("speaker", "未归属")),
                dialogue_type=str(a.get("dialogue_type", "对白")),
                confidence=float(a.get("confidence", 0.0)),
            )
            for a in data.get("speaker_assignments", [])
        ),
    )


def parse_shot_json(data: dict[str, Any], shot_index: int) -> ShotAnalysisDao:
    return ShotAnalysisDao(
        index=shot_index,
        shot_size=snap_to_vocab(str(data.get("shot_size", "")), SHOT_SIZES, "中景"),
        camera_angle=snap_to_vocab(str(data.get("camera_angle", "")), CAMERA_ANGLES, "平视"),
        camera_move=snap_to_vocab(str(data.get("camera_move", "")), CAMERA_MOVES, "固定"),
        blocking=str(data.get("blocking", "")),
        action=str(data.get("action", "")),
        performance=str(data.get("performance", "")),
        scene_desc=str(data.get("scene_desc", "")),
        lighting=str(data.get("lighting", "")),
        mood=str(data.get("mood", "")),
        continuous_with_prev=bool(data.get("continuous_with_prev", False)),
        characters=tuple(n for n in (_character_name(c) for c in data.get("characters", [])) if n),
        confidences={str(k): float(v) for k, v in data.get("confidences", {}).items()},
    )


class GeminiVideoUnderstanding:
    """FR-4 primary backend. API shape is best-effort against 2026-07 docs and MUST be
    live-verified via the FR-13.3 probe before production; parsing is unit-tested
    against recorded-shape fixtures."""

    def __init__(self, api_key: str, timeout_s: float = 300.0) -> None:
        self._api_key = api_key
        self._timeout_s = timeout_s

    @property
    def available(self) -> bool:
        return bool(self._api_key)

    def episode_pass(self, video_abs_path: str, dialogue_lines: list[dict]) -> EpisodeUnderstandingDao:
        prompt = (
            "你是短剧逆向工程分析师。通读整集视频与台词列表，输出 JSON："
            '{"narrative": 叙事梗概, "beats": [beat...], "emotion_curve": 情绪曲线, '
            '"character_continuity": {角色: 服装外观连续性}, '
            '"speaker_assignments": [{"line_index": 台词行号, "speaker": 说话人, '
            '"dialogue_type": "对白|内心独白|旁白", "confidence": 0-1}]}\n台词列表(带行号): '
            + json.dumps(list(enumerate(l["text"] for l in dialogue_lines)), ensure_ascii=False)
        )
        return parse_episode_json(self._generate(video_abs_path, prompt))

    def shot_pass(self, clip_abs_path: str, prev_shot_summary: str,
                  character_descriptors: dict[str, str], shot_index: int) -> ShotAnalysisDao:
        prompt = (
            f"分析这个单镜片段（差分上下文：{prev_shot_summary}）。画面叠加文字层（台标/水印/角色名牌/字幕）"
            "是后期贴的，任何字段不要提及。已知角色："
            + json.dumps(character_descriptors, ensure_ascii=False)
            + "。输出 JSON（闭集词表：shot_size∈" + "/".join(SHOT_SIZES)
            + "，camera_angle∈" + "/".join(CAMERA_ANGLES) + "，camera_move∈" + "/".join(CAMERA_MOVES)
            + '）：{"shot_size","camera_angle","camera_move","blocking","action","performance",'
            '"scene_desc","lighting","mood","continuous_with_prev":bool,"characters":[...],'
            '"confidences":{字段:0-1}}'
        )
        return parse_shot_json(self._generate(clip_abs_path, prompt), shot_index)

    def _generate(self, video_abs_path: str, prompt: str) -> dict[str, Any]:
        video_b64 = base64.b64encode(Path(video_abs_path).read_bytes()).decode()
        body = {
            "contents": [{"parts": [
                {"inline_data": {"mime_type": "video/mp4", "data": video_b64}},
                {"text": prompt},
            ]}],
            "generationConfig": {"response_mime_type": "application/json"},
        }
        resp = httpx.post(
            f"{_BASE}/v1beta/models/{_MODEL}:generateContent",
            json=body, headers={"x-goog-api-key": self._api_key}, timeout=self._timeout_s,
        )
        resp.raise_for_status()
        text = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(text)


class QwenVideoUnderstanding:
    """FR-4.4 fallback backend on DashScope (Qwen3-VL). Reuses the same闭集-vocab JSON
    parsers as Gemini. API shape is best-effort pending the FR-13.3 probe."""

    def __init__(self, api_key: str, timeout_s: float = 300.0) -> None:
        self._api_key = api_key
        self._timeout_s = timeout_s

    @property
    def available(self) -> bool:
        return bool(self._api_key)

    def episode_pass(self, video_abs_path: str, dialogue_lines: list[dict]) -> EpisodeUnderstandingDao:
        prompt = (
            "通读整集视频与台词，输出严格 JSON：narrative, beats[], emotion_curve, "
            "character_continuity{}, speaker_assignments[{line_index,speaker,dialogue_type,confidence}]。台词: "
            + json.dumps(list(enumerate(l["text"] for l in dialogue_lines)), ensure_ascii=False)
        )
        return parse_episode_json(self._generate(video_abs_path, prompt))

    def shot_pass(self, clip_abs_path: str, prev_shot_summary: str,
                  character_descriptors: dict[str, str], shot_index: int) -> ShotAnalysisDao:
        prompt = (
            f"分析单镜（上下文：{prev_shot_summary}）。画面叠加文字层（台标/水印/角色名牌/字幕）后期贴的，"
            "任何字段不要提及。角色："
            + json.dumps(character_descriptors, ensure_ascii=False)
            + "。输出闭集 JSON：shot_size∈" + "/".join(SHOT_SIZES) + "，camera_move∈" + "/".join(CAMERA_MOVES)
            + "，含 blocking/action/performance/scene_desc/lighting/mood/continuous_with_prev/characters/confidences。"
        )
        return parse_shot_json(self._generate(clip_abs_path, prompt), shot_index)

    def _generate(self, video_abs_path: str, prompt: str) -> dict[str, Any]:
        video_b64 = base64.b64encode(Path(video_abs_path).read_bytes()).decode()
        body = {
            "model": "qwen3-vl-plus",
            "messages": [{"role": "user", "content": [
                {"type": "video_url", "video_url": {"url": f"data:video/mp4;base64,{video_b64}"}},
                {"type": "text", "text": prompt},
            ]}],
            "response_format": {"type": "json_object"},
        }
        resp = httpx.post(
            "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
            json=body, headers={"Authorization": f"Bearer {self._api_key}"}, timeout=self._timeout_s,
        )
        resp.raise_for_status()
        return json.loads(resp.json()["choices"][0]["message"]["content"])
