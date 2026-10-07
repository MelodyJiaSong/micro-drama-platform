import { Link, Navigate, useParams } from "react-router-dom";
import { FILMING_KNOWLEDGE_PATH, WORKFLOW_MODULES, WORKFLOW_PATH, workflowGroups } from "../lib/workflowData";
import { numberedTitle } from "../lib/globalWorkflow";
import { useGlobalWorkflow } from "./GlobalWorkflowContext";
import "./EpisodeWorkflowPage.css";
import { GlobalWorkflowOverview } from "./GlobalWorkflowPage";
import { StoryWorkflowOverview } from "./StoryWorkflowOverview";
import { STORY_SECTIONS } from "../lib/storyWorkflow";

export function WorkflowPage(): JSX.Element {
  const { module: moduleId, storySection } = useParams();
  const { catalog } = useGlobalWorkflow();
  const selected = WORKFLOW_MODULES.find(module => module.id === moduleId);
  if (moduleId && !selected) return <Navigate to={WORKFLOW_PATH} replace />;
  const section = STORY_SECTIONS.find(entry => entry.id === storySection);
  if (storySection && (moduleId !== "story" || !section)) return <Navigate to="/workflow/story" replace />;
  const modules = selected ? [selected] : [];
  const title = section?.title || (selected ? numberedTitle(workflowGroups(catalog).find(group => group.id === selected.id) || selected) : "全局工作流");
  return <div className="episode-workflow">
    {selected ? <nav aria-label="工作流导航"><Link to={WORKFLOW_PATH}>工作流</Link><span> / </span><Link to={`${WORKFLOW_PATH}/${selected.id}`}>{selected.title}</Link>{section ? <span> / {section.title}</span> : null}</nav> : null}
    <header><div><p className="workflow-eyebrow">全局输入与设置</p><h1>{title}</h1></div></header>
    {selected && !section ? <div className="workflow-overview" aria-label={selected.title}>
      {modules.map(module => <section key={module.id}>
        <span className="workflow-step">0{WORKFLOW_MODULES.indexOf(module) + 1}</span><h2>{module.title}</h2><p>{module.purpose}</p>
        <dl><dt>输入</dt><dd>{module.input}</dd><dt>输出</dt><dd>{module.output}</dd></dl>
        {module.id === "filming" ? <Link to={FILMING_KNOWLEDGE_PATH}>全局知识：镜头类型与景别 →</Link> : null}
      </section>)}
    </div> : null}
    <p className="workflow-rule">{selected ? "先确定上游版本，再开始下游。上游改变，下游保留并标记待更新。" : "按稳定编号识别全局输入；编号不随标题或排序变化，实际使用版本以 run 保存的内容与指纹为准。"}</p>
    <div className="workflow-support"><span>独立支持：Research · 人物、场景与物件资产</span></div>
    {selected?.id === "story" ? <StoryWorkflowOverview sectionId={storySection} /> : <GlobalWorkflowOverview group={selected?.id} />}
    <Link className="workflow-start" to="/drama?drama=ai_videos%2Fshengji_zhilu">从魔兽世界 EP1 开始 →</Link>
  </div>;
}
