import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { mediaUrl } from "../api";
import { chapterAt, clock, loadReel, startReel, type ReviewReel } from "../lib/reviewReel";

const STATE: Record<ReviewReel["state"], string> = { none: "还没有生成", running: "正在拼接", done: "已生成", failed: "拼接失败", interrupted: "上次拼接被中断" };
const POLL_MS = 2000;

/** 整集审片串联（follow-up 260）：选全集或一场，每镜最新一条拼成一条视频，右边章节列表跟着播放走。 */
export function ReviewReelPanel({ episodePath, initialScene, shotHref }: {
  episodePath: string; initialScene: string | null; shotHref: (scene: string, shot: string) => string;
}): JSX.Element {
  const [scene, setScene] = useState<string | null>(initialScene);
  const [reel, setReel] = useState<ReviewReel | null>(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [current, setCurrent] = useState(-1);
  const player = useRef<HTMLVideoElement>(null);
  const reelFor = reel && reel.episode_path === episodePath && reel.scene === scene ? reel : null;

  useEffect(() => {
    let cancelled = false;
    setError("");
    void loadReel(episodePath, scene).then(data => { if (!cancelled) setReel(data); }).catch(err => { if (!cancelled) setError(String(err)); });
    return () => { cancelled = true; };
  }, [episodePath, scene]);

  useEffect(() => {   // 后台在拼：定时查进度，拼完自动换成结果
    if (reelFor?.state !== "running") return;
    const timer = window.setTimeout(() => {
      void loadReel(episodePath, scene).then(setReel).catch(err => setError(String(err)));
    }, POLL_MS);
    return () => window.clearTimeout(timer);
  }, [reelFor, episodePath, scene]);

  const start = (): void => {
    setBusy(true); setError("");
    void startReel(episodePath, scene).then(setReel).catch(err => setError(String(err))).finally(() => setBusy(false));
  };
  const chapters = reelFor?.manifest?.chapters || [];
  const jump = (index: number): void => {
    setCurrent(index);
    const video = player.current;
    if (!video) return;
    video.currentTime = chapters[index].start + 0.01;
    void Promise.resolve(video.play?.()).catch(() => undefined);
  };
  const running = reelFor?.state === "running";
  const fresh = reelFor?.state === "done" && !reelFor.stale;

  return <section className="workflow-content review-reel" aria-label="审片串联">
    <div className="workflow-content-heading"><h2>审片串联</h2>
      <p>按分镜顺序，取每个镜头最新的一条生成，拼成一条视频一起看。没有生成的镜头跳过，列在下面。</p></div>
    <div className="review-reel-toolbar">
      <label>范围<select aria-label="范围" value={scene || ""} onChange={event => { setScene(event.target.value || null); setCurrent(-1); }}>
        <option value="">全集</option>
        {(reel?.scenes || []).map(item => <option key={item.id} value={item.id}>{item.id} · {item.label}（{item.shots} 镜）</option>)}
      </select></label>
      <button type="button" className="primary" onClick={start} disabled={busy || running || !reelFor || fresh}>
        {running ? "拼接中…" : "生成串联"}</button>
      {reelFor && <span role="status" className={`review-reel-state ${reelFor.state}`}>
        {STATE[reelFor.state]}{running ? ` ${reelFor.done}/${reelFor.total} 镜` : ""}
        {reelFor.state === "done" && reelFor.manifest ? ` · ${reelFor.manifest.created_at} · 共 ${clock(reelFor.manifest.duration)}` : ""}</span>}
    </div>
    {error && <p role="alert" className="workflow-error">{error}</p>}
    {reelFor?.state === "failed" && <p role="alert" className="workflow-error">{reelFor.error}</p>}
    {reelFor?.stale && <p className="workflow-note">有新的生成，或已用的文件变了：这条串联不是最新的。点「生成串联」更新（只重新编码有变化的镜头）。</p>}
    {reelFor?.manifest && reelFor.video_path && <div className="review-reel-body">
      <video ref={player} className="review-reel-video" controls preload="metadata" aria-label="串联视频"
        src={mediaUrl(reelFor.video_path, Date.parse(reelFor.manifest.created_at.replace(" ", "T")) || 0)}
        onTimeUpdate={event => setCurrent(chapterAt(chapters, event.currentTarget.currentTime))} />
      <ol className="review-reel-chapters" aria-label="章节">
        {chapters.map((chapter, index) => <li key={chapter.key} className={index === current ? "current" : ""} aria-current={index === current ? "true" : undefined}>
          <button type="button" onClick={() => jump(index)}>
            <span className="review-reel-time">{clock(chapter.start)}</span>
            <strong>{chapter.key}</strong>
            <span className="review-reel-meta">{chapter.duration.toFixed(1)} 秒{chapter.review_status ? ` · ${chapter.review_status}` : ""}</span>
            {chapter.note && <span className="review-reel-note">{chapter.note}</span>}
          </button>
          <Link to={shotHref(chapter.scene, chapter.key)}>镜头页</Link>
        </li>)}
      </ol>
    </div>}
    {reelFor?.manifest?.skipped.length ? <div className="review-reel-skipped"><h3>跳过的镜头（{reelFor.manifest.skipped.length}）</h3>
      <ul>{reelFor.manifest.skipped.map(item => <li key={item.key}>{item.key} · {item.reason}</li>)}</ul></div> : null}
  </section>;
}
