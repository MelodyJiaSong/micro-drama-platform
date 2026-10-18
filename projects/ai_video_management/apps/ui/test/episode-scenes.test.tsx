import { cleanup, render, screen, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, expect, it, vi } from "vitest";
import { EpisodeWorkflowPage } from "../src/components/EpisodeWorkflowPage";
import { loadWorkflow, type EpisodeWorkflow, type FilmingScene } from "../src/lib/episodeWorkflow";
import { matchesNavigation } from "../src/lib/globalWorkflow";

vi.mock("../src/lib/episodeWorkflow", async importOriginal => ({ ...await importOriginal<typeof import("../src/lib/episodeWorkflow")>(), loadWorkflow: vi.fn() }));
afterEach(() => { cleanup(); vi.clearAllMocks(); });

const scenes: FilmingScene[] = ["s1", "s10"].map(id => ({ id, background: "bg2", location: "交接棚", time: "白天", purpose: "争取差事",
  shots: [{ id: "st1", duration: 6, action: "递出袋子", camera: "固定中景", dialogue: "给你。", cast: [], blocking: "", beats: "0–6秒 递出袋子", lighting: "白天散射光" }] }));
const fixture: EpisodeWorkflow = {
  episode_path: "ai_videos/demo/episodes/ep01", shot_keys: { s1: { st1: "ep1_s1_st1" }, s10: { st1: "ep1_s10_st1" } },
  modules: [
    { id: "story", label: "故事创作", content: { brief: "方向", text: "正文" } },
    { id: "filming", label: "影视改编", content: { scenes } },
    { id: "prompts", label: "Prompt 编译", content: { scenes: scenes.map(scene => ({ id: scene.id, shots: [{ id: `ep1_${scene.id}_st1`, text: `ep1_${scene.id}_st1\n时长：6秒。` }] })) } },
  ].map(module => ({ ...module, status: "approved", etag: "etag", revision: "r", input_revision: null, source_revision: null, can_edit: false })) as EpisodeWorkflow["modules"],
};

function page(query: string): void {
  vi.mocked(loadWorkflow).mockResolvedValue(fixture);
  render(<MemoryRouter initialEntries={[`/drama?episode=ep01&${query}`]}><EpisodeWorkflowPage dramaPath="ai_videos/demo" title="示例" /></MemoryRouter>);
}

it("shows only the selected scene shot while retaining its environment and purpose", async () => {
  page("module=filming&scene=s10&shot=ep1_s10_st1");
  await screen.findByRole("heading", { name: "ep1_s10_st1 · 6秒" });
  expect(screen.queryByRole("heading", { name: "ep1_s1_st1 · 6秒" })).toBeNull();
  expect(screen.getByText("环境资产：bg2")).toBeTruthy();
  expect(screen.getByText("本场目标与变化：争取差事")).toBeTruthy();
  expect(document.querySelectorAll("input,textarea")).toHaveLength(0);
});

it("displays an explicit missing-selection message instead of another shot", async () => {
  page("module=prompts&scene=s1&shot=ep1_s1_st99");
  expect(await screen.findByRole("alert")).toHaveTextContent("找不到指定场次或镜头");
  expect(screen.queryByRole("heading", { name: "ep1_s1_st1" })).toBeNull();
});

it("matches scene and shot navigation exactly", () => {
  const search = "?drama=demo&module=filming&episode=ep01&scene=s10&shot=ep1_s10_st1";
  expect(matchesNavigation("/drama?drama=demo&module=filming&episode=ep01", "/drama", search)).toBe(false);
  expect(matchesNavigation(`/drama${search}`, "/drama", search)).toBe(true);
  expect(matchesNavigation(`/drama${search.replace("scene=s10", "scene=s1")}`, "/drama", search)).toBe(false);
});

it("shows a placeholder for stages that are not designed yet, without loading module content", async () => {
  vi.mocked(loadWorkflow).mockResolvedValue(fixture);
  // 剪辑已有页面（follow-up 269，见 edit-stage.test.tsx）；声音与音乐仍是占位
  render(<MemoryRouter initialEntries={["/drama?episode=ep01&module=sound"]}><EpisodeWorkflowPage dramaPath="ai_videos/demo" title="示例" /></MemoryRouter>);
  expect(screen.getByRole("heading", { name: "声音与音乐" })).toBeInTheDocument();
  expect(screen.getByText("待设计")).toBeInTheDocument();
  expect(screen.queryByText("递出袋子")).not.toBeInTheDocument();
});

it("gives each compiled shot its own page with highlighted field labels and neighbour links", async () => {
  page("module=prompts&scene=s1&shot=ep1_s1_st1");
  expect(await screen.findByRole("heading", { name: "ep1_s1_st1" })).toBeInTheDocument();
  const block = screen.getByLabelText("视频 prompt");
  expect(block.textContent).toBe("ep1_s1_st1\n时长：6秒。");
  expect(block.querySelector(".shot-key-line")?.textContent).toBe("ep1_s1_st1");
  expect(block.querySelector(".field-label")?.textContent).toBe("时长");
  expect(screen.getByRole("link", { name: "ep1_s10_st1 →" })).toHaveAttribute("href", expect.stringContaining("shot=ep1_s10_st1"));
  expect(screen.queryByRole("heading", { name: "ep1_s10_st1" })).toBeNull();
});

it("lists a scene's shots as links instead of printing every prompt", async () => {
  page("module=prompts&scene=s10");
  const link = await screen.findByRole("link", { name: "ep1_s10_st1" });
  expect(link).toHaveAttribute("href", expect.stringContaining("shot=ep1_s10_st1"));
  expect(screen.queryByLabelText("视频 prompt")).toBeNull();
  expect(within(screen.getByRole("region", { name: "场次 s10" })).getByRole("heading", { name: "s10 · 交接棚 · 白天" })).toBeInTheDocument();
});

it("shows the scene's blocking diagram on a filming scene page, and says so when it has not been drawn", async () => {
  page("module=filming&scene=s10");
  const img = await screen.findByAltText("s10 走位图");
  expect(img.getAttribute("src")).toContain(encodeURIComponent("ai_videos/demo/episodes/ep01/scenes/s10/planning/s10_blocking.png"));
  img.dispatchEvent(new Event("error"));
  expect(await screen.findByText(/走位图尚未生成/)).toBeInTheDocument();
});

it("does not repeat the blocking diagram on a single shot page", async () => {
  page("module=filming&scene=s10&shot=ep1_s10_st1");
  await screen.findByRole("heading", { name: "ep1_s10_st1 · 6秒" });
  expect(screen.queryByAltText("s10 走位图")).toBeNull();
});
