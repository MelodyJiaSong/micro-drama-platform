import { ApiError, type ApiErrorDetail, type FileResult, type TreeNode } from "./types";

async function readJson<T>(response: Response): Promise<T> {
  const text = await response.text();
  if (!response.ok) {
    let detail: ApiErrorDetail | null = null;
    try {
      const parsed = text ? JSON.parse(text) : null;
      if (parsed && typeof parsed === "object" && "detail" in parsed) {
        const d = (parsed as { detail: unknown }).detail;
        if (d && typeof d === "object") detail = d as ApiErrorDetail;
        else if (typeof d === "string") detail = { kind: d };
      }
    } catch {
      // body wasn't JSON
    }
    throw new ApiError(response.status, `HTTP ${response.status}`, detail);
  }
  if (!text) return undefined as unknown as T;
  return JSON.parse(text) as T;
}

export async function fetchTree(): Promise<TreeNode> {
  // `no-store`: after a delete/rename the left-nav tree must reflect the
  // current filesystem. Without it the browser can serve a cached /api/tree
  // and a deleted file keeps showing in the sidebar.
  // `lazy=1` (follow-up 280): navigation plus the first folder levels; deeper
  // folders are `lazy` stubs filled by `fetchSubtree` when opened.
  const response = await fetch("/api/tree?lazy=1", {
    method: "GET",
    headers: { Accept: "application/json" },
    cache: "no-store",
  });
  return readJson<TreeNode>(response);
}

/** One lazy folder's contents, `depth` folder levels deep (0 = everything). */
export async function fetchSubtree(path: string, depth = 1): Promise<TreeNode> {
  const response = await fetch(`/api/tree/subtree?path=${encodeURIComponent(path)}&depth=${depth}`, {
    method: "GET",
    headers: { Accept: "application/json" },
    cache: "no-store",
  });
  return readJson<TreeNode>(response);
}

export async function fetchFile(path: string): Promise<FileResult> {
  // `no-store`: after a rename / regeneration the viewer must show current
  // bytes, not a browser-cached stale copy (mirrors fetchTree).
  const response = await fetch(`/api/file?path=${encodeURIComponent(path)}`, {
    method: "GET",
    headers: { Accept: "application/json" },
    cache: "no-store",
  });
  return readJson<FileResult>(response);
}

/** A registered repo source outside `ai_videos/` (e.g. `.agents/references/project/review_roster.json`):
 *  `/api/file` only serves the media root, so repo sources go through the workflow source endpoint. */
export async function fetchRepoSource(path: string): Promise<{ path: string; content: string }> {
  const response = await fetch(`/api/global-workflow/source?${new URLSearchParams({ source_id: `repo:${path}` })}`, {
    method: "GET",
    headers: { Accept: "application/json" },
    cache: "no-store",
  });
  return readJson<{ path: string; content: string }>(response);
}

/** The rename pass that follows a Downloads import (see `importFromDownloads`). */
export interface RenameMediaResult {
  renamed: { from: string; to: string }[];
  skipped: string[];
  errors: { path: string; message: string }[];
}

export interface ArchiveMediaResult {
  from: string;
  to: string;
}

export async function archiveMedia(path: string): Promise<ArchiveMediaResult> {
  const response = await fetch("/api/archive-media", {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify({ path }),
  });
  return readJson<ArchiveMediaResult>(response);
}

export async function unarchiveMedia(path: string): Promise<ArchiveMediaResult> {
  const response = await fetch("/api/unarchive-media", {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify({ path }),
  });
  return readJson<ArchiveMediaResult>(response);
}

export async function deleteMedia(path: string): Promise<ArchiveMediaResult> {
  const response = await fetch("/api/delete-media", {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify({ path }),
  });
  return readJson<ArchiveMediaResult>(response);
}

export interface HardDeleteMediaResult {
  deleted: string;
}

export async function hardDeleteMedia(path: string): Promise<HardDeleteMediaResult> {
  const response = await fetch("/api/hard-delete-media", {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify({ path }),
  });
  return readJson<HardDeleteMediaResult>(response);
}

export interface PurgeDeletedResult {
  purged: number;
}

/** Empty the recycle bin: recursively wipe everything under
 * ai_videos/_deleted/ (every file type + folders), not just media. */
export async function purgeDeleted(): Promise<PurgeDeletedResult> {
  const response = await fetch("/api/purge-deleted", {
    method: "POST",
    headers: { Accept: "application/json" },
  });
  return readJson<PurgeDeletedResult>(response);
}

export interface ImportFromDownloadsResult {
  moved: { from: string; to: string; kind: string }[];
  // Unmatched files are NOT imported — left in Downloads, only reported (no `to`).
  unmatched: { from: string; kind: string }[];
  errors: { path: string; message: string }[];
  rename: RenameMediaResult;
}

export async function importFromDownloads(path: string): Promise<ImportFromDownloadsResult> {
  const response = await fetch("/api/import-from-downloads", {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify({ path }),
  });
  return readJson<ImportFromDownloadsResult>(response);
}

/** Build a same-origin URL for raw media (image / video / audio) via /api/media.
 * Bypasses /api/file's base64 + 1 MB limit. Per follow-up 005.
 *
 * Cache busting: an mtime arg takes precedence (per-file mtime).
 * Otherwise we append a module-level buster bumped on every tree refresh by
 * `bumpMediaCacheBuster()` — this evicts stale browser cache after a regen
 * (e.g. character views) where the URL path is unchanged but the bytes are not.
 */
let _mediaCacheBuster: number = Date.now();
export function bumpMediaCacheBuster(): void {
  _mediaCacheBuster = Date.now();
}
export function mediaUrl(path: string, mtime?: number): string {
  const v = mtime !== undefined ? mtime : _mediaCacheBuster;
  return `/api/media?path=${encodeURIComponent(path)}&v=${encodeURIComponent(String(v))}`;
}

export interface CharacterView {
  timestamp: number;
  role: string;
  path: string;
}

export interface CharacterAudio {
  path: string;
}

export interface CharacterTrim {
  path: string;
  duration_seconds: number;
}

export interface CharacterViewFailure {
  target: string;
  error: string;
}

export interface ExtractCharacterViewsResult {
  src: string;
  views: CharacterView[];
  audio: CharacterAudio | null;
  trim: CharacterTrim | null;
  failures: CharacterViewFailure[];
}

export async function extractCharacterViews(path: string): Promise<ExtractCharacterViewsResult> {
  const response = await fetch("/api/extract-character-views", {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify({ path }),
  });
  return readJson<ExtractCharacterViewsResult>(response);
}

export interface CharacterVideoListing {
  folder: string;
  /** Newest turntable mp4 in the folder (rel path), or null when none rendered yet. */
  latest_video: string | null;
}

export async function listCharacterVideos(
  path: string,
): Promise<{ items: CharacterVideoListing[] }> {
  // no-store: after a render/import the gallery must reflect the newest mp4.
  const response = await fetch(`/api/character-videos?path=${encodeURIComponent(path)}`, {
    method: "GET",
    headers: { Accept: "application/json" },
    cache: "no-store",
  });
  return readJson<{ items: CharacterVideoListing[] }>(response);
}

export interface ExtractAllCharacterViewsItem {
  folder: string;
  status: "ok" | "skipped" | "error";
  result: ExtractCharacterViewsResult | null;
  reason: string;
}

export interface ExtractAllCharacterViewsResult {
  characters_dir: string;
  items: ExtractAllCharacterViewsItem[];
}

/** Batch re-extract 3 views + audio + 2s trim for every character folder under
 *  a drama's `characters/` dir (path = that dir's relative path). */
export async function extractAllCharacterViews(
  path: string,
): Promise<ExtractAllCharacterViewsResult> {
  const response = await fetch("/api/extract-all-character-views", {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify({ path }),
  });
  return readJson<ExtractAllCharacterViewsResult>(response);
}

/** 流程与自检：仓库级总览（只含仓库级检查 + 各剧体检汇总）。只读。 */
export async function fetchProcessQc(): Promise<import("./lib/processQc").ProcessQcRepo> {
  const response = await fetch("/api/process-qc", { headers: { Accept: "application/json" } });
  return readJson(response);
}

/** 流程与自检：单部剧（本剧检查与继承自仓库级的检查分开返回）。只读。 */
export async function fetchProcessQcDrama(drama: string): Promise<import("./lib/processQc").ProcessQcDrama> {
  const response = await fetch(`/api/process-qc/drama?drama=${encodeURIComponent(drama)}`, { headers: { Accept: "application/json" } });
  return readJson(response);
}

/** 审查单索引（follow-up 333）：左侧导航「审查单」一类，所有剧 `reviews/` 下每张审查单的摘要。 */
export interface ReviewRunSummary {
  dir: string; drama: string; drama_name: string; id: string; title: string; episode: string; chain: string; loop: number;
  stage_name: string; state: string; created_at: string; done: number; failed: number; total: number; totals: Record<string, number>;
  /** 阶段（pregen＝出片前）、覆盖的场与最多轮数（follow-up 336：剧页故事板按场显示审查状态）。 */
  stage?: string; scenes?: string[]; max_loops?: number;
  /** 这一轮有没有修复页数据（corrections.json，review_run.py corrections 写）。 */
  corrections?: boolean;
}

/** 一张审查单的 checklist.json（已解析）。不走 /api/file：v5 双审单常超过它的 1 MiB 上限。 */
export async function fetchReviewChecklist<T = unknown>(dir: string): Promise<T> {
  const response = await fetch(`/api/review-runs/checklist?${new URLSearchParams({ path: dir })}`, {
    method: "GET", headers: { Accept: "application/json" }, cache: "no-store",
  });
  return readJson<T>(response);
}

export async function fetchReviewRuns(): Promise<{ runs: ReviewRunSummary[] }> {
  const response = await fetch("/api/review-runs", { method: "GET", headers: { Accept: "application/json" }, cache: "no-store" });
  return readJson<{ runs: ReviewRunSummary[] }>(response);
}
