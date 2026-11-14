import { useCallback, useEffect, useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { mediaUrl } from "../api";
import { useFileChanges } from "../lib/fileEvents";
import { acceptedImage, filterSharedAssets, IMAGE_STATUS, loadSharedLibrary, sharedFile, sharedFileHref, type SharedLibrary } from "../lib/sharedAssets";
import { SharedAssetPreview } from "./SharedAssetPreview";
import "./SharedAssetsPage.css";

const PAGE_SIZE = 24;
export function SharedAssetsPage(): JSX.Element {
  const [data, setData] = useState<SharedLibrary | null>(null);
  const [error, setError] = useState("");
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("");
  const [status, setStatus] = useState("");
  const [viewStatus, setViewStatus] = useState("");
  const [page, setPage] = useState(0);
  const [params, setParams] = useSearchParams();
  const libraryRoot = params.get("library") ?? "";
  const groupId = params.get("group") ?? "";
  const subgroupId = params.get("sub") ?? "";
  const load = useCallback(() => {
    void loadSharedLibrary(libraryRoot).then(value => { setData(value); setError(""); }, (err: unknown) => setError(err instanceof Error ? err.message : String(err)));
  }, [libraryRoot]);
  useEffect(load, [load]);
  useFileChanges(libraryRoot, load, 800);
  const categories = useMemo(() => [...new Set(data?.assets.map(a => a.category) ?? [])], [data]);
  const group = data?.navigation?.find(g => g.id === groupId);
  const subgroup = group?.children.find(s => s.id === subgroupId);
  const filtered = useMemo(() => {
    const members = group ? new Set((subgroup ? [subgroup] : group.children).flatMap(s => s.asset_ids)) : null;
    return filterSharedAssets(data?.assets ?? [], query, data?.navigation ? "" : category, status)
      .filter(a => !members || members.has(a.id))
      .filter(a => !viewStatus || Boolean(a.views) && (viewStatus === "required" || viewStatus === "generated" && Boolean(a.views?.sha256)
        || viewStatus === "accepted" && a.views?.status.startsWith("reviewed") || viewStatus === a.views?.status))
      .sort((a, b) => categories.indexOf(a.category) - categories.indexOf(b.category) || a.id.localeCompare(b.id));
  }, [data, query, category, status, viewStatus, categories, group, subgroup]);
  useEffect(() => { setPage(0); setQuery(""); }, [groupId, subgroupId]);
  const pages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const currentPage = Math.min(page, pages - 1);
  const selected = data?.assets.find(a => a.id === params.get("open"));
  const select = (id: string | null): void => {
    const next = new URLSearchParams(params);
    if (id) {
      next.set("open", id);
      for (const g of data?.navigation ?? []) for (const s of g.children) if (s.asset_ids.includes(id)) {
        next.set("group", g.id); next.set("sub", s.id);
      }
    } else next.delete("open");
    setParams(next, { replace: true });
  };
  const selectCategory = (key: string, value: string): void => {
    const next = new URLSearchParams(params);
    if (value) next.set(key, value); else next.delete(key);
    if (key === "group") next.delete("sub");
    next.delete("open"); setPage(0); setParams(next);
  };
  return <div className="shared-assets-page">
    <header className="shared-assets-heading"><div><p className="shared-eyebrow">系列共用 · 世界规则与美术参考</p><h1>{data?.title.replace(/主数据$/, "") ?? "系列公用资产"}</h1></div>
      <button type="button" onClick={load}>刷新资产</button></header>
    <p>按左侧大类、小类选择资产，点击具体名称在本页查看详情与图片。建筑与场景附正面、侧面、背面三视图；每张图可打开原图查看。</p>
    {group ? <nav className="shared-breadcrumb" aria-label="资产分类位置"><Link to={`/assets?library=${encodeURIComponent(libraryRoot)}`}>公用资产</Link><span> / {group.name}{subgroup ? ` / ${subgroup.name}` : ""}{selected ? ` / ${selected.name}` : ""}</span></nav> : null}
    <nav className="shared-document-links" aria-label="公共资产资料">
      {[['systems.md', '升级与品阶'], ['research/report.md', '深度研究'], ['appendix.md', '术语与采用手册'], ['visual_guide.md', '视觉规范']].map(([path, title]) => <Link key={path} to={sharedFileHref(libraryRoot, path)}>{title}</Link>)}
    </nav>
    {data ? <div className="shared-stats" aria-label="资产进度">
      <span><strong>{data.assets.length}</strong> 项定义</span><span><strong>{data.assets.filter(a => a.image.sha256).length}</strong> 项有图</span>
      <span><strong>{data.assets.filter(acceptedImage).length}</strong> 项基础图已验收</span><span>库版本 {data.version}</span>
      {data.assets.some(a => a.views) ? <><span><strong>{data.assets.filter(a => a.views?.sha256).length}</strong> 项已有三视图</span><span><strong>{data.assets.filter(a => a.views?.status.startsWith("reviewed")).length}</strong> 项三视图已验收</span></> : null}
    </div> : null}
    {selected && data ? <SharedAssetPreview asset={selected} assets={data.assets} libraryRoot={libraryRoot} onClose={() => select(null)} onSelect={select} /> : <>
    {error ? <p role="alert" className="shared-error">公共资产读取失败：{error}。可点击“刷新资产”重试。</p> : null}
    {!data && !error ? <p role="status">正在读取公共资产…</p> : null}
    <div className="shared-filters">
      <input aria-label="搜索公共资产" type="search" placeholder="搜索名称、ID、能力，如重瞳、筑基、飞剑" value={query} onChange={e => { setQuery(e.target.value); setPage(0); }} />
      <select aria-label="资产类别" value={data?.navigation ? groupId : category} onChange={e => { if (data?.navigation) selectCategory("group", e.target.value); else setCategory(e.target.value); setPage(0); }}><option value="">全部类别</option>{data?.navigation ? data.navigation.map(g => <option key={g.id} value={g.id}>{g.name}</option>) : categories.map(c => <option key={c}>{c}</option>)}</select>
      {group ? <select aria-label="资产小类" value={subgroupId} onChange={e => selectCategory("sub", e.target.value)}><option value="">全部小类</option>{group.children.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}</select> : null}
      <select aria-label="验收状态" value={status} onChange={e => { setStatus(e.target.value); setPage(0); }}><option value="">全部状态</option><option value="accepted">全部已验收</option>{Object.entries(IMAGE_STATUS).map(([key, label]) => <option key={key} value={key}>{label}</option>)}</select>
      {data?.assets.some(a => a.views) ? <select aria-label="三视图状态" value={viewStatus} onChange={e => { setViewStatus(e.target.value); setPage(0); }}><option value="">全部三视图状态</option><option value="required">需要三视图的资产</option><option value="generated">已有三视图</option><option value="accepted">三视图已验收</option><option value="revision_required">三视图待修订</option><option value="generated_unreviewed">三视图待验收</option></select> : null}
    </div>
    <p aria-live="polite">找到 {filtered.length} 项资产</p>
    <div className="shared-asset-grid">{filtered.slice(currentPage * PAGE_SIZE, (currentPage + 1) * PAGE_SIZE).map(asset =>
      <button key={asset.id} type="button" className="shared-asset-tile" onClick={() => select(asset.id)} aria-label={`${asset.id} ${asset.name}`}>
        {asset.image.sha256 ? <img src={mediaUrl(sharedFile(libraryRoot, asset.image.anchor))} alt={asset.name} loading="lazy" /> : <div className="shared-no-image">设定已建立 · 暂无图片</div>}
        <div className="shared-tile-body"><small>{asset.id} · {asset.category}</small><h2>{asset.name}</h2><p>{asset.function}</p>
          <span className={acceptedImage(asset) ? "shared-status accepted" : "shared-status"}>{IMAGE_STATUS[asset.image.status] ?? asset.image.status}</span></div>
        {asset.views ? <span className="shared-view-badge">正面 · 侧面 · 背面 · {IMAGE_STATUS[asset.views.status] ?? asset.views.status}</span> : null}
      </button>)}</div>
    {data && !filtered.length ? <p>没有符合条件的资产，请调整搜索词或筛选条件。</p> : null}
    <nav className="shared-pagination" aria-label="资产分页"><button type="button" disabled={!currentPage} onClick={() => setPage(currentPage - 1)}>上一页</button>
      <span>{currentPage + 1} / {pages}</span><button type="button" disabled={currentPage + 1 >= pages} onClick={() => setPage(currentPage + 1)}>下一页</button></nav>
    </>}
  </div>;
}
