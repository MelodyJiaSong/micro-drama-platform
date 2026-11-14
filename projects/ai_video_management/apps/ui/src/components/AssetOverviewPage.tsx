/** AssetOverviewPage：一部剧的资产总览（follow-up 293）。
 *
 * 人物、背景、道具各一节，节内按分组（近卫 / 天灾 / 中立）排；每个资产一格（封面图 + 键 + 名字）。
 * 点一格打开预览：大图（可放大）、该目录的全部图片与视频、卡开头的键与状态行；人物另取
 * `GET /api/character-reel` 列技能图标，点技能看峰值图或正片。← / → 切换上下一个，Esc 关闭；
 * 打开的资产记在 `?open=` 里，链接可直接分享。只读，数据来自 `GET /api/asset-overview`。
 */
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { mediaUrl } from "../api";
import { filterSections, loadAssetOverview, type AssetKind, type AssetOverview, type AssetTile } from "../lib/assetOverview";
import { loadCharacterReel, type SkillReel } from "../lib/characterReel";
import { useFileChanges } from "../lib/fileEvents";
import { useDemoStatus } from "../lib/demoStatus";
import { shopItemsUrl } from "../lib/shopItems";
import { useShopItems } from "../lib/useShopItems";
import { DemoFinalBadge } from "./DemoFinalBadge";
import { ZoomableImage } from "./ZoomableImage";
import { SharedAssetsPage } from "./SharedAssetsPage";
import "./AssetOverviewPage.css";

/** 几个目录的共同上级（盯文件变化用）。 */
function commonDir(paths: string[]): string | null {
  if (paths.length === 0) return null;
  const split = paths.map(p => p.split("/"));
  const out: string[] = [];
  for (let i = 0; i < split[0].length; i++) {
    const seg = split[0][i];
    if (split.some(parts => parts[i] !== seg)) break;
    out.push(seg);
  }
  return out.length ? out.join("/") : null;
}

function fileName(path: string): string {
  return path.slice(path.lastIndexOf("/") + 1);
}

/** 卡开头的 `> ` 行：`code` 与 **粗体** 照样式显示，其余原文。 */
function MetaLine({ text }: { text: string }): JSX.Element {
  const parts = text.split(/(`[^`]+`|\*\*[^*]+\*\*)/g).filter(Boolean);
  return (
    <p className="asset-preview-meta-line">
      {parts.map((part, i) =>
        part.startsWith("`") ? <code key={i}>{part.slice(1, -1)}</code>
          : part.startsWith("**") ? <strong key={i}>{part.slice(2, -2)}</strong>
            : <span key={i}>{part}</span>)}
    </p>
  );
}

interface Selected { kind: "image" | "video"; path: string; caption: string }

function AssetPreview({ tile, kind, index, total, onPrev, onNext, onClose }: {
  tile: AssetTile; kind: AssetKind; index: number; total: number;
  onPrev: () => void; onNext: () => void; onClose: () => void;
}): JSX.Element {
  const navigate = useNavigate();
  const demoStatus = useDemoStatus().get(tile.path);
  const panelRef = useRef<HTMLDivElement>(null);
  const initial = (): Selected | null =>
    tile.portrait ? { kind: "image", path: tile.portrait, caption: fileName(tile.portrait) }
      : tile.videos[0] ? { kind: "video", path: tile.videos[0], caption: fileName(tile.videos[0]) } : null;
  const [selected, setSelected] = useState<Selected | null>(initial);
  const [skills, setSkills] = useState<SkillReel[]>([]);

  useEffect(() => { setSelected(initial()); }, [tile.path]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    setSkills([]);
    if (kind !== "characters") return;
    let cancelled = false;
    loadCharacterReel(tile.path).then(reel => { if (!cancelled) setSkills(reel.skills); }, () => undefined);
    return () => { cancelled = true; };
  }, [kind, tile.path]);

  useEffect(() => {
    panelRef.current?.focus();
    const onKey = (e: KeyboardEvent): void => {
      // 放大查看器自己处理 Esc；它开着时不翻页
      if (document.querySelector(".zoom-viewer")) return;
      if (e.key === "Escape") onClose();
      else if (e.key === "ArrowLeft") onPrev();
      else if (e.key === "ArrowRight") onNext();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose, onPrev, onNext]);

  const media: Selected[] = [
    ...tile.images.map(path => ({ kind: "image" as const, path, caption: fileName(path) })),
    ...tile.videos.map(path => ({ kind: "video" as const, path, caption: fileName(path) })),
  ];

  return createPortal(
    <div className="asset-preview-backdrop" onClick={onClose}>
      <div
        ref={panelRef}
        className="asset-preview"
        role="dialog"
        aria-modal="true"
        aria-label={`${tile.key} ${tile.name}`}
        tabIndex={-1}
        onClick={e => e.stopPropagation()}
      >
        <header className="asset-preview-header">
          <h2>
            {tile.key ? <span className="asset-key">{tile.key}</span> : null}
            {tile.title || tile.name}
            <DemoFinalBadge status={demoStatus} long />
          </h2>
          <span className="asset-preview-pos">{index + 1} / {total}</span>
          <button type="button" onClick={onPrev} aria-label="上一个" title="上一个（←）">‹</button>
          <button type="button" onClick={onNext} aria-label="下一个" title="下一个（→）">›</button>
          <button type="button" className="asset-preview-close" onClick={onClose} aria-label="关闭" title="关闭（Esc）">×</button>
        </header>
        <div className="asset-preview-body">
          <div className="asset-preview-stage">
            {selected === null ? (
              <div className="asset-preview-empty">还没有图片或视频</div>
            ) : selected.kind === "image" ? (
              <ZoomableImage key={selected.path} src={mediaUrl(selected.path)} alt={selected.caption} className="asset-preview-main" />
            ) : (
              <video key={selected.path} src={mediaUrl(selected.path)} controls autoPlay playsInline className="asset-preview-main" />
            )}
            {selected ? <div className="asset-preview-caption">{selected.caption}</div> : null}
          </div>
          <aside className="asset-preview-side">
            {media.length > 1 ? (
              <section>
                <h3>图片与视频 · {media.length}</h3>
                <div className="asset-preview-thumbs">
                  {media.map(m => (
                    <button
                      key={m.path}
                      type="button"
                      className={selected?.path === m.path ? "asset-thumb is-active" : "asset-thumb"}
                      onClick={() => setSelected(m)}
                      title={m.caption}
                    >
                      {m.kind === "image"
                        ? <img src={mediaUrl(m.path)} alt={m.caption} loading="lazy" />
                        : <span className="asset-thumb-video">▶<small>{m.caption}</small></span>}
                    </button>
                  ))}
                </div>
              </section>
            ) : null}
            {skills.length > 0 ? (
              <section>
                <h3>技能 · {skills.length}</h3>
                <ul className="asset-preview-skills">
                  {skills.map(skill => {
                    const target: Selected | null = skill.final
                      ? { kind: "video", path: skill.final.video, caption: `${skill.title} · 正片` }
                      : skill.peak ? { kind: "image", path: skill.peak, caption: `${skill.title} · 峰值图` } : null;
                    return (
                      <li key={skill.key}>
                        <button type="button" disabled={target === null} onClick={() => target && setSelected(target)}
                          title={target ? `看 ${target.caption}` : "还没有峰值图或正片"}>
                          {skill.icon ? <img src={mediaUrl(skill.icon)} alt="" /> : <span className="asset-skill-noicon" />}
                          <span className="asset-skill-title">{skill.title}</span>
                          {skill.final ? <span className="asset-badge">正片</span> : null}
                        </button>
                      </li>
                    );
                  })}
                </ul>
              </section>
            ) : null}
            {tile.meta.length > 0 ? (
              <section className="asset-preview-meta">
                {tile.meta.map((line, i) => <MetaLine key={i} text={line} />)}
              </section>
            ) : null}
            <div className="asset-preview-actions">
              {tile.card ? (
                <button type="button" onClick={() => navigate(`/file/${encodeURIComponent(tile.card)}`)}>📄 打开卡片</button>
              ) : null}
              <code className="asset-preview-path" title={tile.path}>{tile.folder}</code>
            </div>
          </aside>
        </div>
      </div>
    </div>,
    document.body,
  );
}

export function AssetOverviewPage(): JSX.Element {
  const [params] = useSearchParams();
  return params.get("library") ? <SharedAssetsPage /> : <DramaAssetOverviewPage />;
}

function DramaAssetOverviewPage(): JSX.Element {
  const [searchParams, setSearchParams] = useSearchParams();
  const drama = searchParams.get("drama") ?? "";
  const openPath = searchParams.get("open");
  const [data, setData] = useState<AssetOverview | null>(null);
  const [error, setError] = useState<string>("");
  const [query, setQuery] = useState<string>("");
  const demoStatus = useDemoStatus();
  const shop = useShopItems(drama);
  const onlyFinal = searchParams.get("demo") === "final";

  const load = useCallback(() => {
    if (!drama) return;
    loadAssetOverview(drama).then(d => { setData(d); setError(""); }, (err: unknown) => setError(err instanceof Error ? err.message : String(err)));
  }, [drama]);
  useEffect(() => { setData(null); load(); }, [load]);
  useFileChanges(data ? commonDir(data.watch) : null, () => load());

  const sections = useMemo(() => {
    const filtered = data ? filterSections(data.sections, query) : [];
    if (!onlyFinal) return filtered;
    // 只看 demo 定版（follow-up 315）：人物节只留定版英雄，其他节照常
    return filtered.map(s => {
      if (s.kind !== "characters") return s;
      const groups = s.groups.map(g => ({ ...g, tiles: g.tiles.filter(t => demoStatus.has(t.path)) })).filter(g => g.tiles.length > 0);
      return { ...s, groups, count: groups.reduce((n, g) => n + g.tiles.length, 0) };
    });
  }, [data, query, onlyFinal, demoStatus]);
  const finalCount = useMemo(() => (data?.sections.find(s => s.kind === "characters")?.groups ?? [])
    .reduce((n, g) => n + g.tiles.filter(t => demoStatus.has(t.path)).length, 0), [data, demoStatus]);
  const toggleOnlyFinal = useCallback(() => {
    const next = new URLSearchParams(searchParams);
    if (onlyFinal) next.delete("demo"); else next.set("demo", "final");
    setSearchParams(next, { replace: true });
  }, [searchParams, setSearchParams, onlyFinal]);
  // 预览里 ← / → 按当前过滤后的顺序走，跨分组、跨节
  const flat = useMemo(() => sections.flatMap(s => s.groups.flatMap(g => g.tiles.map(tile => ({ tile, kind: s.kind })))), [sections]);
  const openIndex = openPath ? flat.findIndex(item => item.tile.path === openPath) : -1;

  const setOpen = useCallback((path: string | null) => {
    const next = new URLSearchParams(searchParams);
    if (path) next.set("open", path); else next.delete("open");
    setSearchParams(next, { replace: true });
  }, [searchParams, setSearchParams]);
  const step = useCallback((delta: number) => {
    if (openIndex < 0 || flat.length === 0) return;
    setOpen(flat[(openIndex + delta + flat.length) % flat.length].tile.path);
  }, [openIndex, flat, setOpen]);
  const onPrev = useCallback(() => step(-1), [step]);
  const onNext = useCallback(() => step(1), [step]);
  const onClose = useCallback(() => {
    const path = openPath;
    setOpen(null);
    if (path) requestAnimationFrame(() => document.querySelector<HTMLElement>(`[data-asset-path="${CSS.escape(path)}"]`)?.focus());
  }, [openPath, setOpen]);

  const dramaName = drama.slice(drama.lastIndexOf("/") + 1);
  if (!drama) return <div className="asset-overview"><p className="asset-overview-empty">没有指定剧。请从剧页点「🗂 资产总览」。</p></div>;

  return (
    <div className="asset-overview">
      <header className="asset-overview-header">
        <h1>资产总览 <span className="asset-overview-drama">{dramaName}</span></h1>
        <nav className="asset-overview-jump" aria-label="跳到">
          {sections.map(s => <a key={s.kind} href={`#asset-${s.kind}`} onClick={e => { e.preventDefault(); document.getElementById(`asset-${s.kind}`)?.scrollIntoView({ behavior: "smooth" }); }}>{s.label} {s.count}</a>)}
        </nav>
        <input
          type="search"
          className="asset-overview-search"
          placeholder="按键或名字过滤，如 c24、敌法师、Axe"
          value={query}
          onChange={e => setQuery(e.target.value)}
          aria-label="过滤资产"
        />
        {shop ? (
          <Link className="asset-overview-shop-link" to={shopItemsUrl(drama)}
            title="商店货单：建筑商店、商人 NPC 与 Roshan 掉落各卖什么，点物品看哪些出售方卖它（follow-up 316）">
            🛒 商店货单 {shop.sellers.length}
          </Link>
        ) : null}
        {finalCount > 0 ? (
          <button type="button" className="asset-overview-final-filter" aria-pressed={onlyFinal} onClick={toggleOnlyFinal}
            title="人物节只显示 demo 已定版的英雄（绿框 ✓ 定版；黄色表示发布文案还没对上定版成片）">
            ✓ Demo 定版 {finalCount}
          </button>
        ) : null}
      </header>
      {error ? <p className="asset-overview-error" role="alert">读取失败：{error}</p> : null}
      {!data && !error ? <p className="asset-overview-empty">加载中…</p> : null}
      {sections.map(section => (
        <section key={section.kind} id={`asset-${section.kind}`} className={`asset-section asset-section-${section.kind}`} aria-label={section.label}>
          <h2>{section.label} <span className="asset-count">{section.count}</span></h2>
          {section.groups.length === 0 ? <p className="asset-overview-empty">{query ? "没有匹配的资产" : "还没有资产"}</p> : null}
          {section.groups.map(group => (
            <div key={group.name} className="asset-group">
              {group.name ? <h3>{group.name} <span className="asset-count">{group.tiles.length}</span></h3> : null}
              <div className="asset-grid">
                {group.tiles.map(tile => (
                  <button
                    key={tile.path}
                    type="button"
                    className={demoStatus.has(tile.path) ? "asset-tile demo-final" : "asset-tile"}
                    data-asset-path={tile.path}
                    onClick={() => setOpen(tile.path)}
                    title={tile.title || tile.folder}
                  >
                    <span className="asset-tile-media">
                      {tile.portrait ? <img src={mediaUrl(tile.portrait)} alt="" loading="lazy" /> : <span className="asset-tile-noimg">无图</span>}
                      {tile.videos.length > 0 ? <span className="asset-tile-badge" title="有视频">▶</span> : null}
                    </span>
                    <span className="asset-tile-label">
                      {tile.key ? <span className="asset-key">{tile.key}</span> : null}
                      <span className="asset-tile-name">{tile.name}</span>
                      <DemoFinalBadge status={demoStatus.get(tile.path)} />
                    </span>
                  </button>
                ))}
              </div>
            </div>
          ))}
        </section>
      ))}
      {openIndex >= 0 ? (
        <AssetPreview
          tile={flat[openIndex].tile}
          kind={flat[openIndex].kind}
          index={openIndex}
          total={flat.length}
          onPrev={onPrev}
          onNext={onNext}
          onClose={onClose}
        />
      ) : null}
    </div>
  );
}
