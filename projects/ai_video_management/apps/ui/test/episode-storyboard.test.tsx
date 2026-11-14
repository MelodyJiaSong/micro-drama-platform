import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, expect, it, vi } from "vitest";
import { fetchReviewRuns, type ReviewRunSummary } from "../src/api";
import { EpisodeWorkflowPage } from "../src/components/EpisodeWorkflowPage";
import {
  dialogueLines, isCurrentFirstFrame, latestSceneReview, reviewChipText, storyboardScenes,
} from "../src/lib/episodeStoryboard";
import { loadWorkflow, type EpisodeWorkflow, type FilmingScene } from "../src/lib/episodeWorkflow";

vi.mock("../src/lib/episodeWorkflow", async importOriginal => ({ ...await importOriginal<typeof import("../src/lib/episodeWorkflow")>(), loadWorkflow: vi.fn() }));
vi.mock("../src/api", async importOriginal => ({ ...await importOriginal<typeof import("../src/api")>(), fetchReviewRuns: vi.fn() }));
afterEach(() => { cleanup(); vi.clearAllMocks(); });

const EP = "ai_videos/demo/episodes/ep01";
const shot = (id: string, duration: number, dialogue = "") => ({ id, duration, action: `${id} 的行动`, camera: `${id} 的拍法`, dialogue, cast: ["c1"],
  blocking: `${id} 的走位`, beats: `${id} 的分拍`, lighting: "晨光" });
// 故事顺序：s8 排在 s5 前面（filming.json 的顺序就是故事顺序）；场内 st2 在 st1 前面
const scenes: FilmingScene[] = [
  { id: "s1", background: "bg1", location: "海边", time: "清晨", purpose: "开场：她穿越了", shots: [shot("st1", 12, "Riley（压低声音，美式英语）：Okay… I just time-traveled."), shot("st2", 7)] },
  { id: "s8", background: "bg8", location: "浴场", time: "下午", purpose: "泡澡", shots: [shot("st2", 9), shot("st1", 14, "Riley（问）：Garum? / Asellina（拉丁语）：Euge!")] },
  { id: "s5", background: "bg5", location: "熟食铺", time: "下午", purpose: "吃 garum", shots: [shot("st1", 9)] },
];
const frame = (scene: string, st: string, mtime = 1700000000123) =>
  ({ path: `${EP}/scenes/${scene}/shots/${st}/planning/${st}_first_frame.png`, mtime, prompt: `${EP}/scenes/${scene}/shots/${st}/planning/${st}_first_frame_prompt.txt` });
const fixture: EpisodeWorkflow = {
  episode_path: EP,
  shot_keys: { s1: { st1: "ep1_s1_st1", st2: "ep1_s1_st2" }, s8: { st1: "ep1_s8_st1", st2: "ep1_s8_st2" }, s5: { st1: "ep1_s5_st1" } },
  first_frames: {
    "ep1_s1_st1": frame("s1", "st1"),
    "ep1_s1_st2": { path: "", mtime: 0, prompt: "" },
    // 后端万一给了旧版或作废目录里的图，也不当现行首帧
    "ep1_s8_st2": { path: `${EP}/scenes/s8/shots/st2/planning/_r1/st2_first_frame.png`, mtime: 1, prompt: "" },
    "ep1_s8_st1": { path: `${EP}/scenes/s8/groups/g1/_obsolete/board.png`, mtime: 1, prompt: "" },
    "ep1_s5_st1": frame("s5", "st1", 1800000000000),
  },
  packs: { "ep1_s1_st1": { status: "ok", path: `${EP}/scenes/s1/shots/st1/资料包`, prompt: `${EP}/scenes/s1/shots/st1/资料包/prompt.txt`, reason: "", files: [] } },
  modules: [
    { id: "story", label: "故事创作", content: { brief: "方向", text: "正文" } },
    { id: "filming", label: "影视改编", content: { scenes } },
    { id: "prompts", label: "Prompt 编译", content: { scenes: [] } },
  ].map(module => ({ ...module, status: "approved", etag: "etag", revision: "r", input_revision: null, source_revision: null, can_edit: false })) as EpisodeWorkflow["modules"],
};
const run = (over: Partial<ReviewRunSummary>): ReviewRunSummary => ({
  dir: "ai_videos/demo/reviews/ep01_20261108-120012_pregen_r3", drama: "ai_videos/demo", drama_name: "demo", id: "x", title: "t", episode: "ep01",
  chain: "c", loop: 3, max_loops: 3, stage: "pregen", stage_name: "出片前", scenes: ["s1"], state: "进行中", created_at: "2026-11-08T12:00:12",
  done: 3, failed: 0, total: 8, totals: {}, ...over,
});

it("keeps the episode's scene order and each scene's shot order", () => {
  const board = storyboardScenes(fixture);
  expect(board.map(s => s.id)).toEqual(["s1", "s8", "s5"]);
  expect(board[1].shots.map(s => s.key)).toEqual(["ep1_s8_st2", "ep1_s8_st1"]);
  expect(board.map(s => s.total)).toEqual([19, 23, 9]);
});

it("only shows the current first frame — never _r* drafts, _obsolete boards or a missing image", () => {
  const shots = storyboardScenes(fixture).flatMap(s => s.shots);
  expect(shots.map(s => s.image?.path ?? null)).toEqual([frame("s1", "st1").path, null, null, null, frame("s5", "st1").path]);
  expect(isCurrentFirstFrame(`${EP}/scenes/s1/shots/st1/planning/_v2_old/st1_first_frame.png`, EP, "s1", "st1")).toBe(false);
  expect(isCurrentFirstFrame(`${EP}/scenes/s1/_obsolete/board/p01_st1.jpg`, EP, "s1", "st1")).toBe(false);
});

it("splits dialogue into speaker, direction and the full line", () => {
  expect(dialogueLines("Riley（问）：Garum? / Asellina（拉丁语，眼睛一亮）：Euge!")).toEqual([
    { speaker: "Riley", direction: "问", text: "Garum?" }, { speaker: "Asellina", direction: "拉丁语，眼睛一亮", text: "Euge!" }]);
  expect(dialogueLines("")).toEqual([]);
  expect(dialogueLines("Hello there.")).toEqual([{ speaker: "", direction: "", text: "Hello there." }]);
});

it("picks each scene's newest pre-generation review run", () => {
  const runs = [run({ loop: 2, state: "已完成", created_at: "2026-11-08T11:18:37" }), run({}),
    run({ stage: "full", scenes: ["s1", "s8"], created_at: "2026-11-09T00:00:00" }), run({ episode: "ep02", scenes: ["s8"] })];
  expect(reviewChipText(latestSceneReview(runs, "ai_videos/demo", "ep01", "s1"))).toBe("出片前审查 第 3/3 轮 · 进行中（3/8）");
  expect(reviewChipText(latestSceneReview([runs[0]], "ai_videos/demo", "ep01", "s1"))).toBe("出片前审查 第 2/3 轮 · 已完成");
  expect(reviewChipText(latestSceneReview(runs, "ai_videos/demo", "ep01", "s8"))).toBe("未审");
});

it("lays out the storyboard on the episode page: scenes in order, cards with frames, placeholders and review chips", async () => {
  vi.mocked(loadWorkflow).mockResolvedValue(fixture);
  vi.mocked(fetchReviewRuns).mockResolvedValue({ runs: [run({})] });
  render(<MemoryRouter initialEntries={["/drama?episode=ep01&module=filming"]}><EpisodeWorkflowPage dramaPath="ai_videos/demo" title="示例" /></MemoryRouter>);
  const board = await screen.findByRole("region", { name: "故事板" });
  const sections = within(board).getAllByRole("region", { name: /^场次 / });
  expect(sections.map(s => s.getAttribute("aria-label"))).toEqual(["场次 s1", "场次 s8", "场次 s5"]);

  const s1 = sections[0];
  expect(await within(s1).findByRole("link", { name: "出片前审查 第 3/3 轮 · 进行中（3/8）" }))
    .toHaveAttribute("href", expect.stringContaining(encodeURIComponent("reviews/ep01_20261108-120012_pregen_r3")));
  expect(within(sections[1]).getByText("未审")).toBeInTheDocument();
  expect(within(s1).getByText("19 秒")).toBeInTheDocument();
  expect(within(s1).getByText("2 镜")).toBeInTheDocument();

  const img = within(s1).getByAltText("s1_st1 首帧");
  expect(img.getAttribute("src")).toContain(encodeURIComponent(frame("s1", "st1").path));
  expect(img.getAttribute("src")).toContain("v=1700000000123");
  expect(within(s1).getByText("Okay… I just time-traveled.")).toBeInTheDocument();
  expect(within(s1).getByRole("link", { name: "资料包/prompt.txt" })).toBeInTheDocument();
  expect(within(s1).getByLabelText("s1_st2 首帧待出")).toHaveTextContent("首帧待出");
  expect(screen.getAllByText("首帧待出")).toHaveLength(3);
  for (const image of Array.from(board.querySelectorAll("img"))) expect(decodeURIComponent(image.getAttribute("src")!)).not.toMatch(/_obsolete|\/_r\d|_old\/|\/board\//);

  // 卡上只摘要行动，「展开」后看全文：行动、走位、动作分拍、拍摄
  const card = within(s1).getByRole("listitem", { name: "镜头 s1_st1" });
  expect(within(card).queryByText("st1 的拍法")).toBeNull();
  fireEvent.click(within(card).getByRole("button", { name: "展开" }));
  expect(within(card).getByText("st1 的拍法")).toBeInTheDocument();
  expect(within(card).getByText("st1 的分拍")).toBeInTheDocument();
});

it("narrows the storyboard to one scene and shows a shot's first frame on its own page", async () => {
  vi.mocked(loadWorkflow).mockResolvedValue(fixture);
  vi.mocked(fetchReviewRuns).mockResolvedValue({ runs: [] });
  render(<MemoryRouter initialEntries={["/drama?episode=ep01&module=filming&scene=s5"]}><EpisodeWorkflowPage dramaPath="ai_videos/demo" title="示例" /></MemoryRouter>);
  const board = await screen.findByRole("region", { name: "故事板" });
  expect(within(board).getAllByRole("region", { name: /^场次 / }).map(s => s.getAttribute("aria-label"))).toEqual(["场次 s5"]);
  cleanup();
  render(<MemoryRouter initialEntries={["/drama?episode=ep01&module=filming&scene=s1&shot=ep1_s1_st1"]}><EpisodeWorkflowPage dramaPath="ai_videos/demo" title="示例" /></MemoryRouter>);
  expect((await screen.findByAltText("ep1_s1_st1 首帧")).getAttribute("src")).toContain("v=1700000000123");
  expect(screen.queryByRole("region", { name: "故事板" })).toBeNull();
});
