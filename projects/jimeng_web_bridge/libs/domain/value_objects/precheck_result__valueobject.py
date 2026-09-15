from dataclasses import dataclass

from libs.common.enums import CheckSeverity, PrecheckCheck
from libs.domain.errors.precheck__error import InvalidRequestError
from libs.domain.value_objects.price_estimate__valueobject import PriceEstimate

LEGACY_REFERENCE_SYNTAX = "legacy_reference_syntax"


@dataclass(frozen=True)
class PrecheckItem:
    check: PrecheckCheck
    severity: CheckSeverity
    error_code: str
    message: str
    config_key: str | None = None
    reference_name: str | None = None

    def __post_init__(self) -> None:
        if self.error_code == LEGACY_REFERENCE_SYNTAX and self.config_key is not None:
            raise InvalidRequestError("legacy_reference_syntax 不能通过 config 豁免，不带 config_key")

    @property
    def waivable(self) -> bool:
        return self.config_key is not None


@dataclass(frozen=True)
class PrecheckResult:
    items: tuple[PrecheckItem, ...]
    estimate: PriceEstimate
    existing_job_id: str | None = None

    @property
    def severity(self) -> CheckSeverity:
        if any(item.severity is CheckSeverity.ERROR for item in self.items):
            return CheckSeverity.ERROR
        if any(item.severity is CheckSeverity.WARNING for item in self.items):
            return CheckSeverity.WARNING
        return CheckSeverity.OK

    @property
    def errors(self) -> tuple[PrecheckItem, ...]:
        return tuple(item for item in self.items if item.severity is CheckSeverity.ERROR)

    @property
    def warnings(self) -> tuple[PrecheckItem, ...]:
        return tuple(item for item in self.items if item.severity is CheckSeverity.WARNING)

    @property
    def has_errors(self) -> bool:
        return self.severity is CheckSeverity.ERROR
