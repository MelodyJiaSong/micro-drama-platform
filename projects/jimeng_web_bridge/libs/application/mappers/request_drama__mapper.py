from __future__ import annotations

import re
from dataclasses import dataclass

from libs.common.enums import CheckSeverity, PrecheckCheck
from libs.domain.errors.config__error import ConfigError
from libs.domain.value_objects.drama_config__valueobject import DramaConfig
from libs.domain.value_objects.model_limits__valueobject import ModelLimits
from libs.domain.value_objects.precheck_result__valueobject import PrecheckItem
from libs.infrastructure.errors.config_io__error import ConfigParseError
from libs.infrastructure.readers.drama_config__reader import DramaConfigReader

_ABBREV_RE = re.compile(r"^[A-Za-z0-9_]{1,16}$")
_SERIES_EPISODE_DEPTH: int = 3


@dataclass(frozen=True)
class DramaSettings:
    """The drama config a request was built with, plus the notices precheck appends (missing / invalid file)."""

    drama_rel: str | None
    config: DramaConfig
    file_sha256: str | None
    notices: tuple[PrecheckItem, ...]

    @property
    def has_usable_file(self) -> bool:
        return self.file_sha256 is not None and not any(n.severity is CheckSeverity.ERROR for n in self.notices)


class DramaSettingsMapper:
    def __init__(self, reader: DramaConfigReader) -> None:
        self._reader: DramaConfigReader = reader

    def load(self, drama_rel: str | None, limits: ModelLimits) -> DramaSettings:
        if drama_rel is None:
            return DramaSettings(None, DramaConfig.from_dict(DramaConfig.defaults(""), limits), None, ())
        abbrev: str = _default_abbrev(drama_rel)
        try:
            stored = self._reader.read(drama_rel)
        except ConfigParseError as error:
            notice = PrecheckItem(
                PrecheckCheck.PARAMS, CheckSeverity.ERROR, "drama_config_invalid",
                f"{error.location} 不是合法的 TOML：{error.detail}",
            )
            return _defaults(drama_rel, abbrev, limits, None, notice)
        if not stored.exists:
            notice = PrecheckItem(
                PrecheckCheck.PARAMS, CheckSeverity.WARNING, "drama_config_missing",
                f"{drama_rel} 还没有 jimeng_config.toml，本次按默认值预检；请在「剧 config」页点「生成默认 config」后保存",
            )
            return _defaults(drama_rel, abbrev, limits, None, notice)
        try:
            return DramaSettings(drama_rel, DramaConfig.from_dict(stored.data, limits), stored.sha256, ())
        except ConfigError as error:
            notice = PrecheckItem(
                PrecheckCheck.PARAMS, CheckSeverity.ERROR, "drama_config_invalid",
                f"jimeng_config.toml 的 {error.field_path}：{error.message}", error.field_path,
            )
            return _defaults(drama_rel, abbrev, limits, stored.sha256, notice)


class DramaSettingsCache:
    """One config read per drama per precheck call, shared by every item and by cross-episode naming."""

    def __init__(self, mapper: DramaSettingsMapper, limits: ModelLimits) -> None:
        self._mapper: DramaSettingsMapper = mapper
        self._limits: ModelLimits = limits
        self._loaded: dict[str | None, DramaSettings] = {}

    def get(self, drama_rel: str | None) -> DramaSettings:
        if drama_rel not in self._loaded:
            self._loaded[drama_rel] = self._mapper.load(drama_rel, self._limits)
        return self._loaded[drama_rel]


def _defaults(
    drama_rel: str, abbrev: str, limits: ModelLimits, file_sha256: str | None, notice: PrecheckItem
) -> DramaSettings:
    return DramaSettings(drama_rel, DramaConfig.from_dict(DramaConfig.defaults(abbrev), limits), file_sha256, (notice,))


def _default_abbrev(drama_rel: str) -> str:
    parts: list[str] = drama_rel.split("/")
    episode: str = parts[-1]
    return episode if len(parts) == _SERIES_EPISODE_DEPTH and _ABBREV_RE.match(episode) else ""
