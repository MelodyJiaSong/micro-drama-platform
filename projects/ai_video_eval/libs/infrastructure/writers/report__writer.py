_TIER_CN = {
    "pass": "通过",
    "conditional_pass": "有条件通过",
    "fail": "不通过",
    "needs_canon_fix": "需先修 canon",
}
_SEV_CN = {"blocker": "阻断", "major": "严重", "minor": "轻微"}


class ReportWriter:
    def render(self, manifest: dict, verdicts: dict, findings: list[dict], usage: dict) -> str:
        lines: list[str] = []
        project_verdict = verdicts["project_verdict"]
        lines.append(f"# 评测报告 — {verdicts['project']}")
        lines.append("")
        lines.append(f"- 运行: `{verdicts['run_id']}` · rubric v{verdicts['rubric_version']}")
        lines.append(
            f"- 项目判定: **{_TIER_CN[project_verdict['tier']]}**"
            f"（综合分 {project_verdict['composite']}，{project_verdict['unit_count']} 镜）"
        )
        tally = "、".join(
            f"{_TIER_CN[t]} {n}" for t, n in sorted(project_verdict["unit_tally"].items())
        )
        lines.append(f"- 镜次分布: {tally}")
        rule_failed = project_verdict.get("rule_failed_units") or []
        if rule_failed:
            lines.append(
                f"- ⛔ 规则层未过（100% 确定性硬契约·一票否决直达项目级）: {', '.join(rule_failed)}"
            )
        gate_failed = [
            u for u in (project_verdict.get("gate_failed_units") or []) if u not in rule_failed
        ]
        if gate_failed:
            lines.append(
                f"- ⛔ 语义层 gate 未过（一票否决直达项目级）: {', '.join(gate_failed)}"
            )
        lines.append(f"- 用量: {usage['calls']} 次 judge 调用 · 成本 ${usage['cost']:.2f}")
        lines.append("")

        lines.append("## 维度综合分（项目级）")
        lines.append("")
        lines.append("| 维度 | 综合分 |")
        lines.append("|---|---|")
        for dim_id, value in project_verdict["dimension_composites"].items():
            lines.append(f"| {dim_id} | {value} |")
        lines.append("")

        if verdicts.get("episode_verdicts"):
            lines.append("## 各集判定")
            lines.append("")
            lines.append("| 集 | 判定 | 综合分 | 镜数 |")
            lines.append("|---|---|---|---|")
            for scope, rollup in verdicts["episode_verdicts"].items():
                lines.append(
                    f"| {scope} | {_TIER_CN[rollup['tier']]} | {rollup['composite']} |"
                    f" {rollup['unit_count']} |"
                )
            lines.append("")

        lines.append("## 逐镜判定")
        lines.append("")
        lines.append("| 镜 | 判定 | 规则层 | 语义综合分 | 阻断/严重/轻微 | 存疑 | 出错 | 备注 |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for unit in verdicts["units"]:
            severities = {"blocker": 0, "major": 0, "minor": 0}
            for finding in unit["findings"]:
                severities[finding["severity"]] += 1
            note = "沿用上次" if unit.get("carried_forward") else ""
            if unit.get("gate_failures"):
                note = (note + " " if note else "") + f"gate: {','.join(unit['gate_failures'])}"
            rule_failed_fields = unit.get("rule_failed_fields") or []
            rule_total = unit.get("rule_total", 0)
            if rule_failed_fields:
                rule_cell = f"✗ {len(rule_failed_fields)}/{rule_total}（{','.join(rule_failed_fields)}）"
            elif rule_total:
                rule_cell = f"✓ {rule_total}/{rule_total}"
            else:
                rule_cell = "—"
            lines.append(
                f"| {unit['unit_id']} | {_TIER_CN[unit['tier']]} | {rule_cell} | {unit['composite']} |"
                f" {severities['blocker']}/{severities['major']}/{severities['minor']} |"
                f" {unit['inconclusive']} | {unit['errors']} | {note} |"
            )
        lines.append("")

        lines.append("## 发现清单（按严重度）")
        lines.append("")
        if not findings:
            lines.append("（无 3 分及以下发现）")
        for finding in findings:
            lines.append(
                f"### [{_SEV_CN[finding['severity']]}] {finding['unit_id']} ·"
                f" {finding['field_name_cn']}（{finding['grade']} 分）"
            )
            lines.append(f"- id: `{finding['finding_id']}` · {finding['dim_id']}/{finding['field_id']}")
            lines.append(f"- 判词: {finding['justification']}")
            for quote in finding["evidence"][:4]:
                lines.append(f"- 证据: 「{quote}」")
            if finding["revision_hint"]:
                lines.append(f"- 修改建议: {finding['revision_hint']}")
            lines.append(f"- 位置: {finding['locator']}")
            lines.append("")
        return "\n".join(lines)
