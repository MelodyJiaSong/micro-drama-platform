import re
from collections.abc import Iterable
from dataclasses import dataclass
from string import Formatter

from libs.common.enums import OnExisting
from libs.domain.errors.config__error import ConfigError
from libs.domain.value_objects.config_table__valueobject import ConfigTable
from libs.domain.value_objects.entity_naming__valueobject import EntityNaming, validate_name_template
from libs.domain.value_objects.reference_routing__valueobject import ReferenceOverride, ReferenceRouting
from libs.domain.value_objects.reference_rule__valueobject import ReferenceRule

_ABBREV = re.compile(r"^[A-Za-z0-9_]{1,16}$")


@dataclass(frozen=True)
class DramaSection:
    abbrev: str


@dataclass(frozen=True)
class EntitiesConfig:
    naming: EntityNaming
    source_images: tuple[str, ...]
    description_from: str


@dataclass(frozen=True)
class ReferencesConfig:
    routing: ReferenceRouting
    search_exclude: tuple[str, ...]


@dataclass(frozen=True)
class OutputsConfig:
    video_name: str
    image_candidates_dir: str
    on_existing: OnExisting


@dataclass(frozen=True)
class PrecheckConfig:
    prompt_max_chars: int
    entity_name_max_chars: int
    estimate_tolerance_pct: int


def check_template(value: str, path: str, allowed: Iterable[str], required: Iterable[str]) -> None:
    allowed_set: frozenset[str] = frozenset(allowed)
    try:
        fields: set[str] = {field for _, field, _, _ in Formatter().parse(value) if field is not None}
    except ValueError as exc:
        raise ConfigError(path, f"模板花括号不合法：{exc}") from exc
    unknown: set[str] = fields - allowed_set
    if unknown:
        raise ConfigError(path, f"未知占位符 {{{sorted(unknown)[0]}}}")
    missing: set[str] = set(required) - fields
    if missing:
        raise ConfigError(path, f"必须包含 {{{sorted(missing)[0]}}}")


def check_relative(value: str, path: str) -> None:
    segments: list[str] = re.split(r"[\\/]", value)
    if re.match(r"^([A-Za-z]:|[\\/])", value) or ".." in segments or ":" in value:
        raise ConfigError(path, "必须是相对路径，不能含 ..、盘符或绝对路径")


def parse_drama(root: ConfigTable) -> DramaSection:
    table: ConfigTable = root.table("drama")
    table.only_keys(("abbrev",))
    return DramaSection(abbrev=table.string("abbrev", allow_empty=True, pattern=_ABBREV))


def parse_entities(root: ConfigTable, abbrev: str, entity_name_max_chars: int) -> EntitiesConfig:
    table: ConfigTable = root.table("entities")
    table.only_keys(
        ("name_template", "overrides", "source_images", "description_from"),
        {"snapshot_stale_h": "entities.snapshot_stale_h 是全局键，只能写在 global.toml"},
    )
    template: str = table.string("name_template")
    validate_name_template(template, table.at("name_template"))
    overrides: dict[str, str] = table.string_map("overrides")
    override_table: ConfigTable = table.table("overrides")
    for name, value in overrides.items():
        if len(value) > entity_name_max_chars:
            raise ConfigError(override_table.at(name), f"主体名超过 {entity_name_max_chars} 码点")
    source_images: tuple[str, ...] = table.string_list("source_images")
    for index, pattern in enumerate(source_images):
        path: str = f"{table.at('source_images')}[{index}]"
        check_relative(pattern, path)
        check_template(pattern, path, ("card_dir", "card_dir_name"), ("card_dir",))
    return EntitiesConfig(
        naming=EntityNaming(abbrev=abbrev, name_template=template, overrides=overrides),
        source_images=source_images,
        description_from=table.one_of("description_from", ("locked_descriptor",)),
    )


def parse_references(root: ConfigTable) -> ReferencesConfig:
    table: ConfigTable = root.table("references")
    table.only_keys(("rules", "overrides", "search_exclude"))
    rules: tuple[ReferenceRule, ...] = tuple(ReferenceRule.from_table(row) for row in table.table_list("rules"))
    overrides: dict[str, ReferenceOverride] = {
        name: ReferenceOverride.parse(name, value) for name, value in table.string_map("overrides").items()
    }
    search_exclude: tuple[str, ...] = table.string_list("search_exclude", allow_empty=True)
    for index, entry in enumerate(search_exclude):
        check_relative(entry, f"{table.at('search_exclude')}[{index}]")
    return ReferencesConfig(routing=ReferenceRouting(rules=rules, overrides=overrides), search_exclude=search_exclude)


def parse_outputs(root: ConfigTable) -> OutputsConfig:
    table: ConfigTable = root.table("outputs")
    table.only_keys(("video_name", "image_candidates_dir", "on_existing"))
    video_name: str = table.string("video_name")
    if not video_name.endswith(".mp4") or re.search(r"[\\/]", video_name) or ".." in video_name:
        raise ConfigError(table.at("video_name"), "必须是以 .mp4 结尾的纯文件名（不含路径分隔符或 ..）")
    check_template(video_name, table.at("video_name"), ("shot", "ts", "suffix"), ("ts", "suffix"))
    candidates_dir: str = table.string("image_candidates_dir")
    check_relative(candidates_dir, table.at("image_candidates_dir"))
    check_template(candidates_dir, table.at("image_candidates_dir"), ("key",), ("key",))
    return OutputsConfig(
        video_name=video_name,
        image_candidates_dir=candidates_dir,
        on_existing=table.enum("on_existing", OnExisting),
    )


def parse_precheck(root: ConfigTable) -> PrecheckConfig:
    table: ConfigTable = root.table("precheck")
    table.only_keys(("prompt_max_chars", "entity_name_max_chars", "estimate_tolerance_pct"))
    return PrecheckConfig(
        prompt_max_chars=table.integer("prompt_max_chars", 1),
        entity_name_max_chars=table.integer("entity_name_max_chars", 1),
        estimate_tolerance_pct=table.integer("estimate_tolerance_pct", 0, 100),
    )
