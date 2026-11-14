import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchFile, mediaUrl } from "../api";
import { groupPreviewHref } from "../lib/groupPreview";
import { boardIndexPath, boardStripPath, groupRuns, scenePreviewHref, type SceneBoard } from "../lib/sceneBoard";
import "./HeroPreviewPage.css";
import "./SceneBoardPage.css";

const fileHref = (path: string): string => `/file/${encodeURIComponent(path)}`;

/** The scene storyboard strip (follow-up 336/339): used by /scene-preview and inside the scene view of the episode page. */
export function SceneBoardView({ scenePath, revision, compact = false }: { scenePath: string; revision: number; compact?: boolean }): JSX.Element | null {
  const [board, setBoard] = useState<SceneBoard | null>(null);
  const [missing, setMissing] = useState(false);
  // 格子图文件名不变（p01_st1.jpg），重建时 scene_board.json 一起重写：用它的修改时间做图片版本号，重建后刷新即见新图（follow-up 336）
  const [version, setVersion] = useState(0);
  useEffect(() => {
    let cancelled = false;
    fetchFile(boardIndexPath(scenePath)).then(f => { if (!cancelled) { setBoard(JSON.parse(f.content) as SceneBoard); setVersion(f.mtime || 0); setMissing(false); } },
      () => { if (!cancelled) { setBoard(null); setMissing(true); } });
    return () => { cancelled = true; };
  }, [scenePath, revision]);
  if (missing) return compact ? null : <p className="hero-preview-empty">还没有场故事板。</p>;
  if (!board) return null;
  return <section className="scene-board-view" aria-label="场故事板">
    <p className="hero-preview-meta">
      <strong>场故事板</strong><span>{board.panels.length} 镜</span><span>总长 {board.total} 秒</span>
      {compact && <Link to={scenePreviewHref(scenePath)}>单独打开</Link>}
      <Link to={fileHref(boardStripPath(scenePath))}>整场图</Link>
    </p>
    <div className="scene-board-strip" role="list">
      {groupRuns(board.panels).map((run, r) => <div key={r} className="scene-board-run">
        <div className="scene-board-run-label">
          {run.group
            ? <Link to={groupPreviewHref(`${scenePath}/groups/${run.group}`)}>镜组 {run.group} · {run.panels[0].start}–{run.panels[run.panels.length - 1].end} 秒</Link>
            : <span>单镜（未分组）</span>}
        </div>
        <div className="scene-board-cards">
          {run.panels.map(p => <article key={p.shot} className="scene-board-card" role="listitem">
            <a href={mediaUrl(p.image, version || revision)} target="_blank" rel="noreferrer"><img src={mediaUrl(p.image, version || revision)} alt={`${p.shot} 故事板`} loading="lazy" /></a>
            <p className="scene-board-text">{p.text}</p>
            {p.dialogue && <p className="scene-board-dialogue">{p.dialogue}</p>}
            <p className="scene-board-time">{p.start}–{p.end} 秒 · {p.shot}{p.group ? ` · 第 ${p.cell} 格` : ""}</p>
          </article>)}
        </div>
      </div>)}
    </div>
  </section>;
}
