/** Pure query model behind the 样本库 explorer: which rows survive the filter bar,
 * in what order, and where the "top decile" highlight starts. No React here so
 * the table component stays a rendering concern. */
import type { FlatVideo, VideoMark } from "../lib/researchApi";
import type { ExplorerFilters } from "./ResearchVideoExplorerToolbar";

export type SortKey =
  | "bookmark"
  | "title"
  | "series"
  | "views"
  | "likes"
  | "rate"
  | "date"
  | "duration"
  | "layout";

export type SortDir = "asc" | "desc";

export interface Column {
  key: SortKey;
  label: string;
  cls: string;
  descFirst: boolean;
}

export const COLUMNS: Column[] = [
  { key: "bookmark", label: "★", cls: "research-vx-star-cell", descFirst: true },
  { key: "title", label: "标题 / 频道", cls: "research-vx-title-cell", descFirst: false },
  { key: "series", label: "所属系列", cls: "", descFirst: false },
  { key: "views", label: "播放量", cls: "research-vx-num", descFirst: true },
  { key: "likes", label: "点赞", cls: "research-vx-num", descFirst: true },
  { key: "rate", label: "点赞率", cls: "research-vx-num", descFirst: true },
  { key: "date", label: "发布", cls: "research-vx-num", descFirst: true },
  { key: "duration", label: "时长", cls: "research-vx-num", descFirst: true },
  { key: "layout", label: "版式", cls: "", descFirst: true },
];

export interface ParsedFilters {
  query: string;
  series: Set<string>;
  minViews: number;
  minRate: number;
  from: string;
  to: string;
}

/** Text inputs are parsed once per keystroke, not once per row. */
export function parseFilters(f: ExplorerFilters): ParsedFilters {
  const rate = Number(f.minLikeRate);
  return {
    query: f.query.trim().toLowerCase(),
    series: new Set(f.series),
    minViews: f.minViews,
    minRate: f.minLikeRate.trim() !== "" && Number.isFinite(rate) ? rate / 100 : 0,
    from: f.from.replace(/-/g, ""),
    to: f.to.replace(/-/g, ""),
  };
}

/** `ignoreSeries` powers the per-series counts on the chips: each chip shows how
 * many rows it *would* add, which is only meaningful with itself left out. */
export function matches(
  v: FlatVideo,
  f: ExplorerFilters,
  p: ParsedFilters,
  marks: Record<string, VideoMark>,
  ignoreSeries: boolean,
): boolean {
  if (p.query && !`${v.title} ${v.channel}`.toLowerCase().includes(p.query)) return false;
  if (!ignoreSeries && p.series.size > 0 && !p.series.has(v.series_slug)) return false;
  if (f.layout === "vertical" && !v.vertical) return false;
  if (f.layout === "horizontal" && v.vertical) return false;
  if (f.bookmarkedOnly && marks[v.video_id]?.bookmarked !== true) return false;
  if (v.view_count < p.minViews) return false;
  if (v.like_rate < p.minRate) return false;
  if (p.from && v.upload_date < p.from) return false;
  if (p.to && v.upload_date > p.to) return false;
  return true;
}

/** Ascending comparator for one column; the caller flips it for descending. */
export function compareBy(
  a: FlatVideo,
  b: FlatVideo,
  key: SortKey,
  marks: Record<string, VideoMark>,
): number {
  switch (key) {
    case "bookmark":
      return (
        Number(marks[a.video_id]?.bookmarked === true) -
        Number(marks[b.video_id]?.bookmarked === true)
      );
    case "title":
      return a.title.localeCompare(b.title, "zh-Hans-CN");
    case "series":
      return a.series_rank - b.series_rank;
    case "views":
      return a.view_count - b.view_count;
    case "likes":
      return a.like_count - b.like_count;
    case "rate":
      return a.like_rate - b.like_rate;
    case "date":
      return a.upload_date.localeCompare(b.upload_date);
    case "duration":
      return a.duration - b.duration;
    case "layout":
      return Number(a.vertical) - Number(b.vertical);
  }
}

export function sortRows(
  rows: FlatVideo[],
  key: SortKey,
  dir: SortDir,
  marks: Record<string, VideoMark>,
): FlatVideo[] {
  const sorted = [...rows];
  sorted.sort((a, b) => {
    const c = compareBy(a, b, key, marks);
    return (dir === "asc" ? c : -c) || b.view_count - a.view_count;
  });
  return sorted;
}

/** Like-rate floor for "top decile of what is on screen". A decile is
 * meaningless on a handful of rows, so small sets get no highlight at all. */
export function topDecile(rates: number[]): number {
  if (rates.length < 8) return Number.POSITIVE_INFINITY;
  const sorted = [...rates].sort((x, y) => x - y);
  return sorted[Math.max(0, Math.ceil(sorted.length * 0.9) - 1)];
}
