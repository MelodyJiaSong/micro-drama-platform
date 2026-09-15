from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

from libs.common.paths import RepoSandbox
from libs.infrastructure.daos.config_file__dao import ConfigFileDao
from libs.infrastructure.errors.config_io__error import DramaRootNotFoundError
from libs.infrastructure.errors.sandbox__error import SandboxError
from libs.infrastructure.readers.drama_config__reader import DramaConfigReader
from libs.infrastructure.writers.toml_file__writer import TomlFileWriter


class DramaConfigWriter:
    """Writes only `ai_videos/{drama_root}/jimeng_config.toml`; `expected_sha256=None` means "must not exist yet"."""

    def __init__(self, sandbox: RepoSandbox) -> None:
        self._sandbox: RepoSandbox = sandbox
        self._locator: DramaConfigReader = DramaConfigReader(sandbox)
        self._toml: TomlFileWriter = TomlFileWriter()

    def save(self, drama_rel: str, data: Mapping[str, object], expected_sha256: str | None) -> ConfigFileDao:
        rel, path = self._target(drama_rel)
        return self._toml.save(path, rel, data, expected_sha256)

    def save_text(self, drama_rel: str, text: str, expected_sha256: str | None) -> ConfigFileDao:
        rel, path = self._target(drama_rel)
        return self._toml.save_text(path, rel, text, expected_sha256)

    def _target(self, drama_rel: str) -> tuple[str, Path]:
        rel = self._locator.config_rel(drama_rel)
        verdict = self._sandbox.check_write(rel)
        if verdict.path is None:
            raise SandboxError(verdict.violation or "rejected", verdict.rel)
        if verdict.rel != rel or not verdict.path.parent.is_dir():
            raise DramaRootNotFoundError(drama_rel)
        return rel, verdict.path
