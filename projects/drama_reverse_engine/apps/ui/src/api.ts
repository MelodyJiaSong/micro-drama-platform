export interface EpisodeStatus {
  episode_rel_dir: string;
  stage: string;
  failed_reason: string | null;
  gate_hold: boolean;
  busy: boolean;
  shot_count: number;
  degradations: string[];
  artifacts: { script: boolean; dialogue: boolean; novel: boolean; prompts: boolean };
}

export interface DramaNode {
  drama_id: string;
  title: string;
  gate_a_enabled: boolean;
  gate_b_enabled: boolean;
  children: EpisodeStatus[];
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const resp = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!resp.ok) {
    const detail = await resp.json().catch(() => ({ detail: resp.statusText }));
    throw new Error(detail.detail ?? resp.statusText);
  }
  return resp.json() as Promise<T>;
}

async function multipart<T>(url: string, form: FormData): Promise<T> {
  const resp = await fetch(url, { method: "POST", body: form });
  if (!resp.ok) {
    const detail = await resp.json().catch(() => ({ detail: resp.statusText }));
    throw new Error(detail.detail ?? resp.statusText);
  }
  return resp.json() as Promise<T>;
}

function uploadRequest(dramaId: string, file: File): Promise<{ episodes: string[] }> {
  const form = new FormData();
  form.append("file", file);
  return multipart(`/api/dramas/${encodeURIComponent(dramaId)}/upload`, form);
}

function uploadNewRequest(file: File, declarationAccepted: boolean, title: string):
  Promise<{ drama_id: string; title: string; episodes: string[] }> {
  const form = new FormData();
  form.append("file", file);
  form.append("declaration_accepted", String(declarationAccepted));
  form.append("declared_by", "operator");
  form.append("title", title);
  return multipart("/api/uploads", form);
}

export const api = {
  tree: () => request<{ dramas: DramaNode[] }>("/api/dramas"),
  createDrama: (body: object) => request("/api/dramas", { method: "POST", body: JSON.stringify(body) }),
  uploadSource: uploadRequest,
  uploadNewDrama: uploadNewRequest,
  step: (drama_id: string, episode_rel_dir: string) =>
    request("/api/episodes/step", { method: "POST", body: JSON.stringify({ drama_id, episode_rel_dir }) }),
  run: (drama_id: string, episode_rel_dir: string) =>
    request("/api/episodes/run", { method: "POST", body: JSON.stringify({ drama_id, episode_rel_dir }) }),
  releaseGate: (drama_id: string, episode_rel_dir: string) =>
    request("/api/episodes/gate/release", { method: "POST", body: JSON.stringify({ drama_id, episode_rel_dir }) }),
  rerunStage: (drama_id: string, episode_rel_dir: string, stage: string) =>
    request("/api/episodes/rerun-stage", { method: "POST", body: JSON.stringify({ drama_id, episode_rel_dir, stage }) }),
  artifact: (rel_path: string) =>
    request<{ rel_path: string; content: string }>(`/api/artifacts?rel_path=${encodeURIComponent(rel_path)}`),
  shotFiles: (episode_rel_dir: string) =>
    request<{ shot_files: string[] }>(`/api/episodes/shot-files?episode_rel_dir=${encodeURIComponent(episode_rel_dir)}`),
  editArtifact: (episode_rel_dir: string, artifact_rel_path: string, content: string) =>
    request("/api/episodes/edit-artifact", {
      method: "POST", body: JSON.stringify({ episode_rel_dir, artifact_rel_path, content }),
    }),
};
