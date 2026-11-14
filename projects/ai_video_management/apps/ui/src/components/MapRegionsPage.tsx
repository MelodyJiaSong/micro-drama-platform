import { useEffect, useRef, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { mediaUrl } from "../api";
import { BASE_LAYOUT_ROUTE, layoutFile } from "../lib/baseLayout";
import { loadRegionMap, type RegionMap } from "../lib/mapRegions";
import { useFileChanges } from "../lib/fileEvents";
import { dramaOfStagePath, shopItemsUrl } from "../lib/shopItems";
import { useShopItems } from "../lib/useShopItems";
import { ZoomableImage } from "./ZoomableImage";
import { BuildingComparisonPanel } from "./BuildingComparisonPanel";
import { MapNavigationPanel } from "./MapNavigationPanel";
import { RegionOriginalPanel } from "./RegionOriginalPanel";
import "./MapRegionsPage.css";
import "./ShopItemsPage.css";

const statusLabel: Record<string, string> = { existing: "已有远景", planned: "待生成", running: "生成中", generated: "候选图", reviewed: "已初审", layout_stale: "旧布局待更新", layout_candidate: "布局待核准", qc_passed: "独立冷看通过", qc_conditional: "冷看有条件通过", layout_map: "仅作布局地图", qc_failed: "冷看未通过", unknown: "生成未完成", blocked: "等待主图", failed: "生成失败" };
export function MapRegionsPage(): JSX.Element {
  const [params, setParams] = useSearchParams();
  const path = params.get("path") ?? "";
  const [data, setData] = useState<RegionMap | null>(null);
  const [error, setError] = useState("");
  const [revision, refresh] = useState(Date.now);
  const [query, setQuery] = useState("");
  const [angle, setAngle] = useState("overhead");
  const [compare, setCompare] = useState(true);
  const regionId = params.get("region");
  useEffect(() => { setAngle("overhead"); }, [path, regionId]);
  const detail = useRef<HTMLElement>(null);
  const drama = dramaOfStagePath(path);
  const shop = useShopItems(drama);
  const shopSellers = new Set(shop?.sellers.map(s => s.key) ?? []);
  useFileChanges(path ? path.slice(0, path.lastIndexOf("/")) : null, () => refresh(Date.now()));
  useEffect(() => {
    let cancelled = false;
    if (!path) { setError("请从剧内地图资产入口打开。"); return; }
    setError("");
    loadRegionMap(path).then(m => { if (!cancelled) setData(m); }, e => { if (!cancelled) setError(String(e.message ?? e)); });
    return () => { cancelled = true; };
  }, [path, revision]);
  useEffect(() => {
    if (data && params.get("focus") === "buildings") detail.current?.scrollIntoView?.({ block: "start" });
  }, [data, params]);
  if (error) return <section className="map-regions"><h1>地图资产</h1><p role="alert">{error}</p><button onClick={() => refresh(Date.now())}>重新加载</button></section>;
  if (!data) return <p role="status">加载地图区域…</p>;
  const region = data.regions.find(r => r.id === params.get("region")) ?? data.regions[0];
  if (!region) return <p>暂无区域。</p>;
  const group = data.groups.find(g => g.id === region.parent)!;
  const view = angle === "original" ? undefined : region.views.find(v => v.id === angle) ?? region.views.find(v => v.id === "overhead") ?? region.views[0];
  const overhead = region.views.find(v => v.id === "overhead");
  const sameOverhead = view?.reference_overhead?.file === overhead?.file && view?.reference_overhead?.sha256 === overhead?.sha256;
  const reviewedOverhead = view?.layout_review?.overhead_sha256 === overhead?.sha256 && view?.layout_review?.view_sha256 === view?.sha256 && !!view?.layout_review;
  const image = (p: string) => mediaUrl(layoutFile(path, p), revision);
  const file = (p: string) => `/file/${encodeURIComponent(layoutFile(path, p))}`;
  const select = (id: string) => { setAngle("overhead"); const next = new URLSearchParams(params); next.set("region", id); setParams(next); detail.current?.scrollIntoView?.({ block: "start" }); };
  const available = data.regions.flatMap(r => r.views).filter(v => v.file).length;
  const total = data.regions.reduce((n, r) => n + r.views.length, 0);
  const filtered = data.regions.filter(r => `${r.id} ${r.name} ${r.asset_id} ${r.assets.map(a => a.id + a.name).join(" ")}`.toLocaleLowerCase().includes(query.trim().toLocaleLowerCase()));
  return <section className="map-regions">
    <header className="map-regions-header"><div><h1>{data.title}</h1><p>{data.version} · {data.groups.length} 个大区 · {data.regions.length} 个拍摄区 · {available}/{total} 张机位图可查看</p></div><div>{shop && <Link className="shop-entry-link" to={shopItemsUrl(drama)} title="建筑商店、商人 NPC 与 Roshan 掉落各卖什么">🛒 商店货单 · {shop.sellers.length} 个出售方</Link>} <button onClick={() => refresh(Date.now())}>刷新状态</button></div></header>
    <section className="map-regions-overview" aria-label="完整地图与原图对照">
      <h2>先看整张地图 · 大区与原图对照</h2>
      <p>两图方向、范围一致，北在上。红线圈出制作大区；字母是大区代号，字母＋数字是拍摄区，点击编号进入区域，点击地图空白处放大。</p>
      <div className="map-regions-comparison">
        <figure><figcaption><strong>① 完整原图＋红线分区</strong><span>保留全地图地形，标出 {data.groups.length} 个大区和 {data.regions.length} 个拍摄区</span></figcaption>
          <div className="map-regions-map"><ZoomableImage src={image(data.overview)} alt="DotA 完整原图地图，红线标注大区边界及区域代号" />{data.regions.map(r => <button key={r.id} className={r.id === region.id ? "selected" : ""} style={{ left: `${r.position[0]}%`, top: `${r.position[1]}%` }} onClick={() => select(r.id)} aria-label={`定位 ${r.id} ${r.name}`} title={`${r.id} ${r.name}`} />)}</div>
          <a href={image(data.overview)} download>下载标记地图</a>
        </figure>
        <figure><figcaption><strong>② 完整原图 · 对照</strong><span>同一张游戏原版地图，未加分区标记</span></figcaption>
          <div className="map-regions-original"><ZoomableImage src={image(data.source_map)} alt="DotA 6.83d 完整原版地图，无分区标注" /></div>
          <a href={image(data.source_map)} download>下载原版底图</a>
        </figure>
      </div>
      <div className="map-regions-legend" aria-label="大区代号与下属区域">{data.groups.map(g => <div key={g.id}><strong><button onClick={() => { const first = data.regions.find(r => r.parent === g.id); if (first) select(first.id); }} aria-label={`查看${g.name}`}><b>{g.id}</b> {g.name}</button></strong><div>{data.regions.filter(r => r.parent === g.id).map(r => <button key={r.id} onClick={() => select(r.id)} aria-current={r.id === region.id ? "page" : undefined}>{r.id} {r.name}</button>)}</div></div>)}</div>
      <p className="map-regions-source-note">底图为 DotA 6.83d 原版地图纹理（256 × 256，完整放大显示）。红线为本剧资产管理分区，区域编号为定位示意；基地建筑的原版坐标见区域详情。</p>
    </section>
    {data.navigation && <details><summary>整张地图 · 展开通行、高低地与树木研究</summary><MapNavigationPanel path={path} source={data.navigation} revision={revision} /></details>}
    <div className="map-regions-layout">
      <nav className="map-regions-tree" aria-label="地图资产层级"><strong>整张地图</strong><label>查找区域或资产<input value={query} onChange={e => setQuery(e.target.value)} placeholder="泉水、bg25、R2…" /></label>
        {data.groups.map(g => <details key={g.id} open><summary onClick={() => { const first = data.regions.find(r => r.parent === g.id); if (first) select(first.id); }}><span style={{ color: g.color }}>●</span> {g.id} {g.name}</summary>{filtered.filter(r => r.parent === g.id).map(r => <button key={r.id} aria-current={r.id === region.id ? "page" : undefined} onClick={() => select(r.id)}><b>{r.id}</b> {r.name}<small>{r.asset_id} · {r.views.filter(v => v.file).length}/{r.views.length} 图</small></button>)}</details>)}
        {!filtered.length && <p>没有匹配区域。</p>}
      </nav>
      <main className="map-regions-content">
        <article ref={detail} className="map-region-detail" aria-label="区域详情">
          <p className="map-region-breadcrumb">整图 / {group.id} {group.name} / {region.id}</p><h2>{region.id} {region.name} <small>{region.asset_id}</small></h2><p>{region.note}</p>
          <p><Link to={file(region.card)}>场景资产卡</Link>{" · "}<Link to={`${BASE_LAYOUT_ROUTE}?${new URLSearchParams({ path: layoutFile(path, data.base_layout), faction: region.parent === "D" ? "scourge" : "sentinel" })}`}>基地原版坐标与建筑对照</Link></p>
          {region.base_connection && <section className="map-region-image" aria-label="泉水与大本营连接"><h3>泉水出口 → {region.base_connection.landmark}大本营</h3><p>{region.base_connection.note}</p><button onClick={() => select(region.base_connection!.region)}>查看 {region.base_connection.region} 大本营区域</button><details><summary>展开全基地原版坐标图 · 核对泉水与遗迹的位置</summary><ZoomableImage src={image(region.base_connection.plan)} alt={`${region.id} 泉水与大本营完整坐标依据`} /></details></section>}
          {data.navigation && <MapNavigationPanel key={`navigation:${region.id}`} path={path} source={data.navigation} regionId={region.id} revision={revision} />}
          <BuildingComparisonPanel key={region.id} region={region} image={image} file={file} />
          <div className="map-region-angles" role="group" aria-label="区域机位">{[...region.views].sort((a,b) => Number(b.id === "overhead") - Number(a.id === "overhead")).map(v => <button key={v.id} aria-pressed={view?.id === v.id} onClick={() => setAngle(v.id)}>{v.label}<small>{statusLabel[v.status] ?? v.status}</small></button>)}<button aria-pressed={angle === "original"} onClick={() => setAngle("original")}>原图<small>游戏参考</small></button></div>
          {angle !== "original" && <label className="map-region-compare-toggle"><input type="checkbox" checked={compare} onChange={e => setCompare(e.target.checked)} />并排显示原图</label>}
          <div className={view && compare ? "map-region-view-comparison" : undefined}>
          {view && <div className="map-region-image">{view.reference_overhead && <p className="map-region-reference">{sameOverhead ? "本机位以当前俯视图为参考生成" : reviewedOverhead ? `已按当前俯视复核：${view.layout_review!.note}` : "参考俯视图已更新，本机位需要复核"}{" · "}<a href={image(view.reference_overhead.file)} target="_blank" rel="noreferrer">查看生成时使用的俯视母图</a>{" · "}<button onClick={() => setAngle("overhead")}>切换俯视对照</button></p>}{view.file ? <><ZoomableImage src={image(view.file)} alt={`${region.id} ${region.name} ${view.label}`} /><a href={image(view.file)} download>下载{view.label}原图</a></> : <p role="status">{view.label} · {statusLabel[view.status] ?? view.status}</p>}<p>{view.review}</p><Link to={file(view.prompt)}>查看本机位描述</Link>{view.layout_render && <>{" · "}<a href={image(view.layout_render.file)} target="_blank" rel="noreferrer">查看同机位三维布局渲染</a></>}</div>}
          {(angle === "original" || compare) && <RegionOriginalPanel key={region.id} region={region} sourceMap={data.source_map} image={image} file={file} />}
          </div>
          {region.floorplan && <details className="map-region-image"><summary>本区坐标平面图 · 建筑、商人与出生点</summary><ZoomableImage src={image(region.floorplan)} alt={`${region.id} 原版坐标换算平面图`} /><a href={image(region.floorplan)} download>下载本区平面图</a>{region.blocks && <> · <Link to={file(region.blocks)}>位置与机位数据</Link></>}</details>}
          <h3>区域内的建筑与人物资产 · {region.assets.length}</h3><div className="map-region-assets">{region.assets.map(a => <article key={a.id}><Link to={file(a.card)}>{a.id} {a.name}</Link>{shopSellers.has(a.id) && <>{" · "}<Link to={shopItemsUrl(drama, { seller: a.id })}>🛒 货单</Link></>}{a.image && <ZoomableImage loading="lazy" src={image(a.image)} alt={`${a.id} ${a.name}`} />}</article>)}</div>{!region.assets.length && <p>以自然地貌为主；人物、野怪在镜头制作时单独挂入。</p>}
          {!!region.instances.length && <details><summary>原版位置与实例 · {region.instances.length} 处</summary><div className="map-region-table"><table><thead><tr><th>实例</th><th>名称</th><th>原版 X / Y</th></tr></thead><tbody>{region.instances.map(i => <tr key={i.instance_id}><td>{i.instance_id}</td><td>{i.name}</td><td>{i.x}, {i.y}</td></tr>)}</tbody></table></div></details>}
        </article>
        <details><summary>范围与来源说明</summary><ul>{data.notes.map(n => <li key={n}>{n}</li>)}</ul></details>
      </main>
    </div>
  </section>;
}
