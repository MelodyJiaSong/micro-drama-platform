/** EvalRubricView: visualize the frozen rubric (dimensions → subcategories →
 * fields with anchors) and edit any rubric YAML file. Saves run the eval CLI's
 * `rubric validate` server-side and auto-roll back on failure. */
import { useCallback, useEffect, useState } from "react";
import {
  fetchEvalOverview,
  fetchEvalRubricFile,
  putEvalRubricFile,
  type EvalDimension,
  type EvalField,
  type EvalOverview,
} from "../lib/evalApi";

function FieldRow({ field }: { field: EvalField }): JSX.Element {
  const [open, setOpen] = useState<boolean>(false);
  return (
    <>
      <tr className="eval-field-row" onClick={() => setOpen((v) => !v)}>
        <td>
          <span className={field.evaluator === "rule" ? "eval-badge eval-badge-rule" : "eval-badge eval-badge-llm"}>
            {field.evaluator}
          </span>
        </td>
        <td>
          {field.name_cn}
          {field.gate ? <span className="eval-badge eval-badge-gate" title={`gate：低于 ${field.gate_min_grade ?? 3} 分一票否决`}>gate</span> : null}
        </td>
        <td className="muted">{field.id}</td>
        <td>{field.evaluator === "rule" ? <span className="muted">pass/fail</span> : field.weight}</td>
        <td className="muted">{field.applies_when ?? "—"}</td>
      </tr>
      {open ? (
        <tr className="eval-field-detail">
          <td colSpan={5}>
            {field.judge_instruction_cn ? (
              <p>
                <strong>判定说明：</strong>
                {field.judge_instruction_cn}
              </p>
            ) : null}
            {field.rule_id ? (
              <p>
                <strong>规则：</strong>
                <code>{field.rule_id}</code> {JSON.stringify(field.rule_params ?? {})}
              </p>
            ) : null}
            {field.anchors ? (
              <ul className="eval-anchors">
                <li>
                  <strong>1分：</strong>
                  {field.anchors.g1}
                </li>
                <li>
                  <strong>3分：</strong>
                  {field.anchors.g3}
                </li>
                <li>
                  <strong>5分：</strong>
                  {field.anchors.g5}
                </li>
              </ul>
            ) : null}
            {field.sources?.length ? <p className="muted">来源：{field.sources.join("；")}</p> : null}
          </td>
        </tr>
      ) : null}
    </>
  );
}

function DimensionCard({
  dim,
  onEdit,
}: {
  dim: EvalDimension;
  onEdit: (file: string) => void;
}): JSX.Element {
  const [open, setOpen] = useState<boolean>(false);
  const fieldCount = dim.subcategories.reduce((n, s) => n + s.fields.length, 0);
  return (
    <section className="eval-card">
      <div className="eval-card-head">
        <button type="button" className="eval-card-toggle" onClick={() => setOpen((v) => !v)}>
          {open ? "▾" : "▸"} {dim.name_cn}
          <span className="muted">
            （{dim.dimension_id} · 权重 {dim.weight} · {fieldCount} 字段）
          </span>
        </button>
        <button type="button" className="eval-btn" onClick={() => onEdit(dim.file)}>
          编辑 YAML
        </button>
      </div>
      {open ? (
        <>
          <p className="muted">{dim.description_cn}</p>
          {dim.subcategories.map((sub) => (
            <div key={sub.id} className="eval-subcat">
              <h4>
                {sub.name_cn} <span className="muted">({sub.id} · 权重 {sub.weight})</span>
              </h4>
              <table className="eval-table">
                <thead>
                  <tr>
                    <th>评审</th>
                    <th>字段</th>
                    <th>id</th>
                    <th>权重</th>
                    <th>适用条件</th>
                  </tr>
                </thead>
                <tbody>
                  {sub.fields.map((field) => (
                    <FieldRow key={field.id} field={field} />
                  ))}
                </tbody>
              </table>
            </div>
          ))}
        </>
      ) : null}
    </section>
  );
}

function YamlEditor({
  file,
  onClose,
  onSaved,
}: {
  file: string;
  onClose: () => void;
  onSaved: () => void;
}): JSX.Element {
  const [content, setContent] = useState<string | null>(null);
  const [saving, setSaving] = useState<boolean>(false);
  const [status, setStatus] = useState<{ kind: "ok" | "err"; text: string } | null>(null);

  useEffect(() => {
    fetchEvalRubricFile(file)
      .then((r) => setContent(r.content))
      .catch((err: Error) => setStatus({ kind: "err", text: err.message }));
  }, [file]);

  const onSave = async (): Promise<void> => {
    if (content === null) return;
    setSaving(true);
    setStatus(null);
    try {
      const result = await putEvalRubricFile(file, content);
      setStatus({ kind: "ok", text: `已保存并通过 rubric validate。${result.output.trim()}` });
      onSaved();
    } catch (err) {
      setStatus({ kind: "err", text: err instanceof Error ? err.message : String(err) });
    } finally {
      setSaving(false);
    }
  };

  return (
    <section className="eval-card eval-editor-card">
      <div className="eval-card-head">
        <h3>编辑 rubric/{file}</h3>
        <button type="button" className="eval-btn" onClick={onClose}>
          关闭
        </button>
      </div>
      <p className="muted">保存时后端会运行 eval CLI 的 rubric validate；校验失败自动回滚。</p>
      {content !== null ? (
        <>
          <textarea
            className="eval-editor"
            value={content}
            spellCheck={false}
            rows={30}
            onChange={(e) => setContent(e.target.value)}
            aria-label={`${file} 编辑器`}
          />
          <div className="eval-editor-bar">
            <button type="button" className="eval-btn" disabled={saving} onClick={() => void onSave()}>
              {saving ? "校验中…" : "保存并校验"}
            </button>
            {status ? (
              <span className={status.kind === "ok" ? "eval-status-ok" : "eval-status-err"}>
                {status.text}
              </span>
            ) : null}
          </div>
        </>
      ) : status ? (
        <p className="eval-status-err">{status.text}</p>
      ) : (
        <p className="muted">加载中…</p>
      )}
    </section>
  );
}

function filterDimension(dim: EvalDimension, evaluator: "rule" | "llm"): EvalDimension | null {
  const subcategories = dim.subcategories
    .map((sub) => ({ ...sub, fields: sub.fields.filter((f) => f.evaluator === evaluator) }))
    .filter((sub) => sub.fields.length > 0);
  if (!subcategories.length) return null;
  return { ...dim, subcategories };
}

export function EvalRubricView(): JSX.Element {
  const [overview, setOverview] = useState<EvalOverview | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [editing, setEditing] = useState<string | null>(null);

  const load = useCallback(() => {
    fetchEvalOverview()
      .then((o) => {
        setOverview(o);
        setError(null);
      })
      .catch((err: Error) => setError(err.message));
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  if (error) return <p className="eval-status-err">{error}</p>;
  if (!overview) return <p className="muted">加载中…</p>;

  const ruleDims = overview.dimensions
    .map((d) => filterDimension(d, "rule"))
    .filter((d): d is EvalDimension => d !== null);
  const llmDims = overview.dimensions
    .map((d) => filterDimension(d, "llm"))
    .filter((d): d is EvalDimension => d !== null);
  const ruleCount = ruleDims.reduce((n, d) => n + d.subcategories.reduce((m, s) => m + s.fields.length, 0), 0);
  const llmCount = llmDims.reduce((n, d) => n + d.subcategories.reduce((m, s) => m + s.fields.length, 0), 0);

  return (
    <div>
      <section className="eval-card">
        <div className="eval-card-head">
          <h2>
            Rubric v{overview.version}
            <span className="muted">
              （规则层 {ruleCount} 条 · 语义层 {llmCount} 条）
            </span>
          </h2>
          <button type="button" className="eval-btn" onClick={() => setEditing("rubric.yaml")}>
            编辑 rubric.yaml（权重/阈值）
          </button>
        </div>
        <p className="muted">
          判定阈值：{JSON.stringify(overview.verdict)}
        </p>
      </section>
      {editing ? (
        <YamlEditor file={editing} onClose={() => setEditing(null)} onSaved={load} />
      ) : null}
      <section className="eval-layer">
        <div className="eval-layer-head">
          <strong>规则层 · 100% 确定性 check（{ruleCount} 条）</strong>
          <span className="muted">纯代码判定，只有 pass/fail；任一 fail → 该镜/该集/项目直接 FAIL，不参与打分</span>
        </div>
        {ruleDims.map((dim) => (
          <DimensionCard key={`rule-${dim.dimension_id}`} dim={dim} onEdit={(file) => setEditing(file)} />
        ))}
      </section>
      <section className="eval-layer">
        <div className="eval-layer-head">
          <strong>语义层 · LLM 评分 check（{llmCount} 条）</strong>
          <span className="muted">1–5 分锚点评分 × 权重 → 子类/维度/镜 逐层确定性聚合为综合分</span>
        </div>
        {llmDims.map((dim) => (
          <DimensionCard key={`llm-${dim.dimension_id}`} dim={dim} onEdit={(file) => setEditing(file)} />
        ))}
      </section>
    </div>
  );
}
