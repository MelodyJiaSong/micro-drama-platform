from __future__ import annotations

from collections.abc import Mapping, Sequence

from libs.application.dtos.drama_config__dto import ConfigErrorQdto
from libs.application.dtos.global_config__dto import GlobalConfigQdto
from libs.application.mappers.drama_config__mapper import DramaConfigMapper
from libs.domain.errors.config__error import ConfigError
from libs.domain.value_objects.global_config__valueobject import GLOBAL_SECTIONS, GlobalConfig
from libs.infrastructure.errors.config_io__error import ConfigParseError
from libs.infrastructure.readers.global_config__reader import GlobalConfigReader

REDACTED: str = "[redacted]"
_MIN_SECRET_CHARS: int = 8


class GlobalConfigQuery:
    """Reads only `global.toml` (never `.env`). Known secret values are redacted as defence in depth (SEC-K04/S01)."""

    def __init__(
        self,
        reader: GlobalConfigReader,
        mapper: DramaConfigMapper,
        test_mode: bool,
        env_overridden_keys: Sequence[str] = (),
        secret_values: Sequence[str] = (),
    ) -> None:
        self._reader = reader
        self._mapper = mapper
        self._test_mode = test_mode
        self._overridden = tuple(env_overridden_keys)
        self._secrets = tuple(secret for secret in secret_values if len(secret) >= _MIN_SECRET_CHARS)

    def get(self) -> GlobalConfigQdto:
        try:
            stored = self._reader.read()
        except ConfigParseError as error:
            return GlobalConfigQdto(error.location, {}, None, None, self._redact_text(error.detail), None, self._overridden)
        validation: ConfigErrorQdto | None = None
        try:
            GlobalConfig.from_dict(stored.data, self._test_mode)
        except ConfigError as error:
            validation = self._mapper.config_error(error)
        values = {key: self._redact(value) for key, value in stored.data.items() if key in GLOBAL_SECTIONS}
        return GlobalConfigQdto(
            location=stored.location,
            values=values,
            raw_text=None if stored.raw_text is None else self._redact_text(stored.raw_text),
            sha256=stored.sha256,
            parse_error=None,
            validation_error=validation,
            overridden_by_env=self._overridden,
        )

    def _redact(self, value: object) -> object:
        if isinstance(value, str):
            return self._redact_text(value)
        if isinstance(value, Mapping):
            return {key: self._redact(item) for key, item in value.items()}
        if isinstance(value, list):
            return [self._redact(item) for item in value]
        return value

    def _redact_text(self, text: str) -> str:
        for secret in self._secrets:
            text = text.replace(secret, REDACTED)
        return text
