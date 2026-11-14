// 审查大类页（follow-up 338）：点进一个大类，先讲它是什么、想解决什么问题、分几个小类、检查流程、用了哪些 skill，最后才给本轮结果。
// 大类说明的唯一源是名册 .agents/references/project/review_roster.json 的 laws.<law>；本轮结果来自 checklist.json 与各审稿人报告。
import { SEVERITY_ORDER, agentShort, tickedAttempt, type MustCheck, type ReviewItem, type ReviewRun, type RubricDim } from "./reviewRun";

export const REVIEW_LAW_ROUTE = "/review-run/law";
export const reviewLawHref = (dir: string, law: string): string => `${REVIEW_LAW_ROUTE}?${new URLSearchParams({ path: dir, law })}`;
export const ROSTER_PATH = ".agents/references/project/review_roster.json";

export type Partition = "pairs" | "halves" | "whole";
export interface RosterLaw {
  name: string; color?: string; partition?: Partition; blind?: boolean; blind_note?: string; prefer_model?: string;
  what?: string; problem?: string; examples?: string[]; must?: MustCheck[]; checks?: string; how?: string; mechanisms?: string[];
  /** v5：这一类的评分维度（每维 0–3）、审法步骤、两位审稿人（a＝Claude、b＝Codex）与为什么用这两个模型。 */
  rubric?: RubricDim[]; method?: string[]; reviewers?: { slot: string; runner: string; model: string }[]; model_why?: string;
}
export interface Roster { version?: number; laws: Record<string, RosterLaw>; adjudicator?: { runner: string; model: string } }

export const PARTITION_TEXT: Record<Partition, string> = {
  pairs: "每两场一位审稿人（场多时拆成几位，各看两场）",
  halves: "按场分成前后两半，各一位审稿人",
  whole: "一位审稿人看全部",
};

/** 这一类在本轮的审稿人（生成顺序）。 */
export const lawItems = (run: ReviewRun, law: string): ReviewItem[] => run.items.filter(i => i.law === law);

/** 小类＝必查项：本轮单子里的为准（第 2 轮起多一个 R），旧单没有就退回名册。 */
export function lawMust(items: ReviewItem[], roster?: RosterLaw): { must: MustCheck[]; fromRun: boolean } {
  const seen = new Map<string, MustCheck>();
  for (const i of items) for (const m of i.must ?? []) if (!seen.has(m.id)) seen.set(m.id, m);
  if (seen.size) return { must: [...seen.values()], fromRun: true };
  return { must: roster?.must ?? [], fromRun: false };
}

/** 小类 × 审稿人：✓ / ✗ / —（没填或没有这一项）。 */
export function mustMatrix(items: ReviewItem[], must: MustCheck[]): { id: string; text: string; cells: string[]; failed: number }[] {
  return must.map(m => {
    const cells = items.map(i => i.must_result?.[m.id] ?? "—");
    return { id: m.id, text: m.text, cells, failed: cells.filter(c => c === "✗").length };
  });
}

/** 实际跑了哪些 agent：按「执行方式 · 模型」合并计数，并标出打勾的那几次。 */
export function agentTally(items: ReviewItem[]): { who: string; count: number; ticked: number }[] {
  const out = new Map<string, { who: string; count: number; ticked: number }>();
  for (const i of items) {
    const t = tickedAttempt(i);
    for (const a of i.agents ?? []) {
      const who = agentShort(a);
      const row = out.get(who) ?? { who, count: 0, ticked: 0 };
      row.count += 1; if (a === t) row.ticked += 1;
      out.set(who, row);
    }
  }
  return [...out.values()];
}

// —— 合并问题表：只认表头有「严重度」的表（和 tools/review_run.py parse_report 同一规则；道具状态表等其他表不算） ——

export interface Finding {
  item: string; shot: string; time: string; severity: string; rank: number; raw: string;
  sub: string; evidence: string; fix: string; order: number;
}

const cellsOf = (line: string): string[] =>
  line.trim().replace(/^\|/, "").replace(/\|$/, "").split(/(?<!\\)\|/).map(c => c.trim().replace(/\\\|/g, "|"));
const isRule = (line: string): boolean => /^[|\s:-]+$/.test(line.trim());
/** 去掉单元格里的粗体记号和 <br>，留纯文本（行内 `代码` 由页面渲染）。 */
export const plainCell = (s: string): string => s.replace(/<br\s*\/?>/gi, " ").replace(/\*\*/g, "").trim();

/** 严重度归类：和 review_run.py 一样按 重出 → 可剪 → 记录 → 存疑 的顺序找第一个出现的词；都没有（如「通过」）排最后。 */
export function severityOf(raw: string): { severity: string; rank: number } {
  const text = plainCell(raw);
  const rank = SEVERITY_ORDER.findIndex(s => text.includes(s));
  return rank < 0 ? { severity: text || "—", rank: SEVERITY_ORDER.length } : { severity: SEVERITY_ORDER[rank], rank };
}

export function parseFindings(markdown: string, item: string): Finding[] {
  const out: Finding[] = [];
  let header: string[] | null = null;   // 当前表的表头；null＝不在表里
  let col: Record<string, number> | null = null;
  for (const line of markdown.split(/\r?\n/)) {
    if (!line.trim().startsWith("|")) { header = null; col = null; continue; }
    if (!header) {
      header = cellsOf(line);
      const find = (re: RegExp): number => header!.findIndex(h => re.test(h));
      const sev = find(/严重度/);
      col = sev < 0 ? null : { sev, shot: find(/镜头/), time: find(/秒/), sub: find(/子类/), evidence: find(/证据/), fix: find(/建议/) };
      continue;
    }
    if (!col || isRule(line)) continue;
    const c = cellsOf(line);
    if (c.length <= col.sev) continue;
    const get = (k: string): string => (col![k] >= 0 ? plainCell(c[col![k]] ?? "") : "");
    out.push({ item, order: out.length, raw: plainCell(c[col.sev]), ...severityOf(c[col.sev]),
      shot: get("shot"), time: get("time"), sub: get("sub"), evidence: get("evidence"), fix: get("fix") });
  }
  return out;
}

/** 多位审稿人的问题合成一张表：按严重度（重出、可剪、记录、存疑），同级保持审稿人顺序与报告原顺序。 */
export function mergeFindings(reports: { item: string; text: string }[]): Finding[] {
  const all = reports.flatMap((r, n) => parseFindings(r.text, r.item).map(f => ({ f, n })));
  return all.sort((a, b) => a.f.rank - b.f.rank || a.n - b.n || a.f.order - b.f.order).map(x => x.f);
}

export function severityTotals(items: ReviewItem[]): Record<string, number> {
  const t: Record<string, number> = Object.fromEntries(SEVERITY_ORDER.map(s => [s, 0]));
  for (const i of items) for (const [k, v] of Object.entries(i.findings ?? {})) t[k] = (t[k] ?? 0) + v;
  return t;
}
