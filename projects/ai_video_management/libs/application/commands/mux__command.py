"""BGM-mux command: add an uploaded BGM track to an uploaded video.

Upload streaming and the ffmpeg subprocess live in infrastructure
(`mux__writer.py`); this layer only carries the operation.
"""
from __future__ import annotations

from typing import BinaryIO

from libs.application.dtos.mux__dto import MuxOptions, MuxResult
from libs.infrastructure.writers.mux__writer import BgmMuxer


class MuxCommand:
    def __init__(self, muxer: BgmMuxer) -> None:
        self._muxer = muxer

    def add_bgm(
        self,
        video_name: str,
        video_stream: BinaryIO,
        audio_name: str,
        audio_stream: BinaryIO,
        options: MuxOptions,
    ) -> MuxResult:
        return self._muxer.add_bgm(
            video_name, video_stream, audio_name, audio_stream, options
        )
