from collections.abc import Mapping
from dataclasses import dataclass
from fnmatch import fnmatchcase
from types import MappingProxyType

from libs.common.enums import ReferenceResolver, RefKind
from libs.domain.errors.config__error import ConfigError
from libs.domain.value_objects.config_table__valueobject import ConfigTable

RESOLVER_KIND: Mapping[ReferenceResolver, RefKind] = MappingProxyType({
    ReferenceResolver.ASSET_FILE: RefKind.IMAGE,
    ReferenceResolver.ENTITY: RefKind.ENTITY,
    ReferenceResolver.SHOT_VIDEO: RefKind.VIDEO,
    ReferenceResolver.PREV_SHOT_LASTFRAME: RefKind.FIRST_FRAME,
})


@dataclass(frozen=True)
class ReferenceRule:
    label_glob: str
    kind: RefKind
    resolver: ReferenceResolver

    def __post_init__(self) -> None:
        if not self.label_glob:
            raise ConfigError("references.rules", "label_glob 不能为空")
        if RESOLVER_KIND[self.resolver] is not self.kind:
            raise ConfigError(
                "references.rules",
                f"resolver {self.resolver} 只能配 kind={RESOLVER_KIND[self.resolver]}，实际 {self.kind}",
            )

    def matches(self, label: str) -> bool:
        return fnmatchcase(label, self.label_glob)

    def as_dict(self) -> dict[str, str]:
        return {"label_glob": self.label_glob, "kind": self.kind.value, "resolver": self.resolver.value}

    @classmethod
    def from_table(cls, table: ConfigTable) -> "ReferenceRule":
        table.only_keys(("label_glob", "kind", "resolver"))
        label_glob: str = table.string("label_glob")
        kind: RefKind = table.enum("kind", RefKind)
        resolver: ReferenceResolver = table.enum("resolver", ReferenceResolver)
        if RESOLVER_KIND[resolver] is not kind:
            raise ConfigError(table.at("kind"), f"resolver {resolver} 只能配 kind={RESOLVER_KIND[resolver]}，实际 {kind}")
        return cls(label_glob=label_glob, kind=kind, resolver=resolver)


def _rules(kind: RefKind, resolver: ReferenceResolver, *globs: str) -> tuple[ReferenceRule, ...]:
    return tuple(ReferenceRule(glob, kind, resolver) for glob in globs)


DEFAULT_REFERENCE_RULES: tuple[ReferenceRule, ...] = (
    *_rules(
        RefKind.IMAGE, ReferenceResolver.ASSET_FILE,
        "场景参考图*", "*锚点", "角色参考图", "单位参考图", "道具参考图", "场景主体", "物件主体",
    ),
    *_rules(RefKind.ENTITY, ReferenceResolver.ENTITY, "Seedance 人物 entity", "人物主体"),
    *_rules(RefKind.VIDEO, ReferenceResolver.SHOT_VIDEO, "previz灰模视频", "3D预演视频"),
    *_rules(RefKind.FIRST_FRAME, ReferenceResolver.PREV_SHOT_LASTFRAME, "上一镜末帧*"),
)
