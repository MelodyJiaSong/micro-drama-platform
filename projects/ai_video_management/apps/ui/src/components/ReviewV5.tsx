// v5 双审的页面部件（用户 2026-11-08）：审查单页的双审标签、大类页的 rubric 评分表、审稿项详情页的两位审稿人并排卡与对比 / 裁决。
// 没有 slots 的 v2 单不用这些，照旧渲染。
import { Fragment, useState } from "react";
import { Link } from "react-router-dom";
import { fileHref, reviewItemHref, type ReviewItem, type ReviewRun, type ReviewSlot, type RubricDim } from "../lib/reviewRun";
import {
  SCORE_TEXT, dimCell, itemMark, rubricRows, scoreClass, slotMark, slotStatusText, slotWho, slotsOf, type DimCell,
} from "../lib/reviewV5";
import { Inline } from "./ReviewText";
import "./ReviewV5.css";

const at = (t?: string): string => (t ?? "").replace("T", " ");
const ITEM_STATE: Record<string, string> = { done: "已审", failed: "失败", adjudicating: "待裁决", pending: "未审" };
/** 项的状态；还没完时标两位交了几位（「交 1/2」）。 */
const itemState = (item: ReviewItem): string => {
  const slots = slotsOf(item); const n = slots.filter(s => s.status === "done").length;
  return item.status === "pending" && n ? `交 ${n}/${slots.length}` : ITEM_STATE[item.status] ?? item.status;
};
/** 本地文件链接：仓库内 ai_videos/ 下的走文件页，其余（临时目录里的日志）只显示路径。 */
const maybeFile = (path: string, label?: string): JSX.Element =>
  path.startsWith("ai_videos/") ? <Link to={fileHref(path)}><code>{label ?? path}</code></Link> : <code>{label ?? path}</code>;

/** 审查单页的一项：代号 + 状态（含待裁决），下面每位审稿人一行：位、模型、打勾状态；有裁决人再加一行。 */
export function SlotChip({ dir, item }: { dir: string; item: ReviewItem }): JSX.Element {
  const slots = slotsOf(item);
  const tip = [`${item.id} · ${itemState(item)}`,
    ...slots.map(s => `${s.slot} 位 ${slotWho(s)}：${slotStatusText(s)}${s.by ? `（${s.by}）` : ""}${s.note ? ` · ${s.note}` : ""}`),
    ...(item.judge ? [`裁决 ${slotWho(item.judge)}：${item.judge.status === "done" ? "已裁决" : "待裁决"}（${item.judge.dims.join("、")}）`] : [])].join(" / ");
  return <Link to={reviewItemHref(dir, item.id)} className={`rr-agent rr-agent-${item.status} rv-chip5`} title={tip} data-item={item.id}>
    <span className="rr-agent-id">{itemMark(item)} {item.id} <em className={`rv-istate rv-istate-${item.status}`}>{itemState(item)}</em></span>
    {slots.map(s => <span key={s.slot} className={`rv-slotline rv-slot-${s.status}`} data-slot={s.slot}>
      <b>{s.slot}</b> {slotMark(s)} {slotWho(s)}{s.attested ? <em className="rv-attest" title={`凭运行日志代登记：${s.attested.log}`}> 代登记</em> : null}</span>)}
    {item.judge ? <span className={`rv-slotline rv-slot-${item.judge.status}`} data-slot="judge"><b>裁</b> {item.judge.status === "done" ? "✓" : "⚖"} {slotWho(item.judge)}</span> : null}
  </Link>;
}

/** 一格分数：0–3 着色，悬停看证据。 */
export function Score({ n, ev, label }: { n?: number | null; ev?: string; label?: string }): JSX.Element {
  const has = typeof n === "number";
  return <span className={`rv-score ${scoreClass(n)}`} title={[label, has ? `${n} 分：${SCORE_TEXT[n!] ?? ""}` : "还没有分", ev].filter(Boolean).join(" · ")}>
    {has ? n : "—"}</span>;
}

const verdictBadge = (c: DimCell): JSX.Element | null =>
  c.verdict === "分歧" ? <em className="rv-verdict rv-verdict-dispute" title="两位分数差 ≥2，或一人 ≤1 一人 ≥2：交裁决人">分歧</em>
    : c.verdict === "抽查" ? <em className="rv-verdict rv-verdict-audit" title="两人都 ≥2：裁决人随机抽查证据">抽查</em> : null;

/** 大类页「细分成几个小类」的 v5 版：一维一行，每个审稿项三列 Claude a 分 / Codex b 分 / 最终；点「证据」展开两位的证据与裁决。 */
export function RubricTable({ dir, run, items, roster }: { dir: string; run: ReviewRun; items: ReviewItem[]; roster?: RubricDim[] }): JSX.Element {
  const rows = rubricRows(items, roster);
  const [open, setOpen] = useState<Record<string, boolean>>({});
  const scale = run.scoring?.scale ?? SCORE_TEXT;
  const multi = items.length > 1;
  const slotHead = (i: ReviewItem, k: "a" | "b"): string => { const s = i.slots?.[k]; return s ? `${s.runner === "codex" ? "Codex" : s.runner === "claude" ? "Claude" : s.runner} ${k} 分` : `${k} 分`; };
  const anyR = items.some(i => slotsOf(i).some(s => s.r_check));
  const hasB = items.some(i => Boolean(i.slots?.b));   // Claude 单审（follow-up 065）没有 b 位：不画空列
  const per = hasB ? 3 : 2;
  return <>
    <p className="rv-legend">评分 0–3：{[0, 1, 2, 3].map(n => <span key={n}><span className={`rv-score ${scoreClass(n)}`}>{n}</span> {scale[String(n)] ?? SCORE_TEXT[n]} </span>)}
      · <em className="rv-verdict rv-verdict-dispute">分歧</em> 交裁决 · <em className="rv-verdict rv-verdict-audit">抽查</em> 裁决人复核证据</p>
    <div className="rl-scroll"><table className="rr-table rv-rubric">
      <thead>
        {multi ? <tr><th colSpan={2} />{items.map(i => <th key={i.id} colSpan={per} className="rv-grp" title={i.scope.join("、")}>
          <Link to={reviewItemHref(dir, i.id)} className="rv-grp-id">{i.id}</Link>
          <span className="rr-mini"> {i.scope.join("、")}</span></th>)}<th /></tr> : null}
        <tr><th>维度</th><th>查什么</th>{items.map(i => <Fragment key={i.id}>
          <th className="rv-col" title={i.slots?.a?.model}>{slotHead(i, "a")}</th>
          {hasB ? <th className="rv-col" title={i.slots?.b?.model}>{slotHead(i, "b")}</th> : null}
          <th className="rv-col rv-col-final">最终</th></Fragment>)}<th /></tr>
      </thead>
      <tbody>{rows.map(r => {
        const isOpen = Boolean(open[r.dim.id]);
        return <Fragment key={r.dim.id}>
          <tr data-dim={r.dim.id} className={[r.low ? "rv-low" : "", r.disputed ? "rv-disputed" : ""].filter(Boolean).join(" ")}>
            <th scope="row">{r.dim.id} <span className="rv-dimname">{r.dim.name}</span>{r.dim.critical ? <em className="rv-crit" title="名册标为关键维度：≤1 分即严重">关键</em> : null}</th>
            <td className="rv-q">{r.dim.question}</td>
            {r.cells.map(c => <Fragment key={c.item}>
              <td className="rv-col"><Score n={c.a} ev={c.a_ev} label={`${c.item} a 位`} /></td>
              {hasB ? <td className="rv-col"><Score n={c.b} ev={c.b_ev} label={`${c.item} b 位`} /></td> : null}
              <td className="rv-col rv-col-final">{c.awaitingJudge ? <span className="rv-score rv-sna" title="待裁决">?</span>
                : <Score n={c.final} ev={c.judge_reason ? `裁决：${c.judge_reason}` : undefined} label={`${c.item} 最终`} />}{verdictBadge(c)}</td>
            </Fragment>)}
            <td><button type="button" className="rl-more" aria-expanded={isOpen} onClick={() => setOpen(o => ({ ...o, [r.dim.id]: !o[r.dim.id] }))}>
              {isOpen ? "收起" : "证据"}</button></td>
          </tr>
          {isOpen ? <tr className="rv-detail" data-detail={r.dim.id}><td colSpan={3 + items.length * per}>
            {r.cells.map(c => <div key={c.item} className="rv-ev-block">{multi ? <b className="rv-ev-item">{c.item}</b> : null}
              <p><span className="rv-ev-who">a 位 · {slotHead(items.find(i => i.id === c.item)!, "a")}</span> {c.a ?? "—"} 分：{c.a_ev ? <Inline text={c.a_ev} /> : <span className="rr-mini">还没交</span>}</p>
              {hasB ? <p><span className="rv-ev-who">b 位 · {slotHead(items.find(i => i.id === c.item)!, "b")}</span> {c.b ?? "—"} 分：{c.b_ev ? <Inline text={c.b_ev} /> : <span className="rr-mini">还没交</span>}</p> : null}
              {c.verdict ? <p><span className="rv-ev-who">裁决</span> {c.verdict}{c.awaitingJudge ? "，等裁决人"
                : c.judge_reason ? <>，最终 {c.final} 分：<Inline text={c.judge_reason} /></> : typeof c.final === "number" ? `，取 ${c.final} 分` : ""}</p> : null}
            </div>)}
          </td></tr> : null}
        </Fragment>;
      })}</tbody>
    </table></div>
    {anyR ? <p className="rr-mini">R 复核上一轮：{items.map(i => `${i.id} ${slotsOf(i).map(s => `${s.slot} ${s.r_check ?? "—"}`).join(" / ")}`).join("；")}</p> : null}
  </>;
}

/** 详情页：两位审稿人并排。 */
export function SlotCards({ dir, item, rubric }: { dir: string; item: ReviewItem; rubric: RubricDim[] }): JSX.Element {
  return <section className="rr-sec rv-slots-sec" aria-label="双审"><h2>双审 <span className="rr-count">两位独立审稿人，互不读对方报告</span></h2>
    <div className="rv-slots">{slotsOf(item).map(s => <SlotCard key={s.slot} dir={dir} s={s} rubric={rubric} />)}</div>
  </section>;
}

function SlotCard({ dir, s, rubric }: { dir: string; s: ReviewSlot; rubric: RubricDim[] }): JSX.Element {
  const attempts = [...(s.agents ?? [])].sort((a, b) => b.n - a.n);
  return <article className={`rv-slot rv-slot-card-${s.status}`} data-slot={s.slot}>
    <h3><span className="rv-slot-key">{s.slot} 位</span> {slotWho(s)}
      <span className={`rr-done rr-done-${s.status === "done" ? "ok" : s.status === "failed" ? "bad" : "wait"}`}>{slotMark(s)} {slotStatusText(s)}</span></h3>
    <dl className="rr-facts">
      <dt>执行方式</dt><dd>{s.runner}</dd>
      <dt>模型</dt><dd>{s.model}</dd>
      <dt>打勾</dt><dd>{s.by ? <>{s.by} · {at(s.ticked_at)}</> : s.status === "failed" ? <span className="rr-bad">失败：{s.note ?? "—"}{s.failed_at ? `（${at(s.failed_at)}）` : ""}</span> : "还没交报告"}</dd>
      <dt>登记方式</dt><dd>{s.status !== "done" ? "—" : s.attested ? <>凭运行日志代登记（Codex 沙箱跑不了 python）：日志 {maybeFile(s.attested.log)}
        {s.attested.copy ? <> · 副本 {maybeFile(s.attested.copy)}</> : null}</> : "审稿人自己运行 tick"}</dd>
      <dt>文件</dt><dd><Link to={fileHref(`${dir}/${s.prompt}`)}>任务书</Link>
        {s.status === "done" ? <> · <Link to={fileHref(`${dir}/${s.report}`)}>报告</Link></> : null}</dd>
      <dt>派单</dt><dd>{attempts.length ? attempts.map((a, n) => <span key={a.n}>{n ? "；" : ""}第 {a.n} 次 {slotWho(a)} · {at(a.at)} ·{" "}
        <Link to={fileHref(`${dir}/${a.prompt}`)}>指令</Link>{a.note ? <span className="rr-mini">（{a.note}）</span> : null}</span>)
        : <span className="rr-mini">没有派单记录</span>}</dd>
      {s.status === "done" && s.findings ? <><dt>问题</dt><dd>{Object.entries(s.findings).filter(([, v]) => v).map(([k, v]) => `${k} ${v}`).join("，") || "无问题"}
        <span className="rr-mini"> · {s.rows ?? 0} 条</span></dd></> : null}
      {s.r_check ? <><dt>R 复核</dt><dd className={s.r_check === "✓" ? "rr-ok" : "rr-bad"}>{s.r_check}</dd></> : null}
    </dl>
    {s.scores ? <table className="rr-table rv-slot-scores"><tbody>{rubric.map(d => {
      const v = s.scores?.[d.id];
      return <tr key={d.id} data-dim={d.id}><th scope="row">{d.id} <span className="rv-dimname">{d.name}</span></th>
        <td className="rv-col"><Score n={v?.score} ev={v?.evidence} /></td><td className="rv-ev">{v?.evidence ? <Inline text={v.evidence} /> : "—"}</td></tr>;
    })}</tbody></table> : <p className="rr-mini">交报告后在这里显示它按 rubric 打的分。</p>}
  </article>;
}

/** 详情页：两位都勾后的对比，与裁决人的裁决。 */
export function ReconcileSection({ dir, item }: { dir: string; item: ReviewItem }): JSX.Element {
  const j = item.judge;
  const dims = item.rubric ?? [];
  return <section className="rr-sec" aria-label="对比与裁决"><h2>对比与裁决
    {item.disputes?.length ? <span className="rv-verdict rv-verdict-dispute">分歧 {item.disputes.length}</span> : null}
    {item.audits?.length ? <span className="rv-verdict rv-verdict-audit">抽查 {item.audits.length}</span> : null}</h2>
    {!item.scores ? <p className="rr-mini">两位审稿人都交报告并打勾后自动对比（分数差 ≥2 或一高一低是分歧，两人都 ≥2 的维度抽 2 维复核），分歧与抽查交裁决人。</p> : <>
      <dl className="rr-facts">
        <dt>裁决人</dt><dd>{j ? <>{slotWho(j)} · {j.status === "done" ? <>已裁决（{j.by} · {at(j.at)}）</> : j.status === "failed" ? <span className="rr-bad">失败：{j.note ?? "—"}</span> : "待裁决"}
          {" · "}要裁的维度：{j.dims.join("、")} · <Link to={fileHref(`${dir}/${j.prompt}`)}>裁决任务书</Link>
          {j.status === "done" ? <> · <Link to={fileHref(`${dir}/${j.report}`)}>裁决报告</Link></> : null}</> : "不需要（无分歧、无可抽查维度）"}</dd>
        <dt>对比文件</dt><dd><Link to={fileHref(`${dir}/${item.report}`)}>{item.report}</Link>{item.reconciled_at ? <span className="rr-mini"> · {at(item.reconciled_at)}</span> : null}</dd>
      </dl>
      <div className="rl-scroll"><table className="rr-table rv-reconcile">
        <thead><tr><th>维度</th><th className="rv-col">a 分</th><th>a 证据</th>{item.slots?.b ? <><th className="rv-col">b 分</th><th>b 证据</th></> : null}<th>判定</th><th className="rv-col">最终</th><th>裁决理由</th></tr></thead>
        <tbody>{(dims.length ? dims.map(d => d.id) : Object.keys(item.scores)).map(d => {
          const c = dimCell(item, d); const v = item.scores![d];
          if (!v) return null;
          return <tr key={d} data-dim={d} className={v.verdict === "分歧" ? "rv-disputed" : ""}>
            <th scope="row">{d} <span className="rv-dimname">{v.name}</span></th>
            <td className="rv-col"><Score n={v.a} ev={v.a_ev} /></td><td className="rv-ev"><Inline text={v.a_ev} /></td>
            {item.slots?.b ? <><td className="rv-col"><Score n={v.b} ev={v.b_ev} /></td><td className="rv-ev"><Inline text={v.b_ev} /></td></> : null}
            <td>{verdictBadge(c) ?? <span className="rr-mini">一致</span>}</td>
            <td className="rv-col">{c.awaitingJudge ? <span className="rv-score rv-sna">?</span> : <Score n={c.final} />}</td>
            <td className="rv-ev">{v.judge_reason ? <Inline text={v.judge_reason} /> : <span className="rr-mini">{c.awaitingJudge ? "待裁决" : "—"}</span>}</td>
          </tr>;
        })}</tbody>
      </table></div></>}
  </section>;
}
