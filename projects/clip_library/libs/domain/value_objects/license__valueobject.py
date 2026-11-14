from dataclasses import dataclass

from libs.common.options import (CC_MARKER, EVIDENCE_REQUIRED, LICENSE_LABELS, QUOTE_MAX_SECONDS,
                                 LicenseKind)
from libs.domain.errors.license__error import LicenseEvidenceMissingError, LicenseMismatchError


@dataclass(frozen=True)
class License:
    kind: LicenseKind
    note: str = ""

    def __post_init__(self) -> None:
        if self.kind in EVIDENCE_REQUIRED and not self.note.strip():
            raise LicenseEvidenceMissingError(self.kind)

    @classmethod
    def resolve(cls, claimed: LicenseKind | None, platform_license: str, note: str) -> "License":
        platform_cc = CC_MARKER in platform_license
        if claimed is None:
            return cls(LicenseKind.CC_BY, platform_license) if platform_cc else cls(LicenseKind.QUOTE, note)
        if claimed == LicenseKind.CC_BY:
            if not platform_cc:
                raise LicenseMismatchError()
            return cls(claimed, note or platform_license)
        return cls(claimed, note)

    @property
    def label(self) -> str:
        return LICENSE_LABELS[self.kind]

    @property
    def max_clip_seconds(self) -> float | None:
        return QUOTE_MAX_SECONDS if self.kind == LicenseKind.QUOTE else None
