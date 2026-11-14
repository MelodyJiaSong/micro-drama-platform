import { useEffect, useState } from "react";
import { createPortal } from "react-dom";
import { Link } from "react-router-dom";
import type { MapRegion } from "../lib/mapRegions";
import { objectColor, objectLabel, originalPoint, RegionObjectDiagram } from "./RegionObjectDiagram";
import "./BuildingComparisonPanel.css";

export function BuildingComparisonPanel({ region, image, file }: { region: MapRegion; image: (p: string) => string; file: (p: string) => string }): JSX.Element | null {
  const [expanded, setExpanded] = useState(false);
  const [labels, setLabels] = useState(true);
  const [filter, setFilter] = useState("all");
  const [referenceMode, setReferenceMode] = useState("game");
  const [targets, setTargets] = useState(false);
  const [showCapacity, setShowCapacity] = useState(false);
  useEffect(() => {
    if (!expanded) return;
    const close = (e: KeyboardEvent) => { if (e.key === "Escape") setExpanded(false); };
    window.addEventListener("keydown", close);
    return () => window.removeEventListener("keydown", close);
  }, [expanded]);
  const comparison = region.building_comparison;
  const overhead = region.views.find(v => v.id === "overhead")?.file;
  if (!comparison || !overhead) return null;
  const capacity = comparison.capacity?.overhead_sha256 === region.views.find(v => v.id === "overhead")?.sha256 ? comparison.capacity : undefined;
  const markers = comparison.markers.filter(m => filter === "all" || m.category === filter);
  const controls = <div className="building-comparison-controls">
    <label>显示对象 <select value={filter} onChange={e => setFilter(e.target.value)}><option value="all">全部对象</option><option value="building">建筑</option><option value="merchant">商店 NPC</option><option value="spawn">出生圈</option></select></label>
    <label><input type="checkbox" checked={labels} onChange={e => setLabels(e.target.checked)} />显示编号</label>
    {comparison.layout_bounds && <><label>右侧对照 <select value={referenceMode} onChange={e => setReferenceMode(e.target.value)}><option value="game">原版游戏截图</option><option value="coordinates">原版坐标俯视</option></select></label><label><input type="checkbox" checked={targets} onChange={e => setTargets(e.target.checked)} />叠加原版目标位置</label></>}
    {capacity && <label><input type="checkbox" checked={showCapacity} onChange={e => setShowCapacity(e.target.checked)} />五英雄活动空间</label>}
  </div>;
  const pair = <div className="building-comparison-pair">{(["generated", "reference"] as const).map(side => {
    if (side === "reference" && referenceMode === "coordinates") return <figure key={side}><figcaption><strong>原版坐标俯视 · 北朝上</strong><small>按生成请求的目标取景范围换算；原始数据重绘，非游戏截图</small></figcaption><RegionObjectDiagram region={region} filter={filter} labels={labels} image={image} /></figure>;
    const size = side === "generated" ? comparison.generated_size : comparison.reference_size;
    const height = size[1] / size[0] * 1000;
    const source = side === "generated" ? overhead : comparison.reference;
    const title = side === "generated" ? "生成俯视图 · 对象标注" : "原版游戏截图 · 相同对象编号";
    return <figure key={side}><figcaption><strong>{title}</strong><small>{side === "generated" ? "按画面中的实际对象标记；虚线圆为原版目标位置" : comparison.reference_label}</small></figcaption>
      <svg viewBox={`0 0 1000 ${height}`} role="img" aria-label={`${region.id} ${title}`}>
        <image href={image(source)} width="1000" height={height} />
        {side === "generated" && showCapacity && capacity && <g aria-label="五英雄活动范围示意">
          <polygon points={capacity.area.map(([x,y]) => `${x*10},${y/100*height}`).join(" ")} fill="#22d3ee" fillOpacity=".12" stroke="#0891b2" strokeWidth="3" strokeDasharray="10 6" />
          {capacity.heroes.map(([x,y,rx,ry],i) => <g key={i}><ellipse cx={x*10} cy={y/100*height} rx={rx*10} ry={ry/100*height} fill="#e0f2fe" fillOpacity=".7" stroke="#075985" strokeWidth="3" /><text x={x*10} y={y/100*height} dominantBaseline="central" textAnchor="middle" fontSize="20" fontWeight="bold" fill="#075985">H{i+1}</text></g>)}
        </g>}
        {side === "generated" && targets && markers.map(marker => { const p = originalPoint(region, marker); return p && <g key={marker.asset_id}><circle cx={p[0]*10} cy={p[1]/100*height} r="18" fill="none" stroke="#06b6d4" strokeWidth="4" strokeDasharray="6 4" /><path d={`M${p[0]*10-10},${p[1]/100*height}h20M${p[0]*10},${p[1]/100*height-10}v20`} stroke="#06b6d4" strokeWidth="2" /></g>; })}
        {labels && markers.map(marker => {
          const position = marker[side]; if (!position) return null;
          const [px, py, lx, ly] = position;
          const x = px * 10, y = py / 100 * height, tx = lx * 10, ty = ly / 100 * height;
          const color = objectColor(marker.category);
          return <g key={marker.asset_id}>
            <path d={`M${tx},${ty}L${x},${y}`} stroke="white" strokeWidth="6" />
            <path d={`M${tx},${ty}L${x},${y}`} stroke={color} strokeWidth="3" />
            <circle cx={x} cy={y} r="7" fill={color} stroke="white" strokeWidth="3" />
            <rect x={tx-40} y={ty-17} width="80" height="34" rx="6" fill="white" stroke={color} strokeWidth="2" />
            <text x={tx} y={ty} dominantBaseline="central" textAnchor="middle" fontSize="23" fontWeight="700" fontFamily="Arial, sans-serif" fill={color}>{objectLabel(marker.asset_id)}</text>
          </g>;
        })}
      </svg>
      <a href={image(source)} download>下载未标注{side === "generated" ? "生成图" : "游戏原图"}</a>
    </figure>;
  })}</div>;
  const legend = <div className="building-comparison-legend">{markers.map(m => {
    const a = region.assets.find(a => a.id === m.asset_id);
    const name = region.instances.find(i => i.asset_id === m.asset_id)?.name ?? a?.name.replace(new RegExp(`^${m.asset_id}_`), "");
    return a ? <Link key={a.id} to={file(a.card)}><b style={{ color: objectColor(m.category) }}>{a.id}</b> {name}</Link> : <span key={m.asset_id}><b style={{ color: objectColor(m.category) }}>{objectLabel(m.asset_id)}</b> {m.asset_id}</span>;
  })}</div>;
  return <section className="building-comparison" aria-label={`${region.id} 泉水建筑对照`}>
    <header><h3>泉水区 · 建筑、NPC 与出生圈对照</h3><button onClick={() => setExpanded(true)}>放大并排对照</button></header>
    <p>红色：建筑 · 绿色：商店 NPC · 蓝色：出生圈。每方 7 位人形商人＋1 个小精灵，均有商店功能。</p>
    {controls}{pair}{showCapacity && capacity && <p>{capacity.note}</p>}{legend}<p className="building-comparison-note">{comparison.note}</p>
    {comparison.markers.some(m => m.reference_note) && <details><summary>截图遮挡与识别说明</summary><ul>{comparison.markers.filter(m => m.reference_note).map(m => <li key={m.asset_id}>{m.asset_id}：{m.reference_note}</li>)}</ul></details>}
    <Link to={file(comparison.source_record)}>原版截图来源与观察记录</Link>
    {expanded && createPortal(<div className="building-comparison-modal" role="dialog" aria-modal="true" aria-label={`${region.id} 放大建筑对照`}>
      <header><h2>{region.id} 泉水对象对照</h2><button autoFocus onClick={() => setExpanded(false)}>关闭对照</button></header>
      {controls}{pair}{showCapacity && capacity && <p>{capacity.note}</p>}{legend}<p>{comparison.note}</p>
    </div>, document.body)}
  </section>;
}
