from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

from libs.infrastructure.daos.config_file__dao import ConfigFileDao
from libs.infrastructure.readers.global_config__reader import GLOBAL_CONFIG_LOCATION
from libs.infrastructure.writers.toml_file__writer import TomlFileWriter


class GlobalConfigWriter:
    """The UI-only restriction (FR-4) is enforced at the route; this class only guarantees a safe round-trip."""

    def __init__(self, path: Path, location: str = GLOBAL_CONFIG_LOCATION) -> None:
        self._path: Path = path
        self._location: str = location
        self._toml: TomlFileWriter = TomlFileWriter()

    def save(self, data: Mapping[str, object], expected_sha256: str | None) -> ConfigFileDao:
        return self._toml.save(self._path, self._location, data, expected_sha256)

    def save_text(self, text: str, expected_sha256: str | None) -> ConfigFileDao:
        return self._toml.save_text(self._path, self._location, text, expected_sha256)
