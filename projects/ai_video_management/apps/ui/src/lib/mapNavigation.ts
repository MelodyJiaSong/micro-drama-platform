import { fetchFile } from "../api";
import { layoutFile } from "./baseLayout";

export interface NavigationRegion {
  bounds: [number, number, number, number]; tree_count: number;
  layer_percentages: Record<string, number>; percentages: Record<string, number>;
  ground_vertex_z_range: [number, number]; constraints: string;
  candidate?: { file: string; prompt: string; sha256: string; status: string; review: string;
    reference_layout?: { file: string; sha256: string; navigation_revision: string; grid_sha256: string } };
}
export interface MapNavigation {
  schema: number; title: string; revision: string; status: string;
  source_map: string; reconstruction: string; grid: string; report: string;
  layers: { id: string; label: string; note: string; color: string; file: string }[];
  regions: Record<string, NavigationRegion>; limitations: string[];
}
export interface NavigationGrid { width: number; height: number; cell_game_units: number; bits: string[]; cells: Uint8Array; heights: Uint8Array }
export interface NavigationPoint { x: number; y: number }

export async function loadNavigation(path: string, relative: string): Promise<{ data: MapNavigation; grid: NavigationGrid }> {
  const data = JSON.parse((await fetchFile(layoutFile(path, relative))).content) as MapNavigation;
  if (data.schema !== 1 || !Array.isArray(data.layers) || !data.regions || !Array.isArray(data.limitations)) throw new Error("通行研究清单无效。");
  [data.source_map, data.reconstruction, data.grid, data.report, ...data.layers.map(l => l.file), ...Object.values(data.regions).flatMap(r => [r.constraints, ...(r.candidate ? [r.candidate.file, r.candidate.prompt, ...(r.candidate.reference_layout ? [r.candidate.reference_layout.file] : [])] : [])])].forEach(p => layoutFile(path, p));
  const raw = JSON.parse((await fetchFile(layoutFile(path, data.grid))).content);
  const decode = (s: string) => Uint8Array.from(atob(s), c => c.charCodeAt(0));
  const cells = decode(raw.cells_base64), heights = decode(raw.height_layers_base64);
  if (raw.width !== 512 || raw.height !== 512 || raw.cell_game_units !== 32 || raw.origin !== "northwest" || cells.length !== raw.width * raw.height || heights.length !== cells.length || JSON.stringify(raw.bits) !== JSON.stringify(["walk", "blocked", "trees", "cliffs", "ramps", "uncertain"])) throw new Error("通行网格尺寸或图层定义不匹配。");
  return { data, grid: { width: raw.width, height: raw.height, cell_game_units: raw.cell_game_units, bits: raw.bits, cells, heights } };
}

export function inspectNavigation(grid: NavigationGrid, p: NavigationPoint): { flags: string[]; layer: number; world: [number, number] } | null {
  const x = Math.floor(p.x), y = Math.floor(p.y);
  if (x < 0 || y < 0 || x >= grid.width || y >= grid.height) return null;
  const index = y * grid.width + x;
  return { flags: grid.bits.filter((_, bit) => grid.cells[index] & (1 << bit)), layer: grid.heights[index], world: [-8192 + (x + .5) * 32, 8192 - (y + .5) * 32] };
}

/** Conservative swept square, including both endpoints. This is not pathfinding. */
export function inspectSegment(grid: NavigationGrid, a: NavigationPoint, b: NavigationPoint): string[] {
  const hits = new Set<string>();
  const steps = Math.max(1, Math.ceil(Math.hypot(b.x-a.x, b.y-a.y)*4));
  for (let step=0; step<=steps; step++) {
    const x=a.x+(b.x-a.x)*step/steps, y=a.y+(b.y-a.y)*step/steps;
    // 32 game units of clearance, conservative square; not a specific hero radius.
    for (let j=Math.floor(y-1); j<=Math.floor(y+1); j++) for (let i=Math.floor(x-1); i<=Math.floor(x+1); i++) {
      const cell=inspectNavigation(grid,{x:i,y:j});
      if (!cell) hits.add("outside");
      else cell.flags.filter(f=>["blocked","trees","cliffs","uncertain"].includes(f)).forEach(f=>hits.add(f));
    }
  }
  return [...hits];
}
