import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { expect, it, vi } from "vitest";
import { reviewLawHref } from "../src/lib/reviewLaw";
import { reviewItemHref, reviewRunHref, type ReviewRun } from "../src/lib/reviewRun";
import {
  REVIEW_ISSUES_ROUTE, blocksNextRound, dimCell, filterIssues, issueCounts, issueScenes, loopPosition, resolvedIssue, reviewIssuesHref,
  rubricRows, slotTally, sortIssues, type Issue, type IssuesDoc,
} from "../src/lib/reviewV5";

// 审查单 v5（用户 2026-11-08「有了多重 review … based on rubric 两个得分结果 … derive 出问题 … implement solution … loop 回一开始」）。
// fixture 由 tools/review_run.py 在临时目录真跑出来（test/fixtures/review-v5/make_fixtures.py）：
//   done＝全部双审、对比、裁决完，era 有 0 分、1 分、分歧裁决，已推出问题清单并 fix 了 3 条；
//   live＝进行中：era 与 physics_A 待裁决（physics_A 的 b 位凭 Codex 日志代登记），physics_B 只交了 a，continuity 的 b 失败。
vi.setConfig({ testTimeout: 30000 });

const read = (f: string): string => readFileSync(resolve(__dirname, "fixtures/review-v5", f), "utf-8");
const done = JSON.parse(read("done_checklist.json")) as ReviewRun;
const live = JSON.parse(read("live_checklist.json")) as ReviewRun;
const issuesDoc = JSON.parse(read("done_issues.json")) as IssuesDoc;
const issues = issuesDoc.issues;
const RECONCILE = read("done_reconcile_era.md");
const doneDir = `ai_videos/demo/reviews/${done.id}`;
const liveDir = `ai_videos/demo/reviews/${live.id}`;

// v2 单（没有 slots）带问题清单：真实的 chuanyue_yiri ep01 第 1 轮就是这种，要照旧渲染、只多一张问题清单摘要卡。
const v2Dir = "ai_videos/demo/reviews/ep01_20261108-120000_pregen_r1";
const v2: ReviewRun = {
  version: 2, id: "ep01_20261108-120000_pregen_r1", loop: 1, max_loops: 3, episode: "ep01", title: "ep01 · 出片前 · 第 1 轮", target: "x",
  stage: "pregen", stage_name: "出片前", scenes: ["s3"], created_at: "2026-11-08T12:00:00", author: "Claude Code", known: "", state: "已完成", log: [],
  items: [{ id: "physics_A", law: "physics", law_name: "世界物理", color: "#c0502e", scope: ["s3"], checks: "重力", how: "", status: "done",
    report: "reports/physics_A.md", prompt: "items/physics_A.md", ticked_by: "claude-opus-5-5/physics_A", findings: { 重出: 1 }, rows: 1 }],
};
const v2Issues: Issue[] = [{ id: "I1", key: "row:physics:s3st3:x", level: "critical", law: "physics", category: "世界物理", item: "physics_A",
  dimension: "道具守恒·数量", shots: ["s3_st3"], problem: "面包一瓣没少", evidence: ["`zoom_s3_st3_bread.jpg` 一瓣没少"], sources: ["claude-opus-5-5/physics_A"],
  fix: "重出首帧（便宜）", cost: "便宜", severity: "重出", rows: ["| s3_st3 | … |"], status: "implemented", solution: "首帧已重画", reason: "",
  history: [{ at: "2026-11-08T13:47:13", status: "implemented", solution: "首帧已重画" }] }];

/** 名册：从 fixture 的审稿项拼出 v5 法则（rubric、method、reviewers、model_why），不依赖仓库里会变的名册文件。 */
const roster = {
  version: 5, adjudicator: { runner: "claude", model: "claude-opus-5-5" },
  laws: Object.fromEntries(done.items.map(i => [i.law, { name: i.law_name, color: i.color, what: i.what, problem: i.problem, checks: i.checks, how: i.how,
    rubric: i.rubric, method: i.method, model_why: i.model_why, mechanisms: ["时代审稿人"],
    reviewers: Object.values(i.slots ?? {}).map(s => ({ slot: s.slot, runner: s.runner, model: s.model })) }])),
};

// 审查页经 /api/review-runs/checklist 读单（v5 单常超 /api/file 的 1 MiB 上限）；测试里沿用同一份 fetchFile 数据。
const { withChecklist } = vi.hoisted(() => ({
  withChecklist: <T extends { fetchFile: (p: string) => Promise<{ content: string }> }>(m: T) =>
    ({ ...m, fetchReviewChecklist: async (d: string) => JSON.parse((await m.fetchFile(`${d}/checklist.json`)).content) }),
}));
vi.mock("../src/api", () => withChecklist({
  fetchRepoSource: () => Promise.resolve({ path: "x", content: JSON.stringify(roster) }),
  fetchFile: (path: string) => {
    const ok = (content: string) => Promise.resolve({ path, content, encoding: "utf-8", bytes: 1, mtime: 0, mtime_http: "" });
    if (path === `${doneDir}/checklist.json`) return ok(JSON.stringify(done));
    if (path === `${liveDir}/checklist.json`) return ok(JSON.stringify(live));
    if (path === `${v2Dir}/checklist.json`) return ok(JSON.stringify(v2));
    if (path === `${doneDir}/issues.json`) return ok(JSON.stringify(issuesDoc));
    if (path === `${v2Dir}/issues.json`) return ok(JSON.stringify({ issues: v2Issues }));
    if (path.includes("/reconcile/")) return ok(RECONCILE);
    if (path.endsWith(".md")) return ok("# 报告\n结论：无问题");
    return Promise.reject(new Error(`404 ${path}`));
  },
  fetchReviewRuns: () => Promise.resolve({ runs: [] }),
  fetchSubtree: () => Promise.resolve({ type: "directory", name: "reviews", path: "ai_videos/demo/reviews", children: [] }),
}));

const era = (run: ReviewRun) => run.items.find(i => i.id === "era")!;

it("reads two scores per rubric dimension, the agreed score before adjudication, disputes and audits", () => {
  const rows = rubricRows([era(done)]);
  expect(rows.map(r => r.dim.id)).toEqual(["E1", "E2", "E3", "E4", "E5", "E6", "E7"]);
  const e3 = rows.find(r => r.dim.id === "E3")!;
  expect(e3.cells[0]).toMatchObject({ a: 1, b: 3, final: 1, verdict: "分歧", awaitingJudge: false });
  expect(e3.cells[0].judge_reason).toContain("证据成立");
  expect(e3.disputed).toBe(1);
  expect(rows.find(r => r.dim.id === "E1")!.low).toBe(1);
  expect(rows.filter(r => r.audited).length).toBe(era(done).audits!.length);
  // live：era 待裁决——分歧维度 final 未定（等裁决），一致维度先取低分
  const e1 = dimCell(era(live), "E1");
  expect(e1).toMatchObject({ a: 1, b: 3, verdict: "分歧", final: null, awaitingJudge: true });
  const agreed = Object.entries(era(live).scores!).find(([, v]) => v.verdict === "一致")!;
  expect(dimCell(era(live), agreed[0]).final).toBe(agreed[1].agreed);
  // 只勾了 a 的项：取 a 自己的分，b 还没有
  const pb = live.items.find(i => i.id === "physics_B")!;
  expect(dimCell(pb, "P1")).toMatchObject({ a: 3, b: undefined, awaitingJudge: false });
  // 实际跑的 agent：按位合并；physics_A 的 b 位有一次派单
  const tally = slotTally(live.items.filter(i => i.law === "physics"));
  expect(tally.find(t => t.slot === "b" && t.who === "Codex · gpt-6-astra")).toMatchObject({ count: 1, ticked: 1 });
});

it("counts, sorts, filters issues and finds what blocks the next round", () => {
  const c = issueCounts(issues);
  expect(c.level).toEqual({ critical: 3, major: 1, verify: 1, minor: 1 });
  expect(c.status).toEqual({ open: 3, planned: 1, implemented: 1, wontfix: 1 });
  expect(c.blocking).toBe(2);                                   // I3 planned（严重）＋ I4 open（主要）
  expect(issues.filter(blocksNextRound).map(i => i.id)).toEqual(["I3", "I4"]);
  expect(resolvedIssue({ ...issues[1], reason: "" })).toBe(false); // wontfix 不写理由不算处理
  expect(sortIssues([...issues].reverse()).map(i => i.level)).toEqual(["critical", "critical", "critical", "major", "verify", "minor"]);
  expect(filterIssues(issues, { level: "critical", status: "planned" }).map(i => i.id)).toEqual(["I3"]);
  expect(filterIssues(issues, { scene: "s1" }, done).map(i => i.id)).toEqual(["I1", "I2", "I4"]);   // 维度问题没镜头：取审稿项范围
  expect(issueScenes({ ...issues[0], shots: ["s4_st1（连带 s4_st2、st3）", "s6_st4"] })).toEqual(["s4", "s6"]);
  expect(reviewIssuesHref(doneDir, { level: "critical" })).toBe(`${REVIEW_ISSUES_ROUTE}?${new URLSearchParams({ path: doneDir, level: "critical" })}`);
  // 循环位置：本轮 → 问题 → 方案 → 实施 → 下一轮复核
  expect(loopPosition(live, null).step).toBe(0);
  expect(loopPosition(live, null).note).toContain("待裁决");
  expect(loopPosition(done, null).step).toBe(1);
  const pos = loopPosition(done, issues);
  expect(pos.step).toBe(2);
  expect(pos.note).toContain("还有 2 个严重 / 主要问题");
  const planned = issues.map(i => i.id === "I4" ? { ...i, status: "planned" } : i);
  expect(loopPosition(done, planned).step).toBe(3);
  const allDone = issues.map(i => blocksNextRound(i) ? { ...i, status: "implemented" } : i);
  expect(loopPosition(done, allDone)).toMatchObject({ step: 4, blockers: [] });
  expect(loopPosition({ ...done, child: "x" }, issues).step).toBe(4);
});

it("shows both reviewers per category on the checklist page, with tick state, attested ticks and 待裁决", async () => {
  const { ReviewRunPage } = await import("../src/components/ReviewRunPage");
  const { container } = render(<MemoryRouter initialEntries={[reviewRunHref(liveDir)]}><ReviewRunPage /></MemoryRouter>);
  await waitFor(() => expect(container.querySelectorAll("tbody tr").length).toBeGreaterThan(0));
  expect(screen.getByText(/项已审完（两位审稿人 \+ 对比 \+ 裁决）/)).toBeTruthy();
  expect(screen.getByText("2 项待裁决")).toBeTruthy();
  const pa = container.querySelector('.rv-chip5[data-item="physics_A"]')!;
  expect(pa.textContent).toContain("待裁决");
  expect(pa.querySelector('[data-slot="a"]')?.textContent).toContain("✓ Claude · claude-opus-5-5");
  expect(pa.querySelector('[data-slot="b"]')?.textContent).toContain("✓ Codex · gpt-6-astra");
  expect(pa.querySelector('[data-slot="b"]')?.textContent).toContain("代登记");
  expect(pa.querySelector('[data-slot="judge"]')?.textContent).toContain("Claude · claude-opus-5-5");
  expect(pa.getAttribute("href")).toBe(reviewItemHref(liveDir, "physics_A"));
  const pb = container.querySelector('.rv-chip5[data-item="physics_B"]')!;
  expect(pb.textContent).toContain("交 1/2");
  expect(pb.querySelector('[data-slot="b"]')?.textContent).toContain("○ Codex");
  expect(container.querySelector('.rv-chip5[data-item="continuity"] [data-slot="b"]')?.textContent).toContain("!");
  const physics = container.querySelector('tr[data-law="physics"]')!;
  expect(physics.textContent).toContain("待裁决 1");
  expect(container.querySelector(".rv-summary")).toBeNull();    // 没有 issues.json：不出摘要卡
});

it("puts a compact issue summary card on top of a run that has issues.json", async () => {
  const { ReviewRunPage } = await import("../src/components/ReviewRunPage");
  const { container } = render(<MemoryRouter initialEntries={[reviewRunHref(doneDir)]}><ReviewRunPage /></MemoryRouter>);
  await waitFor(() => expect(container.querySelector(".rv-summary")).toBeTruthy());
  const card = container.querySelector(".rv-summary")!;
  expect(card.textContent).toContain("6 条");
  expect(card.textContent).toContain("现在：方案");
  expect(card.textContent).toMatch(/严重\s*3/);
  expect(card.textContent).toMatch(/已定方案\s*1/);
  expect(card.textContent).toContain("还有 2 个未实施");
  const hrefs = [...card.querySelectorAll("a")].map(a => a.getAttribute("href"));
  expect(hrefs).toContain(reviewIssuesHref(doneDir));
  expect(hrefs).toContain(reviewIssuesHref(doneDir, { level: "critical" }));
  // 摘要卡在大类表之前
  expect(card.compareDocumentPosition(container.querySelector("table.rr-table")!) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
});

it("keeps a v2 run (no slots) as before, adding only the issue summary card", async () => {
  const { ReviewRunPage } = await import("../src/components/ReviewRunPage");
  const { container } = render(<MemoryRouter initialEntries={[reviewRunHref(v2Dir)]}><ReviewRunPage /></MemoryRouter>);
  await waitFor(() => expect(container.querySelector(".rv-summary")).toBeTruthy());
  expect(screen.getByText(/位审稿人已打勾/)).toBeTruthy();
  expect(container.querySelector(".rv-chip5")).toBeNull();
  expect(container.querySelector(".rr-agent")?.textContent).toContain("✓ physics_A");
  expect(container.querySelector(".rv-summary")?.textContent).toContain("严重与主要问题都已处理");
});

const renderIssues = (url: string) => import("../src/components/ReviewIssuesPage").then(({ ReviewIssuesPage }) =>
  render(<MemoryRouter initialEntries={[url]}><Routes><Route path={REVIEW_ISSUES_ROUTE} element={<ReviewIssuesPage />} /></Routes></MemoryRouter>));

it("lists derived issues critical first with level, status, cost, solution and the loop position", async () => {
  const { container } = await renderIssues(reviewIssuesHref(doneDir));
  await waitFor(() => expect(container.querySelectorAll("tr[data-issue]")).toHaveLength(6));
  const rows = [...container.querySelectorAll("tr[data-issue]")];
  expect(rows.map(r => r.getAttribute("data-level"))).toEqual(["critical", "critical", "critical", "major", "verify", "minor"]);
  expect(rows[0].querySelector(".rv-level-critical")?.textContent).toBe("严重");
  expect(rows[3].querySelector(".rv-level-major")?.textContent).toBe("主要");
  expect(rows[4].querySelector(".rv-level-verify")?.textContent).toBe("待核实");
  expect(rows[5].querySelector(".rv-level-minor")?.textContent).toBe("记录");
  const i2 = container.querySelector('tr[data-issue="I2"]')!;
  expect(i2.textContent).toContain("时代与世界观");
  expect(i2.textContent).toContain("E3 服饰与发型");
  expect(i2.querySelector(".rv-status-wontfix")?.textContent).toBe("不改");
  expect(i2.textContent).toContain("理由：要积分，交用户决定");
  expect(i2.querySelector(".rv-scores")?.textContent).toMatch(/a 1.*b 3.*1/);
  const i3 = container.querySelector('tr[data-issue="I3"]')!;
  expect(i3.textContent).toContain("s3_st1");
  expect(i3.querySelector(".rv-cost-paid")?.textContent).toBe("要积分");
  expect(i3.textContent).toContain("改场景图去掉百叶窗");
  expect(container.querySelector('tr[data-issue="I4"] .rv-cost-cheap')?.textContent).toBe("便宜");
  // 循环位置
  const loop = container.querySelector(".rv-loop")!;
  expect([...loop.querySelectorAll("li")].map(l => l.textContent)).toEqual(["本轮审查", "问题", "方案", "实施", "下一轮复核"]);
  expect(loop.querySelector(".rv-loop-now")?.textContent).toBe("方案");
  expect(container.querySelector(".rv-loop-note")?.textContent).toContain("其中严重 1、主要 1");
  // 展开证据：两位审稿人与裁决人各一行，标出是哪位、哪个模型、几分；再是历史
  fireEvent.click(within(i2 as HTMLElement).getByRole("button", { name: /证据/ }));
  const detail = container.querySelector('tr[data-detail="I2"]')!;
  const ev = [...detail.querySelectorAll(".rv-evidence li")].map(l => l.textContent);
  expect(ev[0]).toContain("a 位 · Claude · claude-opus-5-5 · 1 分");
  expect(ev[1]).toContain("b 位 · Codex · gpt-6-astra · 3 分");
  expect(ev[2]).toContain("裁决人 · Claude · claude-opus-5-5 · 1 分");
  expect(detail.textContent).toContain("gpt-6-astra/era__b");
  expect(detail.querySelector(".rv-history")?.textContent).toContain("保留现状");
});

it("filters issues by level, status, category and scene through the URL", async () => {
  const { container } = await renderIssues(reviewIssuesHref(doneDir, { level: "critical" }));
  await waitFor(() => expect(container.querySelectorAll("tr[data-issue]")).toHaveLength(3));
  expect(screen.getByText("显示 3 / 6")).toBeTruthy();
  fireEvent.change(screen.getByLabelText("状态"), { target: { value: "planned" } });
  await waitFor(() => expect([...container.querySelectorAll("tr[data-issue]")].map(r => r.getAttribute("data-issue"))).toEqual(["I3"]));
  fireEvent.click(screen.getByText("清除筛选"));
  await waitFor(() => expect(container.querySelectorAll("tr[data-issue]")).toHaveLength(6));
  fireEvent.change(screen.getByLabelText("场"), { target: { value: "s3" } });
  await waitFor(() => expect([...container.querySelectorAll("tr[data-issue]")].map(r => r.getAttribute("data-issue"))).toEqual(["I1", "I2", "I3"]));
  fireEvent.change(screen.getByLabelText("类别"), { target: { value: "时代与世界观" } });
  expect(container.querySelectorAll("tr[data-issue]")).toHaveLength(3);
});

it("explains how to derive issues when a run has none yet, and works for a v2 run's issues", async () => {
  const { container } = await renderIssues(reviewIssuesHref(liveDir));
  await waitFor(() => expect(screen.getByText(/这张单还没有问题清单/)).toBeTruthy());
  expect(container.querySelector(".rv-loop-now")?.textContent).toBe("本轮审查");
  const v = await renderIssues(reviewIssuesHref(v2Dir));
  await waitFor(() => expect(v.container.querySelectorAll("tr[data-issue]")).toHaveLength(1));
  expect(v.container.querySelector(".rv-loop-now")?.textContent).toBe("下一轮复核");
  fireEvent.click(within(v.container.querySelector('tr[data-issue="I1"]') as HTMLElement).getByRole("button", { name: /证据/ }));
  expect(v.container.querySelector(".rv-evidence code")?.textContent).toBe("zoom_s3_st3_bread.jpg");
});

it("turns the category's sub-check section into a rubric table: Claude a / Codex b / final per item, disputes, audits and rulings", async () => {
  const { ReviewLawPage } = await import("../src/components/ReviewLawPage");
  const { container } = render(<MemoryRouter initialEntries={[reviewLawHref(doneDir, "era")]}><ReviewLawPage /></MemoryRouter>);
  await waitFor(() => expect(container.querySelector(".rv-rubric")).toBeTruthy());
  const must = container.querySelector("[data-sec=must]")!;
  expect(must.querySelector("h2")?.textContent).toContain("细分成几个小类");
  expect(must.textContent).toContain("共 7 个维度");
  expect(must.textContent).toMatch(/分歧 1 处、抽查 2 处/);
  expect([...must.querySelectorAll("thead th")].map(t => t.textContent)).toEqual(["维度", "查什么", "Claude a 分", "Codex b 分", "最终", ""]);
  const e3 = must.querySelector('tr[data-dim="E3"]')!;
  expect([...e3.querySelectorAll(".rv-score")].map(s => s.textContent)).toEqual(["1", "3", "1"]);
  expect(e3.querySelector(".rv-s1")).toBeTruthy();
  expect(e3.querySelector(".rv-s3")?.getAttribute("title")).toContain("s1_st1 第3格逐格核过 服饰与发型");   // 悬停看证据
  expect(e3.querySelector(".rv-verdict-dispute")?.textContent).toBe("分歧");
  expect(e3.textContent).toContain("关键");
  expect(must.querySelectorAll("tbody .rv-verdict-audit")).toHaveLength(2);
  expect(must.querySelector('tr[data-dim="E1"] .rv-s0')).toBeTruthy();
  fireEvent.click(within(e3 as HTMLElement).getByRole("button", { name: "证据" }));
  const detail = must.querySelector('tr[data-detail="E3"]')!;
  expect(detail.textContent).toContain("a 位 · Claude a 分");
  expect(detail.textContent).toContain("b 位 · Codex b 分");
  expect(detail.textContent).toContain("分歧，最终 1 分：回到首帧第3格核过，证据成立");
  // 检查流程：method 步骤与双审说明；用了哪些 skill：model_why、两位审稿人与裁决人
  const flow = container.querySelector("[data-sec=flow]")!;
  expect(flow.textContent).toContain("审法（名册 method）");
  expect([...flow.querySelectorAll(".rl-method li")].map(l => l.textContent)).toEqual(era(done).method);
  expect(flow.textContent).toContain("a 位 Claude · claude-opus-5-5、b 位 Codex · gpt-6-astra");
  expect(flow.textContent).toContain("下一轮复核");
  const skills = container.querySelector("[data-sec=skills]")!;
  expect(skills.textContent).toContain(era(done).model_why!);
  expect(skills.textContent).toContain("a 位 Claude · claude-opus-5-5");
  expect(skills.textContent).toContain("b 位 Codex · gpt-6-astra");
  expect(skills.textContent).toContain("裁决人 Claude · claude-opus-5-5");
  expect([...skills.querySelectorAll("a")].map(a => a.getAttribute("href")).some(h => h?.endsWith("/items/era__judge.md"))).toBe(true);
  // 结果：双审卡与本类问题清单链接；对比文件里的问题表照旧合并
  await waitFor(() => expect(container.querySelector("[data-sec=result]")?.textContent).toContain("看这一类的问题清单"));
  const result = container.querySelector("[data-sec=result]")!;
  expect(result.querySelector('.rl-card[data-item="era"]')?.textContent).toContain("b ✓ Codex · gpt-6-astra");
  expect(result.textContent).toContain("这一类有 6 条（严重 3、未处理 3）");
  await waitFor(() => expect(result.querySelectorAll(".rl-findings tbody tr").length).toBeGreaterThan(0));
});

it("splits the rubric table into a/b/final columns per item part and marks pending adjudication", async () => {
  const { ReviewLawPage } = await import("../src/components/ReviewLawPage");
  const { container } = render(<MemoryRouter initialEntries={[reviewLawHref(liveDir, "physics")]}><ReviewLawPage /></MemoryRouter>);
  await waitFor(() => expect(container.querySelector(".rv-rubric")).toBeTruthy());
  const head = container.querySelectorAll(".rv-rubric thead tr");
  expect([...head[0].querySelectorAll(".rv-grp-id")].map(a => a.textContent)).toEqual(["physics_A", "physics_B", "physics_C"]);
  expect(head[1].querySelectorAll("th.rv-col")).toHaveLength(9);
  const p1 = container.querySelector('.rv-rubric tr[data-dim="P1"]')!;
  const cells = [...p1.querySelectorAll("td.rv-col")].map(t => t.textContent);
  expect(cells.slice(3, 6)).toEqual(["3", "—", "—"]);          // physics_B：只交了 a
  expect(cells.slice(6)).toEqual(["—", "—", "—"]);             // physics_C：都没交
  const audited = era(live) && live.items[0].audits![0];
  expect(container.querySelector(`.rv-rubric tr[data-dim="${audited}"]`)?.textContent).toContain("?");   // 抽查待裁决
  expect(container.querySelector("[data-sec=must]")?.textContent).toContain("1 项待裁决");
});

it("shows both reviewers side by side on a v5 item page, the attested-by-log tick and the reconcile/judge section", async () => {
  const { ReviewItemPage } = await import("../src/components/ReviewRunPage");
  const { container } = render(<MemoryRouter initialEntries={[reviewItemHref(liveDir, "physics_A")]}><ReviewItemPage /></MemoryRouter>);
  await waitFor(() => expect(container.querySelectorAll(".rv-slot")).toHaveLength(2));
  const [a, b] = [...container.querySelectorAll(".rv-slot")];
  expect(a.getAttribute("data-slot")).toBe("a");
  expect(a.querySelector("h3")?.textContent).toContain("Claude · claude-opus-5-5");
  expect(a.textContent).toContain("审稿人自己运行 tick");
  expect(a.querySelectorAll(".rv-slot-scores tr")).toHaveLength(8);
  expect(b.querySelector("h3")?.textContent).toContain("Codex · gpt-6-astra");
  expect(b.textContent).toContain("已勾（凭运行日志代登记）");
  expect(b.textContent).toContain("physics_A__b_attest.log");
  expect([...b.querySelectorAll("a")].map(x => x.getAttribute("href")).some(h => h?.endsWith("/agents/physics_A__b_attest.log"))).toBe(true);
  expect(b.textContent).toContain("第 1 次 Codex · gpt-6-astra");
  expect([...b.querySelectorAll("a")].map(x => x.textContent)).toEqual(expect.arrayContaining(["任务书", "报告", "指令"]));
  const rec = screen.getByRole("region", { name: "对比与裁决" });
  expect(rec.textContent).toContain("待裁决");
  expect(rec.textContent).toContain(`要裁的维度：${live.items[0].judge!.dims.join("、")}`);
  expect(rec.querySelectorAll(".rv-verdict-audit").length).toBeGreaterThan(0);
  expect(rec.querySelector(".rv-reconcile tbody tr")?.querySelectorAll(".rv-score")[2]?.textContent).not.toBe("—");   // 一致维度先显示取的分
  expect(screen.getByText("对比报告全文")).toBeTruthy();
});

it("shows a failed slot and a not-yet-reconciled item on the v5 item page", async () => {
  const { ReviewItemPage } = await import("../src/components/ReviewRunPage");
  const { container } = render(<MemoryRouter initialEntries={[reviewItemHref(liveDir, "continuity")]}><ReviewItemPage /></MemoryRouter>);
  await waitFor(() => expect(container.querySelectorAll(".rv-slot")).toHaveLength(2));
  expect(container.querySelector('.rv-slot[data-slot="b"]')?.textContent).toContain("失败：Codex 网络 403");
  expect(screen.getByRole("region", { name: "对比与裁决" }).textContent).toContain("两位审稿人都交报告并打勾后自动对比");
  expect(screen.getByText(/两位审稿人都打勾后生成/)).toBeTruthy();
});
