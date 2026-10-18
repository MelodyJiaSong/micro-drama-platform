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
