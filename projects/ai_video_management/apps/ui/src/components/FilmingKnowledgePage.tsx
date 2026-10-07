import { Link } from "react-router-dom";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeSanitize from "rehype-sanitize";
import shotSizes from "../../../../../../.agents/references/project/ai_video_shot_sizes.md?raw";
import "./EpisodeWorkflowPage.css";
import "./FilmingKnowledgePage.css";

export function FilmingKnowledgePage(): JSX.Element {
  return <div className="episode-workflow filming-knowledge">
    <nav aria-label="知识导航"><Link to="/workflow">工作流</Link><span> / 影视改编</span></nav>
    <p className="workflow-eyebrow">全局知识 · 影视改编</p>
    <article className="markdown-view">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeSanitize]}
        components={{
          table: ({ children }) => <div className="filming-knowledge-table" tabIndex={0} role="region" aria-label="知识对照表"><table>{children}</table></div>,
          a: ({ href, children }) => href === "ai_video_jingbie.md"
            ? <span>{children}</span>
            : <a href={href} target="_blank" rel="noreferrer">{children}</a>,
        }}
      >{shotSizes}</ReactMarkdown>
    </article>
  </div>;
}
