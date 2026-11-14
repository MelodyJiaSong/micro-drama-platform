import { expect, it } from "vitest";
import { groupFiles, groupPreviewHref, groupSpec, parseGroupPath, reviewStatus } from "../src/lib/groupPreview";
import type { TreeNode } from "../src/types";

const root = "ai_videos/demo/episodes/ep01/scenes/s1/groups/g2";
const f = (path: string, type: TreeNode["type"]): TreeNode => ({ type, name: path.split("/").pop()!, path: `${root}/${path}` });
const d = (path: string, children: TreeNode[]): TreeNode => ({ type: "directory", name: path.split("/").pop()!, path: `${root}/${path}`, children });

it("reads the group key from its folder (follow-up 331)", () => {
  expect(parseGroupPath(`${root}/`)).toEqual({ episodePath: "ai_videos/demo/episodes/ep01", episode: "ep01", scene: "s1", group: "g2", key: "ep1_s1_g2" });
  expect(parseGroupPath("ai_videos/demo/episodes/ep01/scenes/s1/shots/st2")).toBeNull();
  expect(groupPreviewHref(root)).toBe(`/group-preview?path=${encodeURIComponent(root)}`);
});

it("finds the board, newest take first across drafts and renders, and the pack", () => {
  const tree = d("", [
    f("board.png", "image"), f("board_v1.png", "image"),
    d("drafts", [d("drafts/.pending", []), d("drafts/20261102-100000_aaa", [f("drafts/20261102-100000_aaa/a.mp4", "video"), f("drafts/20261102-100000_aaa/review.md", "file")])]),
    d("renders", [d("renders/20261103-090000_bbb", [f("renders/20261103-090000_bbb/b.mp4", "video")])]),
    d("资料包", [f("资料包/prompt.txt", "file"), f("资料包/manifest.json", "file")]),
  ]);
  tree.path = root;
  const files = groupFiles(tree);
  expect(files.board?.name).toBe("board.png");
  expect(files.otherImages.map(i => i.name)).toEqual(["board_v1.png"]);
  expect(files.takes.map(t => [t.name, t.stage])).toEqual([["20261103-090000_bbb", "final"], ["20261102-100000_aaa", "draft"]]);
  expect(files.takes[1].review).toBe(`${root}/drafts/20261102-100000_aaa/review.md`);
  expect(files.packPrompt).toBe(`${root}/资料包/prompt.txt`);
  expect(files.packInvalid).toBeNull();
});

it("lays the member shots on one timeline and checks the compiled group matches filming", () => {
  const loc = parseGroupPath(root)!;
  const shot = (id: string, duration: number) => ({ id, duration, action: "a", blocking: "", beats: "b", camera: "c", lighting: "l", dialogue: "", cast: [] });
  const filming = { scenes: [{ id: "s1", location: "冰洞", time: "白天", purpose: "p", background: "bg1",
    shots: [shot("st1", 5), shot("st2", 8), shot("st3", 6)], groups: [{ id: "g2", shots: ["st2", "st3"] }] }] };
  const compiled = { id: "ep1_s1_g2", shots: ["ep1_s1_st2", "ep1_s1_st3"], text: "ep1_s1_g2", refs: [] };
  const spec = groupSpec(loc, filming, { scenes: [{ id: "s1", groups: [compiled] }] });
  expect(spec.members.map(m => [m.shot.id, m.start, m.end])).toEqual([["st2", 0, 8], ["st3", 8, 14]]);
  expect(spec.members[0].overhead).toBe("ai_videos/demo/episodes/ep01/scenes/s1/shots/st2/planning/st2_overhead.png");
  expect(spec.total).toBe(14);
  expect(spec.problem).toBeNull();
  expect(groupSpec(loc, filming, null).problem).toMatch("还没编译");
  expect(groupSpec(loc, filming, { scenes: [{ id: "s1", groups: [{ ...compiled, shots: ["ep1_s1_st2"] }] }] }).problem).toMatch("重新编译");
  expect(groupSpec({ ...loc, group: "g9" }, filming, null).problem).toMatch("没有镜组 g9");
});

it("reads the take status line", () => {
  expect(reviewStatus("# 审核\n\n状态：通过（用户）\n")).toBe("通过（用户）");
  expect(reviewStatus("")).toBe("");
});
