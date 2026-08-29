from dataclasses import asdict

from libs.common.enums import FieldStatus, VerdictTier
from libs.domain.value_objects.judgment__valueobject import FieldResult
from libs.domain.value_objects.verdict__valueobject import RollupVerdict, UnitVerdict


class VerdictMapper:
    @staticmethod
    def unit_to_dict(verdict: UnitVerdict) -> dict:
        data = asdict(verdict)
        data["tier"] = verdict.tier.value
        data["dimension_scores"] = [asdict(s) for s in verdict.dimension_scores]
        data["findings"] = [
            {**asdict(f), "severity": f.severity.value} for f in verdict.findings
        ]
        return data

    @staticmethod
    def rollup_to_dict(rollup: RollupVerdict) -> dict:
        data = asdict(rollup)
        data["tier"] = rollup.tier.value
        return data

    @staticmethod
    def field_result_to_dict(result: FieldResult) -> dict:
        data = asdict(result)
        data["status"] = result.status.value
        return data

    @staticmethod
    def unit_from_dict(data: dict) -> UnitVerdict:
        from libs.domain.value_objects.verdict__valueobject import (
            DimensionScore,
            Finding,
            SubcategoryScore,
        )
        from libs.common.enums import Severity

        return UnitVerdict(
            unit_id=data["unit_id"],
            tier=VerdictTier(data["tier"]),
            composite=data.get("composite"),
            dimension_scores=tuple(
                DimensionScore(
                    dim_id=s["dim_id"],
                    name_cn=s["name_cn"],
                    composite=s.get("composite"),
                    graded=s["graded"],
                    inconclusive=s["inconclusive"],
                    inapplicable=s["inapplicable"],
                    errors=s["errors"],
                    gate_failures=tuple(s.get("gate_failures", ())),
                    subcategories=tuple(
                        SubcategoryScore(
                            sub_id=sub["sub_id"],
                            name_cn=sub["name_cn"],
                            composite=sub.get("composite"),
                            graded=sub.get("graded", 0),
                            inconclusive=sub.get("inconclusive", 0),
                            inapplicable=sub.get("inapplicable", 0),
                            errors=sub.get("errors", 0),
                            rule_passed=sub.get("rule_passed", 0),
                            rule_failed=tuple(sub.get("rule_failed", ())),
                        )
                        for sub in s.get("subcategories", [])
                    ),
                    rule_passed=s.get("rule_passed", 0),
                    rule_failed=tuple(s.get("rule_failed", ())),
                )
                for s in data.get("dimension_scores", [])
            ),
            findings=tuple(
                Finding(
                    finding_id=f["finding_id"],
                    unit_id=f["unit_id"],
                    dim_id=f["dim_id"],
                    sub_id=f["sub_id"],
                    field_id=f["field_id"],
                    field_name_cn=f["field_name_cn"],
                    grade=f["grade"],
                    severity=Severity(f["severity"]),
                    justification=f["justification"],
                    evidence=tuple(f.get("evidence", ())),
                    revision_hint=f["revision_hint"],
                    locator=f["locator"],
                )
                for f in data.get("findings", [])
            ),
            graded=data.get("graded", 0),
            inconclusive=data.get("inconclusive", 0),
            inapplicable=data.get("inapplicable", 0),
            errors=data.get("errors", 0),
            inconclusive_share=data.get("inconclusive_share", 0.0),
            gate_failures=tuple(data.get("gate_failures", ())),
            carried_forward=bool(data.get("carried_forward", False)),
            rule_total=data.get("rule_total", 0),
            rule_passed=data.get("rule_passed", 0),
            rule_failed_fields=tuple(data.get("rule_failed_fields", ())),
        )

    @staticmethod
    def status_of(result_dict: dict) -> FieldStatus:
        return FieldStatus(result_dict["status"])
