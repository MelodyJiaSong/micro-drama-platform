import re
from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

from libs.common.enums import ReferenceResolver, RefKind
from libs.domain.errors.config__error import ConfigError
from libs.domain.value_objects.config_table__valueobject import key_path
from libs.domain.value_objects.reference_rule__valueobject import ReferenceRule

ENTITY_PREFIX = "entity:"
_EXTENSION_KIND: Mapping[str, RefKind] = MappingProxyType({
    ".png": RefKind.IMAGE, ".jpg": RefKind.IMAGE, ".jpeg": RefKind.IMAGE, ".webp": RefKind.IMAGE,
    ".mp4": RefKind.VIDEO, ".mov": RefKind.VIDEO,
    ".mp3": RefKind.AUDIO, ".wav": RefKind.AUDIO, ".m4a": RefKind.AUDIO,
})


@dataclass(frozen=True)
class ReferenceOverride:
    name: str
    target_path: str | None
    entity_name: str | None

    @classmethod
    def parse(cls, name: str, value: str) -> "ReferenceOverride":
        path: str = key_path("references.overrides", name)
        if value.startswith(ENTITY_PREFIX):
            entity_name: str = value[len(ENTITY_PREFIX):]
            if not entity_name:
                raise ConfigError(path, "entity: 后面必须写主体名")
            return cls(name=name, target_path=None, entity_name=entity_name)
        segments: list[str] = value.split("/")
        if (
            not value.startswith("ai_videos/")
            or "\\" in value
            or ":" in value
            or any(segment in ("", ".", "..") for segment in segments)
        ):
            raise ConfigError(path, "必须是 ai_videos/ 开头的正斜杠相对路径（不含 ..、盘符、反斜杠），或 entity:{主体名}")
        return cls(name=name, target_path=value, entity_name=None)

    @property
    def inferred_kind(self) -> RefKind | None:
        if self.entity_name is not None:
            return RefKind.ENTITY
        match = re.search(r"\.[A-Za-z0-9]+$", self.target_path or "")
        return None if match is None else _EXTENSION_KIND.get(match.group(0).lower())


@dataclass(frozen=True)
class ReferenceRoute:
    kind: RefKind
    resolver: ReferenceResolver | None
    override: ReferenceOverride | None
    rule: ReferenceRule | None


@dataclass(frozen=True)
class ReferenceRouting:
    rules: tuple[ReferenceRule, ...]
    overrides: Mapping[str, ReferenceOverride]

    def __post_init__(self) -> None:
        object.__setattr__(self, "overrides", MappingProxyType(dict(self.overrides)))

    def first_rule(self, label: str) -> ReferenceRule | None:
        return next((rule for rule in self.rules if rule.matches(label)), None)

    def route(self, name: str, label: str) -> ReferenceRoute | None:
        rule: ReferenceRule | None = self.first_rule(label)
        override: ReferenceOverride | None = self.overrides.get(name)
        if override is not None:
            kind: RefKind | None = override.inferred_kind
            if override.entity_name is None and rule is not None and rule.kind is not RefKind.ENTITY:
                kind = rule.kind
            return None if kind is None else ReferenceRoute(kind=kind, resolver=None, override=override, rule=rule)
        if rule is not None:
            return ReferenceRoute(kind=rule.kind, resolver=rule.resolver, override=None, rule=rule)
        return None
