import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from types import MappingProxyType

from libs.common.enums import BackendKind, GenerationKind, RefKind
from libs.domain.errors.config__error import ConfigError, UnknownModelError
from libs.domain.value_objects.config_table__valueobject import ConfigTable, key_path
from libs.domain.value_objects.reference_item__valueobject import ReferenceItem

RATIO_PATTERN = re.compile(r"^[1-9]\d*:[1-9]\d*$")
AS_OF_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

_MODEL_KEYS: tuple[str, ...] = (
    "backends", "duration_s", "resolutions", "ratios", "max_images", "max_videos", "max_audios",
    "entities", "count_entities_as_images", "negative_prompt_field",
)


@dataclass(frozen=True)
class ModelCapability:
    key: str
    backends: frozenset[BackendKind]
    duration_range: tuple[int, int] | None
    resolutions: tuple[str, ...]
    ratios: tuple[str, ...]
    max_images: int
    max_videos: int
    max_audios: int
    entities: bool
    count_entities_as_images: bool
    negative_prompt_field: bool

    @property
    def kind(self) -> GenerationKind:
        return GenerationKind.VIDEO if self.duration_range is not None else GenerationKind.IMAGE

    def supports_backend(self, backend: BackendKind) -> bool:
        return backend in self.backends

    def supports_duration(self, duration_s: int) -> bool:
        return self.duration_range is not None and self.duration_range[0] <= duration_s <= self.duration_range[1]

    def supports_resolution(self, resolution: str) -> bool:
        return resolution in self.resolutions

    def supports_ratio(self, ratio: str) -> bool:
        return ratio in self.ratios

    def supports_entities_on(self, backend: BackendKind) -> bool:
        return self.entities and backend is BackendKind.WEB

    def image_count(self, references: Sequence[ReferenceItem]) -> int:
        counted: set[RefKind] = {RefKind.IMAGE, RefKind.FIRST_FRAME}
        if self.count_entities_as_images:
            counted.add(RefKind.ENTITY)
        return sum(1 for ref in references if ref.kind in counted)

    @staticmethod
    def count_of(references: Sequence[ReferenceItem], kind: RefKind) -> int:
        return sum(1 for ref in references if ref.kind is kind)

    @classmethod
    def from_table(cls, key: str, table: ConfigTable) -> "ModelCapability":
        table.only_keys(_MODEL_KEYS)
        backends: list[BackendKind] = []
        for index, name in enumerate(table.string_list("backends")):
            if name not in {b.value for b in BackendKind}:
                raise ConfigError(f"{table.at('backends')}[{index}]", f"backend 必须是 web | cli，实际 {name!r}")
            backends.append(BackendKind(name))
        for index, ratio in enumerate(table.string_list("ratios")):
            if not RATIO_PATTERN.match(ratio):
                raise ConfigError(f"{table.at('ratios')}[{index}]", f"比例格式必须是 W:H，实际 {ratio!r}")
        return cls(
            key=key,
            backends=frozenset(backends),
            duration_range=cls._duration_range(table),
            resolutions=table.string_list("resolutions"),
            ratios=table.string_list("ratios"),
            max_images=table.integer("max_images", lo=0) if table.has("max_images") else 0,
            max_videos=table.integer("max_videos", lo=0) if table.has("max_videos") else 0,
            max_audios=table.integer("max_audios", lo=0) if table.has("max_audios") else 0,
            entities=table.boolean("entities") if table.has("entities") else False,
            count_entities_as_images=(
                table.boolean("count_entities_as_images") if table.has("count_entities_as_images") else False
            ),
            negative_prompt_field=table.boolean("negative_prompt_field") if table.has("negative_prompt_field") else False,
        )

    @staticmethod
    def _duration_range(table: ConfigTable) -> tuple[int, int] | None:
        if not table.has("duration_s"):
            return None
        value: object = table.data["duration_s"]
        path: str = table.at("duration_s")
        if (
            not isinstance(value, Sequence)
            or isinstance(value, str)
            or len(value) != 2
            or any(isinstance(v, bool) or not isinstance(v, int) for v in value)
        ):
            raise ConfigError(path, "必须是 [最小秒, 最大秒] 两个整数")
        low, high = int(value[0]), int(value[1])
        if low < 1 or low > high:
            raise ConfigError(path, f"必须满足 1 ≤ 最小 ≤ 最大，实际 [{low}, {high}]")
        return (low, high)


@dataclass(frozen=True)
class ModelLimits:
    as_of: str
    models: Mapping[str, ModelCapability]

    def __post_init__(self) -> None:
        object.__setattr__(self, "models", MappingProxyType(dict(self.models)))

    def find(self, model: str) -> ModelCapability | None:
        return self.models.get(model)

    def capability(self, model: str) -> ModelCapability:
        found: ModelCapability | None = self.find(model)
        if found is None:
            raise UnknownModelError(key_path("model_limits.models", model), f"未知模型 {model!r}")
        return found

    def resolutions_for(self, kind: GenerationKind) -> frozenset[str]:
        return frozenset(r for cap in self.models.values() if cap.kind is kind for r in cap.resolutions)

    @classmethod
    def from_table(cls, table: ConfigTable) -> "ModelLimits":
        table.only_keys(("as_of", "models"))
        as_of: str = table.string("as_of", pattern=AS_OF_PATTERN)
        models_table: ConfigTable = table.table("models")
        if not models_table.keys():
            raise ConfigError(models_table.path, "至少要有一个模型")
        models: dict[str, ModelCapability] = {
            key: ModelCapability.from_table(key, models_table.table(key)) for key in models_table.keys()
        }
        return cls(as_of=as_of, models=models)

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "ModelLimits":
        return cls.from_table(ConfigTable.of(data, "model_limits"))
