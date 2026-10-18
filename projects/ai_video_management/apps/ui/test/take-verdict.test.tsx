import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, expect, it, vi } from "vitest";
import { EpisodeWorkflowPage } from "../src/components/EpisodeWorkflowPage";
import { judgeTake, loadWorkflow, type EpisodeWorkflow, type ShotTake } from "../src/lib/episodeWorkflow";

vi.mock("../src/lib/episodeWorkflow", async importOriginal => ({ ...await importOriginal<typeof import("../src/lib/episodeWorkflow")>(),
  loadWorkflow: vi.fn(), judgeTake: vi.fn() }));
afterEach(() => { cleanup(); vi.clearAllMocks(); });

const SHOT = "ai_videos/demo/episodes/ep01/scenes/s1/shots/st1/renders";
const takes: ShotTake[] = [
  { id: "20261016-210000_cccc3333", path: `${SHOT}/20261016-210000_cccc3333`, videos: [], review: "", review_path: "", review_status: "待审核",
    generation: { stage: "final", resolution: "720p", from_take: "20261016-200000_aaaa1111" }, prompt_path: "" },
  { id: "20261016-200000_aaaa1111", path: `${SHOT}/20261016-200000_aaaa1111`, videos: [], review: "", review_path: "", review_status: "待审核",
    generation: { stage: "draft", resolution: "480p" }, prompt_path: "" },
];
const fixture = {
  episode_path: "ai_videos/demo/episodes/ep01", shot_keys: { s1: { st1: "ep1_s1_st1" } },
  modules: [
    { id: "story", label: "故事创作", content: { brief: "方向", text: "正文" } },
    { id: "filming", label: "影视改编", content: { scenes: [] } },
    { id: "prompts", label: "Prompt 编译", content: { scenes: [{ id: "s1", shots: [{ id: "ep1_s1_st1", text: "ep1_s1_st1\n时长：6秒" }] }] } },
  ].map(module => ({ ...module, status: "approved", etag: "e", revision: "r", input_revision: null, source_revision: null, can_edit: false })),
  renders: { ep1_s1_st1: takes },
} as unknown as EpisodeWorkflow;

it("labels drafts and finals and lets the user pass a draft (follow-up 265)", async () => {
  vi.mocked(loadWorkflow).mockResolvedValue(fixture);
  vi.mocked(judgeTake).mockResolvedValue({ review_status: "通过（用户 2026-10-16 21:00，可出正式条）" });
  render(<MemoryRouter initialEntries={["/drama?episode=ep01&module=prompts&scene=s1&shot=ep1_s1_st1"]}>
    <EpisodeWorkflowPage dramaPath="ai_videos/demo" title="示例" /></MemoryRouter>);
  const panel = await screen.findByRole("region", { name: "生成记录" });
  expect(within(panel).getByText("草稿")).toBeInTheDocument();
  expect(within(panel).getByText("正式条")).toBeInTheDocument();
  expect(within(panel).getByText("出自草稿 20261016-200000_aaaa1111")).toBeInTheDocument();
  expect(within(panel).getAllByRole("group")).toHaveLength(1);   // 只有草稿能审
  fireEvent.click(within(panel).getByRole("button", { name: "通过，可出正式条" }));
  expect(vi.mocked(judgeTake)).toHaveBeenCalledWith(`${SHOT}/20261016-200000_aaaa1111`, "通过");
  await waitFor(() => expect(vi.mocked(loadWorkflow)).toHaveBeenCalledTimes(2));   // 审完重新读，状态跟着变
});
