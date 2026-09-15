from __future__ import annotations

import hashlib
from pathlib import Path

import tomlkit
from tomlkit.exceptions import TOMLKitError
from tomlkit.toml_document import TOMLDocument

from libs.infrastructure.daos.config_file__dao import ConfigFileDao
from libs.infrastructure.errors.config_io__error import ConfigParseError


class TomlFileReader:
    """The content hash is over the raw bytes, so the save-time conflict check sees whitespace-only edits too."""

    def read(self, path: Path, location: str) -> ConfigFileDao:
        if not path.is_file():
            return ConfigFileDao(location=location, exists=False, data={}, sha256=None, raw_text=None)
        raw = path.read_bytes()
        text = self.decode(raw, location)
        return ConfigFileDao(
            location=location,
            exists=True,
            data=self.parse_document(text, location).unwrap(),
            sha256=hashlib.sha256(raw).hexdigest(),
            raw_text=text,
        )

    def decode(self, raw: bytes, location: str) -> str:
        try:
            return raw.decode("utf-8-sig")
        except UnicodeDecodeError as error:
            raise ConfigParseError(location, "not valid UTF-8") from error

    def parse_document(self, text: str, location: str) -> TOMLDocument:
        try:
            return tomlkit.parse(text)
        except TOMLKitError as error:
            raise ConfigParseError(location, str(error)) from error
