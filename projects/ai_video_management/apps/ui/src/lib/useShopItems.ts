import { useEffect, useState } from "react";
import { loadShopItems, type ShopItems } from "./shopItems";

/** 入口链接用：取一次货单，读不到或剧没有货单都给 null（不打扰所在页面）。 */
export function useShopItems(drama: string): ShopItems | null {
  const [data, setData] = useState<ShopItems | null>(null);
  useEffect(() => {
    setData(null);
    if (!drama) return undefined;
    let cancelled = false;
    loadShopItems(drama).then(d => { if (!cancelled) setData(d?.source ? d : null); }, () => undefined);
    return () => { cancelled = true; };
  }, [drama]);
  return data;
}
