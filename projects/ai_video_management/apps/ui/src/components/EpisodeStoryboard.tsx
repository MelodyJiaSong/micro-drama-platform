import { useEffect, useMemo, useState, type ReactNode } from "react";
import { Link } from "react-router-dom";
import { fetchReviewRuns, mediaUrl, type ReviewRunSummary } from "../api";
import type { EpisodeWorkflow } from "../lib/episodeWorkflow";
import {
  latestSceneReview, reviewChipText, reviewChipTone, storyboardScenes, type StoryboardScene, type StoryboardShot,
} from "../lib/episodeStoryboard";
import { useFileChanges } from "../lib/fileEvents";
import { reviewRunHref } from "../lib/reviewRun";
import { ZoomableImage } from "./ZoomableImage";
import "./EpisodeStoryboard.css";

const fileHref = (path: string): string => `/file/${encodeURIComponent(path)}`;

/** 一镜一张卡：首帧图（16:9，点开看大图）、镜头、时长、人物、整句台词、行动摘要，「展开」看全文。 */
export function ShotCard({ shot, scene, shotHref, lang = "en", label: given }: { shot: StoryboardShot; scene: string; shotHref?: (scene: string, key: string) => string; lang?: string; label?: string }): JSX.Element {
  const [broken, setBroken] = useState(false);
  const [open, setOpen] = useState(false);
  useEffect(() => setBroken(false), [shot.image?.path, shot.image?.mtime]);
  const label = given ?? `${scene}_${shot.id}`;
  const image = shot.image && !broken ? shot.image : null;
  return <li className="storyboard-card" aria-label={`镜头 ${label}`}>
    <div className="storyboard-frame">
      {image
        ? <ZoomableImage src={mediaUrl(image.path, image.mtime)} alt={`${label} 首帧`} loading="lazy" onError={() => setBroken(true)} />
        : <div className="storyboard-placeholder" role="img" aria-label={`${label} 首帧待出`}><span>首帧待出</span></div>}
    </div>
    <div className="storyboard-card-body">
      <p className="storyboard-card-title">
        {shotHref ? <Link to={shotHref(scene, shot.key)} title={`${shot.key}：打开本镜分镜全文`}><strong>{label}</strong></Link> : <strong title={shot.key}>{label}</strong>}
        <span className="storyboard-duration">{shot.duration ? `${shot.duration} 秒` : "时长待定"}</span>
        {shot.cast.length ? shot.cast.map(c => <span key={c} className="storyboard-cast">{c}</span>) : <span className="storyboard-muted">无人物</span>}
      </p>
      {shot.dialogue.length > 0 ? <ul className="storyboard-dialogue" aria-label="台词">
        {shot.dialogue.map((line, i) => <li key={i}>
          {line.speaker && <span className="storyboard-speaker" title={line.direction || undefined}>{line.speaker}{line.direction ? <small>（{line.direction}）</small> : null}</span>}
          <q lang={lang}>{line.text}</q>
        </li>)}
      </ul> : <p className="storyboard-muted">无对白</p>}
      {open ? <dl className="storyboard-full">
        <dt>行动</dt><dd>{shot.action || "—"}</dd>
        <dt>走位</dt><dd>{shot.blocking || "—"}</dd>
        <dt>动作分拍</dt><dd>{shot.beats || "—"}</dd>
        <dt>拍摄</dt><dd>{shot.camera || "—"}</dd>
      </dl> : <p className="storyboard-action">{shot.action}</p>}
      <button type="button" className="storyboard-toggle" aria-expanded={open} onClick={() => setOpen(v => !v)}>{open ? "收起" : "展开"}</button>
      <p className="storyboard-links">
        {shot.packPrompt ? <Link to={fileHref(shot.packPrompt)}>资料包/prompt.txt</Link> : <span className="storyboard-muted">资料包未建</span>}
        {shot.image ? <Link to={fileHref(shot.image.path)} title="planning 目录：首帧图与同目录文件">planning/</Link> : null}
        {shot.framePrompt ? <Link to={fileHref(shot.framePrompt)}>首帧 prompt</Link> : null}
      </p>
    </div>
  </li>;
}

function ReviewChip({ run }: { run: ReviewRunSummary | null }): JSX.Element {
  const text = reviewChipText(run);
  const tone = reviewChipTone(run);
  return run
    ? <Link className={`storyboard-chip ${tone}`} to={reviewRunHref(run.dir)} title={run.title}>{text}</Link>
    : <span className={`storyboard-chip ${tone}`}>{text}</span>;
}

/** 故事板审阅（follow-up 336）：每场一节（场次、地点时间、本场目的、总秒数、镜数、出片前审查状态），下面每镜一张卡。
 *  图只取各镜现行首帧（planning/<镜>_first_frame.png），按文件修改时间换 URL，重画后刷新即见新图；没出的显示「首帧待出」。 */
export function EpisodeStoryboard({ workflow, dramaPath, episode, scene, refresh = 0, shotHref, sceneExtra }: {
  workflow: EpisodeWorkflow; dramaPath: string; episode: string; scene?: string | null; refresh?: number;
  shotHref?: (scene: string, key: string) => string; sceneExtra?: (scene: string) => ReactNode;
}): JSX.Element {
  const [runs, setRuns] = useState<ReviewRunSummary[]>([]);
  const [runsTick, setRunsTick] = useState(0);
  useFileChanges(`${dramaPath}/reviews`, () => setRunsTick(n => n + 1));
  useEffect(() => {
    let cancelled = false;
    void fetchReviewRuns().then(data => { if (!cancelled) setRuns(data.runs); }).catch(() => undefined);
    return () => { cancelled = true; };
  }, [refresh, runsTick]);
  const scenes: StoryboardScene[] = useMemo(() => storyboardScenes(workflow).filter(s => !scene || s.id === scene), [workflow, scene]);
  const shots = scenes.flatMap(s => s.shots);
  const ready = shots.filter(s => s.image).length;
  return <section className="storyboard" aria-label="故事板">
    <div className="storyboard-head">
      <h3>故事板 <span className="storyboard-muted">每镜现行首帧 · {scenes.length} 场 · {shots.length} 镜 · 首帧已出 {ready}/{shots.length}</span></h3>
      <p className="storyboard-muted">图取各镜 <code>planning/&lt;镜&gt;_first_frame.png</code>，重画后刷新即是新图；旧版（_r1、_v2_old、_obsolete）不显示。</p>
      {scenes.length > 1 && <nav className="storyboard-jump" aria-label="跳到场次">
        {scenes.map(s => <a key={s.id} href={`#storyboard-${s.id}`}>{s.id}<small>{s.shots.filter(x => x.image).length}/{s.shots.length}</small></a>)}
      </nav>}
    </div>
    {scenes.map(s => {
      const run = latestSceneReview(runs, dramaPath, episode, s.id);
      return <section key={s.id} id={`storyboard-${s.id}`} className="storyboard-scene" aria-label={`场次 ${s.id}`}>
        <div className="storyboard-scene-head">
          <h4><span className="storyboard-scene-id">{s.id}</span>{s.location}</h4>
          <ReviewChip run={run} />
          <p className="storyboard-scene-meta"><span>{s.time}</span><span>{s.total} 秒</span><span>{s.shots.length} 镜</span></p>
          <p className="storyboard-purpose" title={s.purpose}>{s.purpose}</p>
        </div>
        {sceneExtra?.(s.id)}
        <ol className="storyboard-grid">{s.shots.map(shot => <ShotCard key={shot.id} shot={shot} scene={s.id} shotHref={shotHref} />)}</ol>
      </section>;
    })}
    {!scenes.length && <p className="storyboard-muted">尚无分镜。</p>}
  </section>;
}
