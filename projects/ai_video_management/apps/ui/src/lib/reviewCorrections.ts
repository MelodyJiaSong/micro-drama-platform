// 修复页（用户 2026-11-08「每一次审计的结果应该 link 到另一个 page……correction，基于 review，我们修复了那些……两边是关联的」）。
// 数据是 `python tools/review_run.py corrections <审查单>` 写的 corrections.json：每个有方案的问题（编号、级别、类别·维度、镜头、问题、
// 方案、状态、谁何时、改了的文件、下一轮复核结果），每镜首帧前后（审查时那张 → 现在 / 下一轮那张）、分镜文字逐字段 diff。本站只读。
import { LEVELS, FIX_STATUS } from "./reviewV5";

export const REVIEW_CORRECTIONS_ROUTE = "/review-run/corrections";
export const CORRECTIONS_JSON = "corrections.json";
export const VERIFY = ["已复核通过", "复核仍有问题", "待复核"] as const;
export type VerifyStatus = typeof VERIFY[number];

export interface CorrectionFilter { level?: string; status?: string; scene?: string; verify?: string }
export const reviewCorrectionsHref = (dir: string, filter: CorrectionFilter = {}): string => {
  const q = new URLSearchParams({ path: dir });
  for (const [k, v] of Object.entries(filter)) if (v) q.set(k, v);
  return `${REVIEW_CORRECTIONS_ROUTE}?${q}`;
};
export const correctionsCommand = (dir: string): string => `python tools/review_run.py corrections ${dir}`;

export interface FrameVersion { path: string; label: string; sha256: string; mtime: string; mtime_ms?: number; how?: string }
export interface SpecField { field: string; name: string; before: string; after: string; diff: string[] }
export interface ShotCorrection {
  key: string; scene: string; shot: string; issues: string[];
  frame: { before: FrameVersion | null; after: FrameVersion | null; changed: boolean; note?: string };
  spec: { before_source: string; after_source: string; changed: boolean; fields: SpecField[]; removed?: boolean; added?: boolean };
  prompt?: { before_source: string; after_source: string; changed: boolean; diff: string[] };
  manual_frames?: { before: string; after: string }[];
}
export interface Verification { status: VerifyStatus | string; run?: string; how: string[]; rows?: string[] }
export interface Correction {
  id: string; level: string; law: string; category: string; item: string; dimension: string; shots: string[]; keys: string[]; scenes: string[];
  problem: string; fix?: string; solution: string; status: string; reason?: string; cost?: string; solution_source?: string; solution_line?: string;
  history: { at: string; status: string; by?: string; files?: string[] }[]; files: string[]; frames: { before: string; after: string }[];
  frame_pending?: string[]; verification: Verification;
}
export interface CorrectionsDoc {
  generated_at?: string; run: string; dir: string; title: string; loop?: number; parent?: string; child?: string; child_state?: string;
  issues_source: string; changes_md?: string; has_snapshot?: boolean;
  summary: {
    issues: number; corrections: number; by_level: Record<string, number>; by_status: Record<string, number>; by_verification: Record<string, number>;
    shots: number; frames_changed: number; specs_changed: number; shots_touched?: number;
  };
  corrections: Correction[]; shots: ShotCorrection[];
}

export const verifyClass = (v: string): string => v === "已复核通过" ? "rc-v-ok" : v === "复核仍有问题" ? "rc-v-bad" : "rc-v-wait";

/** 一镜有没有可看的改动：首帧换了、分镜改了，或有方案指到这一镜。 */
export const shotTouched = (s: ShotCorrection): boolean => s.frame.changed || s.spec.changed || Boolean(s.prompt?.changed) || s.issues.length > 0;

const LEVEL_RANK = (l: string): number => { const i = (LEVELS as readonly string[]).indexOf(l); return i < 0 ? 9 : i; };
const idNum = (id: string): number => Number(/\d+/.exec(id)?.[0] ?? 0);

export function matchCorrection(c: Correction, f: CorrectionFilter): boolean {
  return (!f.level || c.level === f.level) && (!f.status || c.status === f.status) && (!f.verify || c.verification.status === f.verify)
    && (!f.scene || c.scenes.includes(f.scene));
}
export const anyFilter = (f: CorrectionFilter): boolean => Boolean(f.level || f.status || f.verify);

export interface ShotGroup { shot: ShotCorrection; corrections: Correction[] }
export interface SceneGroup { scene: string; shots: ShotGroup[]; loose: Correction[] }
/** 按场 → 镜分组。每镜带指到它的方案（按严重在前）；没指到镜头的方案（整场 / 维度问题）挂在场的「整场」卡。
 *  有级别 / 状态 / 复核筛选时，只留有命中方案的镜；没筛选时，首帧或分镜改过的镜也列出（哪怕没有方案指到它）。 */
export function groupCorrections(doc: CorrectionsDoc, f: CorrectionFilter): SceneGroup[] {
  const byId = new Map(doc.corrections.map(c => [c.id, c]));
  const sort = (xs: Correction[]): Correction[] => [...xs].sort((a, b) => LEVEL_RANK(a.level) - LEVEL_RANK(b.level) || idNum(a.id) - idNum(b.id));
  const scenes = [...new Set([...doc.shots.map(s => s.scene), ...doc.corrections.flatMap(c => c.scenes)])];
  const out: SceneGroup[] = [];
  for (const scene of scenes) {
    if (f.scene && scene !== f.scene) continue;
    const shots: ShotGroup[] = [];
    for (const shot of doc.shots.filter(s => s.scene === scene)) {
      const cs = sort(shot.issues.map(id => byId.get(id)).filter((c): c is Correction => Boolean(c)).filter(c => matchCorrection(c, f)));
      if (anyFilter(f) ? cs.length > 0 : shotTouched(shot)) shots.push({ shot, corrections: cs });
    }
    const loose = sort(doc.corrections.filter(c => !c.keys.length && c.scenes.includes(scene) && matchCorrection(c, f)));
    if (shots.length || loose.length) out.push({ scene, shots, loose });
  }
  return out;
}

/** 落不到任何场的方案（审查单范围外、镜头写法认不出）。 */
export const orphanCorrections = (doc: CorrectionsDoc, f: CorrectionFilter): Correction[] =>
  doc.corrections.filter(c => !c.keys.length && !c.scenes.length && matchCorrection(c, f));

export function countBy(cs: Correction[]): { level: Record<string, number>; status: Record<string, number>; verify: Record<string, number> } {
  const level: Record<string, number> = Object.fromEntries(LEVELS.map(l => [l, 0]));
  const status: Record<string, number> = Object.fromEntries(FIX_STATUS.map(s => [s, 0]));
  const verify: Record<string, number> = Object.fromEntries(VERIFY.map(v => [v, 0]));
  for (const c of cs) { level[c.level] = (level[c.level] ?? 0) + 1; status[c.status] = (status[c.status] ?? 0) + 1; verify[c.verification.status] = (verify[c.verification.status] ?? 0) + 1; }
  return { level, status, verify };
}

/** unified diff 的一行 → 显示类型。 */
export const diffKind = (line: string): "add" | "del" | "hunk" | "ctx" =>
  line.startsWith("@@") ? "hunk" : line.startsWith("+") ? "add" : line.startsWith("-") ? "del" : "ctx";

/** 循环条：本轮审查 → 修复 → 下一轮复核，标出现在到哪一步。 */
export const LOOP_CORR = ["本轮审查", "修复", "下一轮复核"] as const;
export function correctionsStep(doc: CorrectionsDoc | null): number {
  if (!doc) return 0;
  if (doc.child && doc.summary.corrections && doc.summary.by_verification["待复核"] < doc.summary.corrections) return 2;
  return 1;
}
