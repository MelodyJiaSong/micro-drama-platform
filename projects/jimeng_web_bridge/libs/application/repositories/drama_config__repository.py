from __future__ import annotations

from collections.abc import Mapping

from libs.application.mappers.drama_config__mapper import DramaConfigMapper
from libs.domain.repositories.drama_config__repository import StoredDramaConfig
from libs.infrastructure.readers.drama_config__reader import DramaConfigReader
from libs.infrastructure.writers.drama_config__writer import DramaConfigWriter


class DramaConfigFileRepository:
    """Implements the domain `DramaConfigRepository` over `ai_videos/{drama_root}/jimeng_config.toml` (spec §8 div. 6).

    Pure persistence: schema validation stays with the caller (`DramaConfig.from_dict`). `drama_root` must be the
    canonical `ai_videos/…` form. Reader/writer errors pass through unchanged: `DramaRootNotFoundError`,
    `SandboxError`, `ConfigParseError`, `ConfigConflictError` (stale `expected_hash`; None = create-only) and
    `ConfigWriteError` (file untouched, safe to retry).
    """

    def __init__(self, reader: DramaConfigReader, writer: DramaConfigWriter, mapper: DramaConfigMapper) -> None:
        self._reader = reader
        self._writer = writer
        self._mapper = mapper

    def read(self, drama_root: str) -> StoredDramaConfig | None:
        return self._mapper.stored(self._reader.read(drama_root))

    def write(self, drama_root: str, data: Mapping[str, object], expected_hash: str | None) -> str:
        saved = self._writer.save(drama_root, data, expected_hash)
        return saved.sha256 or ""
