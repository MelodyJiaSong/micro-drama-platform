export type StoryFrame = Record<"who" | "what" | "why" | "when" | "where" | "how", string>;
export interface RunSummary {
  run_id: string; created_at: string; status: string;
  participant_count: number; proposal_count: number; input_hash: string;
  title?: string; audit_path?: string; audit_folder?: string; rules_hash?: string; selected?: boolean;
}
export interface RunSelection {
  run_id: string; status: "selected" | "stale"; candidate_hash?: string;
  input_hash?: string; story_revision?: string; promoted_at?: string; history?: unknown[];
}
export interface StoryRunIndex { episode_path: string; runs: RunSummary[]; selection?: RunSelection | null; }
export interface StoryParticipant {
  id: string; name: string; role: string; scope: "story" | "implementation";
  runtime_id?: string; model?: string; status: string; started_at?: string; finished_at?: string;
  prompt: string; output: string;
}
export interface StoryProposal {
  id: string; agent_id: string; title: string; detail: string; reason: string; location: string;
  decision: "accepted" | "rejected" | "partial" | "deferred";
  decision_reason: string; decided_by: string; criteria: unknown[]; evidence: unknown[]; applied_in: unknown;
}
export interface StoryEvent {
  id: string; at: string; actor: string; type: string; title: string; body: string;
  proposal_ids: string[]; artifact_refs: unknown[];
}
export interface RunArtifact {
  id: string; kind: "input" | "output" | "process"; scope: "run" | "shared" | "canonical";
  name: string; path: string; sha256?: string; status?: string;
}
export interface StoryRun {
  schema_version: number; run_id: string; episode_path: string; created_at: string; status: string;
  input: { frame: StoryFrame; brief: string; assumptions: unknown[]; sources: unknown[];
    rules: unknown[]; input_hash: string; independence: unknown; prior_accepted_state?: unknown[]; criteria?: string[] };
  participants: StoryParticipant[]; events: StoryEvent[]; proposals: StoryProposal[];
  candidate: { title?: string; frame: StoryFrame; brief: string; text: string; state_changes: unknown[] };
  artifacts: RunArtifact[]; publication?: unknown;
  io?: { items: RunIoItem[]; audit_path: string; coverage: string };
}
export interface RunIoItem {
  id: string; group: string; group_label: string; name: string; value: unknown;
  target: string; snapshot_hash: string; note: string; scope: string; kind: "input" | "output" | "process";
  source_path?: string; source_hash?: string; selection?: string;
  global_source_id?: string;
  source_status?: { status: "same" | "changed" | "missing" | "unavailable" | "unverified"; sha256?: string };
}
export interface StoryInputProfile { id: string; label: string; input_path: string; rules_path: string; input_hash: string; rules_hash: string; }
export interface SharedStoryInput {
  episode_path: string; selected_profile: string; profile_id: string;
  profiles: StoryInputProfile[]; input: StoryRun["input"];
}
async function get<T>(path: string, signal: AbortSignal): Promise<T> {
  const response = await fetch(path, { cache: "no-store", signal });
  if (!response.ok) {
    let detail: string | undefined;
    try { const data = await response.json(); detail = data.detail?.message; } catch { /* Non-JSON server error. */ }
    throw new Error(detail || `HTTP ${response.status}`);
  }
  return response.json() as Promise<T>;
}
export function listStoryRuns(episode: string, signal: AbortSignal): Promise<StoryRunIndex> {
  return get(`/api/story-runs?${new URLSearchParams({ episode_path: episode })}`, signal);
}
export function loadStoryInput(episode: string, profile: string, signal: AbortSignal): Promise<SharedStoryInput> {
  const params = new URLSearchParams({ episode_path: episode });
  if (profile) params.set("profile_id", profile);
  return get(`/api/story-input?${params}`, signal);
}
export function loadStoryRun(episode: string, run: string, signal: AbortSignal): Promise<StoryRun> {
  return get(`/api/story-runs/detail?${new URLSearchParams({ episode_path: episode, run_id: run })}`, signal);
}
