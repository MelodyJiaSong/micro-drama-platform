import { useRef, useState } from "react";
import { Link } from "react-router-dom";
import { mediaUrl } from "../api";
import { clock, episodeNumber, filmIndexAt, FLAG_LABEL, isEduPath, previewFile, type FilmItem, type PreviewNotes, type Verdict } from "../lib/episodePreview";

const fileHref = (path: string): string => `/file/${encodeURIComponent(path)}`;

/** 单集预览页的成片模式（follow-up 328）：没有 filming.json 的系列，preview.json 给成片、章节与逐段说明。
 *  音频预览（follow-up 359）：audio_preview.json 给整集配音，播放器上方大图换成当前段的故事板、叠当前那句台词，进度条与逐段卡片同成片模式。 */
export function EpisodeFilmPreview({ path, lang, audio = false, dramaPath, episode, notes, revision }: {
  path: string; lang?: string | null; audio?: boolean; dramaPath: string; episode: string; notes: PreviewNotes; revision: number;
}): JSX.Element {
  const video = useRef<HTMLMediaElement | null>(null);
  const bindMedia = (el: HTMLMediaElement | null): void => { video.current = el; };
  const [now, setNow] = useState(0);
  const items = notes.items ?? [];
  const chapters = notes.chapters ?? [];
  const duration = notes.duration ?? (items.length ? items[items.length - 1].end : 0);
  const current = filmIndexAt(now, items);
  const cur: FilmItem | undefined = items[current];
  const chapterClass = (id?: string): string => `ep-s${Math.max(0, chapters.findIndex(c => c.id === id)) + 1}`;
  const count = (v: Verdict): number => items.filter(x => (x.flag ?? "pending") === v).length;
  const ep = episodeNumber(episode);
  const cue = (notes.cues ?? []).find(c => now >= c.t && now < c.end);
  const langHref = (l: string): string => `/episode-preview?path=${encodeURIComponent(path)}${audio ? "&audio=1" : ""}${l === "zh" ? "" : `&lang=${l}`}`;

  const seek = (t: number): void => {
    if (!video.current) return;
    video.current.currentTime = t + 0.05;
    void video.current.play().catch(() => undefined);
    (audio ? video.current.parentElement ?? video.current : video.current).scrollIntoView({ behavior: "smooth", block: "center" });
  };

  return <section className="ep-page">
    <header className="ep-hero">
      {audio
        ? <p className="ep-eyebrow">音频预览 · {dramaPath.split("/")[1]} · {episode}</p>
        : isEduPath(path)
        ? <p className="ep-eyebrow">教学视频 · {dramaPath.split("/")[1]} · {episode}</p>
        : <p className="ep-eyebrow">单集预览 · EP{Number.isNaN(ep) ? episode : ep} · <Link to={`/drama?drama=${encodeURIComponent(dramaPath)}`}>{dramaPath.split("/")[1]}</Link></p>}
      <h1>{notes.title ?? episode}</h1>
      {(notes.languages?.length ?? 0) > 1 && <nav className="ep-modes ep-langs" aria-label="语言版本">
        {notes.languages!.map(l => <Link key={l.lang} aria-current={(notes.lang ?? "zh") === l.lang ? "page" : undefined}
          to={langHref(l.lang)}>{l.label}</Link>)}
      </nav>}
      {notes.tagline && <p className="ep-tagline">{notes.tagline}</p>}
      <ul className="ep-stats">
        <li><b>{clock(duration)}</b>{audio ? "全长" : "成片"}</li>
        {chapters.length > 0 && <li><b>{chapters.length}</b>章</li>}
        <li><b>{items.length}</b>{audio ? "镜" : "段"}</li>
        {count("ok") > 0 && <li><b>{count("ok")}</b>{FLAG_LABEL.ok}</li>}
        {count("note") > 0 && <li><b>{count("note")}</b>{FLAG_LABEL.note}</li>}
        {count("redo") > 0 && <li className="ep-warn"><b>{count("redo")}</b>{FLAG_LABEL.redo}</li>}
        {count("pending") > 0 && <li><b>{count("pending")}</b>{FLAG_LABEL.pending}</li>}
      </ul>
      <p className="ep-links">
        {(notes.links ?? []).map(l => <Link key={l.path} to={fileHref(l.path)}>{l.label}</Link>)}
        <Link to={fileHref(previewFile(path, lang, audio))}>本页说明数据</Link>
      </p>
    </header>

    <section className="ep-player" aria-label="播放器">
      {chapters.length > 0 && <div className="ep-modes" role="tablist" aria-label="章节">
        {chapters.map(c => <button key={c.id} type="button" role="tab" aria-selected={cur?.chapter === c.id} onClick={() => seek(c.t)}>
          {clock(c.t)} {c.title}</button>)}
      </div>}
      {audio && notes.audio ? <div className="ep-audio-stage">
        <div className="ep-audio-frame">
          {cur?.image ? <img src={mediaUrl(cur.image, revision)} alt={cur.title} /> : <span className="ep-audio-blank">{cur?.title ?? "按播放开始"}</span>}
          {cue && <p className="ep-audio-cue">{cue.who && <b>{cue.who}</b>}{cue.text}</p>}
        </div>
        <audio ref={bindMedia} controls preload="metadata" src={mediaUrl(notes.audio, revision)} onTimeUpdate={e => setNow(e.currentTarget.currentTime)} />
      </div>
      : notes.video ? <video ref={bindMedia} controls preload="metadata" src={mediaUrl(notes.video, revision)}
        onTimeUpdate={e => setNow(e.currentTarget.currentTime)} /> : <p className="ep-empty">preview.json 没有 video。</p>}
      <div className="ep-film-track">
        <div className="ep-timeline" aria-label="时间线">
          {items.map((x, i) => <button key={i} type="button" className={`ep-seg ${chapterClass(x.chapter)}${i === current ? " ep-on" : ""}`}
            style={{ flexGrow: Math.max(0.1, x.end - x.t) }} title={`${clock(x.t)} ${x.title}`} aria-label={`跳到 ${x.title}`} onClick={() => seek(x.t)} />)}
        </div>
        {duration > 0 && (notes.marks ?? []).map(m => <button key={m.t} type="button" className="ep-mark" style={{ left: `${(m.t / duration) * 100}%` }}
          title={`${clock(m.t)} ${m.label}`} aria-label={`跳到 ${m.label}`} onClick={() => seek(m.t)} />)}
      </div>
      {cur && <div className="ep-now">
        <p className="ep-now-id">{clock(cur.t)}–{clock(cur.end)} · {chapters.find(c => c.id === cur.chapter)?.title ?? ""}</p>
        <p className="ep-now-title"><b>{cur.title}</b>{cur.badge && <span className="ep-badge">{cur.badge}</span>}</p>
        {cur.subtitle && <p className="ep-mute">{cur.subtitle}</p>}
        {cur.note && <p className="ep-now-note">{cur.note}</p>}
      </div>}
    </section>

    {notes.images?.length ? <section className="ep-cast" aria-label="图片">
      <h2>封面候选</h2>
      <div className="ep-film-images">{notes.images.map(im => <figure key={im.path}>
        <a href={mediaUrl(im.path, revision)} target="_blank" rel="noreferrer"><img src={mediaUrl(im.path, revision)} alt={im.caption ?? im.path} loading="lazy" /></a>
        {im.caption && <figcaption>{im.caption}</figcaption>}
      </figure>)}</div>
    </section> : null}

    {notes.notes?.length ? <section className="ep-notes" aria-label="说明">
      {notes.notes.map(g => <div key={g.title}><h2>{g.title}</h2><ul>{g.items.map(i => <li key={i}>{i}</li>)}</ul></div>)}
    </section> : null}

    <section aria-label="逐段">
      {(chapters.length ? chapters : [{ id: "", title: "逐段", t: 0 }]).map(c => {
        const own = items.map((x, i) => [x, i] as const).filter(([x]) => !chapters.length || x.chapter === c.id);
        if (!own.length) return null;
        return <article key={c.id} className={`ep-scene ${chapterClass(c.id)}`} id={c.id || undefined}>
          <header>
            <span className="ep-scene-num">{clock(c.t)}</span>
            <div><h3>{c.title}</h3><p className="ep-mute">{own.length} 段</p></div>
          </header>
          <div className="ep-shots">{own.map(([x, i]) => <div key={i} className={`ep-shot${i === current ? " ep-on" : ""}`}>
            <button type="button" className="ep-thumb" onClick={() => seek(x.t)} aria-label={`播放 ${x.title}`}>
              {x.image ? <img src={mediaUrl(x.image, revision)} alt="" loading="lazy" /> : <span>{x.title}</span>}
              <span className="ep-dur">{clock(x.t)} · {(x.end - x.t).toFixed(1)}s</span>
            </button>
            <p className="ep-shot-meta"><b>{x.title}</b>{x.badge && <span className="ep-badge">{x.badge}</span>}
              {x.flag && <span className={`ep-chip ep-v-${x.flag}`}>{FLAG_LABEL[x.flag]}</span>}</p>
            {x.subtitle && <p className="ep-mute">{x.subtitle}</p>}
            {x.detail && <p className="ep-mute">{x.detail}</p>}
            {x.note && <p className="ep-note">{x.note}</p>}
          </div>)}</div>
        </article>;
      })}
    </section>
  </section>;
}
