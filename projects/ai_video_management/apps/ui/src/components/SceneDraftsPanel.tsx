/**
 * A scene's drafts at a glance (follow-up 267): one tile per shot, in shot order, playing that shot's latest draft
 * (the takes under `drafts/`, follow-up 266) as a muted thumbnail. Clicking a tile opens an enlarged preview with
 * sound and the 通过 / 不通过 verdict; ← / → step to the neighbouring shot's draft, Esc closes.
 * The same grid serves the 正片 tab (follow-up 273): `stage="final"` shows each shot's latest final take (`renders/`).
 */
import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { mediaUrl } from "../api";
import { judgeTake, type PromptScene, type ShotTake } from "../lib/episodeWorkflow";

export type TakeStage = "draft" | "final";

const isDraft = (take: ShotTake): boolean => take.generation.stage === "draft" || take.path.includes("/drafts/");
const ofStage = (stage: TakeStage) => (take: ShotTake): boolean => stage === "draft" ? isDraft(take) : !isDraft(take);
const NAME: Record<TakeStage, string> = { draft: "草稿", final: "正片" };
const PASS: Record<TakeStage, string> = { draft: "通过，可出正式条", final: "通过" };

interface Tile { key: string; drafts: ShotTake[]; latest: ShotTake | null }

function play(video: HTMLVideoElement): void {
  try { void video.play()?.catch(() => undefined); } catch { /* 浏览器不让自动播就停在首帧 */ }
}

export function SceneDraftsPanel({ scene, takes, shotHref, onJudged, stage = "draft" }: {
  scene: PromptScene;
  takes?: Record<string, ShotTake[]>;
  shotHref: (shot: string) => string;
  onJudged: () => void;
  stage?: TakeStage;
}): JSX.Element {
  const name = NAME[stage];
  const tiles: Tile[] = scene.shots.map(shot => {
    const drafts = (takes?.[shot.id] || []).filter(ofStage(stage));   // 接口给的是新的在前
    return { key: shot.id, drafts, latest: drafts[0] || null };
  });
  const withDraft = tiles.filter(tile => tile.latest);
  const [open, setOpen] = useState<string | null>(null);
  return <section className="scene-drafts" aria-label={name}>
    <p className="workflow-note">{tiles.length} 镜 · {withDraft.length} 镜有{name}{stage === "final" ? " · 每格是这一镜最新的一条正式条" : ""}</p>
    <ul className="scene-drafts-grid" aria-label={`${scene.id} ${name}`}>
      {tiles.map(tile => <li key={tile.key} data-shot={tile.key} className={tile.latest ? "scene-draft" : "scene-draft empty"}>
        {tile.latest ? <button type="button" className="scene-draft-thumb" aria-label={`放大 ${tile.key}`} onClick={() => setOpen(tile.key)}>
          <video src={`${mediaUrl(tile.latest.videos[0])}#t=0.5`} muted playsInline preload="metadata" loop
            onMouseEnter={event => play(event.currentTarget)} onMouseLeave={event => event.currentTarget.pause()} />
        </button> : <div className="scene-draft-thumb missing">还没有{name}</div>}
        <div className="scene-draft-caption"><strong>{tile.key}</strong>
          {tile.latest && <><span className="workflow-take-status">{tile.latest.review_status || "待审核"}</span>
            <span className="workflow-pack-path">{tile.drafts.length} 条{name}</span></>}</div>
      </li>)}
    </ul>
    {open && <DraftPreview tiles={withDraft} current={open} onMove={setOpen} onClose={() => setOpen(null)} shotHref={shotHref} onJudged={onJudged} stage={stage} />}
  </section>;
}

function DraftPreview({ tiles, current, onMove, onClose, shotHref, onJudged, stage }: {
  tiles: Tile[]; current: string; onMove: (key: string) => void; onClose: () => void; shotHref: (shot: string) => string; onJudged: () => void;
  stage: TakeStage;
}): JSX.Element | null {
  const dialog = useRef<HTMLDivElement>(null);
  const [busy, setBusy] = useState(false);
  const [failure, setFailure] = useState("");
  useEffect(() => { dialog.current?.focus(); setFailure(""); }, [current]);
  const index = tiles.findIndex(tile => tile.key === current);
  const tile = tiles[index];
  if (!tile?.latest) return null;
  const take = tile.latest;
  const step = (by: number) => { const next = tiles[index + by]; if (next) onMove(next.key); };
  const judge = (verdict: "通过" | "不通过") => {
    setBusy(true); setFailure("");
    void judgeTake(take.path, verdict).then(onJudged).catch(err => setFailure(String(err))).finally(() => setBusy(false));
  };
  return <div className="scene-draft-backdrop" onClick={onClose}>
    <div ref={dialog} role="dialog" aria-modal="true" aria-label={`${NAME[stage]}预览 ${tile.key}`} tabIndex={-1} className="scene-draft-dialog"
      onClick={event => event.stopPropagation()}
      onKeyDown={event => {
        if (event.key === "Escape") onClose();
        else if (event.key === "ArrowRight") step(1);
        else if (event.key === "ArrowLeft") step(-1);
      }}>
      <header><strong>{tile.key}</strong> <span className="workflow-take-status">{take.review_status || "待审核"}</span>
        <span className="workflow-pack-path"> · {take.id}{take.generation.resolution ? ` · ${take.generation.resolution}` : ""}</span>
        <button type="button" className="scene-draft-close" aria-label="关闭" onClick={onClose}>×</button></header>
      <video key={take.path} src={mediaUrl(take.videos[0])} controls autoPlay preload="auto" aria-label={`放大的${NAME[stage]}`} className="scene-draft-player" />
      {failure && <p role="alert" className="workflow-error">{failure}</p>}
      <footer>
        <button type="button" disabled={index <= 0} onClick={() => step(-1)}>← 上一镜</button>
        <button type="button" disabled={busy} onClick={() => judge("通过")}>{PASS[stage]}</button>
        <button type="button" disabled={busy} onClick={() => judge("不通过")}>不通过</button>
        <Link to={shotHref(tile.key)}>打开镜头页</Link>
        <button type="button" disabled={index >= tiles.length - 1} onClick={() => step(1)}>下一镜 →</button>
      </footer>
    </div>
  </div>;
}
