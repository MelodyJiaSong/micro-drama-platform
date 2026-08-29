from dataclasses import dataclass, field

from libs.common.enums import EvaluatorKind
from libs.domain.errors.eval__error import RubricError


@dataclass(frozen=True)
class RubricField:
    field_id: str
    name_cn: str
    evaluator: EvaluatorKind
    judge_instruction: str
    weight: float
    anchors: dict[str, str] = field(compare=False)
    rule_id: str | None = None
    rule_params: dict[str, object] = field(default_factory=dict, compare=False)
    applies_when: str | None = None
    gate: bool = False
    gate_min_grade: float = 3.0
    sources: tuple[str, ...] = ()

    def applies(self, variables: dict[str, object]) -> bool:
        if not self.applies_when:
            return True
        try:
            return bool(eval(self.applies_when, {"__builtins__": {}}, dict(variables)))
        except Exception as exc:
            raise RubricError(
                f"applies_when for field '{self.field_id}' failed: {self.applies_when!r}: {exc}"
            ) from exc


@dataclass(frozen=True)
class RubricSubcategory:
    sub_id: str
    name_cn: str
    weight: float
    fields: tuple[RubricField, ...]


@dataclass(frozen=True)
class RubricDimension:
    dim_id: str
    name_cn: str
    description: str
    weight: float
    subcategories: tuple[RubricSubcategory, ...]

    def iter_fields(self) -> list[tuple[RubricSubcategory, RubricField]]:
        return [(sub, fld) for sub in self.subcategories for fld in sub.fields]


@dataclass(frozen=True)
class VerdictConfig:
    pass_min: float
    conditional_min: float
    inconclusive_share_max: float
    severity_blocker_max: float
    severity_major_max: float
    severity_minor_max: float
    rollup_fail_share_fail: float


@dataclass(frozen=True)
class Rubric:
    version: str
    content_hash: str
    dimensions: tuple[RubricDimension, ...]
    verdict_config: VerdictConfig

    def dimension(self, dim_id: str) -> RubricDimension:
        for dim in self.dimensions:
            if dim.dim_id == dim_id:
                return dim
        raise RubricError(f"unknown dimension: {dim_id}")

    def field_index(self) -> dict[str, tuple[RubricDimension, RubricSubcategory, RubricField]]:
        index: dict[str, tuple[RubricDimension, RubricSubcategory, RubricField]] = {}
        for dim in self.dimensions:
            for sub, fld in dim.iter_fields():
                if fld.field_id in index:
                    raise RubricError(f"duplicate field_id across rubric: {fld.field_id}")
                index[fld.field_id] = (dim, sub, fld)
        return index

    def applicable_fields(
        self, dim_id: str, variables: dict[str, object], kind: EvaluatorKind | None = None
    ) -> list[tuple[RubricSubcategory, RubricField]]:
        result = []
        for sub, fld in self.dimension(dim_id).iter_fields():
            if kind is not None and fld.evaluator is not kind:
                continue
            if fld.applies(variables):
                result.append((sub, fld))
        return result
