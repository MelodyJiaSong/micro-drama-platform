from collections.abc import Mapping
from dataclasses import dataclass
from decimal import ROUND_CEILING, Decimal
from types import MappingProxyType

from libs.common.enums import GenerationKind
from libs.domain.errors.config__error import ConfigError
from libs.domain.value_objects.config_table__valueobject import ConfigTable
from libs.domain.value_objects.generation_request__valueobject import GenerationRequest
from libs.domain.value_objects.model_limits__valueobject import AS_OF_PATTERN, ModelLimits


@dataclass(frozen=True)
class PriceEstimate:
    credits: int | None
    warning: str | None = None
    config_key: str | None = None

    @property
    def known(self) -> bool:
        return self.credits is not None


@dataclass(frozen=True)
class PriceTable:
    as_of: str
    video_rates: Mapping[tuple[str, str], Decimal]
    image_rates: Mapping[tuple[str, str], Decimal]

    def __post_init__(self) -> None:
        object.__setattr__(self, "video_rates", MappingProxyType(dict(self.video_rates)))
        object.__setattr__(self, "image_rates", MappingProxyType(dict(self.image_rates)))

    def estimate(self, request: GenerationRequest) -> PriceEstimate:
        if request.kind is GenerationKind.ENTITY or request.params is None:
            return PriceEstimate(credits=0)
        params = request.params
        slot: tuple[str, str] = (params.model, params.resolution)
        if request.kind is GenerationKind.VIDEO:
            rate: Decimal | None = self.video_rates.get(slot)
            if rate is None or params.duration_s is None:
                return self._unknown("price_table.video", params.model, params.resolution)
            return PriceEstimate(credits=_ceil(Decimal(params.duration_s) * rate * params.count))
        rate = self.image_rates.get(slot)
        if rate is None:
            return self._unknown("price_table.image", params.model, params.resolution)
        return PriceEstimate(credits=_ceil(rate * params.count))

    @staticmethod
    def _unknown(config_key: str, model: str, resolution: str) -> PriceEstimate:
        return PriceEstimate(
            credits=None,
            warning=f"无法估算：{config_key} 里没有 {model} × {resolution} 的单价",
            config_key=config_key,
        )

    @classmethod
    def from_table(cls, table: ConfigTable, limits: ModelLimits) -> "PriceTable":
        table.only_keys(("as_of", "video", "image"))
        return cls(
            as_of=table.string("as_of", pattern=AS_OF_PATTERN),
            video_rates=_rates(table, "video", "credits_per_second", limits),
            image_rates=_rates(table, "image", "credits_per_image", limits),
        )

    @classmethod
    def from_dict(cls, data: Mapping[str, object], limits: ModelLimits) -> "PriceTable":
        return cls.from_table(ConfigTable.of(data, "price_table"), limits)


def _rates(table: ConfigTable, key: str, rate_key: str, limits: ModelLimits) -> dict[tuple[str, str], Decimal]:
    rates: dict[tuple[str, str], Decimal] = {}
    for row in table.table_list(key):
        row.only_keys(("model", "resolution", rate_key))
        model: str = row.string("model")
        if limits.find(model) is None:
            raise ConfigError(row.at("model"), f"model_limits 里没有模型 {model!r}")
        slot: tuple[str, str] = (model, row.string("resolution"))
        if slot in rates:
            raise ConfigError(row.path, f"重复的单价行 {slot[0]} × {slot[1]}")
        rates[slot] = Decimal(str(row.number(rate_key, lo=0)))
    return rates


def _ceil(value: Decimal) -> int:
    return int(value.to_integral_value(rounding=ROUND_CEILING))
