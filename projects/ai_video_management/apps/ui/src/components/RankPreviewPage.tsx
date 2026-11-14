import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { fetchFile, fetchSubtree, mediaUrl } from "../api";
import { useFileChanges } from "../lib/fileEvents";
import {
  buildCuts, buildRankPreview, join, LICENCE_LABEL, rankPreviewHref,
  type AssetRaw, type EpisodeData, type LicenceClass, type ManifestRaw, type RankCut, type RankPreview,
} from "../lib/rankPreview";
import { isRankSeriesPath, RANK_SERIES_PATH } from "../lib/rankReview";
import {
  RankCutTabs, RankEpisodeSummary, RankHandoff, RankItemTable, RankNotes, RankSeriesOverview, RankVerdict, useRankPreview,
} from "./RankReviewSections";
import "./HeroPreviewPage.css";
import "./RankPreviewPage.css";

const fileHref = (path: string): string => `/file/${encodeURIComponent(path)}`;

async function readJson<T>(path: string): Promise<T | null> {
  try { return JSON.parse((await fetchFile(path)).content) as T; } catch { return null; }
}

interface Loaded { preview: RankPreview; cuts: RankCut[]; docs: string[]; thumb: string | null }

async function load(dir: string): Promise<Loaded> {
  const data = await readJson<EpisodeData>(join(dir, "data.json"));
  if (!data) throw new Error(`读不到 ${join(dir, "data.json")}：链接形如 /rank-preview?path=ai_videos/paihangbang/episodes/<集目录>`);
  const assets = (await readJson<AssetRaw[]>(join(dir, "assets.json"))) ?? [];
  const render = await fetchSubtree(join(dir, "render"), 1).catch(() => null);
  const files = (render?.children ?? []).map(c => ({ name: c.name, path: c.path }));
  const manifests = new Map<string, ManifestRaw>();
  for (const f of files.filter(f => f.name.endsWith(".manifest.json"))) {
    const m = await readJson<ManifestRaw>(f.path);
    if (m) manifests.set(f.name, m);
  }
  const root = await fetchSubtree(dir, 1).catch(() => null);
  const docs = (root?.children ?? []).filter(c => /^(qc|publish|sources|topic)\.md$/.test(c.name)).map(c => c.path);
  const thumb = files.find(f => f.name === "thumbnail.png")?.path ?? null;
  return { preview: buildRankPreview(dir, data, assets), cuts: buildCuts(files, manifests), docs, thumb };
}

function Chip({ cls }: { cls: LicenceClass }): JSX.Element {
  return <span className={`rank-chip rank-chip-${cls}`}>{LICENCE_LABEL[cls]}</span>;
}

function RankEpisodePage(): JSX.Element {
  const [params] = useSearchParams();
  const dir = (params.get("path") ?? "").replace(/\/+$/, "");
  const [data, setData] = useState<Loaded | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [revision, refresh] = useState(Date.now);
  const [filter, setFilter] = useState<LicenceClass | "all">("all");
  // `_build/` holds working files (photo research writes there constantly); only finished inputs refresh the page
  useFileChanges(dir || null, paths => {
    if (paths.some(p => p === "*" || !p.startsWith(`${dir}/_build/`) || p === `${dir}/_build/handoff.md`)) refresh(Date.now());
  });
  useEffect(() => {
    let cancelled = false;
    setError(null);
    if (!dir) { setError("缺少集目录：链接形如 /rank-preview?path=ai_videos/paihangbang/episodes/<集目录>"); return; }
    load(dir).then(d => { if (!cancelled) setData(d); }, reason => {
      if (!cancelled) setError(reason instanceof Error ? reason.message : String(reason));
    });
    return () => { cancelled = true; };
  }, [dir, revision]);
  const review = useRankPreview(dir, revision).data?.episode ?? null;
  // data.json 还没生成时（其他代理在产），照样给出成片、审片与交接（follow-up 320）
  if (error) return <section className="hero-preview-page rank-preview-page"><h1>{review?.card.key ?? "排行榜预览"}</h1>
    {review ? <p className="hero-preview-empty">data.json 尚未生成或读不了（{error}）</p> : <p role="alert">{error}</p>}
    {review && <><RankEpisodeSummary ep={review} /><RankHandoff ep={review} />
      <h2>成片</h2><RankCutTabs videos={review.videos} revision={revision} />
      <h2>审片结论</h2><RankVerdict ep={review} /><RankNotes ep={review} /></>}
  </section>;
  if (!data) return <p role="status">加载排行榜预览…</p>;
  const { preview, cuts, docs, thumb } = data;
  const main = cuts[0];
  const tiles = preview.tiles.filter(t => filter === "all" || t.licenceClass === filter);
  const classes = (Object.keys(preview.counts) as LicenceClass[]).filter(c => preview.counts[c] > 0);
  return <section className="hero-preview-page rank-preview-page">
    <header>
      <h1>{preview.kicker && <span className="rank-kicker">{preview.kicker}</span>}{preview.title}</h1>
      <nav>
        <Link to={rankPreviewHref(RANK_SERIES_PATH)}>← 系列总览</Link>
        <a href="#cuts">成片</a><a href="#review">审片结论</a><a href="#music">配乐</a><a href="#tiles">卡片（{preview.tiles.length}）</a>
        <a href="#table">卡片明细</a><a href="#insights">洞察</a><a href="#publish">发布稿</a>
        {docs.map(d => <Link key={d} to={fileHref(d)}>{d.split("/").pop()}</Link>)}
        <Link to={fileHref(join(dir, "data.json"))}>data.json</Link>
      </nav>
    </header>

    {review && <RankEpisodeSummary ep={review} />}
    {review && <RankHandoff ep={review} />}

    <h2 id="cuts">成片</h2>
    {/* follow-up 320：每个成片一个 tab，默认打开「推荐审看」 */}
    {review ? <RankCutTabs videos={review.videos} revision={revision} /> : <p role="status">加载成片…</p>}
    {thumb && <details className="hero-preview-fold"><summary>封面草图</summary>
      <img className="rank-thumb" src={mediaUrl(thumb, revision)} alt="thumbnail" /></details>}

    <h2 id="review">审片结论</h2>
    {review ? <RankVerdict ep={review} /> : <p role="status">加载审片记录…</p>}

    <h2 id="music">配乐</h2>
    {main && main.music.length > 0
      ? <ol className="rank-music">{main.music.map((t, i) => <li key={`${t.path}-${i}`}>
        <audio controls preload="none" src={mediaUrl(t.path, revision)} />
        <span>{t.path.split("/").pop()} · 截取 {t.range}</span></li>)}</ol>
      : <p className="hero-preview-empty">这版成片没有配乐（静音轨）。</p>}

    <h2 id="tiles">卡片</h2>
    <p className="hero-preview-meta rank-filters">
      <button type="button" aria-pressed={filter === "all"} onClick={() => setFilter("all")}>全部 {preview.tiles.length}</button>
      {classes.map(c => <button key={c} type="button" aria-pressed={filter === c} onClick={() => setFilter(c)}>
        <Chip cls={c} /> {preview.counts[c]}</button>)}
    </p>
    <div className="rank-grid">
      {tiles.map(t => <article key={`${t.rank}-${t.name}`} className={`rank-tile rank-tile-${t.licenceClass}`}>
        <div className="rank-photo">
          {t.image
            ? <a href={mediaUrl(t.image, revision)} target="_blank" rel="noreferrer"><img src={mediaUrl(t.image, revision)} alt={t.name} loading="lazy" /></a>
            : <div className="rank-nophoto">无图</div>}
          <span className="rank-no">#{t.rank}</span>
        </div>
        <h3>{t.name}</h3>
        <p className="rank-place">{t.place}</p>
        <p className="rank-value">{t.value}{t.badge && <span className="rank-badge">{t.badge}</span>}</p>
        <p className="rank-credit"><Chip cls={t.licenceClass} /> {t.credit || "—"}</p>
        {t.risk && <p className="rank-risk">⚠ {t.risk}</p>}
        {t.subjectCheck && <p className="rank-check">{t.subjectCheck}</p>}
        {t.sourcePage && <p className="rank-source"><a href={t.sourcePage} target="_blank" rel="noreferrer">来源页</a></p>}
      </article>)}
    </div>

    {review && <><h2 id="table">卡片明细（国旗、主图 / 替代图、许可）</h2>
      <RankItemTable ep={review} revision={revision} />
      <RankNotes ep={review} /></>}
  </section>;
}

/** follow-up 320：系列根给总览，一期目录给单期页。 */
export function RankPreviewPage(): JSX.Element {
  const [params] = useSearchParams();
  const path = (params.get("path") ?? "").replace(/\/+$/, "");
  return isRankSeriesPath(path) ? <RankSeriesOverview path={path} /> : <RankEpisodePage />;
}
