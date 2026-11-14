import { act, cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { MemoryRouter, Route, Routes, useLocation } from "react-router-dom";
import { afterEach, expect, it, vi } from "vitest";
import { AssetOverviewPage } from "../src/components/AssetOverviewPage";
import { filterSections, loadAssetOverview, type AssetOverview, type AssetTile } from "../src/lib/assetOverview";
import { loadCharacterReel } from "../src/lib/characterReel";

vi.mock("../src/lib/assetOverview", async importOriginal => ({ ...await importOriginal<typeof import("../src/lib/assetOverview")>(), loadAssetOverview: vi.fn() }));
vi.mock("../src/lib/characterReel", async importOriginal => ({ ...await importOriginal<typeof import("../src/lib/characterReel")>(), loadCharacterReel: vi.fn() }));
afterEach(() => { cleanup(); vi.clearAllMocks(); });

const W = "ai_videos/dota/2_世界观人设";
function tile(group: string, key: string, name: string, extra: Partial<AssetTile> = {}): AssetTile {
  const folder = `${key}_${name}`;
  const path = `${W}/${group}/${folder}`;
  return { key, folder, path, card: `${path}/${folder}.md`, name, title: `${name} · X`, portrait: `${path}/${folder}.png`,
    images: [`${path}/${folder}.png`], videos: [], meta: [], ...extra };
}
const AM = tile("characters/近卫_sentinel", "c24", "敌法师", {
  images: [`${W}/characters/近卫_sentinel/c24_敌法师/c24_敌法师.png`, `${W}/characters/近卫_sentinel/c24_敌法师/c24_敌法师_v2.png`],
  videos: [`${W}/characters/近卫_sentinel/c24_敌法师/c24_敌法师_turntable.mp4`], meta: ["键：`c24`　｜　近卫 / 敏捷"],
});
const DATA: AssetOverview = {
  drama: "ai_videos/dota",
  watch: [`${W}/background`, `${W}/characters`, `${W}/props`],
  sections: [
    { kind: "characters", label: "人物", count: 3, groups: [
      { name: "近卫_sentinel", tiles: [tile("characters/近卫_sentinel", "c1", "树精卫士"), AM] },
      { name: "天灾_scourge", tiles: [tile("characters/天灾_scourge", "c65", "斧王")] },
    ] },
    { kind: "background", label: "背景", count: 1, groups: [{ name: "", tiles: [tile("background", "bg1", "河道")] }] },
    { kind: "props", label: "道具", count: 0, groups: [] },
  ],
};

function Where(): JSX.Element {
  return <output data-testid="where">{useLocation().search}</output>;
}

async function mount(search = ""): Promise<void> {
  vi.mocked(loadAssetOverview).mockResolvedValue(DATA);
  vi.mocked(loadCharacterReel).mockResolvedValue({ name: "", path: "", turntable: null, watch: [], cuts: { draft: [], final: [] },
    skills: [{ key: "k241", title: "法力损毁 · Mana Break", path: "", card: "", icon: "icon.png", peak: "peak.png", final: null, finals: [], drafts: [] }] });
  render(
    <MemoryRouter initialEntries={[`/assets?drama=ai_videos%2Fdota${search}`]}>
      <Routes><Route path="/assets" element={<><AssetOverviewPage /><Where /></>} /></Routes>
    </MemoryRouter>,
  );
  await act(async () => { await Promise.resolve(); });
}

it("lists every asset as one tile, grouped by section and group", async () => {
  await mount();
  expect(loadAssetOverview).toHaveBeenCalledWith("ai_videos/dota");
  const people = screen.getByRole("region", { name: "人物" });
  expect(within(people).getByText("近卫_sentinel")).toBeTruthy();
  expect(within(people).getAllByRole("button").map(b => b.textContent)).toEqual(["c1树精卫士", "▶c24敌法师", "c65斧王"]);
  expect(within(screen.getByRole("region", { name: "道具" })).getByText("还没有资产")).toBeTruthy();
});

it("clicking a tile opens the preview with its media, meta and skills; arrows step and Esc closes", async () => {
  await mount();
  await act(async () => { fireEvent.click(screen.getByTitle("敌法师 · X")); await Promise.resolve(); });
  const dialog = screen.getByRole("dialog", { name: "c24 敌法师" });
  expect(screen.getByTestId("where").textContent).toContain(encodeURIComponent(AM.path));
  expect(within(dialog).getByText("图片与视频 · 3")).toBeTruthy();
  expect(within(dialog).getByText("2 / 4")).toBeTruthy();
  expect(within(dialog).getByText("c24", { selector: "code" })).toBeTruthy();
  expect(loadCharacterReel).toHaveBeenCalledWith(AM.path);
  expect(within(dialog).getByText("法力损毁 · Mana Break")).toBeTruthy();
  fireEvent.click(within(dialog).getByTitle("c24_敌法师_turntable.mp4"));
  expect(dialog.querySelector("video")?.getAttribute("src")).toContain("turntable.mp4");
  act(() => { fireEvent.keyDown(window, { key: "ArrowRight" }); });
  expect(screen.getByRole("dialog", { name: "c65 斧王" })).toBeTruthy();
  act(() => { fireEvent.keyDown(window, { key: "Escape" }); });
  expect(screen.queryByRole("dialog")).toBeNull();
});

it("opens straight from ?open= and filters by key or name", async () => {
  await mount(`&open=${encodeURIComponent(AM.path)}`);
  expect(screen.getByRole("dialog", { name: "c24 敌法师" })).toBeTruthy();
  const filtered = filterSections(DATA.sections, "斧");
  expect(filtered.map(s => s.count)).toEqual([1, 0, 0]);
  expect(filterSections(DATA.sections, "C24")[0].groups.map(g => g.name)).toEqual(["近卫_sentinel"]);
});
