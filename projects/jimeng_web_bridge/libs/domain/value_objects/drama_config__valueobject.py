from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

from libs.domain.value_objects.config_table__valueobject import ConfigTable
from libs.domain.value_objects.drama_config_generation__valueobject import (
    AssetsConfig, ImageConfig, VideoConfig, parse_assets, parse_image, parse_video,
)
from libs.domain.value_objects.drama_config_sections__valueobject import (
    DramaSection, EntitiesConfig, OutputsConfig, PrecheckConfig, ReferencesConfig,
    parse_drama, parse_entities, parse_outputs, parse_precheck, parse_references,
)
from libs.domain.value_objects.entity_naming__valueobject import DEFAULT_NAME_TEMPLATE, EntityNaming
from libs.domain.value_objects.global_config__valueobject import GLOBAL_SECTIONS
from libs.domain.value_objects.model_limits__valueobject import ModelLimits
from libs.domain.value_objects.reference_rule__valueobject import DEFAULT_REFERENCE_RULES

DRAMA_SECTIONS: tuple[str, ...] = ("drama", "entities", "references", "video", "image", "assets", "outputs", "precheck")
_GLOBAL_ONLY_HINTS: Mapping[str, str] = MappingProxyType({
    name: f"[{name}] 是全局 config 的节，不得出现在每剧 jimeng_config.toml" for name in GLOBAL_SECTIONS
    if name not in DRAMA_SECTIONS
})


@dataclass(frozen=True)
class DramaConfig:
    drama: DramaSection
    entities: EntitiesConfig
    references: ReferencesConfig
    video: VideoConfig
    image: ImageConfig
    assets: AssetsConfig
    outputs: OutputsConfig
    precheck: PrecheckConfig

    @property
    def entity_naming(self) -> EntityNaming:
        return self.entities.naming

    @classmethod
    def from_dict(cls, data: Mapping[str, object], limits: ModelLimits) -> "DramaConfig":
        root: ConfigTable = ConfigTable.of(data)
        root.only_keys(DRAMA_SECTIONS, _GLOBAL_ONLY_HINTS)
        drama: DramaSection = parse_drama(root)
        precheck: PrecheckConfig = parse_precheck(root)
        return cls(
            drama=drama,
            entities=parse_entities(root, drama.abbrev, precheck.entity_name_max_chars),
            references=parse_references(root),
            video=parse_video(root, limits),
            image=parse_image(root, limits),
            assets=parse_assets(root, limits),
            outputs=parse_outputs(root),
            precheck=precheck,
        )

    @staticmethod
    def defaults(abbrev: str) -> dict[str, object]:
        return {
            "drama": {"abbrev": abbrev},
            "entities": {
                "name_template": DEFAULT_NAME_TEMPLATE,
                "overrides": {},
                "source_images": ["{card_dir}/c*-1.*", "{card_dir}/{card_dir_name}.png"],
                "description_from": "locked_descriptor",
            },
            "references": {
                "rules": [rule.as_dict() for rule in DEFAULT_REFERENCE_RULES],
                "overrides": {},
                "search_exclude": ["_deleted", "_candidates", "renders", "frames", "_blender"],
            },
            "video": {
                "model": "seedance2.5",
                "resolution": "720p",
                "count": 1,
                "ratio_source": "shot",
                "duration_source": "shot",
                "negative_prompt": "platform_field_or_omit",
            },
            "image": {
                "model": "seedream5.0",
                "resolution": "2k",
                "count": 1,
                "ratio_by_subject": {"characters": "3:4", "scenes": "16:9", "props": "1:1"},
                "block_overrides": {},
            },
            "assets": {
                "video_block_match": {"first_line_contains": ["turntable"], "has_field": ["时长:"]},
                "video_reference": "{card_dir}/c{N}-1.*",
                "video_default": {"model": "seedance2.5", "resolution": "720p", "ratio": "9:16", "duration_s": 4},
            },
            "outputs": {
                "video_name": "{shot}_{ts}{suffix}.mp4",
                "image_candidates_dir": "_candidates/{key}",
                "on_existing": "archive",
            },
            "precheck": {"prompt_max_chars": 5000, "entity_name_max_chars": 20, "estimate_tolerance_pct": 20},
        }
