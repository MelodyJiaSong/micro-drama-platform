from __future__ import annotations

from libs.application.dtos.extract__dto import ExtractResultCdto
from libs.domain.value_objects.dialogueline__valueobject import RawLine, reconcile_lines
from libs.infrastructure.clients.asr__client import AsrTranscriber
from libs.infrastructure.clients.ffmpeg__client import FfmpegClient
from libs.infrastructure.clients.shotdetect__client import ShotDetector
from libs.infrastructure.clients.subtitle__client import SubtitleExtractor
from libs.infrastructure.readers.artifact__reader import ArtifactReader
from libs.infrastructure.writers.artifact__writer import ArtifactWriter


class ExtractCommand:
    """FR-2: shot detection + dialogue extraction (OCR master / ASR check) per episode.

    Speaker attribution is completed at the understand stage (FR-2.4) — extract
    emits lines with speaker=null, attribution="pending"."""

    def __init__(
        self,
        ffmpeg: FfmpegClient,
        detector: ShotDetector,
        subtitles: SubtitleExtractor,
        asr: AsrTranscriber,
        reader: ArtifactReader,
        writer: ArtifactWriter,
    ) -> None:
        self._ffmpeg = ffmpeg
        self._detector = detector
        self._subtitles = subtitles
        self._asr = asr
        self._reader = reader
        self._writer = writer

    def run(self, episode_rel_dir: str, force: bool = False) -> ExtractResultCdto:
        shots_rel = f"{episode_rel_dir}/shots.json"
        dialogue_rel = f"{episode_rel_dir}/dialogue_raw.json"
        if self._reader.exists(shots_rel) and self._reader.exists(dialogue_rel) and not force:
            shots = self._reader.read_json(shots_rel)
            lines = self._reader.read_json(dialogue_rel)
            return ExtractResultCdto(
                episode_rel_dir=episode_rel_dir, shot_count=len(shots),
                dialogue_line_count=len(lines["lines"]), flagged_line_count=lines["flagged_count"],
                degradations=lines["degradations"], skipped=True,
            )

        source_abs = self._writer.resolve(f"{episode_rel_dir}/source.mp4")
        info = self._ffmpeg.probe(source_abs)
        spans = self._detector.detect(source_abs, info.duration_s)
        self._writer.write_json(shots_rel, [
            {"index": i, "start_s": s.start_s, "end_s": s.end_s, "duration_s": round(s.end_s - s.start_s, 3)}
            for i, s in enumerate(spans, start=1)
        ])

        degradations: list[str] = []
        ocr_lines = [RawLine(l.text, l.start_s, l.end_s) for l in self._subtitles.extract(source_abs)] if self._subtitles.available else []
        asr_lines = [RawLine(l.text, l.start_s, l.end_s) for l in self._asr.transcribe(source_abs)] if self._asr.available else []
        if not self._subtitles.available:
            degradations.append("ocr_backend_unavailable")
        if not self._asr.available:
            degradations.append("asr_backend_unavailable")
        if not ocr_lines and asr_lines:
            degradations.append("asr_only_fidelity_degraded")

        reconciled = reconcile_lines(ocr_lines, asr_lines)
        flagged = sum(1 for r in reconciled if r.flagged)
        self._writer.write_json(dialogue_rel, {
            "lines": [
                {"text": r.text, "start_s": r.start_s, "end_s": r.end_s, "status": r.status,
                 "ocr_text": r.ocr_text, "asr_text": r.asr_text, "speaker": None, "attribution": "pending"}
                for r in reconciled
            ],
            "flagged_count": flagged,
            "degradations": degradations,
        })
        return ExtractResultCdto(
            episode_rel_dir=episode_rel_dir, shot_count=len(spans),
            dialogue_line_count=len(reconciled), flagged_line_count=flagged,
            degradations=degradations,
        )
