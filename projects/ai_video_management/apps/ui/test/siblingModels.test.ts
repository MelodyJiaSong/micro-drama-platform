import { describe, expect, it } from "vitest";
import { findSubfolderModels } from "../src/components/SiblingMedia";
import { collectFilePaths } from "../src/lib/linkResolver";

const PROP = "ai_videos/shikong_lvxing/sk1/2_世界观人设/props/p19_独轮串车";
const MD = `${PROP}/p19_独轮串车.md`;

describe("findSubfolderModels", () => {
  it("pulls a whitemodel/ mesh up onto the prop card", () => {
    expect(
      findSubfolderModels(MD, [
        MD,
        `${PROP}/object.toml`,
        `${PROP}/whitemodel/raw.glb`,
        `${PROP}/whitemodel/peek_iso.png`,
      ]),
    ).toEqual([`${PROP}/whitemodel/raw.glb`]);
  });

  it("takes meshes from any subfolder name, not just whitemodel/", () => {
    const character = "ai_videos/xianjian_yi/_series/characters/c8_酒剑仙";
    expect(
      findSubfolderModels(`${character}/c8_酒剑仙.md`, [`${character}/model/model.glb`]),
    ).toEqual([`${character}/model/model.glb`]);
  });

  it("leaves the sections that already own a mesh alone", () => {
    // same folder → Folder media; renders/ → Renders; archive/ → Archived.
    expect(
      findSubfolderModels(MD, [
        `${PROP}/base.glb`,
        `${PROP}/renders/take3.glb`,
        `${PROP}/archive/old.glb`,
      ]),
    ).toEqual([]);
  });

  it("ignores non-mesh files and anything deeper than one level", () => {
    expect(
      findSubfolderModels(MD, [
        `${PROP}/whitemodel/p19_独轮串车.blend`,
        `${PROP}/whitemodel/angles/front/raw.glb`,
        "ai_videos/other_drama/props/p1_x/whitemodel/raw.glb",
      ]),
    ).toEqual([]);
  });
});

describe("collectFilePaths", () => {
  it("keeps model leaves — knownPaths is what every media lookup filters against", () => {
    const tree = {
      type: "directory",
      path: PROP,
      children: [
        { type: "file", path: MD, children: [] },
        {
          type: "directory",
          path: `${PROP}/whitemodel`,
          children: [{ type: "model", path: `${PROP}/whitemodel/raw.glb`, children: [] }],
        },
      ],
    };

    expect(collectFilePaths(tree)).toContain(`${PROP}/whitemodel/raw.glb`);
  });
});
