import { useState } from "react";
import { Link } from "react-router-dom";
import { storyRunUrl } from "../lib/storyRunRoutes";
import { StoryRunPage, type StoryRunPageData } from "./StoryRunPage";
import { Frame } from "./StoryRunDisplay";

export function StoryRunStoryPage(): JSX.Element {
  return <StoryRunPage document="output">{data => <Story key={data.run.run_id} {...data} />}</StoryRunPage>;
}
function Story({ run: shown, runs, summary, selection }: StoryRunPageData): JSX.Element {
  const [notice, setNotice] = useState("");
  const shellQuote = (value: string): string => `'${value.replace(/'/g, "''")}'`;
  const command = `python tools/story_run.py promote --episode-path ${shellQuote(shown.episode_path)} --run-id ${shellQuote(shown.run_id)}`;
  const copy = (value: string, message: string): void => {
    void navigator.clipboard.writeText(value).then(() => setNotice(message)).catch(() => setNotice("复制失败，请手动选择文本。"));
  };
  const other = runs.find(item => item.run_id !== shown.run_id);
  return <>{notice ? <p role="status">{notice}</p> : null}<div className="story-run-current-selection"><p>当前 EP 草稿：{selection ? `${runs.find(item => item.run_id === selection.run_id)?.title || selection.run_id} · ${selection.status === "stale" ? "采用记录与当前正文不一致，需核对" : "已选为故事草稿，尚未确定"}` : "尚未选用"}</p>{other ? <Link to={storyRunUrl("compare", shown.episode_path, shown.run_id, other.run_id)}>对比其他候选</Link> : null}<Link to={`/story-input?episode_path=${encodeURIComponent(shown.episode_path)}`}>查看共享输入与规则版本</Link></div><><section><div className="story-run-item-heading"><h2>候选故事 <span className="story-run-count">产出 · Transient</span></h2><span className="story-run-badge">候选 · 待确定</span></div>
            <p className="story-run-muted">本次稿件与状态变化独立保存，不自动成为长期事实。</p>
            {shown.candidate.title ? <h3>{shown.candidate.title}</h3> : null}
            <p className="story-run-prose">{shown.candidate.brief}</p><details className="story-run-detail"><summary>候选故事的六个基本问题</summary><Frame frame={shown.candidate.frame} /></details>
            <div className="story-run-prose story-run-story">{shown.candidate.text || "尚未形成候选正文。"}</div>
          </section><section><h2>选用为 EP1 草稿</h2><p>通过 Claude Code/Codex 或 CLI 执行下面的命令。它只选入正文草稿，保留每个候选与历史；不等于确定版本。</p>
            <pre>{command}</pre><button type="button" onClick={() => copy(command, "已复制选用命令；尚未执行。")}>复制选用命令</button>
            <details className="story-run-detail"><summary>本次独立文件夹位置</summary><code>{summary?.audit_folder || summary?.audit_path || "未记录"}</code></details>
          </section></></>;
}
