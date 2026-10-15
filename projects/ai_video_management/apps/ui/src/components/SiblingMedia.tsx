/** SiblingMedia: render images + videos that live in the same folder as the
 * currently-viewed .md file. Per follow-up 005, character / scene / shot folders
 * may contain user-rendered turntable.mp4, ref.png, shot output mp4 etc.
 * This component shows them inline below the markdown so user doesn't have to
 * click each media file separately to preview.
 *
 * Per follow-up 008: each tile gets a per-file Archive / Unarchive button. The
 * archive/ subfolder of the current md folder is also surfaced as an "Archived"
 * subsection so users can unarchive without navigating into archive/.
 *
 * Per follow-up 011: multi-select via always-visible corner checkbox on each
 * tile + per-section toolbar (Select all / Clear / Archive Selected (N) or
 * Unarchive Selected (N)). Batch ops loop the existing per-file endpoints
 * serially with continue-on-error aggregation; per-tile single-file buttons
 * retained for quick single archives.
 *
 * A character turntable video also gets the 🖼 three-view extraction. The old
 * pipeline's per-tile tools (frame / plate / last-frame extraction, subtitle
 * scaffold + burn, intro-card burn) went with follow-up 233.
 */
import { useEffect, useMemo, useState } from "react";
import { archiveMedia, extractCharacterViews, mediaUrl, unarchiveMedia } from "../api";
import { announceToast as announce } from "../lib/announce";
import { ApiError } from "../types";
import { ZoomableImage } from "./ZoomableImage";
import { CHARACTER_DIR_SEGMENT } from "../lib/characterDir";

const VIDEO_EXTS = new Set([".mp4", ".mov", ".webm", ".mkv", ".avi", ".m4v"]);
const IMAGE_EXTS = new Set([".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"]);
const AUDIO_EXTS = new Set([".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac"]);
// White models (image-to-3D output, normalised by tools/whitemodel_normalize.py).
const MODEL_EXTS = new Set([".glb", ".gltf"]);
const MEDIA_EXTS = new Set([...VIDEO_EXTS, ...IMAGE_EXTS, ...AUDIO_EXTS, ...MODEL_EXTS]);
const ARCHIVE_DIR_NAME = "archive";
const RENDERS_DIR_NAME = "renders";

/** Matches `ai_videos/{drama}/characters/{c|m}{N}[_{slug}]/{file}.{video_ext}`.
 * Used to gate the 🖼 three-view + audio + first-2s extraction button so it
 * only appears for character turntable videos (rule #12.5 v10.2 sources).
 * Mirrors the backend `_is_under_character_folder` in character_video__writer.py:
 * `characters/cN` may sit directly under the drama (legacy flat layout) OR under
 * one or more stage folders (staged pipeline, e.g. `2_世界观人设/characters/cN`),
 * so an optional intermediate-segment group precedes `characters/`.
 */
const CHARACTER_VIDEO_PATH_RE = new RegExp(
  `^ai_videos/[^/_][^/]*/(?:[^/]+/)*characters/${CHARACTER_DIR_SEGMENT}/[^/]+\\.(?:mp4|mov|webm|mkv|avi|m4v)$`,
  "i",
);

export function isCharacterVideoPath(path: string): boolean {
  return CHARACTER_VIDEO_PATH_RE.test(path);
}

export interface SiblingMediaProps {
  currentPath: string;
  knownPaths: string[];
  onChange?: () => void;
}

function extOf(p: string): string {
  const dot = p.lastIndexOf(".");
  return dot < 0 ? "" : p.slice(dot).toLowerCase();
}

function findSiblingMedia(currentPath: string, all: string[]): string[] {
  const lastSlash = currentPath.lastIndexOf("/");
  if (lastSlash < 0) return [];
  const parent = currentPath.slice(0, lastSlash + 1);
  return all
    .filter((p) => {
      if (p === currentPath) return false;
      if (!p.startsWith(parent)) return false;
      const tail = p.slice(parent.length);
      if (tail.includes("/")) return false;
      return MEDIA_EXTS.has(extOf(p));
    })
    .sort();
}

/** Media inside the current folder's `renders/` subfolder — where the import
 * flow drops shot-generated images/videos (start-frame / end-frame / video),
 * keeping their original names. Immediate children only. */
function findRendersMedia(currentPath: string, all: string[]): string[] {
  const lastSlash = currentPath.lastIndexOf("/");
  if (lastSlash < 0) return [];
  const rendersPrefix = `${currentPath.slice(0, lastSlash + 1)}${RENDERS_DIR_NAME}/`;
  return all
    .filter((p) => {
      if (!p.startsWith(rendersPrefix)) return false;
      const tail = p.slice(rendersPrefix.length);
      if (tail.includes("/")) return false;
      return MEDIA_EXTS.has(extOf(p));
    })
    .sort();
}

/** White models sitting one level down from the md — `whitemodel/raw.glb` for a
 * prop, `model/model.glb` for a character. Same-folder and `renders/` models are
 * already covered by the sections above, and `archive/` by the one below, so those
 * three are skipped here to keep each mesh on exactly one tile. Only meshes are
 * pulled up: a subfolder's images (views/, frames/, peek renders) would flood the
 * card, and they stay one click away in the tree. */
export function findSubfolderModels(currentPath: string, all: string[]): string[] {
  const lastSlash = currentPath.lastIndexOf("/");
  if (lastSlash < 0) return [];
  const parent = currentPath.slice(0, lastSlash + 1);
  const skipped = new Set([ARCHIVE_DIR_NAME, RENDERS_DIR_NAME]);
  return all
    .filter((p) => {
      if (!p.startsWith(parent)) return false;
      if (!MODEL_EXTS.has(extOf(p))) return false;
      const segments = p.slice(parent.length).split("/");
      if (segments.length !== 2) return false;
      return !skipped.has(segments[0]);
    })
    .sort();
}

function findArchivedMedia(currentPath: string, all: string[]): string[] {
  const lastSlash = currentPath.lastIndexOf("/");
  if (lastSlash < 0) return [];
  const archivePrefix = `${currentPath.slice(0, lastSlash + 1)}${ARCHIVE_DIR_NAME}/`;
  return all
    .filter((p) => {
      if (!p.startsWith(archivePrefix)) return false;
      const tail = p.slice(archivePrefix.length);
      if (tail.includes("/")) return false;
      return MEDIA_EXTS.has(extOf(p));
    })
    .sort();
}

function basename(path: string): string {
  return path.split("/").pop() ?? path;
}

function errorKind(err: unknown): string {
  if (err instanceof ApiError) {
    return err.detail?.kind ?? `HTTP ${err.status}`;
  }
  if (err instanceof Error) return err.message;
  return "unknown_error";
}

interface MediaTileProps {
  path: string;
  archived: boolean;
  busy: boolean;
  extractingViews: boolean;
  selected: boolean;
  selectionBusy: boolean;
  onToggleSelect: (path: string) => void;
  onArchive: (path: string) => void;
  onUnarchive: (path: string) => void;
  onExtractCharacterViews: (path: string) => void;
}

function MediaTile({
  path,
  archived,
  busy,
  extractingViews,
  selected,
  selectionBusy,
  onToggleSelect,
  onArchive,
  onUnarchive,
  onExtractCharacterViews,
}: MediaTileProps): JSX.Element {
  const ext = extOf(path);
  const isVideo = VIDEO_EXTS.has(ext);
  const isAudio = AUDIO_EXTS.has(ext);
  const isModel = MODEL_EXTS.has(ext);
  const isCharacterVideo = isVideo && isCharacterVideoPath(path);
  const filename = basename(path);
  const url = mediaUrl(path);
  const handleClick = (): void => {
    if (busy) return;
    if (archived) onUnarchive(path);
    else onArchive(path);
  };
  const className = [
    "sibling-media-item",
    archived ? "is-archived" : "",
    selected ? "is-selected" : "",
  ]
    .filter(Boolean)
    .join(" ");
  return (
    <figure className={className}>
      <input
        type="checkbox"
        className="tile-checkbox"
        checked={selected}
        disabled={selectionBusy}
        onChange={() => onToggleSelect(path)}
        onClick={(e) => e.stopPropagation()}
        aria-label={`Select ${filename}`}
      />
      {isVideo ? (
        <video controls preload="metadata" src={url} />
      ) : isAudio ? (
        <audio controls preload="metadata" src={url} />
      ) : isModel ? (
        /* @google/model-viewer custom element; see main.tsx for the import.
           `loading="lazy"` keeps a multi-mesh card from fetching every MB up front. */
        <model-viewer
          src={url}
          alt={filename}
          camera-controls
          touch-action="pan-y"
          shadow-intensity="1"
          exposure="1"
          environment-image="neutral"
          loading="lazy"
          ar-status="not-presenting"
        />
      ) : (
        <ZoomableImage src={url} alt={filename} loading="lazy" />
      )}
      <figcaption>
        {archived ? "📦 " : ""}
        {filename}
      </figcaption>
      <div className="sibling-media-actions">
        {isCharacterVideo && !archived ? (
          <button
            type="button"
            className="sibling-media-views-btn"
            onClick={() => onExtractCharacterViews(path)}
            disabled={busy || extractingViews}
            aria-label={`Extract 3 views, audio and first-2s trim from the latest turntable video in ${filename}'s folder`}
            title="一键提取 5 个文件到 ./views/：三视图 (front / side / back .png) + 音频 (.mp3) + 原片前 2 秒 (_trim2s.mp4) — 多个原始视频时取 timestamp 最新的那个；适用于 character turntable 建立视频 (4s locked-framing + 180° slow orbit)"
          >
            {extractingViews ? "⏳ 提取中…" : "🖼 提取三视图+音频+前2s"}
          </button>
        ) : null}
        <button
          type="button"
          className="sibling-media-archive-btn"
          onClick={handleClick}
          disabled={busy}
          aria-label={archived ? `Unarchive ${filename}` : `Archive ${filename}`}
          title={archived ? "Move back to parent folder" : "Move to archive/ subfolder"}
        >
          {archived ? "↺ Unarchive" : "📦 Archive"}
        </button>
      </div>
    </figure>
  );
}

interface ToolbarProps {
  total: number;
  selectedCount: number;
  busy: boolean;
  archived: boolean;
  onSelectAll: () => void;
  onClear: () => void;
  onBatch: () => void;
}

function Toolbar({
  total,
  selectedCount,
  busy,
  archived,
  onSelectAll,
  onClear,
  onBatch,
}: ToolbarProps): JSX.Element {
  const allSelected = selectedCount > 0 && selectedCount === total;
  const actionLabel = archived
    ? `↺ Unarchive Selected (${selectedCount})`
    : `📦 Archive Selected (${selectedCount})`;
  const actionAria = archived
    ? `Unarchive ${selectedCount} selected files`
    : `Archive ${selectedCount} selected files`;
  return (
    <div className="sibling-media-toolbar" role="toolbar">
      <button
        type="button"
        onClick={onSelectAll}
        disabled={busy || allSelected || total === 0}
        aria-label="Select all media in this section"
      >
        Select all
      </button>
      <button
        type="button"
        onClick={onClear}
        disabled={busy || selectedCount === 0}
        aria-label="Clear selection"
      >
        Clear
      </button>
      <button
        type="button"
        className="sibling-media-toolbar-primary"
        onClick={onBatch}
        disabled={busy || selectedCount === 0}
        aria-label={actionAria}
      >
        {actionLabel}
      </button>
    </div>
  );
}

export function SiblingMedia({ currentPath, knownPaths, onChange }: SiblingMediaProps): JSX.Element | null {
  const siblings = useMemo(() => findSiblingMedia(currentPath, knownPaths), [currentPath, knownPaths]);
  const renders = useMemo(() => findRendersMedia(currentPath, knownPaths), [currentPath, knownPaths]);
  const models = useMemo(() => findSubfolderModels(currentPath, knownPaths), [currentPath, knownPaths]);
  const archived = useMemo(() => findArchivedMedia(currentPath, knownPaths), [currentPath, knownPaths]);
  const [busyPath, setBusyPath] = useState<string | null>(null);
  const [busy, setBusy] = useState<boolean>(false);
  const [extractingViewsPath, setExtractingViewsPath] = useState<string | null>(null);
  const [selectedActive, setSelectedActive] = useState<Set<string>>(() => new Set());
  const [selectedRenders, setSelectedRenders] = useState<Set<string>>(() => new Set());
  const [selectedModels, setSelectedModels] = useState<Set<string>>(() => new Set());
  const [selectedArchived, setSelectedArchived] = useState<Set<string>>(() => new Set());

  // Drop selected paths that no longer exist in the lists after a tree refresh
  // (e.g., archive op moved them across sections — old paths become stale).
  useEffect(() => {
    setSelectedActive((prev) => prune(prev, siblings));
  }, [siblings]);
  useEffect(() => {
    setSelectedRenders((prev) => prune(prev, renders));
  }, [renders]);
  useEffect(() => {
    setSelectedModels((prev) => prune(prev, models));
  }, [models]);
  useEffect(() => {
    setSelectedArchived((prev) => prune(prev, archived));
  }, [archived]);

  if (siblings.length === 0 && renders.length === 0 && models.length === 0 && archived.length === 0) return null;

  const handleArchive = async (path: string): Promise<void> => {
    setBusyPath(path);
    try {
      await archiveMedia(path);
      announce(`Archived ${basename(path)}`);
      onChange?.();
    } catch (err) {
      announce(`Archive failed: ${errorKind(err)}`);
    } finally {
      setBusyPath(null);
    }
  };

  const handleUnarchive = async (path: string): Promise<void> => {
    setBusyPath(path);
    try {
      await unarchiveMedia(path);
      announce(`Unarchived ${basename(path)}`);
      onChange?.();
    } catch (err) {
      announce(`Unarchive failed: ${errorKind(err)}`);
    } finally {
      setBusyPath(null);
    }
  };

  const handleExtractCharacterViews = async (path: string): Promise<void> => {
    setExtractingViewsPath(path);
    try {
      const result = await extractCharacterViews(path);
      const viewCount = result.views.length;
      const hasAudio = result.audio !== null;
      const hasTrim = result.trim !== null;
      const failCount = result.failures.length;
      const suffix = `${hasAudio ? " + 音频" : ""}${hasTrim ? " + 前2s" : ""}`;
      const summary =
        failCount === 0
          ? `Extracted ${viewCount} 视图${suffix} from ${basename(path)} → views/`
          : `Extracted ${viewCount} 视图${suffix} from ${basename(path)} (${failCount} failed)`;
      announce(summary);
      onChange?.();
    } catch (err) {
      announce(`Extract views failed: ${errorKind(err)}`);
    } finally {
      setExtractingViewsPath(null);
    }
  };

  const toggleActive = (path: string): void => {
    setSelectedActive((prev) => toggle(prev, path));
  };
  const toggleRendersSel = (path: string): void => {
    setSelectedRenders((prev) => toggle(prev, path));
  };
  const toggleArchivedSel = (path: string): void => {
    setSelectedArchived((prev) => toggle(prev, path));
  };
  const toggleModelsSel = (path: string): void => {
    setSelectedModels((prev) => toggle(prev, path));
  };

  const handleBatchArchiveModels = async (): Promise<void> => {
    const paths = models.filter((p) => selectedModels.has(p));
    if (paths.length === 0) return;
    setBusy(true);
    const successes: string[] = [];
    const failures: { name: string; kind: string }[] = [];
    for (const p of paths) {
      try {
        await archiveMedia(p);
        successes.push(p);
      } catch (err) {
        failures.push({ name: basename(p), kind: errorKind(err) });
      }
    }
    setSelectedModels(new Set());
    setBusy(false);
    onChange?.();
    announce(buildBatchAnnounce("Archived", successes.length, failures));
  };

  const handleBatchArchiveRenders = async (): Promise<void> => {
    const paths = renders.filter((p) => selectedRenders.has(p));
    if (paths.length === 0) return;
    setBusy(true);
    const successes: string[] = [];
    const failures: { name: string; kind: string }[] = [];
    for (const p of paths) {
      try {
        await archiveMedia(p);
        successes.push(p);
      } catch (err) {
        failures.push({ name: basename(p), kind: errorKind(err) });
      }
    }
    setSelectedRenders(new Set());
    setBusy(false);
    onChange?.();
    announce(buildBatchAnnounce("Archived", successes.length, failures));
  };

  const handleBatchArchive = async (): Promise<void> => {
    const paths = siblings.filter((p) => selectedActive.has(p));
    if (paths.length === 0) return;
    setBusy(true);
    const successes: string[] = [];
    const failures: { name: string; kind: string }[] = [];
    for (const p of paths) {
      try {
        await archiveMedia(p);
        successes.push(p);
      } catch (err) {
        failures.push({ name: basename(p), kind: errorKind(err) });
      }
    }
    setSelectedActive(new Set());
    setBusy(false);
    onChange?.();
    announce(buildBatchAnnounce("Archived", successes.length, failures));
  };

  const handleBatchUnarchive = async (): Promise<void> => {
    const paths = archived.filter((p) => selectedArchived.has(p));
    if (paths.length === 0) return;
    setBusy(true);
    const successes: string[] = [];
    const failures: { name: string; kind: string }[] = [];
    for (const p of paths) {
      try {
        await unarchiveMedia(p);
        successes.push(p);
      } catch (err) {
        failures.push({ name: basename(p), kind: errorKind(err) });
      }
    }
    setSelectedArchived(new Set());
    setBusy(false);
    onChange?.();
    announce(buildBatchAnnounce("Unarchived", successes.length, failures));
  };

  return (
    <section className="sibling-media-grid" aria-label="Sibling media in folder">
      {renders.length > 0 ? (
        <>
          <h3>🎬 Renders · 生成产物 (renders/)</h3>
          <Toolbar
            total={renders.length}
            selectedCount={selectedRenders.size}
            busy={busy}
            archived={false}
            onSelectAll={() => setSelectedRenders(new Set(renders))}
            onClear={() => setSelectedRenders(new Set())}
            onBatch={handleBatchArchiveRenders}
          />
          <div className="sibling-media-row">
            {renders.map((p) => (
              <MediaTile
                key={p}
                path={p}
                archived={false}
                busy={busy || busyPath === p}
                extractingViews={extractingViewsPath === p}
                selected={selectedRenders.has(p)}
                selectionBusy={busy}
                onToggleSelect={toggleRendersSel}
                onArchive={handleArchive}
                onUnarchive={handleUnarchive}
                onExtractCharacterViews={handleExtractCharacterViews}
              />
            ))}
          </div>
        </>
      ) : null}
      {models.length > 0 ? (
        <>
          <h3>🧊 3D 白模 · 子目录内的 .glb / .gltf（拖动旋转 · 滚轮缩放）</h3>
          <Toolbar
            total={models.length}
            selectedCount={selectedModels.size}
            busy={busy}
            archived={false}
            onSelectAll={() => setSelectedModels(new Set(models))}
            onClear={() => setSelectedModels(new Set())}
            onBatch={handleBatchArchiveModels}
          />
          <div className="sibling-media-row">
            {models.map((p) => (
              <MediaTile
                key={p}
                path={p}
                archived={false}
                busy={busy || busyPath === p}
                extractingViews={extractingViewsPath === p}
                selected={selectedModels.has(p)}
                selectionBusy={busy}
                onToggleSelect={toggleModelsSel}
                onArchive={handleArchive}
                onUnarchive={handleUnarchive}
                onExtractCharacterViews={handleExtractCharacterViews}
              />
            ))}
          </div>
        </>
      ) : null}
      {siblings.length > 0 ? (
        <>
          <h3>📁 Folder media · 同 folder 媒体</h3>
          <Toolbar
            total={siblings.length}
            selectedCount={selectedActive.size}
            busy={busy}
            archived={false}
            onSelectAll={() => setSelectedActive(new Set(siblings))}
            onClear={() => setSelectedActive(new Set())}
            onBatch={handleBatchArchive}
          />
          <div className="sibling-media-row">
            {siblings.map((p) => (
              <MediaTile
                key={p}
                path={p}
                archived={false}
                busy={busy || busyPath === p}
                extractingViews={extractingViewsPath === p}
                selected={selectedActive.has(p)}
                selectionBusy={busy}
                onToggleSelect={toggleActive}
                onArchive={handleArchive}
                onUnarchive={handleUnarchive}
                onExtractCharacterViews={handleExtractCharacterViews}
              />
            ))}
          </div>
        </>
      ) : null}
      {archived.length > 0 ? (
        <>
          <h3>📦 Archived · 已归档</h3>
          <Toolbar
            total={archived.length}
            selectedCount={selectedArchived.size}
            busy={busy}
            archived
            onSelectAll={() => setSelectedArchived(new Set(archived))}
            onClear={() => setSelectedArchived(new Set())}
            onBatch={handleBatchUnarchive}
          />
          <div className="sibling-media-row sibling-media-archived">
            {archived.map((p) => (
              <MediaTile
                key={p}
                path={p}
                archived
                busy={busy || busyPath === p}
                extractingViews={extractingViewsPath === p}
                selected={selectedArchived.has(p)}
                selectionBusy={busy}
                onToggleSelect={toggleArchivedSel}
                onArchive={handleArchive}
                onUnarchive={handleUnarchive}
                onExtractCharacterViews={handleExtractCharacterViews}
              />
            ))}
          </div>
        </>
      ) : null}
    </section>
  );
}

function toggle(prev: Set<string>, path: string): Set<string> {
  const next = new Set(prev);
  if (next.has(path)) next.delete(path);
  else next.add(path);
  return next;
}

function prune(prev: Set<string>, current: string[]): Set<string> {
  const valid = new Set(current);
  let dirty = false;
  const next = new Set<string>();
  for (const p of prev) {
    if (valid.has(p)) next.add(p);
    else dirty = true;
  }
  return dirty ? next : prev;
}

function buildBatchAnnounce(
  verb: string,
  okCount: number,
  failures: { name: string; kind: string }[],
): string {
  const parts: string[] = [];
  if (okCount > 0) parts.push(`${verb} ${okCount} file${okCount === 1 ? "" : "s"}`);
  if (failures.length > 0) {
    const detail = failures.map((f) => `${f.name} (${f.kind})`).join(", ");
    parts.push(`failed ${failures.length}: ${detail}`);
  }
  if (parts.length === 0) return `${verb}: no files selected`;
  return parts.join("; ");
}
