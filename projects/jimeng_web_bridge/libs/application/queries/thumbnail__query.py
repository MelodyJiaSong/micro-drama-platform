from __future__ import annotations

from libs.application.dtos.thumbnail__dto import ThumbnailQdto
from libs.common.paths import RepoSandbox
from libs.domain.value_objects.global_config__valueobject import GlobalConfig
from libs.infrastructure.errors.artifact__error import UnsupportedThumbnailSourceError
from libs.infrastructure.errors.sandbox__error import SandboxError
from libs.infrastructure.readers.global_config__reader import GlobalConfigReader
from libs.infrastructure.readers.thumbnail__reader import ThumbnailReader

IMAGE_SUFFIXES: frozenset[str] = frozenset({".png", ".jpg", ".jpeg", ".webp"})
MIN_EDGE_PX: int = 16


class ThumbnailQuery:
    """`/api/thumbs`: reference-image previews, read only from `ai_videos/`, long edge ≤ `ui.reference_thumb_max_px`."""

    def __init__(
        self, sandbox: RepoSandbox, thumbnail_reader: ThumbnailReader, global_reader: GlobalConfigReader, test_mode: bool
    ) -> None:
        self._sandbox = sandbox
        self._thumbnails = thumbnail_reader
        self._global = global_reader
        self._test_mode = test_mode

    def get(self, path_rel: str, max_edge: int | None = None) -> ThumbnailQdto:
        if "\\" in path_rel:
            raise SandboxError("backslash", None)
        verdict = self._sandbox.check_read(path_rel)
        if verdict.path is None or verdict.rel is None:
            raise SandboxError(verdict.violation or "rejected", verdict.rel)
        if verdict.path.suffix.lower() not in IMAGE_SUFFIXES:
            raise UnsupportedThumbnailSourceError(verdict.path.suffix)
        if not verdict.path.is_file():
            raise FileNotFoundError(verdict.rel)
        thumbnail = self._thumbnails.thumbnail(verdict.path, self._edge(max_edge))
        return ThumbnailQdto(
            file_path=thumbnail.path, content_type=thumbnail.content_type, width=thumbnail.width, height=thumbnail.height
        )

    def _edge(self, requested: int | None) -> int:
        cap = GlobalConfig.from_dict(self._global.read().data, self._test_mode).ui.reference_thumb_max_px
        if requested is None:
            return cap
        return max(min(requested, cap), min(MIN_EDGE_PX, cap))
