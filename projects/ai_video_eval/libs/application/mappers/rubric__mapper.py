from libs.common.enums import EvaluatorKind
from libs.domain.errors.eval__error import RubricError
from libs.domain.value_objects.rubric__valueobject import (
    Rubric,
    RubricDimension,
    RubricField,
    RubricSubcategory,
    VerdictConfig,
)
from libs.domain.value_objects.rule_check__valueobject import known_rule_ids

_DUMMY_VARS: dict[str, object] = {
    "sub_type": "novel",
    "has_dialogue": True,
    "dialogue_types": {"对白"},
    "seam_mode": "硬切",
    "has_combat": False,
    "has_vfx": False,
    "is_first_shot": False,
    "is_last_shot": False,
    "has_prev_shot": True,
    "has_next_shot": True,
}


class RubricMapper:
    def map(self, top: dict, dims: list[dict], content_hash: str) -> Rubric:
        weights = top.get("dimension_weights", {})
        verdict_raw = top.get("verdict", {})
        severity = verdict_raw.get("severity", {})
        config = VerdictConfig(
            pass_min=float(verdict_raw.get("pass_min", 75)),
            conditional_min=float(verdict_raw.get("conditional_min", 60)),
            inconclusive_share_max=float(verdict_raw.get("inconclusive_share_max", 0.25)),
            severity_blocker_max=float(severity.get("blocker_max", 1)),
            severity_major_max=float(severity.get("major_max", 2)),
            severity_minor_max=float(severity.get("minor_max", 3)),
            rollup_fail_share_fail=float(verdict_raw.get("rollup_fail_share_fail", 0.2)),
        )
        dimensions = tuple(
            self._map_dimension(raw, float(weights.get(raw["dimension_id"], 1.0)))
            for raw in dims
        )
        rubric = Rubric(
            version=str(top.get("version", "0.0.0")),
            content_hash=content_hash,
            dimensions=dimensions,
            verdict_config=config,
        )
        self._validate(rubric)
        return rubric

    def _map_dimension(self, raw: dict, weight: float) -> RubricDimension:
        subs = tuple(self._map_subcategory(sub) for sub in raw.get("subcategories", []))
        if not subs:
            raise RubricError(f"dimension {raw.get('dimension_id')} has no subcategories")
        return RubricDimension(
            dim_id=str(raw["dimension_id"]),
            name_cn=str(raw["name_cn"]),
            description=str(raw.get("description_cn", "")),
            weight=weight,
            subcategories=subs,
        )

    def _map_subcategory(self, raw: dict) -> RubricSubcategory:
        fields = tuple(self._map_field(fld) for fld in raw.get("fields", []))
        if not fields:
            raise RubricError(f"subcategory {raw.get('id')} has no fields")
        return RubricSubcategory(
            sub_id=str(raw["id"]),
            name_cn=str(raw["name_cn"]),
            weight=float(raw.get("weight", 1.0)),
            fields=fields,
        )

    @staticmethod
    def _map_field(raw: dict) -> RubricField:
        evaluator = EvaluatorKind(raw["evaluator"])
        anchors = {str(k): str(v) for k, v in raw.get("anchors", {}).items()}
        for key in ("g1", "g3", "g5"):
            if key not in anchors:
                raise RubricError(f"field {raw.get('id')} missing anchor {key}")
        return RubricField(
            field_id=str(raw["id"]),
            name_cn=str(raw["name_cn"]),
            evaluator=evaluator,
            judge_instruction=str(raw.get("judge_instruction_cn", "")),
            weight=float(raw.get("weight", 3.0)),
            anchors=anchors,
            rule_id=raw.get("rule_id"),
            rule_params=raw.get("rule_params") or {},
            applies_when=raw.get("applies_when"),
            gate=bool(raw.get("gate", False)),
            gate_min_grade=float(raw.get("gate_min_grade", 3.0)),
            sources=tuple(str(s) for s in raw.get("sources", [])),
        )

    @staticmethod
    def _validate(rubric: Rubric) -> None:
        rubric.field_index()
        rules = known_rule_ids()
        for dim in rubric.dimensions:
            for _, fld in dim.iter_fields():
                if fld.evaluator is EvaluatorKind.RULE and fld.rule_id not in rules:
                    raise RubricError(f"field {fld.field_id}: unknown rule_id {fld.rule_id!r}")
                if fld.evaluator is EvaluatorKind.LLM and not fld.judge_instruction:
                    raise RubricError(f"field {fld.field_id}: llm field missing judge_instruction")
                fld.applies(_DUMMY_VARS)
