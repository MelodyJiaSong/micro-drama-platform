from libs.common.enums import EvaluatorKind, FieldStatus, VerdictTier
from libs.domain.value_objects.judgment__valueobject import FieldResult, SampleJudgment
from libs.domain.value_objects.rubric__valueobject import (
    Rubric,
    RubricDimension,
    RubricField,
    RubricSubcategory,
    VerdictConfig,
)
from libs.domain.value_objects.verdict__valueobject import aggregate_rollup, aggregate_unit


def _field(fid: str, weight: float = 1.0, gate: bool = False) -> RubricField:
    return RubricField(
        field_id=fid, name_cn=fid, evaluator=EvaluatorKind.LLM, judge_instruction="x",
        weight=weight, anchors={"g1": "", "g3": "", "g5": ""}, gate=gate, gate_min_grade=3.0,
    )


def _rubric() -> Rubric:
    dim_a = RubricDimension(
        dim_id="a", name_cn="A", description="", weight=2.0,
        subcategories=(
            RubricSubcategory("a1", "A1", 1.0, (_field("f1", 2.0), _field("f2", 1.0, gate=True))),
        ),
    )
    dim_b = RubricDimension(
        dim_id="b", name_cn="B", description="", weight=1.0,
        subcategories=(RubricSubcategory("b1", "B1", 1.0, (_field("f3"), _field("f4"))),),
    )
    return Rubric(
        version="t", content_hash="h", dimensions=(dim_a, dim_b),
        verdict_config=VerdictConfig(
            pass_min=75.0, conditional_min=60.0, inconclusive_share_max=0.25,
            severity_blocker_max=1.0, severity_major_max=2.0, severity_minor_max=3.0,
            rollup_fail_share_fail=0.5,
        ),
    )


def _graded(fid: str, dim: str, sub: str, grade: float) -> FieldResult:
    return FieldResult(
        field_id=fid, dim_id=dim, sub_id=sub, status=FieldStatus.GRADED, grade=grade,
        confidence=1.0, spread=0.0, justification="j", evidence=("e",), revision_hint="r",
        source="llm",
    )


def _status(fid: str, dim: str, sub: str, status: FieldStatus) -> FieldResult:
    return FieldResult(
        field_id=fid, dim_id=dim, sub_id=sub, status=status, grade=None, confidence=0.0,
        spread=0.0, justification="", evidence=(), revision_hint="", source="llm",
    )


def test_composite_weighting_and_findings():
    rubric = _rubric()
    results = [
        _graded("f1", "a", "a1", 5.0),
        _graded("f2", "a", "a1", 3.0),
        _graded("f3", "b", "b1", 2.0),
        _graded("f4", "b", "b1", 4.0),
    ]
    verdict = aggregate_unit(rubric, "u1", "loc", results)
    dim_a = verdict.dimension_scores[0]
    assert dim_a.composite == round((100 * 2 + 50 * 1) / 3, 2)
    assert len(dim_a.subcategories) == 1
    sub_a1 = dim_a.subcategories[0]
    assert sub_a1.sub_id == "a1"
    assert sub_a1.composite == dim_a.composite
    assert sub_a1.graded == 2
    dim_b = verdict.dimension_scores[1]
    assert dim_b.composite == 50.0
    expected = round((dim_a.composite * 2 + 50.0 * 1) / 3, 2)
    assert verdict.composite == expected
    assert {f.field_id for f in verdict.findings} == {"f2", "f3"}
    severities = {f.field_id: f.severity.value for f in verdict.findings}
    assert severities == {"f2": "minor", "f3": "major"}


def test_gate_forces_fail():
    rubric = _rubric()
    results = [
        _graded("f1", "a", "a1", 5.0),
        _graded("f2", "a", "a1", 2.0),
        _graded("f3", "b", "b1", 5.0),
        _graded("f4", "b", "b1", 5.0),
    ]
    verdict = aggregate_unit(rubric, "u1", "loc", results)
    assert verdict.gate_failures == ("f2",)
    assert verdict.tier is VerdictTier.FAIL


def test_inconclusive_share_triggers_canon_fix():
    rubric = _rubric()
    results = [
        _graded("f1", "a", "a1", 5.0),
        _status("f2", "a", "a1", FieldStatus.INCONCLUSIVE),
        _status("f3", "b", "b1", FieldStatus.INCONCLUSIVE),
        _graded("f4", "b", "b1", 5.0),
    ]
    verdict = aggregate_unit(rubric, "u1", "loc", results)
    assert verdict.inconclusive_share == 0.5
    assert verdict.tier is VerdictTier.NEEDS_CANON_FIX


def test_inapplicable_excluded():
    rubric = _rubric()
    results = [
        _graded("f1", "a", "a1", 5.0),
        _status("f2", "a", "a1", FieldStatus.INAPPLICABLE),
        _graded("f3", "b", "b1", 5.0),
        _graded("f4", "b", "b1", 5.0),
    ]
    verdict = aggregate_unit(rubric, "u1", "loc", results)
    assert verdict.tier is VerdictTier.PASS
    assert verdict.composite == 100.0


def test_rollup_caps():
    rubric = _rubric()
    good = aggregate_unit(rubric, "u_good", "loc", [
        _graded("f1", "a", "a1", 5.0), _graded("f2", "a", "a1", 5.0),
        _graded("f3", "b", "b1", 5.0), _graded("f4", "b", "b1", 5.0),
    ])
    soft_fail = aggregate_unit(rubric, "u_soft", "loc", [
        _graded("f1", "a", "a1", 2.0), _graded("f2", "a", "a1", 3.0),
        _graded("f3", "b", "b1", 1.0), _graded("f4", "b", "b1", 2.0),
    ])
    assert soft_fail.tier is VerdictTier.FAIL
    assert soft_fail.gate_failures == ()
    rollup = aggregate_rollup(rubric, "proj", [good, good, good, soft_fail])
    assert rollup.tier is VerdictTier.CONDITIONAL_PASS
    rollup_bad = aggregate_rollup(rubric, "proj", [good, soft_fail, soft_fail])
    assert rollup_bad.tier is VerdictTier.FAIL


def test_gate_failure_propagates_to_top():
    rubric = _rubric()
    good = aggregate_unit(rubric, "u_good", "loc", [
        _graded("f1", "a", "a1", 5.0), _graded("f2", "a", "a1", 5.0),
        _graded("f3", "b", "b1", 5.0), _graded("f4", "b", "b1", 5.0),
    ])
    gated = aggregate_unit(rubric, "u_gated", "loc", [
        _graded("f1", "a", "a1", 5.0), _graded("f2", "a", "a1", 1.0),
        _graded("f3", "b", "b1", 5.0), _graded("f4", "b", "b1", 5.0),
    ])
    assert gated.tier is VerdictTier.FAIL
    assert gated.gate_failures == ("f2",)
    rollup = aggregate_rollup(rubric, "proj", [good] * 14 + [gated])
    assert rollup.tier is VerdictTier.FAIL
    assert rollup.gate_failed_units == ("u_gated",)


def test_rule_layer_binary_and_fatal():
    rubric = _rubric()

    def _rule(fid: str, dim: str, sub: str, passed: bool) -> FieldResult:
        return FieldResult(
            field_id=fid, dim_id=dim, sub_id=sub, status=FieldStatus.GRADED,
            grade=5.0 if passed else 1.0, confidence=1.0, spread=0.0,
            justification="规则", evidence=("e",), revision_hint="", source="rule",
        )

    verdict = aggregate_unit(rubric, "u1", "loc", [
        _rule("f1", "a", "a1", True),
        _rule("f2", "a", "a1", False),
        _graded("f3", "b", "b1", 5.0),
        _graded("f4", "b", "b1", 5.0),
    ])
    assert verdict.tier is VerdictTier.FAIL
    assert verdict.rule_total == 2
    assert verdict.rule_passed == 1
    assert verdict.rule_failed_fields == ("f2",)
    assert verdict.composite == 100.0
    assert verdict.graded == 2
    blockers = [f for f in verdict.findings if f.severity.value == "blocker"]
    assert [f.field_id for f in blockers] == ["f2"]
    dim_a = verdict.dimension_scores[0]
    assert dim_a.composite is None
    assert dim_a.rule_failed == ("f2",)
    assert dim_a.subcategories[0].rule_failed == ("f2",)

    good = aggregate_unit(rubric, "u_good", "loc", [
        _rule("f1", "a", "a1", True), _rule("f2", "a", "a1", True),
        _graded("f3", "b", "b1", 5.0), _graded("f4", "b", "b1", 5.0),
    ])
    rollup = aggregate_rollup(rubric, "proj", [good] * 20 + [verdict])
    assert rollup.tier is VerdictTier.FAIL
    assert rollup.rule_failed_units == ("u1",)


def test_reconcile_median_and_spread():
    samples = [
        SampleJudgment(4, 0.9, "a", ("q1",), "h1"),
        SampleJudgment(2, 0.8, "b", ("q2",), "h2"),
        SampleJudgment(4, 0.7, "c", ("q1",), "h3"),
    ]
    result = FieldResult.reconcile("f", "d", "s", samples, "llm")
    assert result.grade == 4.0
    assert result.spread == 2.0
    assert result.confidence == round(0.7 * 0.6, 3)
    assert result.evidence == ("q1", "q2")
    assert result.justification == "a"
