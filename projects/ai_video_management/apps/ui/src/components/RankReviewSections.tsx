import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { mediaUrl } from "../api";
import { useFileChanges } from "../lib/fileEvents";
import { rankPreviewHref } from "../lib/rankPreview";
import {
  defaultVideo, formatDuration, initials, isAiCredit, isListMode, isNewsAgencyRisk, listModeLabel, loadRankPreview, musicLabel,
  positionLabel, type RankDoc, type RankEpisode, type RankEpisodeCard, type RankImage, type RankItem, type RankPerson,
  type RankPreviewData, type RankVideo,
} from "../lib/rankReview";
import { Renderer } from "../markdown/renderer";
import "./HeroPreviewPage.css";
import "./RankReviewSections.css";

/** 排行榜审片（follow-up 320）：系列总览与单期的审片区块，数据来自 /api/rank-preview。只读。
 *  follow-up 321：列表期（mode=list）不出冠军、名次列改「序」；明细表按字段补 corner / logo / 创始人 / 风险原文 / 备注。 */

const fileHref = (path: string): string => `/file/${encodeURIComponent(path)}`;
const NOT_YET = "尚未生成";

export function useRankPreview(path: string, revision: number): { data: RankPreviewData | null; error: string | null } {
  const [data, setData] = useState<RankPreviewData | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    let cancelled = false;
    setError(null);
    if (!path) return;
    loadRankPreview(path).then(d => { if (!cancelled) setData(d); }, reason => {
      if (!cancelled) setError(reason instanceof Error ? reason.message : String(reason));
    });
    return () => { cancelled = true; };
  }, [path, revision]);
  return { data, error };
}

function StatusBadges({ card }: { card: RankEpisodeCard }): JSX.Element {
  const s = card.stats;
  return <p className="rank-review-badges">
    <span className={card.verdict ? "rank-review-badge rank-review-ok" : "rank-review-badge"} title={card.verdict}>
      {card.verdict ? `审片：${card.verdict.replace(/^(结论|verdict)\S*?[:：]\s*/i, "")}` : "未审片"}</span>
    <span className={card.music ? "rank-review-badge rank-review-ok" : "rank-review-badge"}>{musicLabel(card.music)}</span>
    <span className="rank-review-badge">图 {s.with_image}/{s.items}</span>
    {s.risk > 0 && <span className="rank-review-badge rank-review-risk">风险 {s.risk}</span>}
    {s.alt > 0 && <span className="rank-review-badge">替代图 {s.alt}</span>}
    {s.ai > 0 && <span className="rank-review-badge rank-review-ai">AI 图 {s.ai}</span>}
    {card.error && <span className="rank-review-badge rank-review-risk" title={card.error}>数据有误</span>}
  </p>;
}

function SeriesCard({ card, revision }: { card: RankEpisodeCard; revision: number }): JSX.Element {
  return <Link className="rank-review-card" to={rankPreviewHref(card.path)}>
    {card.thumbnail
      ? <img src={mediaUrl(card.thumbnail, revision)} alt={`${card.key} 封面`} loading="lazy" />
      : <div className="rank-review-nothumb">封面{NOT_YET}</div>}
    <div className="rank-review-card-body">
      <h3><span className="rank-review-epno">ep{String(card.number ?? "?").padStart(2, "0")}</span>{card.title || card.key}</h3>
      <p className="hero-preview-meta"><span>N = {card.n}</span>
        {isListMode(card) ? <span className="rank-review-listmode">列表期 · 不排名</span> : <span>冠军：{card.champion || "—"}</span>}
        <span>{card.videos ? `时长 ${formatDuration(card.duration_s)}` : `成片${NOT_YET}`}</span></p>
      <StatusBadges card={card} />
    </div>
  </Link>;
}

export function RankSeriesOverview({ path }: { path: string }): JSX.Element {
  const [revision, refresh] = useState(Date.now);
  useFileChanges(path, () => refresh(Date.now()));
  const { data, error } = useRankPreview(path, revision);
  if (error) return <section className="hero-preview-page"><h1>排行榜系列</h1><p role="alert">{error}</p></section>;
  const series = data?.series;
  if (!series) return <p role="status">加载排行榜系列…</p>;
  const focus = series.episodes.filter(e => e.number !== null && series.focus.includes(e.number));
  const rest = series.episodes.filter(e => !focus.includes(e));
  return <section className="hero-preview-page rank-review-series">
    <header><h1>排行榜系列 · 审片总览</h1>
      <p className="hero-preview-meta"><span>{series.episodes.length} 期</span><Link to={fileHref(`${series.path}/README.md`)}>README</Link></p></header>
    <h2>重点：ep{series.focus[0]}–ep{series.focus[series.focus.length - 1]}（{focus.length}）</h2>
    <div className="rank-review-cards">{focus.map(c => <SeriesCard key={c.key} card={c} revision={revision} />)}</div>
    {rest.length > 0 && <><h2>其他各期（{rest.length}）</h2>
      <div className="rank-review-cards">{rest.map(c => <SeriesCard key={c.key} card={c} revision={revision} />)}</div></>}
  </section>;
}

export function RankCutTabs({ videos, revision }: { videos: RankVideo[]; revision: number }): JSX.Element {
  const [picked, setPicked] = useState<string | null>(null);
  const current = videos.find(v => v.path === picked) ?? defaultVideo(videos);
  if (!current) return <p className="hero-preview-empty">成片{NOT_YET}。</p>;
  return <div className="rank-review-cuts">
    <div role="tablist" className="rank-review-tabs">{videos.map(v => <button key={v.path} type="button" role="tab"
      aria-selected={v === current} onClick={() => setPicked(v.path)} title={v.name}>
      {v.label}{v.recommended && <span className="rank-review-rec">推荐审看</span>}</button>)}</div>
    {current.complete
      ? <figure className="hero-preview-media hero-preview-hero"><video key={current.path} controls preload="metadata" src={mediaUrl(current.path, revision)} />
        <figcaption><Link to={fileHref(current.path)}>{current.name}</Link> · {formatDuration(current.duration_s)} · {musicLabel(current.music)}</figcaption></figure>
      : <p className="hero-preview-empty">{current.name} 还在渲染（文件不完整），完成后自动出现。</p>}
  </div>;
}

export function RankEpisodeSummary({ ep }: { ep: RankEpisode }): JSX.Element {
  const c = ep.card;
  return <div className="rank-review-summary">
    <p className="hero-preview-meta"><strong>{c.title || c.key}</strong><span>N = {c.n}</span><span>时长 {formatDuration(c.duration_s)}</span>
      <span>主题 {ep.theme || "—"}</span><span>{ep.period_label || "统计期未写"}</span>
      {isListMode(c)
        ? <><span className="rank-review-listmode">{listModeLabel(c)}</span><span>首个：{c.first || "—"} · 末个：{c.last || "—"}</span></>
        : <span>冠军：{c.champion || "—"}</span>}</p>
    {ep.source_line && <p className="hero-preview-meta">{ep.source_line}</p>}
    {ep.scope_note && <p className="rank-review-scope">{ep.scope_note}</p>}
    <StatusBadges card={c} />
  </div>;
}

function Markdown({ doc }: { doc: RankDoc }): JSX.Element {
  return <div className="rank-review-md"><Renderer content={doc.text} currentPath={doc.path} knownPaths={[]} /></div>;
}

export function RankVerdict({ ep }: { ep: RankEpisode }): JSX.Element {
  if (!ep.qc.path) return <p className="hero-preview-empty">审片记录 qc.md {NOT_YET}。</p>;
  return <div className="rank-review-verdict">
    <div className="rank-review-md"><Renderer content={ep.verdict_excerpt} currentPath={ep.qc.path} knownPaths={[]} /></div>
    <details className="hero-preview-fold"><summary>展开 qc.md 全文</summary><Markdown doc={ep.qc} /></details>
  </div>;
}

export function RankHandoff({ ep }: { ep: RankEpisode }): JSX.Element | null {
  if (!ep.handoff.path) return null;
  return <aside className="rank-review-handoff"><h3>交接：遗留问题与待用户决定（<Link to={fileHref(ep.handoff.path)}>handoff.md</Link>）</h3>
    <Markdown doc={ep.handoff} /></aside>;
}

function Thumb({ img, revision }: { img: RankImage | null; revision: number }): JSX.Element {
  if (!img) return <span className="rank-review-dim">—</span>;
  if (!img.path) return <span className="rank-review-risk-text" title={img.declared}>文件不在</span>;
  const src = mediaUrl(img.path, revision);
  return <div className={img.ai ? "rank-review-thumb rank-review-thumb-ai" : "rank-review-thumb"}>
    <a href={src} target="_blank" rel="noreferrer"><img src={src} alt={img.declared} loading="lazy" /></a>
    <small>{img.ai && <b className="rank-review-ai-tag">AI-generated</b>} {img.licence || "许可未登记"}{img.author && ` · ${img.author}`}
      {img.source && <> · <a href={img.source} target="_blank" rel="noreferrer">来源</a></>}</small>
  </div>;
}

function Logo({ img, bg, revision }: { img: RankImage | null; bg: string; revision: number }): JSX.Element {
  if (!img) return <span className="rank-review-dim">—</span>;
  if (!img.path) return <span className="rank-review-risk-text" title={img.declared}>文件不在</span>;
  return <span className="rank-review-logo" style={{ background: bg || "#fff" }} title={img.licence || img.declared}>
    <img src={mediaUrl(img.path, revision)} alt={`${img.declared} logo`} loading="lazy" /></span>;
}

function Person({ person, revision }: { person: RankPerson | null; revision: number }): JSX.Element {
  if (!person) return <span className="rank-review-dim">—</span>;
  const img = person.image;
  const cls = person.image_risk ? "rank-review-avatar rank-review-avatar-risk" : "rank-review-avatar";
  return <div className="rank-review-person">
    {img?.path
      ? <a href={mediaUrl(img.path, revision)} target="_blank" rel="noreferrer">
        <img className={cls} src={mediaUrl(img.path, revision)} alt={person.name} loading="lazy" /></a>
      : <span className={`${cls} rank-review-initials`} title={img ? `文件不在：${img.declared}` : "未写头像"}>{initials(person.name)}</span>}
    <div><strong>{person.name || "—"}</strong>{person.role && <div className="rank-review-dim">{person.role}</div>}
      {person.image_risk && <div className="rank-review-risk-text">⚠ 头像：{person.image_risk}</div>}
      {img?.path && <small className="rank-review-dim">{img.licence || "许可未登记"}{img.author && ` · ${img.author}`}</small>}</div>
  </div>;
}

/** 主图 image_risk 原文；通讯社图（news-agency）红底最醒目。 */
function RiskText({ risk }: { risk: string }): JSX.Element | null {
  if (!risk) return null;
  return <div className={isNewsAgencyRisk(risk) ? "rank-review-risk-text rank-review-news" : "rank-review-risk-text"}>⚠ {risk}</div>;
}

function AltCredit({ credit }: { credit: string }): JSX.Element | null {
  if (!credit) return null;
  return <small className={isAiCredit(credit) ? "rank-review-credit rank-review-ai-tag" : "rank-review-credit"}>署名：{credit}</small>;
}

/** 有字段才出列：ep01/ep02 没有公司卡字段，不出空列。 */
const optionalColumns = (items: RankItem[]) => ({
  corner: items.some(i => i.corner), logo: items.some(i => i.logo), person: items.some(i => i.person), notes: items.some(i => i.notes),
});

const DASH = <span className="rank-review-dim">—</span>;
const NOTE_PREVIEW = 40;

export function RankItemTable({ ep, revision }: { ep: RankEpisode; revision: number }): JSX.Element {
  if (ep.items.length === 0) return <p className="hero-preview-empty">data.json {NOT_YET}。</p>;
  const list = isListMode(ep.card);
  const has = optionalColumns(ep.items);
  return <div className="rank-review-table-wrap">
    {list && <p className="rank-review-listmode-note">{listModeLabel(ep.card)}：「序」是出场位置，不是名次。</p>}
    <table className="rank-review-table">
    <thead><tr><th>{list ? "序" : "名次"}</th>{has.corner && <th>角标 corner</th>}<th>名称</th>{has.logo && <th>Logo</th>}
      {has.person && <th>创始人 person</th>}<th>国家</th><th>数值</th><th>徽章</th><th>主图 image</th><th>替代图 image_alt</th>
      {has.notes && <th>备注 notes</th>}</tr></thead>
    <tbody>{ep.items.map((it, i) => <tr key={`${it.rank}-${it.name}-${i}`} className={it.image_risk ? "rank-review-row-risk" : undefined}>
      <td>{positionLabel(it.rank, list)}</td>
      {has.corner && <td>{it.corner ? <span className="rank-review-corner">{it.corner}</span> : DASH}</td>}
      <td><strong>{it.name}</strong>{it.subtitle && <div className="rank-review-dim">{it.subtitle}</div>}</td>
      {has.logo && <td><Logo img={it.logo} bg={it.logo_bg} revision={revision} /></td>}
      {has.person && <td><Person person={it.person} revision={revision} /></td>}
      <td>{it.flag && <img className="rank-review-flag" src={mediaUrl(it.flag, revision)} alt={it.country_iso2} />}{it.country_name || it.country_iso2}</td>
      <td>{it.value_display}{it.secondary_display && <div className="rank-review-dim">{it.secondary_display}</div>}</td><td>{it.badge}</td>
      <td><Thumb img={it.image} revision={revision} /><RiskText risk={it.image_risk} /></td>
      <td><Thumb img={it.image_alt} revision={revision} /><AltCredit credit={it.image_alt_credit} /></td>
      {has.notes && <td className="rank-review-notes">{!it.notes ? DASH : it.notes.length <= NOTE_PREVIEW ? it.notes
        : <details><summary>{`${it.notes.slice(0, NOTE_PREVIEW)}…`}</summary><p>{it.notes}</p></details>}</td>}
    </tr>)}</tbody>
  </table></div>;
}

export function RankNotes({ ep }: { ep: RankEpisode }): JSX.Element {
  return <>
    <h2 id="insights">洞察卡（{ep.insights.length}）</h2>
    {ep.insights.length > 0
      ? <ol className="rank-review-insights">{ep.insights.map((s, i) => <li key={i}>{s.after_rank !== null && <span className="rank-review-dim">{isListMode(ep.card) ? `序 ${s.after_rank}` : `#${s.after_rank}`} 之后 · </span>}{s.text}</li>)}</ol>
      : <p className="hero-preview-empty">洞察卡{NOT_YET}。</p>}
    <h2 id="publish">发布稿</h2>
    {ep.publish.path
      ? <details className="hero-preview-fold" open><summary><Link to={fileHref(ep.publish.path)}>publish.md</Link>（标题 / 描述 / 置顶评论）</summary><Markdown doc={ep.publish} /></details>
      : <p className="hero-preview-empty">publish.md {NOT_YET}。</p>}
  </>;
}
