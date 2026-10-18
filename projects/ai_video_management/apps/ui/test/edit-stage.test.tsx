import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, expect, it, vi } from "vitest";
import { EditStagePanel } from "../src/components/EditStagePanel";
import { EpisodeWorkflowPage } from "../src/components/EpisodeWorkflowPage";
import { loadWorkflow } from "../src/lib/episodeWorkflow";
import { loadSceneCuts, type CutVersion, type EpisodeCuts, type EpisodeJoin } from "../src/lib/sceneCuts";

vi.mock("../src/lib/sceneCuts", async importOriginal => ({ ...await importOriginal<typeof import("../src/lib/sceneCuts")>(), loadSceneCuts: vi.fn() }));
vi.mock("../src/lib/episodeWorkflow", async importOriginal => ({ ...await importOriginal<typeof import("../src/lib/episodeWorkflow")>(), loadWorkflow: vi.fn() }));
afterEach(() => { cleanup(); vi.clearAllMocks(); });
HTMLMediaElement.prototype.play = vi.fn().mockResolvedValue(undefined);   // jsdom 没有实现播放

const EP = "ai_videos/demo/episodes/ep01";
const DIR = `${EP}/scenes/s1/edit/draft`;
function version(n: number, extra: Partial<CutVersion> = {}): CutVersion {
  return {
    version: n, stage: "draft", phase: "粗剪", status: "草稿", path: `${DIR}/cut_v${n}.json`, approved_by: null, made_by: "代理",
    base_version: n - 1, video: `${DIR}/s1_draft_v${n}.mp4`, labeled_video: `${DIR}/s1_draft_v${n}_标注.mp4`, duration: 12, rendered_at: "2026-10-17T10:00:00",
    shots: 1, placeholders: 1, notes: ["只为看片"], violations: [{ shot: "st1", what: "米莉在门里", why: "三轮上限" }], error: "",
    events: [
      { shot: "st1", start: 0, duration: 5, placeholder: false, take: "20261016-230627_b1c10a24", cut_in: 0, cut_out: 5, audio_in: 0, audio_out: 6,
        reason: "建立", notes: ["L 剪辑"], text: [] },
      { shot: "st2", start: 5, duration: 7, placeholder: true, take: "", cut_in: null, cut_out: null, audio_in: null, audio_out: null,
        reason: "草稿未生成", notes: [], text: ["台词：Hello"] },
    ],
    ...extra,
  };
}
const CUTS: EpisodeCuts = { episode_path: EP, scenes: [
  { scene: "s1", label: "门前 · 白天", draft: [version(2), version(1, { duration: 15 })], final: [] },
  { scene: "s2", label: "路上 · 清晨", draft: [], final: [] },
], joined: { draft: [], final: [] }, galleries: { draft: [], final: [] } };

function panel(search: string): void {
  render(<MemoryRouter initialEntries={[`/drama${search}`]}><EditStagePanel episodePath={EP} refresh={0} /></MemoryRouter>);
}

it("lists scenes per stage and keeps draft and final cuts apart", async () => {
  vi.mocked(loadSceneCuts).mockResolvedValue(CUTS);
  panel("?module=edit");
  const scenes = await screen.findByRole("list", { name: "场次" });
  const items = within(scenes).getAllByRole("listitem");
  expect(items[0]).toHaveTextContent("v2 · 粗剪 · 12.0 秒 · 缺镜 1");
  expect(items[1]).toHaveTextContent("还没有草稿剪辑");
  expect(screen.getByRole("tab", { name: "草稿剪辑（1 场）" })).toHaveAttribute("aria-selected", "true");
  fireEvent.click(screen.getByRole("tab", { name: "正片剪辑（0 场）" }));
  expect(within(screen.getByRole("list", { name: "场次" })).getAllByRole("listitem")[0]).toHaveTextContent("还没有正片剪辑");
  expect(vi.mocked(loadSceneCuts)).toHaveBeenCalledWith(EP);
});

it("plays the newest version of a scene, switches versions and jumps from the timeline", async () => {
  vi.mocked(loadSceneCuts).mockResolvedValue(CUTS);
  panel("?module=edit&scene=s1");
  const video = await screen.findByLabelText("剪辑成片") as HTMLVideoElement;
  expect(video.getAttribute("src")).toContain(encodeURIComponent(`${DIR}/s1_draft_v2.mp4`));
  fireEvent.click(screen.getByRole("button", { name: "标注版（镜号 · 条 · 入出点）" }));
  expect((screen.getByLabelText("剪辑成片") as HTMLVideoElement).getAttribute("src")).toContain(encodeURIComponent(`${DIR}/s1_draft_v2_标注.mp4`));
  const rows = within(screen.getByRole("table", { name: "时间线" })).getAllByRole("row");
  expect(rows[1]).toHaveTextContent("声 0.00–6.00");
  expect(rows[2]).toHaveTextContent("缺镜占位");
  expect(rows[2]).toHaveTextContent("台词：Hello");
  fireEvent.click(within(rows[2]).getByRole("button", { name: "0:05.0" }));
  expect((screen.getByLabelText("剪辑成片") as HTMLVideoElement).currentTime).toBeCloseTo(5.01);
  expect(screen.getByRole("region", { name: "有意违例" })).toHaveTextContent("st1：米莉在门里 —— 三轮上限");
  fireEvent.click(screen.getByRole("link", { name: "v1" }));
  expect(await screen.findByText(/15\.0 秒/)).toBeInTheDocument();
});

it("says the final cut waits for approved final takes", async () => {
  vi.mocked(loadSceneCuts).mockResolvedValue(CUTS);
  panel("?module=edit&scene=s1&cut=final");
  expect(await screen.findByText(/还没有正片剪辑：等各镜草稿标了「通过」/)).toBeInTheDocument();
});

it("replaces the edit placeholder on the episode page", async () => {
  vi.mocked(loadSceneCuts).mockResolvedValue(CUTS);
  vi.mocked(loadWorkflow).mockResolvedValue({ episode_path: EP, modules: [], shot_keys: {} } as never);
  render(<MemoryRouter initialEntries={["/drama?module=edit&episode=ep01"]}><EpisodeWorkflowPage dramaPath="ai_videos/demo" title="Demo" /></MemoryRouter>);
  expect(await screen.findByRole("region", { name: "剪辑" })).toBeInTheDocument();
  expect(screen.queryByText("待设计")).not.toBeInTheDocument();
});

const EDIR = `${EP}/edit/final`;
function joined(n: number, extra: Partial<EpisodeJoin> = {}): EpisodeJoin {
  return {
    version: n, stage: "final", phase: "锁片", status: "草稿（待用户批准锁片）", path: `${EDIR}/cut_v${n}.json`, approved_by: null, base_version: n - 1,
    video: `${EDIR}/ep01_final_v${n}.mp4`, duration: 37.6, rendered_at: "2026-10-18T09:30:00", head: "切", tail: "切",
    segments: [{ scene: "s1", cut_version: 3, start: 0, duration: 28 }, { scene: "s2", cut_version: 3, start: 28, duration: 9.6 }],
    transitions: [{ from_scene: "s1", to_scene: "s2", type: "cut", name: "切", duration: 0, at: 28, audio_j: 0.75, audio_l: null, reason: "同一时刻" }],
    review_verdict: "可锁片", review_stale: false, review_items: ["调色压黑位"], changes: ["s2 换条"], note: "", error: "", ...extra,
  };
}

it("shows the whole episode with its transitions, review and the transition gallery", async () => {
  vi.mocked(loadSceneCuts).mockResolvedValue({ ...CUTS, joined: { draft: [], final: [joined(2), joined(1, { review_stale: true, review_verdict: "" })] },
    galleries: { draft: [], final: [{ from_scene: "s1", to_scene: "s2", video: `${EDIR}/转场样片_s1_s2.mp4`,
      entries: [{ start: 0, label: "切 cut" }, { start: 16.5, label: "叠化 dissolve 1.0s" }] }] } });
  panel("?module=edit&cut=final");
  const first = within(await screen.findByRole("list", { name: "场次" })).getAllByRole("listitem")[0];
  expect(first).toHaveTextContent("整集 · 场与场接起来、转场");
  expect(first).toHaveTextContent("v2 · 锁片 · 37.6 秒 · 转场样片 1 条");
  fireEvent.click(within(first).getByRole("link"));
  const video = await screen.findByLabelText("整集成片") as HTMLVideoElement;
  expect(video.getAttribute("src")).toContain(encodeURIComponent(`${EDIR}/ep01_final_v2.mp4`));
  expect(screen.getByRole("region", { name: "独立审稿" })).toHaveTextContent("可锁片");
  const rows = within(screen.getByRole("table", { name: "各场与转场" })).getAllByRole("row");
  expect(rows[2]).toHaveTextContent("转场 · 切 cut");
  expect(rows[2]).toHaveTextContent("J：下一场声音提前 0.75 秒");
  fireEvent.click(within(rows[2]).getByRole("button", { name: "0:26.5" }));
  expect(video.currentTime).toBeCloseTo(26.51);
  expect(within(rows[3]).getByRole("link", { name: "s2" }).getAttribute("href")).toContain("scene=s2&v=3");
  const gallery = screen.getByLabelText("转场样片") as HTMLVideoElement;
  fireEvent.click(screen.getByRole("button", { name: "0:16.5" }));
  expect(gallery.currentTime).toBeCloseTo(16.51);
  fireEvent.click(screen.getByRole("link", { name: "v1" }));
  expect(await screen.findByText("审稿结论审的是另一版成片，这一版还没审。")).toBeInTheDocument();
});
