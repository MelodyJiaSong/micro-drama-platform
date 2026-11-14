import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { fetchFile, fetchRepoSource } from "../api";
import { globalSourceUrl } from "../lib/globalWorkflow";
import {
  PARTITION_TEXT, ROSTER_PATH, agentTally, lawItems, lawMust, mergeFindings, mustMatrix, plainCell, reviewLawHref, severityTotals,
  type Finding, type Roster, type RosterLaw,
} from "../lib/reviewLaw";
import {
  LOOP_STEPS, agentShort, byLaw, fileHref, itemStatusText, mustFailed, reviewItemHref, reviewRunHref, tickedAttempt,
  type ReviewItem, type ReviewRun,
} from "../lib/reviewRun";
import { Counts, useRun } from "./ReviewRunPage";
import { Clip, Inline } from "./ReviewText";
import { useIssues } from "./ReviewIssues";
import { RubricTable } from "./ReviewV5";
import { isV5Item, lawReviewers, reviewIssuesHref, slotMark, slotTally, slotWho } from "../lib/reviewV5";
import "./ReviewRunPage.css";
import "./ReviewLawPage.css";

// 审查大类页（follow-up 338）：先讲这一类是什么、想解决什么问题、分几个小类、怎么查、用了哪些 skill，最后给本轮结果。

function useRoster(): Roster | null | undefined {
  // undefined＝加载中；null＝名册读不到（页面退回审查单里的快照）。
  const [roster, setRoster] = useState<Roster | null | undefined>(undefined);
  useEffect(() => {
    let live = true;
    fetchRepoSource(ROSTER_PATH).then(f => { if (live) setRoster(JSON.parse(f.content) as Roster); }).catch(() => { if (live) setRoster(null); });
    return () => { live = false; };
  }, []);
  return roster;
}

function useReports(dir: string, items: ReviewItem[]): { item: string; text: string }[] | null {
  const done = items.filter(i => i.status === "done");
  const key = done.map(i => `${i.id}:${i.report}`).join("|");
  const [reports, setReports] = useState<{ item: string; text: string }[] | null>(null);
  useEffect(() => {
    let live = true; setReports(null);
    Promise.all(done.map(i => fetchFile(`${dir}/${i.report}`).then(f => ({ item: i.id, text: f.content })).catch(() => ({ item: i.id, text: "" }))))
      .then(list => { if (live) setReports(list); });
    return () => { live = false; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [dir, key]);
  return reports;
}


const mark = (v: string): string => v === "✓" ? "rr-ok" : v === "✗" ? "rr-bad" : "rr-mini";

export function ReviewLawPage(): JSX.Element {
  const [params] = useSearchParams();
  const path = (params.get("path") ?? "").replace(/\/+$/, "");
  const law = params.get("law") ?? "";
  return <div className="review-run review-law">{!path || !law ? <p role="alert">缺少 path 或 law 参数</p> : <LawView dir={path} law={law} />}</div>;
}

function LawView({ dir, law }: { dir: string; law: string }): JSX.Element {
  const { run, error } = useRun(dir);
  const roster = useRoster();
  const laws = roster === undefined ? undefined : roster?.laws ?? null;
  const items = run ? lawItems(run, law) : [];
  const reports = useReports(dir, items);
  if (error) return <p role="alert">读不到审查单：{error}</p>;
  if (!run || laws === undefined) return <p role="status">加载…</p>;
  if (!items.length) return <p role="alert">这张审查单里没有大类 {law}。<Link to={reviewRunHref(dir)}>回审查单</Link></p>;
  const r = laws?.[law];
  const first = items[0];
  const name = r?.name ?? first.law_name;
  const done = items.filter(i => i.status === "done").length;
  const v5 = items.some(isV5Item);
  return <>
    <p className="rr-crumb"><Link to={reviewRunHref(dir)}>← {run.title}</Link></p>
    <h1><i className="rr-dot" style={{ background: r?.color ?? first.color }} />{name} <code className="rl-key">{law}</code>
      <span className={`rr-done rr-done-${done === items.length ? "ok" : items.some(i => i.status === "failed") ? "bad" : "wait"}`}>{done}/{items.length} 已审</span></h1>
    <p className="rr-tabs rl-tabs">{byLaw(run).map(([n, list]) => list[0].law === law ? <strong key={n}>{n}</strong>
      : <Link key={n} to={reviewLawHref(dir, list[0].law)}>{n}</Link>)}</p>
    {!r ? <p className="rr-gate">名册 <code>{ROSTER_PATH}</code> {laws ? `里没有 laws.${law} 的说明` : "读不到"}，下面只按这张审查单里的快照显示。</p> : null}

    <section className="rr-sec rl-sec" data-sec="what"><h2>这一类是什么</h2>
      <p className="rl-lead">{r?.what ?? first.checks}</p>
    </section>

    <section className="rr-sec rl-sec" data-sec="problem"><h2>想解决什么问题</h2>
      {r?.problem ? <p>{r.problem}</p> : <p className="rr-mini">名册里还没有写。</p>}
      {r?.examples?.length ? <><h3 className="rl-h3">真实踩过的例子</h3><ul className="rl-examples">{r.examples.map(e => <li key={e}>{e}</li>)}</ul></> : null}
    </section>

    {v5 ? <RubricSection dir={dir} run={run} items={items} r={r} /> : <MustSection run={run} items={items} r={r} />}
    <FlowSection run={run} items={items} r={r} />
    <SkillSection dir={dir} law={law} run={run} items={items} r={r} adjudicator={roster?.adjudicator} />
    <ResultSection dir={dir} items={items} reports={reports} category={name} />
  </>;
}

function MustSection({ run, items, r }: { run: ReviewRun; items: ReviewItem[]; r?: RosterLaw }): JSX.Element {
  const { must, fromRun } = lawMust(items, r);
  const base = must.filter(m => m.id !== "R");
  const rows = mustMatrix(items, must);
  const loop = run.loop ?? 1;
  return <section className="rr-sec rl-sec" data-sec="must"><h2>细分成几个小类</h2>
    {!must.length ? <p className="rr-mini">这一类没有编号小类。</p> : <>
      <p>共 <strong>{base.length}</strong> 个小类{loop >= 2 ? <>；这是第 {loop} 轮，每位审稿人多一项 <b>R</b>「复核上一轮」</> : <>；第 2 轮起每位审稿人会多一项 <b>R</b>「复核上一轮」</>}。</p>
      {!fromRun ? <p className="rr-mini">这张是补登的旧审查单，没有逐项结果；小类按现行名册列出。</p> : null}
      <table className="rr-table rl-must">
        <thead><tr><th>小类</th><th>查什么</th>{fromRun ? items.map(i => <th key={i.id} className="rl-col" title={i.scope.join("、")}>{i.id}</th>) : null}</tr></thead>
        <tbody>{rows.map(m => <tr key={m.id} className={m.failed ? "rl-must-fail" : ""}><th scope="row">{m.id}</th><td>{m.text}</td>
          {fromRun ? m.cells.map((c, n) => <td key={items[n].id} className={`rl-col ${mark(c)}`}>{c}</td>) : null}</tr>)}</tbody>
      </table></>}
  </section>;
}

/** v5：小类＝rubric 维度，一维一行，每个审稿项三列（Claude a 分 / Codex b 分 / 最终），悬停或展开看证据，标分歧与抽查。 */
function RubricSection({ dir, run, items, r }: { dir: string; run: ReviewRun; items: ReviewItem[]; r?: RosterLaw }): JSX.Element {
  const dims = items.find(i => i.rubric?.length)?.rubric ?? r?.rubric ?? [];
  const disputes = items.reduce((n, i) => n + (i.disputes?.length ?? 0), 0);
  const audits = items.reduce((n, i) => n + (i.audits?.length ?? 0), 0);
  const judging = items.filter(i => i.status === "adjudicating").length;
  const loop = run.loop ?? 1;
  return <section className="rr-sec rl-sec" data-sec="must"><h2>细分成几个小类 <span className="rr-count">评分维度（rubric）</span></h2>
    {!dims.length ? <p className="rr-mini">这一类没有评分维度。</p> : <>
      <p>共 <strong>{dims.length}</strong> 个维度，每维两位审稿人各打 0–3 分{items.length > 1 ? `，分 ${items.length} 段审（${items.map(i => i.id).join("、")}）` : ""}；
        分歧 <strong>{disputes}</strong> 处、抽查 <strong>{audits}</strong> 处{judging ? <>，<span className="rv-judging">{judging} 项待裁决</span></> : null}。
        {loop >= 2 ? <>这是第 {loop} 轮，每位审稿人另写一行 <b>R</b>「复核上一轮」。</> : null}</p>
      <RubricTable dir={dir} run={run} items={items} roster={r?.rubric} /></>}
  </section>;
}

const stripMd = (s: string): string => s.replace(/\*\*/g, "").replace(/`/g, "");

function FlowSection({ run, items, r }: { run: ReviewRun; items: ReviewItem[]; r?: RosterLaw }): JSX.Element {
  const first = items[0];
  const blind = r?.blind ?? first.blind;
  const part = r?.partition ? PARTITION_TEXT[r.partition] : "";
  const method = r?.method ?? first.method ?? [];
  const v5 = items.some(isV5Item);
  const reviewers = lawReviewers(items, r?.reviewers);
  return <section className="rr-sec rl-sec" data-sec="flow"><h2>检查流程</h2>
    <ol className="rl-flow">
      <li><b>分工</b>：{part ? `${part}。` : ""}本轮审 {run.scenes.join("、")}，共 {items.length} 位：{items.map(i => `${i.id}（${i.scope.join("、") || "全部"}）`).join("、")}。</li>
      <li><b>{blind ? "盲审" : "对照材料"}</b>：{blind ? <>不读分镜、故事稿与规格，只看给它的材料。{r?.blind_note ? <>名册给审稿人的原话：「{stripMd(r.blind_note)}」</> : null}</> : "不是盲审，可以读本集的分镜、规格与 prompt 对照着查。"}
        每位审稿人都在全新的上下文里审，看不到作者会话和别的审稿报告。</li>
      <li><b>要查什么</b>：<Inline text={r?.checks ?? first.checks} /></li>
      <li><b>怎么查</b>：<Inline text={r?.how ?? (first.how || "—")} /></li>
      {method.length ? <li><b>审法</b>（名册 method）：<ol className="rl-method">{method.map(m => <li key={m}><Inline text={m} /></li>)}</ol></li> : null}
      {v5 ? <li><b>双审、对比、裁决</b>：两位审稿人（{reviewers.map(x => `${x.slot} 位 ${slotWho(x)}`).join("、")}）各拿自己的任务书独立审，互不读对方报告，
        按 rubric 每维 0–3 打分（≥2 要证据、1 要在问题表里有行、0 要写原因），自己运行 <code>review_run.py tick --slot a|b</code> 打勾（Codex 沙箱跑不了 python 时由调用方凭运行日志代登记）。
        两位都勾后自动对比：分数差 ≥2 或一高一低是<b>分歧</b>，两人都 ≥2 的维度随机<b>抽查</b> 2 维，交裁决人定最终分；全部完成后推出问题清单。</li>
        : <li><b>交报告、打勾</b>：报告逐条写每个小类 ✓ / ✗，问题表按严重度排（重出 / 可剪 / 记录 / 存疑）；审稿人自己运行 <code>review_run.py tick</code> 打勾，作者不能代勾。</li>}
      {v5 ? <li><b>循环</b>：本轮双审 → 由评分推出问题（严重 / 主要 / 待核实 / 记录）→ 逐条定方案 → 实施 → 下一轮复核（最多 {run.max_loops ?? 3} 轮）；
        严重与主要都实施或写明理由不改后才能开下一轮。本单是第 {run.loop ?? 1} / {run.max_loops ?? 3} 轮。</li> : <li><b>循环</b>：出审查单 → 独立审 → 打勾 → 便宜的改动直接改 → 下一轮（最多 {run.max_loops ?? 3} 轮）→ 收轮记结论（出片时你在对话里确认）。本单是第 {run.loop ?? 1} / {run.max_loops ?? 3} 轮。
        <details className="rl-loop"><summary>六步细节</summary><ol>{LOOP_STEPS.map(s => <li key={s}>{s}</li>)}</ol></details></li>}
    </ol>
  </section>;
}

/** 旧单只有打勾署名「模型/代号」：按模型合并计数。 */
const signers = (items: ReviewItem[]): string => {
  const n = new Map<string, number>();
  for (const i of items) if (i.ticked_by) { const k = i.ticked_by.split("/")[0]; n.set(k, (n.get(k) ?? 0) + 1); }
  return [...n.entries()].map(([k, c]) => `${k} ×${c}`).join("，");
};

function SkillSection({ dir, law, run, items, r, adjudicator }: { dir: string; law: string; run: ReviewRun; items: ReviewItem[]; r?: RosterLaw;
  adjudicator?: { runner: string; model: string } }): JSX.Element {
  if (items.some(isV5Item)) return <SkillSection5 dir={dir} law={law} run={run} items={items} r={r} adjudicator={adjudicator} />;
  const tally = agentTally(items);
  const prefer = r?.prefer_model;
  const off = prefer ? items.map(i => tickedAttempt(i)).filter(a => a && !agentShort(a).toLowerCase().includes(prefer.toLowerCase())) : [];
  return <section className="rr-sec rl-sec" data-sec="skills"><h2>用了哪些 skill / 规则</h2>
    <dl className="rr-facts">
      <dt>审查机制</dt><dd>{r?.mechanisms?.length ? <ul className="rl-plain">{r.mechanisms.map(m => <li key={m}>{m}</li>)}</ul> : "—"}</dd>
      <dt>照着做的文件</dt><dd><ul className="rl-plain">
        <li>名册 <Link to={globalSourceUrl(`repo:${ROSTER_PATH}`)}><code>review_roster.json</code></Link> · 法则 <code>{law}</code>（是什么、小类、怎么查）</li>
        <li>审稿说明 <Link to={fileHref(`${dir}/BRIEF.md`)}><code>BRIEF.md</code></Link>（材料、规则、报告格式）</li>
        <li>任务书 {items.map((i, n) => <span key={i.id}>{n ? "、" : ""}<Link to={fileHref(`${dir}/${i.prompt}`)}><code>{i.prompt}</code></Link></span>)}（范围、必查项、打勾命令）</li>
      </ul></dd>
      {prefer ? <><dt>指定模型</dt><dd>尽量换模型审：<code>{prefer}</code>（和作者、和别的审稿人不是同一个模型）
        {off.length ? <span className="rr-bad">；本轮打勾的是 {off.map(a => agentShort(a!)).join("、")}，没用上 {prefer}</span> : null}</dd></> : null}
      <dt>实际跑的 agent</dt><dd>{tally.length ? tally.map((t, n) => <span key={t.who}>{n ? "，" : ""}{t.who} ×{t.count}
        <span className="rr-mini">（{t.ticked === 0 ? "没打勾" : t.ticked === t.count ? "打勾" : `打勾 ${t.ticked}/${t.count}`}）</span></span>)
        : <span className="rr-mini">没有派单记录（旧单），只知道打勾署名：{signers(items) || "—"}</span>}</dd>
    </dl>
  </section>;
}

/** v5：为什么用这两个模型、两位审稿人与裁决人、照着做的文件、实际跑的 agent（按位）。 */
function SkillSection5({ dir, law, run, items, r, adjudicator }: { dir: string; law: string; run: ReviewRun; items: ReviewItem[]; r?: RosterLaw;
  adjudicator?: { runner: string; model: string } }): JSX.Element {
  const reviewers = lawReviewers(items, r?.reviewers);
  const judge = run.adjudicator ?? adjudicator;
  const tally = slotTally(items);
  const off = items.flatMap(i => Object.values(i.slots ?? {}).filter(s => s.by && s.by.split("/")[0] !== s.model).map(s => `${i.id} ${s.slot} 位署名 ${s.by}`));
  return <section className="rr-sec rl-sec" data-sec="skills"><h2>用了哪些 skill / 规则</h2>
    <dl className="rr-facts">
      <dt>审稿人</dt><dd><ul className="rl-plain">{reviewers.map(x => <li key={x.slot}><b>{x.slot} 位</b> {slotWho(x)} <span className="rr-mini">（{x.runner} · {x.model}）</span></li>)}
        {judge ? <li><b>裁决人</b> {slotWho(judge)} <span className="rr-mini">（只裁分歧与抽查的维度，不能是这一项的审稿人）</span></li> : null}</ul></dd>
      <dt>为什么用这两个模型</dt><dd>{r?.model_why ?? items.find(i => i.model_why)?.model_why ?? <span className="rr-mini">名册里还没有写。</span>}</dd>
      <dt>审查机制</dt><dd>{r?.mechanisms?.length ? <ul className="rl-plain">{r.mechanisms.map(m => <li key={m}>{m}</li>)}</ul> : "—"}</dd>
      <dt>照着做的文件</dt><dd><ul className="rl-plain">
        <li>名册 <Link to={globalSourceUrl(`repo:${ROSTER_PATH}`)}><code>review_roster.json</code></Link> · 法则 <code>{law}</code>（是什么、rubric、审法、审稿人）</li>
        <li>审稿说明 <Link to={fileHref(`${dir}/BRIEF.md`)}><code>BRIEF.md</code></Link>（材料、评分规则、报告格式）</li>
        <li>任务书 {items.flatMap(i => Object.values(i.slots ?? {}).map(s => s.prompt).concat(i.judge ? [i.judge.prompt] : []))
          .map((p, n) => <span key={p}>{n ? "、" : ""}<Link to={fileHref(`${dir}/${p}`)}><code>{p}</code></Link></span>)}（每位审稿人一份，裁决人另一份）</li>
      </ul></dd>
      <dt>实际跑的 agent</dt><dd>{tally.length ? tally.map((t, n) => <span key={`${t.slot}|${t.who}`}>{n ? "，" : ""}{t.slot === "裁决" ? "裁决" : `${t.slot} 位`} {t.who} ×{t.count}
        <span className="rr-mini">（{t.ticked === 0 ? "没打勾" : t.ticked === t.count ? "打勾" : `打勾 ${t.ticked}/${t.count}`}）</span></span>)
        : <span className="rr-mini">还没有派单或打勾记录</span>}
        {off.length ? <span className="rr-bad">；署名和名册排的模型不一致：{off.join("、")}</span> : null}</dd>
    </dl>
  </section>;
}

function ResultSection({ dir, items, reports, category }: { dir: string; items: ReviewItem[]; reports: { item: string; text: string }[] | null; category: string }): JSX.Element {
  const t = severityTotals(items);
  const rows = items.reduce((n, i) => n + (i.rows ?? 0), 0);
  const findings = reports ? mergeFindings(reports) : null;
  const missing = (reports ?? []).filter(x => !x.text).map(x => x.item);
  const issues = useIssues(dir);
  const catIssues = (issues?.issues ?? []).filter(i => i.category === category);
  return <section className="rr-sec rl-sec" data-sec="result"><h2>检查结果</h2>
    <p className="rl-totals"><Counts f={t} empty={items.some(i => i.status === "done") ? "无问题" : "还没有结果"} /> <span className="rr-mini">共 {rows} 条</span></p>
    <div className="rl-cards">{items.map(i => <ReviewerCard key={i.id} dir={dir} item={i} />)}</div>
    {issues?.issues.length ? <p className="rv-summary-note">问题清单里这一类有 <b>{catIssues.length}</b> 条（严重 {catIssues.filter(i => i.level === "critical").length}、未处理 {catIssues.filter(i => i.status === "open").length}）：<Link to={reviewIssuesHref(dir, { category })}>看这一类的问题清单 →</Link></p> : null}
    <h3 className="rl-h3">合并问题表 <span className="rr-mini">各审稿人报告里「严重度」表合在一起，按重出、可剪、记录、存疑排</span></h3>
    {findings === null ? <p role="status">加载报告…</p>
      : !findings.length ? <p className="rr-mini">{items.some(i => i.status === "done") ? "报告里没有问题行。" : "审稿人交报告并打勾后在这里显示。"}</p>
      : <FindingsTable rows={findings} />}
    {missing.length ? <p role="alert" className="rr-bad">读不到报告：{missing.join("、")}</p> : null}
  </section>;
}

function ReviewerCard({ dir, item }: { dir: string; item: ReviewItem }): JSX.Element {
  if (isV5Item(item)) return <ReviewerCard5 dir={dir} item={item} />;
  const a = tickedAttempt(item);
  const bad = mustFailed(item);
  return <Link to={reviewItemHref(dir, item.id)} className={`rl-card rr-agent-${item.status}`} data-item={item.id}>
    <span className="rl-card-head"><b>{item.id}</b> <span className={`rr-done rr-done-${item.status === "done" ? "ok" : item.status === "failed" ? "bad" : "wait"}`}>{itemStatusText(item)}</span></span>
    <span className="rr-mini">范围 {item.scope.join("、") || "全部"}</span>
    <span className="rr-mini">{item.status !== "done" ? (item.status === "failed" ? "失败，待重派" : "还没打勾") : a ? `打勾：${agentShort(a)}` : `打勾：${item.ticked_by ?? "—"}`}</span>
    <span>{item.status === "done" ? <Counts f={item.findings} /> : <span className="rr-mini">—</span>}
      {bad ? <span className="rr-sev rr-sev-重出">小类 ✗ {bad}</span> : null}</span>
    <span className="rl-card-go">看详情 →</span>
  </Link>;
}

function ReviewerCard5({ dir, item }: { dir: string; item: ReviewItem }): JSX.Element {
  const low = Object.values(item.final_scores ?? {}).filter(f => typeof f === "number" && f <= 1).length;
  return <Link to={reviewItemHref(dir, item.id)} className={`rl-card rr-agent-${item.status}`} data-item={item.id}>
    <span className="rl-card-head"><b>{item.id}</b> <span className={`rr-done rr-done-${item.status === "done" ? "ok" : item.status === "failed" ? "bad" : "wait"}`}>{itemStatusText(item)}</span></span>
    <span className="rr-mini">范围 {item.scope.join("、") || "全部"}</span>
    {Object.values(item.slots ?? {}).map(s => <span key={s.slot} className={`rv-slotline rv-slot-${s.status}`}><b>{s.slot}</b> {slotMark(s)} {slotWho(s)}{s.attested ? " · 代登记" : ""}</span>)}
    {item.judge ? <span className={`rv-slotline rv-slot-${item.judge.status}`}><b>裁</b> {item.judge.status === "done" ? "✓" : "⚖"} {slotWho(item.judge)} · {item.judge.dims.join("、")}</span> : null}
    <span>{item.status === "done" ? <Counts f={item.findings} /> : <span className="rr-mini">—</span>}
      {low ? <span className="rr-sev rr-sev-重出">≤1 分 {low} 维</span> : null}</span>
    <span className="rl-card-go">看双审详情 →</span>
  </Link>;
}

function FindingsTable({ rows }: { rows: Finding[] }): JSX.Element {
  return <div className="rl-scroll"><table className="rr-table rl-findings">
    <thead><tr><th>镜头</th><th>严重度</th><th>子类</th><th>证据</th><th>建议改动</th><th>审稿人</th></tr></thead>
    <tbody>{rows.map(f => <tr key={`${f.item}-${f.order}`} data-sev={f.severity}>
      <td className="rl-shot">{f.shot}{f.time ? <span className="rr-mini rl-time" title={f.time}>{f.time.length > 16 ? `${f.time.slice(0, 16)}…` : f.time}</span> : null}</td>
      <td className="rl-sev"><span className={`rr-sev rr-sev-${f.severity}`} title={f.raw !== f.severity ? `原文：${f.raw}` : undefined}>{f.severity}</span></td>
      <td className="rl-sub">{plainCell(f.sub)}</td>
      <td className="rl-ev"><Clip text={f.evidence} /></td>
      <td className="rl-fix"><Clip text={f.fix} max={60} /></td>
      <td className="rr-mini">{f.item}</td>
    </tr>)}</tbody>
  </table></div>;
}
