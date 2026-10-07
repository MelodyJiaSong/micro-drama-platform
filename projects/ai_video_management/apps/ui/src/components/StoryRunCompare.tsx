import { useEffect, useState } from "react";
import { loadStoryRun, type RunSummary, type StoryRun } from "../lib/storyRuns";
import { Frame, Notes, Sources, Markdown, DECISIONS, when } from "./StoryRunDisplay";

function canonical(value: unknown): string {
  if (Array.isArray(value)) return `[${value.map(canonical).join(",")}]`;
  if (value && typeof value === "object") return `{${Object.entries(value).sort(([a], [b]) => a.localeCompare(b)).map(([key, item]) => `${JSON.stringify(key)}:${canonical(item)}`).join(",")}}`;
  return JSON.stringify(value) ?? "null";
}
const paragraphs = (text: string): string[] => text.trim().split(/\n\s*\n/).filter(Boolean);
function Review({ run }: { run: StoryRun }): JSX.Element {
  const reviewers = run.participants.filter(item => item.scope === "story" && /审稿|审查|review/i.test(item.role));
  return <><h3>审稿意见与明确取舍</h3>
    {run.proposals.map(item => <details key={item.id} className="story-run-detail"><summary>{DECISIONS[item.decision]} · {item.title}</summary>
      <p>{item.detail}</p><p><strong>决定理由：</strong>{item.decision_reason || "未记录"}</p>
      <p className="story-run-muted">对应标准：{item.criteria.map(String).join("；") || "未逐项绑定"}</p></details>)}
    {!run.proposals.length ? <p className="story-run-muted">尚无逐项意见。</p> : null}
    {reviewers.map(item => <details key={item.id} className="story-run-detail"><summary>{item.name} · 完整审稿回复</summary><Markdown text={item.output || "尚未返回"} /></details>)}
  </>;
}
function Candidate({ label, run, other, summary }: { label: string; run: StoryRun; other: StoryRun; summary?: RunSummary }): JSX.Element {
  const counterpart = new Set(paragraphs(other.candidate.text));
  return <article className="story-compare-candidate" aria-label={`${label} 候选`}>
    <header><h2>{label} · {run.candidate.title || summary?.title || "候选故事"}</h2><p className="story-run-muted">{when(run.created_at)}</p>
      <code>{run.run_id}</code><details className="story-run-detail"><summary>独立文件夹位置</summary><code>{summary?.audit_folder || summary?.audit_path || "未记录"}</code></details></header>
    <h3>六个基本问题</h3><Frame frame={run.candidate.frame} />
    <h3>候选正文</h3><p className="story-run-prose">{run.candidate.brief}</p>
    <div className="story-run-story">{paragraphs(run.candidate.text).map((paragraph, index) => <p key={index} className={`story-run-prose ${counterpart.has(paragraph) ? "" : "story-compare-changed"}`}>{paragraph}</p>)}</div>
    {!run.candidate.text ? <p>尚未形成候选正文。</p> : null}
    <h3>候选状态变化</h3><Notes values={run.candidate.state_changes} empty="尚未记录状态变化。" /><Review run={run} />
  </article>;
}
export function StoryRunCompare({ run, runs, compareId, onCompare, onPrimary }: {
  run: StoryRun; runs: RunSummary[]; compareId: string;
  onCompare: (id: string) => void; onPrimary: (id: string) => void;
}): JSX.Element {
  const [comparison, setComparison] = useState<StoryRun | null>(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const other = comparison?.run_id === compareId && comparison.episode_path === run.episode_path ? comparison : null;
  useEffect(() => {
    const controller = new AbortController(); setComparison(null); setError("");
    if (!compareId || compareId === run.run_id) { setBusy(false); return () => controller.abort(); }
    setBusy(true);
    void loadStoryRun(run.episode_path, compareId, controller.signal).then(data => {
      if (controller.signal.aborted) return;
      if (data.run_id !== compareId || data.episode_path !== run.episode_path) throw new Error("对比记录归属不匹配");
      setComparison(data);
    }).catch(err => { if (!controller.signal.aborted) setError(`读取对比失败：${err instanceof Error ? err.message : String(err)}`); })
      .finally(() => { if (!controller.signal.aborted) setBusy(false); });
    return () => controller.abort();
  }, [compareId, run.run_id, run.episode_path]);
  const sameInput = other && !!run.input.input_hash && run.input.input_hash === other.input.input_hash;
  const sameRules = other && canonical(run.input.rules) === canonical(other.input.rules);
  const criteria = [...new Set([...(run.input.criteria || []), ...(other?.input.criteria || [])])];
  return <div className="story-run-comparison">
    <section><h2>两个独立 run 对比</h2><div className="story-compare-selectors">
      <label>A · 主要查看 <select value={run.run_id} onChange={event => onPrimary(event.target.value)}>{runs.map(item => <option key={item.run_id} value={item.run_id}>{item.title || item.run_id}</option>)}</select></label>
      <label>B · 对比查看 <select value={compareId} onChange={event => onCompare(event.target.value)}><option value="">选择另一个 run</option>{runs.filter(item => item.run_id !== run.run_id).map(item => <option key={item.run_id} value={item.run_id}>{item.title || item.run_id}</option>)}</select></label>
    </div><p className="story-run-muted">分别保留输入、候选与过程文件夹；对比仅查看，不改变 EP1 当前采用稿。</p>
      {compareId === run.run_id ? <p role="alert">请选择两个不同的 run。</p> : null}
      {busy ? <p role="status">读取 B 运行…</p> : null}{error ? <p role="alert">{error}</p> : null}
      {other ? <><div className="story-compare-facts"><strong>{sameInput ? "输入指纹相同（覆盖规则）" : "输入指纹不同"}</strong><strong>{sameRules ? "冻结规则快照相同" : "冻结规则快照不同"}</strong></div>
        <p className="story-run-muted">{Array.from(run.candidate.text).length} / {Array.from(other.candidate.text).length} 字；着色段落在另一稿中没有完全相同的文本。它只表示文字差异，不是剧情质量评分。</p>
        <p className="story-run-muted">两次运行不足以证明规则造成质量变化。模型未公开时，也不能据此认定使用了相同模型。</p>
      </> : null}
    </section>
    {other ? <><div className="story-compare-columns">
      <Candidate label="A" run={run} other={other} summary={runs.find(item => item.run_id === run.run_id)} />
      <Candidate label="B" run={other} other={run} summary={runs.find(item => item.run_id === other.run_id)} />
    </div><section><h2>规则约束与记录的检查</h2><p className="story-run-muted">只展示实际绑定的意见；没有对应记录时标明未逐项记录，不代替审稿结论。</p>
      {criteria.length ? <div className="story-run-table-scroll"><table className="story-run-files"><thead><tr><th>共用检查问题</th><th>A 的对应记录</th><th>B 的对应记录</th></tr></thead><tbody>
        {criteria.map(item => <tr key={item}><td>{item}</td>{[run, other].map(value => <td key={value.run_id}>{value.proposals.filter(proposal => proposal.criteria.some(criterion => typeof criterion === "string" && criterion.includes(item))).map(proposal => `${DECISIONS[proposal.decision]}：${proposal.title} — ${proposal.decision_reason}`).join("；") || "无逐项绑定记录"}</td>)}</tr>)}
      </tbody></table></div> : <p>未记录逐项检查问题。</p>}
      <Sources label="A · 冻结规则正文" values={run.input.rules} /><Sources label="B · 冻结规则正文" values={other.input.rules} />
    </section></> : null}
  </div>;
}
