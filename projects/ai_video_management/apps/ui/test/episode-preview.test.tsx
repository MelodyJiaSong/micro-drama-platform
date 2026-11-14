import { expect, it } from "vitest";
import {
  episodePreviewHref, parseDialogue, parseEpisodePath, pickTake, shotAt, shotStart, takesFromTree, verdictFromStatus,
} from "../src/lib/episodePreview";
import type { CutVersion, EpisodeJoin } from "../src/lib/sceneCuts";
import type { TreeNode } from "../src/types";

const ep = "ai_videos/demo/episodes/ep01";

it("only accepts an episode folder (follow-up 326)", () => {
  expect(parseEpisodePath(`${ep}/`)).toEqual({ dramaPath: "ai_videos/demo", episode: "ep01" });
  expect(parseEpisodePath(`${ep}/scenes/s1`)).toBeNull();
  expect(episodePreviewHref(ep)).toBe(`/episode-preview?path=${encodeURIComponent(ep)}`);
});

it("splits dialogue by speaker, marks Latin lines and attaches glosses", () => {
  const lines = parseDialogue("Felix（拉丁语，洪亮带笑）：Salve! / Riley（学着说，美式英语）：Salve! / Riley：Okay.", { "Salve!": "你好！" });
  expect(lines.map(l => [l.who, l.foreign, l.gloss])).toEqual([["Felix", true, "你好！"], ["Riley", false, "你好！"], ["Riley", false, ""]]);
  expect(parseDialogue("")).toEqual([]);
});

it("reads the verdict off review.md's 状态 line", () => {
  expect(verdictFromStatus("已审核（保留）")).toBe("ok");
  expect(verdictFromStatus("已审核（保留，有备注）")).toBe("note");
  expect(verdictFromStatus("已审核（重出）")).toBe("redo");
  expect(verdictFromStatus("")).toBe("pending");
});

it("prefers the take the scene cut uses, else the newest take with a video", () => {
  const r = `${ep}/scenes/s1/shots/st3/renders`;
  const take = (name: string, files: string[]): TreeNode => ({ type: "directory", name, path: `${r}/${name}`,
    children: files.map(f => ({ type: f.endsWith(".mp4") ? "video" : "file", name: f, path: `${r}/${name}/${f}` }) as TreeNode) });
  const tree: TreeNode = { type: "directory", name: "renders", path: r, children: [
    take("20261106-231858_477425d8", ["a.mp4", "review.md"]), take("20261107-011606_2e74fd12", ["b.mp4", "review.md"]),
    take("20261107-020000_pending00", ["generation.json"]), { type: "directory", name: ".pending", path: `${r}/.pending`, children: [] }] };
  const takes = takesFromTree(tree);
  expect(takes.map(t => t.name)).toEqual(["20261107-011606_2e74fd12", "20261106-231858_477425d8"]);
  expect(pickTake(takes, null)?.video).toBe(`${r}/20261107-011606_2e74fd12/b.mp4`);
  expect(pickTake(takes, "20261106-231858_477425d8")?.review).toBe(`${r}/20261106-231858_477425d8/review.md`);
});

it("maps episode time to scene and shot through the scene cuts, dissolve overlap included", () => {
  const ev = (shot: string, start: number, duration: number) => ({ shot, start, duration }) as CutVersion["events"][number];
  const cuts = { s1: { events: [ev("st1", 0, 6), ev("st2", 6, 12)] }, s2: { events: [ev("st1", 0, 5)] } } as unknown as Record<string, CutVersion>;
  const join = { segments: [{ scene: "s1", cut_version: 1, start: 0, duration: 18 }, { scene: "s2", cut_version: 1, start: 17.25, duration: 5 }] } as EpisodeJoin;
  expect(shotAt(3, join, cuts)?.key).toBe("s1_st1");
  expect(shotAt(10, join, cuts)?.key).toBe("s1_st2");
  expect(shotAt(17.5, join, cuts)?.key).toBe("s2_st1");
  expect(shotStart("s1_st2", join, cuts)).toBe(6);
  expect(shotStart("s2_st1", join, cuts)).toBe(17.25);
  expect(shotAt(3, null, cuts)).toBeNull();
});

it("finds a shot's place inside its group take", async () => {
  const { groupOf } = await import("../src/lib/episodePreview");
  const scene = { id: "s1", shots: [{ id: "st1", duration: 8 }, { id: "st2", duration: 15 }, { id: "st4", duration: 10 }],
    groups: [{ id: "g1", shots: ["st1", "st2"] }] };
  expect(groupOf(scene, "st1")).toEqual({ id: "g1", offset: 0 });
  expect(groupOf(scene, "st2")).toEqual({ id: "g1", offset: 8 });
  expect(groupOf(scene, "st4")).toBeNull();
});

it("accepts suffixed episode folders and finds the film segment at a time (follow-up 328)", async () => {
  const { episodeNumber, filmIndexAt } = await import("../src/lib/episodePreview");
  const sfx = "ai_videos/zhenshi_chidu/episodes/ep01_largest_land_animals";
  expect(parseEpisodePath(sfx)).toEqual({ dramaPath: "ai_videos/zhenshi_chidu", episode: "ep01_largest_land_animals" });
  expect(parseEpisodePath("edu_videos/ai_terms/t01_overfitting")).toEqual({ dramaPath: "edu_videos/ai_terms", episode: "t01_overfitting" });
  expect(parseEpisodePath("edu_videos/ai_terms/_shared")).toBeNull();
  const { previewFile } = await import("../src/lib/episodePreview");
  expect(previewFile("edu_videos/ai_terms/t01_overfitting")).toBe("edu_videos/ai_terms/t01_overfitting/preview.json");
  expect(previewFile("edu_videos/ai_terms/t01_overfitting", "zh")).toBe("edu_videos/ai_terms/t01_overfitting/preview.json");
  expect(previewFile("edu_videos/ai_terms/t01_overfitting", "en")).toBe("edu_videos/ai_terms/t01_overfitting/preview.en.json");
  expect(previewFile("edu_videos/ai_terms/t01_overfitting", "../x")).toBe("edu_videos/ai_terms/t01_overfitting/preview.json");
  expect(episodeNumber("ep01_largest_land_animals")).toBe(1);
  expect(episodeNumber("ep12")).toBe(12);
  const items = [{ t: 0, end: 7, title: "hook" }, { t: 7, end: 14.5, title: "#30" }, { t: 14.5, end: 21, title: "#28" }];
  expect(filmIndexAt(0, items)).toBe(0);
  expect(filmIndexAt(7.2, items)).toBe(1);
  expect(filmIndexAt(30, items)).toBe(2);
  expect(filmIndexAt(-1, items)).toBe(-1);
});
