import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { mediaUrl } from "../api";
import { layoutFile } from "../lib/baseLayout";
import { inspectNavigation, inspectSegment, loadNavigation, type MapNavigation, type NavigationGrid, type NavigationPoint } from "../lib/mapNavigation";
import { ZoomableImage } from "./ZoomableImage";
import "./MapNavigationPanel.css";

export function MapNavigationPanel({ path, source, regionId, revision }: { path: string; source: string; regionId?: string; revision: number }): JSX.Element {
  const [loaded, setLoaded] = useState<{data: MapNavigation; grid: NavigationGrid} | null>(null);
  const [error, setError] = useState("");
  const [layers, setLayers] = useState(["blocked", "trees", "cliffs", "ramps", "uncertain"]);
  const [points, setPoints] = useState<NavigationPoint[]>([]);
  useEffect(() => { let live=true; setError(""); setLoaded(null); loadNavigation(path,source).then(v=>{if(live)setLoaded(v);},e=>{if(live)setError(e.message);}); return()=>{live=false;}; },[path,source,revision]);
  useEffect(()=>setPoints([]),[regionId,source,revision]);
  if(error) return <section className="map-navigation"><p role="alert">通行研究加载失败：{error}</p></section>;
  if(!loaded) return <p role="status">加载原版通行研究…</p>;
  const {data,grid}=loaded;
  const region=regionId ? data.regions[regionId] : undefined;
  if(regionId && !region) return <p role="alert">本区尚无通行研究，不能引用其他区域数据。</p>;
  const bounds=(region?.bounds ?? [0,0,100,100]).map(n=>n*5.12);
  const [x0,y0,x1,y1]=bounds, width=x1-x0, height=y1-y0;
  const image=(p:string)=>mediaUrl(layoutFile(path,p),revision);
  const file=(p:string)=>`/file/${encodeURIComponent(layoutFile(path,p))}`;
  const selected=points.length ? inspectNavigation(grid,points[points.length-1]) : null;
  const hits=points.length===2 ? inspectSegment(grid,points[0],points[1]) : null;
  const names=(ids:string[])=>ids.map(id=>data.layers.find(l=>l.id===id)?.label ?? (id==="outside"?"地图外":id)).join("、");
  function pick(event: React.MouseEvent<SVGSVGElement>) {
    const rect=event.currentTarget.getBoundingClientRect();
    const point={x:x0+(event.clientX-rect.left)/rect.width*width,y:y0+(event.clientY-rect.top)/rect.height*height};
    setPoints(old=>old.length===2 ? [point] : [...old,point]);
  }
  return <section className="map-navigation" aria-label={regionId ? `${regionId} 通行与高差研究` : "整图通行与高差研究"}>
    <h3>{regionId ?? "整图"} · 通行、高低地与阻挡</h3>
    <p>北在上，左右共用原版坐标。左为数据重建图，右为 6.83d 原地图；勾选图层同步对照。高程底色由蓝（低）到沙色（高），点击可读地形层。蓝色只表示低地，不代表该处一定有水。</p>
    <div className="navigation-layers">{data.layers.map(l=><label key={l.id} title={l.note}><input type="checkbox" checked={layers.includes(l.id)} onChange={()=>setLayers(old=>old.includes(l.id)?old.filter(x=>x!==l.id):[...old,l.id])}/><i style={{background:l.color}}/>{l.label}</label>)}</div>
    <div className="navigation-layers" aria-label="地形高度图例">{[["L8 低", "#4a8db9"],["L9", "#73ada4"],["L10", "#c7c19b"],["L11", "#e1ae72"],["L12–13 高", "#d38c5d"]].map(([label,color])=><span key={label}><i style={{display:"inline-block",background:color,marginRight:5}}/>{label}</span>)}</div>
    <div className="navigation-pair">{[{title:"数据重建 · 地形层与阻挡",src:data.reconstruction},{title:"6.83d 原图 · 相同坐标标注",src:data.source_map}].map(item=><figure key={item.src}>
      <figcaption>{item.title}</figcaption>
      <svg viewBox={`${x0} ${y0} ${width} ${height}`} style={{aspectRatio:`${width}/${height}`}} onClick={pick} role="img" aria-label={`${regionId ?? "整图"} ${item.title}，点击两点检查直线路段`}>
        <image href={image(item.src)} width="512" height="512" preserveAspectRatio="none" />
        {data.layers.filter(l=>layers.includes(l.id)).map(l=><image key={l.id} href={image(l.file)} width="512" height="512" preserveAspectRatio="none"/>)}
        {points.length===2 && <line x1={points[0].x} y1={points[0].y} x2={points[1].x} y2={points[1].y} stroke={hits?.length?"#fffbeb":"#ffffff"} strokeWidth={width/200} strokeDasharray={`${width/90} ${width/130}`}/>}
        {points.map((p,i)=><g key={i}><circle cx={p.x} cy={p.y} r={width/65} fill="#fff" stroke="#172554" strokeWidth={width/300}/><text x={p.x} y={p.y} textAnchor="middle" dominantBaseline="central" fontSize={width/45} fill="#172554">{i+1}</text></g>)}
      </svg>
    </figure>)}</div>
    <p>点两处检查直线路段（含 32 游戏单位方形余量）；第三次点击重新开始。<button onClick={()=>setPoints([])}>清除路线</button></p>
    <div className="navigation-result" aria-live="polite">{selected ? <p>当前位置 X/Y：{selected.world.join(" / ")} · 地形层 L{selected.layer} · {names(selected.flags)}</p> : <p>高低是相对关系：河谷、坡道、基地平台分别核对，不能仅凭画面颜色判断可通行。</p>}
      {hits && <p><strong>{hits.length ? `该直线路段命中：${names(hits)}。需绕行或重新核实，不能用于普通行走。` : "当前静态图层未发现该直线路段阻挡；尚未通过实机与角色碰撞验证。"}</strong></p>}
    </div>
    {region && <p>本区记录 {region.tree_count} 棵树 · 高程层 {Object.keys(region.layer_percentages).map(l=>`L${l}`).join(" / ")} · 原版顶点高度 {region.ground_vertex_z_range.join("–")} 游戏单位。</p>}
    <p><Link to={file(data.report)}>调研依据与已知限制</Link>{region && <> · <Link to={file(region.constraints)}>本区出图／视频约束</Link></>} · <a href={image(`navigation/${regionId ? regionId+"_" : ""}original${regionId?"":"_annotated"}_export.png`)} download>下载原图标注</a> · <a href={image(`navigation/${regionId ? regionId+"_" : ""}reconstruction${regionId?"":"_annotated"}_export.png`)} download>下载重建标注</a></p>
    <details><summary>证据等级与未验证范围</summary><ul>{data.layers.map(l=><li key={l.id}><strong>{l.label}：</strong>{l.note}</li>)}{data.limitations.map(l=><li key={l}>{l}</li>)}</ul></details>
    {region?.candidate && <details className="navigation-candidate"><summary>查看本区出图与原图对照 · {region.candidate.status}</summary><p>{region.candidate.review}</p>{region.candidate.reference_layout && <details><summary>生成时直接参考的布局图</summary><p>自绘数据图：深绿为树木占地，灰红为静态禁行，黄为坡道候选；橙点为建筑中心，白点为人物或出生点，青点为精灵。底色表示高度层，不表示水域；点的大小不等于物体占地。</p><ZoomableImage src={image(region.candidate.reference_layout.file)} alt={`${regionId} 生成输入布局图`} /><p><a href={image(region.candidate.reference_layout.file)} target="_blank" rel="noreferrer">打开生成参考布局图</a> · {region.candidate.reference_layout.navigation_revision} · 布局指纹 {region.candidate.reference_layout.sha256.slice(0,12)}</p></details>}<p>图内代号和引导线同样需要核对，不能覆盖原版数据结论。</p><div className="navigation-pair"><figure><figcaption>出图版本 · 尚未成为路线母图</figcaption><ZoomableImage src={image(region.candidate.file)} alt={`${regionId} 地形出图待核对`} /></figure><figure><figcaption>原版坐标标注 · 核对地形关系</figcaption><ZoomableImage src={image(`navigation/${regionId}_original.png`)} alt={`${regionId} 原版通行标注对照`} /></figure></div><Link to={file(region.candidate.prompt)}>本次出图约束</Link></details>}
    <p className="navigation-boundary">电影机位还未完成与原版网格的空间配准。下方所有角度共用本区约束；人物路线先在研究图检查，再在实际镜头复核。</p>
  </section>;
}
