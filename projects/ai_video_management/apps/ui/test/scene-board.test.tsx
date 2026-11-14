import { expect, it } from "vitest";
import { boardIndexPath, groupRuns, parseScenePath, scenePreviewHref, type ScenePanel } from "../src/lib/sceneBoard";

const panel = (shot: string, group: string | null, start: number, end: number): ScenePanel =>
  ({ shot, group, start, end, image: `${shot}.jpg`, text: "", action: "", dialogue: "", board: null, cell: 1 });

it("reads the scene from its folder and finds the board index (follow-up 336)", () => {
  const scene = "ai_videos/demo/episodes/ep01/scenes/s1";
  expect(parseScenePath(`${scene}/`)).toEqual({ episodePath: "ai_videos/demo/episodes/ep01", scene: "s1" });
  expect(parseScenePath(`${scene}/groups/g1`)).toBeNull();
  expect(boardIndexPath(scene)).toBe(`${scene}/board/scene_board.json`);
  expect(scenePreviewHref(scene)).toBe(`/scene-preview?path=${encodeURIComponent(scene)}`);
});

it("brackets consecutive panels of one group and keeps ungrouped shots apart", () => {
  const runs = groupRuns([panel("st1", "g1", 0, 8), panel("st2", "g1", 8, 16), panel("st3", null, 16, 20), panel("st4", null, 20, 24), panel("st5", "g2", 24, 30)]);
  expect(runs.map(r => [r.group, r.panels.map(p => p.shot)])).toEqual([
    ["g1", ["st1", "st2"]], [null, ["st3"]], [null, ["st4"]], ["g2", ["st5"]]]);
});
