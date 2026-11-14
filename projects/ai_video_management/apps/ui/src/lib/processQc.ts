/** 流程与自检：仓库级（对所有剧生效）与剧级（只对一部剧生效）分开展示、不混。
 * 页面只读；「管理」＝ 复制一段写好的指令给 Claude Code / Codex 执行，规则文件只由代理改（日志与锁不被绕过）。 */

export const PROCESS_QC_REPO_PATH = "/workflow/qc";
export const PROCESS_QC_DRAMA_ROUTE = "/qc";
export const processQcDramaUrl = (drama: string): string => `${PROCESS_QC_DRAMA_ROUTE}?drama=${encodeURIComponent(drama)}`;
export const REPO_REGISTRY = ".agents/references/project/qc_checks.toml";
export const dramaRegistry = (drama: string): string => `${drama}/qc_checks.toml`;

export interface QcCheck {
  id: string; stage: string; kind: "machine" | "review"; gate: boolean; auto: boolean; level: string;
  when: string; desc: string; how: string; basis: string; sources: string[]; perspective?: string;
}
export interface QcDefect { ts: string; category: string; caught_by: string; artifact: string; followup: string; note: string }
export interface QcEscape extends QcDefect { reason: string; action: string; level: string }
export interface QcRender { path: string; artifact: string; verdicts: Record<string, string> }
export interface FollowupHealth { window_days: number; followups: number; logged: number; duplicates: number[]; pending: number; last_number: number }
export interface DramaQcSummary {
  drama: string; spec: string; enabled: boolean; drama_checks: number; defects: number; user_caught: number; false_positives: number;
  escape_rate: number | null; renders_total: number; followup: FollowupHealth;
}
export interface ProcessQcRepo { stages: string[]; checks: QcCheck[]; dramas: DramaQcSummary[] }
export interface ProcessQcDrama {
  drama: string; spec: string; enabled: boolean; stages: string[]; drama_checks: QcCheck[]; repo_checks: QcCheck[];
  defects: QcDefect[]; escapes: QcEscape[]; escape_rate: number | null; renders: QcRender[]; renders_total: number;
  followup: FollowupHealth;
}

export const STAGE_LABEL: Record<string, string> = {
  ref_image: "参考图", ref_audio: "原声", spec: "技能规格", prompt: "Prompt", keyframe: "关键帧",
  video: "出片", audio: "声音", cut: "剪辑成片",
};
export const stageLabel = (stage: string): string => STAGE_LABEL[stage] ?? stage;

/** 按流程顺序分组；登记表里出现了未知环节也照样列在最后，不吞掉。 */
export function byStage(checks: QcCheck[], stages: string[]): [string, QcCheck[]][] {
  const order = [...stages, ...checks.map(c => c.stage).filter(s => !stages.includes(s))];
  return [...new Set(order)].map(stage => [stage, checks.filter(c => c.stage === stage)] as [string, QcCheck[]]).filter(([, list]) => list.length);
}

export const percent = (rate: number | null): string => rate === null ? "—" : `${Math.round(rate * 100)}%`;

export function escapeInstruction(drama: string, e: QcEscape): string {
  const head = `在 ${drama} 处理一条用户抓到的缺陷（类别 ${e.category}，follow-up ${e.followup || "-"}）：原因「${e.reason}」，动作「${e.action}」。`;
  const tail = `改完用 python tools/followup.py 记录，并重跑 python tools/qc.py escapes ${drama.split("/").pop()}。`;
  // 这条检查若在仓库级，收紧它会影响所有剧：只给建议、等用户同意；本剧先在剧级加更严的补充检查兜住。
  return e.level === "仓库级"
    ? `${head}这条检查在仓库级 ${REPO_REGISTRY}，对所有剧生效：先给出修改建议，征得我同意后才改；同意前可以在本剧剧级登记表 ${dramaRegistry(drama)} 加一条更严的补充检查兜住。${tail}`
    : `${head}新增或修改的检查写进剧级登记表 ${dramaRegistry(drama)}，不要动仓库级 ${REPO_REGISTRY}。${tail}`;
}

export function promoteInstruction(drama: string, c: QcCheck): string {
  return `提议把 ${drama} 的剧级检查 ${c.id}（${c.desc}）升为仓库级。先列出它在其他剧也反复出现的证据（剧名 + follow-up 号）` +
    `和撑着它的共用依据，交给我确认；我明确同意之前不要改 ${REPO_REGISTRY}。同意后再迁移（两层 id 不许重复），写 basis，并记 follow-up 与 changelog。`;
}

export function reviewRepoInstruction(c: QcCheck): string {
  return `复核仓库级检查 ${c.id}（${c.desc}）：它对所有剧生效。核对依据「${c.basis || "未写"}」是否成立、各剧近期是否命中过、是否应收紧或降回剧级。` +
    `只给出结论和建议，改动 ${REPO_REGISTRY} 前必须先征得我同意。`;
}

export const PERSPECTIVE_LABEL: Record<string, string> = {
  character: "每个角色各审一次（立场与视线）", director: "导演", audience: "观众（不看规格）", fidelity: "原版还原",
};
