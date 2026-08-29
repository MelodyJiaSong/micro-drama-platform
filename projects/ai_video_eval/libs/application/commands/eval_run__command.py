import asyncio
import math
import re
from datetime import datetime, timezone

from libs.common.enums import EvaluatorKind, FieldStatus, SubType
from libs.domain.value_objects.grounding__valueobject import GroundingBundle
from libs.domain.value_objects.judgment__valueobject import FieldResult, SampleJudgment
from libs.domain.value_objects.rubric__valueobject import Rubric
from libs.domain.value_objects.rule_check__valueobject import evaluate_rule
from libs.domain.value_objects.shot__valueobject import ShotUnit
from libs.domain.value_objects.verdict__valueobject import aggregate_rollup, aggregate_unit
from libs.application.dtos.eval__dto import EstimateQdto, RunResultCdto, SelectorCdto, UsageCdto
from libs.application.mappers.grounding__mapper import GroundingMapper
from libs.application.mappers.judge__mapper import JudgeMapper
from libs.application.mappers.shot__mapper import ShotMapper
from libs.application.mappers.verdict__mapper import VerdictMapper
from libs.infrastructure.clients.anthropic__client import AnthropicClient
from libs.infrastructure.daos.config__dao import EvalConfigDao
from libs.infrastructure.errors.judge__error import JudgeError, JudgeSchemaError
from libs.infrastructure.readers.canon__reader import CanonReader
from libs.infrastructure.readers.layout__reader import LayoutReader, ProjectLayout
from libs.infrastructure.readers.run__reader import RunReader
from libs.infrastructure.readers.script__reader import ScriptReader
from libs.infrastructure.readers.shot__reader import ShotReader
from libs.infrastructure.writers.report__writer import ReportWriter
from libs.infrastructure.writers.run__writer import RunWriter

_CHARS_PER_TOKEN = 0.9
_EST_OUTPUT_TOKENS_PER_FIELD = 260


class _BudgetExhausted(Exception):
    pass


class EvalRunCommand:
    def __init__(
        self,
        config: EvalConfigDao,
        rubric: Rubric,
        layout_reader: LayoutReader,
        shot_reader: ShotReader,
        canon_reader: CanonReader,
        script_reader: ScriptReader,
        run_reader: RunReader,
        run_writer: RunWriter,
        report_writer: ReportWriter,
        client: AnthropicClient,
        shot_mapper: ShotMapper,
        grounding_mapper: GroundingMapper,
        judge_mapper: JudgeMapper,
        verdict_mapper: VerdictMapper,
    ) -> None:
        self._config = config
        self._rubric = rubric
        self._layout_reader = layout_reader
        self._shot_reader = shot_reader
        self._canon_reader = canon_reader
        self._script_reader = script_reader
        self._run_reader = run_reader
        self._run_writer = run_writer
        self._report_writer = report_writer
        self._client = client
        self._shot_mapper = shot_mapper
        self._grounding_mapper = grounding_mapper
        self._judge_mapper = judge_mapper
        self._verdict_mapper = verdict_mapper

    # ---------- unit collection ----------

    def _collect_units(self, selector: SelectorCdto) -> tuple[ProjectLayout, dict[str, list[ShotUnit]]]:
        layout = self._layout_reader.detect(selector.project)
        if layout.sub_type is SubType.NOVEL:
            eps = list(selector.eps) if selector.eps else list(layout.episodes)
        else:
            eps = [None]
        by_scope: dict[str, list[ShotUnit]] = {}
        for ep in eps:
            paths = self._layout_reader.shot_paths(layout, ep)
            units: list[ShotUnit] = []
            for index, path in enumerate(paths):
                shot_id = re.search(r"(shot\d+)\.md$", path).group(1)
                dao = self._shot_reader.read(path)
                units.append(
                    self._shot_mapper.map(
                        dao, selector.project, layout.sub_type, ep, shot_id, index, len(paths)
                    )
                )
            if selector.shots:
                units = [u for u in units if u.shot_id in selector.shots]
            by_scope[ep or "flat"] = units
        return layout, by_scope

    def _grounding_for(
        self, layout: ProjectLayout, scope: str, units: list[ShotUnit], index: int
    ) -> GroundingBundle:
        unit = units[index]
        ep = None if scope == "flat" else scope
        canon = self._canon_reader.read(layout.canon_dir)
        script_path, dialogue_path = self._layout_reader.script_paths(layout, ep)
        prior_script = ""
        if ep is not None:
            ep_num = int(re.sub(r"\D", "", ep) or 0)
            if ep_num > 1:
                prev_ep = f"ep{ep_num - 1:02d}"
                prev_script_path, _ = self._layout_reader.script_paths(layout, prev_ep)
                prior_script = self._script_reader.read(prev_script_path)
        structure_text = ""
        if layout.sub_type is SubType.SHORT:
            structure_text = self._script_reader.read(self._layout_reader.structure_path(layout))
        return self._grounding_mapper.build(
            shot=unit,
            canon=canon,
            script_text=self._script_reader.read(script_path),
            dialogue_text=self._script_reader.read(dialogue_path),
            prev_shot=units[index - 1] if index > 0 else None,
            next_shot=units[index + 1] if index < len(units) - 1 else None,
            prior_ep_script=prior_script,
            structure_text=structure_text,
        )

    # ---------- estimate ----------

    def estimate(self, selector: SelectorCdto) -> EstimateQdto:
        _, by_scope = self._collect_units(selector)
        units = [u for scope_units in by_scope.values() for u in scope_units]
        call_count = 0
        input_tokens = 0
        output_tokens = 0
        cost = 0.0
        cost_cached = 0.0
        for unit in units:
            variables = unit.applicability_vars()
            shared_tokens = int((len(unit.raw_text) + 24000) / _CHARS_PER_TOKEN)
            unit_calls = 0
            unit_shared_read_cost = 0.0
            first_price: float | None = None
            for dim in self._rubric.dimensions:
                if selector.dimensions and dim.dim_id not in selector.dimensions:
                    continue
                fields = self._rubric.applicable_fields(dim.dim_id, variables, EvaluatorKind.LLM)
                if not fields:
                    continue
                model_config = self._config.judge_for(dim.dim_id)
                samples = selector.samples_override or model_config.samples
                unique_input = int(len(fields) * 700 / _CHARS_PER_TOKEN)
                call_output = len(fields) * _EST_OUTPUT_TOKENS_PER_FIELD
                pricing = self._config.pricing.get(model_config.model, {})
                in_price = pricing.get("input_per_mtok", 5.0)
                out_price = pricing.get("output_per_mtok", 25.0)
                if first_price is None:
                    first_price = in_price
                for _ in range(samples):
                    call_count += 1
                    unit_calls += 1
                    input_tokens += shared_tokens + unique_input
                    output_tokens += call_output
                    cost += (shared_tokens + unique_input) / 1e6 * in_price + call_output / 1e6 * out_price
                    cost_cached += unique_input / 1e6 * in_price + call_output / 1e6 * out_price
                    unit_shared_read_cost += shared_tokens / 1e6 * in_price * 0.1
            if unit_calls > 0 and first_price is not None:
                write_cost = shared_tokens / 1e6 * first_price * 1.25
                first_read = shared_tokens / 1e6 * first_price * 0.1
                cost_cached += write_cost + unit_shared_read_cost - first_read
        return EstimateQdto(
            project=selector.project,
            unit_count=len(units),
            llm_call_count=call_count,
            est_input_tokens=input_tokens,
            est_output_tokens=output_tokens,
            est_cost_usd=round(cost, 2),
            est_cost_cached_usd=round(cost_cached, 2),
            budget_usd=selector.budget_usd or self._config.budget_default_usd,
        )

    # ---------- run ----------

    async def run(self, selector: SelectorCdto) -> RunResultCdto:
        layout, by_scope = self._collect_units(selector)
        run_id = f"{datetime.now():%Y%m%d-%H%M%S}-{selector.project}"
        budget = selector.budget_usd or self._config.budget_default_usd

        usage = {"input": 0, "output": 0, "cache_read": 0, "cache_write": 0,
                 "cost": 0.0, "calls": 0}
        usage_lock = asyncio.Lock()
        semaphore = asyncio.Semaphore(self._config.concurrency)
        halted: list[str] = []

        manifest = {
            "run_id": run_id,
            "ts": datetime.now(timezone.utc).isoformat(),
            "project": selector.project,
            "sub_type": layout.sub_type.value,
            "selector": {
                "eps": list(selector.eps), "shots": list(selector.shots),
                "dimensions": list(selector.dimensions),
                "dry_run": selector.dry_run,
            },
            "rubric_version": self._rubric.version,
            "rubric_hash": self._rubric.content_hash,
            "aggregation": 2,
            "judge_models": {
                dim.dim_id: self._config.judge_for(dim.dim_id).model
                for dim in self._rubric.dimensions
            },
            "unit_hashes": {},
            "status": "running",
        }
        self._run_writer.init_run(run_id, manifest)

        scope_map: dict[str, list[str]] = {}

        for scope, units in by_scope.items():
            scope_map[scope] = [u.unit_id for u in units]
            for u in units:
                manifest["unit_hashes"][u.unit_id] = u.unit_hash

        field_index = self._rubric.field_index()

        async def evaluate_and_record(unit: ShotUnit, grounding: GroundingBundle):
            results = await self._evaluate_unit(
                run_id, unit, grounding, selector, budget, usage, usage_lock, semaphore, halted
            )
            verdict = aggregate_unit(self._rubric, unit.unit_id, unit.path, results)
            field_meta = {
                r.field_id: {
                    "name_cn": field_index[r.field_id][2].name_cn,
                    "dim_id": field_index[r.field_id][0].dim_id,
                    "dim_name": field_index[r.field_id][0].name_cn,
                    "sub_id": field_index[r.field_id][1].sub_id,
                    "sub_name": field_index[r.field_id][1].name_cn,
                    "weight": field_index[r.field_id][2].weight,
                    "gate": field_index[r.field_id][2].gate,
                    "evaluator": field_index[r.field_id][2].evaluator.value,
                }
                for r in results
                if r.field_id in field_index
            }
            self._run_writer.write_unit_results(
                run_id,
                unit.unit_id,
                {
                    "unit_id": unit.unit_id,
                    "unit_hash": unit.unit_hash,
                    "fields": [self._verdict_mapper.field_result_to_dict(r) for r in results],
                    "field_meta": field_meta,
                    "verdict": self._verdict_mapper.unit_to_dict(verdict),
                },
            )
            return unit.unit_id, verdict

        unit_jobs = [
            (unit, self._grounding_for(layout, scope, units, index))
            for scope, units in by_scope.items()
            for index, unit in enumerate(units)
        ]
        pairs = await asyncio.gather(
            *(evaluate_and_record(unit, grounding) for unit, grounding in unit_jobs)
        )
        verdict_by_id = dict(pairs)
        unit_verdicts = [
            verdict_by_id[unit_id]
            for unit_ids in scope_map.values()
            for unit_id in unit_ids
            if unit_id in verdict_by_id
        ]

        ep_rollups = {
            scope: aggregate_rollup(
                self._rubric, f"{selector.project}/{scope}",
                [v for v in unit_verdicts if v.unit_id in set(unit_ids)],
            )
            for scope, unit_ids in scope_map.items()
        }
        project_rollup = aggregate_rollup(self._rubric, selector.project, unit_verdicts)

        verdicts_doc = {
            "run_id": run_id,
            "project": selector.project,
            "rubric_version": self._rubric.version,
            "project_verdict": self._verdict_mapper.rollup_to_dict(project_rollup),
            "episode_verdicts": {
                scope: self._verdict_mapper.rollup_to_dict(rollup)
                for scope, rollup in ep_rollups.items()
            },
            "units": [self._verdict_mapper.unit_to_dict(v) for v in unit_verdicts],
        }
        findings_doc = [
            {**f, "unit_tier": unit["tier"]}
            for unit in verdicts_doc["units"]
            for f in unit["findings"]
        ]
        findings_doc.sort(key=lambda f: ({"blocker": 0, "major": 1, "minor": 2}[f["severity"]], f["grade"]))

        self._run_writer.write_verdicts(run_id, verdicts_doc)
        self._run_writer.write_findings(run_id, findings_doc)
        report_text = self._report_writer.render(manifest, verdicts_doc, findings_doc, usage)
        report_path = self._run_writer.write_report(run_id, report_text)

        manifest["status"] = "halted" if halted else "completed"
        manifest["halted_reason"] = halted[0] if halted else None
        manifest["usage"] = {
            "input_tokens": usage["input"], "output_tokens": usage["output"],
            "cache_read_tokens": usage["cache_read"], "cache_write_tokens": usage["cache_write"],
            "cost_usd": round(usage["cost"], 4), "api_calls": usage["calls"],
        }
        self._run_writer.write_manifest(run_id, manifest)
        if not selector.dry_run and not selector.dimensions:
            self._run_writer.write_latest_pointer(
                selector.project,
                {
                    "run_id": run_id,
                    "ts": manifest["ts"],
                    "project": selector.project,
                    "tier": project_rollup.tier.value,
                    "composite": project_rollup.composite,
                    "verdicts_path": f"{run_id}/verdicts.json",
                    "findings_path": f"{run_id}/findings.json",
                    "report_path": f"{run_id}/report.md",
                },
            )

        blockers = sum(1 for f in findings_doc if f["severity"] == "blocker")
        return RunResultCdto(
            run_id=run_id,
            run_dir=self._run_writer.run_dir(run_id),
            report_path=report_path,
            project=selector.project,
            project_tier=project_rollup.tier.value,
            project_composite=project_rollup.composite,
            unit_count=len(unit_verdicts),
            findings_total=len(findings_doc),
            findings_blocker=blockers,
            usage=UsageCdto(
                input_tokens=usage["input"], output_tokens=usage["output"],
                cache_read_tokens=usage["cache_read"], cache_write_tokens=usage["cache_write"],
                cost_usd=round(usage["cost"], 4), api_calls=usage["calls"],
            ),
            halted_reason=halted[0] if halted else None,
        )

    # ---------- per-unit evaluation ----------

    async def _evaluate_unit(
        self, run_id, unit, grounding, selector, budget, usage, usage_lock, semaphore, halted
    ) -> list[FieldResult]:
        variables = unit.applicability_vars()
        overrides = self._config.project_overrides.get(unit.project, {})
        results: list[FieldResult] = []
        llm_dims: list[str] = []

        for dim in self._rubric.dimensions:
            if selector.dimensions and dim.dim_id not in selector.dimensions:
                continue
            for sub, fld in dim.iter_fields():
                if not fld.applies(variables):
                    results.append(
                        FieldResult(
                            field_id=fld.field_id, dim_id=dim.dim_id, sub_id=sub.sub_id,
                            status=FieldStatus.INAPPLICABLE, grade=None, confidence=0.0,
                            spread=0.0, justification="applies_when 不满足", evidence=(),
                            revision_hint="", source="applicability",
                        )
                    )
                    continue
                if fld.evaluator is EvaluatorKind.RULE:
                    results.append(
                        evaluate_rule(fld, dim.dim_id, sub.sub_id, unit, grounding, overrides)
                    )
            if self._rubric.applicable_fields(dim.dim_id, variables, EvaluatorKind.LLM):
                llm_dims.append(dim.dim_id)

        if not llm_dims:
            return results

        chunks = await asyncio.gather(
            *(
                self._judge_dimension(
                    run_id, dim_id, unit, grounding, variables, selector, budget,
                    usage, usage_lock, semaphore, halted
                )
                for dim_id in llm_dims
            )
        )
        for chunk in chunks:
            results.extend(chunk)
        return results

    async def _judge_dimension(
        self, run_id, dim_id, unit, grounding, variables, selector, budget, usage, usage_lock,
        semaphore, halted
    ) -> list[FieldResult]:
        dim = self._rubric.dimension(dim_id)
        fields = self._rubric.applicable_fields(dim_id, variables, EvaluatorKind.LLM)
        field_ids = [fld.field_id for _, fld in fields]
        sub_by_field = {fld.field_id: sub.sub_id for sub, fld in fields}
        model_config = self._config.judge_for(dim_id)
        samples_n = selector.samples_override or model_config.samples

        def error_results(message: str) -> list[FieldResult]:
            return [
                FieldResult(
                    field_id=fid, dim_id=dim_id, sub_id=sub_by_field[fid],
                    status=FieldStatus.JUDGE_ERROR, grade=None, confidence=0.0, spread=0.0,
                    justification="", evidence=(), revision_hint="", source="llm", error=message,
                )
                for fid in field_ids
            ]

        if selector.dry_run:
            return error_results("dry_run")

        content = self._judge_mapper.shared_blocks(unit, grounding)
        content.append(self._judge_mapper.dimension_block(dim, fields))
        schema = self._judge_mapper.output_schema(field_ids)
        system = self._judge_mapper.system_prompt()

        samples_by_field: dict[str, list[SampleJudgment]] = {fid: [] for fid in field_ids}
        conflict_counts: dict[str, int] = {fid: 0 for fid in field_ids}
        errors: list[str] = []

        async def one_sample(sample_index: int) -> dict:
            if halted:
                return {"sample": sample_index, "error": f"skipped: {halted[0]}"}
            async with usage_lock:
                if usage["cost"] >= budget:
                    if "budget_exhausted" not in halted:
                        halted.append("budget_exhausted")
                    return {"sample": sample_index, "error": "budget_exhausted"}
            async with semaphore:
                try:
                    call = await self._client.judge(model_config, system, content, schema)
                except JudgeError as exc:
                    return {"sample": sample_index, "error": f"{type(exc).__name__}: {exc}"}
                except Exception as exc:
                    return {"sample": sample_index, "error": f"api_error: {type(exc).__name__}: {exc}"}
            pricing = self._config.pricing.get(model_config.model, {})
            in_price = pricing.get("input_per_mtok", 5.0)
            out_price = pricing.get("output_per_mtok", 25.0)
            cost = (
                call.input_tokens / 1e6 * in_price
                + call.output_tokens / 1e6 * out_price
                + call.cache_read_tokens / 1e6 * in_price * 0.1
                + call.cache_write_tokens / 1e6 * in_price * 1.25
            )
            async with usage_lock:
                usage["input"] += call.input_tokens
                usage["output"] += call.output_tokens
                usage["cache_read"] += call.cache_read_tokens
                usage["cache_write"] += call.cache_write_tokens
                usage["cost"] += cost
                usage["calls"] += 1
            return {"sample": sample_index, "text": call.text}

        raw_records = sorted(
            await asyncio.gather(*(one_sample(i) for i in range(samples_n))),
            key=lambda record: record["sample"],
        )
        for record in raw_records:
            if "text" not in record:
                errors.append(record.get("error", "unknown"))
                continue
            try:
                parsed = self._judge_mapper.parse(record["text"], field_ids)
            except JudgeSchemaError as exc:
                record["error"] = str(exc)
                errors.append(str(exc))
                continue
            for fid, judgment in parsed.items():
                if judgment.justification.startswith("CANON_CONFLICT:"):
                    conflict_counts[fid] += 1
                samples_by_field[fid].append(judgment)

        self._run_writer.write_raw(
            run_id, unit.unit_id, dim_id,
            {"model": model_config.model, "samples": samples_n, "records": raw_records},
        )

        results: list[FieldResult] = []
        for fid in field_ids:
            samples = samples_by_field[fid]
            if not samples:
                results.append(
                    FieldResult(
                        field_id=fid, dim_id=dim_id, sub_id=sub_by_field[fid],
                        status=FieldStatus.JUDGE_ERROR, grade=None, confidence=0.0, spread=0.0,
                        justification="", evidence=(), revision_hint="", source="llm",
                        error="; ".join(errors[-3:]) or "all samples failed",
                    )
                )
                continue
            if conflict_counts[fid] >= math.ceil(len(samples) / 2):
                conflict = next(s for s in samples if s.justification.startswith("CANON_CONFLICT:"))
                results.append(
                    FieldResult(
                        field_id=fid, dim_id=dim_id, sub_id=sub_by_field[fid],
                        status=FieldStatus.INCONCLUSIVE, grade=None, confidence=0.0, spread=0.0,
                        justification=conflict.justification, evidence=conflict.evidence,
                        revision_hint="先修复 canon 矛盾再复评", source="llm",
                    )
                )
                continue
            results.append(
                FieldResult.reconcile(fid, dim_id, sub_by_field[fid], samples, source="llm")
            )
        return results
