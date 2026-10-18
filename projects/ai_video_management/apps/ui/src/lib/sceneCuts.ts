import { ApiError } from "../types";

/** 剪辑模块（follow-up 269）：每场的剪辑决定分草稿剪辑（480p 草稿条）与正片剪辑（720p 正式条）。 */
export type CutStage = "draft" | "final";
export const CUT_STAGES: CutStage[] = ["draft", "final"];
export const CUT_STAGE_LABEL: Record<CutStage, string> = { draft: "草稿剪辑", final: "正片剪辑" };

export interface CutEvent {
  shot: string;
  start: number;
  duration: number;
  placeholder: boolean;
  take: string;
  cut_in: number | null;
  cut_out: number | null;
  audio_in: number | null;
  audio_out: number | null;
  reason: string;
  notes: string[];
  text: string[];
}
export interface CutViolation { shot?: string; what?: string; why?: string }
export interface CutVersion {
  version: number;
  stage: CutStage;
  phase: string;
  status: string;
  path: string;
  approved_by: string | null;
  made_by: string;
  base_version: number | null;
  video: string;
  labeled_video: string;
  duration: number;
  rendered_at: string;
  shots: number;
  placeholders: number;
  events: CutEvent[];
  notes: string[];
  violations: CutViolation[];
  error: string;
}
export interface SceneCuts { scene: string; label: string; draft: CutVersion[]; final: CutVersion[] }
/** 集级剪辑（follow-up 278）：把各场接起来的成片、转场、独立审稿结论。 */
export const EPISODE_CUT = "episode";
export interface JoinSegment { scene: string; cut_version: number; start: number; duration: number }
export interface JoinTransition {
  from_scene: string; to_scene: string; type: string; name: string; duration: number; at: number;
  audio_j: number | null; audio_l: number | null; reason: string;
}
export interface EpisodeJoin {
  version: number; stage: CutStage; phase: string; status: string; path: string; approved_by: string | null; base_version: number | null;
  video: string; duration: number; rendered_at: string; head: string; tail: string;
  segments: JoinSegment[]; transitions: JoinTransition[];
  review_verdict: string; review_stale: boolean; review_items: string[]; changes: string[]; note: string; error: string;
}
export interface GalleryEntry { start: number; label: string }
export interface Gallery { from_scene: string; to_scene: string; video: string; entries: GalleryEntry[] }
export interface EpisodeCuts {
  episode_path: string; scenes: SceneCuts[];
  joined: Record<CutStage, EpisodeJoin[]>; galleries: Record<CutStage, Gallery[]>;
}

export async function loadSceneCuts(episodePath: string): Promise<EpisodeCuts> {
  const response = await fetch(`/api/scene-cuts?episode_path=${encodeURIComponent(episodePath)}`, { cache: "no-store" });
  const data = await response.json();
  if (!response.ok) throw new ApiError(response.status, data.detail?.message || `HTTP ${response.status}`, data.detail);
  return data as EpisodeCuts;
}

/** 秒数写成 m:ss.s，时间线与成片对得上。 */
export function cutClock(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = seconds - m * 60;
  return `${m}:${s < 10 ? "0" : ""}${s.toFixed(1)}`;
}
