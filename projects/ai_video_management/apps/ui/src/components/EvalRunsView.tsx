/** EvalRunsView: read-only browsing of eval runs with full drill-down:
 * run list (timestamped) → per-shot verdicts → per-field results → the judge's
 * per-sample raw judgments (how the agent graded). */
import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import {
  SEVERITY_CN,
  TIER_CN,
  fetchEvalRawJudgments,
  fetchEvalReport,
  fetchEvalRunDetail,
  fetchEvalRuns,
  fetchEvalUnitResults,
  formatEvalTs,
  type EvalDimensionScore,
  type EvalFieldMeta,
  type EvalFieldResult,
  type EvalFinding,
  type EvalRawJudgments,
  type EvalRollup,
  type EvalRunDetail,
  type EvalRunManifest,
  type EvalSubcategoryScore,
  type EvalUnitResults,
  type EvalUnitVerdict,
} from "../lib/evalApi";

function TierChip({ tier }: { tier?: string }): JSX.Element {
  if (!tier) return <span className="muted">—</span>;
  return <span className={`eval-tier eval-tier--${tier}`}>{TIER_CN[tier] ?? tier}</span>;
}

function RollupCard({ title, rollup }: { title: string; rollup: EvalRollup }): JSX.Element {
  const ruleFailed = rollup.rule_failed_units ?? [];
  const semanticGateFailed = (rollup.gate_failed_units ?? []).filter((u) => !ruleFailed.includes(u));
  return (
    <div className="eval-rollup">
      <div className="eval-rollup-head">
        <strong>{title}</strong> <TierChip tier={rollup.tier} />
        <span className="muted">{rollup.unit_count} 镜</span>
      </div>
      <div className="eval-rollup-line">
        <span className="eval-rollup-label">规则层</span>
        {rollup.rule_failed_units !== undefined ? (
          ruleFailed.length ? (
            <span className="eval-passfail eval-fail" title={ruleFailed.join(", ")}>
              ✗ 未过 ×{ruleFailed.length}（{ruleFailed.map((u) => u.split("/").pop()).join(", ")}）
            </span>
          ) : (
            <span className="eval-passfail eval-pass">✓ 全部通过</span>
          )
        ) : (
          <span className="muted">—（旧运行无规则层数据）</span>
        )}
      </div>
      <div className="eval-rollup-line">
        <span className="eval-rollup-label">语义层</span>
        <span className="eval-composite">{rollup.composite ?? "—"}</span>
        {semanticGateFailed.length ? (
          <span className="eval-badge eval-badge-gate" title={semanticGateFailed.join(", ")}>
            ⛔ gate 未过 ×{semanticGateFailed.length}
          </span>
        ) : null}
        <span className="eval-dim-chips">
          {Object.entries(rollup.dimension_composites).map(([dim, value]) => (
            <span key={dim} className="eval-dim-chip" title={dim}>
              {dim}: {value}
            </span>
          ))}
        </span>
      </div>
    </div>
  );
}

type RawLoader = (dim: string) => Promise<EvalRawJudgments>;

function SampleJudgments({
  fieldId,
  dim,
  loadRaw,
}: {
  fieldId: string;
  dim: string;
  loadRaw: RawLoader;
}): JSX.Element {
  const [raw, setRaw] = useState<EvalRawJudgments | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadRaw(dim)
      .then(setRaw)
      .catch((err: Error) => setError(err.message));
  }, [dim, loadRaw]);

  if (error) return <p className="eval-status-err">评审样本加载失败：{error}</p>;
  if (!raw) return <p className="muted">加载评审样本…</p>;

  return (
    <div className="eval-samples">
      <p className="muted">
        评审模型：{raw.model ?? "?"} · 请求样本数 {raw.samples_requested ?? raw.samples.length}
      </p>
      {raw.samples.map((sample, index) => {
        const judgment = sample.judgments?.find((j) => j.field_id === fieldId);
        return (
          <div key={index} className="eval-sample">
            <div className="eval-sample-head">
              样本 #{(sample.sample ?? index) + 1}
              {sample.error ? <span className="eval-status-err">（{sample.error}）</span> : null}
            </div>
            {judgment ? (
              <div className="eval-sample-body">
                <p>
                  <strong>{judgment.grade} 分</strong> · 置信 {judgment.confidence}
                </p>
                <p>{judgment.justification}</p>
                {judgment.evidence.map((quote) => (
                  <blockquote key={quote}>{quote}</blockquote>
                ))}
                {judgment.revision_hint ? (
                  <p>
                    <strong>修改建议：</strong>
                    {judgment.revision_hint}
                  </p>
                ) : null}
              </div>
            ) : sample.text_preview ? (
              <pre className="eval-raw-text">{sample.text_preview}</pre>
            ) : (
              <p className="muted">该样本无此字段的判定（可能校验失败被丢弃）。</p>
            )}
          </div>
        );
      })}
    </div>
  );
}

function FieldResultRow({
  field,
  meta,
  loadRaw,
}: {
  field: EvalFieldResult;
  meta?: EvalFieldMeta;
  loadRaw: RawLoader;
}): JSX.Element {
  const [open, setOpen] = useState<boolean>(false);
  const [showSamples, setShowSamples] = useState<boolean>(false);
  const flagged = field.grade !== null && field.grade <= 3;

  return (
    <>
      <tr
        className={flagged ? "eval-field-row eval-row-flag" : "eval-field-row"}
        onClick={() => setOpen((v) => !v)}
      >
        <td>
          {open ? "▾" : "▸"} {meta?.name_cn ?? field.field_id}
          {meta?.gate ? <span className="eval-badge eval-badge-gate">gate</span> : null}
        </td>
        <td className="muted">{field.field_id}</td>
        <td>
          <span className={field.source === "rule" ? "eval-badge eval-badge-rule" : "eval-badge eval-badge-llm"}>
            {field.source}
          </span>
        </td>
        <td>{field.status}</td>
        <td>
          {field.source === "rule" && field.grade !== null ? (
            <span className={field.grade >= 5 ? "eval-passfail eval-pass" : "eval-passfail eval-fail"}>
              {field.grade >= 5 ? "通过" : "不通过"}
            </span>
          ) : (
            field.grade ?? "—"
          )}
        </td>
        <td>{field.source === "rule" ? "—" : field.confidence}</td>
        <td>{field.source === "rule" ? "" : field.spread || ""}</td>
      </tr>
      {open ? (
        <tr className="eval-field-detail">
          <td colSpan={7}>
            {field.justification ? <p>{field.justification}</p> : null}
            {field.error ? <p className="eval-status-err">错误：{field.error}</p> : null}
            {field.evidence.map((quote) => (
              <blockquote key={quote}>{quote}</blockquote>
            ))}
            {field.revision_hint ? (
              <p>
                <strong>修改建议：</strong>
                {field.revision_hint}
              </p>
            ) : null}
            {field.source !== "rule" ? (
              <>
                <button
                  type="button"
                  className="eval-btn"
                  onClick={(e) => {
                    e.stopPropagation();
                    setShowSamples((v) => !v);
                  }}
                >
                  {showSamples ? "收起评审样本" : "查看逐样本评审详情"}
                </button>
                {showSamples ? (
                  <SampleJudgments fieldId={field.field_id} dim={field.dim_id} loadRaw={loadRaw} />
                ) : null}
              </>
            ) : (
              <p className="muted">规则字段：由确定性代码判定，无 LLM 评审样本。</p>
            )}
          </td>
        </tr>
      ) : null}
    </>
  );
}

function ScoreBadge({ composite }: { composite: number | null | undefined }): JSX.Element {
  if (composite === null || composite === undefined) return <span className="muted">—</span>;
  const cls = composite >= 75 ? "eval-agg-good" : composite >= 60 ? "eval-agg-mid" : "eval-agg-bad";
  return <span className={`eval-agg ${cls}`}>{composite}</span>;
}

function SubcategorySection({
  layer,
  sub,
  fields,
  metaOf,
  loadRaw,
}: {
  layer: Layer;
  sub: EvalSubcategoryScore;
  fields: EvalFieldResult[];
  metaOf: (id: string) => EvalFieldMeta | undefined;
  loadRaw: RawLoader;
}): JSX.Element {
  const ruleFailed = fields.filter((f) => f.source === "rule" && f.grade !== null && f.grade < 5).length;
  const rulePassed = fields.filter((f) => f.source === "rule" && f.grade !== null && f.grade >= 5).length;
  return (
    <div className="eval-sub-section">
      <div className="eval-sub-head">
        {sub.name_cn}
        <span className="muted">（{sub.sub_id}）</span>
        {layer === "semantic" ? (
          <>
            <ScoreBadge composite={sub.composite} />
            <span className="muted">
              {sub.graded} 判分{sub.inconclusive ? ` · ${sub.inconclusive} 存疑` : ""}
              {sub.errors ? ` · ${sub.errors} 出错` : ""}
            </span>
          </>
        ) : (
          <RulePassFail failed={ruleFailed} passed={rulePassed} />
        )}
      </div>
      <table className="eval-table">
        <thead>
          <tr>
            <th>字段</th>
            <th>id</th>
            <th>来源</th>
            <th>状态</th>
            <th>分</th>
            <th>置信</th>
            <th>样本分歧</th>
          </tr>
        </thead>
        <tbody>
          {fields.map((field) => (
            <FieldResultRow key={field.field_id} field={field} meta={metaOf(field.field_id)} loadRaw={loadRaw} />
          ))}
        </tbody>
      </table>
    </div>
  );
}

type Layer = "rule" | "semantic";

function RulePassFail({ failed, passed }: { failed: number; passed: number }): JSX.Element {
  if (failed > 0) return <span className="eval-passfail eval-fail">✗ 未过 {failed} 项</span>;
  return <span className="eval-passfail eval-pass">✓ {passed}/{passed}</span>;
}

function DimensionSection({
  layer,
  score,
  fields,
  metaOf,
  loadRaw,
}: {
  layer: Layer;
  score: EvalDimensionScore;
  fields: EvalFieldResult[];
  metaOf: (id: string) => EvalFieldMeta | undefined;
  loadRaw: RawLoader;
}): JSX.Element {
  const [open, setOpen] = useState<boolean>(false);
  const bySub = new Map<string, EvalFieldResult[]>();
  for (const field of fields) {
    const list = bySub.get(field.sub_id) ?? [];
    list.push(field);
    bySub.set(field.sub_id, list);
  }
  const subs: EvalSubcategoryScore[] = score.subcategories?.length
    ? score.subcategories
    : [...bySub.keys()].map((subId) => {
        const graded = (bySub.get(subId) ?? []).filter((f) => f.grade !== null);
        const mean = graded.length
          ? Math.round(
              (graded.reduce((sum, f) => sum + ((f.grade as number) - 1) * 25, 0) / graded.length) * 100,
            ) / 100
          : null;
        return {
          sub_id: subId,
          name_cn: metaOf(bySub.get(subId)?.[0]?.field_id ?? "")?.sub_name ?? subId,
          composite: mean,
          graded: graded.length,
          inconclusive: 0,
          inapplicable: 0,
          errors: 0,
        };
      });

  const ruleFailedInDim = fields.filter((f) => f.source === "rule" && f.grade !== null && f.grade < 5).length;
  const rulePassedInDim = fields.filter((f) => f.source === "rule" && f.grade !== null && f.grade >= 5).length;

  return (
    <div className="eval-dim-section">
      <button type="button" className="eval-dim-head" onClick={() => setOpen((v) => !v)}>
        <span>
          {open ? "▾" : "▸"} {score.name_cn} <span className="muted">（{score.dim_id}）</span>
        </span>
        <span className="eval-dim-head-right">
          {layer === "semantic" && score.gate_failures.length ? (
            <span className="eval-badge eval-badge-gate">gate: {score.gate_failures.join(",")}</span>
          ) : null}
          {layer === "semantic" ? (
            <>
              <span className="muted">
                {score.graded} 判分{score.inconclusive ? ` · ${score.inconclusive} 存疑` : ""}
                {score.errors ? ` · ${score.errors} 出错` : ""}
              </span>
              <ScoreBadge composite={score.composite} />
            </>
          ) : (
            <RulePassFail failed={ruleFailedInDim} passed={rulePassedInDim} />
          )}
        </span>
      </button>
      {open
        ? subs
            .filter((sub) => (bySub.get(sub.sub_id) ?? []).length > 0)
            .map((sub) => (
              <SubcategorySection
                key={sub.sub_id}
                layer={layer}
                sub={sub}
                fields={bySub.get(sub.sub_id) ?? []}
                metaOf={metaOf}
                loadRaw={loadRaw}
              />
            ))
        : null}
    </div>
  );
}

function UnitRow({ runId, unit }: { runId: string; unit: EvalUnitVerdict }): JSX.Element {
  const [open, setOpen] = useState<boolean>(false);
  const [results, setResults] = useState<EvalUnitResults | null>(null);
  const [error, setError] = useState<string | null>(null);
  const rawCache = useRef<Map<string, Promise<EvalRawJudgments>>>(new Map());

  const loadRaw: RawLoader = (dim) => {
    const cached = rawCache.current.get(dim);
    if (cached) return cached;
    const promise = fetchEvalRawJudgments(runId, unit.unit_id, dim);
    rawCache.current.set(dim, promise);
    return promise;
  };

  const toggle = (): void => {
    const next = !open;
    setOpen(next);
    if (next && results === null && !unit.carried_forward) {
      fetchEvalUnitResults(runId, unit.unit_id)
        .then(setResults)
        .catch((err: Error) => setError(err.message));
    }
  };

  const severities = { blocker: 0, major: 0, minor: 0 } as Record<string, number>;
  for (const finding of unit.findings) severities[finding.severity] += 1;
  const ruleFailedCount = unit.rule_failed_fields?.length ?? 0;

  return (
    <>
      <tr className="eval-field-row" onClick={toggle}>
        <td>{open ? "▾" : "▸"} {unit.unit_id}</td>
        <td>
          <TierChip tier={unit.tier} />
        </td>
        <td>
          {unit.rule_total ? (
            <RulePassFail failed={ruleFailedCount} passed={unit.rule_passed ?? 0} />
          ) : (
            <span className="muted">—</span>
          )}
        </td>
        <td>{unit.composite ?? "—"}</td>
        <td>
          {severities.blocker}/{severities.major}/{severities.minor}
        </td>
        <td>{unit.inconclusive}</td>
        <td>{unit.errors}</td>
        <td className="muted">
          {unit.carried_forward ? "沿用上次" : ""}
          {unit.gate_failures.length ? ` gate: ${unit.gate_failures.join(",")}` : ""}
        </td>
      </tr>
      {open ? (
        <tr className="eval-field-detail">
          <td colSpan={8}>
            {unit.carried_forward ? (
              <p className="muted">该镜结果沿用上一次运行（文件未变化），字段级详情见其原运行。</p>
            ) : error ? (
              <p className="eval-status-err">{error}</p>
            ) : results ? (
              (() => {
                const visible = results.fields.filter((f) => f.status !== "inapplicable");
                const ruleFields = visible.filter((f) => f.source === "rule");
                const semanticFields = visible.filter((f) => f.source !== "rule");
                const metaOf = (id: string): EvalFieldMeta | undefined => results.field_meta?.[id];
                const byDim = (fields: EvalFieldResult[]): Map<string, EvalFieldResult[]> => {
                  const grouped = new Map<string, EvalFieldResult[]>();
                  for (const field of fields) {
                    const list = grouped.get(field.dim_id) ?? [];
                    list.push(field);
                    grouped.set(field.dim_id, list);
                  }
                  return grouped;
                };
                const renderLayer = (layer: Layer, fields: EvalFieldResult[]): JSX.Element[] => {
                  const grouped = byDim(fields);
                  return unit.dimension_scores
                    .filter((score) => (grouped.get(score.dim_id) ?? []).length > 0)
                    .map((score) => (
                      <DimensionSection
                        key={`${layer}-${score.dim_id}`}
                        layer={layer}
                        score={score}
                        fields={grouped.get(score.dim_id) ?? []}
                        metaOf={metaOf}
                        loadRaw={loadRaw}
                      />
                    ));
                };
                return (
                  <>
                    <div className="eval-layer">
                      <div className="eval-layer-head">
                        <strong>规则层 · 100% 确定性硬契约</strong>
                        <span className="muted">二元判定；任一未过 → 本镜/本集/项目直接 FAIL</span>
                        {unit.rule_total ? (
                          <RulePassFail failed={ruleFailedCount} passed={unit.rule_passed ?? 0} />
                        ) : null}
                      </div>
                      {ruleFields.length ? renderLayer("rule", ruleFields) : <p className="muted">本镜无适用规则字段。</p>}
                    </div>
                    <div className="eval-layer">
                      <div className="eval-layer-head">
                        <strong>语义层 · LLM 评分</strong>
                        <span className="muted">加权聚合；判定阈值见 rubric</span>
                        <ScoreBadge composite={unit.composite} />
                      </div>
                      {semanticFields.length ? renderLayer("semantic", semanticFields) : <p className="muted">本镜无适用语义字段。</p>}
                    </div>
                  </>
                );
              })()
            ) : (
              <p className="muted">加载中…</p>
            )}
          </td>
        </tr>
      ) : null}
    </>
  );
}

function FindingCard({ finding }: { finding: EvalFinding }): JSX.Element {
  const [open, setOpen] = useState<boolean>(false);
  return (
    <div className={`eval-finding eval-finding--${finding.severity}`}>
      <button type="button" className="eval-finding-head" onClick={() => setOpen((v) => !v)}>
        <span className={`eval-sev eval-sev--${finding.severity}`}>{SEVERITY_CN[finding.severity]}</span>
        <strong>{finding.field_name_cn}</strong>
        <span className="muted">
          {finding.unit_id} · {finding.dim_id}/{finding.field_id} · {finding.grade} 分
        </span>
        <code className="muted">{finding.finding_id}</code>
      </button>
      {open ? (
        <div className="eval-finding-body">
          <p>{finding.justification}</p>
          {finding.evidence.slice(0, 4).map((quote) => (
            <blockquote key={quote}>{quote}</blockquote>
          ))}
          {finding.revision_hint ? (
            <p>
              <strong>修改建议：</strong>
              {finding.revision_hint}
            </p>
          ) : null}
          <p className="muted">{finding.locator}</p>
        </div>
      ) : null}
    </div>
  );
}

function RunDetailPanel({ runId }: { runId: string }): JSX.Element {
  const [detail, setDetail] = useState<EvalRunDetail | null>(null);
  const [report, setReport] = useState<string | null>(null);
  const [showReport, setShowReport] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setDetail(null);
    setReport(null);
    setShowReport(false);
    fetchEvalRunDetail(runId)
      .then((d) => {
        setDetail(d);
        setError(null);
      })
      .catch((err: Error) => setError(err.message));
  }, [runId]);

  const toggleReport = (): void => {
    const next = !showReport;
    setShowReport(next);
    if (next && report === null) {
      fetchEvalReport(runId)
        .then((r) => setReport(r.content))
        .catch((err: Error) => setReport(`报告加载失败：${err.message}`));
    }
  };

  if (error) return <p className="eval-status-err">{error}</p>;
  if (!detail) return <p className="muted">加载中…</p>;
  const verdicts = detail.verdicts;

  return (
    <div>
      <p className="muted">
        运行 {runId} · 评测时间 {formatEvalTs(detail.manifest.ts)} · rubric v{detail.manifest.rubric_version}
      </p>
      {verdicts ? (
        <>
          <RollupCard title={`项目 ${detail.manifest.project}`} rollup={verdicts.project_verdict} />
          <div className="eval-rollup-grid">
            {Object.entries(verdicts.episode_verdicts).map(([scope, rollup]) => (
              <RollupCard key={scope} title={scope} rollup={rollup} />
            ))}
          </div>
          <h3>逐镜判定（点击展开 规则层/语义层 → 维度 → 子类 → 字段 → 逐样本评审）</h3>
          <table className="eval-table">
            <thead>
              <tr>
                <th>镜</th>
                <th>判定</th>
                <th>规则层</th>
                <th>语义综合分</th>
                <th>阻/严/轻</th>
                <th>存疑</th>
                <th>出错</th>
                <th>备注</th>
              </tr>
            </thead>
            <tbody>
              {verdicts.units.map((unit) => (
                <UnitRow key={unit.unit_id} runId={runId} unit={unit} />
              ))}
            </tbody>
          </table>
        </>
      ) : (
        <p className="muted">该运行没有 verdicts.json。</p>
      )}
      {detail.findings?.length ? (
        <>
          <h3>发现清单（{detail.findings.length}）</h3>
          {detail.findings.map((finding) => (
            <FindingCard key={`${finding.finding_id}-${finding.unit_id}`} finding={finding} />
          ))}
        </>
      ) : null}
      <div className="eval-editor-bar">
        <button type="button" className="eval-btn" onClick={toggleReport}>
          {showReport ? "收起报告" : "查看 report.md"}
        </button>
      </div>
      {showReport ? (
        <div className="eval-report markdown-body">
          {report === null ? (
            <p className="muted">加载中…</p>
          ) : (
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{report}</ReactMarkdown>
          )}
        </div>
      ) : null}
    </div>
  );
}

export function EvalRunsView(): JSX.Element {
  const [runs, setRuns] = useState<EvalRunManifest[] | null>(null);
  const [latest, setLatest] = useState<Record<string, string>>({});
  const [selected, setSelected] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchEvalRuns()
      .then((r) => {
        setRuns(r.runs);
        setLatest(r.latest);
        const firstLatest = Object.values(r.latest)[0];
        setSelected((prev) => prev ?? firstLatest ?? r.runs[0]?.run_id ?? null);
        setError(null);
      })
      .catch((err: Error) => setError(err.message));
  }, []);

  if (error) return <p className="eval-status-err">{error}</p>;
  if (!runs) return <p className="muted">加载中…</p>;
  if (!runs.length)
    return (
      <p className="muted">
        还没有评测运行。用 CLI 触发：<code>python -m apps.cli.main run --project ...</code>
      </p>
    );

  const latestIds = new Set(Object.values(latest));

  return (
    <div>
      <table className="eval-table">
        <thead>
          <tr>
            <th>评测时间</th>
            <th>运行</th>
            <th>项目</th>
            <th>状态</th>
            <th>判定</th>
            <th>综合分</th>
            <th>发现(阻断)</th>
            <th>成本</th>
          </tr>
        </thead>
        <tbody>
          {runs.map((run) => (
            <tr
              key={run.run_id}
              className={run.run_id === selected ? "eval-run-row eval-run-row-active" : "eval-run-row"}
              onClick={() => setSelected(run.run_id)}
            >
              <td>{formatEvalTs(run.ts)}</td>
              <td>
                {run.run_id}
                {latestIds.has(run.run_id) ? <span className="eval-badge eval-badge-latest">latest</span> : null}
                {run.selector?.dry_run ? <span className="eval-badge">dry</span> : null}
              </td>
              <td>{run.project}</td>
              <td>{run.status}{run.halted_reason ? ` (${run.halted_reason})` : ""}</td>
              <td>
                <TierChip tier={run.tier} />
              </td>
              <td>{run.composite ?? "—"}</td>
              <td>
                {run.findings_total ?? "—"}
                {run.findings_blocker ? ` (${run.findings_blocker})` : ""}
              </td>
              <td>{run.usage?.cost_usd !== undefined ? `$${run.usage.cost_usd}` : "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {selected ? <RunDetailPanel runId={selected} /> : null}
    </div>
  );
}
