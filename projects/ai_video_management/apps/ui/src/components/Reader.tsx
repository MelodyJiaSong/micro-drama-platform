/** Reader: render-mode dispatch by file extension.
 *
 * Read-only for everything under `ai_videos/` (follow-up 233 removed the old
 * pipeline's per-file tools — prompt block editing, shot / shotlist / casting /
 * actor / voice views, frame / plate / last-frame extraction, the episode
 * takes / concat / subtitle toolbar — together with the whole-file editor,
 * which only ever served files outside `ai_videos/`). Media keep their preview,
 * archive / delete, and the 🖼 three-view extraction on character turntables. */
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Breadcrumb } from "./Breadcrumb";
import { ParseFallback } from "./ParseFallback";
import { Renderer } from "../markdown/renderer";
import { CodeView } from "../markdown/CodeView";
import { JsonlView } from "../markdown/JsonlView";
import { SiblingMedia, isCharacterVideoPath } from "./SiblingMedia";
import { announceToast } from "../lib/announce";
import {
  archiveMedia,
  deleteMedia,
  extractCharacterViews,
  fetchFile,
  mediaUrl,
  unarchiveMedia,
} from "../api";
import { ApiError, type FileResult } from "../types";
import { ZoomableImage } from "./ZoomableImage";
import { useFileChanges } from "../lib/fileEvents";

const IMAGE_EXTS = new Set([".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"]);
const VIDEO_EXTS = new Set([".mp4", ".mov", ".webm", ".mkv", ".avi", ".m4v"]);
const AUDIO_EXTS = new Set([".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac"]);
const PDF_EXTS = new Set([".pdf"]);
// White-model meshes handed back by image-to-3D — previewed in-browser so the user
// can judge a mesh (thin structures, silhouette) without opening Blender.
const MODEL_EXTS = new Set([".glb", ".gltf"]);
// Script-built scene files (`_blender/{bg}.blend`): no browser preview, served by
// /api/media as a plain download (follow-up 173).
const DOWNLOAD_EXTS = new Set([".blend"]);

export interface ReaderProps {
  knownPaths: string[];
  /** Folders not loaded yet (follow-up 280): links into them are not flagged broken. */
  unloadedDirs?: string[];
  onSaved: () => void;
}

export function Reader({ knownPaths, unloadedDirs, onSaved }: ReaderProps): JSX.Element {
  const location = useLocation();
  const navigate = useNavigate();
  const path = useMemo<string | null>(() => {
    if (!location.pathname.startsWith("/file/")) return null;
    const encoded = location.pathname.slice("/file/".length);
    try { return decodeURIComponent(encoded); } catch { return null; }
  }, [location.pathname]);

  const [file, setFile] = useState<FileResult | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [archiving, setArchiving] = useState<boolean>(false);
  const [deleting, setDeleting] = useState<boolean>(false);
  const videoRef = useRef<HTMLVideoElement>(null);
  const [extractingViews, setExtractingViews] = useState<boolean>(false);

  const ext = path ? extOf(path) : "";
  const isMediaImage = IMAGE_EXTS.has(ext);
  const isMediaVideo = VIDEO_EXTS.has(ext);
  const isMediaAudio = AUDIO_EXTS.has(ext);
  const isMediaPdf = PDF_EXTS.has(ext);
  const isMediaModel = MODEL_EXTS.has(ext);
  const isMediaDownload = DOWNLOAD_EXTS.has(ext);
  const isMediaOnly =
    isMediaVideo || isMediaImage || isMediaAudio || isMediaPdf || isMediaModel || isMediaDownload;

  const load = useCallback(async () => {
    if (!path) return;
    if (isMediaOnly) {
      // Media files (video / non-png-jpg images) are streamed via /api/media —
      // skip /api/file fetch entirely (videos can exceed the 1 MB limit).
      setFile({ path, content: "", encoding: "media", bytes: 0, mtime: 0, mtime_http: "" });
      setError(null);
      return;
    }
    try {
      const f = await fetchFile(path);
      setFile(f);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err : new Error(String(err)));
    }
  }, [path, isMediaOnly]);

  useEffect(() => {
    setFile(null); setError(null);
    void load();
  }, [load]);
  // Live updates (follow-up 280): the open text file changed on disk → show the new content.
  useFileChanges(path && !isMediaOnly ? path : null, () => { void load(); });

  const onArchiveToggle = useCallback(async () => {
    if (!path) return;
    const parts = path.split("/");
    const inArchive = parts.length >= 2 && parts[parts.length - 2] === "archive";
    setArchiving(true);
    try {
      const result = inArchive ? await unarchiveMedia(path) : await archiveMedia(path);
      announceToast(`${inArchive ? "Unarchived" : "Archived"} ${parts[parts.length - 1] ?? path}`);
      onSaved();
      navigate(`/file/${encodeURIComponent(result.to)}`);
    } catch (err) {
      announceToast(`${inArchive ? "Unarchive" : "Archive"} failed: ${archiveErrorKind(err)}`);
    } finally {
      setArchiving(false);
    }
  }, [path, onSaved, navigate]);

  const onDeleteClick = useCallback(async () => {
    if (!path) return;
    const name = path.split("/").pop() ?? path;
    if (!window.confirm(`Move ${name} to _deleted/?`)) return;
    setDeleting(true);
    // Release the preview stream FIRST: while a <video> is loaded it streams through
    // the server, which then holds an open handle on the file and a rename/delete on
    // Windows fails with "资源忙". Unloading the element drops the browser's request so
    // the server closes the handle; the backend's retry-through-lock then succeeds.
    const v = videoRef.current;
    if (v) {
      try { v.pause(); } catch { /* ignore */ }
      v.removeAttribute("src");
      v.load();
      await new Promise((r) => setTimeout(r, 250));
    }
    try {
      const result = await deleteMedia(path);
      announceToast(`Deleted ${name}`);
      onSaved();
      navigate(`/file/${encodeURIComponent(result.to)}`);
    } catch (err) {
      announceToast(`Delete failed: ${archiveErrorKind(err)}`);
    } finally {
      setDeleting(false);
    }
  }, [path, onSaved, navigate]);

  const onExtractCharacterViewsClick = useCallback(async () => {
    if (!path) return;
    const name = path.split("/").pop() ?? path;
    setExtractingViews(true);
    try {
      const result = await extractCharacterViews(path);
      const okCount = result.views.length + (result.audio ? 1 : 0) + (result.trim ? 1 : 0);
      const failCount = result.failures.length;
      const summary =
        failCount === 0
          ? `Extracted ${okCount} 文件 (三视图 + 音频 + 前2s) from ${name} → views/`
          : `Extracted ${okCount} from ${name} (${failCount} failed)`;
      announceToast(summary);
      onSaved();
    } catch (err) {
      announceToast(`Extract views failed: ${archiveErrorKind(err)}`);
    } finally {
      setExtractingViews(false);
    }
  }, [path, onSaved]);

  if (!path) return <div className="muted">No file selected.</div>;
  if (error) {
    return (
      <div className="reader">
        <div role="alert" className="save-error-banner">
          {error instanceof ApiError ? `${error.status} ${apiErrorLabel(error)}` : error.message}
        </div>
      </div>
    );
  }
  if (!file) return <div className="muted">Loading…</div>;

  const isMarkdown = ext === ".md";
  const isJsonl = ext === ".jsonl";
  const isCode = ext === ".json" || ext === ".yaml" || ext === ".yml" || ext === ".toml";

  const filename = path.split("/").pop() ?? path;
  const pathParts = path.split("/");
  const isArchivedFile = pathParts.length >= 2 && pathParts[pathParts.length - 2] === "archive";
  const isDeletedFile = path.startsWith("ai_videos/_deleted/");
  const mediaActionsBusy = archiving || deleting || extractingViews;
  const archiveLabel = isArchivedFile
    ? (archiving ? "Unarchiving…" : "↺ Unarchive")
    : (archiving ? "Archiving…" : "📦 Archive");
  const deleteLabel = deleting ? "Deleting…" : "🗑 Delete";
  const viewsExtractLabel = extractingViews ? "⏳ 提取中…" : "🖼 提取三视图+音频+前2s";
  const showViewsBtn = isMediaVideo && !isArchivedFile && !isDeletedFile && isCharacterVideoPath(path);

  const archiveAndDelete = !isDeletedFile ? (
    <>
      <button type="button" className="reader-media-archive-btn"
        onClick={onArchiveToggle} disabled={mediaActionsBusy}
        aria-label={isArchivedFile ? `Unarchive ${filename}` : `Archive ${filename}`}>
        {archiveLabel}
      </button>
      <button type="button" className="reader-media-delete-btn"
        onClick={onDeleteClick} disabled={mediaActionsBusy}
        aria-label={`Delete ${filename}`}>
        {deleteLabel}
      </button>
    </>
  ) : null;

  return (
    <div className="reader">
      <div className="reader-toolbar" role="toolbar" aria-label="File toolbar">
        <Breadcrumb
          path={path}
          knownPaths={knownPaths}
          onNavigate={(target) => navigate(`/file/${encodeURIComponent(target)}`)}
        />
      </div>
      <div className="reader-body">
        {isMediaVideo ? (
          <div className="media-view">
            <video ref={videoRef} controls preload="metadata" src={mediaUrl(path)} />
            {!isDeletedFile ? (
              <div className="reader-media-actions">
                {showViewsBtn ? (
                  <button type="button" className="reader-media-views-btn"
                    onClick={onExtractCharacterViewsClick} disabled={mediaActionsBusy}
                    aria-label={`Extract 3 views, audio and first-2s trim from the latest turntable video in ${filename}'s folder`}
                    title="一键提取 5 个文件到 ./views/：三视图 (front / side / back .png) + 音频 (.mp3) + 原片前 2 秒 (_trim2s.mp4) — 多个原始视频时取 timestamp 最新的那个；适用于 character turntable 建立视频 (4s locked-framing + 180° slow orbit)">
                    {viewsExtractLabel}
                  </button>
                ) : null}
                {archiveAndDelete}
              </div>
            ) : null}
          </div>
        ) : isMediaImage ? (
          <div className="media-view">
            <ZoomableImage src={mediaUrl(path)} alt={filename} />
            {archiveAndDelete ? <div className="reader-media-actions">{archiveAndDelete}</div> : null}
          </div>
        ) : isMediaModel ? (
          <div className="media-view model-view">
            {/* @google/model-viewer custom element; see main.tsx for the import. */}
            <model-viewer
              src={mediaUrl(path)}
              alt={filename}
              camera-controls
              touch-action="pan-y"
              shadow-intensity="1"
              exposure="1"
              environment-image="neutral"
              ar-status="not-presenting"
            />
            <p className="muted model-view-hint">
              拖动旋转 · 滚轮缩放 · 右键平移。白模只承载几何，材质与长相由出片模型提供。
            </p>
            {archiveAndDelete ? <div className="reader-media-actions">{archiveAndDelete}</div> : null}
          </div>
        ) : isMediaDownload ? (
          <div className="media-view">
            <p className="muted">浏览器里没法预览这个文件，下载后用 Blender 打开。</p>
            <a href={mediaUrl(path)} download={filename}>⬇ 下载 {filename}</a>
          </div>
        ) : isMediaPdf ? (
          <div className="media-view pdf-view">
            <iframe src={mediaUrl(path)} title={filename} />
            {archiveAndDelete ? <div className="reader-media-actions">{archiveAndDelete}</div> : null}
          </div>
        ) : isMediaAudio ? (
          <div className="media-view">
            <audio controls preload="metadata" src={mediaUrl(path)} />
            {archiveAndDelete ? <div className="reader-media-actions">{archiveAndDelete}</div> : null}
          </div>
        ) : isJsonl ? (
          <ParseFallback rawText={file.content} componentName="JsonlView">
            <JsonlView content={file.content} />
          </ParseFallback>
        ) : isCode ? (
          <ParseFallback rawText={file.content} componentName="CodeView">
            <CodeView content={file.content} filename={filename} />
          </ParseFallback>
        ) : isMarkdown ? (
          <ParseFallback rawText={file.content} componentName="MarkdownView">
            <Renderer content={file.content} currentPath={path} knownPaths={knownPaths} unloadedDirs={unloadedDirs} />
            <SiblingMedia currentPath={path} knownPaths={knownPaths} onChange={onSaved} />
          </ParseFallback>
        ) : (
          <pre className="text-view">{file.content}</pre>
        )}
      </div>
    </div>
  );
}

function apiErrorLabel(err: ApiError): string {
  if (err.status === 404) return "not found";
  if (err.status === 400) return err.detail?.kind ?? "bad request";
  if (err.status === 413) return "file too large";
  if (err.status === 403) return "forbidden";
  if (err.status === 409) return "stale write";
  return err.detail?.kind ?? err.message;
}

function extOf(path: string): string {
  const dot = path.lastIndexOf(".");
  if (dot < 0) return "";
  return path.slice(dot).toLowerCase();
}

function archiveErrorKind(err: unknown): string {
  if (err instanceof ApiError) return err.detail?.kind ?? `HTTP ${err.status}`;
  if (err instanceof Error) return err.message;
  return "unknown_error";
}
