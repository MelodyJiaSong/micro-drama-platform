from __future__ import annotations

from pathlib import Path

from libs.infrastructure.daos.config_file__dao import ConfigFileDao
from libs.infrastructure.readers.toml_file__reader import TomlFileReader

GLOBAL_CONFIG_LOCATION: str = "config/global.toml"


class GlobalConfigReader:
    """Path is fixed by the container (`JIMENG_BRIDGE_GLOBAL_CONFIG` in tests), never taken from a request."""

    def __init__(self, path: Path, location: str = GLOBAL_CONFIG_LOCATION) -> None:
        self._path: Path = path
        self._location: str = location
        self._toml: TomlFileReader = TomlFileReader()

    def read(self) -> ConfigFileDao:
        return self._toml.read(self._path, self._location)
