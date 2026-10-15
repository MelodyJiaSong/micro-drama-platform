export type TreeNodeType =
  | "section"
  | "workflow"
  /** A series folder (`ai_videos/{s}/series.json`) — its children are dramas. */
  | "series"
  | "directory"
  | "file"
  | "image"
  | "video"
  | "audio"
  | "pdf"
  /** A 3D white model (`.glb` / `.gltf`) — previewed in <model-viewer>. */
  | "model";

export interface TreeNode {
  type: TreeNodeType;
  name: string;
  path: string;
  children?: TreeNode[];
  /** Client-side navigation destination; filesystem nodes omit this. */
  navigation_href?: string;
  /** True on a drama root. A drama is `ai_videos/{drama}` when flat and
   *  `ai_videos/{series}/{drama}` inside a series, so path depth is NOT a
   *  reliable test — always use this flag. */
  is_drama?: boolean;
  workflow?: "three-module-v1";
  /** True when this folder — or, for a drama, its series folder — holds an
   *  `OBSOLETE.md`: made with or only serving the removed old pipeline, kept for
   *  reference (follow-up 233). Rendered as the「已过时」badge. */
  obsolete?: boolean;
  /** Path of the `OBSOLETE.md` that marks this node (only on `obsolete` nodes). */
  obsolete_note?: string;
  drama_path?: string;
  workflow_module?: "story" | "filming" | "prompts" | "edit" | "sound" | "delivery";
  workflow_episode?: string;
  episode_path?: string;
  lifetime?: "persistent" | "transient" | "workspace";
  /** True when this leaf is a cross-episode shortcut (`*.link.json`). `path`
   *  already points at the real asset, so preview/download need no special
   *  case — only the label does. */
  is_link?: boolean;
  /** Where the `*.link.json` manifest itself lives (only on `is_link` nodes). */
  link_at?: string;
  /** Why the shortcut exists, shown as the link leaf's tooltip. */
  link_note?: string;
  /** Chinese (or otherwise human-friendly) label rendered in place of `name` when present: a drama's README H1 title, a library folder's label, a keyed asset's `{key} {rest}`. */
  display_name?: string;
}

export interface FileResult {
  path: string;
  content: string;
  encoding: string;
  bytes: number;
  mtime: number;
  mtime_http: string;
}

export interface ApiErrorDetail {
  kind: string;
  [key: string]: unknown;
}

export class ApiError extends Error {
  readonly status: number;
  readonly detail: ApiErrorDetail | null;

  constructor(status: number, message: string, detail: ApiErrorDetail | null) {
    super(message);
    this.status = status;
    this.detail = detail;
  }
}
