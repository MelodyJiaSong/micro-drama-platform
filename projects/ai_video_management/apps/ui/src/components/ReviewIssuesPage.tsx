// 问题清单页 /review-run/issues?path=<审查单>（v5，用户 2026-11-08）：由双审评分（最终分 ≤1 的维度）与问题表推出的分级问题，
// 严重在前；每条：级别、类别·维度、镜头、问题、两位审稿人的证据（展开）、建议改动、成本、状态、选定方案 / 不改理由、历史。
// 只读：方案与状态由 `python tools/review_run.py fix <审查单> <I编号> …` 登记。
import { Fragment, useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { reviewLawHref } from "../lib/reviewLaw";
import { fileHref, reviewItemHref, reviewRunHref, type ReviewRun } from "../lib/reviewRun";
import {
  FIX_STATUS, LEVELS, LEVEL_NAME, STATUS_NAME, filterIssues, issueCounts, issueScenes, scoreClass, slotWho,
  type Issue, type IssueFilter,
} from "../lib/reviewV5";
import { CostBadge, LevelBadge, LoopBar, StatusBadge, useIssues } from "./ReviewIssues";
import { FixLinks, State, useRun } from "./ReviewRunPage";
import { Clip, Inline } from "./ReviewText";
import "./ReviewRunPage.css";
import "./ReviewV5.css";

const KEYS = ["level", "status", "category", "scene"] as const;
const at = (t?: string): string => (t ?? "").replace("T", " ");

export function ReviewIssuesPage(): JSX.Element {
  const [params] = useSearchParams();
  const path = (params.get("path") ?? "").replace(/\/+$/, "");
  return <div className="review-run review-issues">{!path ? <p role="alert">缺少 path 参数</p> : <IssuesView dir={path} />}</div>;
}

function IssuesView({ dir }: { dir: string }): JSX.Element {
  const { run, error } = useRun(dir);
  const doc = useIssues(dir);
  const [params, setParams] = useSearchParams();
  const filter: IssueFilter = Object.fromEntries(KEYS.map(k => [k, params.get(k) ?? ""]));
  const issues = useMemo(() => doc?.issues ?? [], [doc]);
  const shown = useMemo(() => filterIssues(issues, filter, run), [issues, filter.level, filter.status, filter.category, filter.scene, run]);
  const categories = useMemo(() => [...new Set(issues.map(i => i.category))], [issues]);
  const scenes = useMemo(() => [...new Set(issues.flatMap(i => issueScenes(i, run)))]
    .sort((a, b) => Number(a.slice(1)) - Number(b.slice(1))), [issues, run]);
  if (error) return <p role="alert">读不到审查单：{error}</p>;
  if (!run || doc === undefined) return <p role="status">加载问题清单…</p>;
  const set = (k: string, v: string): void => {
    const next = new URLSearchParams(params);
    if (v) next.set(k, v); else next.delete(k);
    setParams(next, { replace: true });
  };
  const c = issueCounts(issues);
  const any = KEYS.some(k => filter[k]);
  return <>
    <p className="rr-crumb"><Link to={reviewRunHref(dir)}>← {run.title}</Link></p>
    <h1>问题清单 <State s={run.state} /> <span className="rr-count">{c.total} 条</span></h1>
    <p className="rr-sub">{run.stage_name} · 第 {run.loop ?? 1} / {run.max_loops ?? 3} 轮{doc?.generated_at ? ` · 推出于 ${at(doc.generated_at)}` : ""}
      {doc ? <> · <Link to={fileHref(`${dir}/issues.md`)}>issues.md</Link> · <Link to={fileHref(`${dir}/issues.json`)}>issues.json</Link></> : null}</p>
    <FixLinks dir={dir} run={run} here="issues" />
    <LoopBar dir={dir} run={run} issues={doc ? issues : null} />
    {!doc ? <p className="rr-empty">这张单还没有问题清单。全部审完（v5 还要对比、裁决完）后运行 <code>python tools/review_run.py issues {dir}</code>。</p> : <>
      <div className="rv-filters" role="group" aria-label="筛选">
        <Select label="级别" value={filter.level ?? ""} onChange={v => set("level", v)}
          options={LEVELS.map(l => [l, `${LEVEL_NAME[l]}（${c.level[l] ?? 0}）`])} />
        <Select label="状态" value={filter.status ?? ""} onChange={v => set("status", v)}
          options={FIX_STATUS.map(s => [s, `${STATUS_NAME[s]}（${c.status[s] ?? 0}）`])} />
        <Select label="类别" value={filter.category ?? ""} onChange={v => set("category", v)} options={categories.map(x => [x, x])} />
        <Select label="场" value={filter.scene ?? ""} onChange={v => set("scene", v)} options={scenes.map(x => [x, x])} />
        <span className="rr-mini">显示 {shown.length} / {c.total}</span>
        {any ? <button type="button" className="rv-clear" onClick={() => setParams(new URLSearchParams({ path: dir }), { replace: true })}>清除筛选</button> : null}
      </div>
      {!shown.length ? <p className="rr-mini">{c.total ? "没有符合筛选的问题。" : "没有问题。"}</p> : <IssueTable dir={dir} run={run} issues={shown} />}
    </>}
  </>;
}

function Select({ label, value, onChange, options }: { label: string; value: string; onChange: (v: string) => void; options: string[][] }): JSX.Element {
  return <label className="rv-select">{label}
    <select value={value} onChange={e => onChange(e.target.value)} aria-label={label}>
      <option value="">全部</option>
      {options.map(([v, t]) => <option key={v} value={v}>{t}</option>)}
    </select></label>;
}

function IssueTable({ dir, run, issues }: { dir: string; run: ReviewRun; issues: Issue[] }): JSX.Element {
  const [open, setOpen] = useState<Record<string, boolean>>({});
  return <div className="rl-scroll"><table className="rr-table rv-issues">
    <thead><tr><th>编号</th><th>级别</th><th>类别 · 维度</th><th>镜头</th><th>问题</th><th>建议改动</th><th>成本</th><th>状态</th><th>方案 / 不改理由</th><th /></tr></thead>
    <tbody>{issues.map(i => {
      const isOpen = Boolean(open[i.id]);
      return <Fragment key={i.id}>
        <tr data-issue={i.id} data-level={i.level} data-status={i.status} className={isOpen ? "rv-open" : ""}>
          <th scope="row" className="rv-id">{i.id}</th>
          <td><LevelBadge level={i.level} /></td>
          <td className="rv-cat"><Link to={reviewLawHref(dir, i.law)}>{i.category}</Link><span className="rv-dim">{i.dimension}</span>
            <Link className="rr-mini" to={reviewItemHref(dir, i.item)}>{i.item}</Link></td>
          <td className="rv-shots">{i.shots.length ? i.shots.join("、") : <span className="rr-mini">{issueScenes(i, run).join("、") || "—"}</span>}</td>
          <td className="rv-problem"><Clip text={i.problem} max={90} />
            {i.scores ? <span className="rv-scores" title="a 分 / b 分 → 最终">
              <span className={`rv-score ${scoreClass(i.scores.a)}`}>a {i.scores.a}</span>
              <span className={`rv-score ${scoreClass(i.scores.b)}`}>b {i.scores.b}</span>→
              <span className={`rv-score ${scoreClass(i.scores.final)}`}>{i.scores.final}</span></span> : null}</td>
          <td className="rv-fix">{i.fix ? <Clip text={i.fix} max={70} /> : <span className="rr-mini">—</span>}</td>
          <td><CostBadge cost={i.cost} /></td>
          <td><StatusBadge status={i.status} /></td>
          <td className="rv-solution">{i.solution ? <Clip text={i.solution} max={70} /> : <span className="rr-mini">—</span>}
            {i.reason ? <span className="rv-reason">理由：{i.reason}</span> : null}
            {i.status === "wontfix" && !i.reason ? <span className="rr-bad rv-reason">不改但没写理由，仍挡着下一轮</span> : null}</td>
          <td><button type="button" className="rl-more" aria-expanded={isOpen} onClick={() => setOpen(o => ({ ...o, [i.id]: !o[i.id] }))}>
            {isOpen ? "收起" : `证据 ${i.evidence.length}`}</button></td>
        </tr>
        {isOpen ? <tr className="rv-detail" data-detail={i.id}><td colSpan={10}><IssueDetail run={run} issue={i} /></td></tr> : null}
      </Fragment>;
    })}</tbody>
  </table></div>;
}

/** 证据前缀「a（0 分）」「b（1 分）」「裁决（…）」换成是哪位审稿人。 */
function evidenceWho(run: ReviewRun, issue: Issue, e: string): { who: string; text: string } {
  const m = /^(a|b|裁决)（(\d) 分）：/.exec(e);
  if (!m) return { who: "", text: e };
  const it = run.items.find(x => x.id === issue.item);
  const slot = m[1] === "裁决" ? it?.judge : it?.slots?.[m[1]];
  const who = `${m[1] === "裁决" ? "裁决人" : `${m[1]} 位`}${slot ? ` · ${slotWho(slot)}` : ""} · ${m[2]} 分`;
  return { who, text: e.slice(m[0].length) };
}

function IssueDetail({ run, issue }: { run: ReviewRun; issue: Issue }): JSX.Element {
  return <div className="rv-detail-grid">
    <div><h4>证据（两位审稿人与裁决人）</h4>
      <ul className="rv-evidence">{issue.evidence.filter(Boolean).map((e, n) => {
        const x = evidenceWho(run, issue, e);
        return <li key={n}>{x.who ? <b>{x.who}：</b> : null}<Inline text={x.text} /></li>;
      })}</ul>
      <p className="rr-mini">来源：{issue.sources.join("、") || "—"}{issue.severity ? ` · 问题表严重度：${issue.severity}` : ""}</p>
      {issue.rows?.length ? <details className="rv-rows"><summary>问题表原行 {issue.rows.length}</summary>
        <pre>{issue.rows.join("\n")}</pre></details> : null}
    </div>
    <div><h4>历史</h4>
      {issue.history?.length ? <ol className="rv-history">{issue.history.map((h, n) => <li key={n}>
        <span className="rr-mini">{at(h.at)}</span> <StatusBadge status={h.status} /> {h.solution}{h.reason ? `（理由：${h.reason}）` : ""}</li>)}</ol>
        : <p className="rr-mini">还没有登记方案。登记：<code>python tools/review_run.py fix &lt;审查单&gt; {issue.id} --solution "…" --status planned|implemented|wontfix</code></p>}
    </div>
  </div>;
}
