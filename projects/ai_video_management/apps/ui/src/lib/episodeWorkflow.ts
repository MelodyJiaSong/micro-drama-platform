import { ApiError } from "../types";

export type ModuleId = "story" | "filming" | "prompts";
export interface Shot {
  id: string;
  duration: number;
  action: string;
  camera: string;
  dialogue: string;
}
export interface FilmingScene {
  id: string;
  background: string;
  location: string;
  time: string;
  purpose: string;
  shots: Shot[];
}
export interface PromptScene {
  id: string;
  shots: { id: string; text: string }[];
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
}

async function read<T>(response: Response): Promise<T> {
  const data = await response.json();
  if (!response.ok) throw new ApiError(response.status, data.detail?.message || `HTTP ${response.status}`, data.detail);
  return data as T;
}

export async function loadWorkflow(path: string): Promise<EpisodeWorkflow> {
  return read(await fetch(`/api/episode-workflow?episode_path=${encodeURIComponent(path)}`, { cache: "no-store" }));
}

export async function changeWorkflow(path: string, module: WorkflowModule, operation: "save" | "approve" | "compile", content?: ModuleContent): Promise<void> {
  await read(await fetch("/api/episode-workflow", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ episode_path: path, module: module.id, operation, expected: module.etag, source: module.input_revision, content }),
  }));
}
