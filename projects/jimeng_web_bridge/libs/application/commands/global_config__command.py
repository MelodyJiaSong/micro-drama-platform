from __future__ import annotations

import json
import logging
from collections.abc import Mapping

from libs.application.dtos.global_config__dto import GlobalConfigSaveCdto
from libs.application.mappers.drama_config__mapper import DramaConfigMapper
from libs.domain.errors.config__error import ConfigError
from libs.domain.value_objects.global_config__valueobject import GlobalConfig
from libs.infrastructure.errors.config_io__error import ConfigParseError
from libs.infrastructure.readers.global_config__reader import GlobalConfigReader
from libs.infrastructure.readers.toml_file__reader import TomlFileReader
from libs.infrastructure.writers.global_config__writer import GlobalConfigWriter

AUDIT_LOGGER_NAME: str = "jimeng_web_bridge.audit"
CLI_PATH_KEY: str = "cli.path"
BODY_FIELD: str = "<body>"


class GlobalConfigCommand:
    """UI-only at the route (FR-4). Every value, bound and cross-field rule comes from `GlobalConfig.from_dict`."""

    def __init__(
        self,
        reader: GlobalConfigReader,
        writer: GlobalConfigWriter,
        toml_reader: TomlFileReader,
        mapper: DramaConfigMapper,
        test_mode: bool,
        audit_logger: logging.Logger | None = None,
    ) -> None:
        self._reader = reader
        self._writer = writer
        self._toml = toml_reader
        self._mapper = mapper
        self._test_mode = test_mode
        self._audit = audit_logger or logging.getLogger(AUDIT_LOGGER_NAME)

    def save(
        self, data: Mapping[str, object] | None, text: str | None, expected_sha256: str | None
    ) -> GlobalConfigSaveCdto:
        if (data is None) == (text is None):
            raise ConfigError(BODY_FIELD, "data 与 text 必须且只能提供一个")
        try:
            current = self._reader.read()
            location, current_data = current.location, current.data
        except ConfigParseError as error:
            location, current_data = error.location, {}
        parsed = data if text is None else self._toml.parse_document(text, location).unwrap()
        GlobalConfig.from_dict(parsed, self._test_mode)
        saved = self._writer.save(parsed, expected_sha256) if text is None else self._writer.save_text(text, expected_sha256)
        changes = self._mapper.diff(current_data, parsed)
        for change in changes:
            if change.key == CLI_PATH_KEY:
                self._log(logging.WARNING, "global_config.cli_path_changed", before=change.current, after=change.proposed)
        changed_keys = tuple(change.key for change in changes)
        self._log(logging.INFO, "global_config.saved", location=saved.location, changed_keys=list(changed_keys))
        return GlobalConfigSaveCdto(location=saved.location, sha256=saved.sha256 or "", changed_keys=changed_keys)

    def _log(self, level: int, event: str, **fields: object) -> None:
        self._audit.log(level, json.dumps({"event": event, **fields}, ensure_ascii=False, default=str))
