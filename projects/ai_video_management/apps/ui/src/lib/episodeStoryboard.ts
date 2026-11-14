/** 故事板审阅（follow-up 336）：剧页按场列出每镜最新的首帧图，给出片前最后一轮人工 review。
 *  图只认 `scenes/sN/shots/stN/planning/stN_first_frame.png`（后端 `first_frames` 给路径与修改时间）；
 *  `planning/_r1`、`_r2`、`_v2_old` 等旧版和 `_obsolete/` 下的旧镜组板、旧场故事板一律不当现行图。 */
import type { ReviewRunSummary } from "../api";
import type { EpisodeWorkflow, FilmingScene } from "./episodeWorkflow";

export interface FirstFrame { path: string; mtime: number; prompt: string }
export interface DialogueLine { speaker: string; direction: string; text: string }
export interface StoryboardShot {
  id: string; key: string; duration: number; cast: string[]; dialogue: DialogueLine[];
  action: string; beats: string; camera: string; blocking: string;
  /** 现行首帧图；还没出（或路径不合规）时为 null，页面显示「首帧待出」。 */
  image: { path: string; mtime: number } | null;
  framePrompt: string; packPrompt: string; shotDir: string;
}
export interface StoryboardScene {
  id: string; location: string; time: string; purpose: string; total: number; shots: StoryboardShot[];
}

/** 首帧图的固定位置：planning 目录下 `<st>_first_frame.png`，不能在任何子目录（_r1、_v2_old、_obsolete…）里。 */
export function isCurrentFirstFrame(path: string, episodePath: string, scene: string, shot: string): boolean {
  return path === `${episodePath}/scenes/${scene}/shots/${shot}/planning/${shot}_first_frame.png`;
}

/** 「Riley（压低声音，美式英语）：Okay…」按「 / 」拆成多句，每句分出说话人、表演提示与台词原文。 */
export function dialogueLines(dialogue: string): DialogueLine[] {
  return (dialogue || "").split(/\s+\/\s+|\n+/).map(part => part.trim()).filter(Boolean).map(part => {
    const m = /^([^（：:]{1,40}?)\s*(?:（(.*?)）)?\s*[：:]\s*(.+)$/s.exec(part);
    return m ? { speaker: m[1].trim(), direction: (m[2] || "").trim(), text: m[3].trim() } : { speaker: "", direction: "", text: part };
  });
}

/** 场按分镜（filming.json）里的顺序——就是故事顺序（如 s1 s2 s3 s4 s8 s5 s6 s7），镜头按场内顺序。 */
export function storyboardScenes(workflow: EpisodeWorkflow): StoryboardScene[] {
  const episodePath = workflow.episode_path;
  const filming = (workflow.modules.find(m => m.id === "filming")?.content.scenes || []) as FilmingScene[];
  return filming.map(scene => ({
    id: scene.id, location: scene.location, time: scene.time, purpose: scene.purpose,
    total: scene.shots.reduce((sum, shot) => sum + (Number(shot.duration) || 0), 0),
    shots: scene.shots.map(shot => {
      const key = workflow.shot_keys[scene.id]?.[shot.id] || `${scene.id}_${shot.id}`;
      const frame = workflow.first_frames?.[key];
      const current = frame?.path && isCurrentFirstFrame(frame.path, episodePath, scene.id, shot.id);
      const shotDir = `${episodePath}/scenes/${scene.id}/shots/${shot.id}`;
      return {
        id: shot.id, key, duration: shot.duration, cast: shot.cast || [], dialogue: dialogueLines(shot.dialogue),
        action: shot.action || "", beats: shot.beats || "", camera: shot.camera || "", blocking: shot.blocking || "",
        image: current ? { path: frame!.path, mtime: frame!.mtime } : null,
        framePrompt: frame?.prompt || "", packPrompt: workflow.packs?.[key]?.prompt || "", shotDir,
      };
    }),
  }));
}

/** 本场最新一张出片前审查单（stage=pregen，scenes 含本场；没写 scenes 的单视为覆盖全集）。 */
export function latestSceneReview(runs: ReviewRunSummary[], dramaPath: string, episode: string, scene: string): ReviewRunSummary | null {
  const mine = runs.filter(r => r.drama === dramaPath && r.episode.toLowerCase() === episode.toLowerCase() && r.stage === "pregen"
    && (!r.scenes?.length || r.scenes.includes(scene)));
  return mine.sort((a, b) => b.created_at.localeCompare(a.created_at))[0] ?? null;
}

export function reviewChipText(run: ReviewRunSummary | null): string {
  if (!run) return "未审";
  return `出片前审查 第 ${run.loop}/${run.max_loops ?? 3} 轮 · ${run.state}${run.state === "进行中" ? `（${run.done}/${run.total}）` : ""}`;
}

export function reviewChipTone(run: ReviewRunSummary | null): "none" | "open" | "done" | "void" {
  if (!run) return "none";
  if (run.state === "已作废") return "void";
  return run.state === "进行中" ? "open" : "done";
}
