// 修复页 /review-run/corrections?path=<审查单>（用户 2026-11-08）：基于这一轮审查，我们修了哪些、怎么修的、首帧前后、分镜文字改了什么、
// 下一轮复核过没有。和审查单页、问题清单页双向链接。数据是 `review_run.py corrections` 写的 corrections.json，只读。
import { useEffect, useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { fetchFile, mediaUrl } from "../api";
import { fileHref, reviewRunHref } from "../lib/reviewRun";
import {
  CORRECTIONS_JSON, LOOP_CORR, VERIFY, correctionsCommand, correctionsStep, countBy, diffKind, groupCorrections, orphanCorrections,
  reviewCorrectionsHref, verifyClass,
  type Correction, type CorrectionFilter, type CorrectionsDoc, type FrameVersion, type ShotCorrection, type SpecField,
} from "../lib/reviewCorrections";
import { FIX_STATUS, LEVELS, LEVEL_NAME, STATUS_NAME, reviewIssuesHref } from "../lib/reviewV5";
import { LevelBadge, StatusBadge } from "./ReviewIssues";
import { State, useRun } from "./ReviewRunPage";
import { Clip, Inline } from "./ReviewText";
import { ZoomableImage } from "./ZoomableImage";
import "./ReviewRunPage.css";
import "./ReviewV5.css";
import "./ReviewCorrectionsPage.css";

const KEYS = ["level", "status", "verify", "scene"] as const;
const at = (t?: string): string => (t ?? "").replace("T", " ");

/** undefined＝加载中；null＝还没生成 corrections.json。 */
export function useCorrections(dir: string): CorrectionsDoc | null | undefined {
  const [doc, setDoc] = useState<CorrectionsDoc | null | undefined>(undefined);
  useEffect(() => {
    let live = true; setDoc(undefined);
    fetchFile(`${dir}/${CORRECTIONS_JSON}`)
      .then(f => { if (live) { const d = JSON.parse(f.content) as CorrectionsDoc; setDoc(Array.isArray(d?.corrections) ? d : null); } })
      .catch(() => { if (live) setDoc(null); });
    return () => { live = false; };
  }, [dir]);
  return doc;
}

export function ReviewCorrectionsPage(): JSX.Element {
  const [params] = useSearchParams();
  const path = (params.get("path") ?? "").replace(/\/+$/, "");
  return <div className="review-run review-corrections">{!path ? <p role="alert">缺少 path 参数</p> : <CorrectionsView dir={path} />}</div>;
}

function CorrectionsView({ dir }: { dir: string }): JSX.Element {
  const { run, error } = useRun(dir);
  const doc = useCorrections(dir);
  const [params, setParams] = useSearchParams();
  const filter: CorrectionFilter = Object.fromEntries(KEYS.map(k => [k, params.get(k) ?? ""]));
  const groups = useMemo(() => (doc ? groupCorrections(doc, filter) : []), [doc, filter.level, filter.status, filter.verify, filter.scene]);
  const orphans = useMemo(() => (doc ? orphanCorrections(doc, filter) : []), [doc, filter.level, filter.status, filter.verify]);
  if (error) return <p role="alert">读不到审查单：{error}</p>;
  if (!run || doc === undefined) return <p role="status">加载修复记录…</p>;
  const set = (k: string, v: string): void => {
    const next = new URLSearchParams(params);
    if (v) next.set(k, v); else next.delete(k);
    setParams(next, { replace: true });
  };
  const child = doc?.child || run.child || "";
  const step = correctionsStep(doc);
  const shown = groups.reduce((n, g) => n + g.shots.length, 0);
  return <>
    <p className="rr-crumb rc-links">
      <Link to={reviewRunHref(dir)}>← 本轮审查单</Link>
      <Link to={reviewIssuesHref(dir)}>← 问题清单</Link>
      {run.parent ? <Link to={reviewCorrectionsHref(run.parent)}>← 上一轮修复页</Link> : null}
      {child ? <Link to={reviewRunHref(child)}>→ 下一轮审查单</Link> : <span className="rr-mini">下一轮还没开</span>}
    </p>
    <h1>修复页 · {run.title} <State s={run.state} /></h1>
    <p className="rr-sub">基于这一轮审查，修了哪些、怎么修的、首帧与分镜前后、下一轮复核结果。
      {doc?.generated_at ? ` 生成于 ${at(doc.generated_at)}` : ""}
      {doc ? <> · <Link to={fileHref(`${dir}/corrections.md`)}>corrections.md</Link> · <Link to={fileHref(`${dir}/${CORRECTIONS_JSON}`)}>corrections.json</Link></> : null}</p>
    <div className="rv-loopbox" aria-label="修复循环">
      <ol className="rv-loop">{LOOP_CORR.map((s, n) => <li key={s} data-step={n}
        className={n < step ? "rv-loop-done" : n === step ? "rv-loop-now" : ""}>
        {n === 0 ? <Link to={reviewRunHref(dir)}>{s}</Link> : n === 2 && child ? <Link to={reviewRunHref(child)}>{s}</Link> : s}</li>)}</ol>
      <p className="rv-loop-note">{!doc ? "还没生成修复记录。"
        : child ? `下一轮 ${child.split("/").pop()}（${doc.child_state || "—"}）的审稿人复核了这里的方案，结果见每条的复核标签。`
        : "下一轮还没开：方案都待复核。"}</p>
    </div>
    {!doc ? <div className="rr-empty rc-empty"><p>还没生成修复记录。生成：</p><pre><code>{correctionsCommand(dir)}</code></pre>
      <p className="rr-mini">修复方案用 <code>review_run.py fix &lt;审查单&gt; &lt;I编号&gt; --solution … --status implemented --file &lt;改了的文件&gt;</code> 登记；重跑 corrections 会刷新这一页。</p></div>
      : <Body dir={dir} doc={doc} filter={filter} set={set} groups={groups} orphans={orphans} shown={shown}
        clear={() => setParams(new URLSearchParams({ path: dir }), { replace: true })} />}
  </>;
}

function Body({ dir, doc, filter, set, groups, orphans, shown, clear }: {
  dir: string; doc: CorrectionsDoc; filter: CorrectionFilter; set: (k: string, v: string) => void;
  groups: ReturnType<typeof groupCorrections>; orphans: Correction[]; shown: number; clear: () => void;
}): JSX.Element {
  const c = countBy(doc.corrections);
  const s = doc.summary;
  const scenes = [...new Set([...doc.shots.map(x => x.scene), ...doc.corrections.flatMap(x => x.scenes)])];
  const any = KEYS.some(k => filter[k]);
  return <>
    <section className="rv-summary rc-summary" aria-label="修复汇总">
      <h2>修复汇总 <span className="rr-count">有方案 {s.corrections} / {s.issues} 条问题</span></h2>
      <div className="rv-summary-row"><span className="rv-summary-k">级别</span>
        {LEVELS.map(l => <button type="button" key={l} className="rv-chip" onClick={() => set("level", filter.level === l ? "" : l)} aria-pressed={filter.level === l}>
          <LevelBadge level={l} /> {c.level[l] ?? 0}</button>)}</div>
      <div className="rv-summary-row"><span className="rv-summary-k">状态</span>
        {FIX_STATUS.filter(x => x !== "open").map(x => <button type="button" key={x} className="rv-chip" onClick={() => set("status", filter.status === x ? "" : x)} aria-pressed={filter.status === x}>
          <StatusBadge status={x} /> {c.status[x] ?? 0}</button>)}</div>
      <div className="rv-summary-row"><span className="rv-summary-k">复核</span>
        {VERIFY.map(v => <button type="button" key={v} className="rv-chip" onClick={() => set("verify", filter.verify === v ? "" : v)} aria-pressed={filter.verify === v}>
          <span className={`rc-v ${verifyClass(v)}`}>{v}</span> {c.verify[v] ?? 0}</button>)}</div>
      <p className="rv-summary-note">首帧换了 <b>{s.frames_changed}</b> 镜，分镜文字改了 <b>{s.specs_changed}</b> 镜（共 {s.shots} 镜）。
        问题来源：{doc.issues_source}{doc.changes_md && doc.issues_source !== "issues.json" ? <>，方案配自 <Link to={fileHref(doc.changes_md)}>下一轮 changes.md</Link></> : null}
        {doc.has_snapshot ? "" : "；这张单没有快照，修复前的首帧按审查开始时已在的那版（含 _r1 等归档）、分镜按审查材料里的 spec.md"}。</p>
    </section>
    <div className="rv-filters" role="group" aria-label="筛选">
      <Select label="级别" value={filter.level ?? ""} onChange={v => set("level", v)} options={LEVELS.map(l => [l, `${LEVEL_NAME[l]}（${c.level[l] ?? 0}）`])} />
      <Select label="状态" value={filter.status ?? ""} onChange={v => set("status", v)} options={FIX_STATUS.map(x => [x, `${STATUS_NAME[x]}（${c.status[x] ?? 0}）`])} />
      <Select label="复核" value={filter.verify ?? ""} onChange={v => set("verify", v)} options={VERIFY.map(v => [v, `${v}（${c.verify[v] ?? 0}）`])} />
      <Select label="场" value={filter.scene ?? ""} onChange={v => set("scene", v)} options={scenes.map(x => [x, x])} />
      <span className="rr-mini">显示 {shown} 镜</span>
      {any ? <button type="button" className="rv-clear" onClick={clear}>清除筛选</button> : null}
    </div>
    {!groups.length && !orphans.length ? <p className="rr-mini">{doc.corrections.length || doc.shots.some(x => x.frame.changed || x.spec.changed) ? "没有符合筛选的修复。" : "这一轮还没有登记方案，首帧和分镜也都没改。"}</p> : null}
    {groups.map(g => <section key={g.scene} className="rc-scene" data-scene={g.scene}>
      <h2>{g.scene} <span className="rr-count">{g.shots.length} 镜{g.loose.length ? ` · 整场 ${g.loose.length} 条` : ""}</span></h2>
      {g.shots.map(({ shot, corrections }) => <ShotCard key={shot.key} dir={dir} shot={shot} corrections={corrections} />)}
      {g.loose.length ? <article className="rc-shot rc-loose" data-shot={`${g.scene}_整场`}>
        <h3>{g.scene} 整场 / 没指明镜头</h3>
        <div className="rc-issues">{g.loose.map(x => <CorrectionRow key={x.id} dir={dir} c={x} />)}</div>
      </article> : null}
    </section>)}
    {orphans.length ? <section className="rc-scene"><h2>其他</h2><article className="rc-shot">
      <div className="rc-issues">{orphans.map(x => <CorrectionRow key={x.id} dir={dir} c={x} />)}</div></article></section> : null}
  </>;
}

function Select({ label, value, onChange, options }: { label: string; value: string; onChange: (v: string) => void; options: string[][] }): JSX.Element {
  return <label className="rv-select">{label}
    <select value={value} onChange={e => onChange(e.target.value)} aria-label={label}>
      <option value="">全部</option>
      {options.map(([v, t]) => <option key={v} value={v}>{t}</option>)}
    </select></label>;
}

function Frame({ v, side }: { v: FrameVersion | null; side: string }): JSX.Element {
  const [broken, setBroken] = useState(false);
  return <figure className="rc-frame" data-side={side}>
    <figcaption><b>{side}</b>{v ? <span className="rr-mini"> · {v.label} · {at(v.mtime)}</span> : null}</figcaption>
    {!v ? <div className="rc-noimg">没有这一版</div>
      : broken ? <div className="rc-noimg">读不到图 <code>{v.path}</code></div>
      : <ZoomableImage src={mediaUrl(v.path, v.mtime_ms)} alt={`${side} ${v.path}`} loading="lazy" onError={() => setBroken(true)} />}
    {v?.how ? <span className="rr-mini rc-how">{v.how}</span> : null}
  </figure>;
}

function ShotCard({ dir, shot, corrections }: { dir: string; shot: ShotCorrection; corrections: Correction[] }): JSX.Element {
  const f = shot.frame;
  const pending = corrections.some(c => c.frame_pending?.includes(shot.key));
  return <article className="rc-shot" data-shot={shot.key}>
    <h3>{shot.key}
      {f.changed ? <span className="rc-tag rc-tag-frame">首帧换了</span> : f.before ? <span className="rc-tag">首帧没换</span> : null}
      {shot.spec.changed ? <span className="rc-tag rc-tag-spec">分镜改了 {shot.spec.fields.length} 处</span> : null}
      {shot.spec.added ? <span className="rc-tag">新加的镜头</span> : null}
      {shot.spec.removed ? <span className="rc-tag rc-tag-bad">这一镜删了</span> : null}
      {pending ? <span className="rc-tag rc-tag-bad" title="方案写了要重画首帧，但首帧还是审查时那张">首帧待重画</span> : null}
    </h3>
    {f.changed ? <div className="rc-frames"><Frame v={f.before} side="修复前" /><span className="rc-arrow" aria-hidden="true">→</span><Frame v={f.after} side="修复后" /></div>
      : f.before ? <div className="rc-frames rc-frames-one"><Frame v={f.before} side="首帧（没换）" /></div> : null}
    {f.note ? <p className="rr-mini rr-bad">{f.note}</p> : null}
    {shot.manual_frames?.length ? <div className="rc-frames">{shot.manual_frames.map(m => <div key={m.before + m.after} className="rc-manual">
      <Frame v={{ path: m.before, label: "fix 登记", sha256: "", mtime: "" }} side="登记的旧图" /><span className="rc-arrow">→</span>
      <Frame v={{ path: m.after, label: "fix 登记", sha256: "", mtime: "" }} side="登记的新图" /></div>)}</div> : null}
    {corrections.length ? <div className="rc-issues">{corrections.map(c => <CorrectionRow key={c.id} dir={dir} c={c} />)}</div>
      : <p className="rr-mini">没有登记方案指到这一镜{f.changed || shot.spec.changed ? "（但首帧或分镜改过）" : ""}。</p>}
    {shot.spec.fields.length ? <details className="rc-diff">
      <summary>分镜文字 diff：{shot.spec.fields.map(x => x.name).join("、")} <span className="rr-mini">{shot.spec.before_source.split("/").slice(-2).join("/")} → {shot.spec.after_source.split("/").slice(-1)[0]}</span></summary>
      {shot.spec.fields.map(x => <FieldDiff key={x.field} f={x} />)}
    </details> : null}
    {shot.prompt?.changed ? <details className="rc-diff"><summary>编译 prompt diff</summary><Diff lines={shot.prompt.diff} /></details> : null}
  </article>;
}

function FieldDiff({ f }: { f: SpecField }): JSX.Element {
  return <div className="rc-field"><h4>{f.name} <code className="rr-mini">{f.field}</code></h4>
    {f.diff.length ? <Diff lines={f.diff} /> : <Diff lines={[...(f.before ? [`-${f.before}`] : []), ...(f.after ? [`+${f.after}`] : [])]} />}</div>;
}

function Diff({ lines }: { lines: string[] }): JSX.Element {
  return <pre className="rc-pre">{lines.map((ln, i) => {
    const k = diffKind(ln);
    return <span key={i} className={`rc-d rc-d-${k}`}>{k === "hunk" ? "⋯" : ln}{"\n"}</span>;
  })}</pre>;
}

function CorrectionRow({ dir, c }: { dir: string; c: Correction }): JSX.Element {
  const [open, setOpen] = useState(false);
  const last = c.history[c.history.length - 1];
  return <div className="rc-issue" data-issue={c.id} data-level={c.level}>
    <div className="rc-issue-head">
      <Link to={reviewIssuesHref(dir, { level: c.level })} className="rv-id" title="在问题清单里看">{c.id}</Link>
      <LevelBadge level={c.level} />
      <span className="rv-cat">{c.category}<span className="rv-dim">{c.dimension}</span></span>
      <StatusBadge status={c.status} />
      <button type="button" className={`rc-v ${verifyClass(c.verification.status)}`} aria-expanded={open} onClick={() => setOpen(!open)}
        title={c.verification.how.join("\n")}>{c.verification.status}</button>
    </div>
    <p className="rc-problem"><b>问题：</b><Clip text={c.problem} max={110} /></p>
    <p className="rc-solution"><b>方案：</b><Clip text={c.solution} max={180} />
      {c.reason ? <span className="rv-reason">（不改理由：{c.reason}）</span> : null}
      {c.solution_source === "changes.md" ? <span className="rr-mini">（配自下一轮 changes.md）</span> : null}</p>
    {c.files.length ? <p className="rc-files"><b>改了：</b>{c.files.map(f => <Link key={f} to={fileHref(f)}><code>{f.split("/").slice(-3).join("/")}</code></Link>)}</p> : null}
    {last ? <p className="rr-mini">{last.by ? `${last.by} · ` : ""}{at(last.at)}{c.history.length > 1 ? ` · 共登记 ${c.history.length} 次` : ""}</p> : null}
    {open ? <div className="rc-verify"><h4>下一轮复核{c.verification.run ? <> · <Link to={reviewRunHref(c.verification.run)}>{c.verification.run.split("/").pop()}</Link></> : null}</h4>
      <ul>{c.verification.how.map((h, i) => <li key={i}><Inline text={h} /></li>)}</ul>
      {c.verification.rows?.length ? <details><summary>下一轮问题表原行 {c.verification.rows.length}</summary><pre>{c.verification.rows.join("\n")}</pre></details> : null}
    </div> : null}
  </div>;
}
