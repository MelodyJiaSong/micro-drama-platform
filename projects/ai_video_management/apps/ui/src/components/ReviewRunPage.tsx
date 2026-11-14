import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import rehypeSanitize from "rehype-sanitize";
import remarkGfm from "remark-gfm";
import { Link, useSearchParams } from "react-router-dom";
import { fetchFile, fetchReviewChecklist, fetchReviewRuns, fetchSubtree, type ReviewRunSummary } from "../api";
import { globalSourceUrl } from "../lib/globalWorkflow";
import { reviewLawHref } from "../lib/reviewLaw";
import { REVIEW_STRATEGY_PATH } from "../lib/reviewStrategy";
import {
  LOOP_STEPS, SEVERITY_ORDER, SHOOT_CONFIRM_NOTE, agentShort, attemptsNewestFirst, displayState, episodeScopes, fileHref, isRunDir, itemStatusText,
  latestInScope, lawRows, listScope, mustFailed, needsShootConfirm, progress, reviewItemHref, reviewRunHref, shownAttempt, skillPart, stateText, tickedAttempt, totals,
  type AgentDispatch, type ReviewItem, type ReviewRun,
} from "../lib/reviewRun";
import { reviewCorrectionsHref } from "../lib/reviewCorrections";
import { LOOP_V5, isV5Item, isV5Run, reviewIssuesHref } from "../lib/reviewV5";
import { IssueSummaryCard } from "./ReviewIssues";
import { ReconcileSection, SlotCards, SlotChip } from "./ReviewV5";
import "./ReviewRunPage.css";

// 两层（follow-up 333）：审查单页只给每个大类一行摘要（审了没、问题数、哪些审稿人）；
// 点进去是审稿人详情页：怎么审、审查流程、必查项结果、报告全文。

// 「已收轮」是中性的绿色：每轮审查不等用户 review（用户 2026-11-08）；旧单的「待用户确认」按「已收轮」显示。
const STATE_CLASS: Record<string, string> = {
  已完成: "rr-state-ok", 进行中: "rr-state-run", 已作废: "rr-state-void", 已收轮: "rr-state-closed", 用户已确认出片: "rr-state-go",
};

async function loadRun(dir: string): Promise<ReviewRun> {
  return fetchReviewChecklist<ReviewRun>(dir);
}

export function useRun(dir: string): { run: ReviewRun | null; error: string } {
  const [run, setRun] = useState<ReviewRun | null>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    let live = true; setRun(null); setError("");
    loadRun(dir).then(r => { if (live) setRun(r); }).catch(e => { if (live) setError(String(e)); });
    return () => { live = false; };
  }, [dir]);
  return { run, error };
}

export function State({ s }: { s: string }): JSX.Element {
  const d = displayState(s);
  return <span className={`rr-state ${STATE_CLASS[d] ?? ""}`}>{d}</span>;
}

/** 审查单页 / 问题清单页上的「修复页」入口（用户 2026-11-08：每一轮的审查结果链到修复页，两边关联）。 */
export function FixLinks({ dir, run, here }: { dir: string; run: ReviewRun; here: "run" | "issues" }): JSX.Element {
  return <p className="rr-fixbar">
    <Link className="rr-fixlink" to={reviewCorrectionsHref(dir)} title="基于这一轮审查修了哪些：方案、首帧前后、分镜 diff、下一轮复核">🛠 修复页</Link>
    {here === "run" ? <Link to={reviewIssuesHref(dir)}>问题清单</Link> : <Link to={reviewRunHref(dir)}>← 本轮审查单</Link>}
    {run.child ? <Link to={reviewRunHref(run.child)}>下一轮审查单 →</Link> : null}
  </p>;
}

function Verdict({ run }: { run: ReviewRun }): JSX.Element | null {
  const v = run.verdict;
  if (!v?.result && !v?.text) return null;
  const yes = v.result === "可出片";
  return <div className={`rr-verdict ${yes ? "rr-verdict-yes" : v.result ? "rr-verdict-no" : ""}`}>
    <b>结论：{v.result || "—"}</b>{v.text && v.text !== v.result ? <span>（{v.text}）</span> : null}
    {v.reasons?.length ? <ul>{v.reasons.map(r => <li key={r}>{r}</li>)}</ul> : null}
  </div>;
}

export function Counts({ f, empty = "无问题" }: { f?: Record<string, number>; empty?: string }): JSX.Element {
  const parts = SEVERITY_ORDER.filter(s => f?.[s]);
  return parts.length ? <span className="rr-findings">{parts.map(s => <span key={s} className={`rr-sev rr-sev-${s}`}>{s} {f![s]}</span>)}</span>
    : <span className="rr-sev rr-sev-ok">{empty}</span>;
}

const shortName = (by?: string): string => (by ?? "").split("/").slice(-1)[0] || (by ?? "");

/** 审查单页的一位审稿人：状态 + 代号，下一行是哪个独立 agent（执行方式 · 模型），重派的标第几次（follow-up 337）。 */
function AgentChip({ dir, item }: { dir: string; item: ReviewItem }): JSX.Element {
  const a = shownAttempt(item);
  const n = item.agents?.length ?? 0;
  const tip = [`${item.id} · ${itemStatusText(item)}${item.ticked_by ? ` · 打勾：${item.ticked_by}` : ""}`,
    ...attemptsNewestFirst(item).map(x => `第 ${x.n} 次派单：${agentShort(x)}`)].join(" / ");
  return <Link to={reviewItemHref(dir, item.id)} className={`rr-agent rr-agent-${item.status}`} title={tip}>
    <span className="rr-agent-id">{item.status === "done" ? "✓" : item.status === "failed" ? "!" : "○"} {item.ticked_by ? shortName(item.ticked_by) : item.id}</span>
    {a ? <span className="rr-agent-who">{agentShort(a)}{n > 1 ? <em className="rr-redo" title={`共派了 ${n} 次`}> ↻ 第 {a.n} 次派单</em> : null}</span>
      : <span className="rr-agent-who rr-muted">没有派单记录</span>}
  </Link>;
}

/** 同一剧的审查单摘要（/api/review-runs），用来判断这张是不是同范围里最新的一张；读不到就不显示。 */
function useDramaRuns(drama: string): ReviewRunSummary[] | null {
  const [runs, setRuns] = useState<ReviewRunSummary[] | null>(null);
  useEffect(() => {
    let live = true; setRuns(null);
    fetchReviewRuns().then(r => { if (live) setRuns((Array.isArray(r?.runs) ? r.runs : []).filter(x => x.drama === drama)); }).catch(() => { if (live) setRuns([]); });
    return () => { live = false; };
  }, [drama]);
  return runs;
}

/** 审查单页标题旁：最新的标「最新」；不是最新的给横幅链到最新一张（用户 2026-11-08：看不出哪个是最新的）。 */
function useLatest(dir: string, run: ReviewRun | null): { latest: boolean; newer?: ReviewRunSummary } {
  const runs = useDramaRuns(dir.replace(/\/reviews\/[^/]+$/, ""));
  if (!run || !runs?.length) return { latest: false };
  const me = runs.find(r => r.dir === dir) ?? { ...run, dir };
  const top = latestInScope(runs, me);
  if (!top) return { latest: false };
  return top.dir === dir ? { latest: true } : { latest: false, newer: top };
}

function RunView({ dir }: { dir: string }): JSX.Element {
  const { run, error } = useRun(dir);
  const fresh = useLatest(dir, run);
  if (error) return <p role="alert">读不到审查单：{error}</p>;
  if (!run) return <p role="status">加载审查单…</p>;
  const p = progress(run); const t = totals(run);
  const pct = p.total ? Math.round((p.done / p.total) * 100) : 0;
  const drama = dir.replace(/\/reviews\/[^/]+$/, "");
  const v5 = isV5Run(run);
  const judging = run.items.filter(i => i.status === "adjudicating").length;
  return <>
    <p className="rr-crumb"><Link to={reviewRunHref(drama)}>← 本剧全部审查单</Link></p>
    {fresh.newer ? <p className="rr-stale" role="note"><b>这不是最新的审查单</b> → 打开最新：<Link to={reviewRunHref(fresh.newer.dir)}>{fresh.newer.title}</Link></p> : null}
    <h1>{run.title} {fresh.latest ? <span className="rr-latest" title="同一集、同一阶段、同一组场里最新开的一张">最新</span> : null}<State s={run.state} /></h1>
    <p className="rr-sub">{run.stage_name} · 第 {run.loop ?? 1} / {run.max_loops ?? 3} 轮 · {run.scenes.join("、")} · {run.created_at.replace("T", " ")}
      {run.parent ? <> · <Link to={reviewRunHref(run.parent)}>← 上一轮</Link></> : null}
      {run.child ? <> · <Link to={reviewRunHref(run.child)}>下一轮 →</Link></> : null}</p>
    <div className="rr-progress" aria-label={`进度 ${p.done}/${p.total}`}>
      <div className="rr-bar"><span style={{ width: `${pct}%` }} /></div>
      <strong>{p.done} / {p.total}</strong> {v5 ? "项已审完（两位审稿人 + 对比 + 裁决）" : "位审稿人已打勾"}{judging ? <em className="rv-judging">{judging} 项待裁决</em> : null}{p.failed ? <em className="rr-bad">，{p.failed} {v5 ? "项" : "位"}失败</em> : null}
      <Counts f={t} empty="暂无问题" />
    </div>
    <p className={`rr-gate rr-gate-${STATE_CLASS[displayState(run.state)] ?? ""}`}>{stateText(run.state)}
      {run.result ? <> · <Link to={fileHref(`${dir}/${run.result}`)}>审查结果</Link></> : null}
      {run.confirm_quote ? <> · 你的原话：「{run.confirm_quote}」</> : null}</p>
    <Verdict run={run} />
    {needsShootConfirm(run) ? <p className="rr-mini rr-shoot-note">{SHOOT_CONFIRM_NOTE}</p> : null}
    <FixLinks dir={dir} run={run} here="run" />
    <IssueSummaryCard dir={dir} run={run} />
    <table className="rr-table">
      <thead><tr><th>审查大类</th><th>审了没</th><th>问题</th><th>谁审的（独立 agent）</th></tr></thead>
      <tbody>{lawRows(run).map(row => {
        const status = row.done === row.total ? "ok" : row.failed ? "bad" : "wait";
        return <tr key={row.law} data-law={row.law}>
          <th scope="row"><i className="rr-dot" style={{ background: row.color }} />
            <Link to={reviewLawHref(dir, row.law)} title="这一类是什么、想解决什么、分几个小类、怎么查，再看结果">{row.name}</Link></th>
          <td><span className={`rr-done rr-done-${status}`}>{status === "ok" ? "✓ 已审" : status === "bad" ? "! 有失败" : "未审完"}</span>
            <span className="rr-mini"> {row.done}/{row.total}</span>
            {row.items.some(i => i.status === "adjudicating") ? <span className="rv-judging">待裁决 {row.items.filter(i => i.status === "adjudicating").length}</span> : null}</td>
          <td>{row.done ? <Counts f={row.findings} /> : <span className="rr-mini">—</span>}</td>
          <td className="rr-reviewers">{row.items.map(i => isV5Item(i) ? <SlotChip key={i.id} dir={dir} item={i} /> : <AgentChip key={i.id} dir={dir} item={i} />)}</td>
        </tr>;
      })}</tbody>
    </table>
    <p className="rr-foot">{v5 ? "点大类名看这一类是什么、rubric 每维两位审稿人的分与裁决、怎么查和用了哪些模型；点审稿项看两位审稿人并排的分、对比与裁决。"
      : "点大类名看这一类是什么、想解决什么问题、分几个小类、怎么查和用了哪些 skill，再看合并的问题表；点审稿人看哪个 agent、发给它的指令、必查项和报告全文。"}<Link to={REVIEW_STRATEGY_PATH}>审查机制</Link></p>
  </>;
}

function ItemView({ dir, id }: { dir: string; id: string }): JSX.Element {
  const { run, error } = useRun(dir);
  const [report, setReport] = useState<string | null>(null);
  const item = run?.items.find(i => i.id === id);
  useEffect(() => {
    let live = true; setReport(null);
    if (item?.status === "done" || (item?.slots && item.reconciled_at)) fetchFile(`${dir}/${item.report}`).then(f => { if (live) setReport(f.content); }).catch(() => { if (live) setReport(""); });
    return () => { live = false; };
  }, [dir, item?.id, item?.status, item?.report, item?.reconciled_at]);
  if (error) return <p role="alert">读不到审查单：{error}</p>;
  if (!run) return <p role="status">加载…</p>;
  if (!item) return <p role="alert">这张审查单里没有审稿人 {id}。<Link to={reviewRunHref(dir)}>回审查单</Link></p>;
  if (isV5Item(item)) return <ItemView5 dir={dir} run={run} item={item} report={report} />;
  const siblings = run.items.filter(i => i.law === item.law);
  const res = item.must_result ?? {};
  const step = item.status === "done" ? (run.state === "进行中" ? 2 : run.state === "已完成" ? 3 : 5) : 1;   // 已收轮 / 已确认 → 最后一步
  return <>
    <p className="rr-crumb"><Link to={reviewRunHref(dir)}>← {run.title}</Link> · <Link to={reviewLawHref(dir, item.law)}>这一大类：{item.law_name}</Link></p>
    <h1><i className="rr-dot" style={{ background: item.color }} />{item.law_name} · <code>{item.id}</code>
      <span className={`rr-done rr-done-${item.status === "done" ? "ok" : item.status === "failed" ? "bad" : "wait"}`}>{itemStatusText(item)}</span></h1>
    {siblings.length > 1 ? <p className="rr-tabs">{siblings.map(s => s.id === item.id ? <strong key={s.id}>{s.id}</strong>
      : <Link key={s.id} to={reviewItemHref(dir, s.id)}>{s.id}</Link>)}</p> : null}
    <dl className="rr-facts">
      <dt>范围</dt><dd>{item.scope.join("、") || "全部"}{item.blind ? "（不看规格，只看成片）" : ""}</dd>
      <dt>打勾</dt><dd>{item.ticked_by ? <>{item.ticked_by} · {item.ticked_at?.replace("T", " ")}</> : "还没交报告"}</dd>
      <dt>结果</dt><dd>{item.status === "done" ? <><Counts f={item.findings} /> <span className="rr-mini">{item.rows ?? 0} 条</span>
        {mustFailed(item) ? <span className="rr-sev rr-sev-重出">必查 ✗ {mustFailed(item)}</span> : null}</> : "—"}</dd>
      {item.note ? <><dt>{item.status === "failed" ? "失败" : "备注"}</dt><dd className={item.status === "failed" ? "rr-bad" : ""}>{item.note}{item.failed_at ? `（${item.failed_at.replace("T", " ")}）` : ""}</dd></> : null}
    </dl>

    <AgentSection dir={dir} item={item} />

    <section className="rr-sec"><h2>怎么审</h2>
      <p>{item.checks}</p>
      {item.how ? <p className="rr-how">方法：{item.how}</p> : null}
      {item.must?.length ? <table className="rr-table rr-must-table"><thead><tr><th>必查项</th><th>内容</th><th>结果</th></tr></thead>
        <tbody>{item.must.map(m => <tr key={m.id}><th scope="row">{m.id}</th><td>{m.text}</td>
          <td className={res[m.id] === "✓" ? "rr-ok" : res[m.id] === "✗" ? "rr-bad" : "rr-mini"}>{res[m.id] ?? "未填"}</td></tr>)}</tbody></table>
        : <p className="rr-mini">这张单没有编号必查项（补登的旧审查）。</p>}
      <p className="rr-links"><Link to={fileHref(`${dir}/${item.prompt}`)}>审稿人任务书</Link> · <Link to={fileHref(`${dir}/BRIEF.md`)}>审稿说明</Link></p>
    </section>

    <section className="rr-sec"><h2>审查流程</h2>
      <ol className="rr-steps">{LOOP_STEPS.map((s, i) => <li key={s} className={i < step ? "rr-step-done" : i === step ? "rr-step-now" : ""}>{s}</li>)}</ol>
    </section>

    <section className="rr-sec"><h2>结果细节</h2>
      {item.status !== "done" ? <p className="rr-mini">审稿人交报告并打勾后在这里显示。</p>
        : report === null ? <p role="status">加载报告…</p>
        : report === "" ? <p role="alert">读不到报告 {item.report}</p>
        : <div className="markdown-view rr-report"><ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeSanitize]}>{report}</ReactMarkdown></div>}
      {item.status === "done" ? <p className="rr-links"><Link to={fileHref(`${dir}/${item.report}`)}>原始报告文件</Link></p> : null}
    </section>
  </>;
}

/** v5 审稿项详情：两位审稿人并排（执行方式、模型、打勾 / 凭日志代登记、报告、按 rubric 的分），再是对比与裁决、怎么审、对比报告全文。 */
function ItemView5({ dir, run, item, report }: { dir: string; run: ReviewRun; item: ReviewItem; report: string | null }): JSX.Element {
  const siblings = run.items.filter(i => i.law === item.law);
  const rubric = item.rubric ?? [];
  const cls = item.status === "done" ? "ok" : item.status === "failed" ? "bad" : "wait";
  const step = item.status !== "done" ? 0 : run.state === "进行中" ? 0 : 1;
  return <>
    <p className="rr-crumb"><Link to={reviewRunHref(dir)}>← {run.title}</Link> · <Link to={reviewLawHref(dir, item.law)}>这一大类：{item.law_name}</Link></p>
    <h1><i className="rr-dot" style={{ background: item.color }} />{item.law_name} · <code>{item.id}</code>
      <span className={`rr-done rr-done-${cls}`}>{itemStatusText(item)}</span></h1>
    {siblings.length > 1 ? <p className="rr-tabs">{siblings.map(s => s.id === item.id ? <strong key={s.id}>{s.id}</strong>
      : <Link key={s.id} to={reviewItemHref(dir, s.id)}>{s.id}</Link>)}</p> : null}
    <dl className="rr-facts">
      <dt>范围</dt><dd>{item.scope.join("、") || "全部"}{item.blind ? "（不看规格，只看成片）" : ""}</dd>
      <dt>打勾</dt><dd>{item.ticked_by_list?.length ? item.ticked_by_list.join(" + ") : "还没有审稿人交报告"}</dd>
      <dt>结果</dt><dd>{item.scores ? <><Counts f={item.findings} /> <span className="rr-mini">{item.rows ?? 0} 条（两位与裁决人的并集）</span>
        {mustFailed(item) ? <span className="rr-sev rr-sev-重出">≤1 分维度 {mustFailed(item)}</span> : null}</> : "—"}</dd>
    </dl>
    <SlotCards dir={dir} item={item} rubric={rubric} />
    <ReconcileSection dir={dir} item={item} />
    <section className="rr-sec"><h2>怎么审</h2>
      <p>{item.what || item.checks}</p>
      {item.how ? <p className="rr-how">方法：{item.how}</p> : null}
      {item.method?.length ? <><h4 className="rl-h3">审法</h4><ol className="rl-flow">{item.method.map(m => <li key={m}>{m}</li>)}</ol></> : null}
      {rubric.length ? <table className="rr-table rr-must-table"><thead><tr><th>维度</th><th>问题</th><th>最终分</th></tr></thead>
        <tbody>{rubric.map(d => { const f = item.final_scores?.[d.id] ?? item.scores?.[d.id]?.final;
          return <tr key={d.id}><th scope="row">{d.id} {d.name}</th><td>{d.question}</td>
            <td className={typeof f === "number" ? (f >= 2 ? "rr-ok" : "rr-bad") : "rr-mini"}>{typeof f === "number" ? f : "未定"}</td></tr>; })}</tbody></table> : null}
      <p className="rr-links">{Object.values(item.slots ?? {}).map(s => <span key={s.slot}><Link to={fileHref(`${dir}/${s.prompt}`)}>{s.slot} 位任务书</Link> · </span>)}
        <Link to={fileHref(`${dir}/BRIEF.md`)}>审稿说明</Link></p>
    </section>
    <section className="rr-sec"><h2>审查流程</h2>
      <ol className="rr-steps">{LOOP_V5.map((s, i) => <li key={s} className={i < step ? "rr-step-done" : i === step ? "rr-step-now" : ""}>{s}</li>)}</ol>
    </section>
    <section className="rr-sec"><h2>对比报告全文</h2>
      {!item.reconciled_at ? <p className="rr-mini">两位审稿人都打勾后生成 {item.report}。</p>
        : report === null ? <p role="status">加载报告…</p>
        : report === "" ? <p role="alert">读不到报告 {item.report}</p>
        : <div className="markdown-view rr-report"><ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeSanitize]}>{report}</ReactMarkdown></div>}
    </section>
  </>;
}

const at = (t?: string): string => (t ?? "").replace("T", " ");
/** 指令原文里的控制字符（例如路径里的 \a 被转义成了响铃符）换成可见的 ␇ 等符号：原样放进 <pre> 会让 Chrome 卡死，也看不出原文坏了。 */
const visibleControls = (text: string): string =>
  text.replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/g, c => String.fromCharCode(c.charCodeAt(0) === 0x7f ? 0x2421 : 0x2400 + c.charCodeAt(0)));

/** 详情页顶部「审稿 agent」：每次派单一张卡，最新的在前（follow-up 337）。 */
function AgentSection({ dir, item }: { dir: string; item: ReviewItem }): JSX.Element {
  const list = attemptsNewestFirst(item);
  const ticked = tickedAttempt(item);
  return <section className="rr-sec rr-agents" aria-label="审稿 agent"><h2>审稿 agent <span className="rr-count">{list.length ? `派了 ${list.length} 次` : ""}</span></h2>
    {!list.length ? <p className="rr-mini">没有派单记录（这张单派单时还没登记，只知道打勾署名：{item.ticked_by ?? "—"}）。
      登记方式：<code>python tools/review_run.py dispatch &lt;审查单&gt; {item.id} --runner … --model … --prompt-file …</code></p>
      : list.map((a, i) => <AgentCard key={a.n} dir={dir} item={item} a={a} latest={i === 0} ticked={a === ticked} />)}
  </section>;
}

function AgentCard({ dir, item, a, latest, ticked }: { dir: string; item: ReviewItem; a: AgentDispatch; latest: boolean; ticked: boolean }): JSX.Element {
  const [text, setText] = useState<string | null>(null);
  useEffect(() => {
    let live = true; setText(null);
    fetchFile(`${dir}/${a.prompt}`).then(f => { if (live) setText(f.content); }).catch(() => { if (live) setText(""); });
    return () => { live = false; };
  }, [dir, a.prompt]);
  const outcome = ticked ? <span className="rr-done rr-done-ok">打勾的是这次</span>
    : item.status === "done" || !latest ? <span className="rr-done rr-done-bad">这次没打勾</span>
    : <span className="rr-done rr-done-wait">{item.status === "failed" ? "失败，待重派" : "等它交报告"}</span>;
  return <article className={`rr-attempt${latest ? " rr-attempt-latest" : ""}`} data-attempt={a.n}>
    <h3><span className="rr-attempt-n">第 {a.n} 次派单</span> {agentShort(a)} {outcome}</h3>
    <dl className="rr-facts">
      <dt>执行方式</dt><dd>{a.runner}</dd>
      <dt>模型</dt><dd>{a.model}</dd>
      <dt>独立性</dt><dd>{a.context || "—"}</dd>
      <dt>派单时间</dt><dd>{at(a.at)}</dd>
      <dt>打勾</dt><dd>{ticked ? <>{item.ticked_by} · {at(item.ticked_at)}</> : "—"}</dd>
      {a.note ? <><dt>说明</dt><dd className="rr-attempt-note">{a.note}</dd></> : null}
    </dl>
    <h4>用了哪些规则 / skill</h4>
    {a.skills?.length ? <ul className="rr-skills">{a.skills.map(sk => {
      const p = skillPart(sk, dir, path => globalSourceUrl(`repo:${path}`));
      return <li key={sk}>{p.before}{p.path ? p.href ? <Link to={p.href}><code>{p.path}</code></Link> : <code>{p.path}</code> : null}{p.after}</li>;
    })}</ul> : <p className="rr-mini">没有登记。</p>}
    <details className="rr-instr" open={latest}>
      <summary>发给它的完整指令 <span className="rr-mini">{a.prompt}{text ? ` · ${text.length} 字` : ""}</span></summary>
      {text === null ? <p role="status">加载指令…</p> : text === "" ? <p role="alert">读不到指令文件 {a.prompt}</p> : <>
        <pre>{visibleControls(text)}</pre>
        {visibleControls(text) !== text ? <p className="rr-mini rr-bad">原文里有控制字符（显示成 ␇ 等符号），多半是 Windows 路径里的反斜杠被当成转义写坏了。</p> : null}
      </>}
      <p className="rr-links"><Link to={fileHref(`${dir}/${a.prompt}`)}>指令原文文件</Link></p>
    </details>
    <h4>它的回复{a.replied_at ? <span className="rr-mini"> · {at(a.replied_at)} 补登</span> : null}</h4>
    {a.reply ? <div className="markdown-view rr-reply"><ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeSanitize]}>{a.reply}</ReactMarkdown></div>
      : <p className="rr-mini">回复未存档，结果见下方报告。</p>}
  </article>;
}

function RunList({ target }: { target: string }): JSX.Element {
  const [runs, setRuns] = useState<{ dir: string; run: ReviewRun }[] | null>(null);
  const scope = listScope(target);
  useEffect(() => {
    let live = true; setRuns(null);
    fetchSubtree(scope.reviews, 1)
      .then(tree => Promise.all((tree.children ?? []).filter(c => c.type === "directory")
        .map(c => loadRun(c.path).then(run => ({ dir: c.path, run })).catch(() => null))))
      .then(list => { if (live) setRuns((list.filter(Boolean) as { dir: string; run: ReviewRun }[]).filter(r => !scope.episode || r.run.episode === scope.episode)); })
      .catch(() => { if (live) setRuns([]); });
    return () => { live = false; };
  }, [scope.reviews, scope.episode]);
  const drama = scope.reviews.replace(/\/reviews$/, "");
  return <>
    <p className="rr-crumb"><Link to={`/drama?drama=${encodeURIComponent(drama)}`}>← 回到剧页</Link> · <Link to={REVIEW_STRATEGY_PATH}>审查机制</Link></p>
    <h1>审查单 · {drama.split("/").slice(-1)[0]}{scope.episode ? ` · ${scope.episode}` : ""}</h1>
    <p className="rr-sub">文件夹：<Link to={fileHref(scope.reviews)}>{scope.reviews}/</Link>。按「集 → 范围（同一阶段、同一组场）」分组，新的在前；每个范围最上面一张是最新的，旧的标明被哪张取代。</p>
    {!runs ? <p role="status">加载…</p> : !runs.length ? <p className="rr-empty">还没有审查单。出片前生成：<code>python tools/review_run.py new &lt;集目录&gt; --stage pregen</code></p>
      : episodeScopes(runs.map(r => ({ ...r.run, dir: r.dir, run: r.run }))).map(e => <section key={e.episode} className="rr-ep">
        <h2>{e.episode}</h2>
        {e.scopes.map(s => <section key={s.key} className="rr-chain rr-scope">
          <h3>{s.label} · {s.stage} <span className="rr-count">{s.runs.length} 张</span></h3>
          <ol className="rr-runs">{s.runs.map(({ run: x, latest, supersededBy }) => {
            const p = progress(x.run);
            return <li key={x.dir} className={latest ? "rr-run-latest" : "rr-run-old"}>
              <div className="rr-run-main">
                {latest ? <span className="rr-latest">最新</span> : null}
                <Link to={reviewRunHref(x.dir)}>{x.title}</Link>
                <State s={x.state} /><Link className="rr-mini" to={reviewCorrectionsHref(x.dir)}>修复页</Link>
                <span className="rr-mini">{p.done}/{p.total} 已打勾</span>
                <Counts f={totals(x.run)} empty="暂无问题" />
              </div>
              {supersededBy ? <p className="rr-superseded">已被 <Link to={reviewRunHref(supersededBy.dir)}>{supersededBy.title}</Link> 取代</p> : null}
            </li>;
          })}</ol>
        </section>)}
      </section>)}
  </>;
}

export function ReviewRunPage(): JSX.Element {
  const [params] = useSearchParams();
  const path = (params.get("path") ?? "").replace(/\/+$/, "");
  return <div className="review-run">{!path ? <p role="alert">缺少 path 参数</p> : isRunDir(path) ? <RunView dir={path} /> : <RunList target={path} />}</div>;
}

export function ReviewItemPage(): JSX.Element {
  const [params] = useSearchParams();
  const path = (params.get("path") ?? "").replace(/\/+$/, "");
  const item = params.get("item") ?? "";
  return <div className="review-run">{!path || !item ? <p role="alert">缺少 path 或 item 参数</p> : <ItemView dir={path} id={item} />}</div>;
}

