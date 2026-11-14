import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchProcessQc } from "../api";
import { PROCESS_QC_REPO_PATH, percent, processQcDramaUrl, type DramaQcSummary } from "../lib/processQc";
import { LAWS, ROLLOUT, SEVERITY, STAGES, STRATEGY_STATUS, lawsAt, type LawId, type StageId } from "../lib/reviewStrategy";
import { CaseDiagram, DependencyDiagram, FlowDiagram, LaneDiagram, VerdictTree } from "./ReviewStrategyDiagrams";
import { reviewRunHref } from "../lib/reviewRun";
import "./ReviewStrategyPage.css";

const PILOT = "ai_videos/chuanyue_yiri";

function PilotStatus(): JSX.Element | null {
  const [d, setD] = useState<DramaQcSummary | null>(null);
  useEffect(() => {
    let live = true;
    fetchProcessQc().then(r => { if (live) setD(r.dramas.find(x => x.drama === PILOT) ?? null); }).catch(() => undefined);
    return () => { live = false; };
  }, []);
  if (!d) return null;
  return <div className="rs-status" aria-label="试点剧当前状态">
    <span className="rs-status-k">试点 · <Link to={processQcDramaUrl(PILOT)}>chuanyue_yiri</Link></span>
    <span className={d.enabled ? "rs-chip rs-chip-ok" : "rs-chip rs-chip-bad"}>自检闸门：{d.enabled ? "已启用" : "未启用"}</span>
    <span className="rs-chip">缺陷 {d.defects}（用户抓到 {d.user_caught}）</span>
    <span className={d.escape_rate && d.escape_rate > 0.5 ? "rs-chip rs-chip-bad" : "rs-chip"}>逃逸率 {percent(d.escape_rate)}</span>
    <span className="rs-chip">剧级检查 {d.drama_checks}</span>
  </div>;
}

function StagePanel({ id }: { id: StageId }): JSX.Element {
  const s = STAGES.find(x => x.id === id) ?? STAGES[0];
  return <div className="rs-panel" aria-live="polite">
    <div className="rs-panel-head"><strong>{s.no} {s.name}</strong><span>{s.question}</span><code>{s.file}</code></div>
    <div className="rs-panel-grid">
      <div><h4>机检</h4><ul>{s.machine.map(m => <li key={m.text}>{m.text}{m.isNew ? <em className="rs-newtag">新</em> : null}</li>)}</ul></div>
      <div><h4>独立审稿人</h4><ul>{lawsAt(s.id).map(l => <li key={l.id}><i className="rs-dot" style={{ background: l.color }} />{l.name}：{l.rule}{l.isNew ? <em className="rs-newtag">新</em> : null}</li>)}</ul></div>
      <div><h4>闸门</h4><p>{s.gate}</p>{s.human ? <p className="rs-human-p">★ {s.human}</p> : null}<h4>在这关返工的代价</h4><p>{s.cost}</p></div>
    </div>
  </div>;
}

function LawPanel({ id }: { id: LawId | null }): JSX.Element {
  const l = LAWS.find(x => x.id === id);
  if (!l) return <p className="rs-caption">点一条泳道，看这位审稿人管什么、看什么材料，以及 EP01 里的真实例子。</p>;
  return <div className="rs-panel" aria-live="polite">
    <div className="rs-panel-head"><i className="rs-dot" style={{ background: l.color }} /><strong>{l.name}</strong>
      <span>上岗：{l.stages.map(s => STAGES.find(x => x.id === s)?.no).join(" ")}</span></div>
    <div className="rs-panel-grid">
      <div><h4>管什么</h4><p>{l.rule}</p></div>
      <div><h4>看什么材料</h4><p>{l.materials}</p></div>
      <div><h4>EP01 的真实例子</h4><p>{l.example}</p></div>
    </div>
  </div>;
}

export function ReviewStrategyPage(): JSX.Element {
  const [stage, setStage] = useState<StageId>("filming");
  const [law, setLaw] = useState<LawId | null>(null);
  return <div className="review-strategy">
    <p className="rs-crumb"><Link to={PROCESS_QC_REPO_PATH}>← 自检与进化（仓库级）</Link></p>
    <h1>审查机制</h1>
    <p className="rs-draft">{STRATEGY_STATUS}</p>
    <p className="rs-lede">六道关，每关先跑机检，再交给专职审稿人。每位审稿人只管一条法则，由另一个模型在全新上下文里审。结论按「法则 · 严重度 · 本该哪关抓到 · 怎么处理」归档；漏网的问题补到更早的一关。</p>
    <PilotStatus />
    <p className="rs-caption">每次审查都生成一张<strong>审查单</strong>：按下面的分工列出要有哪些独立审稿人、各审什么；每位审稿人交报告后自己打勾，全部打勾才算审完。试点：<Link to={reviewRunHref(`${PILOT}/episodes/ep01`)}>Portal Travel EP01 的审查单</Link>。</p>

    <section>
      <h2><span className="rs-k">1</span>主流程：产物 → 机检 → 审稿 → 闸门</h2>
      <p className="rs-caption">绿线：过了进下一关。红色虚线：不过，回本关或更上游返工。★：必须由你点头的关键节点。橙线：漏网回路。点任一列看这一关的细节。</p>
      <div className="rs-scroll"><FlowDiagram selected={stage} onSelect={setStage} highlightLaw={law} /></div>
      <StagePanel id={stage} />
    </section>

    <section>
      <h2><span className="rs-k">2</span>依赖：改了谁，谁的结论作废</h2>
      <p className="rs-caption">每个结论都绑定它审的那个产物的哈希。<span className="rs-legend rs-lg-up">蓝＝它依赖的上游</span><span className="rs-legend rs-lg-down">橙＝改了它要重做或重审的下游</span><span className="rs-legend rs-lg-gate">绿＝闸门放行</span></p>
      <DependencyDiagram />
    </section>

    <section>
      <h2><span className="rs-k">3</span>审稿人分工：谁在哪几关上岗</h2>
      <div className="rs-scroll"><LaneDiagram selected={law} onSelect={setLaw} /></div>
      <LawPanel id={law} />
    </section>

    <section>
      <h2><span className="rs-k">4</span>结论怎么分类</h2>
      <div className="rs-sev-row">{SEVERITY.map(s => <span key={s.id} className={`rs-sevchip rs-sevchip-${s.id}`}>{s.label}{s.hint ? <small>{s.hint}</small> : null}</span>)}</div>
      <div className="rs-scroll"><VerdictTree /></div>
    </section>

    <section>
      <h2><span className="rs-k">5</span>漏网案例：错误从哪进来，新检查在哪拦下</h2>
      <CaseDiagram />
    </section>

    <section>
      <h2><span className="rs-k">6</span>落地顺序</h2>
      <ol className="rs-rollout">{ROLLOUT.map((r, i) => <li key={r.step}>
        <span className="rs-step-n">{i + 1}</span>
        <span className="rs-step-b"><span className="rs-step-s">{r.scope}</span>{r.step}{r.needs ? <em className="rs-needs">{r.needs}</em> : null}</span>
      </li>)}</ol>
      <p className="rs-caption">出片后每条片子约 6–8 位审稿人，EP01 一轮约 200 次审稿调用，走订阅额度，不花即梦积分。出片前的分镜审稿每场一次，最便宜，也最值。</p>
    </section>
  </div>;
}
