import type { BuildingComparison, MapRegion } from "../lib/mapRegions";

export function originalPoint(region: MapRegion, marker: BuildingComparison["markers"][number]): [number, number] | null {
  const bounds = region.building_comparison?.layout_bounds;
  const row = region.instances.find(r => r.instance_id === (marker.instance_id ?? `${marker.asset_id}#01`));
  if (!bounds || !row) return null;
  return [(row.x - bounds[0]) / (bounds[2] - bounds[0]) * 100, (bounds[3] - row.y) / (bounds[3] - bounds[1]) * 100];
}
export function objectColor(category?: string): string { return category === "merchant" ? "#087d47" : category === "spawn" ? "#1d4ed8" : "#b91c1c"; }
export function objectLabel(id: string): string { return id.replace("SPAWN#0", "P"); }
export function RegionObjectDiagram({ region, filter, labels, image }: { region: MapRegion; filter: string; labels: boolean; image: (p: string) => string }): JSX.Element {
  const comparison = region.building_comparison!;
  const bounds = comparison.layout_bounds!;
  const height = Math.round((bounds[3] - bounds[1]) / (bounds[2] - bounds[0]) * 1000);
  const underlay = comparison.layout_underlay;
  return <svg viewBox={`0 0 1000 ${height}`} role="img" aria-label={`${region.id} 原版坐标俯视图`}>
    <rect width="1000" height={height} fill="#f8fafc" />
    {underlay ? <image href={image(underlay.file)} width="1000" height={height} preserveAspectRatio="none" opacity=".85" />
      : Array.from({ length: 11 }, (_, n) => <path key={n} d={`M${n*100},0V${height}M0,${n*height/10}H1000`} stroke="#dbe2ea" strokeWidth="1" />)}
    <text x="930" y="50" fontSize="28" fill="#334155">北 ↑</text>
    {comparison.markers.filter(m => filter === "all" || m.category === filter).map(m => {
      const p = originalPoint(region, m); if (!p) return null;
      const x = p[0] * 10, y = p[1] / 100 * height; const color = objectColor(m.category);
      return <g key={m.asset_id}>
        {m.category === "building" ? <rect x={x-24} y={y-24} width="48" height="48" rx="8" stroke={color} fill="white" fillOpacity={underlay ? 0.35 : 1} strokeWidth="3" /> : <circle cx={x} cy={y} r={m.category === "spawn" ? 14 : 7} stroke={color} fill="white" fillOpacity={underlay ? 0.35 : 1} strokeWidth="3" />}
        {labels && <text x={x} y={y+(m.category === "building" ? 44 : -14)} textAnchor="middle" fontSize="18" fontWeight="bold" fill={color} stroke="white" strokeWidth="4" paintOrder="stroke">{objectLabel(m.asset_id)}</text>}
      </g>;
    })}
    <text x="25" y={height - 25} fontSize="20" fill="#64748b" stroke="white" strokeWidth="4" paintOrder="stroke">{underlay ? underlay.note : "符号中心来自原版坐标；符号大小不代表物体尺寸"}</text>
  </svg>;
}
