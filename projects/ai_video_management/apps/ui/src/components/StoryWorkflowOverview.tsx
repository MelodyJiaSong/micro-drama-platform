import { Link } from "react-router-dom";
import { useGlobalWorkflow } from "./GlobalWorkflowContext";
import { globalSourceUrl, sourceTitle } from "../lib/globalWorkflow";
import { STORY_SECTIONS, storySectionUrl, storyTopicUrl } from "../lib/storyWorkflow";
import "./GlobalWorkflowPage.css";

export function StoryWorkflowOverview({ sectionId }: { sectionId?: string }): JSX.Element {
  const { catalog, error, refresh } = useGlobalWorkflow();
  const sections = STORY_SECTIONS.filter(section => !sectionId || section.id === sectionId);
  return <section className="global-workflow">
    <header><h2>{sectionId ? "主题目录" : "故事内容与执行规则"}</h2><button onClick={refresh}>刷新目录</button></header>
    <p>内容类定义故事标准；执行类说明如何运行、记录与验证。创作时两类均适用。</p>
    {error ? <p role="alert">{error}。主题目录仍可使用；全局来源尚未核验。</p> : !catalog ? <p role="status">正在核验全局来源…</p> : null}
    <div className="story-workflow-sections">{sections.map(section => {
      const source = catalog?.sources.find(entry => entry.id === section.source_id);
      return <section key={section.id}>
        <h3><Link to={storySectionUrl(section.id)}>{section.title}</Link></h3><p>{section.description}</p>
        <ul>{section.topics.map(topic => <li key={topic.id}><Link to={storyTopicUrl(section, topic)}>{topic.title}</Link></li>)}</ul>
        <Link to={globalSourceUrl(section.source_id)}>{source ? `完整原文：${sourceTitle(source)}` : "查看完整源文档"}</Link>
      </section>;
    })}</div>
  </section>;
}
