import argparse
import asyncio
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from dotenv import load_dotenv

from apps.cli.container import PROJECT_ROOT, Container
from libs.application.dtos.eval__dto import SelectorCdto


def _selector(args: argparse.Namespace) -> SelectorCdto:
    eps = tuple(f"ep{int(e):02d}" if str(e).isdigit() else str(e) for e in (args.ep or []))
    return SelectorCdto(
        project=args.project,
        eps=eps,
        shots=tuple(args.shot or []),
        dimensions=tuple(args.dimension or []),
        dry_run=getattr(args, "dry_run", False),
        budget_usd=getattr(args, "budget", None),
        samples_override=getattr(args, "samples", None),
        assume_yes=getattr(args, "yes", False),
    )


def _print_estimate(estimate) -> None:
    print(f"项目: {estimate.project}")
    print(f"评测镜数: {estimate.unit_count}")
    print(f"LLM 调用数(样本已计): {estimate.llm_call_count}")
    print(f"预计输入 tokens: {estimate.est_input_tokens:,}")
    print(f"预计输出 tokens: {estimate.est_output_tokens:,}")
    print(
        f"预计成本: ${estimate.est_cost_cached_usd:.2f}（按提示缓存生效估算；"
        f"无缓存上限 ${estimate.est_cost_usd:.2f}）/ 预算 ${estimate.budget_usd:.2f}"
    )


def cmd_estimate(container: Container, args: argparse.Namespace) -> int:
    _print_estimate(container.eval_run_command().estimate(_selector(args)))
    return 0


def cmd_run(container: Container, args: argparse.Namespace) -> int:
    command = container.eval_run_command()
    selector = _selector(args)
    estimate = command.estimate(selector)
    _print_estimate(estimate)
    if not selector.dry_run and estimate.est_cost_cached_usd > estimate.budget_usd and not selector.assume_yes:
        print("预计成本超出预算；用 --budget 提高预算或 --yes 强制继续。", file=sys.stderr)
        return 2
    result = asyncio.run(command.run(selector))
    print()
    print(f"运行: {result.run_id}  ->  {result.run_dir}")
    print(f"项目判定: {result.project_tier}  综合分: {result.project_composite}")
    print(f"镜数: {result.unit_count}  发现: {result.findings_total}（阻断 {result.findings_blocker}）")
    print(f"用量: {result.usage.api_calls} 次评审调用, 成本 ${result.usage.cost_usd:.2f}")
    if result.halted_reason:
        print(f"注意: 运行中断 — {result.halted_reason}", file=sys.stderr)
    print(f"报告: {result.report_path}")
    return 0 if result.halted_reason is None else 3


def cmd_report(container: Container, args: argparse.Namespace) -> int:
    query = container.report_query()
    text = query.report_for(args.run) if args.run else query.latest_report(args.project)
    print(text)
    return 0


def cmd_trends(container: Container, args: argparse.Namespace) -> int:
    trends = container.trends_query().compute(args.project)
    print(f"# 趋势 — {trends.project}\n")
    for run in trends.runs:
        print(f"{run['ts']}  {run['run_id']}: {run['tier']} {run['composite']} ({run['unit_count']} 镜)")
    print("\n高频失分字段（最近一次运行）:")
    for entry in trends.recurring_fields:
        print(
            f"  {entry['dim_id']}/{entry['field_id']} {entry['field_name_cn']}: "
            f"{entry['count']} 次（阻断 {entry['blockers']}）"
        )
    return 0


def cmd_dispute(container: Container, args: argparse.Namespace) -> int:
    path = container.dispute_command().record(args.project, args.finding, args.because, args.run)
    print(f"已记录争议并写入 golden set: {path}")
    return 0


def cmd_rubric(container: Container, args: argparse.Namespace) -> int:
    rubric = container.rubric()
    fields = rubric.field_index()
    rule_count = sum(1 for _, _, f in fields.values() if f.evaluator.value == "rule")
    print(f"rubric v{rubric.version}  hash {rubric.content_hash[:12]}")
    print(f"维度 {len(rubric.dimensions)} · 字段 {len(fields)}（rule {rule_count} / llm {len(fields) - rule_count}）")
    if args.json:
        doc = {
            dim.dim_id: {
                "name": dim.name_cn,
                "weight": dim.weight,
                "fields": [f.field_id for _, f in dim.iter_fields()],
            }
            for dim in rubric.dimensions
        }
        print(json.dumps(doc, ensure_ascii=False, indent=1))
    print("校验通过。")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="eval", description="AI-video shot-prompt eval system")
    sub = parser.add_subparsers(dest="cmd", required=True)

    def add_selector(p: argparse.ArgumentParser, run_flags: bool) -> None:
        p.add_argument("--project", required=True)
        p.add_argument("--ep", action="append", help="episode number or epNN (repeatable)")
        p.add_argument("--shot", action="append", help="shotNN (repeatable)")
        p.add_argument("--dimension", action="append", help="dimension id filter (repeatable)")
        if run_flags:
            p.add_argument("--dry-run", action="store_true", help="rule fields only, no LLM calls")
            p.add_argument("--budget", type=float, help="budget in USD for this run")
            p.add_argument("--samples", type=int, help="override samples per judge call")
            p.add_argument("--yes", action="store_true", help="proceed even if estimate exceeds budget")

    p_run = sub.add_parser("run", help="evaluate shots and produce verdicts + report")
    add_selector(p_run, run_flags=True)
    p_run.set_defaults(fn=cmd_run)

    p_est = sub.add_parser("estimate", help="estimate cost without calling the API")
    add_selector(p_est, run_flags=True)
    p_est.set_defaults(fn=cmd_estimate)

    p_rep = sub.add_parser("report", help="print a run's report")
    p_rep.add_argument("--project")
    p_rep.add_argument("--run")
    p_rep.set_defaults(fn=cmd_report)

    p_tr = sub.add_parser("trends", help="cross-run trends for a project")
    p_tr.add_argument("--project", required=True)
    p_tr.set_defaults(fn=cmd_trends)

    p_dis = sub.add_parser("dispute", help="dispute a finding; accumulates the golden set")
    p_dis.add_argument("--project", required=True)
    p_dis.add_argument("--finding", required=True)
    p_dis.add_argument("--because", required=True)
    p_dis.add_argument("--run")
    p_dis.set_defaults(fn=cmd_dispute)

    p_rub = sub.add_parser("rubric", help="rubric operations")
    rub_sub = p_rub.add_subparsers(dest="rubric_cmd", required=True)
    p_val = rub_sub.add_parser("validate", help="load + validate the rubric")
    p_val.add_argument("--json", action="store_true")
    p_val.set_defaults(fn=cmd_rubric)

    return parser


def main(argv: list[str] | None = None) -> int:
    load_dotenv(os.path.join(PROJECT_ROOT, ".env"))
    args = build_parser().parse_args(argv)
    container = Container()
    try:
        return args.fn(container, args)
    except Exception as exc:
        print(f"错误: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
