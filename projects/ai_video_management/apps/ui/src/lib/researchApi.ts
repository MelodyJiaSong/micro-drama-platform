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
}

export interface ResearchDatasetSummary {
  dataset: string;
  title: string;
  generated_at: string | null;
  window: { from: string; to: string } | null;
  series_count: number;
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
