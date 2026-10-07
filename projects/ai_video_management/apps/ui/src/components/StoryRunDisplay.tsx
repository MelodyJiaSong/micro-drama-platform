import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Link } from "react-router-dom";
import type { StoryFrame } from "../lib/storyRuns";

export const FRAME_LABELS: Record<keyof StoryFrame, string> = {
  who: "谁 · Who", what: "发生什么 · What", why: "为什么 · Why",
  when: "何时 · When", where: "何地 · Where", how: "如何发生 · How",
};
export const DECISIONS = { accepted: "采纳", rejected: "否决", partial: "部分采纳", deferred: "暂缓" };
export const RUN_STATUS: Record<string, string> = { running: "进行中", in_progress: "进行中", started: "待创作", ready_for_review: "候选待确定", completed: "已完成", failed: "失败", draft: "草稿", candidate: "候选", published: "已发布", pending: "待开始", selected: "当前采用", stale: "采用记录待核对" };
export const format = (value: unknown): string => typeof value === "string" ? value : JSON.stringify(value, null, 2) ?? "未记录";
export const when = (value: string): string => {
  const date = new Date(value);
  return Number.isNaN(date.valueOf()) ? value : date.toLocaleString("zh-CN", { hour12: false });
};
export function Frame({ frame }: { frame: StoryFrame }): JSX.Element {
  return <dl className="story-run-frame">{Object.entries(FRAME_LABELS).map(([key, label]) =>
    <div key={key}><dt>{label}</dt><dd>{frame?.[key as keyof StoryFrame] || "未记录"}</dd></div>)}</dl>;
}
export function Markdown({ text, resolveLocalLink }: { text: string; resolveLocalLink?: (href: string) => string | undefined }): JSX.Element {
  const metadata = text.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/);
  return <div className="story-run-markdown">
    {metadata ? <Evidence label="文件元数据（原文）" value={metadata[1]} /> : null}
    <ReactMarkdown remarkPlugins={[remarkGfm]} components={{
    h1: ({ children }) => <h3>{children}</h3>, h2: ({ children }) => <h4>{children}</h4>,
    h3: ({ children }) => <h5>{children}</h5>,
    a: ({ href, children }) => {
      if (!resolveLocalLink || !href || /^(?:[a-z][a-z\d+.-]*:|\/\/|#)/i.test(href)) return <a href={href}>{children}</a>;
      const recorded = resolveLocalLink(href);
      return recorded ? <Link to={recorded}>{children}</Link> : <span title={`本run未记录此引用的内容：${href}`}>{children}（未记录引用）</span>;
    },
  }}>{metadata ? text.slice(metadata[0].length) : text}</ReactMarkdown></div>;
}
export function Evidence({ label, value }: { label: string; value: unknown }): JSX.Element {
  return <details className="story-run-detail"><summary>{label}</summary><pre>{format(value)}</pre></details>;
}
export function Sources({ label, values, frozen = true }: { label: string; values: unknown[]; frozen?: boolean }): JSX.Element {
  return <details className="story-run-detail"><summary>{label}</summary>
    <p className="story-run-muted">{frozen ? "源文件为 Persistent；以下内容与指纹是本次运行冻结的版本，不代表当前最新文件。" : "这里展示所选共享版本中的资料，不自动更新为来源文件的最新内容。"}</p>
    {values.map((value, index) => {
      if (!value || typeof value !== "object" || Array.isArray(value)) return <Markdown key={index} text={format(value)} />;
      const item = value as Record<string, unknown>;
      return <div className="story-run-source" key={index}>
        <h3>{typeof item.name === "string" ? item.name : typeof item.path === "string" ? item.path.split("/").at(-1) : `资料 ${index + 1}`}</h3>
        {typeof item.content === "string" ? <Markdown text={item.content} /> : <p>未记录资料正文。</p>}
        {typeof item.selection === "string" ? <p className="story-run-muted">取用范围：{item.selection === "full_file" ? "全文" : item.selection === "explicit_excerpt" ? "明确选定摘录" : item.selection}</p> : null}
        <Evidence label="来源路径与版本证据" value={{ path: item.path, sha256: item.sha256, selection: item.selection }} />
      </div>;
    })}
    {!values.length ? <p>没有选用的来源。</p> : null}
  </details>;
}
export function Notes({ values, empty }: { values: unknown[]; empty: string }): JSX.Element {
  if (!values.length) return <p className="story-run-muted">{empty}</p>;
  return <ul className="story-run-notes">{values.map((value, index) => {
    if (value && typeof value === "object" && !Array.isArray(value)) {
      const item = value as Record<string, unknown>;
      if (typeof item.statement === "string") return <li key={index}><strong>{item.status === "confirmed" ? "已确认" : "本次假设"}：</strong>{item.statement}
        {item.reason ? <p className="story-run-muted">依据：{format(item.reason)}</p> : null}</li>;
      if (typeof item.change === "string") return <li key={index}><strong>{format(item.entity)}：</strong>{item.change}
        {item.evidence ? <p className="story-run-muted">正文依据：{format(item.evidence)}</p> : null}</li>;
    }
    return <li key={index}>{format(value)}</li>;
  })}</ul>;
}
