/** API client + types for the 调研 (research) module — ranked content-series
 * datasets under `ai_videos/_research/`. Read-only: every metric here was
 * measured offline by tools/yt_research.py, so the UI never re-derives one. */

export interface ResearchVideo {
  video_id: string;
  title: string;
  channel: string;
  channel_url?: string;
  url: string;
  upload_date: string;
  view_count: number;
  like_count: number;
  like_rate: number;
  duration: number;
  vertical: boolean;
  note?: string;
}

export interface ResearchStats {
  videos: number;
  total_views: number;
  median_views: number;
  max_views: number;
  median_like_rate: number;
}

export interface ResearchReplication {
  score: number;
  hours_per_episode: string;
  tools: string[];
  stack_fit: string;
  blockers: string;
  how_to: string[];
}

export interface RevenueScenario {
  views_6mo: number;
  subs_estimate: number;
  watch_hours_estimate: number;
  /** Month the YPP gate clears, or null if it never does inside 6 months. */
  ypp_cleared_month: number | null;
  monetized_views: number;
  adsense_usd_low: number;
  adsense_usd_high: number;
  reaches_payout_floor: boolean;
}

export interface ResearchRevenue {
  market_key: string;
  market_label: string;
  rpm_low: number;
  rpm_high: number;
  sustainable_uploads_per_month: number;
  median_duration_sec: number;
  assumptions: {
    views_per_sub: number;
    retention: number;
    ypp_subs: number;
    ypp_watch_hours: number;
    review_lag_months: number;
    payout_floor_usd: number;
    ramp_share_by_month: number[];
  };
  scenarios: { low: RevenueScenario; mid: RevenueScenario; high: RevenueScenario };
  views_basis: string;
  rpm_basis: string;
  ad_friendliness: string;
  off_adsense_6mo: string;
  confidence: string;
  new_channels_measured: number;
}

export interface ResearchSeries {
  rank: number;
  slug: string;
  name_zh: string;
  name_en: string;
  description: string;
  why_it_works: string;
  orientation: string;
  market: string;
  typical_length: string;
  stats: ResearchStats;
  replication: ResearchReplication;
  risk: string;
  monetization: string;
  verdict: string;
  videos: ResearchVideo[];
  /** 6-month solo revenue projection; absent on datasets generated before it existed. */
  revenue?: ResearchRevenue;
}

export interface ResearchDataset {
  schema_version: number;
  title: string;
  generated_at: string;
  window: { from: string; to: string };
  method: string;
  criteria: string[];
  series: ResearchSeries[];
  rejected?: string[];
  caveats?: string[];
  revenue_gate?: string;
  revenue_caveats?: string;
}

export interface ResearchSeriesRef {
  slug: string;
  name_zh: string;
  rank: number;
}

export interface ResearchDatasetSummary {
  dataset: string;
  title: string;
  /** Nav grouping, e.g. 调研结果. */
  group?: string;
  /** Month key, e.g. 2026-09 — datasets are one file per month. */
  month?: string;
  generated_at: string | null;
  window: { from: string; to: string } | null;
  series_count: number;
  /** Enough of each series to build the sidebar without fetching the whole dataset. */
  series?: ResearchSeriesRef[];
}

const GET_OPTS: RequestInit = {
  method: "GET",
  headers: { Accept: "application/json" },
  cache: "no-store",
};

async function researchJson<T>(response: Response): Promise<T> {
  const text = await response.text();
  if (!response.ok) {
    let message = `HTTP ${response.status}`;
    try {
      const parsed = JSON.parse(text) as { detail?: { message?: string; kind?: string } };
      message = parsed.detail?.message ?? parsed.detail?.kind ?? message;
    } catch {
      // body wasn't JSON
    }
    throw new Error(message);
  }
  return JSON.parse(text) as T;
}

export async function fetchResearchDatasets(): Promise<{ datasets: ResearchDatasetSummary[] }> {
  return researchJson(await fetch("/api/research/datasets", GET_OPTS));
}

export async function fetchResearchDataset(dataset: string): Promise<ResearchDataset> {
  return researchJson(await fetch(`/api/research/dataset/${encodeURIComponent(dataset)}`, GET_OPTS));
}

/** Sort keys the series list exposes. `balanced` is the default because the
 * brief weighs return AND replicability — sorting by either alone hides the
 * series that are merely easy or merely popular. */
export type ResearchSort = "balanced" | "views" | "like_rate" | "replication";

export function sortSeries(series: ResearchSeries[], key: ResearchSort): ResearchSeries[] {
  const copy = [...series];
  if (key === "balanced") return copy.sort((a, b) => a.rank - b.rank);
  if (key === "views") return copy.sort((a, b) => b.stats.median_views - a.stats.median_views);
  if (key === "like_rate") return copy.sort((a, b) => b.stats.median_like_rate - a.stats.median_like_rate);
  return copy.sort((a, b) => b.replication.score - a.replication.score || a.rank - b.rank);
}

export function formatCount(n: number): string {
  if (!Number.isFinite(n)) return "—";
  if (n >= 100_000_000) return `${(n / 100_000_000).toFixed(1)}亿`;
  if (n >= 10_000) return `${(n / 10_000).toFixed(1)}万`;
  return String(n);
}

export function formatRate(rate: number): string {
  return Number.isFinite(rate) ? `${(rate * 100).toFixed(2)}%` : "—";
}

export function formatDate(yyyymmdd: string): string {
  return /^\d{8}$/.test(yyyymmdd)
    ? `${yyyymmdd.slice(0, 4)}-${yyyymmdd.slice(4, 6)}-${yyyymmdd.slice(6, 8)}`
    : yyyymmdd;
}

export function formatDuration(seconds: number): string {
  if (!Number.isFinite(seconds) || seconds <= 0) return "—";
  const m = Math.floor(seconds / 60);
  const s = Math.round(seconds % 60);
  return m > 0 ? `${m}分${String(s).padStart(2, "0")}秒` : `${s}秒`;
}

/* ---------------- workspace: the user's decisions, persisted server-side ---------------- */

export type SeriesStatus = "none" | "shortlist" | "doing" | "rejected";

export const STATUS_LABEL: Record<SeriesStatus, string> = {
  none: "未定",
  shortlist: "短名单",
  doing: "在做",
  rejected: "已弃",
};

export const STATUS_ORDER: SeriesStatus[] = ["none", "shortlist", "doing", "rejected"];

export interface SeriesMark {
  status?: SeriesStatus;
  rating?: number;
  note?: string;
}

export interface VideoMark {
  bookmarked?: boolean;
  note?: string;
}

export interface ResearchWorkspace {
  dataset: string;
  series: Record<string, SeriesMark>;
  videos: Record<string, VideoMark>;
}

async function put<T>(url: string, body: unknown): Promise<T> {
  const response = await fetch(url, {
    method: "PUT",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify(body),
  });
  return researchJson<T>(response);
}

export async function fetchWorkspace(dataset: string): Promise<ResearchWorkspace> {
  return researchJson(
    await fetch(`/api/research/dataset/${encodeURIComponent(dataset)}/workspace`, GET_OPTS),
  );
}

export async function markSeries(
  dataset: string,
  slug: string,
  patch: SeriesMark,
): Promise<ResearchWorkspace> {
  return put(
    `/api/research/dataset/${encodeURIComponent(dataset)}/series/${encodeURIComponent(slug)}/mark`,
    patch,
  );
}

export async function markVideo(
  dataset: string,
  videoId: string,
  patch: VideoMark,
): Promise<ResearchWorkspace> {
  return put(
    `/api/research/dataset/${encodeURIComponent(dataset)}/video/${encodeURIComponent(videoId)}/mark`,
    patch,
  );
}

/* ---------------- derived views ---------------- */

/** One row per video, flattened across series — the shape the sample explorer needs. */
export interface FlatVideo extends ResearchVideo {
  series_slug: string;
  series_name: string;
  series_rank: number;
}

export function flattenVideos(data: ResearchDataset): FlatVideo[] {
  return data.series.flatMap((s) =>
    s.videos.map((v) => ({
      ...v,
      series_slug: s.slug,
      series_name: s.name_zh,
      series_rank: s.rank,
    })),
  );
}

/** Median of a numeric list; 0 for an empty list. */
export function median(values: number[]): number {
  if (values.length === 0) return 0;
  const sorted = [...values].sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 === 0 ? (sorted[mid - 1] + sorted[mid]) / 2 : sorted[mid];
}

/** The two thresholds the brief implies: a series must clear BOTH to be a real
 * candidate. Derived from the dataset itself (its own medians) rather than
 * hardcoded, so they stay meaningful when the research is re-run. */
export interface Thresholds {
  views: number;
  likeRate: number;
}

export function thresholds(data: ResearchDataset): Thresholds {
  return {
    views: median(data.series.map((s) => s.stats.median_views)),
    likeRate: median(data.series.map((s) => s.stats.median_like_rate)),
  };
}

export type Quadrant = "both" | "views_only" | "likes_only" | "neither";

export function quadrantOf(s: ResearchSeries, t: Thresholds): Quadrant {
  const v = s.stats.median_views >= t.views;
  const l = s.stats.median_like_rate >= t.likeRate;
  if (v && l) return "both";
  if (v) return "views_only";
  if (l) return "likes_only";
  return "neither";
}

export const QUADRANT_LABEL: Record<Quadrant, string> = {
  both: "两项都过",
  views_only: "只有播放",
  likes_only: "只有点赞率",
  neither: "两项都不过",
};

export function formatUsd(n: number): string {
  if (!Number.isFinite(n)) return "—";
  return n >= 1000 ? `$${(n / 1000).toFixed(1)}k` : `$${Math.round(n)}`;
}
