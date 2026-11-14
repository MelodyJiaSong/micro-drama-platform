import { ApiError } from "../types";

/** 资产总览（follow-up 293）：后端 `GET /api/asset-overview`。 */
export interface AssetTile {
  key: string; folder: string; path: string; card: string;
  /** 卡标题 ` · ` 前的第一段；没有卡为目录名。 */
  name: string;
  title: string;
  portrait: string;
  /** 封面在前。 */
  images: string[];
  /** 新的在前。 */
  videos: string[];
  /** 卡开头的 `> ` 行（键、状态）。 */
  meta: string[];
}
export interface AssetGroup { name: string; tiles: AssetTile[] }
export type AssetKind = "characters" | "background" | "props";
export interface AssetSection { kind: AssetKind; label: string; count: number; groups: AssetGroup[] }
export interface AssetOverview { drama: string; sections: AssetSection[]; watch: string[] }

export async function loadAssetOverview(drama: string): Promise<AssetOverview> {
  const response = await fetch(`/api/asset-overview?drama=${encodeURIComponent(drama)}`, { cache: "no-store" });
  const data = await response.json();
  if (!response.ok) throw new ApiError(response.status, data.detail?.message || data.detail?.kind || `HTTP ${response.status}`, data.detail);
  return data as AssetOverview;
}

/** 按键、名字、目录名、卡标题过滤（不分大小写）；空关键词原样返回。 */
export function matchesQuery(tile: AssetTile, query: string): boolean {
  const q = query.trim().toLowerCase();
  if (!q) return true;
  return [tile.key, tile.name, tile.folder, tile.title].some(text => text.toLowerCase().includes(q));
}

/** 过滤后的节：空组去掉，节保留（显示 0）。 */
export function filterSections(sections: AssetSection[], query: string): AssetSection[] {
  return sections.map(section => {
    const groups = section.groups
      .map(group => ({ ...group, tiles: group.tiles.filter(tile => matchesQuery(tile, query)) }))
      .filter(group => group.tiles.length > 0);
    return { ...section, groups, count: groups.reduce((n, g) => n + g.tiles.length, 0) };
  });
}
