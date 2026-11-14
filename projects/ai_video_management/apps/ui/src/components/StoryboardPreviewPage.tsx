import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { fetchFile } from "../api";
import type { StoryboardScene } from "../lib/episodeStoryboard";
import { audioPreviewHref } from "../lib/episodePreview";
import { useFileChanges } from "../lib/fileEvents";
import { ShotCard } from "./EpisodeStoryboard";
import "./EpisodeWorkflowPage.css";
import "./EpisodeStoryboard.css";

/** 故事板预览（follow-up 359）：没有 filming.json 的系列（教学视频等）用 `<path>/storyboard/storyboard.json`，
 *  与短剧「影视改编」故事板同样式：每场一节（场名、比例尺 / 时间、本场目的、总秒数、镜数），每镜一张卡（图、时长、人物、台词、展开全文）。
 *  数据由各系列的适配脚本写（如 edu_videos/tansuo/t01_inside_a_chip/storyboard/build_preview.py）。 */
export const STORYBOARD_PREVIEW_ROUTE = "/storyboard-preview";

interface BoardScene extends StoryboardScene { question?: string }
interface Board {
  title: string; eyebrow?: string; lang?: string; version?: string; updated?: string;
  notes?: string[]; links?: { label: string; path?: string; href?: string }[]; scenes: BoardScene[];
}

export function storyboardPreviewHref(path: string): string {
  return `${STORYBOARD_PREVIEW_ROUTE}?${new URLSearchParams({ path })}`;
}

export function StoryboardPreviewPage(): JSX.Element {
  const [params] = useSearchParams();
  const path = (params.get("path") ?? "").replace(/\/+$/, "");
  const file = `${path}/storyboard/storyboard.json`;
  const [board, setBoard] = useState<Board | null>(null);
  const [error, setError] = useState("");
  const [tick, setTick] = useState(0);
  useFileChanges(path ? `${path}/storyboard` : null, () => setTick(n => n + 1));
  useEffect(() => {
    let cancelled = false;
    if (!path) { setError("链接形如 /storyboard-preview?path=edu_videos/<系列>/t01_<主题>"); return undefined; }
    fetchFile(file).then(r => { if (!cancelled) { setBoard(JSON.parse(r.content) as Board); setError(""); } })
      .catch(err => { if (!cancelled) setError(`读不到 ${file}：${String(err)}`); });
    return () => { cancelled = true; };
  }, [file, path, tick]);
  if (error) return <div className="episode-workflow"><h1>故事板</h1><p role="alert" className="workflow-error">{error}</p></div>;
  if (!board) return <p role="status">加载故事板…</p>;
  const shots = board.scenes.flatMap(s => s.shots);
  const total = shots.reduce((a, s) => a + (Number(s.duration) || 0), 0);
  const ready = shots.filter(s => s.image).length;
  return <div className="episode-workflow storyboard-wide">
    <header><div><p className="workflow-eyebrow">{board.eyebrow ?? "故事板"}{board.version ? ` · ${board.version}` : ""}{board.updated ? ` · ${board.updated}` : ""}</p>
      <h1>{board.title}</h1></div>
      <div className="workflow-header-actions">
        <Link className="workflow-header-link" to={audioPreviewHref(path, board.lang)}>音频预览</Link>
        <button type="button" onClick={() => setTick(n => n + 1)}>刷新</button></div></header>
    {board.notes?.length ? <ul className="workflow-note">{board.notes.map(n => <li key={n}>{n}</li>)}</ul> : null}
    {board.links?.length ? <p className="storyboard-links">{board.links.map(l => l.href
      ? <Link key={l.label} to={l.href}>{l.label}</Link>
      : <Link key={l.label} to={`/file/${encodeURIComponent(l.path ?? "")}`}>{l.label}</Link>)}</p> : null}
    <section className="storyboard" aria-label="故事板">
      <div className="storyboard-head">
        <h3>故事板 <span className="storyboard-muted">{board.scenes.length} 场 · {shots.length} 镜 · 图已出 {ready}/{shots.length}{total ? ` · 共 ${Math.floor(total / 60)} 分 ${total % 60} 秒` : ""}</span></h3>
        {board.scenes.length > 1 && <nav className="storyboard-jump" aria-label="跳到场次">
          {board.scenes.map(s => <a key={s.id} href={`#storyboard-${s.id}`}>{s.id}<small>{s.shots.length} 镜</small></a>)}
        </nav>}
      </div>
      {board.scenes.map(s => <section key={s.id} id={`storyboard-${s.id}`} className="storyboard-scene" aria-label={`场次 ${s.id}`}>
        <div className="storyboard-scene-head">
          <h4><span className="storyboard-scene-id">{s.id}</span>{s.location}</h4>
          <p className="storyboard-scene-meta"><span>{s.time}</span>{s.total ? <span>{s.total} 秒</span> : null}<span>{s.shots.length} 镜</span></p>
          {s.question && <p className="storyboard-purpose" title={s.question}>问：{s.question}</p>}
          <p className="storyboard-purpose" title={s.purpose}>{s.purpose}</p>
        </div>
        <ol className="storyboard-grid">{s.shots.map(shot => <ShotCard key={shot.id} shot={shot} scene={s.id} label={shot.id} lang={board.lang ?? "zh"} />)}</ol>
      </section>)}
    </section>
  </div>;
}
