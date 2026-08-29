from __future__ import annotations

import json
import re
from pathlib import Path

from libs.application.dtos.ingest__dto import EpisodeSplitCdto, MediaValidationCdto
from libs.common.constants import MAX_UPLOAD_BYTES
from libs.domain.value_objects.episodesplit__valueobject import fuse_episode_boundaries
from libs.infrastructure.clients.ffmpeg__client import FfmpegClient
from libs.infrastructure.writers.artifact__writer import ArtifactWriter


class IngestCommand:
    """FR-1: media validation + whole-drama file auto-split into episodes."""

    def __init__(self, ffmpeg: FfmpegClient, writer: ArtifactWriter) -> None:
        self._ffmpeg = ffmpeg
        self._writer = writer

    def validate_media(self, rel_path: str, size_bytes: int) -> MediaValidationCdto:
        if size_bytes > MAX_UPLOAD_BYTES:
            return MediaValidationCdto(ok=False, duration_s=0, width=0, height=0, reason="file exceeds 2GB limit")
        info = self._ffmpeg.probe(self._writer.resolve(rel_path))
        if not info.decodable:
            return MediaValidationCdto(ok=False, duration_s=0, width=0, height=0, reason=f"undecodable: {info.detail}")
        return MediaValidationCdto(ok=True, duration_s=info.duration_s, width=info.width, height=info.height)

    def split_episodes(self, drama_id: str, source_rel_path: str) -> EpisodeSplitCdto:
        abs_source = self._writer.resolve(source_rel_path)
        info = self._ffmpeg.probe(abs_source)
        blacks = self._ffmpeg.black_ranges(abs_source)
        spans = fuse_episode_boundaries(info.duration_s, blacks)
        # append after the highest existing ep index — numbering from ep01 clobbered
        # prior episodes on 追加上传 (2026-07-18: an append reset a done episode's
        # source + state and the pipeline silently reprocessed it)
        start = _next_episode_index(self._writer.resolve(drama_id))
        rel_paths: list[str] = []
        for i, span in enumerate(spans, start=start):
            rel_dir = f"{drama_id}/ep{i:02d}"
            self._writer.ensure_dir(rel_dir)
            rel_clip = f"{rel_dir}/source.mp4"
            if len(spans) == 1:
                import shutil

                shutil.copyfile(abs_source, self._writer.resolve(rel_clip))
            else:
                self._ffmpeg.cut_clip(abs_source, span.start_s, span.end_s, self._writer.resolve(rel_clip))
            rel_paths.append(rel_clip)
        index_path = Path(self._writer.resolve(f"{drama_id}/episodes.json"))
        existing = json.loads(index_path.read_text(encoding="utf-8")) if index_path.exists() else []
        self._writer.write_json(
            f"{drama_id}/episodes.json",
            existing + [{"rel_path": p, "start_s": s.start_s, "end_s": s.end_s, "confidence": s.confidence}
                        for p, s in zip(rel_paths, spans)],
        )
        return EpisodeSplitCdto(episode_rel_paths=rel_paths, confidences=[s.confidence for s in spans])


def _next_episode_index(drama_abs_dir: str) -> int:
    root = Path(drama_abs_dir)
    if not root.exists():
        return 1
    taken = [int(m.group(1)) for p in root.iterdir()
             if p.is_dir() and (m := re.fullmatch(r"ep(\d{2,})", p.name))]
    return max(taken, default=0) + 1
