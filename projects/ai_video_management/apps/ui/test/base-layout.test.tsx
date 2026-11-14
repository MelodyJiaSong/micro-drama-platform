import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, expect, it, vi } from "vitest";
import { BaseLayoutPage } from "../src/components/BaseLayoutPage";
import { fetchFile } from "../src/api";
import { layoutFile, loadBaseLayout } from "../src/lib/baseLayout";

vi.mock("../src/api", async original => ({ ...await original<typeof import("../src/api")>(), fetchFile: vi.fn() }));
vi.mock("../src/lib/fileEvents", () => ({ useFileChanges: vi.fn() }));
afterEach(() => { cleanup(); vi.clearAllMocks(); });
const path = "ai_videos/dota/0_research/layout/manifest.json";
const charts = { asset: "asset.png", number: "number.png", shops: "shops.png" };
const data = { title: "两方基地", version: "6.83d", references_file: "refs.json", limitations: [],
  charts: { sentinel: charts, scourge: { ...charts, asset: "scourge.png" } },
  assets: { bg37: { name: "天灾四级蛛魔塔", card: "../../background/bg37.md", anchor: "tower.png", views: "views.png", status: "待确认" } },
  rows: [
    { faction: "sentinel", category: "building", point_number: 1, instance_id: "bg2#01", asset_id: null, name: "树", x: -10, y: -20, facing: 270 },
    ...[1, 2].map(n => ({ faction: "scourge", category: "building", point_number: n, instance_id: `bg37#0${n}`, asset_id: "bg37", name: "蛛魔塔", x: n * 10, y: 20, facing: 270 })),
  ] };
function mockFiles() {
  vi.mocked(fetchFile).mockImplementation(async p => ({ content: JSON.stringify(p === path ? data : { references: [] }) } as Awaited<ReturnType<typeof fetchFile>>));
}

it("switches bases and chart modes, filters instances and opens the matching asset", async () => {
  mockFiles();
  render(<MemoryRouter initialEntries={[`/base-layout?path=${encodeURIComponent(path)}`]}><BaseLayoutPage /></MemoryRouter>);
  await screen.findByRole("heading", { name: "两方基地" });
  expect(screen.getByText(/1 座建筑待补图/)).toBeTruthy();
  fireEvent.click(screen.getByRole("button", { name: "天灾基地" }));
  expect(screen.getByText(/2 座建筑 · 1 类建筑素材/)).toBeTruthy();
  expect(screen.getByAltText("天灾基地资产编号坐标图").getAttribute("src")).toContain("scourge.png");
  fireEvent.click(screen.getByRole("button", { name: "数字位置编号" }));
  expect(screen.getByAltText("天灾基地数字位置坐标图").getAttribute("src")).toContain("number.png");
  fireEvent.change(screen.getByRole("textbox"), { target: { value: "bg37#02" } });
  expect(screen.queryByText("bg37#01")).toBeNull();
  fireEvent.click(screen.getByRole("button", { name: "查看 bg37" }));
  const preview = screen.getByRole("complementary", { name: "选中素材" });
  expect(within(preview).getByRole("link").getAttribute("href")).toContain(encodeURIComponent("ai_videos/dota/background/bg37.md"));
  expect(within(preview).getByRole("img").getAttribute("src")).toContain("views.png");
});

it("shows a recoverable load error", async () => {
  vi.mocked(fetchFile).mockRejectedValueOnce(new Error("资料暂不可用"));
  render(<MemoryRouter initialEntries={[`/base-layout?path=${encodeURIComponent(path)}`]}><BaseLayoutPage /></MemoryRouter>);
  expect((await screen.findByRole("alert")).textContent).toBe("资料暂不可用");
  mockFiles(); fireEvent.click(screen.getByRole("button", { name: "重新加载" }));
  await screen.findByRole("heading", { name: "两方基地" });
});

it("loads native assembly plans and downloads the selected base's Blender file", async () => {
  vi.mocked(fetchFile).mockImplementation(async p => ({ content: JSON.stringify(p === path
    ? { ...data, assembly_file: "assembly.json" }
    : p.endsWith("assembly.json") ? { scourge: { asset_id: "bg39", card: "base.md", floorplan: "floorplan.png", placements: "placements.json", blocks: "blocks.toml", overview: null, note: "尺寸待校准", blend: "bg39.blend", checks: ["check.png"], terrain: "terrain.png" } }
    : { references: [] }) } as Awaited<ReturnType<typeof fetchFile>>));
  render(<MemoryRouter initialEntries={[`/base-layout?path=${encodeURIComponent(path)}&faction=scourge`]}><BaseLayoutPage /></MemoryRouter>);
  await screen.findByRole("heading", { name: "两方基地" });
  fireEvent.click(screen.getByText(/搭景方案 · bg39/));
  expect(screen.getByAltText("天灾基地米制搭景候选").getAttribute("src")).toContain("floorplan.png");
  expect(screen.getByRole("link", { name: "下载 Blender 场景" }).getAttribute("href")).toContain("bg39.blend");
  expect(screen.getByRole("link", { name: "逐实例摆放表" }).getAttribute("href")).toContain("placements.json");
  expect(screen.getByAltText("天灾基地原版地形高程调查").getAttribute("src")).toContain("terrain.png");
  fireEvent.click(screen.getByRole("button", { name: "近卫基地" }));
  expect(screen.queryByRole("link", { name: "下载 Blender 场景" })).toBeNull();
});

it("rejects external references and malformed coordinates", async () => {
  expect(() => layoutFile(path, "https://example.com/a.png")).toThrow();
  expect(() => layoutFile(path, "../../../../../secret.txt")).toThrow();
  vi.mocked(fetchFile).mockResolvedValue({ content: JSON.stringify({ ...data, rows: [{ ...data.rows[0], x: "oops" }] }) } as Awaited<ReturnType<typeof fetchFile>>);
  await expect(loadBaseLayout(path)).rejects.toThrow("基地布局资料不完整");
});
