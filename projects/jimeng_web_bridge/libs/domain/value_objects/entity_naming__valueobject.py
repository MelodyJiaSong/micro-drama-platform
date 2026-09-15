import re
from collections.abc import Mapping
from dataclasses import dataclass
from string import Formatter
from types import MappingProxyType

from libs.domain.errors.config__error import ConfigError, MissingAbbrevError

DEFAULT_NAME_TEMPLATE = "{abbrev}_{character_name}"
_CARD_PREFIX = re.compile(r"^c\d+_")
_PLACEHOLDERS: frozenset[str] = frozenset({"abbrev", "character_name"})


@dataclass(frozen=True)
class EntityNaming:
    abbrev: str
    name_template: str
    overrides: Mapping[str, str]

    def __post_init__(self) -> None:
        validate_name_template(self.name_template, "entities.name_template")
        object.__setattr__(self, "overrides", MappingProxyType(dict(self.overrides)))

    @staticmethod
    def character_name(card_dir_name: str) -> str:
        stripped: str = _CARD_PREFIX.sub("", card_dir_name, count=1)
        return stripped or card_dir_name

    def entity_name(self, card_dir_name: str) -> str:
        override: str | None = self.overrides.get(card_dir_name)
        if override is not None:
            return override
        if "{abbrev}" in self.name_template and self.abbrev == "":
            raise MissingAbbrevError("drama.abbrev", "独立剧没有填写缩写，无法按模板生成主体名")
        return self.name_template.format(abbrev=self.abbrev, character_name=self.character_name(card_dir_name))

    @classmethod
    def for_linked_card(
        cls, source: "EntityNaming | None", source_episode_dir: str, fallback_template: str
    ) -> "EntityNaming":
        if source is not None:
            return source
        return cls(abbrev=source_episode_dir, name_template=fallback_template, overrides={})


def validate_name_template(template: str, field_path: str) -> None:
    if template == "":
        raise ConfigError(field_path, "不能为空")
    try:
        fields: list[tuple[str, str | None, str | None, str | None]] = list(Formatter().parse(template))
    except ValueError as exc:
        raise ConfigError(field_path, f"模板花括号不合法：{exc}") from exc
    names: set[str] = set()
    for _, field, spec, conversion in fields:
        if field is None:
            continue
        if field not in _PLACEHOLDERS or spec or conversion:
            raise ConfigError(field_path, f"只允许占位符 {{abbrev}} 与 {{character_name}}，实际 {{{field}}}")
        names.add(field)
    if "character_name" not in names:
        raise ConfigError(field_path, "必须包含 {character_name}")
