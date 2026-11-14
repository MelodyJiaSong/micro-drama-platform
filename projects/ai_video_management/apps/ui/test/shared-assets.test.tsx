import { act, cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, expect, it, vi } from "vitest";
import { AssetOverviewPage } from "../src/components/AssetOverviewPage";
import { loadSharedLibrary, type SharedAsset } from "../src/lib/sharedAssets";
import { matchesNavigation } from "../src/lib/globalWorkflow";

vi.mock("../src/lib/sharedAssets", async original => ({ ...await original<typeof import("../src/lib/sharedAssets")>(), loadSharedLibrary: vi.fn() }));
afterEach(() => { cleanup(); vi.clearAllMocks(); });
const asset = (id: string, status: string, hasImage: boolean): SharedAsset => ({
  id, name: id === "PHY001" ? "重瞳" : "飞剑", aliases: ["双瞳"], category: id === "PHY001" ? "灵体" : "法宝",
  version: "1", grade: null, function: "比对灵流", activation: { trigger: "主动", requirement: "训练" },
  cost_limit: "眼部负荷", counter_failure: "遮蔽", visual_signature: "双瞳", parameters: "按剧配置", relations: [],
  image: { anchor: `${id}/anchor.png`, prompt: `${id}/prompt.txt`, sha256: hasImage ? "abc" : null, status, review_notes: ["留意边界"] },
});
async function mount(query = ""): Promise<void> {
  vi.mocked(loadSharedLibrary).mockResolvedValue({ title: "仙侠公共资产主数据", version: "1", assets: [asset("PHY001", "reviewed_with_notes", true), asset("ART001", "generated_unreviewed", true), asset("ART002", "failed_or_unknown", false)] });
  render(<MemoryRouter initialEntries={[`/assets?library=ai_videos%2F_shared%2Fxianxia${query}`]}><AssetOverviewPage /></MemoryRouter>);
  await act(async () => { await Promise.resolve(); });
}
it("opens the series library through the existing asset overview and separates image count from acceptance", async () => {
  await mount();
  expect(loadSharedLibrary).toHaveBeenCalledWith("ai_videos/_shared/xianxia");
  expect(screen.getByRole("heading", { name: "仙侠公共资产" })).toBeTruthy();
  expect(screen.getByLabelText("资产进度").textContent).toContain("3 项定义2 项有图1 项基础图已验收");
  fireEvent.change(screen.getByLabelText("验收状态"), { target: { value: "accepted" } });
  expect(screen.getByRole("button", { name: "PHY001 重瞳" })).toBeTruthy();
  expect(screen.queryByRole("button", { name: "ART001 飞剑" })).toBeNull();
});
it("finds aliases and previews limitations, notes and the actual image through existing file endpoints", async () => {
  await mount();
  fireEvent.change(screen.getByLabelText("资产类别"), { target: { value: "灵体" } });
  fireEvent.change(screen.getByLabelText("搜索公共资产"), { target: { value: "双瞳" } });
  fireEvent.click(screen.getByRole("button", { name: "PHY001 重瞳" }));
  const panel = screen.getByRole("article", { name: "PHY001 重瞳" });
  expect(screen.queryByRole("dialog")).toBeNull();
  expect(screen.queryByRole("button", { name: "PHY001 重瞳" })).toBeNull();
  expect(within(panel).getByText("眼部负荷")).toBeTruthy();
  expect(within(panel).getByText("留意边界")).toBeTruthy();
  expect(within(panel).getByRole("img").getAttribute("src")).toContain(encodeURIComponent("ai_videos/_shared/xianxia/PHY001/anchor.png"));
  fireEvent.click(within(panel).getByRole("button", { name: "返回资产列表" }));
  expect(screen.queryByRole("article")).toBeNull();
  expect(screen.getByRole("button", { name: "PHY001 重瞳" })).toBeTruthy();
});
it("supports a direct asset link and shows missing output without a broken image", async () => {
  await mount("&open=ART002");
  const panel = screen.getByRole("article", { name: "ART002 飞剑" });
  expect(within(panel).getByText("尚无图片，设定已建立")).toBeTruthy();
  expect(within(panel).queryByRole("img")).toBeNull();
});

it("opens a Chinese subgroup from navigation and displays all three views for its asset", async () => {
  const building = { ...asset("BG001", "reviewed", true), name: "云阶山门",
    views: { sheet: "background/bg001/views_v1.png", prompt: "background/bg001/views_v1.txt", sha256: "views-sha", status: "generated_unreviewed", panels: ["正面", "侧面", "背面"] } };
  vi.mocked(loadSharedLibrary).mockResolvedValue({ title: "仙侠公共资产主数据", version: "1", assets: [building, asset("PHY001", "reviewed", true)],
    navigation: [{ id: "buildings", name: "建筑与设施", children: [{ id: "sect", name: "宗门与修行", asset_ids: ["BG001"] }] },
      { id: "traits", name: "灵体与天赋", children: [{ id: "eyes", name: "瞳术", asset_ids: ["PHY001"] }] }] });
  render(<MemoryRouter initialEntries={["/assets?library=ai_videos%2F_shared%2Fxianxia&group=buildings&sub=sect&open=BG001"]}><AssetOverviewPage /></MemoryRouter>);
  await act(async () => { await Promise.resolve(); });
  expect(screen.getByLabelText("资产分类位置").textContent).toContain("建筑与设施 / 宗门与修行 / 云阶山门");
  const views = screen.getByLabelText("资产三视图");
  expect(within(views).getByRole("img").getAttribute("src")).toContain(encodeURIComponent("background/bg001/views_v1.png"));
  expect(within(views).getByText(/左起依次/)).toBeTruthy();
  fireEvent.click(screen.getByRole("button", { name: "返回资产列表" }));
  expect(screen.getByText("找到 1 项资产")).toBeTruthy();
  expect(screen.queryByRole("button", { name: "PHY001 重瞳" })).toBeNull();
  fireEvent.change(screen.getByLabelText("资产类别"), { target: { value: "traits" } });
  expect(screen.getByRole("button", { name: "PHY001 重瞳" })).toBeTruthy();
  expect(screen.queryByRole("button", { name: "BG001 云阶山门" })).toBeNull();
  fireEvent.change(screen.getByLabelText("资产类别"), { target: { value: "buildings" } });
  fireEvent.change(screen.getByLabelText("三视图状态"), { target: { value: "accepted" } });
  expect(screen.queryByRole("button", { name: "BG001 云阶山门" })).toBeNull();
  fireEvent.change(screen.getByLabelText("三视图状态"), { target: { value: "generated_unreviewed" } });
  expect(screen.getByRole("button", { name: "BG001 云阶山门" })).toBeTruthy();
});

it("only highlights the selected asset route rather than every ancestor with a library link", () => {
  const root = "/assets?library=ai_videos%2F_shared%2Fxianxia";
  const selected = "?library=ai_videos%2F_shared%2Fxianxia&group=buildings&sub=sect&open=BG001";
  expect(matchesNavigation(root, "/assets", selected)).toBe(false);
  expect(matchesNavigation(root + "&group=buildings", "/assets", selected)).toBe(false);
  expect(matchesNavigation(root + "&group=buildings&sub=sect&open=BG001", "/assets", selected)).toBe(true);
});
