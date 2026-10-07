import { useEffect, useState, type ReactNode } from "react";
import { useSearchParams } from "react-router-dom";
import { listStoryRuns, loadStoryRun, type RunSummary, type StoryRun, type RunSelection } from "../lib/storyRuns";
import { STORY_RUN_PAGES, type StoryRunDocument } from "../lib/storyRunRoutes";
import { RUN_STATUS as STATUS, when } from "./StoryRunDisplay";
import "./StoryRunsPage.css";

export interface StoryRunPageData {
  run: StoryRun;
  runs: RunSummary[];
  summary?: RunSummary;
  selection: RunSelection | null;
}
export function StoryRunPage({ document, children }: { document: StoryRunDocument; children: (data: StoryRunPageData) => ReactNode }): JSX.Element {
  const [params] = useSearchParams();
  const episode = params.get("episode_path") || "";
  const requested = params.get("run_id") || "";
  const itemId = params.get("item_id") || "";
  const [runs, setRuns] = useState<RunSummary[]>([]);
  const [loadedEpisode, setLoadedEpisode] = useState("");
  const [run, setRun] = useState<StoryRun | null>(null);
  const [selection, setSelection] = useState<RunSelection | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [refresh, setRefresh] = useState(0);
  const selected = requested || runs[0]?.run_id || "";
  const shown = run?.episode_path === episode && run.run_id === selected ? run : null;
  const page = STORY_RUN_PAGES[document];
  const item = document === "item" ? shown?.io?.items.find(entry => entry.id === itemId) : undefined;
  const episodeLabel = episode.split("/").at(-1)?.toUpperCase() || "故事";

  useEffect(() => {
    documentScrollToTop();
  }, [episode, requested, document, itemId]);
  useEffect(() => {
    const controller = new AbortController();
    setRuns([]); setSelection(null); setLoadedEpisode(""); setRun(null); setError("");
    if (!episode) return () => controller.abort();
    setBusy(true);
    void listStoryRuns(episode, controller.signal).then(data => {
      if (!controller.signal.aborted) { setRuns(data.runs); setSelection(data.selection || null); setLoadedEpisode(episode); }
    }).catch(err => { if (!controller.signal.aborted) { setError(`读取运行索引失败：${err instanceof Error ? err.message : String(err)}`); setBusy(false); } });
    return () => controller.abort();
  }, [episode, refresh]);
  useEffect(() => {
    const controller = new AbortController();
    setRun(null);
    if (loadedEpisode !== episode) return () => controller.abort();
    if (!selected) { setBusy(false); return () => controller.abort(); }
    setBusy(true); setError("");
    void loadStoryRun(episode, selected, controller.signal).then(data => {
      if (!controller.signal.aborted) {
        if (data.episode_path !== episode || data.run_id !== selected) throw new Error("记录归属不匹配");
        setRun(data);
      }
    }).catch(err => { if (!controller.signal.aborted) setError(`读取文档失败：${err instanceof Error ? err.message : String(err)}`); })
      .finally(() => { if (!controller.signal.aborted) setBusy(false); });
    return () => controller.abort();
  }, [episode, selected, loadedEpisode, refresh]);

  return <div className="story-runs-page" data-document={document}>
    <header className="story-runs-header"><div>
      <p className="story-run-eyebrow">{episodeLabel} · {item?.group_label || page.category} · Transient</p>
      <h1>{item?.name || page.title}</h1>
      <p className="story-run-muted">本页只读。通过 Claude Code/Codex 修改，刷新查看。</p>
    </div><button type="button" onClick={() => setRefresh(value => value + 1)} disabled={!episode || busy}>刷新文档</button></header>
    {!episode ? <p role="alert">请从左侧每集的 run 文档打开。</p> : null}
    {error ? <p className="story-run-error" role="alert">{error}</p> : null}
    <div className="story-run-content" aria-busy={busy}>
      {busy && !shown ? <p role="status">读取文档…</p> : null}
      {!busy && !error && episode && !runs.length ? <p>还没有创作记录。</p> : null}
      {shown ? <>
        <div className="story-run-meta"><span>{`run${runs.findIndex(item => item.run_id === shown.run_id) + 1}`}</span>
          <strong>{shown.candidate.title}</strong><code>{shown.run_id}</code><span>{when(shown.created_at)}</span>
          <span>{STATUS[shown.status] || shown.status} · 本 run 独立文档，历史留存，不跨 run 自动继承</span></div>
        {children({ run: shown, runs, summary: runs.find(item => item.run_id === shown.run_id), selection })}
      </> : null}
    </div>
  </div>;
}
function documentScrollToTop(): void {
  const main = globalThis.document.getElementById("main");
  if (main) main.scrollTop = 0;
}
