// 问题清单的共用部件（v5，用户 2026-11-08）：读 issues.json、级别 / 状态标签、审查单页顶部的摘要卡、循环位置条。
// 「有了多重 review，我们应该看到 based on rubric 两个得分结果，根据结果 derive 出问题，哪些是 critical 的，然后应该怎么解决，
//  然后 implement solution，然后继续 loop 回一开始继续检查」——这里把这条循环摆在页面上。
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchFile } from "../api";
import { fileHref, reviewRunHref, type ReviewRun } from "../lib/reviewRun";
import {
  FIX_STATUS, ISSUES_JSON, LEVELS, LEVEL_NAME, LOOP_V5, STATUS_NAME, issueCounts, loopPosition, reviewIssuesHref,
  type Issue, type IssuesDoc,
} from "../lib/reviewV5";
import "./ReviewV5.css";

/** undefined＝加载中；null＝这张单还没有 issues.json。 */
export function useIssues(dir: string): IssuesDoc | null | undefined {
  const [doc, setDoc] = useState<IssuesDoc | null | undefined>(undefined);
  useEffect(() => {
    let live = true; setDoc(undefined);
    fetchFile(`${dir}/${ISSUES_JSON}`)
      .then(f => { if (live) { const d = JSON.parse(f.content) as IssuesDoc; setDoc(Array.isArray(d?.issues) ? d : null); } })
      .catch(() => { if (live) setDoc(null); });
    return () => { live = false; };
  }, [dir]);
  return doc;
}

export const LevelBadge = ({ level }: { level: string }): JSX.Element =>
  <span className={`rv-level rv-level-${level}`} title={level}>{LEVEL_NAME[level] ?? level}</span>;
export const StatusBadge = ({ status }: { status: string }): JSX.Element =>
  <span className={`rv-status rv-status-${status}`} title={status}>{STATUS_NAME[status] ?? status}</span>;
export const CostBadge = ({ cost }: { cost: string }): JSX.Element =>
  cost ? <span className={`rv-cost ${cost === "要积分" ? "rv-cost-paid" : "rv-cost-cheap"}`}>{cost}</span> : <span className="rr-mini">—</span>;

/** 本轮 → 问题 → 方案 → 实施 → 下一轮复核，标出现在到哪一步、什么挡着下一轮。 */
export function LoopBar({ dir, run, issues }: { dir: string; run: ReviewRun; issues: Issue[] | null }): JSX.Element {
  const pos = loopPosition(run, issues);
  const crit = pos.blockers.filter(i => i.level === "critical").length;
  return <div className="rv-loopbox" aria-label="审查循环">
    <ol className="rv-loop">{LOOP_V5.map((s, n) => <li key={s} data-step={n}
      className={n < pos.step ? "rv-loop-done" : n === pos.step ? "rv-loop-now" : ""}>{s}</li>)}</ol>
    <p className={`rv-loop-note${pos.blockers.length ? " rv-loop-blocked" : ""}`}>{pos.note}
      {pos.blockers.length ? <> 其中严重 <b>{crit}</b>、主要 <b>{pos.blockers.length - crit}</b>。
        <Link to={reviewIssuesHref(dir, { status: "open" })}>看未处理的</Link></> : null}
      {run.child ? <> <Link to={reviewRunHref(run.child)}>下一轮 →</Link></> : null}</p>
  </div>;
}

/** 审查单页顶部的摘要卡：有 issues.json 才显示。 */
export function IssueSummaryCard({ dir, run }: { dir: string; run: ReviewRun }): JSX.Element | null {
  const doc = useIssues(dir);
  if (!doc) return null;
  const c = issueCounts(doc.issues);
  const pos = loopPosition(run, doc.issues);
  return <section className="rv-summary" aria-label="问题清单">
    <h2><Link to={reviewIssuesHref(dir)}>问题清单</Link> <span className="rr-count">{c.total} 条</span>
      <span className="rv-summary-step">现在：{LOOP_V5[pos.step]}</span></h2>
    <div className="rv-summary-row"><span className="rv-summary-k">级别</span>
      {LEVELS.map(l => <Link key={l} to={reviewIssuesHref(dir, { level: l })} className="rv-chip"><LevelBadge level={l} /> {c.level[l] ?? 0}</Link>)}</div>
    <div className="rv-summary-row"><span className="rv-summary-k">状态</span>
      {FIX_STATUS.map(s => <Link key={s} to={reviewIssuesHref(dir, { status: s })} className="rv-chip"><StatusBadge status={s} /> {c.status[s] ?? 0}</Link>)}</div>
    <p className={c.blocking ? "rv-loop-blocked rv-summary-note" : "rv-summary-note"}>
      {c.blocking ? <>挡着下一轮：严重 / 主要还有 <b>{c.blocking}</b> 个未实施（或不改但没写理由）。</> : "严重与主要问题都已处理，可以开下一轮复核。"}
      {" "}<Link to={reviewIssuesHref(dir)}>看问题清单 →</Link>
      {" · "}<Link to={fileHref(`${dir}/issues.md`)}>issues.md</Link></p>
  </section>;
}
