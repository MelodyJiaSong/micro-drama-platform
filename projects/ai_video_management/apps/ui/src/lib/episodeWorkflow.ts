import { ApiError } from "../types";

export type ModuleId = "story" | "filming" | "prompts";
/** Stages after Prompt 编译与出片 are placeholders until designed: no episode documents yet. */
export type PlaceholderStageId = "edit" | "sound" | "delivery";
export type StageId = ModuleId | PlaceholderStageId;
export const PLACEHOLDER_STAGES: PlaceholderStageId[] = ["edit", "sound", "delivery"];
export const isPlaceholderStage = (id: string | null): id is PlaceholderStageId => PLACEHOLDER_STAGES.includes(id as PlaceholderStageId);
export interface Shot {
  id: string;
  duration: number;
  action: string;
  camera: string;
  dialogue: string;
  /** Asset keys of the people in frame (`c1-1`, `c14`), plus blocking, timed beats and light (follow-up 227). */
  cast: string[];
  blocking: string;
  beats: string;
  lighting: string;
  /** Story props in frame by prop key (`p475`); each prop's anchor image joins the 参考 line (follow-up 231). */
  props?: string[];
  /** Background view for this shot only (`bg1-13`), when it faces away from the scene's background (follow-up 261). */
  background?: string;
}
export interface FilmingScene {
  id: string;
  background: string;
  location: string;
  time: string;
  purpose: string;
  shots: Shot[];
}
/** One referenced file, in upload order. v7 names it by key id (`key=>@` on the 参考 line); v5/v6 used tag. */
export interface PromptRef {
  key?: string;
  tag?: string;
  kind: "image" | "video" | "audio";
  role: string;
  path: string;
}
/** A shot's 资料包: copies of every referenced file, kept in sync with the sources (follow-up 229). */
export interface ShotPack {
  status: "ok" | "stale" | "invalid" | "missing";
  path: string;
  prompt: string;
  reason: string;
  files: { tag: string; key: string; kind: "image" | "video" | "audio"; role: string; path: string; src: string }[];
}
export interface PromptScene {
  id: string;
  shots: { id: string; text: string; refs?: PromptRef[] }[];
}
export interface ModuleContent {
  brief?: string;
  text?: string;
  scenes?: FilmingScene[] | PromptScene[];
}
export interface WorkflowModule {
  id: ModuleId;
  label: string;
  status: "empty" | "draft" | "approved" | "stale" | "blocked";
  etag: string;
  revision: string;
  input_revision: string | null;
  source_revision: string | null;
  can_edit: boolean;
  content: ModuleContent;
}
export interface EpisodeWorkflow {
  episode_path: string;
  modules: WorkflowModule[];
  shot_keys: Record<string, Record<string, string>>;
  packs?: Record<string, ShotPack>;
  renders?: Record<string, ShotTake[]>;
}
/** One generation of a shot: its folder under renders/ with the video, record and review (follow-up 230). */
export interface ShotTake {
  id: string;
  path: string;
  videos: string[];
  review: string;
  review_path: string;
  review_status: string;
  /** stage: draft＝低价草稿（用户审过才能出正式条），final＝正式条，from_take＝它出自哪条草稿（follow-up 265） */
  generation: { submit_id?: string; model?: string; stage?: "draft" | "final"; duration_s?: number; ratio?: string; resolution?: string;
    credits?: number; downloaded_at?: string; from_take?: string };
  prompt_path: string;
}

async function read<T>(response: Response): Promise<T> {
  const data = await response.json();
  if (!response.ok) throw new ApiError(response.status, data.detail?.message || `HTTP ${response.status}`, data.detail);
  return data as T;
}

export async function loadWorkflow(path: string): Promise<EpisodeWorkflow> {
  return read(await fetch(`/api/episode-workflow?episode_path=${encodeURIComponent(path)}`, { cache: "no-store" }));
}

/** 用户对草稿条的结论（follow-up 265）：「通过」后才能用它出正式条。 */
export async function judgeTake(takePath: string, verdict: "通过" | "不通过"): Promise<{ review_status: string }> {
  return read(await fetch("/api/shot-take/verdict", {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ take_path: takePath, verdict }),
  }));
}

export async function changeWorkflow(path: string, module: WorkflowModule, operation: "save" | "approve" | "compile", content?: ModuleContent): Promise<void> {
  await read(await fetch("/api/episode-workflow", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ episode_path: path, module: module.id, operation, expected: module.etag, source: module.input_revision, content }),
  }));
}
