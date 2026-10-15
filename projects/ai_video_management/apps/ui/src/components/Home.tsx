import { Link } from "react-router-dom";
import type { TreeNode } from "../types";
import { collectDramaNodes } from "../lib/dramas";
import { ObsoleteBadge } from "./ObsoleteBadge";

export interface HomeProps {
  tree: TreeNode | null;
}

export function Home({ tree }: HomeProps): JSX.Element {
  const dramas = collectDramaNodes(tree).filter((d) => !d.name.startsWith("_"));
  return (
    <div className="home-view">
      <h1>ai_video_management</h1>
      <p>
        浏览 <code>ai_videos/</code> 下的短剧。六模块流程的剧在左侧按 stage 展开（故事创作 →
        影视改编 → Prompt 编译与出片），每镜可看编译好的 prompt、资料包与生成记录；人物、背景、道具等资产在
        「1_资产库」。标「已过时」的剧由已删除的旧流程制作，只作参考。
      </p>
      <Link to="/workflow" className="home-workflow-link">
        查看创作流程：故事创作 → 影视改编 → Prompt 编译
      </Link>
      {tree === null ? (
        <p className="muted">Loading tree…</p>
      ) : dramas.length === 0 ? (
        <p className="muted">
          <code>ai_videos/</code> 下还没有剧。
        </p>
      ) : (
        <section className="home-projects" aria-labelledby="home-projects-heading">
          <h2 id="home-projects-heading">剧目</h2>
          <ul className="home-project-list">
            {dramas.map((d) => (
              <li key={d.path} className="home-project-item">
                <Link to={`/drama?drama=${encodeURIComponent(d.path)}`} className="home-project-name">
                  {d.display_name || d.name}
                </Link>
                {d.workflow === "three-module-v1" ? <span className="muted"> · 六模块</span> : null}
                {d.obsolete ? <ObsoleteBadge note={d.obsolete_note} /> : null}
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  );
}
