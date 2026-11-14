import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, expect, it, vi } from "vitest";
import { MapRegionsPage } from "../src/components/MapRegionsPage";
import { loadRegionMap, parseRegionMap, type RegionMap } from "../src/lib/mapRegions";
import { fetchFile } from "../src/api";
import { originalPoint, RegionObjectDiagram } from "../src/components/RegionObjectDiagram";

vi.mock("../src/api", async original => ({ ...await original<typeof import("../src/api")>(), fetchFile: vi.fn() }));
vi.mock("../src/lib/fileEvents", () => ({ useFileChanges: vi.fn() }));
afterEach(() => { cleanup(); vi.clearAllMocks(); });
const path = "ai_videos/dota/0_research/map/manifest.json";
const data: RegionMap = { schema: 1, title: "地图区域", version: "6.83d", overview: "map.png", source_map: "source.png", base_layout: "base.json", notes: [],
  groups: [{ id: "S", name: "近卫基地", color: "green" }, { id: "D", name: "天灾基地", color: "blue" }],
  regions: ["S", "D"].map((id, index) => ({ id: id + "1", parent: id, name: "泉水与商店", asset_id: `bg${13 + index}`, position: [10 + index * 80, 90 - index * 80], card: `${id}.md`, note: "候选",
    instance_refs: [], instances: [], assets: [{ id: "bg25", name: "泉水", card: "fountain.md", image: "fountain.png" }],
    views: [{ id: "wide", label: "远景", file: `${id}.png`, target: `${id}.png`, status: "existing", review: "已有", prompt: "prompt.txt" },
      { id: "side", label: "侧面", file: null, target: "side.png", status: "unknown", review: "未收到图片", prompt: "side.txt" }] })) };

it("keeps exactly one navigation panel when switching regions and camera tabs", async () => {
  const d=structuredClone(data);d.navigation="nav.json";
  const nav={schema:1,title:"通行研究",revision:"v1",status:"静态",source_map:"source.png",reconstruction:"terrain.png",grid:"grid.json",report:"research.md",layers:[],limitations:[],
    regions:Object.fromEntries(d.regions.map(r=>[r.id,{bounds:[0,0,100,100],tree_count:1,layer_percentages:{10:100},percentages:{walk:100},ground_vertex_z_range:[1024,1024],constraints:"constraints.md"}]))};
  const grid={width:512,height:512,cell_game_units:32,origin:"northwest",bits:["walk","blocked","trees","cliffs","ramps","uncertain"],cells_base64:btoa("\x01".repeat(512*512)),height_layers_base64:btoa("\x0a".repeat(512*512))};
  vi.mocked(fetchFile).mockImplementation(async p=>({content:JSON.stringify(p===path?d:p.endsWith("nav.json")?nav:p.endsWith("grid.json")?grid:{rows:[]})} as Awaited<ReturnType<typeof fetchFile>>));
  render(<MemoryRouter initialEntries={[`/map-regions?path=${encodeURIComponent(path)}&region=S1`]}><MapRegionsPage/></MemoryRouter>);
  await screen.findByRole("region",{name:"S1 通行与高差研究"});
  fireEvent.click(within(screen.getByRole("navigation",{name:"地图资产层级"})).getByRole("button",{name:/^D1 /}));
  await screen.findByRole("region",{name:"D1 通行与高差研究"});
  for(const label of [/^侧面/,/^远景/,/^侧面/]){
    fireEvent.click(within(screen.getByRole("group",{name:"区域机位"})).getByRole("button",{name:label}));
    expect(screen.getAllByRole("region",{name:"D1 通行与高差研究"})).toHaveLength(1);
  }
  expect(screen.queryByRole("region",{name:"S1 通行与高差研究"})).toBeNull();
});

it("navigates hierarchy and map, keeps region URL, and does not invent a link for missing media", async () => {
  vi.mocked(fetchFile).mockImplementation(async p => ({ content: JSON.stringify(p === path ? data : { rows: [] }) } as Awaited<ReturnType<typeof fetchFile>>));
  render(<MemoryRouter initialEntries={[`/map-regions?path=${encodeURIComponent(path)}&region=D1`]}><MapRegionsPage /></MemoryRouter>);
  await screen.findByRole("heading", { name: "地图区域" });
  expect(screen.getByAltText("D1 泉水与商店 远景")).toBeTruthy();
  fireEvent.click(screen.getByRole("button", { name: "定位 S1 泉水与商店" }));
  expect(screen.getByAltText("S1 泉水与商店 远景")).toBeTruthy();
  fireEvent.click(screen.getByRole("button", { name: /侧面/ }));
  expect(screen.getByRole("status").textContent).toContain("生成未完成");
  expect(screen.queryByRole("link", { name: "下载侧面原图" })).toBeNull();
  const nav = screen.getByRole("navigation", { name: "地图资产层级" });
  fireEvent.change(within(nav).getByRole("textbox"), { target: { value: "bg14" } });
  expect(within(nav).queryByRole("button", { name: /S1/ })).toBeNull();
  expect(within(nav).getByRole("button", { name: /D1/ })).toBeTruthy();
});

it("rejects duplicate region IDs, invalid parents and out-of-map positions", () => {
  for (const mutate of [(d: RegionMap) => { d.regions[1].id = "S1"; }, (d: RegionMap) => { d.regions[0].parent = "missing"; }, (d: RegionMap) => { d.regions[0].position[0] = 101; }]) {
    const d = structuredClone(data); mutate(d); expect(() => parseRegionMap(JSON.stringify(d), path)).toThrow();
  }
});
it("rejects paths outside exposed assets", () => {
  const d = structuredClone(data); d.regions[0].views[0].file = "../../../../../../secrets.png";
  expect(() => parseRegionMap(JSON.stringify(d), path)).toThrow();
});
it("resolves instance positions from the canonical base layout and rejects duplicate assignments", async () => {
  const d = structuredClone(data); d.regions[0].instance_refs = ["sentinel:bg15#01"];
  const row = { faction: "sentinel", instance_id: "bg15#01", asset_id: "bg15", name: "泉水", x: -7296, y: -7200, facing: 270, category: "building", point_number: 2 };
  vi.mocked(fetchFile).mockImplementation(async p => ({ content: JSON.stringify(p === path ? d : { rows: [row] }) } as Awaited<ReturnType<typeof fetchFile>>));
  expect((await loadRegionMap(path)).regions[0].instances[0]).toEqual(row);
  d.regions[1].instance_refs = ["sentinel:bg15#01"];
  await expect(loadRegionMap(path)).rejects.toThrow("重复");
});
it("shows fetch errors without presenting broken images", async () => {
  vi.mocked(fetchFile).mockRejectedValueOnce(new Error("清单不可读"));
  render(<MemoryRouter initialEntries={[`/map-regions?path=${encodeURIComponent(path)}`]}><MapRegionsPage /></MemoryRouter>);
  expect((await screen.findByRole("alert")).textContent).toContain("清单不可读");
  expect(screen.queryByRole("img")).toBeNull();
});

it("keeps the actual overhead reference and flags a changed anchor", async () => {
  const d = structuredClone(data), r = d.regions[0];
  r.views[0].reference_overhead = { file: "old-overhead.png", sha256: "a".repeat(64) };
  r.views.push({ id: "overhead", label: "俯视", file: "new-overhead.png", target: "new-overhead.png", status: "reviewed", review: "", prompt: "overhead.txt", sha256: "b".repeat(64) });
  vi.mocked(fetchFile).mockImplementation(async p => ({ content: JSON.stringify(p === path ? d : { rows: [] }) } as Awaited<ReturnType<typeof fetchFile>>));
  render(<MemoryRouter initialEntries={[`/map-regions?path=${encodeURIComponent(path)}`]}><MapRegionsPage /></MemoryRouter>);
  await screen.findByRole("heading", { name: "地图区域" });
  fireEvent.click(within(screen.getByRole("group", { name: "区域机位" })).getByRole("button", { name: /^远景/ }));
  expect(await screen.findByText(/参考俯视图已更新，本机位需要复核/)).toBeTruthy();
  expect(screen.getByRole("link", { name: "查看生成时使用的俯视母图" }).getAttribute("href")).toContain("old-overhead.png");
  fireEvent.click(screen.getByRole("button", { name: "切换俯视对照" }));
  expect(screen.getByAltText("S1 泉水与商店 俯视")).toBeTruthy();
  r.views[0].reference_overhead.sha256 = "invalid";
  expect(() => parseRegionMap(JSON.stringify(d), path)).toThrow("指纹无效");
});

it("pairs the same building ID on generated and original views and can expand the comparison", async () => {
  const d = structuredClone(data);
  d.regions[0].views[0].id = "overhead";
  d.regions[0].building_comparison = { reference: "game.jpg", source_record: "refs.md", reference_label: "6.83d", note: "位置未校准", generated_size: [1600,900], reference_size: [640,480], markers: [{ asset_id: "bg25", generated: [40,40,20,20], reference: [60,60,80,80] }] };
  vi.mocked(fetchFile).mockImplementation(async p => ({ content: JSON.stringify(p === path ? d : { rows: [] }) } as Awaited<ReturnType<typeof fetchFile>>));
  render(<MemoryRouter initialEntries={[`/map-regions?path=${encodeURIComponent(path)}&region=S1&focus=buildings`]}><MapRegionsPage /></MemoryRouter>);
  const comparison = await screen.findByRole("region", { name: "S1 泉水建筑对照" });
  expect(within(comparison).getAllByRole("img")).toHaveLength(2);
  expect(comparison.querySelectorAll("svg text")).toHaveLength(2);
  expect([...comparison.querySelectorAll("svg text")].every(t => t.textContent === "bg25")).toBe(true);
  expect(within(comparison).getByRole("link", { name: "下载未标注游戏原图" }).getAttribute("href")).toContain("game.jpg");
  fireEvent.click(within(comparison).getByRole("button", { name: "放大并排对照" }));
  const dialog = screen.getByRole("dialog", { name: "S1 放大建筑对照" });
  fireEvent.click(within(dialog).getByRole("checkbox"));
  expect(dialog.querySelectorAll("svg text")).toHaveLength(0);
  fireEvent.keyDown(window, { key: "Escape" });
  expect(screen.queryByRole("dialog")).toBeNull();
  d.regions[0].building_comparison.markers[0].asset_id = "unknown";
  expect(() => parseRegionMap(JSON.stringify(d), path)).toThrow("建筑对照标注资料无效");
});

it("uses canonical instance coordinates for north-up positions, including NPCs and spawn points", () => {
  const r = structuredClone(data.regions[0]);
  r.instances = [
    { instance_id: "m300#01", x: 20, y: 80 },
    { instance_id: "SPAWN#01", x: 50, y: 20 },
  ] as typeof r.instances;
  r.building_comparison = { reference: "game.jpg", source_record: "refs.md", reference_label: "原图", note: "", generated_size: [1000,1000], reference_size: [640,480], layout_bounds: [0,0,100,100], markers: [] };
  expect(originalPoint(r, { asset_id: "m300", generated: [0,0,0,0], reference: null })).toEqual([20,20]);
  expect(originalPoint(r, { asset_id: "SPAWN#01", instance_id: "SPAWN#01", generated: [0,0,0,0], reference: null })).toEqual([50,80]);
  expect(originalPoint(r, { asset_id: "missing", generated: [0,0,0,0], reference: null })).toBeNull();
});

it("draws the coordinate overhead at the true bounds aspect, over a registered layout underlay when given", () => {
  const r = structuredClone(data.regions[0]);
  r.instances = [{ instance_id: "m300#01", x: 150, y: 110 }] as typeof r.instances;
  r.building_comparison = { reference: "game.jpg", source_record: "refs.md", reference_label: "原图", note: "", generated_size: [1000,1000], reference_size: [640,480],
    layout_bounds: [0,0,300,220], layout_underlay: { file: "layout_top.png", note: "三维布局正交俯视" }, markers: [{ asset_id: "m300", category: "merchant", generated: [0,0,0,0], reference: null }] };
  const { container } = render(<RegionObjectDiagram region={r} filter="all" labels image={p => `/img/${p}`} />);
  const svg = container.querySelector("svg")!;
  expect(svg.getAttribute("viewBox")).toBe("0 0 1000 733");
  expect(svg.querySelector("image")?.getAttribute("href")).toBe("/img/layout_top.png");
  const dot = svg.querySelector("circle")!;
  expect([dot.getAttribute("cx"), Number(dot.getAttribute("cy")).toFixed(1)]).toEqual(["500", "366.5"]);
  const d = structuredClone(data);
  d.regions[0].building_comparison = { ...r.building_comparison, layout_bounds: undefined, markers: [{ asset_id: "bg25", generated: [1,1,1,1], reference: null }] };
  d.regions[0].views.push({ id: "overhead", label: "俯视", file: "top.png", target: "top.png", status: "reviewed", review: "", prompt: "top.txt" });
  expect(() => parseRegionMap(JSON.stringify(d), path)).toThrow("原版布局底图无效");
});

it.each(["current", "changed-anchor", "changed-view"])("keeps historical generation references and invalidates stale manual layout reviews: %s", async scenario => {
  const d = structuredClone(data), r = d.regions[0];
  r.views[0].sha256 = "c".repeat(64);
  r.views[0].reference_overhead = { file: "old-overhead.png", sha256: "a".repeat(64) };
  r.views[0].layout_review = { overhead_sha256: "b".repeat(64), view_sha256: "c".repeat(64), note: "仅补出生圈，通道位置保留" };
  r.views.push({ id: "overhead", label: "俯视", file: "new-overhead.png", target: "new-overhead.png", status: "reviewed", review: "", prompt: "overhead.txt", sha256: scenario === "changed-anchor" ? "d".repeat(64) : "b".repeat(64) });
  if (scenario === "changed-view") r.views[0].sha256 = "e".repeat(64);
  vi.mocked(fetchFile).mockImplementation(async p => ({ content: JSON.stringify(p === path ? d : { rows: [] }) } as Awaited<ReturnType<typeof fetchFile>>));
  render(<MemoryRouter initialEntries={[`/map-regions?path=${encodeURIComponent(path)}`]}><MapRegionsPage /></MemoryRouter>);
  await screen.findByRole("heading", { name: "地图区域" });
  fireEvent.click(within(screen.getByRole("group", { name: "区域机位" })).getByRole("button", { name: /^远景/ }));
  expect(await screen.findByText(scenario === "current" ? /已按当前俯视复核/ : /参考俯视图已更新，本机位需要复核/)).toBeTruthy();
  expect(screen.getByRole("link", { name: "查看生成时使用的俯视母图" }).getAttribute("href")).toContain("old-overhead.png");
});

it("defaults each region to overhead and keeps its original beside every angle or in its own tab", async () => {
  const d = structuredClone(data);
  for (const r of d.regions) {
    r.views.push({ id: "overhead", label: "俯视", file: r.id + "-top.png", target: r.id + "-top.png", status: "reviewed", review: "", prompt: "top.txt" });
    r.original_reference = { file: r.id + "-game.jpg", kind: "gameplay", label: "游戏截图", note: "原图参考", source_record: "refs.json", map_bounds: [0, 10, 30, 50] };
  }
  vi.mocked(fetchFile).mockImplementation(async p => ({ content: JSON.stringify(p === path ? d : { rows: [] }) } as Awaited<ReturnType<typeof fetchFile>>));
  render(<MemoryRouter initialEntries={[`/map-regions?path=${encodeURIComponent(path)}&region=S1`]}><MapRegionsPage /></MemoryRouter>);
  await screen.findByAltText("S1 泉水与商店 俯视");
  const tabs = screen.getByRole("group", { name: "区域机位" });
  expect(within(tabs).getAllByRole("button")[0].textContent).toContain("俯视");
  for (const name of [/^远景/, /^侧面/, /^原图/]) {
    fireEvent.click(within(tabs).getByRole("button", { name }));
    expect(screen.getByAltText("S1 泉水与商店 游戏原图")).toBeTruthy();
  }
  fireEvent.click(screen.getByRole("button", { name: "定位 D1 泉水与商店" }));
  expect(screen.getByAltText("D1 泉水与商店 俯视")).toBeTruthy();
  expect(screen.getByAltText("D1 泉水与商店 游戏原图")).toBeTruthy();
  expect(screen.queryByAltText("S1 泉水与商店 游戏原图")).toBeNull();
  fireEvent.click(screen.getByLabelText("并排显示原图"));
  expect(screen.queryByRole("region", { name: "D1 原图对照" })).toBeNull();
  fireEvent.click(within(tabs).getByRole("button", { name: /^原图/ }));
  expect(screen.getByRole("region", { name: "D1 原图对照" })).toBeTruthy();
  fireEvent.click(screen.getByRole("button", { name: "查看近卫基地" }));
  expect(screen.getByAltText("S1 泉水与商店 俯视")).toBeTruthy();
});

it("rejects invalid original reference crops and paths", () => {
  const d = structuredClone(data);
  d.regions[0].original_reference = { file: "source.png", kind: "map", label: "原版地图", note: "", source_record: "refs.json", map_bounds: [20, 10, 10, 50] };
  expect(() => parseRegionMap(JSON.stringify(d), path)).toThrow("原图资料无效");
  d.regions[0].original_reference.map_bounds = [0,0,100,100];
  d.regions[0].original_reference.file = "../../../../../../secret.png";
  expect(() => parseRegionMap(JSON.stringify(d), path)).toThrow();
});

it.each([false,true])("shows five hero envelopes only for the reviewed overhead, stale=%s", async stale => {
  const d = structuredClone(data), r = d.regions[0];
  r.views[0].id = "overhead"; r.views[0].sha256 = "a".repeat(64);
  r.building_comparison = { reference: "game.jpg", source_record: "refs.md", reference_label: "原图", note: "", generated_size: [1600,1000], reference_size: [640,480], markers: [{asset_id:"bg25",generated:[40,40,20,20],reference:null}], capacity: {overhead_sha256:(stale ? "b" : "a").repeat(64),area:[[20,20],[80,20],[80,80],[20,80]],heroes:[[30,30,3,2],[50,30,3,2],[70,30,3,2],[40,60,3,2],[60,60,3,2]],note:"占位示意"} };
  vi.mocked(fetchFile).mockImplementation(async p => ({ content: JSON.stringify(p === path ? d : { rows: [] }) } as Awaited<ReturnType<typeof fetchFile>>));
  render(<MemoryRouter initialEntries={[`/map-regions?path=${encodeURIComponent(path)}`]}><MapRegionsPage /></MemoryRouter>);
  await screen.findByRole("region",{name:"S1 泉水建筑对照"});
  const toggle=screen.queryByLabelText("五英雄活动空间");
  if(stale) expect(toggle).toBeNull();
  else {fireEvent.click(toggle!);expect(document.querySelectorAll('[aria-label="五英雄活动范围示意"] ellipse')).toHaveLength(5);fireEvent.click(toggle!);expect(document.querySelector('[aria-label="五英雄活动范围示意"]')).toBeNull();}
});
