import { ApiError } from "../types";

/** 商店货单（follow-up 316）：后端 `GET /api/shop-items`，数据源剧的 `2_世界观人设/props/shop_items.json`。 */
export const SHOP_ITEMS_ROUTE = "/shop-items";

export interface ShopItem {
  prop_key: string; name_zh: string; name_en: string; category: string;
  /** 原文，如 `50`、`250 / 875`（卷轴 / 总价）。 */
  price: string;
  /** 合成路线原文；基础件为空串。 */
  recipe: string;
  /** 仓库相对路径；文件不在为空串。 */
  card: string; image: string;
  /** 卖它的出售方键，按货单顺序。 */
  sold_by: string[];
}
export interface ShopSeller {
  key: string; name_zh: string; name_en: string; kind: string; where: string;
  folder: string; card: string; image: string; count: number; items: ShopItem[];
}
export interface ShopItems {
  drama: string;
  /** 剧没有货单为空串。 */
  source: string;
  doc: string; version: string; note: string;
  sellers: ShopSeller[];
  /** 去重后的全部物品。 */
  items: ShopItem[];
  error: string;
}

export function shopItemsUrl(drama: string, params: Record<string, string> = {}): string {
  return `${SHOP_ITEMS_ROUTE}?${new URLSearchParams({ drama, ...params })}`;
}

export async function loadShopItems(drama: string): Promise<ShopItems> {
  const response = await fetch(`/api/shop-items?drama=${encodeURIComponent(drama)}`, { cache: "no-store" });
  const data = await response.json();
  if (!response.ok) throw new ApiError(response.status, data.detail?.message || data.detail?.kind || `HTTP ${response.status}`, data.detail);
  return data as ShopItems;
}

/** 剧内阶段目录下的文件（`ai_videos/剧/0_research/…`）→ 剧根：取第一个 `数字_` 段之前的部分。 */
export function dramaOfStagePath(path: string): string {
  const parts = path.split("/");
  const stage = parts.findIndex((part, i) => i >= 2 && /^\d+_/.test(part));
  return stage > 0 ? parts.slice(0, stage).join("/") : "";
}

/** 按键、中英文名、类别过滤（不分大小写）；空关键词原样返回。 */
export function matchesItem(item: ShopItem, query: string): boolean {
  const q = query.trim().toLowerCase();
  if (!q) return true;
  return [item.prop_key, item.name_zh, item.name_en, item.category].some(text => text.toLowerCase().includes(q));
}

