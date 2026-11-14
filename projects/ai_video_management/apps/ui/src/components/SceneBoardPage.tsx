import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { fetchFile } from "../api";
import { useFileChanges } from "../lib/fileEvents";
import { boardIndexPath, parseScenePath, type SceneBoard } from "../lib/sceneBoard";
import { SceneBoardView } from "./SceneBoardView";
import "./HeroPreviewPage.css";
import "./SceneBoardPage.css";

const fileHref = (path: string): string => `/file/${encodeURIComponent(path)}`;

export function SceneBoardPage(): JSX.Element {
  const [params] = useSearchParams();
  const path = (params.get("path") ?? "").replace(/\/+$/, "");
  const loc = parseScenePath(path);
  const [board, setBoard] = useState<SceneBoard | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [revision, refresh] = useState(Date.now);
  useFileChanges(loc ? path : null, () => refresh(Date.now()));
  useEffect(() => {
    let cancelled = false;
    setError(null);
    if (!loc) { setError("链接形如 /scene-preview?path=ai_videos/<剧>/episodes/ep01/scenes/s1"); return; }
    fetchFile(boardIndexPath(path)).then(f => { if (!cancelled) setBoard(JSON.parse(f.content) as SceneBoard); },
      () => { if (!cancelled) setError(`还没有场故事板：跑 python tools/scene_board.py ${loc.episodePath}`); });
    return () => { cancelled = true; };
  }, [path, revision]);   // eslint-disable-line react-hooks/exhaustive-deps
  if (error) return <section className="hero-preview-page"><h1>场故事板</h1><p role="alert">{error}</p></section>;
  if (!board || !loc) return <p role="status">加载场故事板…</p>;
  return <section className="hero-preview-page scene-board-page">
    <header>
      <h1>场故事板 · {board.scene} · {board.location}</h1>
      <p className="hero-preview-meta"><span>{board.time}</span><Link to={fileHref(boardIndexPath(path))}>scene_board.json</Link></p>
      <p className="hero-preview-meta">只给 review 用，不上传；每格取自所属镜组的镜组板，改了镜组板会自动跟着更新。</p>
    </header>
    <SceneBoardView scenePath={path} revision={revision} />
  </section>;
}
