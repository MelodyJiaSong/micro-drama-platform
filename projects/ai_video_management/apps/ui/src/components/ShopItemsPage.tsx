/** ShopItemsPage：一部剧的商店货单（follow-up 316）。
 *
 * 左边出售方（建筑商店、商人 NPC、Roshan 掉落），点开右边是它的物品格（缩略图、中英文名、价格、合成路线）；
 * 点物品看详情与「哪些出售方卖它」，点出售方跳过去。选中的出售方、物品记在 `?seller=` / `?item=`，链接可分享。
 * 搜索框跨全部出售方找物品。只读，数据来自 `GET /api/shop-items`（剧的 `2_世界观人设/props/shop_items.json`）。
 */
import { useCallback, useEffect, useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { mediaUrl } from "../api";
import { useFileChanges } from "../lib/fileEvents";
import { loadShopItems, matchesItem, type ShopItem, type ShopItems, type ShopSeller } from "../lib/shopItems";
import { ZoomableImage } from "./ZoomableImage";
import "./ShopItemsPage.css";

const fileLink = (path: string): string => `/file/${encodeURIComponent(path)}`;

function ItemTile({ item, selected, onSelect }: { item: ShopItem; selected: boolean; onSelect: () => void }): JSX.Element {
  return (
    <button type="button" className="shop-item-tile" aria-pressed={selected} onClick={onSelect} title={`${item.prop_key} ${item.name_zh} · ${item.name_en}`}>
      <span className="shop-item-media">
        {item.image ? <img src={mediaUrl(item.image)} alt="" loading="lazy" /> : <span className="shop-noimg">无图</span>}
      </span>
      <span className="shop-item-name"><span className="asset-key">{item.prop_key}</span>{item.name_zh}</span>
      <span className="shop-item-en">{item.name_en}</span>
      <span className="shop-item-price">💰 {item.price || "—"}</span>
      {item.recipe ? <span className="shop-item-recipe">合成：{item.recipe}</span> : null}
    </button>
  );
}

function ItemDetail({ item, sellers, current, onSeller, onClose }: {
  item: ShopItem; sellers: Map<string, ShopSeller>; current: string; onSeller: (key: string) => void; onClose: () => void;
}): JSX.Element {
  return (
    <aside className="shop-item-detail" aria-label={`${item.prop_key} ${item.name_zh}`}>
      <header>
        <h3><span className="asset-key">{item.prop_key}</span>{item.name_zh} <small>{item.name_en}</small></h3>
        <button type="button" onClick={onClose} aria-label="关闭物品详情">✕</button>
      </header>
      <div className="shop-item-detail-body">
        {item.image ? <ZoomableImage src={mediaUrl(item.image)} alt={`${item.prop_key} ${item.name_zh}`} /> : <span className="shop-noimg">无图</span>}
        <dl>
          <dt>类别</dt><dd>{item.category || "—"}</dd>
          <dt>价格</dt><dd>{item.price || "—"}</dd>
          <dt>合成路线</dt><dd>{item.recipe || "不需合成"}</dd>
        </dl>
        {item.card ? <Link to={fileLink(item.card)}>道具资产卡</Link> : <span className="shop-muted">道具卡未找到</span>}
      </div>
      <h4>哪些出售方卖它 · {item.sold_by.length}</h4>
      <ul className="shop-sold-by">
        {item.sold_by.map(key => {
          const s = sellers.get(key);
          return (
            <li key={key}>
              <button type="button" aria-current={key === current ? "true" : undefined} onClick={() => onSeller(key)}>
                <span className="asset-key">{key}</span>{s?.name_zh ?? key}<small>{s ? `${s.kind} · ${s.where}` : ""}</small>
              </button>
            </li>
          );
        })}
      </ul>
    </aside>
  );
}

export function ShopItemsPage(): JSX.Element {
  const [params, setParams] = useSearchParams();
  const drama = params.get("drama") ?? "";
  const [data, setData] = useState<ShopItems | null>(null);
  const [error, setError] = useState("");
  const [query, setQuery] = useState("");

  const load = useCallback(() => {
    if (!drama) return;
    loadShopItems(drama).then(d => { setData(d); setError(""); }, (err: unknown) => setError(err instanceof Error ? err.message : String(err)));
  }, [drama]);
  useEffect(() => { setData(null); load(); }, [load]);
  useFileChanges(data?.source ? data.source.slice(0, data.source.lastIndexOf("/")) : null, () => load());

  const sellers = useMemo(() => new Map((data?.sellers ?? []).map(s => [s.key, s])), [data]);
  const itemsByKey = useMemo(() => new Map((data?.items ?? []).map(i => [i.prop_key, i])), [data]);
  const seller = sellers.get(params.get("seller") ?? "") ?? data?.sellers[0];
  const item = itemsByKey.get(params.get("item") ?? "");
  const searching = query.trim() !== "";
  const shown = searching ? (data?.items ?? []).filter(i => matchesItem(i, query)) : seller?.items ?? [];

  const update = useCallback((changes: Record<string, string | null>) => {
    const next = new URLSearchParams(params);
    for (const [k, v] of Object.entries(changes)) { if (v) next.set(k, v); else next.delete(k); }
    setParams(next, { replace: true });
  }, [params, setParams]);

  const dramaName = drama.slice(drama.lastIndexOf("/") + 1);
  if (!drama) return <section className="shop-items"><p className="shop-muted">没有指定剧。请从资产总览或地图资产页点「🛒 商店货单」。</p></section>;
  if (error) return <section className="shop-items"><h1>商店货单</h1><p role="alert">读取失败：{error}</p><button type="button" onClick={load}>重新加载</button></section>;
  if (!data) return <section className="shop-items"><p role="status">加载商店货单…</p></section>;
  if (!data.source) return <section className="shop-items"><h1>商店货单 <span className="shop-muted">{dramaName}</span></h1><p className="shop-muted">本剧还没有商店货单（`2_世界观人设/props/shop_items.json`）。</p></section>;

  return (
    <section className="shop-items">
      <header className="shop-items-header">
        <div>
          <h1>商店货单 <span className="shop-muted">{dramaName}</span></h1>
          <p>{data.version ? `${data.version} · ` : ""}{data.sellers.length} 个出售方 · {data.items.length} 件物品
            {" · "}<Link to={fileLink(data.source)}>机读源</Link>{data.doc ? <>{" · "}<Link to={fileLink(data.doc)}>人读版</Link></> : null}</p>
          {data.note ? <p className="shop-muted">{data.note}</p> : null}
          {data.error ? <p role="alert">{data.error}</p> : null}
        </div>
        <input type="search" className="asset-overview-search" placeholder="跨全部出售方找物品：p157、净化药水、Clarity" value={query}
          onChange={e => setQuery(e.target.value)} aria-label="查找物品" />
      </header>
      <div className="shop-items-layout">
        <nav className="shop-sellers" aria-label="出售方">
          {data.sellers.map(s => (
            <button key={s.key} type="button" aria-current={!searching && s.key === seller?.key ? "page" : undefined}
              onClick={() => { setQuery(""); update({ seller: s.key }); }}>
              <span className="shop-seller-title"><span className="asset-key">{s.key}</span>{s.name_zh}<span className="shop-count">{s.count} 件</span></span>
              <small>{s.kind}</small>
              <small>{s.where}</small>
            </button>
          ))}
        </nav>
        <main className="shop-items-main">
          {searching ? <h2>查找「{query.trim()}」 · {shown.length} 件</h2> : seller ? (
            <header className="shop-seller-header">
              {seller.image ? <img src={mediaUrl(seller.image)} alt={`${seller.key} ${seller.name_zh}`} /> : null}
              <div>
                <h2><span className="asset-key">{seller.key}</span>{seller.name_zh} <small>{seller.name_en}</small></h2>
                <p>{seller.kind} · {seller.where} · {seller.items.length} 件{seller.count !== seller.items.length ? `（清单写 ${seller.count}）` : ""}</p>
                {seller.card ? <Link to={fileLink(seller.card)}>出售方资产卡</Link> : null}
              </div>
            </header>
          ) : null}
          <div className={item ? "shop-items-body with-detail" : "shop-items-body"}>
            <div className="shop-item-grid" role="list" aria-label="物品">
              {shown.map(i => (
                <div role="listitem" key={i.prop_key}>
                  <ItemTile item={i} selected={i.prop_key === item?.prop_key} onSelect={() => update({ item: i.prop_key })} />
                </div>
              ))}
              {!shown.length ? <p className="shop-muted">{searching ? "没有匹配的物品" : "这个出售方没有物品"}</p> : null}
            </div>
            {item ? <ItemDetail item={item} sellers={sellers} current={searching ? "" : seller?.key ?? ""}
              onSeller={key => { setQuery(""); update({ seller: key }); }} onClose={() => update({ item: null })} /> : null}
          </div>
        </main>
      </div>
    </section>
  );
}
