import { useSearchParams, Link } from "react-router-dom";
import type { RunIoItem, StoryRun } from "../lib/storyRuns";
import { storyRunUrl } from "../lib/storyRunRoutes";
import { StoryRunPage } from "./StoryRunPage";
import { Markdown, format } from "./StoryRunDisplay";
import { globalSourceUrl, sourceTitle } from "../lib/globalWorkflow";
import { useGlobalWorkflow } from "./GlobalWorkflowContext";

export const SOURCE_STATUS = { same: "源文件仍与当时版本一致", changed: "源文件已变化；本页保留当时版本",
  missing: "源文件现已不存在；本页保留历史记录", unavailable: "来源路径不可核验", unverified: "未记录源版本指纹，无法核对" };
const FIELD_LABELS: Record<string, string> = { who: "谁 · Who", what: "发生什么 · What", why: "为什么 · Why",
  when: "何时 · When", where: "何地 · Where", how: "如何发生 · How", participants: "实际参与者",
  id: "身份", name: "名称", role: "职责", runtime_id: "运行身份", model: "模型", settings: "设置",
  started_at: "开始时间", finished_at: "完成时间", sampling_parameters: "采样参数", runtime_settings: "运行设置",
  shared_profile: "共享配置关联", statement: "假设内容", reason: "依据", status: "状态", entity: "对象",
  change: "变化", evidence: "证据", fact: "候选设定", path: "来源路径", rules_path: "规则来源路径",
  note: "说明", title: "标题", brief: "方向", text: "正文", frame: "故事六问", state_changes: "候选状态变化",
  fictional_facts: "候选虚构设定", causal_outline: "因果骨架", criterion: "检查标准", result: "检查结果",
  checks: "逐项检查", overall: "总体结论", story: "故事", implementation: "系统实现", accepted: "采纳",
  rejected: "否决", deferred: "暂缓", partial: "部分采纳", previous_candidates: "旧候选",
  previous_decisions: "旧决策", previous_agent_sessions: "旧代理会话", canonical_story_draft: "当前工作区草稿",
  future_episodes: "未来集", input: "实际冻结输入", candidate: "候选数据", sources: "背景与事实资料",
  rules: "流程规则", content: "取用正文", selection: "取用范围", sha256: "源文件指纹",
  input_hash: "输入指纹", assumptions: "本次假设", prior_accepted_state: "此前已确定状态",
  independence: "隔离边界", criteria: "接受标准", proposals: "逐项提议", detail: "提议内容",
  alternatives: "替代选择", recommended: "推荐选择", candidate_status: "候选状态",
  decision: "取舍", decision_reason: "取舍理由", decided_by: "决策者", applied_in: "落点",
  location: "定位", at: "时间", actor: "参与者", type: "事件类型", body: "说明",
  proposal_ids: "关联提议", artifact_refs: "关联资料", purpose: "目的", limits: "适用限制",
  same_input_hash: "冻结输入相同", same_rules: "冻结规则相同", baseline_run_id: "对照基线run" };
const VALUE_LABELS: Record<string, string> = { excluded: "排除", assumed: "暂定假设", confirmed: "已确认",
  unknown: "未知", candidate_acceptable: "候选可接受", pass: "通过", issue: "有问题" };

export function RunIoLinks({ run, kind }: { run: StoryRun; kind: RunIoItem["kind"] }): JSX.Element {
  const { catalog } = useGlobalWorkflow();
  const items = run.io?.items.filter(item => item.kind === kind) || [];
  return <section><h2>{kind === "input" ? "本次输入与规则清单" : "关联文档"}</h2>
    <p className="story-run-muted">{run.io?.coverage || "本run尚无关联清单，请查看原始记录。"}</p>
    <div className="story-run-table-scroll"><table className="story-run-files" aria-label="实际关联清单"><thead><tr><th>类别与文档</th><th>关联来源</th><th>当前源版本</th></tr></thead>
      <tbody>{items.map(item => <tr key={item.id}><td><small>{item.group_label}</small><br />
        <Link to={storyRunUrl("item", run.episode_path, run.run_id, undefined, item.id)}>{item.name} ↗</Link></td>
        <td><code>{item.source_path || item.target}</code>{item.selection === "explicit_excerpt" ? <span>仅选定摘录</span> : null}</td>
        <td>{item.source_status ? SOURCE_STATUS[item.source_status.status] : "本run独立记录"}{item.global_source_id ? <><br /><Link to={globalSourceUrl(item.global_source_id)}>{sourceTitle(catalog?.sources.find(source => source.id === item.global_source_id) || { title: "当前全局源" })} ↗</Link></> : null}</td></tr>)}</tbody></table></div>
  </section>;
}

export function StoryRunItemPage(): JSX.Element {
  const { catalog } = useGlobalWorkflow();
  const [params] = useSearchParams();
  const identity = params.get("item_id");
  return <StoryRunPage document="item">{({ run }) => {
    const item = run.io?.items.find(entry => entry.id === identity);
    if (!item) return <p role="alert">本run没有记录这项资料，请从左侧关联文档打开。</p>;
    const globalEntry = catalog?.sources.find(source => source.id === item.global_source_id);
    return <><section><h2>本次实际使用的记录</h2>
      {item.global_source_id ? <p className="story-run-muted">全局输入：<Link to={globalSourceUrl(item.global_source_id)}>{sourceTitle(globalEntry || { title: "全局源未登记或目录尚未加载" })}</Link> · 当前目录编号；正文保留当时版本。</p> : null}
      <p className="story-run-muted">{item.note || "软链接关联本run记录，内容不会被共享源文件后续修改替换。"}</p>
      {typeof item.value === "string" ? <Markdown text={item.value || "未记录内容。"} resolveLocalLink={href => {
        if (!item.source_path) return undefined;
        try {
          const resolved = new URL(href, `https://run.invalid/${item.source_path}`).pathname.slice(1);
          const recorded = run.io?.items.find(entry => entry.source_path === decodeURIComponent(resolved));
          return recorded ? storyRunUrl("item", run.episode_path, run.run_id, undefined, recorded.id) : undefined;
        } catch { return undefined; }
      }} /> : <StructuredValue value={item.value} />}
    </section><section><h2>来源与版本</h2><dl className="story-run-frame">
      <div><dt>本次版本定位</dt><dd><code>{item.target}</code></dd></div>
      <div><dt>取用内容指纹</dt><dd><code>{item.snapshot_hash}</code></dd></div>
      {item.source_path ? <div><dt>共享源文件</dt><dd><code>{item.source_path}</code></dd></div> : null}
      {item.global_source_id ? <div><dt>全局引用（当前目录）</dt><dd>{sourceTitle(globalEntry || { title: "全局源未登记或目录尚未加载" })}</dd></div> : null}
      {item.source_status ? <div><dt>当前源版本</dt><dd>{SOURCE_STATUS[item.source_status.status]}</dd></div> : null}
      {item.source_hash ? <div><dt>当时源文件 SHA256</dt><dd><code>{item.source_hash}</code></dd></div> : null}
      {item.source_status?.sha256 ? <div><dt>当前源文件 SHA256</dt><dd><code>{item.source_status.sha256}</code></dd></div> : null}
    </dl><p className="story-run-muted">{run.io?.coverage}</p>
    {item.global_source_id ? <p><Link to={globalSourceUrl(item.global_source_id)}>在工作流中查看当前全局源 ↗</Link> · 此页仍显示当时冻结版本。</p> : null}
    <Link to={storyRunUrl("input", run.episode_path, run.run_id)}>查看本run完整输入清单</Link></section></>;
  }}</StoryRunPage>;
}

function StructuredValue({ value }: { value: unknown }): JSX.Element {
  if (Array.isArray(value)) return value.length ? <ol className="story-run-notes">{value.map((entry, index) =>
    <li key={index}><StructuredValue value={entry} /></li>)}</ol> : <p>空列表；本次未选用条目。</p>;
  if (value && typeof value === "object") return <dl className="story-run-data">{Object.entries(value).map(([key, entry]) =>
    <div key={key}><dt>{FIELD_LABELS[key] || key}</dt><dd><StructuredValue value={entry} /></dd></div>)}</dl>;
  return <p className="story-run-prose">{value == null ? "未记录" : typeof value === "string" ? VALUE_LABELS[value] || value : format(value)}</p>;
}
