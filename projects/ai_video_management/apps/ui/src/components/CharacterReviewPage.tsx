import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { fetchFile, mediaUrl } from "../api";
import { useFileChanges } from "../lib/fileEvents";
import { isReviewPath, parseCharacterReview, statusTone, type CharacterReview, type ReviewItem } from "../lib/characterReview";
import "./HeroPreviewPage.css";
import "./CharacterReviewPage.css";

const fileHref = (path: string): string => `/file/${encodeURIComponent(path)}`;

function Item({ item, revision }: { item: ReviewItem; revision: number }): JSX.Element {
  const src = mediaUrl(item.path, revision);
  const tone = statusTone(item.status);
  return <article className={`creview-item creview-${tone}`} id={item.id}>
    <header>
      <span className="creview-id">{item.id}</span>
      <strong>{item.label}</strong>
      <span className={`creview-status creview-status-${tone}`}>{item.status ?? "待审"}</span>
    </header>
    {item.kind === "video" && <video controls preload="metadata" src={src} />}
    {item.kind === "image" && <a href={src} target="_blank" rel="noreferrer"><img src={src} alt={`${item.id} ${item.label}`} loading="lazy" /></a>}
    {item.kind === "audio" && <audio controls preload="none" src={src} />}
    {item.desc && <p className="creview-desc">{item.desc}</p>}
    {item.note && <p className="creview-note">{item.note}</p>}
    <Link className="creview-file" to={fileHref(item.path)}>{item.path.split("/").pop()}</Link>
  </article>;
}

export function CharacterReviewPage(): JSX.Element {
  const [params] = useSearchParams();
  const path = (params.get("path") ?? "").replace(/\/+$/, "");
  const [data, setData] = useState<{ review: CharacterReview | null; problems: string[] } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [revision, refresh] = useState(Date.now);
  useFileChanges(path || null, () => refresh(Date.now()));
  useEffect(() => {
    let cancelled = false;
    setError(null);
    if (!isReviewPath(path)) { setError("链接形如 /character-review?path=ai_videos/<剧>/2_世界观人设/characters/<人物目录>，或 edu_videos/ 下带 review.json 的目录"); return; }
    fetchFile(`${path}/review.json`)
      .then(f => { if (!cancelled) setData(parseCharacterReview(JSON.parse(f.content))); })
      .catch(reason => { if (!cancelled) setError(`读不到 ${path}/review.json（先运行 python tools/character_review.py ${path}）：${reason instanceof Error ? reason.message : String(reason)}`); });
    return () => { cancelled = true; };
  }, [path, revision]);
  if (error) return <section className="hero-preview-page"><h1>人物审阅</h1><p role="alert">{error}</p></section>;
  if (!data) return <p role="status">加载人物审阅…</p>;
  const { review, problems } = data;
  if (!review) return <section className="hero-preview-page"><h1>人物审阅</h1><p role="alert">{problems.join("；")}</p></section>;
  const total = review.sections.reduce((n, s) => n + s.items.length, 0);
  return <section className="hero-preview-page creview-page">
    <header>
      <h1>{review.title}</h1>
      <p className="hero-preview-meta">
        <span>{review.character}</span><span>{total} 项</span>
        {review.updated && <span>更新于 {review.updated}</span>}
        <Link to={fileHref(`${path}/review.json`)}>review.json</Link>
        <Link to={fileHref(path)}>人物目录</Link>
      </p>
      <p className="creview-howto">要修哪一项，直接告诉我编号和问题，例如「<strong>E05</strong> 表情太僵，再自然一点」「<strong>T2</strong> 侧面头发太短」。</p>
      {review.notes?.map(n => <p key={n} className="creview-desc">{n}</p>)}
      {problems.length > 0 && <p role="alert" className="creview-problem">{problems.join("；")}</p>}
      <nav>{review.sections.map(s => <a key={s.id} href={`#sec-${s.id}`}>{s.title}（{s.items.length}）</a>)}</nav>
    </header>
    {review.sections.map(s => <section key={s.id} id={`sec-${s.id}`} className="creview-section">
      <h2>{s.title}</h2>
      {s.hint && <p className="creview-desc">{s.hint}</p>}
      {s.items.length
        ? <div className={s.layout === "wide" ? "creview-wide" : "creview-grid"}>{s.items.map(i => <Item key={i.id} item={i} revision={revision} />)}</div>
        : <p className="hero-preview-empty">还没有内容。</p>}
    </section>)}
  </section>;
}
