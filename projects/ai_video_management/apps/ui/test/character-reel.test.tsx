import { act, cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, expect, it, vi } from "vitest";
import { CharacterReelPanel } from "../src/components/CharacterReelPanel";
import { characterCardDir, loadCharacterReel, type CharacterReel, type ReelClip, type SkillReel } from "../src/lib/characterReel";

vi.mock("../src/lib/characterReel", async importOriginal => ({ ...await importOriginal<typeof import("../src/lib/characterReel")>(), loadCharacterReel: vi.fn() }));
afterEach(() => { cleanup(); vi.clearAllMocks(); });

const DIR = "ai_videos/dota/2_世界观人设/characters/天灾_scourge/c65_Axe";
function clip(id: string, stage: ReelClip["stage"], credits: number | null = 120): ReelClip {
  return { id, video: `${DIR}/${id}/clip.mp4`, stage, submit_id: id.slice(-8), credits, generated_at: "2026-10-18T16:06:42",
    duration: 10, resolution: "", review_status: "" };
}
function skill(key: string, title: string, drafts: string[], final: boolean): SkillReel {
  const finals = final ? [clip(`20261018-202244_${key}final`, "final", 286)] : [];
  return { key, title, path: `${DIR}/skills/${key}_x`, card: "", icon: `${DIR}/skills/${key}_x/icon/${key}_icon_dota1.png`, peak: `${DIR}/skills/${key}_x/${key}_x_peak.png`,
    final: finals[0] ?? null, finals, drafts: drafts.map(id => clip(id, "draft")) };
}
const REEL: CharacterReel = {
  name: "c65_Axe", path: DIR, turntable: clip("c65_Axe_turntable.mp4", "turntable", null), watch: [DIR, "ai_videos/dota/episodes"],
  skills: [skill("k651", "狂战士的怒吼 · Berserker's Call", ["20261018-180942_16cf9c07", "20261018-160642_2008d025"], true),
    skill("k652", "战斗饥渴 · Battle Hunger", ["20261018-181133_eb10c118"], true),
    skill("k653", "反击螺旋 · Counter Helix", [], true), skill("k654", "淘汰之刃 · Culling Blade", [], true)],
  cuts: {
    draft: [2, 1].map(v => ({ version: v, stage: "draft" as const, episode: "ep01", path: `ai_videos/dota/episodes/ep01/edit/draft/cut_v${v}.json`,
      video: `ai_videos/dota/episodes/ep01/edit/draft/ep01_draft_v${v}.mp4`, duration: 56.32, note: `草稿第 ${v} 版`, status: "待用户看", phase: "初接", error: "", own: false })),
    final: [{ version: 1, stage: "final", episode: "ep01", path: "ai_videos/dota/episodes/ep01/edit/final/cut_v1.json", video: "",
      duration: null, note: "正片", status: "", phase: "", error: "", own: false }],
  },
};

async function panel(reel: CharacterReel): Promise<void> {
  vi.mocked(loadCharacterReel).mockResolvedValue(reel);
  await act(async () => { render(<MemoryRouter><CharacterReelPanel dir={DIR} /></MemoryRouter>); });
}

it("finds the card folder only for the card's own md", () => {
  expect(characterCardDir(`${DIR}/c65_Axe.md`)).toBe(DIR);
  expect(characterCardDir("ai_videos/hy/characters/c1_裴知秋/c1_裴知秋.md")).toBe("ai_videos/hy/characters/c1_裴知秋");
  expect(characterCardDir(`${DIR}/skills/k651_x/k651_x.md`)).toBeNull();
  expect(characterCardDir(`${DIR}/notes.md`)).toBeNull();
  expect(characterCardDir("ai_videos/dota/2_世界观人设/background/bg1_河道/bg1_河道.md")).toBeNull();
});

it("finals tab lists the character video plus each skill's newest final", async () => {
  await panel(REEL);
  expect(await screen.findByRole("tab", { name: "正片（5）" })).toHaveAttribute("aria-selected", "true");
  const finals = screen.getByRole("list", { name: "正片" });
  expect(within(finals).getAllByRole("listitem")).toHaveLength(5);
  expect(within(finals).getByLabelText("人物视频")).toBeInTheDocument();
  expect(within(finals).getByLabelText("k651 正片")).toBeInTheDocument();
  expect(within(finals).getByAltText("k651 图标")).toBeInTheDocument();
  expect(within(finals).getAllByText(/286 积分/)).toHaveLength(4);
  expect(within(finals).getAllByText("10.0 秒")).toHaveLength(5);
});

it("drafts tab groups every draft per skill, newest first, with the peak image", async () => {
  await panel(REEL);
  fireEvent.click(await screen.findByRole("tab", { name: "样片（3）" }));
  const q = screen.getByRole("region", { name: "k651 样片" });
  const videos = within(q).getAllByLabelText(/k651 草稿/);
  expect(videos.map(v => v.getAttribute("aria-label"))).toEqual(["k651 草稿 20261018-180942_16cf9c07", "k651 草稿 20261018-160642_2008d025"]);
  expect(within(q).getByText("2026-10-18 16:06 · 2008d025 · 120 积分")).toBeInTheDocument();
  expect(within(q).getByAltText("k651 峰值图")).toBeInTheDocument();
  expect(within(screen.getByRole("region", { name: "k653 样片" })).getByText("还没有草稿")).toBeInTheDocument();
});

it("cuts tab keeps draft and final cuts apart with note and render state", async () => {
  await panel(REEL);
  fireEvent.click(await screen.findByRole("tab", { name: "剪辑拼接（3）" }));
  const drafts = screen.getByRole("region", { name: "草稿剪辑" });
  expect(within(drafts).getAllByText(/^ep01 · v\d$/).map(n => n.textContent)).toEqual(["ep01 · v2", "ep01 · v1"]);
  expect(within(drafts).getByText("草稿第 2 版")).toBeInTheDocument();
  expect(within(drafts).getAllByText("初接 · 待用户看 · 56.3 秒")).toHaveLength(2);
  const finals = screen.getByRole("region", { name: "正片剪辑" });
  expect(within(finals).getByText("还没渲染")).toBeInTheDocument();
  expect(screen.getAllByRole("region").map(r => r.getAttribute("aria-label")).filter(n => n?.endsWith("剪辑"))).toEqual(["正片剪辑", "草稿剪辑"]);
});

it("cuts in the character's demo folder are labelled and listed first", async () => {
  const demo: CharacterReel["cuts"]["final"][number] = { version: 6, stage: "final", episode: "demo", path: `${DIR}/demo/edit/final/cut_v4.json`,
    video: `${DIR}/demo/edit/final/ep01_final_v6.mp4`, duration: 53.12, note: "第 6 版", status: "", phase: "", error: "", own: true };
  await panel({ ...REEL, cuts: { ...REEL.cuts, final: [demo, ...REEL.cuts.final] } });
  fireEvent.click(await screen.findByRole("tab", { name: "剪辑拼接（4）" }));
  const finals = screen.getByRole("region", { name: "正片剪辑" });
  expect(within(finals).getAllByText(/ · v\d$/).map(n => n.textContent)).toEqual(["人物 demo · v6", "ep01 · v1"]);
  expect(within(finals).getByLabelText("正片剪辑 v6")).toBeInTheDocument();
});

it("stays hidden for characters without skill videos", async () => {
  await panel({ ...REEL, skills: [skill("k1", "x", [], false)] });
  expect(loadCharacterReel).toHaveBeenCalledWith(DIR);
  expect(screen.queryByRole("region", { name: "样片与正片" })).toBeNull();
});
