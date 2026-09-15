import re
from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

from libs.common.enums import GenerationKind, NegativePromptStrategy
from libs.domain.errors.config__error import ConfigError
from libs.domain.value_objects.config_table__valueobject import ConfigTable
from libs.domain.value_objects.drama_config_sections__valueobject import check_relative, check_template
from libs.domain.value_objects.model_limits__valueobject import RATIO_PATTERN, ModelLimits

ROUTING_KEY = re.compile(r"^(bg|c|p)\d+-\d+$")
SUBJECT_KINDS: tuple[str, ...] = ("characters", "scenes", "props")
MAX_COUNT = 4


@dataclass(frozen=True)
class VideoConfig:
    model: str
    resolution: str
    count: int
    ratio_source: str
    duration_source: str
    negative_prompt: NegativePromptStrategy


@dataclass(frozen=True)
class ImageBlockOverride:
    ratio: str | None
    model: str | None
    reference_keys: tuple[str, ...]


@dataclass(frozen=True)
class ImageConfig:
    model: str
    resolution: str
    count: int
    ratio_by_subject: Mapping[str, str]
    block_overrides: Mapping[str, ImageBlockOverride]

    def __post_init__(self) -> None:
        object.__setattr__(self, "ratio_by_subject", MappingProxyType(dict(self.ratio_by_subject)))
        object.__setattr__(self, "block_overrides", MappingProxyType(dict(self.block_overrides)))


@dataclass(frozen=True)
class VideoBlockMatch:
    first_line_contains: tuple[str, ...]
    has_field: tuple[str, ...]


@dataclass(frozen=True)
class VideoDefault:
    model: str
    resolution: str
    ratio: str
    duration_s: int


@dataclass(frozen=True)
class AssetsConfig:
    video_block_match: VideoBlockMatch
    video_reference: str
    video_default: VideoDefault


def _model(table: ConfigTable, key: str, limits: ModelLimits, kind: GenerationKind) -> str:
    model: str = table.string(key)
    capability = limits.find(model)
    if capability is None:
        raise ConfigError(table.at(key), f"model_limits 里没有模型 {model!r}")
    if capability.kind is not kind:
        raise ConfigError(table.at(key), f"{model} 不是{'视频' if kind is GenerationKind.VIDEO else '图片'}模型")
    return model


def _resolution(table: ConfigTable, key: str, limits: ModelLimits, kind: GenerationKind) -> str:
    resolution: str = table.string(key)
    if resolution not in limits.resolutions_for(kind):
        raise ConfigError(table.at(key), f"没有任何{kind}模型支持分辨率 {resolution!r}")
    return resolution


def _ratio(table: ConfigTable, key: str) -> str:
    return table.string(key, pattern=RATIO_PATTERN)


def parse_video(root: ConfigTable, limits: ModelLimits) -> VideoConfig:
    table: ConfigTable = root.table("video")
    table.only_keys(("model", "resolution", "count", "ratio_source", "duration_source", "negative_prompt"))
    return VideoConfig(
        model=_model(table, "model", limits, GenerationKind.VIDEO),
        resolution=_resolution(table, "resolution", limits, GenerationKind.VIDEO),
        count=table.integer("count", 1, MAX_COUNT),
        ratio_source=table.one_of("ratio_source", ("shot",)),
        duration_source=table.one_of("duration_source", ("shot",)),
        negative_prompt=table.enum("negative_prompt", NegativePromptStrategy),
    )


def parse_image(root: ConfigTable, limits: ModelLimits) -> ImageConfig:
    table: ConfigTable = root.table("image")
    table.only_keys(("model", "resolution", "count", "ratio_by_subject", "block_overrides"))
    ratios: ConfigTable = table.table("ratio_by_subject")
    ratios.only_keys(SUBJECT_KINDS)
    overrides_table: ConfigTable = table.table("block_overrides")
    block_overrides: dict[str, ImageBlockOverride] = {}
    for key in overrides_table.keys():
        if not ROUTING_KEY.match(key):
            raise ConfigError(overrides_table.at(key), "键必须是路由键（如 c1-1）")
        block: ConfigTable = overrides_table.table(key)
        block.only_keys(("ratio", "model", "reference_keys"))
        reference_keys: tuple[str, ...] = (
            block.string_list("reference_keys", allow_empty=True) if block.has("reference_keys") else ()
        )
        for index, ref_key in enumerate(reference_keys):
            if not ROUTING_KEY.match(ref_key):
                raise ConfigError(f"{block.at('reference_keys')}[{index}]", "必须是路由键（如 c1-1）")
        block_overrides[key] = ImageBlockOverride(
            ratio=_ratio(block, "ratio") if block.has("ratio") else None,
            model=_model(block, "model", limits, GenerationKind.IMAGE) if block.has("model") else None,
            reference_keys=reference_keys,
        )
    return ImageConfig(
        model=_model(table, "model", limits, GenerationKind.IMAGE),
        resolution=_resolution(table, "resolution", limits, GenerationKind.IMAGE),
        count=table.integer("count", 1, MAX_COUNT),
        ratio_by_subject={kind: _ratio(ratios, kind) for kind in SUBJECT_KINDS},
        block_overrides=block_overrides,
    )


def parse_assets(root: ConfigTable, limits: ModelLimits) -> AssetsConfig:
    table: ConfigTable = root.table("assets")
    table.only_keys(("video_block_match", "video_reference", "video_default"))
    match: ConfigTable = table.table("video_block_match")
    match.only_keys(("first_line_contains", "has_field"))
    block_match = VideoBlockMatch(
        first_line_contains=match.string_list("first_line_contains", allow_empty=True),
        has_field=match.string_list("has_field", allow_empty=True),
    )
    if not block_match.first_line_contains and not block_match.has_field:
        raise ConfigError(match.path, "两个条件不能同时为空")
    reference: str = table.string("video_reference")
    check_relative(reference, table.at("video_reference"))
    check_template(reference, table.at("video_reference"), ("card_dir", "N"), ("card_dir",))
    default: ConfigTable = table.table("video_default")
    default.only_keys(("model", "resolution", "ratio", "duration_s"))
    return AssetsConfig(
        video_block_match=block_match,
        video_reference=reference,
        video_default=VideoDefault(
            model=_model(default, "model", limits, GenerationKind.VIDEO),
            resolution=_resolution(default, "resolution", limits, GenerationKind.VIDEO),
            ratio=_ratio(default, "ratio"),
            duration_s=default.integer("duration_s", 1),
        ),
    )
