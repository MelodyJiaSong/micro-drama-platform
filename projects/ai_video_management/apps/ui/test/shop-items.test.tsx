import { act, cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { MemoryRouter, Route, Routes, useLocation } from "react-router-dom";
import { afterEach, expect, it, vi } from "vitest";
import { ShopItemsPage } from "../src/components/ShopItemsPage";
import { MapRegionsPage } from "../src/components/MapRegionsPage";
import { fetchFile } from "../src/api";
import type { RegionMap } from "../src/lib/mapRegions";
import { dramaOfStagePath, loadShopItems, matchesItem, type ShopItem, type ShopItems } from "../src/lib/shopItems";

vi.mock("../src/lib/shopItems", async importOriginal => ({ ...await importOriginal<typeof import("../src/lib/shopItems")>(), loadShopItems: vi.fn() }));
vi.mock("../src/lib/fileEvents", () => ({ useFileChanges: vi.fn() }));
vi.mock("../src/api", async original => ({ ...await original<typeof import("../src/api")>(), fetchFile: vi.fn() }));
afterEach(() => { cleanup(); vi.clearAllMocks(); });

const W = "ai_videos/dota/2_世界观人设";
function item(key: string, zh: string, en: string, sold_by: string[], extra: Partial<ShopItem> = {}): ShopItem {
  const dir = `${W}/props/中立_neutral/${key}_${en.replace(/ /g, "_")}`;
  return { prop_key: key, name_zh: zh, name_en: en, category: "消耗品", price: "50", recipe: "", card: `${dir}/x.md`, image: `${dir}/x.png`, sold_by, ...extra };
}
const CLARITY = item("p157", "净化药水", "Clarity Potion", ["bg22", "m302"]);
const URN = item("p187", "影之灵龛", "Urn of Shadows", ["m302"], { category: "合成成品", price: "250 / 875", recipe: "艺人面罩 + 2 力量手套 + 卷轴", image: "" });
const DATA: ShopItems = {
  drama: "ai_videos/dota", source: `${W}/props/shop_items.json`, doc: `${W}/props/shop_items.md`, version: "6.83d", note: "两边货单相同。", error: "",
  sellers: [
    { key: "bg22", name_zh: "奇迹古树", name_en: "Ancient of Wonders", kind: "建筑（消耗品商店）", where: "近卫泉水区 bg13", folder: "", card: "", image: "", count: 1, items: [CLARITY] },
    { key: "m302", name_zh: "支援法衣", name_en: "Supportive Vestments", kind: "人形商人（合成）", where: "近卫泉水区", folder: "", card: "c.md", image: "", count: 2, items: [URN, CLARITY] },
  ],
  items: [CLARITY, URN],
};

function Where(): JSX.Element {
  return <output data-testid="where">{useLocation().search}</output>;
}

async function mount(search = "", data: ShopItems = DATA): Promise<void> {
  vi.mocked(loadShopItems).mockResolvedValue(data);
  render(
    <MemoryRouter initialEntries={[`/shop-items?drama=ai_videos%2Fdota${search}`]}>
      <Routes><Route path="/shop-items" element={<><ShopItemsPage /><Where /></>} /></Routes>
    </MemoryRouter>,
  );
  await act(async () => { await Promise.resolve(); });
}

it("lists sellers with key, name, kind, place and count; first seller's items by default", async () => {
  await mount();
  expect(loadShopItems).toHaveBeenCalledWith("ai_videos/dota");
  const nav = screen.getByRole("navigation", { name: "出售方" });
  const buttons = within(nav).getAllByRole("button");
  expect(buttons.map(b => b.textContent)).toEqual([
    "bg22奇迹古树1 件建筑（消耗品商店）近卫泉水区 bg13",
    "m302支援法衣2 件人形商人（合成）近卫泉水区",
  ]);
  expect(buttons[0].getAttribute("aria-current")).toBe("page");
  const grid = screen.getByRole("list", { name: "物品" });
  expect(within(grid).getAllByRole("listitem")).toHaveLength(1);
  expect(within(grid).getByText("Clarity Potion")).toBeTruthy();
  expect(screen.getByText("2 个出售方 · 2 件物品", { exact: false })).toBeTruthy();
});

it("clicking a seller shows its grid with price and recipe; clicking an item shows who sells it", async () => {
  await mount();
  fireEvent.click(within(screen.getByRole("navigation", { name: "出售方" })).getByRole("button", { name: /^m302/ }));
  expect(screen.getByTestId("where").textContent).toContain("seller=m302");
  const grid = screen.getByRole("list", { name: "物品" });
  expect(within(grid).getAllByRole("listitem")).toHaveLength(2);
  expect(within(grid).getByText("合成：艺人面罩 + 2 力量手套 + 卷轴")).toBeTruthy();
  expect(within(grid).getByText("💰 250 / 875")).toBeTruthy();
  expect(within(grid).getByText("无图")).toBeTruthy();

  fireEvent.click(within(grid).getByTitle("p157 净化药水 · Clarity Potion"));
  const detail = screen.getByRole("complementary", { name: "p157 净化药水" });
  expect(within(detail).getByText("哪些出售方卖它 · 2")).toBeTruthy();
  const sellers = within(detail).getAllByRole("button", { name: /^(bg22|m302)/ });
  expect(sellers.map(b => b.textContent?.slice(0, 4))).toEqual(["bg22", "m302"]);
  expect(sellers[1].getAttribute("aria-current")).toBe("true");
  fireEvent.click(sellers[0]);
  expect(screen.getByTestId("where").textContent).toMatch(/seller=bg22.*item=p157|item=p157.*seller=bg22/);
  expect(screen.getByRole("heading", { level: 2 }).textContent).toContain("奇迹古树");
  fireEvent.click(within(screen.getByRole("complementary")).getByRole("button", { name: "关闭物品详情" }));
  expect(screen.queryByRole("complementary")).toBeNull();
});

it("opens straight from ?seller=&item= and searches across all sellers", async () => {
  await mount("&seller=m302&item=p187");
  expect(screen.getByRole("complementary", { name: "p187 影之灵龛" })).toBeTruthy();
  fireEvent.change(screen.getByRole("searchbox", { name: "查找物品" }), { target: { value: "clarity" } });
  expect(screen.getByRole("heading", { name: "查找「clarity」 · 1 件" })).toBeTruthy();
  expect(within(screen.getByRole("list", { name: "物品" })).getAllByRole("listitem")).toHaveLength(1);
});

it("says so when the drama has no shop list", async () => {
  await mount("", { ...DATA, source: "", doc: "", sellers: [], items: [] });
  expect(screen.getByText(/本剧还没有商店货单/)).toBeTruthy();
});

it("helpers: drama root from a stage path, item matching", () => {
  expect(dramaOfStagePath("ai_videos/dota_yingxiong/0_research/map_regions/map_regions.json")).toBe("ai_videos/dota_yingxiong");
  expect(dramaOfStagePath("ai_videos/xianxia/xianjian_yi/0_research/m.json")).toBe("ai_videos/xianxia/xianjian_yi");
  expect(dramaOfStagePath("ai_videos/dota/map.json")).toBe("");
  expect(matchesItem(CLARITY, "P157")).toBe(true);
  expect(matchesItem(CLARITY, "净化")).toBe(true);
  expect(matchesItem(URN, "clarity")).toBe(false);
});

it("map asset page links to the shop list and to each seller's goods", async () => {
  const path = "ai_videos/dota/0_research/map/manifest.json";
  const map: RegionMap = { schema: 1, title: "地图区域", version: "6.83d", overview: "map.png", source_map: "source.png", base_layout: "base.json", notes: [],
    groups: [{ id: "S", name: "近卫基地", color: "green" }],
    regions: [{ id: "S1", parent: "S", name: "泉水与商店", asset_id: "bg13", position: [10, 90], card: "S.md", note: "", instance_refs: [], instances: [],
      assets: [{ id: "bg22", name: "奇迹古树", card: "a.md", image: null }, { id: "bg25", name: "泉水", card: "b.md", image: null }],
      views: [{ id: "overhead", label: "俯视", file: null, target: "o.png", status: "planned", review: "", prompt: "o.txt" }] }] };
  vi.mocked(fetchFile).mockImplementation(async p => ({ content: JSON.stringify(p === path ? map : { rows: [] }) } as Awaited<ReturnType<typeof fetchFile>>));
  vi.mocked(loadShopItems).mockResolvedValue(DATA);
  render(<MemoryRouter initialEntries={[`/map-regions?path=${encodeURIComponent(path)}`]}><MapRegionsPage /></MemoryRouter>);
  await screen.findByRole("heading", { name: "地图区域" });
  await act(async () => { await Promise.resolve(); });
  expect(loadShopItems).toHaveBeenCalledWith("ai_videos/dota");
  expect(screen.getByRole("link", { name: "🛒 商店货单 · 2 个出售方" }).getAttribute("href")).toBe("/shop-items?drama=ai_videos%2Fdota");
  const goods = screen.getAllByRole("link", { name: "🛒 货单" });
  expect(goods).toHaveLength(1);
  expect(goods[0].getAttribute("href")).toBe("/shop-items?drama=ai_videos%2Fdota&seller=bg22");
});
