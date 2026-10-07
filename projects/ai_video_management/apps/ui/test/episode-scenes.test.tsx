import { cleanup, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, expect, it, vi } from "vitest";
import { EpisodeWorkflowPage } from "../src/components/EpisodeWorkflowPage";
import { loadWorkflow, type EpisodeWorkflow, type FilmingScene } from "../src/lib/episodeWorkflow";
import { matchesNavigation } from "../src/lib/globalWorkflow";
import { isSceneVideoPath, isShotVideoPath } from "../src/components/SiblingMedia";

vi.mock("../src/lib/episodeWorkflow", () => ({ loadWorkflow: vi.fn() }));
afterEach(() => { cleanup(); vi.clearAllMocks(); });

const scenes: FilmingScene[] = ["s1", "s10"].map(id => ({ id, background: "bg2", location: "交接棚", time: "白天", purpose: "争取差事",
  shots: [{ id: "st1", duration: 6, action: "递出袋子", camera: "固定中景", dialogue: "给你。" }] }));
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

it("distinguishes background videos from scene-shot renders", () => {
  expect(isSceneVideoPath("ai_videos/demo/2_assets/background/bg2/video.mp4")).toBe(true);
  expect(isSceneVideoPath("ai_videos/demo/2_assets/scenes/bg2/video.mp4")).toBe(true);
  const path = "ai_videos/demo/episodes/ep01/scenes/s1/shots/st1/renders/take.mp4";
  expect(isShotVideoPath(path)).toBe(true);
  expect(isSceneVideoPath(path)).toBe(false);
});
