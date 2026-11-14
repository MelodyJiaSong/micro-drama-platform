import { fetchFile } from "../api";
import { layoutFile, type BasePosition } from "./baseLayout";

export const MAP_REGIONS_ROUTE = "/map-regions";
export interface RegionView { id: string; label: string; file: string | null; target: string; status: string; review: string; prompt: string; sha256?: string; reference_overhead?: { file: string; sha256: string }; layout_render?: { file: string; sha256: string }; layout_review?: { overhead_sha256: string; view_sha256: string; note: string } }
export interface BuildingComparison {
  reference: string; source_record: string; reference_label: string; note: string;
  generated_size: [number, number]; reference_size: [number, number];
  layout_bounds?: [number, number, number, number];
  layout_underlay?: { file: string; note: string };
  capacity?: { overhead_sha256: string; area: [number, number][]; heroes: [number, number, number, number][]; note: string };
  markers: { asset_id: string; instance_id?: string; category?: string; generated: [number, number, number, number]; reference: [number, number, number, number] | null; reference_note?: string }[];
}
export interface MapRegion {
  id: string; parent: string; name: string; asset_id: string; position: [number, number]; card: string; note: string; floorplan?: string; blocks?: string;
  assets: { id: string; name: string; card: string; image: string | null }[];
  instance_refs: string[]; instances: BasePosition[]; views: RegionView[]; building_comparison?: BuildingComparison;
  base_connection?: { region: string; landmark: string; plan: string; note: string };
  original_reference?: { file: string; kind: "gameplay" | "map"; label: string; note: string; source_record: string; map_bounds: [number, number, number, number] };
}
export interface RegionMap {
  schema: number; navigation?: string; title: string; version: string; overview: string; source_map: string; base_layout: string;
  groups: { id: string; name: string; color: string }[]; regions: MapRegion[]; notes: string[];
}
export function parseRegionMap(content: string, path: string): RegionMap {
  const m = JSON.parse(content) as RegionMap;
  if (m.schema !== 1 || !Array.isArray(m.groups) || !Array.isArray(m.regions) || !Array.isArray(m.notes)
    || typeof m.title !== "string" || !m.overview || !m.base_layout || !m.source_map
    || m.notes.some(n => typeof n !== "string")
    || m.groups.some(g => typeof g.id !== "string" || typeof g.name !== "string" || typeof g.color !== "string")) throw new Error("地图区域清单不完整。");
  const groups = new Set(m.groups.map(g => g.id));
  const ids = new Set(m.regions.map(r => r.id));
  if (groups.size !== m.groups.length || ids.size !== m.regions.length) throw new Error("地图区域编号重复。");
  const files = [m.overview, m.source_map, m.base_layout];
  if (m.navigation) files.push(m.navigation);
  for (const r of m.regions) {
    if (!r.id || typeof r.name !== "string" || !r.asset_id || typeof r.note !== "string" || !groups.has(r.parent) || !Array.isArray(r.position) || r.position.length !== 2
      || !r.position.every(n => Number.isFinite(n) && n >= 0 && n <= 100)
      || !Array.isArray(r.views) || !Array.isArray(r.assets) || !Array.isArray(r.instance_refs)
      || r.instance_refs.some(id => typeof id !== "string")
      || new Set(r.views.map(v => v.id)).size !== r.views.length) throw new Error("区域层级或机位资料无效。");
    files.push(r.card);
    r.instances = [];
    if (r.floorplan) files.push(r.floorplan);
    if (r.blocks) files.push(r.blocks);
    if (r.original_reference) {
      const ref = r.original_reference;
      if (!["gameplay", "map"].includes(ref.kind) || typeof ref.label !== "string" || typeof ref.note !== "string"
        || !Array.isArray(ref.map_bounds) || ref.map_bounds.length !== 4 || ref.map_bounds.some(n => !Number.isFinite(n) || n < 0 || n > 100)
        || ref.map_bounds[0] >= ref.map_bounds[2] || ref.map_bounds[1] >= ref.map_bounds[3]) throw new Error("区域原图资料无效。");
      files.push(ref.file, ref.source_record);
    }
    if (r.base_connection) {
      const c = r.base_connection;
      if (!ids.has(c.region) || c.region === r.id || typeof c.landmark !== "string" || typeof c.note !== "string") throw new Error("基地连接资料无效。");
      files.push(c.plan);
    }
    if (r.building_comparison) {
      const c = r.building_comparison;
      files.push(c.reference, c.source_record);
      if (typeof c.reference_label !== "string" || typeof c.note !== "string"
        || ![c.generated_size, c.reference_size].every(size => Array.isArray(size) && size.length === 2 && size.every(n => Number.isFinite(n) && n > 0))
        || !Array.isArray(c.markers) || !c.markers.length || new Set(c.markers.map(m => m.asset_id)).size !== c.markers.length
        || c.markers.some(m => (!r.assets.some(a => a.id === m.asset_id) && !r.instance_refs.some(ref => ref.endsWith(`:${m.asset_id}`))) || ![m.generated, ...(m.reference ? [m.reference] : [])].every(p => Array.isArray(p) && p.length === 4 && p.every(n => Number.isFinite(n) && n >= 0 && n <= 100)))
        || !r.views.some(v => v.id === "overhead" && v.file)) throw new Error("建筑对照标注资料无效。");
      if (c.capacity) {
        const k = c.capacity;
        if (!/^[a-f0-9]{64}$/.test(k.overhead_sha256) || typeof k.note !== "string" || !Array.isArray(k.area) || k.area.length < 3 || !Array.isArray(k.heroes) || k.heroes.length !== 5
          || k.area.some(p => !Array.isArray(p) || p.length !== 2 || p.some(n => !Number.isFinite(n) || n < 0 || n > 100))
          || k.heroes.some(p => !Array.isArray(p) || p.length !== 4 || p.some(n => !Number.isFinite(n) || n < 0 || n > 100) || p[2] <= 0 || p[3] <= 0)) throw new Error("英雄活动空间标注无效。");
      }
      if (c.layout_bounds && (!Array.isArray(c.layout_bounds) || c.layout_bounds.length !== 4 || !c.layout_bounds.every(Number.isFinite) || c.layout_bounds[0] >= c.layout_bounds[2] || c.layout_bounds[1] >= c.layout_bounds[3])) throw new Error("原版布局范围无效。");
      if (c.layout_underlay) {
        if (!c.layout_bounds || typeof c.layout_underlay.file !== "string" || typeof c.layout_underlay.note !== "string") throw new Error("原版布局底图无效。");
        files.push(c.layout_underlay.file);
      }
    }
    for (const v of r.views) {
      if (!v.id || typeof v.label !== "string" || !v.status || typeof v.review !== "string" || (v.file !== null && typeof v.file !== "string")) throw new Error("区域机位资料无效。");
      files.push(v.prompt, v.target); if (v.file) files.push(v.file);
      if (v.layout_review && (!/^[a-f0-9]{64}$/.test(v.layout_review.overhead_sha256) || !/^[a-f0-9]{64}$/.test(v.layout_review.view_sha256) || typeof v.layout_review.note !== "string")) throw new Error("机位布局复核记录无效。");
      if (v.layout_render) {
        files.push(v.layout_render.file);
        if (!/^[a-f0-9]{64}$/.test(v.layout_render.sha256)) throw new Error("机位布局渲染指纹无效。");
      }
      if (v.reference_overhead) {
        files.push(v.reference_overhead.file);
        if (!/^[a-f0-9]{64}$/.test(v.reference_overhead.sha256)) throw new Error("机位参考俯视图指纹无效。");
      }
    }
    for (const a of r.assets) {
      if (!a.id || typeof a.name !== "string") throw new Error("区域资产资料无效。");
      files.push(a.card); if (a.image) files.push(a.image);
    }
  }
  for (const file of files) { if (typeof file !== "string" || !file) throw new Error("地图资料路径缺失。"); layoutFile(path, file); }
  return m;
}
export async function loadRegionMap(path: string): Promise<RegionMap> {
  const m = parseRegionMap((await fetchFile(path)).content, path);
  const source = JSON.parse((await fetchFile(layoutFile(path, m.base_layout))).content) as { rows: BasePosition[] };
  if (!Array.isArray(source.rows)) throw new Error("原版实例坐标资料不可读。");
  const positions = new Map(source.rows.map(row => [`${row.faction}:${row.instance_id}`, row]));
  const assigned = new Set<string>();
  for (const r of m.regions) r.instances = r.instance_refs.map(id => {
    const row = positions.get(id);
    if (!row || assigned.has(id)) throw new Error(`区域实例引用缺失或重复：${id}`);
    assigned.add(id); return row;
  });
  return m;
}
