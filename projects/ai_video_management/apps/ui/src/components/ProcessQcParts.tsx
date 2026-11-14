import { useState } from "react";
import { PERSPECTIVE_LABEL, byStage, stageLabel, type FollowupHealth, type QcCheck } from "../lib/processQc";

export function CopyButton({ text, label }: { text: string; label: string }): JSX.Element {
  const [state, setState] = useState<"" | "已复制" | "复制失败">("");
  const copy = (): void => {
    void navigator.clipboard.writeText(text).then(() => setState("已复制")).catch(() => setState("复制失败"));
    window.setTimeout(() => setState(""), 2000);
  };
  return <button type="button" className="qc-copy" onClick={copy} title={text}>{state || `📋 ${label}`}</button>;
}

export function LevelBadge({ level }: { level: string }): JSX.Element {
  return <span className={`qc-level ${level === "仓库级" ? "qc-level-repo" : "qc-level-drama"}`}>{level}</span>;
}

export function LevelBanner({ level }: { level: "仓库级" | "剧级" }): JSX.Element {
  return level === "仓库级"
    ? <p className="qc-banner qc-banner-repo"><strong>仓库级</strong>：对所有剧生效，影响面大。只收背后有共用依据的检查；改动须你明确同意。拿不准是否适用于所有剧的，一律放剧级。</p>
    : <p className="qc-banner qc-banner-drama"><strong>剧级</strong>：只对本剧生效。新增检查默认放这里；同类问题在两部以上的剧反复出现，再提议升为仓库级。</p>;
}

function CheckBadges({ c }: { c: QcCheck }): JSX.Element {
  return <span className="qc-badges">
    <span className={c.gate ? "qc-b qc-b-gate" : "qc-b"}>{c.gate ? "交付闸门" : "建议"}</span>
    <span className="qc-b">{c.kind === "review" ? "独立审稿" : "机检"}</span>
    {c.kind === "review" && c.perspective ? <span className="qc-b qc-b-persp">视角：{PERSPECTIVE_LABEL[c.perspective] ?? c.perspective}</span> : null}
    <span className={c.auto ? "qc-b qc-b-auto" : "qc-b qc-b-todo"}>{c.auto ? "已自动化" : "待自动化"}</span>
    {c.when ? <span className="qc-b">仅当：{c.when}</span> : null}
  </span>;
}

export function CheckList({ checks, stages, action }: {
  checks: QcCheck[]; stages: string[]; action?: (c: QcCheck) => JSX.Element;
}): JSX.Element {
  if (!checks.length) return <p className="qc-empty">（没有登记的检查）</p>;
  return <>{byStage(checks, stages).map(([stage, list]) => <section key={stage} className="qc-stage">
    <h4>{stageLabel(stage)} <span className="qc-count">{list.length}</span></h4>
    <ul className="qc-checks">{list.map(c => <li key={c.id} className="qc-check">
      <div className="qc-check-head"><code>{c.id}</code><LevelBadge level={c.level} /><CheckBadges c={c} /></div>
      <p>{c.desc}</p>
      {c.how ? <p className="qc-how">怎么查：{c.how}</p> : null}
      {c.basis ? <p className="qc-basis">共用依据：{c.basis}</p> : null}
      {c.sources.length ? <p className="qc-sources">来自实战反馈：{c.sources.map(s => <span key={s} className="qc-src">{s.replace("#", " #")}</span>)}</p> : null}
      {action ? <div className="qc-actions">{action(c)}</div> : null}
    </li>)}</ul>
  </section>)}</>;
}

export function Pipeline({ checks, stages }: { checks: QcCheck[]; stages: string[] }): JSX.Element {
  return <ol className="qc-pipeline" aria-label="流程环节">{stages.map(stage => {
    const n = checks.filter(c => c.stage === stage);
    return <li key={stage} className={n.length ? "" : "qc-pipe-empty"}>
      <span>{stageLabel(stage)}</span><small>{n.length ? `${n.length} 项 · 闸门 ${n.filter(c => c.gate).length}` : "无检查"}</small>
    </li>;
  })}</ol>;
}

export function HealthLine({ f }: { f: FollowupHealth }): JSX.Element {
  const missing = f.followups - f.logged;
  return <span className="qc-health">
    近 {f.window_days} 天 follow-up {f.followups} 条 · 进 changelog {f.logged}
    {missing ? <em className="qc-bad"> · 漏记 {missing}</em> : null}
    {f.duplicates.length ? <em className="qc-bad"> · 撞号 {f.duplicates.join("、")}</em> : null}
    {f.pending ? <em className="qc-warn"> · 待补 {f.pending}</em> : null}
  </span>;
}
