import { describe, expect, it } from "vitest";
import {
  formatCount,
  formatDate,
  formatDuration,
  formatRate,
  sortSeries,
  type ResearchSeries,
} from "../src/lib/researchApi";

function series(
  slug: string,
  rank: number,
  medianViews: number,
  medianLikeRate: number,
  score: number,
): ResearchSeries {
  return {
    rank,
    slug,
    name_zh: slug,
    name_en: slug,
    description: "",
    why_it_works: "",
    orientation: "shorts",
    market: "English",
    typical_length: "60s",
    stats: {
      videos: 10,
      total_views: medianViews * 10,
      median_views: medianViews,
      max_views: medianViews * 2,
      median_like_rate: medianLikeRate,
    },
    replication: { score, hours_per_episode: "4h", tools: [], stack_fit: "", blockers: "", how_to: [] },
    risk: "",
    monetization: "",
    verdict: "",
    videos: [],
  };
}

const SET: ResearchSeries[] = [
  series("b", 2, 5_000_000, 0.01, 5),
  series("a", 1, 1_000_000, 0.04, 3),
  series("c", 3, 9_000_000, 0.02, 4),
];

describe("sortSeries", () => {
  it("balanced follows the curated rank, not any single metric", () => {
    expect(sortSeries(SET, "balanced").map((s) => s.slug)).toEqual(["a", "b", "c"]);
  });

  it("views sorts by median views descending", () => {
    expect(sortSeries(SET, "views").map((s) => s.slug)).toEqual(["c", "b", "a"]);
  });

  it("like_rate can disagree with views — that is the point of having both", () => {
    expect(sortSeries(SET, "like_rate").map((s) => s.slug)).toEqual(["a", "c", "b"]);
  });

  it("replication sorts by score, breaking ties on rank", () => {
    expect(sortSeries(SET, "replication").map((s) => s.slug)).toEqual(["b", "c", "a"]);
  });

  it("does not mutate the input array", () => {
    const before = SET.map((s) => s.slug);
    sortSeries(SET, "views");
    expect(SET.map((s) => s.slug)).toEqual(before);
  });
});

describe("formatters", () => {
  it("scales counts to 万 and 亿", () => {
    expect(formatCount(842)).toBe("842");
    expect(formatCount(41_329_312)).toBe("4132.9万");
    expect(formatCount(120_000_000)).toBe("1.2亿");
  });

  it("renders like-rate as a percentage with two decimals", () => {
    expect(formatRate(0.0137)).toBe("1.37%");
    expect(formatRate(0.0006)).toBe("0.06%");
  });

  it("renders yyyymmdd upload dates, passing anything else through", () => {
    expect(formatDate("20260412")).toBe("2026-04-12");
    expect(formatDate("unverified")).toBe("unverified");
  });

  it("renders durations in 分/秒", () => {
    expect(formatDuration(45)).toBe("45秒");
    expect(formatDuration(571)).toBe("9分31秒");
    expect(formatDuration(0)).toBe("—");
  });
});
