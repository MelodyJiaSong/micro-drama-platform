import { Link } from "react-router-dom";
import type { MapRegion } from "../lib/mapRegions";
import { ZoomableImage } from "./ZoomableImage";

export function RegionOriginalPanel({ region, sourceMap, image, file }: {
  region: MapRegion; sourceMap: string; image: (p: string) => string; file: (p: string) => string;
}): JSX.Element {
  const ref = region.original_reference;
  if (!ref) return <section className="map-region-image" aria-label={`${region.id} 原图对照`}><h3>原图 · 完整地图</h3><ZoomableImage src={image(sourceMap)} alt={`${region.id} 原版完整地图`} /><p>本区专用原图尚未归档，先参考完整地图。</p></section>;
  const [x, y, right, bottom] = ref.map_bounds;
  return <section className="map-region-image map-region-original" aria-label={`${region.id} 原图对照`}>
    <h3>原图 · {ref.kind === "gameplay" ? "游戏实机" : "本区地图"}</h3><p>{ref.label}</p>
    {ref.kind === "gameplay" ? <ZoomableImage src={image(ref.file)} alt={`${region.id} ${region.name} 游戏原图`} /> :
      <svg viewBox={`${x} ${y} ${right - x} ${bottom - y}`} role="img" aria-label={`${region.id} ${region.name} 原版地图局部`}><image href={image(ref.file)} width="100" height="100" /></svg>}
    <p>{ref.note}</p>
    <p><a href={image(ref.file)} download>下载{ref.kind === "gameplay" ? "游戏原图" : "原版完整地图"}</a>{" · "}<Link to={file(ref.source_record)}>查看原图来源</Link></p>
    <details><summary>在完整原版地图上定位本区</summary><svg viewBox="0 0 100 100" role="img" aria-label={`${region.id} 原图区域定位`}><image href={image(sourceMap)} width="100" height="100" /><rect x={x} y={y} width={right-x} height={bottom-y} fill="none" stroke="#ff3030" strokeWidth="1" /><text x={x+1} y={y+5} fill="white" stroke="black" strokeWidth=".3" paintOrder="stroke" fontSize="5">{region.id}</text></svg><a href={image(sourceMap)} download>下载无标记整图</a></details>
  </section>;
}
