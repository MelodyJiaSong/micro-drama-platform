// 审查单 v5（tools/review_run.py，用户 2026-11-08）：每个审稿项默认一位 Kimi 按该类 rubric 每维 0–3 打分；旧双审记录仍可显示，
// 旧双审两位都勾后自动对比（reconcile/<代号>.md），分歧与抽查交裁决人；全部完成后推出分级问题清单（issues.json），逐条记方案、实施，
// 严重与主要都处理完才开下一轮复核。本站只读：打勾、裁决、fix 都由 review_run.py 写。没有 slots 的 v2 单不走这里。
import {
  agentKind, modelShort, type AgentDispatch, type ReviewItem, type ReviewRun, type ReviewSlot, type RubricDim,
} from "./reviewRun";

export const REVIEW_ISSUES_ROUTE = "/review-run/issues";
export const ISSUES_JSON = "issues.json";
export const ISSUES_MD = "issues.md";

export interface IssueFilter { level?: string; status?: string; category?: string; scene?: string }
export const reviewIssuesHref = (dir: string, filter: IssueFilter = {}): string => {
  const q = new URLSearchParams({ path: dir });
  for (const [k, v] of Object.entries(filter)) if (v) q.set(k, v);
  return `${REVIEW_ISSUES_ROUTE}?${q}`;
};

export const isV5Item = (item: ReviewItem): boolean => Boolean(item.slots && Object.keys(item.slots).length);
export const isV5Run = (run: ReviewRun): boolean => run.items.some(isV5Item);

/** 一位审稿人的简称：「Kimi · kimi」。 */
export const slotWho = (s: { runner: string; model: string }): string => `${agentKind(s.runner)} · ${modelShort(s.model)}`;
export const slotMark = (s: { status: string }): string => s.status === "done" ? "✓" : s.status === "failed" ? "!" : "○";
export const slotStatusText = (s: ReviewSlot): string =>
  s.status === "done" ? (s.attested ? "已勾（凭运行日志代登记）" : "已勾") : s.status === "failed" ? "失败" : "未交";
export const slotsOf = (item: ReviewItem): ReviewSlot[] => Object.values(item.slots ?? {}).sort((a, b) => a.slot.localeCompare(b.slot));
export const itemMark = (item: ReviewItem): string =>
  item.status === "done" ? "✓" : item.status === "failed" ? "!" : item.status === "adjudicating" ? "⚖" : "○";

// —— rubric 评分 ——

export const SCORE_TEXT: Record<string, string> = { 0: "没查或查不了", 1: "有问题", 2: "基本没问题", 3: "没问题" };
export const scoreClass = (n?: number | null): string => (n === undefined || n === null ? "rv-sna" : `rv-s${n}`);

/** 一项在某一维上的分：两位都勾后取对比表（item.scores），只勾了一位时取那一位自己的分。 */
export interface DimCell {
  item: string; a?: number; a_ev?: string; b?: number; b_ev?: string; final?: number | null;
  verdict?: string; judge_reason?: string; awaitingJudge: boolean;
}
export function dimCell(item: ReviewItem, dim: string): DimCell {
  const r = item.scores?.[dim];
  if (r) {
    // 一致的维度在裁决前 final 还是 null（review_run.py finalize 才填），先显示取的低分 agreed。
    return { item: item.id, a: r.a, a_ev: r.a_ev, b: r.b, b_ev: r.b_ev, final: r.final ?? (r.verdict === "一致" ? r.agreed : null), verdict: r.verdict, judge_reason: r.judge_reason,
      awaitingJudge: r.final === null && (r.verdict === "分歧" || r.verdict === "抽查") };
  }
  const a = item.slots?.a?.scores?.[dim]; const b = item.slots?.b?.scores?.[dim];
  return { item: item.id, a: a?.score, a_ev: a?.evidence, b: b?.score, b_ev: b?.evidence, final: undefined, awaitingJudge: false };
}

export interface RubricRow { dim: RubricDim; cells: DimCell[]; disputed: number; audited: number; low: number }
/** 这一类的评分表：一维一行，每个审稿项（physics_A…）三列 a 分 / b 分 / 最终。维度以审查单为准，没有就退回名册。 */
export function rubricRows(items: ReviewItem[], roster?: RubricDim[]): RubricRow[] {
  const dims = items.find(i => i.rubric?.length)?.rubric ?? roster ?? [];
  return dims.map(dim => {
    const cells = items.map(i => dimCell(i, dim.id));
    return { dim, cells, disputed: cells.filter(c => c.verdict === "分歧").length, audited: cells.filter(c => c.verdict === "抽查").length,
      low: cells.filter(c => typeof c.final === "number" && c.final <= 1).length };
  });
}

/** 这一类的两位审稿人：名册 reviewers 为准，其次审查单里第一项的 slots。 */
export function lawReviewers(items: ReviewItem[], roster?: { slot: string; runner: string; model: string }[]): { slot: string; runner: string; model: string }[] {
  if (roster?.length) return roster;
  const first = items.find(isV5Item);
  return first ? slotsOf(first).map(s => ({ slot: s.slot, runner: s.runner, model: s.model })) : [];
}

/** v5 实际跑的 agent：按位（a / b / 裁决）× 模型合并，打勾的那位算一次「打勾」。 */
export function slotTally(items: ReviewItem[]): { who: string; slot: string; count: number; ticked: number }[] {
  const out = new Map<string, { who: string; slot: string; count: number; ticked: number }>();
  const add = (slot: string, list: AgentDispatch[] | undefined, fallback: { runner: string; model: string }, done: boolean): void => {
    const runs = list?.length ? list : done ? [fallback] : [];
    runs.forEach((a, n) => {
      const who = slotWho(a); const key = `${slot}|${who}`;
      const row = out.get(key) ?? { who, slot, count: 0, ticked: 0 };
      row.count += 1; if (done && n === runs.length - 1) row.ticked += 1;
      out.set(key, row);
    });
  };
  for (const i of items) {
    for (const s of slotsOf(i)) add(s.slot, s.agents as AgentDispatch[] | undefined, s, s.status === "done");
    if (i.judge) add("裁决", i.judge.agents, i.judge, i.judge.status === "done");
  }
  return [...out.values()];
}

// —— 问题清单（issues.json） ——

export const LEVELS = ["critical", "major", "verify", "minor"] as const;
export type IssueLevel = typeof LEVELS[number];
export const LEVEL_NAME: Record<string, string> = { critical: "严重", major: "主要", verify: "待核实", minor: "记录" };
export const FIX_STATUS = ["open", "planned", "implemented", "wontfix"] as const;
export const STATUS_NAME: Record<string, string> = { open: "未处理", planned: "已定方案", implemented: "已实施", wontfix: "不改" };

export interface IssueHistory { at: string; status: string; solution: string; reason?: string }
export interface Issue {
  id: string; key: string; level: IssueLevel; law: string; category: string; item: string; dimension: string; shots: string[];
  problem: string; evidence: string[]; sources: string[]; fix: string; cost: string; severity?: string;
  scores?: { a: number; b: number; final: number }; rows?: string[];
  status: string; solution?: string; reason?: string; history?: IssueHistory[];
}
export interface IssuesDoc { run?: string; generated_at?: string; issues: Issue[] }

/** 与 review_run.py resolved() 同一规则：implemented，或 wontfix 且写了理由。 */
export const resolvedIssue = (i: Issue): boolean => i.status === "implemented" || (i.status === "wontfix" && Boolean((i.reason ?? "").trim()));
export const blocksNextRound = (i: Issue): boolean => (i.level === "critical" || i.level === "major") && !resolvedIssue(i);

export function issueCounts(issues: Issue[]): { level: Record<string, number>; status: Record<string, number>; total: number; blocking: number } {
  const level: Record<string, number> = Object.fromEntries(LEVELS.map(l => [l, 0]));
  const status: Record<string, number> = Object.fromEntries(FIX_STATUS.map(s => [s, 0]));
  for (const i of issues) { level[i.level] = (level[i.level] ?? 0) + 1; status[i.status] = (status[i.status] ?? 0) + 1; }
  return { level, status, total: issues.length, blocking: issues.filter(blocksNextRound).length };
}

const idNum = (id: string): number => Number(/\d+/.exec(id)?.[0] ?? 0);
/** 严重在前，同级按编号。 */
export const sortIssues = (issues: Issue[]): Issue[] =>
  [...issues].sort((a, b) => LEVELS.indexOf(a.level) - LEVELS.indexOf(b.level) || idNum(a.id) - idNum(b.id));

const SCENE = /(?<![A-Za-z0-9])s\d+(?=_)/g;
/** 问题涉及的场：镜头里的 s3_st3 → s3；按维度推出的问题没有镜头时取该审稿项的范围。 */
export function issueScenes(i: Issue, run?: ReviewRun | null): string[] {
  const found = [...new Set(i.shots.flatMap(s => s.match(SCENE) ?? []))];
  if (found.length) return found;
  return run?.items.find(x => x.id === i.item)?.scope ?? [];
}

export function filterIssues(issues: Issue[], f: IssueFilter, run?: ReviewRun | null): Issue[] {
  return sortIssues(issues.filter(i => (!f.level || i.level === f.level) && (!f.status || i.status === f.status)
    && (!f.category || i.category === f.category) && (!f.scene || issueScenes(i, run).includes(f.scene))));
}

// —— 循环：本轮 → 问题 → 方案 → 实施 → 下一轮复核 ——

export const LOOP_V5 = ["本轮审查", "问题", "方案", "实施", "下一轮复核"] as const;
export interface LoopPos { step: number; blockers: Issue[]; note: string }
export function loopPosition(run: ReviewRun, issues: Issue[] | null): LoopPos {
  const notDone = run.items.filter(i => i.status !== "done");
  if (notDone.length) {
    const judging = notDone.filter(i => i.status === "adjudicating").length;
    return { step: 0, blockers: [], note: `还有 ${notDone.length} 项没审完${judging ? `（其中 ${judging} 项待裁决）` : ""}；全部双审、对比、裁决完才能推出问题清单。` };
  }
  if (!issues) return { step: 1, blockers: [], note: "本轮审完，还没推出问题清单：运行 python tools/review_run.py issues <审查单>。" };
  const blockers = sortIssues(issues.filter(blocksNextRound));
  if (run.child) return { step: 4, blockers, note: "下一轮已开：新一轮审稿人用 R 逐条复核这里的方案。" };
  if (!blockers.length) return { step: 4, blockers, note: "严重与主要问题都已实施或写明理由不改：可以 new --after 开下一轮复核。" };
  const open = blockers.filter(i => i.status === "open").length;
  const planned = blockers.filter(i => i.status === "planned").length;
  const wontfixNoReason = blockers.length - open - planned;
  const parts = [open ? `未处理 ${open}` : "", planned ? `已定方案未实施 ${planned}` : "", wontfixNoReason ? `不改但没写理由 ${wontfixNoReason}` : ""].filter(Boolean);
  return { step: open ? 2 : 3, blockers, note: `还有 ${blockers.length} 个严重 / 主要问题挡着下一轮（${parts.join("，")}）。` };
}
