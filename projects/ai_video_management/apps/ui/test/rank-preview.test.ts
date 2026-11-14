import { describe, expect, it } from "vitest";
import { buildCuts, buildRankPreview, licenceClass, rankPreviewHref, repoRelative } from "../src/lib/rankPreview";

describe("rank preview (follow-up 317)", () => {
  it("classifies licences", () => {
    expect(licenceClass("Pexels License", undefined, true)).toBe("free");
    expect(licenceClass("CC BY-SA 2.0", undefined, true)).toBe("attribution");
    expect(licenceClass("CC BY-NC-SA 2.0", undefined, true)).toBe("risk");
    expect(licenceClass("Pexels License", "No commercial freedom of panorama", true)).toBe("risk");
    expect(licenceClass("AI-generated", undefined, true)).toBe("ai");
    expect(licenceClass("", undefined, false)).toBe("none");
  });

  it("builds tiles in rank order with repo paths and counts", () => {
    const dir = "ai_videos/paihangbang/episodes/ep01";
    const p = buildRankPreview(dir, { title: "T", kicker: "TOP 2", items: [
      { rank: 2, name: "B", image: "assets/img/b.jpg", image_credit: "x / CC BY 2.0", country_name: "C" },
      { rank: 1, name: "A", image: "assets/img/a.jpg", image_risk: "licence unknown", value_display: "828 m" },
    ] }, [{ file: "assets/img/b.jpg", licence: "CC BY 2.0", subject_check: "match: ok" }, { file: "assets/img/a.jpg", licence: "unknown" }]);
    expect(p.tiles.map(t => t.name)).toEqual(["A", "B"]);
    expect(p.tiles[1].image).toBe(`${dir}/assets/img/b.jpg`);
    expect(p.tiles[1].subjectCheck).toBe("match: ok");
    expect(p.counts).toMatchObject({ risk: 1, attribution: 1 });
  });

  const win = (...parts: string[]): string => parts.join(String.fromCharCode(92));   // Windows path from a manifest

  it("orders cuts full-version first and reads music ranges", () => {
    const cuts = buildCuts([
      { name: "ep_master.mp4", path: "r/ep_master.mp4" },
      { name: "ep_master_with-risk-images.mp4", path: "r/ep_master_with-risk-images.mp4" },
      { name: "thumbnail.png", path: "r/thumbnail.png" },
    ], new Map([["ep_master_with-risk-images.manifest.json", { duration_s: 321.6,
      inputs: { music: [{ path: win("C:", "w", "ai_videos", "x", "a.mp3"), in_s: 0, out_s: 180 }] } }]]));
    expect(cuts.map(c => c.label)).toEqual(["完整版（含待签字图）", "默认版（风险图扣下）"]);
    expect(cuts[0].music[0]).toEqual({ path: "ai_videos/x/a.mp3", range: "0.0–180.0 s" });
    expect(repoRelative(win("C:", "a", "ai_videos", "b.mp3"))).toBe("ai_videos/b.mp3");
    expect(rankPreviewHref("ai_videos/p")).toBe("/rank-preview?path=ai_videos%2Fp");
  });
});
