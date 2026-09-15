from dataclasses import dataclass

from libs.domain.errors.precheck__error import InvalidRequestError


@dataclass(frozen=True)
class GenerationParams:
    model: str
    ratio: str
    resolution: str
    count: int
    duration_s: int | None = None
    reference_mode: str | None = None

    def __post_init__(self) -> None:
        if not self.model:
            raise InvalidRequestError("params.model 不能为空")
        if not self.ratio:
            raise InvalidRequestError("params.ratio 不能为空")
        if not self.resolution:
            raise InvalidRequestError("params.resolution 不能为空")
        if isinstance(self.count, bool) or not isinstance(self.count, int) or self.count < 1:
            raise InvalidRequestError("params.count 必须是 ≥ 1 的整数")
        if self.duration_s is not None and (
            isinstance(self.duration_s, bool) or not isinstance(self.duration_s, int) or self.duration_s < 0
        ):
            raise InvalidRequestError("params.duration_s 必须是非负整数秒")

    def canonical(self) -> dict[str, object]:
        return {
            "model": self.model,
            "ratio": self.ratio,
            "resolution": self.resolution,
            "count": self.count,
            "duration_s": self.duration_s,
            "reference_mode": self.reference_mode,
        }
