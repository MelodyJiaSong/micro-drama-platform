import { useEffect, useMemo, useRef, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { mediaUrl } from "../api";
import { MAP_REGIONS_ROUTE } from "../lib/mapRegions";
import { layoutFile, loadBaseLayout, type BaseChartMode, type BaseFaction } from "../lib/baseLayout";
import { useFileChanges } from "../lib/fileEvents";
import { ZoomableImage } from "./ZoomableImage";
import "./BaseLayoutPage.css";

export function BaseLayoutPage(): JSX.Element {
  const [params, setParams] = useSearchParams();
  const path = params.get("path") ?? "";
  const faction: BaseFaction = params.get("faction") === "scourge" ? "scourge" : "sentinel";
  const [data, setData] = useState<Awaited<ReturnType<typeof loadBaseLayout>> | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [mode, setMode] = useState<BaseChartMode>("asset");
  const [query, setQuery] = useState("");
  const [selected, setSelected] = useState<string | null>(null);
  const preview = useRef<HTMLElement>(null);
  const [revision, refresh] = useState(Date.now);
  useEffect(() => { if (selected) preview.current?.scrollIntoView?.({ behavior: "smooth", block: "nearest" }); }, [selected]);
  useFileChanges(path ? path.slice(0, path.lastIndexOf("/")) : null, () => refresh(() => Date.now()));
  useEffect(() => {
    let cancelled = false;
    setData(null); setError(null); setSelected(null);
    if (!path) { setError("请从剧内的「基地布局」入口打开。"); return; }
    loadBaseLayout(path).then(value => { if (!cancelled) setData(value); }, reason => {
      if (!cancelled) setError(reason instanceof Error ? reason.message : String(reason));
    });
    return () => { cancelled = true; };
  }, [path, revision]);
  const rows = useMemo(() => data?.layout.rows.filter(r => r.faction === faction) ?? [], [data, faction]);
  const filtered = rows.filter(r => `${r.point_number} ${r.instance_id} ${r.name}`.toLocaleLowerCase().includes(query.trim().toLocaleLowerCase()));
  if (error) return <section className="base-layout-page"><h1>基地布局</h1><p role="alert">{error}</p><button onClick={() => refresh(() => Date.now())}>重新加载</button></section>;
  if (!data) return <p role="status">加载基地布局…</p>;
  const { layout, references } = data;
  const image = (relative: string): string => mediaUrl(layoutFile(path, relative), revision);
  const fileHref = (relative: string): string => `/file/${encodeURIComponent(layoutFile(path, relative))}`;
  const buildings = rows.filter(r => r.category === "building");
  const missing = buildings.filter(r => !r.asset_id || !layout.assets[r.asset_id]?.anchor).length;
  const assetIds = [...new Set(rows.filter(r => r.category === "building" && r.asset_id).map(r => r.asset_id!))];
  const active = selected ? layout.assets[selected] : null;
  const assembly = data.assembly?.[faction];
  const factionName = faction === "sentinel" ? "近卫" : "天灾";
  return <section className="base-layout-page">
    <header><div><h1>{layout.title || "两方基地 · 坐标与素材"}</h1><p>{layout.version} · 原版位置与本剧建筑素材</p></div><button onClick={() => refresh(() => Date.now())}>刷新资料</button></header>
    {layout.map_regions && <p><Link to={`${MAP_REGIONS_ROUTE}?${new URLSearchParams({ path: layoutFile(path, layout.map_regions) })}`}>整张地图 · 分区与多机位资产 →</Link></p>}
    <nav aria-label="基地"><button aria-pressed={faction === "sentinel"} onClick={() => { const next = new URLSearchParams(params); next.set("faction", "sentinel"); setParams(next); setSelected(null); }}>近卫基地</button><button aria-pressed={faction === "scourge"} onClick={() => { const next = new URLSearchParams(params); next.set("faction", "scourge"); setParams(next); setSelected(null); }}>天灾基地</button></nav>
    <p className="base-layout-summary">{buildings.length} 座建筑 · {assetIds.length} 类建筑素材 · {rows.filter(r => r.category === "merchant").length} 位商人 · {rows.filter(r => r.category === "spawn").length} 个出生圈{missing ? ` · ${missing} 座建筑待补图` : " · 建筑主图已齐"}</p>
    <div role="group" aria-label="坐标图类型" className="base-layout-controls">
      {([["asset", "真实资产编号"], ["number", "数字位置编号"], ["shops", "泉水与商店放大图"]] as const).map(([value, label]) => <button key={value} aria-pressed={mode === value} onClick={() => setMode(value)}>{label}</button>)}
      <a href={image(layout.charts[faction][mode])} download>下载当前坐标图</a>
    </div>
    <ZoomableImage className="base-layout-map" src={image(layout.charts[faction][mode])} alt={`${factionName}基地${mode === "shops" ? "泉水与商店" : mode === "number" ? "数字位置" : "资产编号"}坐标图`} />
    <p>同款建筑共用资产，用 <code>bg19#01</code> 等实例号区分位置。坐标为游戏世界单位；建筑占地、高度和电影尺度尚待确定。</p>
    {assembly && <details className="base-layout-assembly"><summary>搭景方案 · {assembly.asset_id} · 米制平面图与摆放表</summary>
      <p>{assembly.note}</p><p><Link to={fileHref(assembly.card)}>整体场景卡</Link> · <Link to={fileHref(assembly.placements)}>逐实例摆放表</Link> · <Link to={fileHref(assembly.blocks)}>场地尺寸与机位</Link>{assembly.blend && <> · <a href={image(assembly.blend)} download>下载 Blender 场景</a></>}</p>
      <ZoomableImage className="base-layout-map" src={image(assembly.floorplan)} alt={`${factionName}基地米制搭景候选`} />
      {assembly.terrain && <><h3>原版地形高程调查</h3><ZoomableImage className="base-layout-map" src={image(assembly.terrain)} alt={`${factionName}基地原版地形高程调查`} /></>}
      {assembly.overview && <><h3>电影概念候选</h3><ZoomableImage className="base-layout-map" src={image(assembly.overview)} alt={`${factionName}基地电影概念候选`} /></>}
      {assembly.checks?.map((check, i) => <ZoomableImage key={check} className="base-layout-map" src={image(check)} alt={`${factionName}基地白模取景 ${i + 1}`} />)}
    </details>}
    <h2>位置与素材对照</h2><label>搜索位置、建筑或资产编号 <input value={query} onChange={e => setQuery(e.target.value)} placeholder="例如 bg37、泉水、01" /></label>
    <div className="base-layout-table"><table><thead><tr><th>位置号</th><th>实例</th><th>名称</th><th>X / Y</th><th>脚本朝向</th><th>素材</th></tr></thead><tbody>
      {filtered.map(r => <tr key={r.instance_id}><td>{r.point_number}</td><td>{r.instance_id}</td><td>{r.name}</td><td>{r.x}, {r.y}</td><td>{r.facing}°</td><td>{r.asset_id && layout.assets[r.asset_id] ? <button onClick={() => setSelected(r.asset_id)}>查看 {r.asset_id}</button> : "待补独立素材"}</td></tr>)}
    </tbody></table>{!filtered.length && <p>没有匹配的位置。</p>}</div>
    {active && <aside ref={preview} className="base-layout-preview" aria-label="选中素材"><header><h2>{active.name}</h2><button onClick={() => setSelected(null)}>关闭预览</button></header>{(active.views || active.anchor) && <ZoomableImage src={image((active.views || active.anchor)!)} alt={active.name} />}<p>{active.status}</p><Link to={fileHref(active.card)}>打开建筑 / 人物卡</Link></aside>}
    <h2>{factionName}建筑素材</h2><div className="base-layout-grid">{assetIds.map(id => {
      const a = layout.assets[id]; if (!a) return null;
      return <article key={id}><h3><Link to={fileHref(a.card)}>{a.name}</Link></h3>{a.views || a.anchor ? <ZoomableImage loading="lazy" src={image((a.views || a.anchor)!)} alt={a.name} /> : <p>待生成</p>}<p>{a.status}</p></article>;
    })}</div>
    <h2>原游戏参考</h2><p>用于人眼核对建筑与位置；相邻版本只辅助对照外观。</p><div className="base-layout-grid">{references.map(r => <article key={r.file}><ZoomableImage loading="lazy" src={image(r.file)} alt={r.caption} /><h3>{r.caption}</h3><p>{r.status}</p><a href={image(r.file)} download>下载参考原图</a>{" · "}{r.source_url && /^https?:\/\//i.test(r.source_url) ? <a href={r.source_url} target="_blank" rel="noreferrer">原始来源</a> : r.source_record ? <Link to={fileHref(r.source_record)}>来源记录</Link> : null}</article>)}</div>
    <details><summary>制作范围与待完善项</summary><ul>{layout.limitations.map(note => <li key={note}>{note}</li>)}</ul></details>
  </section>;
}
