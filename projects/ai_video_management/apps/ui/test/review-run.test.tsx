import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { expect, it, vi } from "vitest";
import {
  agentShort, byLaw, chains, episodeScopes, isRunDir, latestInScope, lawRows, listScope, mustFailed, navGroups, navLabel, progress, reviewItemHref, reviewRunHref,
  scopeGroups, scopeKey, scopeLabel, shortTitle, shownAttempt, skillPart, tickedAttempt, totals, type AgentDispatch, type ReviewRun,
} from "../src/lib/reviewRun";

// 第一次动态 import 页面组件（含 react-markdown）在满并发下会超过默认 5 秒。
vi.setConfig({ testTimeout: 30000 });

const dir = "ai_videos/demo/reviews/ep01_20261108-090000_pregen_r2";
const SKILLS = ["审稿人名册 .agents/references/project/review_roster.json · 法则 physics（世界物理）", "审稿说明 BRIEF.md（材料、规则、报告格式）",
  "任务书 items/physics_A.md（范围、要查什么、怎么查、必查项、打勾命令）"];
const codex: AgentDispatch = { n: 1, at: "2026-11-08T09:01:00", runner: "Codex CLI（codex exec -s workspace-write，另起进程）",
  model: "gpt-6-astra（reasoning high，~/.codex/config.toml）", context: "全新的 Codex 进程", prompt: "agents/physics_A_1.md", skills: SKILLS,
  note: "沙盒找不到 python，没能打勾" };
const claude: AgentDispatch = { n: 2, at: "2026-11-08T09:05:00", runner: "Claude Code 子代理（Agent 工具 · general-purpose，后台运行）",
  model: "claude-opus-5-5", context: "全新上下文，看不到作者会话与别的审稿报告", prompt: "agents/physics_A_2.md", skills: SKILLS,
  reply: "已写报告，**2 条重出**。", replied_at: "2026-11-08T09:12:00" };
const run: ReviewRun = {
  version: 2, id: "ep01_20261108-090000_pregen_r2", chain: "ep01_20261108-080000_pregen_r1", loop: 2, max_loops: 3,
  parent: "ai_videos/demo/reviews/ep01_20261108-080000_pregen_r1", episode: "ep01", gate_stage: true,
  title: "ep01 · 出片前 · 第 2 轮", target: "ai_videos/demo/episodes/ep01", stage: "pregen", stage_name: "出片前",
  scenes: ["s1", "s2"], created_at: "2026-11-08T09:00:00", author: "Claude Code", known: "旧发色", changes: "改了 s3_st2 的分镜：固定机位双手掰",
  state: "进行中", log: [],
  items: [
    { id: "physics_A", law: "physics", law_name: "世界物理", color: "#c0502e", scope: ["s1"], checks: "重力", how: "", status: "done",
      must: [{ id: "P1", text: "手数" }, { id: "P2", text: "道具来源" }, { id: "R", text: "复核上一轮" }],
      must_result: { P1: "✗", P2: "✓", R: "✓" },
      report: "reports/physics_A.md", prompt: "items/physics_A.md", ticked_by: "claude-opus-5-5/physics_A", ticked_at: "2026-11-08T09:10:00",
      agents: [codex, claude],
      findings: { 重出: 2, 记录: 1 }, rows: 3 },
    { id: "physics_B", law: "physics", law_name: "世界物理", color: "#c0502e", scope: ["s2"], checks: "重力", how: "", status: "failed",
      report: "reports/physics_B.md", prompt: "items/physics_B.md", note: "网络 403", failed_at: "2026-11-08T09:11:00" },
    { id: "audience", law: "audience", law_name: "观众", color: "#c23f7a", scope: ["s1", "s2"], checks: "看懂没", how: "", blind: true,
      status: "pending", report: "reports/audience.md", prompt: "items/audience.md",
      agents: [{ n: 1, at: "2026-11-08T09:02:00", runner: "Codex CLI（codex exec）", model: "gpt-6-astra", prompt: "agents/audience_1.md" }] },
  ],
};
const first: ReviewRun = { ...run, id: "ep01_20261108-080000_pregen_r1", loop: 1, parent: "", child: dir, title: "ep01 · 出片前 · 第 1 轮",
  created_at: "2026-11-08T08:00:00", state: "已完成", items: run.items.map(i => ({ ...i, status: "done" as const })) };

// 已收轮的单（用户 2026-11-08：每轮审查不等用户 review，只记结论）
const closedDir = "ai_videos/demo/reviews/ep03_20261108-100000_pregen_r1";
const closed: ReviewRun = { ...first, id: "ep03_20261108-100000_pregen_r1", child: "", episode: "ep03", title: "ep03 · 出片前 · 第 1 轮", state: "已收轮",
  verdict: { result: "可出片", text: "没有未处理的严重问题", reasons: [] } };

const REPORT = ["# 物理 A", "", "| 镜头 | 严重度 |", "|---|---|", "| s1_st1 | 重出 |", ""].join(String.fromCharCode(10));
// 审查页经 /api/review-runs/checklist 读单（v5 单常超 /api/file 的 1 MiB 上限）；测试里沿用同一份 fetchFile 数据。
const { withChecklist } = vi.hoisted(() => ({
  withChecklist: <T extends { fetchFile: (p: string) => Promise<{ content: string }> }>(m: T) =>
    ({ ...m, fetchReviewChecklist: async (d: string) => JSON.parse((await m.fetchFile(`${d}/checklist.json`)).content) }),
}));
vi.mock("../src/api", () => withChecklist({
  fetchFile: (path: string) => Promise.resolve({
    path, content: path.includes("/agents/") ? `INSTRUCTION ${path.endsWith("_1.md") ? "C:\\x\u0007i_videos " : ""}${path.split("/").pop()}` : path.endsWith(".md") ? REPORT : JSON.stringify(path.startsWith(closedDir) ? closed : path.includes("_r1/") ? first : run), encoding: "utf-8", bytes: 1, mtime: 0, mtime_http: "",
  }),
  fetchReviewRuns: () => Promise.resolve({ runs: [
    { dir, drama: "ai_videos/demo", drama_name: "demo", id: run.id, title: run.title, episode: "ep01", chain: run.chain, loop: 2,
      stage: "pregen", scenes: ["s1", "s2"], stage_name: "出片前", state: "进行中", created_at: run.created_at, done: 1, failed: 1, total: 3, totals: { 重出: 2 } },
    { dir: "ai_videos/demo/reviews/ep01_20261108-080000_pregen_r1", drama: "ai_videos/demo", drama_name: "demo", id: first.id, title: first.title,
      episode: "ep01", chain: run.chain, loop: 1, stage: "pregen", scenes: ["s1", "s2"], stage_name: "出片前", state: "已完成", created_at: first.created_at, done: 3, failed: 0, total: 3, totals: {} },
    { dir: "ai_videos/demo/reviews/ep02_20261109-080000_pregen_r1", drama: "ai_videos/demo", drama_name: "demo", id: "x", title: "x",
      episode: "ep02", chain: "x", loop: 1, stage_name: "出片前", state: "待用户确认", created_at: "2026-11-09T08:00:00", done: 3, failed: 0, total: 3, totals: {} },
  ] }),
  fetchSubtree: () => Promise.resolve({ type: "directory", name: "reviews", path: "ai_videos/demo/reviews", children: [
    { type: "directory", name: run.id, path: dir },
    { type: "directory", name: first.id, path: "ai_videos/demo/reviews/ep01_20261108-080000_pregen_r1" }] }),
  fetchProcessQc: () => Promise.reject(new Error("offline")),
}));

it("finds the drama reviews folder from a drama or episode path (follow-up 035)", () => {
  expect(listScope("ai_videos/demo")).toEqual({ reviews: "ai_videos/demo/reviews", episode: null });
  expect(listScope("ai_videos/demo/episodes/ep01")).toEqual({ reviews: "ai_videos/demo/reviews", episode: "ep01" });
  expect(isRunDir(dir)).toBe(true);
  expect(isRunDir("ai_videos/demo")).toBe(false);
});

it("summarises ticks, failures, findings, must checks and rounds", () => {
  expect(progress(run)).toEqual({ done: 1, failed: 1, total: 3 });
  expect(totals(run)["重出"]).toBe(2);
  expect(mustFailed(run.items[0])).toBe(1);
  expect(byLaw(run).map(([k, v]) => [k, v.length])).toEqual([["世界物理", 2], ["观众", 1]]);
  const c = chains([{ dir, run }, { dir: "x", run: first }]);
  expect(c).toHaveLength(1);
  expect(c[0].rounds.map(r => r.run.loop)).toEqual([1, 2]);
  expect(reviewRunHref(dir)).toContain("/review-run?path=");
  const rows = lawRows(run);
  expect(rows[0]).toMatchObject({ name: "世界物理", done: 1, failed: 1, total: 2, reviewers: ["claude-opus-5-5/physics_A"] });
  expect(rows[0].findings["重出"]).toBe(2);
});

it("keeps the checklist to one row per review category: reviewed or not, issue counts, reviewers (follow-up 333)", async () => {
  const { ReviewRunPage } = await import("../src/components/ReviewRunPage");
  const { container } = render(<MemoryRouter initialEntries={[reviewRunHref(dir)]}><ReviewRunPage /></MemoryRouter>);
  await waitFor(() => expect(screen.getByText(/1 \/ 3/)).toBeTruthy());
  const rows = container.querySelectorAll("tbody tr");
  expect([...rows].map(r => r.getAttribute("data-law"))).toEqual(["physics", "audience"]);
  expect(rows[0].textContent).toContain("! 有失败");
  expect(rows[0].textContent).toContain("重出 2");
  expect(rows[0].textContent).toContain("✓ physics_A");
  expect(rows[0].textContent).toContain("Claude 子代理 · claude-opus-5-5");   // 打勾的那次派单
  expect(rows[0].textContent).toContain("↻ 第 2 次派单");
  expect(rows[0].textContent).toContain("没有派单记录");                      // physics_B 没登记派单
  expect(rows[1].textContent).toContain("Codex · gpt-6-astra");             // 未打勾：显示最新一次派单
  expect(rows[1].textContent).not.toContain("↻");
  expect(rows[1].textContent).toContain("未审完");
  expect(screen.getByText(/审查未完成/)).toBeTruthy();
  expect(screen.getByText("← 上一轮")).toBeTruthy();
  expect(screen.queryByText("P1 ✗")).toBeNull();          // 必查项细节只在下一层
  expect(screen.queryByText("查什么")).toBeNull();
  expect([...container.querySelectorAll("a")].map(a => a.getAttribute("href"))).toContain(reviewItemHref(dir, "physics_B"));
});

it("opens one reviewer's detail: how it reviews, must results, the loop and the report", async () => {
  const { ReviewItemPage } = await import("../src/components/ReviewRunPage");
  render(<MemoryRouter initialEntries={[reviewItemHref(dir, "physics_A")]}><ReviewItemPage /></MemoryRouter>);
  await waitFor(() => expect(screen.getByText("物理 A")).toBeTruthy());
  expect(screen.getByText("手数")).toBeTruthy();
  expect(screen.getAllByText("✗").length).toBeGreaterThan(0);
  expect(screen.getByText("审查流程")).toBeTruthy();
  expect(screen.getByText("physics_B")).toBeTruthy();       // 同类的另一位审稿人
  expect(screen.getByText("s1_st1")).toBeTruthy();          // 报告表格渲染出来
});

it("shows a failed reviewer's failure on its detail page", async () => {
  const { ReviewItemPage } = await import("../src/components/ReviewRunPage");
  render(<MemoryRouter initialEntries={[reviewItemHref(dir, "physics_B")]}><ReviewItemPage /></MemoryRouter>);
  await waitFor(() => expect(screen.getByText(/网络 403/)).toBeTruthy());
  expect(screen.getByText(/审稿人交报告并打勾后/)).toBeTruthy();
});

it("lists review runs in the left nav as a category: drama → episode → rounds, newest first", async () => {
  const g = navGroups((await (await import("../src/api")).fetchReviewRuns()).runs);
  expect(g).toHaveLength(1);
  expect(g[0].episodes.map(e => e.episode)).toEqual(["ep01", "ep02"]);
  expect(g[0].episodes[0].runs.map(r => r.loop)).toEqual([2, 1]);
  expect(g[0].episodes[0].scopes).toHaveLength(1);          // 同一集、同一阶段、同一组场：一个范围
  const { ReviewNav } = await import("../src/components/ReviewNav");
  render(<MemoryRouter initialEntries={[reviewRunHref(dir)]}><ReviewNav /></MemoryRouter>);
  await waitFor(() => expect(screen.getByText("☑ 审查单")).toBeTruthy());
  expect(screen.getByText("ep02")).toBeTruthy();
  expect(screen.getByText("11-08 09:00 · 第 2 轮")).toBeTruthy();     // 时间在前（标题末段，没有就取开单时间）
  expect(navLabel({ dir: "x", title: "ep01 · 场一 · 出片前（第 2 次） 第 1 轮 · 11-08 15:32", episode: "ep01", created_at: "2026-11-08T15:32:08", loop: 1 }))
    .toBe("11-08 15:32 · 第 1 轮");
  const selected = screen.getByRole("treeitem", { selected: true });
  expect(selected.textContent).toContain("第 2 轮");
  expect(selected.textContent).toContain("最新");
  const older = screen.getAllByRole("treeitem").find(t => t.textContent?.includes("第 1 轮"))!;
  expect(older.classList.contains("rn-old")).toBe(true);
  expect(older.getAttribute("title")).toContain("已被「ep01 · 出片前 · 第 2 轮」取代");
  expect(screen.getAllByText("最新")).toHaveLength(2);       // ep01 一个范围、ep02 一个范围
  // 用户 2026-11-08：每轮审查不等用户 review——旧单的「待用户确认」显示成「已收轮」（绿点）；每轮都有「修复」入口
  expect(screen.queryByText("待用户确认")).toBeNull();
  // 常态（已完成 / 已收轮）只用绿点，状态字在悬停提示里，把导航宽度留给开单时间
  const ep02 = screen.getAllByRole("treeitem").find(t => t.getAttribute("title")?.includes("已收轮"))!;
  expect(ep02.textContent).not.toContain("已收轮");
  expect(ep02.querySelector(".rn-dot-ok")).toBeTruthy();
  expect(screen.getAllByRole("button", { name: "修复" })).toHaveLength(3);
});

it("states: 已收轮 replaces 待用户确认, no wording that the review waits for the user (用户 2026-11-08)", async () => {
  const { STATE_TEXT, stateText, displayState, needsShootConfirm, SHOOT_CONFIRM_NOTE, LOOP_STEPS } = await import("../src/lib/reviewRun");
  expect(Object.keys(STATE_TEXT)).toEqual(["进行中", "已完成", "已作废", "已收轮", "用户已确认出片"]);
  expect(displayState("待用户确认")).toBe("已收轮");
  expect(stateText("待用户确认")).toBe(STATE_TEXT["已收轮"]);
  const all = [...Object.values(STATE_TEXT), ...LOOP_STEPS].join(" ");
  expect(all).not.toMatch(/待你确认|待用户确认|交用户确认|结果待/);
  expect(needsShootConfirm(closed)).toBe(true);
  expect(needsShootConfirm({ ...closed, confirm_quote: "出吧", state: "用户已确认出片" })).toBe(false);
  expect(needsShootConfirm({ ...closed, verdict: { result: "不可出片", text: "x" } })).toBe(false);
  expect(needsShootConfirm({ ...closed, state: "待用户确认" })).toBe(true);
  const { ReviewRunPage } = await import("../src/components/ReviewRunPage");
  const { container } = render(<MemoryRouter initialEntries={[reviewRunHref(closedDir)]}><ReviewRunPage /></MemoryRouter>);
  await waitFor(() => expect(container.querySelector(".rr-verdict")).toBeTruthy());
  expect(container.querySelector(".rr-verdict")!.textContent).toContain("结论：可出片");
  expect(screen.getByText(SHOOT_CONFIRM_NOTE)).toBeTruthy();
  expect(container.querySelector("h1 .rr-state-closed")?.textContent).toBe("已收轮");
  const fix = screen.getByRole("link", { name: /修复页/ });
  expect(fix.getAttribute("href")).toBe(`/review-run/corrections?${new URLSearchParams({ path: closedDir })}`);
  expect(container.textContent).not.toMatch(/待你确认|待用户确认/);
});

it("lists an episode's runs by scope, newest first, older ones marked as replaced (用户 2026-11-08)", async () => {
  const { ReviewRunPage } = await import("../src/components/ReviewRunPage");
  const { container } = render(<MemoryRouter initialEntries={[reviewRunHref("ai_videos/demo/episodes/ep01")]}><ReviewRunPage /></MemoryRouter>);
  await waitFor(() => expect(container.querySelectorAll(".rr-runs li")).toHaveLength(2));
  expect(screen.getByText("2 张")).toBeTruthy();
  const items = [...container.querySelectorAll(".rr-runs li")];
  expect(items.map(li => li.className)).toEqual(["rr-run-latest", "rr-run-old"]);
  expect(items[0].querySelector(".rr-latest")?.textContent).toBe("最新");
  expect(items[0].textContent).toContain("ep01 · 出片前 · 第 2 轮");
  expect(items[1].querySelector(".rr-superseded")?.textContent).toBe("已被 ep01 · 出片前 · 第 2 轮 取代");
  expect(items.every(li => li.querySelector('a[href^="/review-run/corrections"]'))).toBe(true);   // 每张都留修复页入口
});

it("groups runs by scope across chains and picks the newest (用户 2026-11-08：看不出哪个是最新的)", () => {
  const mk = (dir: string, title: string, scenes: string[], created_at: string, chain: string) =>
    ({ dir, title, episode: "ep01", stage: "pregen", stage_name: "出片前（故事＋分镜）", scenes, created_at, chain });
  const s1a = [1, 2, 3].map(n => mk(`r/s1a_r${n}`, `ep01 · 场一 · 出片前 第 ${n} 轮 · 11-08 1${n}:00`, ["s1"], `2026-11-08T1${n}:00:00`, "a"));
  const s1b = mk("r/153208_r1", "ep01 · 场一 · 出片前（第 2 次） 第 1 轮 · 11-08 15:32", ["s1"], "2026-11-08T15:32:08", "b");
  const s28 = [mk("r/s28_r1", "ep01 · 场二到场八 · 出片前 第 1 轮 · 11-08 13:17", ["s2", "s3"], "2026-11-08T13:17:24", "c"),
    mk("r/153205_r2", "ep01 · 场二到场八 · 出片前 第 2 轮 · 11-08 15:32", ["s3", "s2"], "2026-11-08T15:32:08", "c")];
  const all = [...s1a, s28[0], s1b, s28[1]];
  expect(scopeKey(s28[0])).toBe(scopeKey(s28[1]));            // 场的顺序不影响范围
  expect(scopeLabel(s1b)).toBe("场一");
  expect(scopeLabel({ ...s1b, title: "自定义标题" })).toBe("s1");
  expect(shortTitle(s1b)).toBe("出片前（第 2 次） 第 1 轮 · 11-08 15:32");
  const g = scopeGroups(all);
  expect(g.map(x => x.label)).toEqual(["场一", "场二到场八"]);   // 同一秒：按目录名排
  expect(g[0].stage).toBe("出片前");
  expect(g[0].runs.map(r => r.run.dir)).toEqual(["r/153208_r1", "r/s1a_r3", "r/s1a_r2", "r/s1a_r1"]);
  expect(g[0].runs.map(r => r.latest)).toEqual([true, false, false, false]);
  expect(g[0].runs.slice(1).every(r => r.supersededBy?.dir === "r/153208_r1")).toBe(true);
  expect(g[1].runs.map(r => r.run.dir)).toEqual(["r/153205_r2", "r/s28_r1"]);
  expect(latestInScope(all, s1a[0])?.dir).toBe("r/153208_r1");
  expect(latestInScope(all, s28[1])?.dir).toBe("r/153205_r2");
  expect(episodeScopes([...all, { ...s1b, dir: "r/e2", episode: "" }]).map(e => e.episode)).toEqual(["ep01", "未分集"]);
});

it("checklist page: banner to the newest run when this one is replaced, 「最新」 badge when it is newest", async () => {
  const { ReviewRunPage } = await import("../src/components/ReviewRunPage");
  const old = render(<MemoryRouter initialEntries={[reviewRunHref("ai_videos/demo/reviews/ep01_20261108-080000_pregen_r1")]}><ReviewRunPage /></MemoryRouter>);
  await waitFor(() => expect(old.container.querySelector(".rr-stale")).toBeTruthy());
  const banner = old.container.querySelector(".rr-stale")!;
  expect(banner.textContent).toBe("这不是最新的审查单 → 打开最新：ep01 · 出片前 · 第 2 轮");
  expect(banner.querySelector("a")?.getAttribute("href")).toBe(reviewRunHref(dir));
  expect(old.container.querySelector("h1 .rr-latest")).toBeNull();
  old.unmount();
  const fresh = render(<MemoryRouter initialEntries={[reviewRunHref(dir)]}><ReviewRunPage /></MemoryRouter>);
  await waitFor(() => expect(fresh.container.querySelector("h1 .rr-latest")?.textContent).toBe("最新"));
  expect(fresh.container.querySelector(".rr-stale")).toBeNull();
});

it("names the agent behind each tick: kind + short model, which attempt ticked, skill file links (follow-up 337)", () => {
  expect(agentShort(codex)).toBe("Codex · gpt-6-astra");
  expect(agentShort(claude)).toBe("Claude 子代理 · claude-opus-5-5");
  const a = run.items[0];
  expect(tickedAttempt(a)?.n).toBe(2);
  expect(tickedAttempt({ ...a, ticked_by: "codex/physics_A" })?.n).toBe(1);
  expect(tickedAttempt(run.items[2])).toBeUndefined();
  expect(shownAttempt(run.items[2])?.n).toBe(1);
  expect(shownAttempt(run.items[1])).toBeUndefined();
  const src = (p: string): string => `/src?${p}`;
  expect(skillPart(SKILLS[0], dir, src)).toMatchObject({ path: ".agents/references/project/review_roster.json", href: "/src?.agents/references/project/review_roster.json" });
  expect(skillPart(SKILLS[1], dir, src).href).toBe(`/file/${dir.split("/").map(encodeURIComponent).join("/")}/BRIEF.md`);
  expect(skillPart(SKILLS[2], dir, src)).toMatchObject({ before: "任务书 ", path: "items/physics_A.md" });
  expect(skillPart("技能 ai-videos-self-check", dir, src)).toEqual({ before: "技能 ai-videos-self-check", after: "" });
});

it("shows the review agents on the detail page: newest attempt first, runner, model, skills, full instruction, reply (follow-up 337)", async () => {
  const { ReviewItemPage } = await import("../src/components/ReviewRunPage");
  const { container } = render(<MemoryRouter initialEntries={[reviewItemHref(dir, "physics_A")]}><ReviewItemPage /></MemoryRouter>);
  await waitFor(() => expect(screen.getByText("INSTRUCTION physics_A_2.md")).toBeTruthy());
  const section = container.querySelector("section.rr-agents")!;
  expect(section.querySelector("h2")?.textContent).toContain("审稿 agent");
  expect(section.compareDocumentPosition(screen.getByText("怎么审")) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
  const cards = [...section.querySelectorAll("article")];
  expect(cards.map(c => c.getAttribute("data-attempt"))).toEqual(["2", "1"]);
  expect(cards[0].textContent).toContain("打勾的是这次");
  expect(cards[0].textContent).toContain("Claude Code 子代理（Agent 工具 · general-purpose，后台运行）");
  expect(cards[0].textContent).toContain("claude-opus-5-5/physics_A · 2026-11-08 09:10:00");
  expect(cards[0].querySelector("details")?.open).toBe(true);
  expect(cards[0].querySelector(".rr-reply strong")?.textContent).toBe("2 条重出");
  expect(cards[1].textContent).toContain("这次没打勾");
  expect(cards[1].textContent).toContain("gpt-6-astra（reasoning high，~/.codex/config.toml）");
  expect(cards[1].textContent).toContain("沙盒找不到 python");
  expect(cards[1].querySelector("details")?.open).toBe(false);
  expect(cards[1].textContent).toContain("回复未存档，结果见下方报告");
  // 控制字符（路径里 \a 被转义成的响铃符）换成可见符号并提示，原样放进 <pre> 会卡死 Chrome
  await waitFor(() => expect(cards[1].querySelector("pre")?.textContent).toBe("INSTRUCTION C:\\x\u2407i_videos physics_A_1.md"));
  expect(cards[1].textContent).toContain("原文里有控制字符");
  expect(cards[0].textContent).not.toContain("原文里有控制字符");
  const hrefs = [...cards[0].querySelectorAll(".rr-skills a")].map(a => a.getAttribute("href"));
  expect(hrefs[0]).toContain("/workflow/source?source_id=repo%3A.agents%2Freferences%2Fproject%2Freview_roster.json");
  expect(hrefs[1]).toContain("/BRIEF.md");
  expect(hrefs[2]).toContain("/items/physics_A.md");
});

it("says there is no dispatch record for an item without agents", async () => {
  const { ReviewItemPage } = await import("../src/components/ReviewRunPage");
  render(<MemoryRouter initialEntries={[reviewItemHref(dir, "physics_B")]}><ReviewItemPage /></MemoryRouter>);
  await waitFor(() => expect(screen.getByText(/没有派单记录/)).toBeTruthy());
  expect(screen.getByText("审稿 agent")).toBeTruthy();
});
