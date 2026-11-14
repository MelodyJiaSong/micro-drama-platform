import { fetchFile } from "../api";
import { resolveLink } from "./linkResolver";

export const BASE_LAYOUT_ROUTE = "/base-layout";
export type BaseFaction = "sentinel" | "scourge";
export type BaseChartMode = "asset" | "number" | "shops";
export interface BasePosition {
  faction: BaseFaction; category: "building" | "merchant" | "spawn"; point_number: number;
  instance_id: string; asset_id: string | null; name: string; x: number; y: number; facing: number;
}
export interface BaseAsset { name: string; card: string; anchor: string | null; views: string | null; status: string }
export interface BaseReference { file: string; caption: string; status: string; source_url?: string; source_record?: string }
export interface BaseAssembly { asset_id: string; card: string; floorplan: string; placements: string; blocks: string; overview: string | null; note: string; blend?: string; checks?: string[]; terrain?: string }
export interface BaseLayout {
  title: string; version: string; rows: BasePosition[]; assets: Record<string, BaseAsset>;
  charts: Record<BaseFaction, Record<BaseChartMode, string>>; references_file: string; limitations: string[];
  assembly_file?: string;
  map_regions?: string;
}

export function layoutFile(manifest: string, relative: string): string {
  const result = resolveLink({ currentFile: manifest, href: relative, isKnown: p => p.startsWith("ai_videos/") });
  if (result.kind !== "internal") throw new Error("布局资料路径不在资产库内。");
  return result.path;
}

export async function loadBaseLayout(path: string): Promise<{ layout: BaseLayout; references: BaseReference[]; assembly?: Partial<Record<BaseFaction, BaseAssembly>> }> {
  const file = await fetchFile(path);
  const layout = JSON.parse(file.content) as BaseLayout;
  if (!Array.isArray(layout.rows) || !layout.assets || !layout.charts?.sentinel || !layout.charts?.scourge
    || !Array.isArray(layout.limitations) || !layout.references_file
    || layout.rows.some(r => !r.instance_id || !r.name || !["sentinel", "scourge"].includes(r.faction)
      || ![r.x, r.y, r.facing, r.point_number].every(Number.isFinite))) {
    throw new Error("基地布局资料不完整，请检查坐标清单。");
  }
  const refs = JSON.parse((await fetchFile(layoutFile(path, layout.references_file))).content) as { references: BaseReference[] };
  if (!Array.isArray(refs.references)) throw new Error("游戏参考清单不完整。");
  const assembly = layout.assembly_file
    ? JSON.parse((await fetchFile(layoutFile(path, layout.assembly_file))).content) as Partial<Record<BaseFaction, BaseAssembly>> : undefined;
  return { layout, references: refs.references, assembly };
}
