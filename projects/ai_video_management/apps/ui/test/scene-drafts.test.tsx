import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, expect, it, vi } from "vitest";
import { EpisodeWorkflowPage } from "../src/components/EpisodeWorkflowPage";
import { judgeTake, loadWorkflow, type EpisodeWorkflow, type ShotTake } from "../src/lib/episodeWorkflow";

vi.mock("../src/lib/episodeWorkflow", async importOriginal => ({ ...await importOriginal<typeof import("../src/lib/episodeWorkflow")>(),
  loadWorkflow: vi.fn(), judgeTake: vi.fn() }));
afterEach(() => { cleanup(); vi.clearAllMocks(); });

const SHOT = (st: string) => `ai_videos/demo/episodes/ep01/scenes/s1/shots/${st}`;
const take = (st: string, id: string, stage: "draft" | "final", status = "待审核"): ShotTake => ({
  id, path: `${SHOT(st)}/${stage === "draft" ? "drafts" : "renders"}/${id}`, videos: [`${SHOT(st)}/${stage === "draft" ? "drafts" : "renders"}/${id}/ep1_s1_${st}_${id}.mp4`],
  review: "", review_path: "", review_status: status, generation: { stage, resolution: stage === "draft" ? "480p" : "720p" }, prompt_path: "" });
const fixture = {
  episode_path: "ai_videos/demo/episodes/ep01", shot_keys: { s1: { st1: "ep1_s1_st1", st2: "ep1_s1_st2", st3: "ep1_s1_st3" } },
  modules: [
    { id: "story", label: "故事创作", content: { brief: "方向", text: "正文" } },
    { id: "filming", label: "影视改编", content: { scenes: [{ id: "s1", location: "门前", time: "清晨", shots: [] }] } },
    { id: "prompts", label: "Prompt 编译", content: { scenes: [{ id: "s1", shots: ["st1", "st2", "st3"].map(st => ({ id: `ep1_s1_${st}`, text: `ep1_s1_${st}\n时长：6秒` })) }] } },
  ].map(module => ({ ...module, status: "approved", etag: "e", revision: "r", input_revision: null, source_revision: null, can_edit: false })),
  renders: {
    // 最新在前：st1 有一条正式条和两条草稿，草稿 tab 只看最新一条草稿
    ep1_s1_st1: [take("st1", "20261016-230000_ffff0003", "final"), take("st1", "20261016-220000_bbbb0002", "draft", "通过（用户 2026-10-16 22:30，可出正式条）"),
      take("st1", "20261016-210000_aaaa0001", "draft")],
    ep1_s1_st3: [take("st3", "20261016-213000_cccc0003", "draft")],
  },
} as unknown as EpisodeWorkflow;

function page(query: string): void {
  vi.mocked(loadWorkflow).mockResolvedValue(fixture);
  render(<MemoryRouter initialEntries={[`/drama?episode=ep01&module=prompts&${query}`]}><EpisodeWorkflowPage dramaPath="ai_videos/demo" title="示例" /></MemoryRouter>);
}

it("the scene page switches to a drafts tab with one tile per shot in shot order", async () => {
  page("scene=s1");
  fireEvent.click(await screen.findByRole("tab", { name: "草稿" }));
  const grid = await screen.findByRole("list", { name: "s1 草稿" });
  const tiles = within(grid).getAllByRole("listitem");
  expect(tiles.map(tile => tile.getAttribute("data-shot"))).toEqual(["ep1_s1_st1", "ep1_s1_st2", "ep1_s1_st3"]);
  const thumb = tiles[0].querySelector("video")!;
  expect(thumb.getAttribute("src")).toContain(encodeURIComponent("20261016-220000_bbbb0002"));   // 最新一条草稿，不是正式条
  expect(thumb.muted).toBe(true);
  expect(thumb.hasAttribute("controls")).toBe(false);
  expect(tiles[0]).toHaveTextContent("2 条草稿");
  expect(tiles[0]).toHaveTextContent("通过");
  expect(tiles[1]).toHaveTextContent("还没有草稿");
  expect(tiles[1].querySelector("video")).toBeNull();
  expect(screen.getByText("3 镜 · 2 镜有草稿")).toBeInTheDocument();
});

it("a tile opens an enlarged preview that steps between drafts and closes on Escape", async () => {
  vi.mocked(judgeTake).mockResolvedValue({ review_status: "不通过（用户）" });
  page("scene=s1&tab=drafts");
  const grid = await screen.findByRole("list", { name: "s1 草稿" });
  fireEvent.click(within(grid).getAllByRole("button", { name: /放大/ })[0]);
  const dialog = screen.getByRole("dialog", { name: "草稿预览 ep1_s1_st1" });
  const player = within(dialog).getByLabelText("放大的草稿") as HTMLVideoElement;
  expect(player.hasAttribute("controls")).toBe(true);
  expect(within(dialog).getByRole("link", { name: "打开镜头页" })).toHaveAttribute("href", expect.stringContaining("shot=ep1_s1_st1"));
  fireEvent.keyDown(dialog, { key: "ArrowRight" });   // st2 没有草稿，跳到 st3
  expect(screen.getByRole("dialog", { name: "草稿预览 ep1_s1_st3" })).toBeInTheDocument();
  fireEvent.click(within(screen.getByRole("dialog")).getByRole("button", { name: "不通过" }));
  expect(vi.mocked(judgeTake)).toHaveBeenCalledWith(`${SHOT("st3")}/drafts/20261016-213000_cccc0003`, "不通过");
  fireEvent.keyDown(screen.getByRole("dialog"), { key: "Escape" });
  expect(screen.queryByRole("dialog")).toBeNull();
});

it("the 正片 tab shows each shot's latest final take, and judges it for the cut", async () => {
  page("scene=s1&tab=finals");
  const grid = await screen.findByRole("list", { name: "s1 正片" });
  const tiles = within(grid).getAllByRole("listitem");
  expect(tiles.map(tile => tile.getAttribute("data-shot"))).toEqual(["ep1_s1_st1", "ep1_s1_st2", "ep1_s1_st3"]);
  expect(tiles[0].querySelector("video")?.getAttribute("src")).toContain("20261016-230000_ffff0003");
  expect(within(tiles[2]).getByText("还没有正片")).toBeInTheDocument();
  vi.mocked(judgeTake).mockResolvedValue({ review_status: "通过（用户，正片可用）" });
  fireEvent.click(within(tiles[0]).getByRole("button", { name: "放大 ep1_s1_st1" }));
  const dialog = await screen.findByRole("dialog", { name: "正片预览 ep1_s1_st1" });
  fireEvent.click(within(dialog).getByRole("button", { name: "通过" }));
  expect(judgeTake).toHaveBeenCalledWith(`${SHOT("st1")}/renders/20261016-230000_ffff0003`, "通过");
});
