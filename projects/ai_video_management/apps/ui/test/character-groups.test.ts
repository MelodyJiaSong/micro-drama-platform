import { describe, expect, it } from "vitest";
import { isCharacterVideoPath } from "../src/components/SiblingMedia";
import { characterFolders, characterGroups, extractDramas } from "../src/lib/dramas";
import type { TreeNode } from "../src/types";

const dir = (path: string, children: TreeNode[] = []): TreeNode => ({
  type: "directory",
  name: path.slice(path.lastIndexOf("/") + 1),
  path,
  children,
});

const CH = "ai_videos/demo/2_世界观人设/characters";

function drama(characters: TreeNode): TreeNode {
  return {
    type: "section",
    name: "root",
    path: "",
    children: [{ ...dir("ai_videos/demo", [dir("ai_videos/demo/2_世界观人设", [characters])]), is_drama: true }],
  };
}

describe("character folders (follow-up 284)", () => {
  it("lists flat cards as before", () => {
    const chars = dir(CH, [dir(`${CH}/c1_Aaron`), dir(`${CH}/m2_Wolf`)]);
    expect(characterFolders(chars).map((c) => [c.node.name, c.group])).toEqual([
      ["c1_Aaron", null],
      ["m2_Wolf", null],
    ]);
    expect(characterGroups(chars)).toEqual([]);
  });

  it("lists cards one group folder down, with their group", () => {
    const sentinel = dir(`${CH}/近卫_sentinel`, [dir(`${CH}/近卫_sentinel/c65_Axe`)]);
    const scourge = dir(`${CH}/天灾_scourge`, [dir(`${CH}/天灾_scourge/c8_Lich`)]);
    const chars = dir(CH, [sentinel, scourge]);
    expect(characterFolders(chars).map((c) => [c.node.name, c.group])).toEqual([
      ["c65_Axe", "近卫_sentinel"],
      ["c8_Lich", "天灾_scourge"],
    ]);
    expect(characterGroups(chars).map((g) => g.name)).toEqual(["近卫_sentinel", "天灾_scourge"]);
    expect(extractDramas(drama(chars))[0].characters).toEqual(["c65_Axe", "c8_Lich"]);
  });

  it("gates the view-extraction button on flat and grouped turntables only", () => {
    expect(isCharacterVideoPath(`${CH}/c1_Aaron/c1_Aaron_turntable.mp4`)).toBe(true);
    expect(isCharacterVideoPath(`${CH}/近卫_sentinel/c65_Axe/c65_Axe_turntable.mp4`)).toBe(true);
    expect(isCharacterVideoPath(`${CH}/c1_Aaron/c1-1_铠甲/clip.mp4`)).toBe(false);
    expect(isCharacterVideoPath(`${CH}/近卫_sentinel/clip.mp4`)).toBe(false);
  });
});
