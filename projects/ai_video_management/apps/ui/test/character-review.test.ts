import { expect, it } from "vitest";
import { characterReviewHref, isReviewPath, parseCharacterReview, statusTone } from "../src/lib/characterReview";

const dir = "ai_videos/demo/2_世界观人设/characters/c1_Riley";

it("links to the review page by character folder (follow-up 329)", () => {
  expect(characterReviewHref(dir)).toBe(`/character-review?path=${encodeURIComponent(dir)}`);
});

it("normalises review.json: kinds from extensions, drops broken items, flags duplicate ids", () => {
  const { review, problems } = parseCharacterReview({
    title: "Riley", character: "c1_Riley",
    sections: [
      { id: "V", title: "建立视频", layout: "wide", items: [{ id: "V1", label: "中英", path: `${dir}/c1_Riley_turntable.mp4` }] },
      { id: "E", title: "表情", items: [
        { id: "E01", label: "开心", path: `${dir}/expressions/a.png`, status: "要修" },
        { id: "E01", label: "重复", path: `${dir}/expressions/b.png` },
        { label: "缺编号", path: `${dir}/x.png` },
        { id: "A1", path: `${dir}/views/c1_Riley_audio.mp3` },
      ] },
    ],
  });
  expect(review?.sections.map(s => [s.id, s.layout, s.items.map(i => `${i.id}:${i.kind}`)])).toEqual([
    ["V", "wide", ["V1:video"]],
    ["E", "grid", ["E01:image", "E01:image", "A1:audio"]],
  ]);
  expect(review?.sections[1].items[2].label).toBe("A1");
  expect(problems).toEqual(["编号 E01 重复", "「表情」里有一项缺编号或路径"]);
});

it("rejects a file without sections and grades statuses", () => {
  expect(parseCharacterReview(null).review).toBeNull();
  expect(parseCharacterReview({ sections: [] }).problems).toEqual(["review.json 没有任何分区"]);
  expect(statusTone("通过（用户）")).toBe("ok");
  expect(statusTone("要修：嘴太大")).toBe("fix");
  expect(statusTone("待审")).toBe("pending");
  expect(statusTone()).toBe("pending");
});

it("accepts edu_videos folders as well as drama characters (follow-up 344)", () => {
  expect(isReviewPath(dir)).toBe(true);
  expect(isReviewPath("edu_videos/_shared/voice_lab")).toBe(true);
  expect(isReviewPath("specs/edu_video")).toBe(false);
  expect(isReviewPath("ai_videos")).toBe(false);
});
