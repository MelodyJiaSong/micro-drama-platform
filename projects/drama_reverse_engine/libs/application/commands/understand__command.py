from __future__ import annotations

from dataclasses import asdict

from libs.application.dtos.understand__dto import UnderstandResultCdto
from libs.common.vocab import LOW_CONFIDENCE_FLOOR
from libs.infrastructure.clients.composer__client import LlmComposer
from libs.infrastructure.clients.ffmpeg__client import FfmpegClient
from libs.infrastructure.clients.understanding__client import VideoUnderstanding
from libs.infrastructure.errors.understanding__error import UnderstandingBackendUnavailableError
from libs.infrastructure.readers.artifact__reader import ArtifactReader
from libs.infrastructure.writers.artifact__writer import ArtifactWriter


class UnderstandCommand:
    """FR-4: episode pass + per-shot clip pass; also closes two loops deferred here —
    speaker attribution (FR-2.4, via the episode pass) and 锁定描述符 authoring
    (FR-3.3: cards leave the assets stage with empty descriptors; this stage authors
    and persists them so compose can enforce byte-identical pasting)."""

    def __init__(
        self, ffmpeg: FfmpegClient, vlm: VideoUnderstanding, composer: LlmComposer,
        reader: ArtifactReader, writer: ArtifactWriter,
        low_confidence_floor: float = LOW_CONFIDENCE_FLOOR,
    ) -> None:
        self._ffmpeg = ffmpeg
        self._vlm = vlm
        self._composer = composer
        self._reader = reader
        self._writer = writer
        self._floor = low_confidence_floor

    def run(self, drama_id: str, episode_rel_dir: str, force: bool = False) -> UnderstandResultCdto:
        out_rel = f"{episode_rel_dir}/understanding.json"
        if self._reader.exists(out_rel) and not force:
            data = self._reader.read_json(out_rel)
            return UnderstandResultCdto(
                episode_rel_dir=episode_rel_dir, shot_count=len(data["shots"]),
                low_confidence_count=len(data["review_queue"]),
                speaker_low_confidence_count=data["speaker_low_confidence_count"], skipped=True,
            )
        if not self._vlm.available:
            raise UnderstandingBackendUnavailableError("cannot reverse-engineer without a VLM backend")

        shots = self._reader.read_json(f"{episode_rel_dir}/shots.json")
        dialogue = self._reader.read_json(f"{episode_rel_dir}/dialogue_raw.json")
        library = self._reader.read_json(f"{drama_id}/characters/library.json")
        source_abs = self._writer.resolve(f"{episode_rel_dir}/source.mp4")

        episode = self._vlm.episode_pass(source_abs, dialogue["lines"])
        descriptors = self._reconcile_characters(
            drama_id, library, list(episode.character_continuity), episode.character_continuity
        )

        assignments = {a.line_index: a for a in episode.speaker_assignments}
        final_lines = []
        speaker_low = 0
        for idx, line in enumerate(dialogue["lines"]):
            assign = assignments.get(idx)
            speaker = assign.speaker if assign else "未归属"
            confidence = assign.confidence if assign else 0.0
            dtype = assign.dialogue_type if assign else "对白"
            if confidence < self._floor:
                speaker_low += 1
            final_lines.append({**line, "speaker": speaker, "dialogue_type": dtype,
                                "attribution": "episode_pass", "speaker_confidence": confidence})
        self._writer.write_json(f"{episode_rel_dir}/dialogue.json", {
            "lines": final_lines, "speaker_low_confidence_count": speaker_low,
        })

        analyses = []
        review_queue = []
        shot_names: set[str] = set()
        prev_summary = "（本集第一镜，无上文）"
        self._writer.ensure_dir(f"{episode_rel_dir}/clips")
        for shot in shots:
            clip_rel = f"{episode_rel_dir}/clips/shot{shot['index']:02d}.mp4"
            self._ffmpeg.cut_clip(source_abs, shot["start_s"], shot["end_s"], self._writer.resolve(clip_rel))
            analysis = self._vlm.shot_pass(self._writer.resolve(clip_rel), prev_summary, descriptors, shot["index"])
            analyses.append(asdict(analysis))
            shot_names.update(analysis.characters)
            for field_name, conf in analysis.confidences.items():
                if conf < self._floor:
                    review_queue.append({"shot_index": shot["index"], "field": field_name, "confidence": conf})
            prev_summary = f"上一镜：{analysis.action}；人物：{'、'.join(analysis.characters)}"
        self._reconcile_characters(drama_id, library, sorted(shot_names), episode.character_continuity)

        self._writer.write_json(out_rel, {
            "narrative": episode.narrative, "beats": list(episode.beats),
            "emotion_curve": episode.emotion_curve,
            "character_continuity": episode.character_continuity,
            "shots": analyses, "review_queue": review_queue,
            "speaker_low_confidence_count": speaker_low,
        })
        return UnderstandResultCdto(
            episode_rel_dir=episode_rel_dir, shot_count=len(analyses),
            low_confidence_count=len(review_queue), speaker_low_confidence_count=speaker_low,
        )

    def _reconcile_characters(
        self, drama_id: str, library: dict, names: list[str], continuity: dict[str, str]
    ) -> dict[str, str]:
        """FR-3.3 closure: every VLM-named character must leave this stage with a library
        card + locked descriptor. Face-cluster cards get empty descriptors authored;
        names the face backend never saw (Null default install) get a vlm_discovered
        card created here — otherwise compose dead-ends on DescriptorDriftError."""
        changed = False
        known = {c["name"] for c in library["characters"]}
        for name in names:
            if name and name not in known:
                library["characters"].append({
                    "character_id": f"vlm{len(library['characters']) + 1:02d}",
                    "name": name, "descriptor": "", "centroid": [], "refs": [],
                    "face_count": 0, "origin": "vlm_discovered",
                })
                known.add(name)
                changed = True
        for card in library["characters"]:
            if card["descriptor"].strip() or not self._composer.available:
                continue
            notes = continuity.get(card["name"], "") or f"参考帧×{len(card['refs'])}，出现 {card['face_count']} 次"
            card["descriptor"] = self._composer.author_descriptor(card["name"], notes)
            changed = True
        if changed:
            self._writer.write_json(f"{drama_id}/characters/library.json", library)
        return {c["name"]: c["descriptor"] for c in library["characters"]}
