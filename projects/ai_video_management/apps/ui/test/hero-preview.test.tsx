import { cleanup, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, expect, it, vi } from "vitest";
import { HeroPreviewPage } from "../src/components/HeroPreviewPage";
import { fetchSubtree } from "../src/api";
import { buildHeroPreview, heroPreviewHref } from "../src/lib/heroPreview";
import { resetDemoStatusForTest } from "../src/lib/demoStatus";
import type { TreeNode } from "../src/types";

vi.mock("../src/api", async original => ({ ...await original<typeof import("../src/api")>(), fetchSubtree: vi.fn() }));
vi.mock("../src/lib/fileEvents", () => ({ useFileChanges: vi.fn(), subscribeFileChanges: vi.fn(() => () => undefined) }));
afterEach(() => { cleanup(); vi.clearAllMocks(); vi.unstubAllGlobals(); resetDemoStatusForTest(); });

const root = "ai_videos/dota/chars/c75_Sand_King";
const f = (path: string, type: TreeNode["type"]): TreeNode => ({ type, name: path.split("/").pop()!, path: `${root}/${path}` });
const d = (path: string, children: TreeNode[]): TreeNode => ({ type: "directory", name: path.split("/").pop()!, path: `${root}/${path}`, children });
const k = "skills/k753_Caustic_Finale";
const tree: TreeNode = d("", [
  f("c75_Sand_King.md", "file"), f("c75_Sand_King.png", "image"), f("c75_Sand_King_v1.png", "image"), f("c75_Sand_King_turntable.mp4", "video"),
  d("_history", [f("_history/old.png", "image")]),
  d("source", [f("source/old_turntable.mp4", "video")]),
  d("views", [f("views/front.png", "image"), f("views/audio.mp3", "audio")]),
  d("skills", [d(k, [
    f(`${k}/k753_Caustic_Finale.md`, "file"), f(`${k}/k753_Caustic_Finale_peak.png`, "image"),
    d(`${k}/ref`, [f(`${k}/ref/frame.png`, "image")]),
    d(`${k}/planning`, [f(`${k}/planning/start_a.png`, "image"), f(`${k}/planning/start_b.png`, "image")]),
    d(`${k}/renders`, [
      d(`${k}/renders/.pending`, []),
      d(`${k}/renders/20261024-114849_aaa`, [f(`${k}/renders/20261024-114849_aaa/clip.mp4`, "video")]),
      d(`${k}/renders/20261027-181103_bbb`, [f(`${k}/renders/20261027-181103_bbb/sheet.jpg`, "image"), f(`${k}/renders/20261027-181103_bbb/clip.mp4`, "video"), f(`${k}/renders/20261027-181103_bbb/review.md`, "file")]),
    ]),
  ])]),
  d("demo", [f("demo/publish.md", "file"), d("demo/edit", [d("demo/edit/final", [f("demo/edit/final/v2.mp4", "video"), f("demo/edit/final/v3.mp4", "video")])])]),
]);
tree.name = "c75_Sand_King"; tree.path = root;

it("groups a hero folder into portrait, intro, skills with latest render first, and demo cuts", () => {
  const p = buildHeroPreview(tree);
  expect(p.portrait?.name).toBe("c75_Sand_King.png");
  expect(p.otherImages.map(i => i.name)).toEqual(["c75_Sand_King_v1.png"]);
  expect(p.intro.map(i => i.name)).toEqual(["c75_Sand_King_turntable.mp4", "audio.mp3"]);
  expect(p.views.map(i => i.name)).toEqual(["front.png"]);
  const [skill] = p.skills;
  expect(skill.card).toBe(`${root}/${k}/k753_Caustic_Finale.md`);
  expect(skill.latest?.name).toBe("20261027-181103_bbb");
  expect(skill.latest?.items[0].kind).toBe("video");
  expect(skill.latest?.review).toBe(`${root}/${k}/renders/20261027-181103_bbb/review.md`);
  expect(skill.history.map(h => h.name)).toEqual(["20261024-114849_aaa"]);
  expect(skill.images.map(i => i.name)).toEqual(["k753_Caustic_Finale_peak.png"]);
  expect(skill.planning.map(i => i.name)).toEqual(["start_b.png", "start_a.png"]);
  expect(p.demo.map(i => i.name)).toEqual(["v3.mp4", "v2.mp4"]);
  expect(p.demoNotes.map(i => i.name)).toEqual(["publish.md"]);
});

it("puts the newest final cut first even when review packs sit beside edit/ (follow-up 314)", () => {
  const demo = d("demo", [
    d("demo/review_168_20261024", [f("demo/review_168_20261024/k21.mp4", "video")]),
    d("demo/edit", [
      d("demo/edit/draft", [f("demo/edit/draft/ep01_draft_v5.mp4", "video")]),
      d("demo/edit/final", [f("demo/edit/final/ep01_final_v3.mp4", "video"), f("demo/edit/final/ep01_final_v10.mp4", "video"), f("demo/edit/final/ep01_final_v4.mp4", "video")]),
    ]),
  ]);
  const p = buildHeroPreview({ ...tree, children: [...tree.children!.filter(c => c.name !== "demo"), demo] });
  expect(p.demo.map(i => i.name)).toEqual(["ep01_final_v10.mp4", "ep01_final_v4.mp4", "ep01_final_v3.mp4", "ep01_draft_v5.mp4", "k21.mp4"]);
});

it("renders the page from the hero folder in the link", async () => {
  vi.mocked(fetchSubtree).mockResolvedValue(tree);
  render(<MemoryRouter initialEntries={[heroPreviewHref(root)]}><HeroPreviewPage /></MemoryRouter>);
  await screen.findByRole("heading", { name: "c75_Sand_King" });
  expect(fetchSubtree).toHaveBeenCalledWith(root, 0);
  expect(screen.getByText("最新 20261027-181103_bbb")).toBeTruthy();
  expect(screen.getByText("历史出片（1）")).toBeTruthy();
  expect(screen.getByText("拼图与测速图（1）")).toBeTruthy();
  expect(screen.getByRole("link", { name: "审稿记录" })).toBeTruthy();
  // Demo, intro and the skill's latest clip stay open; every image is folded.
  const open = [...document.querySelectorAll("video")].filter(v => !v.closest("details"));
  expect(open).toHaveLength(3);
  expect([...document.querySelectorAll("img")].every(i => i.closest("details"))).toBe(true);
});

it("marks a finalized demo and plays the finalized cut first, not the newest (follow-up 315)", async () => {
  vi.mocked(fetchSubtree).mockResolvedValue(tree);
  const status = {
    hero: root, folder: "c75_Sand_King", version: 2, cut: `${root}/demo/edit/final/cut_v2.json`,
    video: `${root}/demo/edit/final/v2.mp4`, status: "定版", newer: [3],
    publish: `${root}/demo/publish.md`, publish_video: "v2.mp4", publish_state: "ok",
  };
  vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify({ heroes: [status] }), { status: 200 })));
  render(<MemoryRouter initialEntries={[heroPreviewHref(root)]}><HeroPreviewPage /></MemoryRouter>);
  expect(await screen.findByText(/Demo 定版 v2 · 发布文案已就绪/)).toBeTruthy();
  expect(screen.getByRole("link", { name: "v2.mp4 · 定版 v2" })).toBeTruthy();
  expect(screen.getByText(/定版之后还有未定的剪辑 v3/)).toBeTruthy();
});
