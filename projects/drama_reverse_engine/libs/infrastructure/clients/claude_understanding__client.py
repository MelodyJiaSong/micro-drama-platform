from __future__ import annotations

import json
import shutil
from pathlib import Path

from libs.common.vocab import CAMERA_ANGLES, CAMERA_MOVES, SHOT_SIZES
from libs.infrastructure.clients.claudecli__client import ClaudeCliClient, extract_json_object
from libs.infrastructure.clients.ffmpeg__client import FfmpegClient
from libs.infrastructure.clients.gemini_understanding__client import parse_episode_json, parse_shot_json
from libs.infrastructure.daos.shotanalysis__dao import EpisodeUnderstandingDao, ShotAnalysisDao
from libs.infrastructure.errors.claudecli__error import ClaudeCliError

_SHOT_FRAME_POSITIONS = (0.15, 0.5, 0.85)
_RETRY_SUFFIX = "\n（上次输出不是合法 JSON，这次务必只输出一个合法的 JSON 对象。）"


class ClaudeVideoUnderstanding:
    """VideoUnderstanding backend on the local Claude Code CLI (zero API key,
    follow-up 002). The CLI cannot ingest mp4, so keyframes are sampled with ffmpeg
    and the session Reads them; the JSON output contract (and闭集 vocab snapping)
    is identical to the Gemini/Qwen backends."""

    def __init__(self, cli: ClaudeCliClient, ffmpeg: FfmpegClient,
                 episode_max_frames: int = 24, max_turns: int = 40) -> None:
        self._cli = cli
        self._ffmpeg = ffmpeg
        self._episode_max_frames = episode_max_frames
        self._max_turns = max_turns

    @property
    def available(self) -> bool:
        return self._cli.available

    def episode_pass(self, video_abs_path: str, dialogue_lines: list[dict]) -> EpisodeUnderstandingDao:
        duration = self._ffmpeg.probe(video_abs_path).duration_s
        count = min(self._episode_max_frames, max(6, int(duration // 5) + 1)) if duration > 0 else 1
        times = [(i + 0.5) * duration / count for i in range(count)] if duration > 0 else [0.0]
        frames_dir, listing = self._sample(video_abs_path, times, "episode")
        lines = [{"line_index": i, "text": l["text"], "start_s": l.get("start_s"), "end_s": l.get("end_s")}
                 for i, l in enumerate(dialogue_lines)]
        prompt = (
            "你是短剧逆向工程分析师。下面是从整集视频按时间顺序抽出的关键帧，先用 Read 工具逐张查看：\n"
            + listing
            + "\n注意：画面上的叠加文字层（台标/水印/角色名牌/字幕浮层）是后期贴的，不属于场景内容，不要写进任何描述。"
            "\n结合台词列表（带行号与秒数区间），推断整集叙事并归属每行说话人。只输出一个 JSON 对象，不要输出其他文字："
            '{"narrative": 叙事梗概, "beats": [beat...], "emotion_curve": 情绪曲线, '
            '"character_continuity": {角色名字符串: 服装外观连续性描述}, '
            '"speaker_assignments": [{"line_index": 台词行号, "speaker": 说话人, '
            '"dialogue_type": "对白|内心独白|旁白", "confidence": 0-1}]}\n'
            "无论帧内容是什么（哪怕是测试图/纯色/无人物），都必须只输出上述契约的 JSON——"
            '没有叙事就在 narrative 里如实写「无叙事内容：<所见>」并给空数组/空对象，'
            "绝不输出 JSON 以外的解释、追问或拒绝。\n台词列表: "
            + json.dumps(lines, ensure_ascii=False)
        )
        try:
            data = self._ask_json(prompt, frames_dir)
        finally:
            shutil.rmtree(frames_dir, ignore_errors=True)
        return parse_episode_json(data)

    def shot_pass(self, clip_abs_path: str, prev_shot_summary: str,
                  character_descriptors: dict[str, str], shot_index: int) -> ShotAnalysisDao:
        duration = self._ffmpeg.probe(clip_abs_path).duration_s
        times = [duration * p for p in _SHOT_FRAME_POSITIONS] if duration > 0 else [0.0]
        frames_dir, listing = self._sample(clip_abs_path, times, f"shot{shot_index:02d}")
        prompt = (
            "下面是同一个单镜片段的起/中/末关键帧，先用 Read 工具逐张查看：\n" + listing
            + "\n注意：画面上的叠加文字层（台标/水印/角色名牌/字幕浮层）是后期贴的，不属于场景内容，"
            "任何字段都不要提及它们。"
            + f"\n分析这个单镜（差分上下文：{prev_shot_summary}）。已知角色："
            + json.dumps(character_descriptors, ensure_ascii=False)
            + "。只输出一个 JSON 对象，不要输出其他文字（闭集词表：shot_size∈" + "/".join(SHOT_SIZES)
            + "，camera_angle∈" + "/".join(CAMERA_ANGLES) + "，camera_move∈" + "/".join(CAMERA_MOVES)
            + '）：{"shot_size","camera_angle","camera_move","blocking","action","performance",'
            '"scene_desc","lighting","mood","continuous_with_prev":bool,'
            '"characters":[出现的角色名字符串,...],"confidences":{字段:0-1}}。'
            "scene_desc 以「地点短名，细节描述」开头（全角逗号分隔）；同一地点在不同镜中必须复用"
            "完全相同的地点短名（供剧本按场分组）。"
            "无论画面是什么（哪怕无人物/纯图形）都只输出该 JSON——字段如实描述、"
            "characters 可为空数组，绝不输出 JSON 以外的解释或拒绝。"
        )
        try:
            data = self._ask_json(prompt, frames_dir)
        finally:
            shutil.rmtree(frames_dir, ignore_errors=True)
        return parse_shot_json(data, shot_index)

    def _ask_json(self, prompt: str, frames_dir: Path) -> dict:
        reply = self._cli.run_text(prompt, read_dirs=(str(frames_dir),), max_turns=self._max_turns)
        try:
            return extract_json_object(reply)
        except ClaudeCliError:
            reply = self._cli.run_text(prompt + _RETRY_SUFFIX, read_dirs=(str(frames_dir),),
                                       max_turns=self._max_turns)
            return extract_json_object(reply)

    def _sample(self, video_abs_path: str, times: list[float], tag: str) -> tuple[Path, str]:
        source = Path(video_abs_path)
        frames_dir = source.parent / f".claude_frames_{tag}_{source.stem}"
        shutil.rmtree(frames_dir, ignore_errors=True)
        frames_dir.mkdir(parents=True, exist_ok=True)
        rows = []
        for i, at_s in enumerate(times):
            out = frames_dir / f"f{i:02d}.jpg"
            self._ffmpeg.extract_frame(str(source), at_s, str(out))
            rows.append(f"- 帧{i:02d} @ {at_s:.1f}s: {out}")
        return frames_dir, "\n".join(rows)
