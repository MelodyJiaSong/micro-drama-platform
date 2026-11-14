import type { TreeNode } from "../types";
import type { CutVersion, EpisodeCuts, EpisodeJoin } from "./sceneCuts";

/** 单集预览页（follow-up 326）：三模块剧一集的整集成片、各场剪辑、逐镜正式条与台词、审片结论、人物，一个链接看完。
 *  数据只读：filming.json、各镜 renders/ 的条与 review.md、/api/scene-cuts，以及可选的 `{集}/preview.json`。 */
export const EPISODE_PREVIEW_ROUTE = "/episode-preview";

/** 集目录名 `ep01`，或带后缀的 `ep01_largest_land_animals`（非短剧系列，follow-up 328）。 */
const EPISODE_PATH_RE = /^(ai_videos\/[^/]+)\/episodes\/(ep\d+(?:_[\w-]+)?)$/;
/** 教学视频的一个知识点 `edu_videos/<系列>/tNN_<slug>`（follow-up 339），只走成片模式。 */
const EDU_TOPIC_RE = /^(edu_videos\/[^/]+)\/(t\d+(?:_[\w-]+)?)$/;

export const isEduPath = (path: string): boolean => path.startsWith("edu_videos/");

export function episodePreviewHref(path: string): string {
  return `${EPISODE_PREVIEW_ROUTE}?${new URLSearchParams({ path })}`;
}

export function parseEpisodePath(path: string): { dramaPath: string; episode: string } | null {
  const clean = path.replace(/\/+$/, "");
  const m = EPISODE_PATH_RE.exec(clean) ?? EDU_TOPIC_RE.exec(clean);
  return m ? { dramaPath: m[1], episode: m[2] } : null;
}

/** `ep01_largest_land_animals` → 1 */
export function episodeNumber(episode: string): number {
  return Number(/^ep(\d+)/.exec(episode)?.[1] ?? NaN);
}

/** `{集}/preview.json`：这一集给人看的说明，全部可选。 */
export interface PreviewNotes {
  title?: string;
  tagline?: string;
  scenes?: Record<string, { title?: string; subtitle?: string; time?: string; summary?: string }>;
  /** 外语台词原文 → 中文意思 */
  glosses?: Record<string, string>;
  cast?: { name: string; role?: string; desc?: string; image?: string }[];
  /** `s1_st1` → 审片结论；verdict 缺省时按 review.md 的「状态：」推 */
  shots?: Record<string, { verdict?: Verdict; note?: string }>;
  notes?: { title: string; items: string[] }[];
  /** 成片模式（follow-up 328）：没有 filming.json 的系列（如真实尺度）给成片路径，页面按 items 时间线审片 */
  video?: string;
  duration?: number;
  chapters?: FilmChapter[];
  items?: FilmItem[];
  /** 时间线上的标记（片头卡、洞察卡等叠加物） */
  marks?: { t: number; label: string }[];
  /** 封面候选等图片 */
  images?: { path: string; caption?: string }[];
  links?: { label: string; path: string }[];
  /** 音频预览（follow-up 359 / 360）：出视频前的整集听感，`tools/audio_preview.py build` 写 `audio_preview[.<lang>].json`；
   *  有 audio 时播放器放音频，上方大图换成当前段的故事板，cues 是逐句字幕（秒） */
  audio?: string;
  cues?: { t: number; end: number; who?: string; text: string }[];
  /** 双语成片（edu_videos follow-up 006）：本页语言与可切换的语言版本 */
  lang?: string;
  languages?: { lang: string; label: string; preview: string }[];
}

/** 成片模式的说明数据文件：中文（缺省）`preview.json`，其他语言 `preview.<lang>.json`。 */
export function previewFile(path: string, lang?: string | null, audio = false): string {
  const base = audio ? "audio_preview" : "preview";
  return lang && lang !== "zh" && /^[a-z]{2}$/.test(lang) ? `${path}/${base}.${lang}.json` : `${path}/${base}.json`;
}

/** 整集音频预览（follow-up 359）：`/episode-preview?path=<集或知识点>&audio=1`。 */
export function audioPreviewHref(path: string, lang?: string | null): string {
  const q = new URLSearchParams({ path, audio: "1" });
  if (lang && lang !== "zh") q.set("lang", lang);
  return `${EPISODE_PREVIEW_ROUTE}?${q}`;
}

export interface FilmChapter { id: string; title: string; t: number }
/** 成片里的一段：t–end 秒；chapter 对应 chapters[].id；flag 是审片结论 */
export interface FilmItem {
  t: number; end: number; title: string; subtitle?: string; badge?: string; chapter?: string;
  note?: string; detail?: string; image?: string; flag?: Verdict;
}
export const FLAG_LABEL: Record<Verdict, string> = { ok: "通过", note: "有备注", redo: "要重做", pending: "未审" };

/** 成片第 t 秒落在哪一段（按 t 升序，取最后一个起点 ≤ t 的）。 */
export function filmIndexAt(t: number, items: FilmItem[]): number {
  let hit = -1;
  items.forEach((x, i) => { if (t >= x.t) hit = i; });
  return hit;
}

export type Verdict = "ok" | "note" | "redo" | "pending";
export const VERDICT_LABEL: Record<Verdict, string> = { ok: "保留", note: "保留 · 有备注", redo: "要重出", pending: "未审" };

/** review.md「状态：」一行 → 结论。 */
export function verdictFromStatus(status: string): Verdict {
  if (!status) return "pending";
  if (/重出|不通过|不保留/.test(status)) return "redo";
  if (/备注/.test(status)) return "note";
  if (/保留|通过/.test(status)) return "ok";
  return "pending";
}

export interface Line { who: string; how: string; text: string; foreign: boolean; gloss: string }

/** filming.json 的对白：`Riley（美式英语）：… / Felix（拉丁语，洪亮）：…`。括号里不写英语的当外语。 */
export function parseDialogue(dialogue: string, glosses: Record<string, string> = {}): Line[] {
  const out: Line[] = [];
  for (const part of dialogue.split(" / ").map(p => p.trim()).filter(Boolean)) {
    const m = /^([^（(：:]+)[（(]([^）)]*)[）)][：:]\s*(.*)$/.exec(part) ?? /^([^：:]+)[：:]\s*(.*)$/.exec(part);
    if (!m) continue;
    const [who, how, text] = m.length === 4 ? [m[1], m[2], m[3]] : [m[1], "", m[2]];
    const foreign = /拉丁语|希腊语|外语/.test(how);
    out.push({ who: who.trim(), how, text: text.trim(), foreign, gloss: glosses[text.trim()] ?? "" });
  }
  return out;
}

export interface FilmingShot { id: string; duration: number; dialogue?: string; action?: string }
export interface FilmingScene {
  id: string; location?: string; time?: string; purpose?: string; shots: FilmingShot[];
  groups?: { id: string; shots: string[] }[];
}

/** 镜组（follow-up 331）：这一镜在哪个镜组、在镜组条里从第几秒开始（前面成员镜头的时长之和）。 */
export function groupOf(scene: FilmingScene, shot: string): { id: string; offset: number } | null {
  const g = (scene.groups ?? []).find(x => x.shots.includes(shot));
  if (!g) return null;
  let offset = 0;
  for (const id of g.shots) {
    if (id === shot) break;
    offset += scene.shots.find(x => x.id === id)?.duration ?? 0;
  }
  return { id: g.id, offset };
}

export interface TakeFiles { name: string; video: string | null; review: string | null }

/** renders/ 子树（depth 2）→ 各条（新的在前），只收有 mp4 的条目录。 */
export function takesFromTree(node: TreeNode | null): TakeFiles[] {
  const dirs = (node?.children ?? []).filter(c => c.type === "directory" && /^\d{8}-\d{6}_/.test(c.name));
  return dirs.map(d => {
    const files = d.children ?? [];
    return {
      name: d.name,
      video: files.find(f => f.type !== "directory" && f.name.toLowerCase().endsWith(".mp4"))?.path ?? null,
      review: files.find(f => f.type !== "directory" && f.name === "review.md")?.path ?? null,
    };
  }).filter(t => t.video).sort((a, b) => b.name.localeCompare(a.name));
}

/** 用哪一条：本场最新正片剪辑里用到的那条优先，否则最新一条。 */
export function pickTake(takes: TakeFiles[], usedTake: string | null): TakeFiles | null {
  return (usedTake && takes.find(t => t.name === usedTake)) || takes[0] || null;
}

export function latest<T extends { version: number }>(items: T[] | undefined): T | null {
  return (items ?? []).reduce<T | null>((best, x) => (!best || x.version > best.version ? x : best), null);
}

export function latestSceneCut(cuts: EpisodeCuts | null, scene: string): CutVersion | null {
  return latest(cuts?.scenes.find(s => s.scene === scene)?.final);
}

export function latestJoin(cuts: EpisodeCuts | null): EpisodeJoin | null {
  return latest(cuts?.joined?.final);
}

export interface PlayShot { key: string; scene: string; shot: string }

/** 整集成片里的某一秒是哪场哪镜：场段起点（含叠化重叠）+ 本场剪辑里的镜头起点。 */
export function shotAt(t: number, join: EpisodeJoin | null, sceneCuts: Record<string, CutVersion | null>): PlayShot | null {
  if (!join) return null;
  let hit = null as null | { scene: string; local: number };
  for (const seg of join.segments) if (t >= seg.start) hit = { scene: seg.scene, local: t - seg.start };
  if (!hit) return null;
  const cut = sceneCuts[hit.scene];
  let shot = cut?.events[0]?.shot ?? "";
  for (const ev of cut?.events ?? []) if (hit.local >= ev.start) shot = ev.shot;
  return shot ? { key: `${hit.scene}_${shot}`, scene: hit.scene, shot } : null;
}

/** 某场某镜在整集成片里从第几秒开始（跳转用）。 */
export function shotStart(key: string, join: EpisodeJoin | null, sceneCuts: Record<string, CutVersion | null>): number | null {
  const [scene, shot] = key.split("_");
  const seg = join?.segments.find(s => s.scene === scene);
  const ev = sceneCuts[scene]?.events.find(e => e.shot === shot);
  return seg && ev ? seg.start + ev.start : null;
}

export function clock(seconds: number): string {
  const s = Math.max(0, Math.round(seconds));
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
}
