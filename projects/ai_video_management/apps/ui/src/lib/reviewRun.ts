// 审查单（tools/review_run.py 写的 checklist.json，存在 ai_videos/<剧>/reviews/）：每位独立审稿人一个勾，全部打勾才算审完；
// 出片前最多循环 3 轮（chuanyue_yiri follow-up 034 / 035）；每轮收轮只记结论（已收轮），不等用户 review——用户只在出片时确认，
// shot_take 出片前查（用户 2026-11-08）。本站只读：打勾只能由审稿人运行 `review_run.py tick`。

export const REVIEW_RUN_ROUTE = "/review-run";
export const REVIEW_ITEM_ROUTE = "/review-run/item";
export const reviewRunHref = (path: string): string => `${REVIEW_RUN_ROUTE}?${new URLSearchParams({ path })}`;
/** 第二层：一位审稿人怎么审、流程、必查项结果和报告全文（follow-up 333）。 */
export const reviewItemHref = (dir: string, item: string): string => `${REVIEW_ITEM_ROUTE}?${new URLSearchParams({ path: dir, item })}`;
export const SEVERITY_ORDER = ["重出", "可剪", "记录", "存疑"] as const;

export interface MustCheck { id: string; text: string }
/** 一次派单（`review_run.py dispatch` 写入，follow-up 036 / 337）：谁在什么上下文里审、发了什么指令、依据哪些规则。 */
export interface AgentDispatch {
  n: number; at: string; runner: string; model: string; context?: string;
  /** 发给审稿人的完整指令原文，相对审查单目录（agents/<代号>_<n>.md）。 */
  prompt: string; skills?: string[]; note?: string; reply?: string; replied_at?: string;
}
/** v5 一维评分：0–3 分＋证据（审稿人报告「## 评分表」，tools/review_run.py validate_scores）。 */
export interface DimScore { score: number; evidence: string }
/** v5 Kimi 单审的任务书、报告、派单记录与评分；旧双审记录也可读。 */
export interface ReviewSlot {
  slot: string; runner: string; model: string; status: "pending" | "done" | "failed"; report: string; prompt: string; agents?: AgentDispatch[];
  by?: string; ticked_at?: string; scores?: Record<string, DimScore>; findings?: Record<string, number>; rows?: number; clean?: boolean;
  /** Codex 沙箱跑不了 python 时，调用方凭运行日志代为登记（log＝原日志，copy＝审查单里留的副本）。 */
  attested?: { log: string; copy?: string; at?: string; log_sha?: string };
  r_check?: string; note?: string; failed_at?: string;
}
/** v5 两位都勾后的对比（reconcile）：每维 a / b 分、证据、一致 / 分歧 / 抽查，裁决后有 final 与裁决理由。 */
export interface ReconciledScore {
  name: string; a: number; a_ev: string; b: number; b_ev: string; verdict: "一致" | "分歧" | "抽查" | string;
  agreed: number | null; final: number | null; judge_reason?: string;
}
export interface RubricDim { id: string; name: string; question: string; critical?: boolean }
export interface ReviewJudge {
  runner: string; model: string; status: "pending" | "done" | "failed"; dims: string[]; prompt: string; report: string; agents?: AgentDispatch[];
  by?: string; at?: string; ruling?: Record<string, DimScore>; note?: string;
}
export type ItemStatus = "pending" | "done" | "failed" | "adjudicating";
export interface ReviewItem {
  id: string; law: string; law_name: string; color: string; scope: string[]; checks: string; how: string; blind?: boolean;
  must?: MustCheck[]; must_result?: Record<string, string>;
  status: ItemStatus; report: string; prompt: string;
  ticked_at?: string; ticked_by?: string; agents?: (AgentDispatch & { slot?: string })[]; findings?: Record<string, number>; rows?: number; clean?: boolean; note?: string; failed_at?: string;
  // —— v5 双审（没有 slots 的是 v2 单，照旧渲染） ——
  slots?: Record<string, ReviewSlot>; rubric?: RubricDim[]; method?: string[]; model_why?: string; what?: string; problem?: string;
  ticked_by_list?: string[]; scores?: Record<string, ReconciledScore>; disputes?: string[]; audits?: string[]; judge?: ReviewJudge;
  final_scores?: Record<string, number | null>; reconciled_at?: string; done_at?: string;
}
/** 「待用户确认」是旧单的收轮状态，review_run.py migrate / status 会改成「已收轮」；页面也按「已收轮」显示。 */
export type ReviewState = "进行中" | "已完成" | "已作废" | "已收轮" | "用户已确认出片" | "待用户确认";
export const displayState = (s: string): string => (s === "待用户确认" ? "已收轮" : s);
/** 收轮结论（review_run.py conclude）：可出片 / 不可出片＋理由。 */
export interface ReviewVerdict { result: string; text: string; reasons?: string[] }
export interface ReviewRun {
  /** v5：名册的评分规则与裁决人（tools/review_run.py DEFAULT_SCORING / adjudicator）。 */
  scoring?: { scale?: Record<string, string>; evidence_rule?: string; disagreement?: string; audit?: string };
  adjudicator?: { runner: string; model: string };
  version: number; id: string; title: string; target: string; stage: string; stage_name: string; scenes: string[];
  created_at: string; author: string; known: string; items: ReviewItem[]; state: ReviewState;
  chain?: string; loop?: number; max_loops?: number; parent?: string; child?: string; episode?: string; gate_stage?: boolean;
  changes?: string; result?: string; concluded_at?: string; confirmed_at?: string; confirm_quote?: string;
  verdict?: ReviewVerdict; corrections?: string;
  log: { at: string; item?: string; slot?: string; event: string; by?: string; note?: string; quote?: string; log?: string }[];
}

export const CHECKLIST = "checklist.json";
export const isRunDir = (path: string): boolean => /\/reviews\/[^/]+\/?$/.test(path);

/** 列表页：给剧目录或集目录，审查单都在剧目录的 reviews/ 下；集目录时只列这一集的。 */
export function listScope(path: string): { reviews: string; episode: string | null } {
  const i = path.indexOf("/episodes/");
  if (i < 0) return { reviews: `${path}/reviews`, episode: null };
  return { reviews: `${path.slice(0, i)}/reviews`, episode: path.slice(i + "/episodes/".length).split("/")[0] };
}

export function progress(run: ReviewRun): { done: number; failed: number; total: number } {
  return { done: run.items.filter(i => i.status === "done").length, failed: run.items.filter(i => i.status === "failed").length, total: run.items.length };
}

export function totals(run: ReviewRun): Record<string, number> {
  const t: Record<string, number> = Object.fromEntries(SEVERITY_ORDER.map(s => [s, 0]));
  for (const i of run.items) for (const [k, v] of Object.entries(i.findings ?? {})) t[k] = (t[k] ?? 0) + v;
  return t;
}

export function mustFailed(item: ReviewItem): number {
  return Object.values(item.must_result ?? {}).filter(v => v === "✗").length;
}

/** 清单按法则分组，组内保持生成顺序（physics_A、physics_B…）。 */
export function byLaw(run: ReviewRun): [string, ReviewItem[]][] {
  const out = new Map<string, ReviewItem[]>();
  for (const i of run.items) out.set(i.law_name, [...(out.get(i.law_name) ?? []), i]);
  return [...out.entries()];
}

/** 列表页按「集 → 一条循环链（第 1–3 轮）」分组，最新的链在前。 */
export function chains(runs: { dir: string; run: ReviewRun }[]): { episode: string; chain: string; rounds: { dir: string; run: ReviewRun }[] }[] {
  const map = new Map<string, { dir: string; run: ReviewRun }[]>();
  for (const r of runs) {
    const key = `${r.run.episode ?? ""}|${r.run.chain ?? r.run.id}`;
    map.set(key, [...(map.get(key) ?? []), r]);
  }
  return [...map.entries()].map(([key, rounds]) => ({
    episode: key.split("|")[0], chain: key.split("|")[1], rounds: rounds.sort((a, b) => (a.run.loop ?? 1) - (b.run.loop ?? 1)),
  })).sort((a, b) => b.rounds[0].run.created_at.localeCompare(a.rounds[0].run.created_at));
}

export const STATE_TEXT: Record<string, string> = {
  进行中: "审查未完成：还有审稿人没打勾。全部打勾前，不能据此出片、进剪辑或交付。",
  已完成: "本轮审完：所有审稿人都交了报告并打勾，被审材料没有变。便宜的改动改完后开下一轮（最多 3 轮），或收轮记下结论。",
  已作废: "已作废：审查开始后被审材料变了，需要重开一张审查单。",
  已收轮: "已收轮：这一轮的结论已记下（见下）。",
  用户已确认出片: "你已确认出片：这张单覆盖的场可以提交生成（材料再变会自动失效）。",
};
export const stateText = (s: string): string => STATE_TEXT[displayState(s)] ?? s;
/** 出片前只需一句中性的提示：结论是可出片、又还没登记确认时才显示。 */
export const needsShootConfirm = (run: ReviewRun): boolean =>
  displayState(run.state) === "已收轮" && run.verdict?.result === "可出片" && !run.confirm_quote;
export const SHOOT_CONFIRM_NOTE = "出片前需用户在对话里确认（出片工具会检查）";

export const fileHref = (path: string): string => `/file/${path.split("/").map(encodeURIComponent).join("/")}`;

/** 审查单页每个大类一行（follow-up 333）：审了没、问题数、哪些审稿人参与。 */
export interface LawRow {
  law: string; name: string; color: string; items: ReviewItem[]; done: number; failed: number; total: number;
  findings: Record<string, number>; reviewers: string[];
}
export function lawRows(run: ReviewRun): LawRow[] {
  return byLaw(run).map(([name, items]) => {
    const findings: Record<string, number> = Object.fromEntries(SEVERITY_ORDER.map(s => [s, 0]));
    for (const i of items) for (const [k, v] of Object.entries(i.findings ?? {})) findings[k] = (findings[k] ?? 0) + v;
    return {
      law: items[0].law, name, color: items[0].color, items, total: items.length, findings,
      done: items.filter(i => i.status === "done").length, failed: items.filter(i => i.status === "failed").length,
      reviewers: [...new Set(items.map(i => i.ticked_by).filter((x): x is string => Boolean(x)))],
    };
  });
}

/** 一位审稿人的状态（审查单页一行里的小标签）。 */
export const itemStatusText = (i: ReviewItem): string => i.status === "done" ? "已审" : i.status === "failed" ? "失败" : i.status === "adjudicating" ? "待裁决" : "未审";

// —— 同一范围里哪张是最新的（用户 2026-11-08：「审查单我看不出来哪个是最新的」） ——

/** 一张审查单的「范围」＝同一集、同一阶段、同一组场；同一范围可开几条审查链（第几次），每条链 1–3 轮。 */
export interface ScopeFields { dir: string; title: string; episode?: string; stage?: string; stage_name?: string; scenes?: string[]; created_at: string }
export const scopeKey = (r: ScopeFields): string => [r.episode ?? "", r.stage ?? "", [...(r.scenes ?? [])].sort().join(",")].join("|");
/** 范围的人话名：标题第二段（review_run.py scope_label：场一 / 场二到场八 / 全集）；标题不是这个格式时用场号。 */
export function scopeLabel(r: ScopeFields): string {
  const seg = r.title.split(" · ");
  if (seg.length >= 4 && seg[0] === r.episode) return seg[1];
  return r.scenes?.length ? r.scenes.join("、") : "全集";
}
export const stageShort = (r: ScopeFields): string => (r.stage_name || r.stage || "").split("（")[0];
/** 标题去掉上层分组已经写了的「集 · 范围 · 」前缀（导航里用；完整标题放在悬停提示）。 */
export function shortTitle(r: ScopeFields): string {
  const prefix = `${r.episode ?? ""} · ${scopeLabel(r)} · `;
  return r.title.startsWith(prefix) ? r.title.slice(prefix.length) : r.title;
}
/** 导航叶子用的短名：开单时间 + 轮次「11-08 15:32 · 第 1 轮」（范围已在上一层；「第 2 次」等完整标题放悬停提示，导航宽度放不下）。
 * 时间取标题末段，没有就取开单时间。 */
export function navLabel(r: ScopeFields & { loop?: number }): string {
  const seg = r.title.split(" · ");
  const when = /^\d{2}-\d{2} \d{2}:\d{2}$/.test(seg[seg.length - 1]) ? seg[seg.length - 1] : r.created_at.slice(5, 16).replace("T", " ");
  return `${when} · 第 ${r.loop ?? 1} 轮`;
}
/** 新的在前：开单时间；同一秒再按目录名（目录名里有秒级时间和轮次）。 */
export const newerFirst = (a: ScopeFields, b: ScopeFields): number => b.created_at.localeCompare(a.created_at) || b.dir.localeCompare(a.dir);
export interface ScopedRun<T> { run: T; latest: boolean; supersededBy?: T }
export interface ScopeGroup<T> { key: string; episode: string; label: string; stage: string; latest: T; runs: ScopedRun<T>[] }
/** 按范围分组：组内所有链的所有轮按开单时间新的在前，最上面一张是「最新」，其余标「已被最新那张取代」；组按最新一张排。 */
export function scopeGroups<T extends ScopeFields>(runs: T[]): ScopeGroup<T>[] {
  const map = new Map<string, T[]>();
  for (const r of runs) map.set(scopeKey(r), [...(map.get(scopeKey(r)) ?? []), r]);
  return [...map.entries()].map(([key, list]) => {
    const sorted = [...list].sort(newerFirst);
    const latest = sorted[0];
    return { key, episode: latest.episode ?? "", label: scopeLabel(latest), stage: stageShort(latest), latest,
      runs: sorted.map((run, i) => ({ run, latest: i === 0, supersededBy: i === 0 ? undefined : latest })) };
  }).sort((a, b) => newerFirst(a.latest, b.latest));
}
/** 集 → 范围：集按名字排，集内范围新的在前。 */
export function episodeScopes<T extends ScopeFields>(runs: T[]): { episode: string; scopes: ScopeGroup<T>[] }[] {
  const eps = new Map<string, T[]>();
  for (const r of runs) eps.set(r.episode || "未分集", [...(eps.get(r.episode || "未分集") ?? []), r]);
  return [...eps.entries()].map(([episode, list]) => ({ episode, scopes: scopeGroups(list) })).sort((a, b) => a.episode.localeCompare(b.episode));
}
/** 同一剧里与 run 同范围的最新一张（审查单页顶部「这不是最新的」横幅）；runs 只放同一剧的。 */
export function latestInScope<T extends ScopeFields>(runs: T[], run: ScopeFields): T | undefined {
  const key = scopeKey(run);
  return runs.filter(r => scopeKey(r) === key).sort(newerFirst)[0];
}

/** 左侧导航「审查单」：剧 → 集 → 范围 → 每一张（所有链的各轮），新的在前（follow-up 333；范围分组见上）。 */
export interface NavRun extends ScopeFields { loop: number; stage_name: string; state: string; chain: string; corrections?: boolean }
export interface NavEpisode { episode: string; scopes: ScopeGroup<NavRun>[]; runs: NavRun[] }
export interface NavDrama { drama: string; name: string; episodes: NavEpisode[] }
export type NavInput = NavRun & { drama: string; drama_name: string; episode: string };
export function navGroups(runs: NavInput[]): NavDrama[] {
  const dramas = new Map<string, { name: string; runs: NavInput[] }>();
  for (const r of runs) {
    const d = dramas.get(r.drama) ?? { name: r.drama_name, runs: [] };
    d.runs.push(r);
    dramas.set(r.drama, d);
  }
  return [...dramas.entries()].map(([drama, d]) => ({
    drama, name: d.name,
    episodes: episodeScopes<NavRun>(d.runs).map(e => ({ ...e, runs: e.scopes.flatMap(s => s.runs.map(x => x.run)) })),
  })).sort((a, b) => a.name.localeCompare(b.name));
}

/** 出片前审查循环的步骤（详情页「审查流程」）。 */
export const LOOP_STEPS = [
  "出审查单：名册决定要哪几位审稿人、各审哪几场，每位有编号的必查项",
  "独立审：每位审稿人在全新上下文里只看材料，报告逐条写必查项 ✓ / ✗",
  "打勾：审稿人自己运行 review_run.py tick，作者不能代勾；失败的要记下、重派",
  "全部打勾后看结果：便宜的改动（除 Seedance 积分外都算）直接改",
  "开下一轮：写明改了什么，新一轮加必查项 R 复核上一轮，最多 3 轮",
  "收轮：记下结论（可出片 / 不可出片＋理由），不等你 review；出片时你在对话里确认，出片工具会检查",
] as const;

// —— 审稿 agent（follow-up 337）：每一步是哪个独立 agent 审的、用的什么指令和规则 ——

/** 执行方式的简称；旧 Claude / Codex 记录仍可显示。 */
export function agentKind(runner: string): string {
  if (/kimi/i.test(runner)) return /子代理|agent/i.test(runner) ? "Kimi 子代理" : "Kimi";
  if (/codex/i.test(runner)) return "Codex";
  if (/claude/i.test(runner)) return /子代理|agent/i.test(runner) ? "Claude 子代理" : "Claude";
  return runner.split(/[（(]/)[0].trim() || runner;
}
/** 模型简称：去掉括号里的配置说明（gpt-6-astra（reasoning high…）→ gpt-6-astra）。 */
export const modelShort = (model: string): string => model.split(/[（(]/)[0].trim() || model;
export const agentShort = (a: AgentDispatch): string => `${agentKind(a.runner)} · ${modelShort(a.model)}`;

/** 派单记录，最新的在前。 */
export const attemptsNewestFirst = (item: ReviewItem): AgentDispatch[] => [...(item.agents ?? [])].sort((a, b) => b.n - a.n);

/** 打勾的是哪一次派单：按 ticked_by 的前缀（kimi/…；旧记录可能是 claude-…、codex-…）对上模型或执行方式，从新到旧找；对不上取最新一次。 */
export function tickedAttempt(item: ReviewItem): AgentDispatch | undefined {
  const list = attemptsNewestFirst(item);
  if (item.status !== "done" || !list.length) return undefined;
  const who = (item.ticked_by ?? "").split("/")[0].toLowerCase();
  return (who && list.find(a => modelShort(a.model).toLowerCase() === who || a.runner.toLowerCase().includes(who))) || list[0];
}
/** 审查单页标签上显示的那一次：打勾的那次，没打勾就是最新一次。 */
export const shownAttempt = (item: ReviewItem): AgentDispatch | undefined => tickedAttempt(item) ?? attemptsNewestFirst(item)[0];

/** 「用了哪些规则 / skill」一行拆成 前文 + 文件路径 + 后文；路径相对审查单目录（BRIEF.md、items/x.md）或仓库根（.agents/…、ai_videos/…）。 */
export interface SkillPart { before: string; path?: string; after: string; href?: string }
const SKILL_PATH = /(?:\.agents\/|ai_videos\/|tools\/|specs\/|projects\/)?[A-Za-z0-9_][\w./-]*\.(?:json|md|toml|py|txt)/;
export function skillPart(skill: string, dir: string, sourceHref: (repoPath: string) => string): SkillPart {
  const m = SKILL_PATH.exec(skill);
  if (!m) return { before: skill, after: "" };
  const path = m[0];
  const before = skill.slice(0, m.index); const after = skill.slice(m.index + path.length);
  const href = path.startsWith("ai_videos/") ? fileHref(path)
    : path.startsWith(".agents/") ? sourceHref(path)
    : /^(tools|specs|projects)\//.test(path) ? undefined
    : fileHref(`${dir}/${path}`);
  return { before, path, after, href };
}
