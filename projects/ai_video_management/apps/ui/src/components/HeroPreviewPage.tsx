import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { fetchSubtree, mediaUrl } from "../api";
import { useFileChanges } from "../lib/fileEvents";
import { buildHeroPreview, type HeroPreview, type PreviewItem, type RenderGroup } from "../lib/heroPreview";
import { useDemoStatus } from "../lib/demoStatus";
import { DemoFinalBadge } from "./DemoFinalBadge";
import "./HeroPreviewPage.css";

const fileHref = (path: string): string => `/file/${encodeURIComponent(path)}`;

function Media({ item, revision, caption, lazy }: { item: PreviewItem; revision: number; caption?: string; lazy?: boolean }): JSX.Element {
  const src = mediaUrl(item.path, revision);
  return <figure className="hero-preview-media">
    {item.kind === "video" && <video controls preload={lazy ? "none" : "metadata"} src={src} />}
    {item.kind === "image" && <a href={src} target="_blank" rel="noreferrer"><img src={src} alt={item.name} loading="lazy" /></a>}
    {item.kind === "audio" && <audio controls preload="none" src={src} />}
    <figcaption><Link to={fileHref(item.path)}>{caption ?? item.name}</Link></figcaption>
  </figure>;
}

/** Secondary material: thumbnails inside a closed <details>. */
function Folded({ title, items, revision }: { title: string; items: PreviewItem[]; revision: number }): JSX.Element | null {
  if (items.length === 0) return null;
  return <details className="hero-preview-fold"><summary>{title}（{items.length}）</summary>
    <div className="hero-preview-thumbs">{items.map(i => <Media key={i.path} item={i} revision={revision} lazy />)}</div>
  </details>;
}

const videos = (items: PreviewItem[]): PreviewItem[] => items.filter(i => i.kind === "video");
const others = (items: PreviewItem[]): PreviewItem[] => items.filter(i => i.kind !== "video");

function History({ groups, revision }: { groups: RenderGroup[]; revision: number }): JSX.Element | null {
  if (groups.length === 0) return null;
  return <details className="hero-preview-fold"><summary>历史出片（{groups.length}）</summary>
    {groups.map(g => <div key={g.name}>
      <h4>{g.name}{g.review && <> · <Link to={fileHref(g.review)}>审稿记录</Link></>}</h4>
      <div className="hero-preview-thumbs">{g.items.map(i => <Media key={i.path} item={i} revision={revision} lazy />)}</div>
    </div>)}
  </details>;
}

export function HeroPreviewPage(): JSX.Element {
  const [params] = useSearchParams();
  const path = (params.get("path") ?? "").replace(/\/+$/, "");
  const [data, setData] = useState<HeroPreview | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [revision, refresh] = useState(Date.now);
  const demoStatus = useDemoStatus().get(path);
  useFileChanges(path || null, () => refresh(Date.now()));
  useEffect(() => {
    let cancelled = false;
    setError(null);
    if (!path) { setError("缺少英雄目录：链接形如 /hero-preview?path=ai_videos/<剧>/2_世界观人设/characters/<阵营>/<英雄>"); return; }
    fetchSubtree(path, 0).then(node => { if (!cancelled) setData(buildHeroPreview(node)); }, reason => {
      if (!cancelled) setError(reason instanceof Error ? reason.message : String(reason));
    });
    return () => { cancelled = true; };
  }, [path, revision]);
  if (error) return <section className="hero-preview-page"><h1>英雄预览</h1><p role="alert">{error}</p></section>;
  if (!data) return <p role="status">加载英雄预览…</p>;
  const introVideos = videos(data.intro);
  const portraitAndViews = [...(data.portrait ? [data.portrait] : []), ...others(data.intro), ...data.views];
  // 定版成片放在最前（follow-up 315）；没有定版照旧取最新的剪辑
  const finalCut = demoStatus?.video ? data.demo.find(i => i.path === demoStatus.video) : undefined;
  const demoMain = finalCut ?? data.demo[0];
  const demoRest = data.demo.filter(i => i !== demoMain);
  return <section className="hero-preview-page">
    <header>
      <h1>{data.name}<DemoFinalBadge status={demoStatus} long /></h1>
      <nav>
        <a href="#demo">Demo</a><a href="#intro">人物亮相</a>
        {data.skills.map(s => <a key={s.path} href={`#${s.name}`}>{s.name}</a>)}
        {data.card && <Link to={fileHref(data.card)}>人物卡</Link>}
      </nav>
    </header>

    <h2 id="demo">Demo{finalCut && <DemoFinalBadge status={demoStatus} />}</h2>
    {demoMain
      ? <div className="hero-preview-hero"><Media item={demoMain} revision={revision}
        caption={finalCut ? `${demoMain.name} · 定版 v${demoStatus!.version}` : undefined} /></div>
      : <p className="hero-preview-empty">还没有 demo 成片。</p>}
    {demoStatus && demoStatus.newer.length > 0 && <p className="hero-preview-meta">定版之后还有未定的剪辑 v{demoStatus.newer.join(" / v")}，在「其他剪辑版本」里。</p>}
    {data.demoNotes.length > 0 && <p className="hero-preview-meta">{data.demoNotes.map(n => <Link key={n.path} to={fileHref(n.path)}>{n.name}</Link>)}</p>}
    <Folded title="其他剪辑版本" items={demoRest} revision={revision} />

    <h2 id="intro">人物亮相</h2>
    {introVideos.length > 0
      ? <div className="hero-preview-hero">{introVideos.map(i => <Media key={i.path} item={i} revision={revision} />)}</div>
      : <p className="hero-preview-empty">还没有亮相视频。</p>}
    <Folded title="立绘、三视图与声样" items={portraitAndViews} revision={revision} />
    <Folded title="其他人物图" items={data.otherImages} revision={revision} />

    <h2>技能</h2>
    <div className="hero-preview-skills">
      {data.skills.map(skill => {
        const latestVideos = skill.latest ? videos(skill.latest.items) : [];
        return <article key={skill.path} id={skill.name} className="hero-preview-skill">
          <h3>{skill.name}</h3>
          {latestVideos.length > 0
            ? latestVideos.map(i => <Media key={i.path} item={i} revision={revision} />)
            : <p className="hero-preview-empty">还没有出片。</p>}
          <p className="hero-preview-meta">
            {skill.latest && <span>最新 {skill.latest.name}</span>}
            {skill.latest?.review && <Link to={fileHref(skill.latest.review)}>审稿记录</Link>}
            {skill.card && <Link to={fileHref(skill.card)}>技能卡</Link>}
          </p>
          {skill.latest && <Folded title="拼图与测速图" items={others(skill.latest.items)} revision={revision} />}
          <Folded title="峰值图与关键帧" items={skill.images} revision={revision} />
          <Folded title="开场图" items={skill.planning} revision={revision} />
          <History groups={skill.history} revision={revision} />
        </article>;
      })}
    </div>
  </section>;
}
