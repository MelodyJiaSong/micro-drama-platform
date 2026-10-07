import { useState } from "react";
import type { StoryRun } from "../lib/storyRuns";
import { StoryRunPage } from "./StoryRunPage";
import { DECISIONS, RUN_STATUS as STATUS, Evidence, when } from "./StoryRunDisplay";

export function StoryRunProcessPage(): JSX.Element {
  return <StoryRunPage document="process">{({ run }) => <Process key={run.run_id} shown={run} />}</StoryRunPage>;
}
function Process({ shown }: { shown: StoryRun }): JSX.Element {
  const [filter, setFilter] = useState("all");
  return <><section><h2>实际参与者 <span className="story-run-count">过程 · Transient · {shown.participants.length}</span></h2>
            {!shown.participants.length ? <p>尚未记录参与者。</p> : null}
            {shown.participants.map(person => <article className="story-run-person" key={person.id}>
              <div className="story-run-item-heading"><h3>{person.name}</h3><span className="story-run-badge">{person.scope === "story" ? "故事创作" : "系统实现"}</span></div>
              <p>{person.role} · {STATUS[person.status] || person.status}</p>
              <details className="story-run-detail"><summary>完整任务、回复与身份</summary>
                <dl><dt>记录 ID</dt><dd>{person.id}</dd><dt>运行身份</dt><dd>{person.runtime_id || "未公开"}</dd>
                  <dt>模型</dt><dd>{person.model || "未公开"}</dd><dt>开始 / 结束</dt><dd>{person.started_at ? when(person.started_at) : "未记录"} / {person.finished_at ? when(person.finished_at) : "未记录"}</dd></dl>
                <h4>分配的任务</h4><pre>{person.prompt || "未记录"}</pre><h4>实际回复</h4><pre>{person.output || "尚未返回"}</pre>
              </details></article>)}
          </section>
          <section><div className="story-run-item-heading"><h2>意见与决定 <span className="story-run-count">过程 · Transient · {shown.proposals.length}</span></h2>
            <label>筛选 <select value={filter} onChange={event => setFilter(event.target.value)}><option value="all">全部决定</option>
              {Object.entries(DECISIONS).map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select></label></div>
            {!shown.proposals.length ? <p>尚未记录意见。</p> : null}
            {shown.proposals.filter(item => filter === "all" || item.decision === filter).map(item => <article className="story-run-proposal" key={item.id}>
              <div className="story-run-item-heading"><h3>{item.title}</h3><span className={`story-run-badge decision-${item.decision}`}>{DECISIONS[item.decision]}</span></div>
              <p className="story-run-muted">提出：{shown.participants.find(person => person.id === item.agent_id)?.name || item.agent_id} · {item.location || "未指定位置"}</p>
              <p className="story-run-prose">{item.detail}</p><p><strong>提出原因：</strong>{item.reason || "未记录"}</p>
              <p><strong>决定理由：</strong>{item.decision_reason || "尚未记录"}</p>
              <p className="story-run-muted">决定者：{shown.participants.find(person => person.id === item.decided_by)?.name || item.decided_by || "未记录"}</p>
              <Evidence label="判断标准、证据与应用位置" value={{ 标准: item.criteria, 证据: item.evidence, 应用位置: item.applied_in, 意见编号: item.id }} />
            </article>)}
          </section>
          <section><h2>过程时间线 <span className="story-run-count">过程 · Transient</span></h2><ol className="story-run-timeline">{shown.events.map(event => <li key={event.id}>
            <small>{when(event.at)} · {shown.participants.find(person => person.id === event.actor)?.name || event.actor}</small><h3>{event.title}</h3>
            <p className="story-run-prose">{event.body}</p>
            {(event.proposal_ids?.length || event.artifact_refs?.length) ? <Evidence label="关联意见与产物" value={{ 意见: event.proposal_ids, 产物: event.artifact_refs }} /> : null}
          </li>)}</ol>{!shown.events.length ? <p>尚未记录过程事件。</p> : null}</section><section><h2>完整过程记录</h2><Evidence label="原始 JSON" value={shown} /></section></>;
}
