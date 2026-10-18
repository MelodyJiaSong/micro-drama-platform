import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, expect, it, vi } from "vitest";
import { EpisodeWorkflowPage } from "../src/components/EpisodeWorkflowPage";
import { ReviewReelPanel } from "../src/components/ReviewReelPanel";
import { loadWorkflow, type EpisodeWorkflow } from "../src/lib/episodeWorkflow";
import { chapterAt, loadReel, startReel, type ReviewReel } from "../src/lib/reviewReel";

vi.mock("../src/lib/reviewReel", async importOriginal => ({ ...await importOriginal<typeof import("../src/lib/reviewReel")>(), loadReel: vi.fn(), startReel: vi.fn() }));
vi.mock("../src/lib/episodeWorkflow", async importOriginal => ({ ...await importOriginal<typeof import("../src/lib/episodeWorkflow")>(), loadWorkflow: vi.fn() }));
afterEach(() => { cleanup(); vi.clearAllMocks(); });
HTMLMediaElement.prototype.play = vi.fn().mockResolvedValue(undefined);   // jsdom 没有实现播放

const EP = "ai_videos/demo/episodes/ep01";
const done: ReviewReel = {
  episode_path: EP, scene: null, name: "ep01_all", state: "done", done: 3, total: 3, error: "",
  video_path: `${EP}/review_reel/ep01_all.mp4`, stale: false,
  scenes: [{ id: "s1", label: "门前 · 白天", shots: 2 }, { id: "s2", label: "路上 · 清晨", shots: 1 }],
  manifest: {
    name: "ep01_all", created_at: "2026-10-15 20:30:00", duration: 11,
    chapters: [
      { scene: "s1", key: "ep1_s1_st1", take: "t1", video: "v1", start: 0, end: 5, duration: 5, review_status: "候选", note: "" },
      { scene: "s2", key: "ep1_s2_st3", take: "t3", video: "v3", start: 5, end: 11, duration: 6, review_status: "建议重出", note: "最新一条读不出，用了上一条" },
    ],
    skipped: [{ key: "ep1_s1_st2", scene: "s1", reason: "还没有生成" }],
  },
};

function panel(): void {
  render(<MemoryRouter><ReviewReelPanel episodePath={EP} initialScene={null} shotHref={(s, k) => `?scene=${s}&shot=${k}`} /></MemoryRouter>);
}

it("plays the reel with chapters that follow playback and jump on click", async () => {
  vi.mocked(loadReel).mockResolvedValue(done);
  panel();
  const chapters = await screen.findByRole("list", { name: "章节" });
  const items = within(chapters).getAllByRole("listitem");
  expect(items).toHaveLength(2);
  expect(items[1]).toHaveTextContent("建议重出");
  expect(items[1]).toHaveTextContent("用了上一条");
  const video = screen.getByLabelText("串联视频") as HTMLVideoElement;
  expect(video.getAttribute("src")).toContain(encodeURIComponent(`${EP}/review_reel/ep01_all.mp4`));
  video.currentTime = 6;
  fireEvent.timeUpdate(video);
  expect(items[1]).toHaveAttribute("aria-current", "true");
  fireEvent.click(within(items[0]).getByRole("button"));
  expect(video.currentTime).toBeCloseTo(0.01);
  expect(items[0]).toHaveAttribute("aria-current", "true");
  expect(screen.getByText("ep1_s1_st2 · 还没有生成")).toBeInTheDocument();
  expect(screen.getByRole("button", { name: "生成串联" })).toBeDisabled();   // 已是最新，不用重拼
});

it("starts a reel for the chosen scene and shows progress while it runs", async () => {
  vi.mocked(loadReel).mockResolvedValue({ ...done, scene: "s2", state: "none", video_path: "", manifest: null });
  vi.mocked(startReel).mockResolvedValue({ ...done, scene: "s2", state: "running", done: 0, total: 1, video_path: "", manifest: null });
  panel();
  fireEvent.change(await screen.findByLabelText("范围"), { target: { value: "s2" } });
  expect(vi.mocked(loadReel)).toHaveBeenLastCalledWith(EP, "s2");
  fireEvent.click(await screen.findByRole("button", { name: "生成串联" }));
  expect(vi.mocked(startReel)).toHaveBeenCalledWith(EP, "s2");
  expect(await screen.findByText(/正在拼接 0\/1 镜/)).toBeInTheDocument();
});

it("asks for a rebuild when newer takes exist", async () => {
  vi.mocked(loadReel).mockResolvedValue({ ...done, stale: true });
  panel();
  expect(await screen.findByText(/这条串联不是最新的/)).toBeInTheDocument();
  expect(screen.getByRole("button", { name: "生成串联" })).toBeEnabled();
});

it("is reached from the episode page header", async () => {
  vi.mocked(loadWorkflow).mockResolvedValue({ episode_path: EP, modules: [], shot_keys: {} } as EpisodeWorkflow);
  vi.mocked(loadReel).mockResolvedValue(done);
  render(<MemoryRouter initialEntries={["/drama?episode=ep01&module=prompts&view=reel"]}><EpisodeWorkflowPage dramaPath="ai_videos/demo" title="示例" /></MemoryRouter>);
  expect(await screen.findByRole("heading", { name: "审片串联" })).toBeInTheDocument();
  expect(screen.getByRole("link", { name: "返回模块" })).toHaveAttribute("href", expect.not.stringContaining("view=reel"));
});

it("maps playback time to a chapter", () => {
  const chapters = done.manifest!.chapters;
  expect(chapterAt(chapters, 0)).toBe(0);
  expect(chapterAt(chapters, 5)).toBe(1);
  expect(chapterAt(chapters, 11)).toBe(1);
});
