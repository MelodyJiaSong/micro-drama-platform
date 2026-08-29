import hashlib
from dataclasses import dataclass

from libs.common.enums import SEVERITY_ORDER, TIER_ORDER, FieldStatus, Severity, VerdictTier
from libs.domain.value_objects.judgment__valueobject import FieldResult
from libs.domain.value_objects.rubric__valueobject import Rubric


def grade_to_composite(grade: float) -> float:
    return round((grade - 1.0) / 4.0 * 100.0, 2)


@dataclass(frozen=True)
class Finding:
    finding_id: str
    unit_id: str
    dim_id: str
    sub_id: str
    field_id: str
    field_name_cn: str
    grade: float
    severity: Severity
    justification: str
    evidence: tuple[str, ...]
    revision_hint: str
    locator: str

    @staticmethod
    def make_id(unit_id: str, field_id: str) -> str:
        return hashlib.sha1(f"{unit_id}|{field_id}".encode("utf-8")).hexdigest()[:10]


@dataclass(frozen=True)
class SubcategoryScore:
    sub_id: str
    name_cn: str
    composite: float | None
    graded: int
    inconclusive: int
    inapplicable: int
    errors: int
    rule_passed: int = 0
    rule_failed: tuple[str, ...] = ()


@dataclass(frozen=True)
class DimensionScore:
    dim_id: str
    name_cn: str
    composite: float | None
    graded: int
    inconclusive: int
    inapplicable: int
    errors: int
    gate_failures: tuple[str, ...]
    subcategories: tuple[SubcategoryScore, ...] = ()
    rule_passed: int = 0
    rule_failed: tuple[str, ...] = ()


@dataclass(frozen=True)
class UnitVerdict:
    unit_id: str
    tier: VerdictTier
    composite: float | None
    dimension_scores: tuple[DimensionScore, ...]
    findings: tuple[Finding, ...]
    graded: int
    inconclusive: int
    inapplicable: int
    errors: int
    inconclusive_share: float
    gate_failures: tuple[str, ...]
    carried_forward: bool = False
    rule_total: int = 0
    rule_passed: int = 0
    rule_failed_fields: tuple[str, ...] = ()


@dataclass(frozen=True)
class RollupVerdict:
    scope_id: str
    tier: VerdictTier
    composite: float | None
    unit_tally: dict[str, int]
    dimension_composites: dict[str, float]
    unit_count: int
    gate_failed_units: tuple[str, ...] = ()
    rule_failed_units: tuple[str, ...] = ()


def _severity_for(grade: float, rubric: Rubric) -> Severity | None:
    cfg = rubric.verdict_config
    if grade <= cfg.severity_blocker_max:
        return Severity.BLOCKER
    if grade <= cfg.severity_major_max:
        return Severity.MAJOR
    if grade <= cfg.severity_minor_max:
        return Severity.MINOR
    return None


def _tier_from_composite(composite: float | None, rubric: Rubric) -> VerdictTier:
    if composite is None:
        return VerdictTier.PASS
    cfg = rubric.verdict_config
    if composite >= cfg.pass_min:
        return VerdictTier.PASS
    if composite >= cfg.conditional_min:
        return VerdictTier.CONDITIONAL_PASS
    return VerdictTier.FAIL


def _is_rule(result: FieldResult) -> bool:
    return result.source == "rule"


def _rule_failed(result: FieldResult) -> bool:
    return (
        _is_rule(result)
        and result.status is FieldStatus.GRADED
        and result.grade is not None
        and result.grade < 5.0
    )


def aggregate_unit(
    rubric: Rubric, unit_id: str, locator: str, results: list[FieldResult]
) -> UnitVerdict:
    """Two-layer aggregation.

    Rule layer (source == "rule"): binary pass/fail hard contracts. Any failure
    fails the unit outright and propagates to every rollup above it. Rule fields
    never contribute to composites.

    Semantic layer (LLM-judged): weighted composites at subcategory, dimension,
    and unit level; tier from thresholds; gates may additionally veto.
    """
    index = rubric.field_index()
    by_dim: dict[str, list[FieldResult]] = {}
    for result in results:
        by_dim.setdefault(result.dim_id, []).append(result)

    dim_scores: list[DimensionScore] = []
    findings: list[Finding] = []
    all_gate_failures: list[str] = []
    all_rule_failed: list[str] = []
    rule_total = 0
    rule_passed = 0
    totals = {"graded": 0, "inconclusive": 0, "inapplicable": 0, "errors": 0}

    for dim in rubric.dimensions:
        dim_results = by_dim.get(dim.dim_id, [])
        weighted_sum = 0.0
        weight_total = 0.0
        counts = {"graded": 0, "inconclusive": 0, "inapplicable": 0, "errors": 0}
        gate_failures: list[str] = []
        dim_rule_passed = 0
        dim_rule_failed: list[str] = []
        sub_acc: dict[str, dict[str, float]] = {}
        sub_counts: dict[str, dict[str, int]] = {}
        sub_rules: dict[str, dict[str, object]] = {}

        for result in dim_results:
            scount = sub_counts.setdefault(
                result.sub_id, {"graded": 0, "inconclusive": 0, "inapplicable": 0, "errors": 0}
            )
            srule = sub_rules.setdefault(result.sub_id, {"passed": 0, "failed": []})
            _, sub, fld = index[result.field_id]

            if _is_rule(result):
                if result.status is FieldStatus.GRADED:
                    rule_total += 1
                    if _rule_failed(result):
                        dim_rule_failed.append(result.field_id)
                        srule["failed"].append(result.field_id)
                        findings.append(
                            Finding(
                                finding_id=Finding.make_id(unit_id, fld.field_id),
                                unit_id=unit_id,
                                dim_id=dim.dim_id,
                                sub_id=sub.sub_id,
                                field_id=fld.field_id,
                                field_name_cn=fld.name_cn,
                                grade=result.grade or 1.0,
                                severity=Severity.BLOCKER,
                                justification=result.justification,
                                evidence=result.evidence,
                                revision_hint=result.revision_hint,
                                locator=locator,
                            )
                        )
                    else:
                        rule_passed += 1
                        dim_rule_passed += 1
                        srule["passed"] = int(srule["passed"]) + 1
                elif result.status is FieldStatus.INCONCLUSIVE:
                    counts["inconclusive"] += 1
                    scount["inconclusive"] += 1
                elif result.status is FieldStatus.JUDGE_ERROR:
                    counts["errors"] += 1
                    scount["errors"] += 1
                continue

            acc = sub_acc.setdefault(result.sub_id, {"sum": 0.0, "weight": 0.0})
            if result.status is FieldStatus.GRADED and result.grade is not None:
                counts["graded"] += 1
                scount["graded"] += 1
                weight = fld.weight * sub.weight
                weighted_sum += grade_to_composite(result.grade) * weight
                weight_total += weight
                acc["sum"] += grade_to_composite(result.grade) * fld.weight
                acc["weight"] += fld.weight
                if fld.gate and result.grade < fld.gate_min_grade:
                    gate_failures.append(fld.field_id)
                severity = _severity_for(result.grade, rubric)
                if severity is not None:
                    findings.append(
                        Finding(
                            finding_id=Finding.make_id(unit_id, fld.field_id),
                            unit_id=unit_id,
                            dim_id=dim.dim_id,
                            sub_id=sub.sub_id,
                            field_id=fld.field_id,
                            field_name_cn=fld.name_cn,
                            grade=result.grade,
                            severity=severity,
                            justification=result.justification,
                            evidence=result.evidence,
                            revision_hint=result.revision_hint,
                            locator=locator,
                        )
                    )
            elif result.status is FieldStatus.INCONCLUSIVE:
                counts["inconclusive"] += 1
                scount["inconclusive"] += 1
            elif result.status is FieldStatus.INAPPLICABLE:
                counts["inapplicable"] += 1
                scount["inapplicable"] += 1
            else:
                counts["errors"] += 1
                scount["errors"] += 1

        sub_scores = tuple(
            SubcategoryScore(
                sub_id=sub.sub_id,
                name_cn=sub.name_cn,
                composite=(
                    round(sub_acc[sub.sub_id]["sum"] / sub_acc[sub.sub_id]["weight"], 2)
                    if sub_acc.get(sub.sub_id, {}).get("weight", 0.0) > 0
                    else None
                ),
                graded=sub_counts.get(sub.sub_id, {}).get("graded", 0),
                inconclusive=sub_counts.get(sub.sub_id, {}).get("inconclusive", 0),
                inapplicable=sub_counts.get(sub.sub_id, {}).get("inapplicable", 0),
                errors=sub_counts.get(sub.sub_id, {}).get("errors", 0),
                rule_passed=int(sub_rules.get(sub.sub_id, {}).get("passed", 0)),
                rule_failed=tuple(sub_rules.get(sub.sub_id, {}).get("failed", [])),
            )
            for sub in dim.subcategories
            if sub.sub_id in sub_counts
        )

        for key in totals:
            totals[key] += counts[key]
        all_gate_failures.extend(gate_failures)
        all_rule_failed.extend(dim_rule_failed)
        dim_scores.append(
            DimensionScore(
                dim_id=dim.dim_id,
                name_cn=dim.name_cn,
                composite=round(weighted_sum / weight_total, 2) if weight_total > 0 else None,
                graded=counts["graded"],
                inconclusive=counts["inconclusive"],
                inapplicable=counts["inapplicable"],
                errors=counts["errors"],
                gate_failures=tuple(gate_failures),
                subcategories=sub_scores,
                rule_passed=dim_rule_passed,
                rule_failed=tuple(dim_rule_failed),
            )
        )

    dim_weighted = [
        (score.composite, rubric.dimension(score.dim_id).weight)
        for score in dim_scores
        if score.composite is not None
    ]
    composite: float | None = None
    if dim_weighted:
        total_weight = sum(weight for _, weight in dim_weighted)
        composite = round(sum(value * weight for value, weight in dim_weighted) / total_weight, 2)

    decided = totals["graded"] + totals["inconclusive"]
    inconclusive_share = totals["inconclusive"] / decided if decided > 0 else 0.0

    if all_rule_failed or all_gate_failures:
        tier = VerdictTier.FAIL
    elif inconclusive_share > rubric.verdict_config.inconclusive_share_max:
        tier = VerdictTier.NEEDS_CANON_FIX
    else:
        tier = _tier_from_composite(composite, rubric)

    findings.sort(key=lambda f: (SEVERITY_ORDER[f.severity], f.grade, f.dim_id, f.field_id))
    return UnitVerdict(
        unit_id=unit_id,
        tier=tier,
        composite=composite,
        dimension_scores=tuple(dim_scores),
        findings=tuple(findings),
        graded=totals["graded"],
        inconclusive=totals["inconclusive"],
        inapplicable=totals["inapplicable"],
        errors=totals["errors"],
        inconclusive_share=round(inconclusive_share, 3),
        gate_failures=tuple(all_gate_failures),
        rule_total=rule_total,
        rule_passed=rule_passed,
        rule_failed_fields=tuple(all_rule_failed),
    )


def aggregate_rollup(rubric: Rubric, scope_id: str, verdicts: list[UnitVerdict]) -> RollupVerdict:
    tally: dict[str, int] = {}
    for verdict in verdicts:
        tally[verdict.tier.value] = tally.get(verdict.tier.value, 0) + 1

    composites = [v.composite for v in verdicts if v.composite is not None]
    composite = round(sum(composites) / len(composites), 2) if composites else None

    dim_values: dict[str, list[float]] = {}
    for verdict in verdicts:
        for score in verdict.dimension_scores:
            if score.composite is not None:
                dim_values.setdefault(score.dim_id, []).append(score.composite)
    dim_composites = {
        dim_id: round(sum(values) / len(values), 2) for dim_id, values in dim_values.items()
    }

    gate_failed_units = tuple(v.unit_id for v in verdicts if v.gate_failures)
    rule_failed_units = tuple(v.unit_id for v in verdicts if v.rule_failed_fields)

    tier = _tier_from_composite(composite, rubric)
    total = len(verdicts)
    fail_count = tally.get(VerdictTier.FAIL.value, 0)
    canon_count = tally.get(VerdictTier.NEEDS_CANON_FIX.value, 0)
    if rule_failed_units or gate_failed_units:
        tier = VerdictTier.FAIL
    elif total > 0:
        if fail_count / total >= rubric.verdict_config.rollup_fail_share_fail:
            tier = VerdictTier.FAIL
        elif fail_count > 0 and TIER_ORDER[tier] < TIER_ORDER[VerdictTier.CONDITIONAL_PASS]:
            tier = VerdictTier.CONDITIONAL_PASS
        if (
            tier is not VerdictTier.FAIL
            and canon_count / total > rubric.verdict_config.inconclusive_share_max
        ):
            tier = VerdictTier.NEEDS_CANON_FIX

    return RollupVerdict(
        scope_id=scope_id,
        tier=tier,
        composite=composite,
        unit_tally=tally,
        dimension_composites=dim_composites,
        unit_count=total,
        gate_failed_units=gate_failed_units,
        rule_failed_units=rule_failed_units,
    )
