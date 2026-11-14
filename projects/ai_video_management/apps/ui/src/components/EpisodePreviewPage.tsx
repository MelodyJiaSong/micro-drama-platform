import { useEffect, useMemo, useRef, useState, type VideoHTMLAttributes } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { fetchFile, fetchSubtree, mediaUrl } from "../api";
import { useFileChanges } from "../lib/fileEvents";
import { reviewStatus } from "../lib/groupPreview";
import { loadSceneCuts, type CutVersion, type EpisodeCuts, type EpisodeJoin } from "../lib/sceneCuts";
import {
  clock, episodeNumber, groupOf, latestJoin, latestSceneCut, parseDialogue, parseEpisodePath, pickTake, previewFile, shotAt, shotStart, takesFromTree,
  verdictFromStatus, VERDICT_LABEL, type FilmingScene, type Line, type PreviewNotes, type TakeFiles, type Verdict,
} from "../lib/episodePreview";
import { EpisodeFilmPreview } from "./EpisodeFilmPreview";
import { reviewRunHref } from "../lib/reviewRun";
import "./EpisodePreviewPage.css";

const fileHref = (path: string): string => `/file/${encodeURIComponent(path)}`;

async function readJson<T>(path: string): Promise<T | null> {
  try { return JSON.parse((await fetchFile(path)).content) as T; } catch { return null; }
}
async function readText(path: string | null): Promise<string> {
  if (!path) return "";
  try { return (await fetchFile(path)).content; } catch { return ""; }
}

interface ShotView {
  key: string; scene: string; shot: string; duration: number; take: TakeFiles | null; start: number; group: string | null;
  lines: Line[]; verdict: Verdict; note: string; cutIn: number | null; cutOut: number | null; cutReason: string;
}
interface Loaded {
  film?: false; notes: PreviewNotes; scenes: FilmingScene[]; shots: ShotView[]; cuts: EpisodeCuts | null;
  join: EpisodeJoin | null; sceneCuts: Record<string, CutVersion | null>;
}

/** 成片模式（follow-up 328）：没有 filming.json、preview.json 给了 video */
interface FilmLoaded { film: true; notes: PreviewNotes }

async function load(episodePath: string, lang: string | null, audio = false): Promise<Loaded | FilmLoaded> {
  if (audio) {   // 音频预览（follow-up 359）：只读 audio_preview.json，与有没有 filming.json 无关
    const notes = await readJson<PreviewNotes>(previewFile(episodePath, lang, true));
    if (!notes?.audio) throw new Error(`还没有音频预览：先运行 python tools/audio_preview.py build（读不到 ${previewFile(episodePath, lang, true)}）`);
    return { film: true, notes };
  }
  const [filming, notes, cuts] = await Promise.all([
    readJson<{ content: { scenes: FilmingScene[] } }>(`${episodePath}/filming.json`),
    readJson<PreviewNotes>(previewFile(episodePath, lang)),
    loadSceneCuts(episodePath).catch(() => null),
  ]);
  if (!filming && notes?.video) return { film: true, notes };
  if (!filming) throw new Error(`读不到 ${episodePath}/filming.json，也没有带 video 的 preview.json（单集预览支持三模块剧，或成片模式）`);
  const n = notes ?? {};
  const scenes = filming.content.scenes;
  const sceneCuts = Object.fromEntries(scenes.map(sc => [sc.id, latestSceneCut(cuts, sc.id)]));
  const shots = await Promise.all(scenes.flatMap(sc => sc.shots.map(async sh => {
    const key = `${sc.id}_${sh.id}`;
    const own = await fetchSubtree(`${episodePath}/scenes/${sc.id}/shots/${sh.id}/renders`, 2).catch(() => null);
    const ev = sceneCuts[sc.id]?.events.find(e => e.shot === sh.id && !e.placeholder) ?? null;
    const ownTakes = takesFromTree(own);
    let take = pickTake(ownTakes, ev?.take ?? null);
    let start = ev?.cut_in ?? 0;
    // 镜组的镜头（follow-up 331）：条在 groups/gN/renders，这一镜从镜组条的第 offset 秒开始。
    // 只有本场剪辑明确用的是这一镜自己的条时才用它，否则用镜组的条（旧的单镜条留作备用）
    const grp = groupOf(sc, sh.id);
    const cutUsesOwn = !!ev && ownTakes.some(x => x.name === ev.take);
    if (grp && !cutUsesOwn) {
      const gtree = await fetchSubtree(`${episodePath}/scenes/${sc.id}/groups/${grp.id}/renders`, 2).catch(() => null);
      const gtake = pickTake(takesFromTree(gtree), ev?.take ?? null);
      if (gtake) { take = gtake; start = ev?.cut_in ?? grp.offset; }
    }
    const preset = n.shots?.[key];
    const verdict = preset?.verdict ?? verdictFromStatus(reviewStatus(await readText(take?.review ?? null)));
    return {
      key, scene: sc.id, shot: sh.id, duration: sh.duration, take, start, group: grp?.id ?? null, verdict, note: preset?.note ?? "",
      lines: parseDialogue(sh.dialogue ?? "", n.glosses), cutIn: ev?.cut_in ?? null, cutOut: ev?.cut_out ?? null,
      cutReason: ev?.reason ?? "",
    };
  })));
  return { notes: n, scenes, shots, cuts, join: latestJoin(cuts), sceneCuts };
}

function Lines({ lines }: { lines: Line[] }): JSX.Element {
  if (!lines.length) return <p className="ep-line ep-mute">无对白</p>;
  return <>{lines.map((l, i) => <p key={i} className={`ep-line${l.foreign ? " ep-foreign" : ""}`}>
    <b>{l.who}</b><span>{l.text}</span>{l.gloss && <em>{l.gloss}</em>}
  </p>)}</>;
}

/** 滚到附近才挂上 <video>：一页二三十条视频同时取元数据会把浏览器的媒体连接占满、页面卡死。 */
function LazyVideo(props: VideoHTMLAttributes<HTMLVideoElement>): JSX.Element {
  const box = useRef<HTMLDivElement>(null);
  const [near, setNear] = useState(typeof IntersectionObserver === "undefined");
  useEffect(() => {
    if (near || !box.current) return;
    const io = new IntersectionObserver(es => { if (es.some(e => e.isIntersecting)) { setNear(true); io.disconnect(); } }, { rootMargin: "200px" });
    io.observe(box.current);
    return () => io.disconnect();
  }, [near]);
  return <div ref={box} className="ep-lazy">{near ? <video preload="metadata" {...props} /> : null}</div>;
}

export function EpisodePreviewPage(): JSX.Element {
  const [params] = useSearchParams();
  const path = (params.get("path") ?? "").replace(/\/+$/, "");
  const loc = parseEpisodePath(path);
  const lang = params.get("lang");
  const audio = params.get("audio") === "1";
  const [loaded, setData] = useState<Loaded | FilmLoaded | null>(null);
  const data = loaded && !loaded.film ? loaded : null;
  const [error, setError] = useState<string | null>(null);
  const [revision, refresh] = useState(Date.now);
  useFileChanges(loc ? path : null, () => refresh(Date.now()));
  useEffect(() => {
    let cancelled = false;
    setError(null);
    if (!loc) { setError("链接形如 /episode-preview?path=ai_videos/<剧>/episodes/ep01，或教学视频 edu_videos/<系列>/t01_<主题>"); return; }
    load(path, lang, audio).then(d => { if (!cancelled) setData(d); })
      .catch(reason => { if (!cancelled) setError(reason instanceof Error ? reason.message : String(reason)); });
    return () => { cancelled = true; };
  }, [path, lang, audio, revision]);   // eslint-disable-line react-hooks/exhaustive-deps

  // 播放器：整集成片（有集级正片剪辑时）或逐镜连播
  const [mode, setMode] = useState<"episode" | "shots">("episode");
  const [index, setIndex] = useState(0);
  const [now, setNow] = useState(0);
  const video = useRef<HTMLVideoElement>(null);
  const pending = useRef<number | null>(null);
  const [inline, setInline] = useState<string | null>(null);   // 分场里就地播放的镜头（不跳到顶部播放器）
  const playable = useMemo(() => (data?.shots ?? []).filter(s => s.take?.video), [data]);
  const episodeMode = mode === "episode" && !!data?.join?.video;
  const current = episodeMode ? shotAt(now, data!.join, data!.sceneCuts)?.key ?? null : playable[index]?.key ?? null;
  const currentShot = data?.shots.find(s => s.key === current) ?? null;

  if (error) return <section className="ep-page"><h1>单集预览</h1><p role="alert" className="ep-alert">{error}</p></section>;
  if (loaded?.film && loc) return <EpisodeFilmPreview path={path} lang={lang} audio={audio} dramaPath={loc.dramaPath} episode={loc.episode} notes={loaded.notes} revision={revision} />;
  if (!data || !loc) return <p role="status">加载单集预览…</p>;

  const { notes, scenes, shots, join, sceneCuts } = data;
  const ep = episodeNumber(loc.episode);
  const total = shots.reduce((a, s) => a + s.duration, 0);
  const count = (v: Verdict): number => shots.filter(s => s.verdict === v).length;
  const src = episodeMode ? mediaUrl(join!.video, revision) : playable[index]?.take?.video ? mediaUrl(playable[index].take!.video!, revision) : "";

  const play = (key: string): void => {
    if (episodeMode) {
      const t = shotStart(key, join, sceneCuts);
      if (t !== null && video.current) { video.current.currentTime = t + 0.05; void video.current.play().catch(() => undefined); }
    } else {
      const i = playable.findIndex(s => s.key === key);
      if (i >= 0) { setIndex(i); pending.current = playable[i].start; }
    }
    video.current?.scrollIntoView({ behavior: "smooth", block: "center" });
  };
  const next = (): void => {
    const nx = playable[index + 1];
    if (!nx) return;
    const sameVideo = nx.take?.video === playable[index]?.take?.video;
    setIndex(index + 1);
    if (sameVideo && video.current) video.current.currentTime = nx.start;   // 同一条镜组视频：接着放
    else pending.current = nx.start;
  };
  const switchMode = (m: "episode" | "shots"): void => { setMode(m); setNow(0); pending.current = null; };

  return <section className="ep-page">
    <header className="ep-hero">
      <p className="ep-eyebrow">单集预览 · EP{ep} · <Link to={`/drama?drama=${encodeURIComponent(loc.dramaPath)}`}>{loc.dramaPath.split("/")[1]}</Link> · <Link to={reviewRunHref(`${loc.dramaPath}/episodes/${loc.episode}`)}>审查单</Link></p>
      <h1>{notes.title ?? `EP${ep}`}</h1>
      {notes.tagline && <p className="ep-tagline">{notes.tagline}</p>}
      <ul className="ep-stats">
        <li><b>{join ? clock(join.duration) : clock(total)}</b>{join ? "整集成片" : "各镜合计"}</li>
        <li><b>{scenes.length}</b>场</li>
        <li><b>{shots.length}</b>镜</li>
        <li><b>{count("ok")}</b>保留</li>
        {count("note") > 0 && <li><b>{count("note")}</b>有备注</li>}
        {count("redo") > 0 && <li className="ep-warn"><b>{count("redo")}</b>要重出</li>}
        {count("pending") > 0 && <li><b>{count("pending")}</b>未审</li>}
      </ul>
      <p className="ep-links">
        <Link to={`/drama?drama=${encodeURIComponent(loc.dramaPath)}&episode=${loc.episode}&module=edit`}>剪辑模块（时间线与剪辑理由）</Link>
        {join && <Link to={fileHref(join.path)}>整集剪辑决定</Link>}
        <Link to={fileHref(`${path}/preview.json`)}>本页说明数据</Link>
      </p>
    </header>

    <section className="ep-player" aria-label="播放器">
      <div className="ep-modes" role="tablist">
        {join?.video && <button type="button" role="tab" aria-selected={episodeMode} onClick={() => switchMode("episode")}>
          整集成片 v{join.version} · {join.phase} · {clock(join.duration)}</button>}
        <button type="button" role="tab" aria-selected={!episodeMode} onClick={() => switchMode("shots")}>逐镜连播（原始正式条）</button>
      </div>
      {src ? <video ref={video} key={src} controls preload="metadata" src={src} onPlay={() => setInline(null)}
        onLoadedMetadata={() => { if (pending.current !== null && video.current) { video.current.currentTime = pending.current; void video.current.play().catch(() => undefined); pending.current = null; } }}
        onTimeUpdate={e => {
          const t = e.currentTarget.currentTime; setNow(t);
          const cur = playable[index];
          if (!episodeMode && cur && t >= cur.start + cur.duration && index < playable.length - 1) next();
        }}
        onEnded={() => { if (!episodeMode && index < playable.length - 1) next(); }} />
        : <p className="ep-empty">还没有可播放的正式条。</p>}
      <div className="ep-timeline" aria-label="时间线">
        {(episodeMode ? shots.filter(s => shotStart(s.key, join, sceneCuts) !== null) : playable).map(s =>
          <button key={s.key} type="button" className={`ep-seg ep-${s.scene}${s.key === current ? " ep-on" : ""}`}
            style={{ flexGrow: episodeMode && s.cutIn !== null && s.cutOut !== null ? s.cutOut - s.cutIn : s.duration }}
            title={`${s.scene} ${s.shot}`} aria-label={`跳到 ${s.scene} ${s.shot}`} onClick={() => play(s.key)} />)}
      </div>
      {currentShot && <div className="ep-now">
        <p className="ep-now-id">{currentShot.scene.toUpperCase()} · {notes.scenes?.[currentShot.scene]?.title ?? ""} · {currentShot.shot}</p>
        <Lines lines={currentShot.lines} />
      </div>}
      {episodeMode && join?.note && <p className="ep-mute">{join.note}</p>}
    </section>

    {notes.cast?.length ? <section className="ep-cast" aria-label="人物">
      <h2>人物</h2>
      <div className="ep-cast-row">{notes.cast.map(c => <figure key={c.name}>
        {c.image && <img src={mediaUrl(c.image, revision)} alt={`${c.name} 定妆`} loading="lazy" />}
        <figcaption><b>{c.name}</b>{c.role && <span>{c.role}</span>}{c.desc && <small>{c.desc}</small>}</figcaption>
      </figure>)}</div>
    </section> : null}

    <section aria-label="分场">
      <h2>分场</h2>
      {scenes.map(sc => {
        const meta = notes.scenes?.[sc.id] ?? {};
        const cut = sceneCuts[sc.id];
        const own = shots.filter(s => s.scene === sc.id);
        return <article key={sc.id} className={`ep-scene ep-${sc.id}`} id={sc.id}>
          <header>
            <span className="ep-scene-num">{sc.id.toUpperCase()}</span>
            <div>
              <h3>{meta.title ?? sc.location}{meta.subtitle && <small>{meta.subtitle}</small>}</h3>
              <p className="ep-mute">{meta.time ?? sc.time} · {own.length} 镜 · {cut ? `剪辑 ${cut.duration.toFixed(1)}s` : `${own.reduce((a, s) => a + s.duration, 0)}s`}</p>
              {(meta.summary ?? sc.purpose) && <p>{meta.summary ?? sc.purpose}</p>}
            </div>
          </header>
          {cut?.video && <div className="ep-scene-cut">
            <LazyVideo controls src={mediaUrl(cut.video, revision)} />
            <p className="ep-mute">本场剪辑 v{cut.version} · {cut.phase} · {cut.status} · {cut.duration.toFixed(1)}s ·{" "}
              <Link to={fileHref(cut.path)}>剪辑决定</Link>{cut.labeled_video && <> · <Link to={fileHref(cut.labeled_video)}>带标注版</Link></>}</p>
          </div>}
          <div className="ep-shots">{own.map(s => <div key={s.key} className={`ep-shot${s.key === current ? " ep-on" : ""}`}>
            {inline === s.key && s.take?.video
              ? <video className="ep-inline" controls autoPlay src={mediaUrl(s.take.video, revision)} aria-label={`正在播放 ${s.scene} ${s.shot}`}
                  onLoadedMetadata={e => { e.currentTarget.currentTime = s.start; }}
                  onTimeUpdate={e => { if (e.currentTarget.currentTime >= s.start + s.duration) e.currentTarget.pause(); }} />
              : <button type="button" className="ep-thumb" onClick={() => { video.current?.pause(); setInline(s.key); }} disabled={!s.take?.video} aria-label={`播放 ${s.scene} ${s.shot}`}>
                  {s.take?.video ? <LazyVideo muted src={`${mediaUrl(s.take.video, revision)}#t=${(s.start + 0.8).toFixed(2)}`} /> : <span>没有正式条</span>}
                  <span className="ep-dur">{s.duration}s</span>
                </button>}
            <p className="ep-shot-meta"><b>{s.shot}</b>{s.group && <span className="ep-mute">镜组 {s.group}</span>}<span className={`ep-chip ep-v-${s.verdict}`}>{VERDICT_LABEL[s.verdict]}</span>
              {s.take?.review && <Link to={fileHref(s.take.review)}>审片记录</Link>}</p>
            <Lines lines={s.lines} />
            {s.note && <p className="ep-note">{s.note}</p>}
            {s.cutReason && <details className="ep-cut"><summary>剪辑：用 {s.cutIn?.toFixed(2)}–{s.cutOut?.toFixed(2)}s</summary><p>{s.cutReason}</p></details>}
          </div>)}</div>
        </article>;
      })}
    </section>

    {notes.notes?.length ? <section className="ep-notes" aria-label="说明">
      {notes.notes.map(g => <div key={g.title}><h2>{g.title}</h2><ul>{g.items.map(i => <li key={i}>{i}</li>)}</ul></div>)}
    </section> : null}
  </section>;
}
