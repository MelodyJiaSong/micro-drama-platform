import statistics
from dataclasses import dataclass

from libs.common.enums import FieldStatus


@dataclass(frozen=True)
class SampleJudgment:
    grade: int
    confidence: float
    justification: str
    evidence: tuple[str, ...]
    revision_hint: str


@dataclass(frozen=True)
class FieldResult:
    field_id: str
    dim_id: str
    sub_id: str
    status: FieldStatus
    grade: float | None
    confidence: float
    spread: float
    justification: str
    evidence: tuple[str, ...]
    revision_hint: str
    source: str
    error: str | None = None

    @staticmethod
    def reconcile(
        field_id: str, dim_id: str, sub_id: str, samples: list[SampleJudgment], source: str
    ) -> "FieldResult":
        grades = [s.grade for s in samples]
        median_grade = float(statistics.median(grades))
        spread = float(max(grades) - min(grades))
        confidence = min(s.confidence for s in samples)
        if spread >= 2.0:
            confidence *= 0.6
        representative = min(samples, key=lambda s: abs(s.grade - median_grade))
        evidence: list[str] = []
        for sample in samples:
            for quote in sample.evidence:
                if quote not in evidence:
                    evidence.append(quote)
        return FieldResult(
            field_id=field_id,
            dim_id=dim_id,
            sub_id=sub_id,
            status=FieldStatus.GRADED,
            grade=median_grade,
            confidence=round(confidence, 3),
            spread=spread,
            justification=representative.justification,
            evidence=tuple(evidence),
            revision_hint=representative.revision_hint,
            source=source,
        )
