import { ApiError } from "../types";

/** 整集审片串联（follow-up 260）：每镜最新一条按分镜顺序拼成一条，带章节。 */
export interface ReelChapter {
  scene: string;
  key: string;
  take: string;
  video: string;
  start: number;
  end: number;
  duration: number;
  review_status: string;
  note: string;
}
export interface ReelSkipped { key: string; scene: string; reason: string }
export interface ReelManifest {
  name: string;
  created_at: string;
  duration: number;
  chapters: ReelChapter[];
  skipped: ReelSkipped[];
}
export interface ReviewReel {
  episode_path: string;
  scene: string | null;
  name: string;
  state: "none" | "running" | "done" | "failed" | "interrupted";
  done: number;
  total: number;
  error: string;
  video_path: string;
  stale: boolean;
  manifest: ReelManifest | null;
  scenes: { id: string; label: string; shots: number }[];
}

async function read<T>(response: Response): Promise<T> {
  const data = await response.json();
  if (!response.ok) throw new ApiError(response.status, data.detail?.message || `HTTP ${response.status}`, data.detail);
  return data as T;
}

export async function loadReel(episodePath: string, scene: string | null): Promise<ReviewReel> {
  const query = new URLSearchParams({ episode_path: episodePath, ...(scene ? { scene } : {}) });
  return read(await fetch(`/api/review-reel?${query.toString()}`, { cache: "no-store" }));
}

export async function startReel(episodePath: string, scene: string | null): Promise<ReviewReel> {
  return read(await fetch("/api/review-reel", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ episode_path: episodePath, scene }),
  }));
}

/** 播放到 t 秒时所在的章节；没有落在任何一镜里返回 -1。 */
export function chapterAt(chapters: ReelChapter[], t: number): number {
  return chapters.findIndex((c, i) => t >= c.start && (t < c.end || i === chapters.length - 1));
}

export function clock(seconds: number): string {
  const s = Math.max(0, Math.floor(seconds));
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
}
