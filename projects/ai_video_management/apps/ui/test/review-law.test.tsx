import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { expect, it, vi } from "vitest";
import { agentTally, lawMust, mergeFindings, mustMatrix, parseFindings, reviewLawHref, severityOf } from "../src/lib/reviewLaw";
import { reviewRunHref, type ReviewRun } from "../src/lib/reviewRun";

// 审查大类页（follow-up 338）：先讲这一类是什么、想解决什么、几个小类、怎么查、用了哪些 skill，最后给结果。
vi.setConfig({ testTimeout: 30000 });

const NL = String.fromCharCode(10);
const dir = "ai_videos/demo/reviews/ep01_20261108-090000_pregen_r2";
const oldDir = "ai_videos/demo/reviews/ep01_20261107-090000_full_r1";

const state = vi.hoisted(() => ({ rosterFails: false }));

const ROSTER = { version: 4, laws: {
  physics: { name: "世界物理", color: "#c0502e", partition: "pairs", what: "东西不会悬空、不会凭空出现。", problem: "模型最常犯的硬伤。",
    examples: ["s3_st2 面包黏在指尖", "s6_st2 铜钱悬空"], must: [{ id: "P1", text: "手数" }, { id: "P2", text: "道具来源" }],
    checks: "重力与支撑", how: "逐镜看 sheet4.jpg", mechanisms: ["物理审稿人（逐镜规格）", "镜头接口帧拼图"] },
  native_ear: { name: "母语听感", partition: "whole", blind: true, prefer_model: "codex", blind_note: "**只读 `materials/lines.md`**",
    what: "母语者听着自然吗", problem: "直译腔", examples: [], must: [{ id: "N1", text: "逐句判断" }], checks: "逐句听", how: "只用台词表", mechanisms: ["母语听感审稿人"] },
} };

const claude = { runner: "Claude Code 子代理（Agent 工具）", model: "claude-opus-5-5", prompt: "agents/x.md", at: "2026-11-08T09:00:00" };
const codex = { runner: "Codex CLI（codex exec）", model: "gpt-6-astra（reasoning high）", prompt: "agents/y.md", at: "2026-11-08T09:00:00" };
const base = { law: "physics", law_name: "世界物理", color: "#c0502e", checks: "快照：重力", how: "快照：看拼图", status: "done" as const };
const run: ReviewRun = {
  version: 2, id: "ep01_20261108-090000_pregen_r2", loop: 2, max_loops: 3, episode: "ep01", title: "ep01 · 出片前 · 第 2 轮",
  target: "ai_videos/demo/episodes/ep01", stage: "pregen", stage_name: "出片前", scenes: ["s1", "s2", "s3"], created_at: "2026-11-08T09:00:00",
  author: "Claude Code", known: "", state: "已完成", log: [],
  items: [
    { ...base, id: "physics_A", scope: ["s1", "s2"], report: "reports/physics_A.md", prompt: "items/physics_A.md", ticked_by: "claude-opus-5-5/physics_A",
      must: [{ id: "P1", text: "手数" }, { id: "P2", text: "道具来源" }, { id: "R", text: "复核上一轮" }], must_result: { P1: "✓", P2: "✗", R: "✓" },
      findings: { 重出: 1, 记录: 1 }, rows: 2, agents: [{ n: 1, ...claude }] },
    { ...base, id: "physics_B", scope: ["s3"], report: "reports/physics_B.md", prompt: "items/physics_B.md", ticked_by: "claude-opus-5-5/physics_B",
      must: [{ id: "P1", text: "手数" }, { id: "P2", text: "道具来源" }, { id: "R", text: "复核上一轮" }], must_result: { P1: "✗", P2: "✓" },
      findings: { 可剪: 1, 存疑: 1 }, rows: 2, agents: [{ n: 1, ...codex }, { n: 2, ...claude }] },
    { ...base, id: "native_ear", law: "native_ear", law_name: "母语听感", scope: ["s1", "s2", "s3"], report: "reports/native_ear.md",
      prompt: "items/native_ear.md", ticked_by: "claude-opus-5-5/native_ear", findings: {}, rows: 0, agents: [{ n: 1, ...codex }, { n: 2, ...claude }] },
  ],
};
const old: ReviewRun = { ...run, id: "ep01_20261107-090000_full_r1", loop: 1, title: "ep01 · 全量 · 第 1 轮",
  items: run.items.slice(0, 2).map(i => ({ ...i, must: undefined, must_result: undefined, agents: undefined, ticked_by: `claude-opus-5-5-subagent/${i.id}` })) };

const table = (rows: string[][]): string => rows.map(r => `| ${r.join(" | ")} |`).join(NL);
const HEAD = ["镜头", "原条秒数", "法则·子类", "严重度", "本该哪关抓到", "证据", "建议改动"];
const RULE = HEAD.map(() => "---");
const REPORT_A = ["# physics_A", "", "## 道具状态表", "", table([["道具", "s1", "s2"], ["---", "---", "---"], ["钱", "4 枚 重出", "3 枚"]]), "",
  "## 问题表", "", table([HEAD, RULE, ["s1_st2", "3–5 秒", "道具·钱悬空", "**记录**", "③", "钱在 `sheet4.jpg` 第 3 格悬空", "便宜：改文字"],
    ["s1_st1", "0 秒", "手数·两只手", "重出", "②", "自拍时两只手都在干活", "要积分：重出"]]), ""].join(NL);
const REPORT_B = ["# physics_B", "", table([HEAD, RULE, ["s3_st1", "1 秒", "支撑·灰浆", "存疑（偏模型）", "④", "证据".repeat(60), "便宜"],
  ["s3_st2", "2 秒", "穿模", "可剪", "④", "骡筐穿过工人", "剪掉 0–1.5 秒"]]), ""].join(NL);

// 审查页经 /api/review-runs/checklist 读单（v5 单常超 /api/file 的 1 MiB 上限）；测试里沿用同一份 fetchFile 数据。
const { withChecklist } = vi.hoisted(() => ({
  withChecklist: <T extends { fetchFile: (p: string) => Promise<{ content: string }> }>(m: T) =>
    ({ ...m, fetchReviewChecklist: async (d: string) => JSON.parse((await m.fetchFile(`${d}/checklist.json`)).content) }),
}));
vi.mock("../src/api", () => withChecklist({
  fetchRepoSource: () => state.rosterFails ? Promise.reject(new Error("404")) : Promise.resolve({ path: "x", content: JSON.stringify(ROSTER) }),
  fetchFile: (path: string) => Promise.resolve({
    path, encoding: "utf-8", bytes: 1, mtime: 0, mtime_http: "",
    content: path.endsWith("checklist.json") ? JSON.stringify(path.includes("full_r1") ? old : run)
      : path.endsWith("physics_A.md") ? REPORT_A : path.endsWith("physics_B.md") ? REPORT_B : "# 无问题" + NL + "结论：无问题",
  }),
  fetchReviewRuns: () => Promise.resolve({ runs: [] }),
  fetchSubtree: () => Promise.resolve({ type: "directory", name: "reviews", path: "ai_videos/demo/reviews", children: [] }),
}));

it("parses only tables with a 严重度 header and sorts merged findings by severity", () => {
  const a = parseFindings(REPORT_A, "physics_A");
  expect(a.map(f => f.shot)).toEqual(["s1_st2", "s1_st1"]);             // 道具状态表里的「重出」不算
  expect(a[0]).toMatchObject({ severity: "记录", sub: "道具·钱悬空", time: "3–5 秒", fix: "便宜：改文字" });
  expect(severityOf("存疑（偏模型）").severity).toBe("存疑");
  expect(severityOf("记录（重出时改）").severity).toBe("重出");          // 与 review_run.py parse_report 计数同一规则
  expect(severityOf("通过").rank).toBe(4);
  const merged = mergeFindings([{ item: "physics_A", text: REPORT_A }, { item: "physics_B", text: REPORT_B }]);
  expect(merged.map(f => `${f.severity}:${f.item}`)).toEqual(["重出:physics_A", "可剪:physics_B", "记录:physics_A", "存疑:physics_B"]);
});

it("builds the sub-check matrix per reviewer and tallies the agents that ran", () => {
  const items = run.items.slice(0, 2);
  const { must, fromRun } = lawMust(items, ROSTER.laws.physics as never);
  expect(fromRun).toBe(true);
  expect(mustMatrix(items, must).map(m => [m.id, ...m.cells])).toEqual([["P1", "✓", "✗"], ["P2", "✗", "✓"], ["R", "✓", "—"]]);
  expect(lawMust(old.items, ROSTER.laws.physics as never)).toMatchObject({ fromRun: false, must: [{ id: "P1" }, { id: "P2" }] });
  expect(agentTally(items)).toEqual([{ who: "Claude 子代理 · claude-opus-5-5", count: 2, ticked: 2 }, { who: "Codex · gpt-6-astra", count: 1, ticked: 0 }]);
});

it("explains the category first (what, problem, sub-checks, process, skills) and only then the results", async () => {
  state.rosterFails = false;
  const { ReviewLawPage } = await import("../src/components/ReviewLawPage");
  const { container } = render(<MemoryRouter initialEntries={[reviewLawHref(dir, "physics")]}><ReviewLawPage /></MemoryRouter>);
  await waitFor(() => expect(container.querySelectorAll(".rl-findings tbody tr")).toHaveLength(4));
  const secs = [...container.querySelectorAll("section[data-sec]")];
  expect(secs.map(s => s.getAttribute("data-sec"))).toEqual(["what", "problem", "must", "flow", "skills", "result"]);
  expect(secs.map(s => s.querySelector("h2")?.textContent)).toEqual(["这一类是什么", "想解决什么问题", "细分成几个小类", "检查流程", "用了哪些 skill / 规则", "检查结果"]);
  expect(secs[0].textContent).toContain("东西不会悬空");
  expect(secs[1].textContent).toContain("真实踩过的例子");
  expect(secs[1].querySelectorAll("li")).toHaveLength(2);
  expect(secs[2].textContent).toContain("共 2 个小类");
  expect(secs[2].textContent).toContain("这是第 2 轮");
  // 小类 × 审稿人
  const head = [...secs[2].querySelectorAll("thead th")].map(t => t.textContent);
  expect(head).toEqual(["小类", "查什么", "physics_A", "physics_B"]);
  const p2 = [...secs[2].querySelectorAll("tbody tr")].find(r => r.querySelector("th")?.textContent === "P2")!;
  expect([...p2.querySelectorAll("td")].slice(1).map(t => t.textContent)).toEqual(["✗", "✓"]);
  expect(secs[3].textContent).toContain("每两场一位审稿人");
  expect(secs[3].textContent).toContain("physics_A（s1、s2）");
  expect(secs[3].textContent).toContain("逐镜看 sheet4.jpg");
  expect(secs[3].textContent).toContain("本单是第 2 / 3 轮");
  expect(secs[4].textContent).toContain("物理审稿人（逐镜规格）");
  expect(secs[4].textContent).toContain("Claude 子代理 · claude-opus-5-5 ×2");
  expect(secs[4].textContent).toContain("Codex · gpt-6-astra ×1（没打勾）");
  const hrefs = [...secs[4].querySelectorAll("a")].map(a => a.getAttribute("href"));
  expect(hrefs.some(h => h?.includes("review_roster.json"))).toBe(true);
  expect(hrefs.some(h => h?.endsWith("/BRIEF.md"))).toBe(true);
  expect(hrefs.some(h => h?.endsWith("/items/physics_B.md"))).toBe(true);
  // 结果：每位审稿人一张卡，再合并问题表
  expect(secs[5].textContent).toContain("共 4 条");
  expect([...secs[5].querySelectorAll(".rl-card")].map(c => c.getAttribute("data-item"))).toEqual(["physics_A", "physics_B"]);
  const rows = [...secs[5].querySelectorAll(".rl-findings tbody tr")];
  expect(rows.map(r => r.getAttribute("data-sev"))).toEqual(["重出", "可剪", "记录", "存疑"]);
  expect(rows[0].textContent).toContain("手数·两只手");
  expect(rows[0].lastElementChild?.textContent).toBe("physics_A");
  expect(rows[2].querySelector("code")?.textContent).toBe("sheet4.jpg");
  expect(rows[3].textContent).toContain("展开");                         // 长证据先截断
  expect(screen.queryByText("钱")).toBeNull();
});

it("notes blind review and a preferred model that the ticking agent did not use", async () => {
  state.rosterFails = false;
  const { ReviewLawPage } = await import("../src/components/ReviewLawPage");
  const { container } = render(<MemoryRouter initialEntries={[reviewLawHref(dir, "native_ear")]}><ReviewLawPage /></MemoryRouter>);
  await waitFor(() => expect(container.querySelector("[data-sec=flow]")).toBeTruthy());
  expect(container.querySelector("[data-sec=flow]")?.textContent).toContain("盲审");
  expect(container.querySelector("[data-sec=flow]")?.textContent).toContain("只读 materials/lines.md");
  expect(container.querySelector("[data-sec=must]")?.textContent).toContain("共 1 个小类");
  expect(container.querySelector("[data-sec=skills]")?.textContent).toContain("没用上 codex");
  await waitFor(() => expect(container.querySelector("[data-sec=result]")?.textContent).toContain("报告里没有问题行"));
});

it("degrades for an old run without sub-check results or dispatch records", async () => {
  state.rosterFails = false;
  const { ReviewLawPage } = await import("../src/components/ReviewLawPage");
  const { container } = render(<MemoryRouter initialEntries={[reviewLawHref(oldDir, "physics")]}><ReviewLawPage /></MemoryRouter>);
  await waitFor(() => expect(container.querySelectorAll(".rl-findings tbody tr")).toHaveLength(4));
  const must = container.querySelector("[data-sec=must]")!;
  expect(must.textContent).toContain("没有逐项结果");
  expect([...must.querySelectorAll("thead th")].map(t => t.textContent)).toEqual(["小类", "查什么"]);
  expect(must.textContent).toContain("第 2 轮起");
  expect(container.querySelector("[data-sec=skills]")?.textContent).toContain("没有派单记录（旧单），只知道打勾署名：claude-opus-5-5-subagent ×2");
});

it("falls back to the checklist snapshot when the roster cannot be read", async () => {
  state.rosterFails = true;
  const { ReviewLawPage } = await import("../src/components/ReviewLawPage");
  const { container } = render(<MemoryRouter initialEntries={[reviewLawHref(dir, "physics")]}><ReviewLawPage /></MemoryRouter>);
  await waitFor(() => expect(screen.getByText(/读不到，下面只按这张审查单里的快照显示/)).toBeTruthy());
  expect(container.querySelector("[data-sec=what]")?.textContent).toContain("快照：重力");
  expect(container.querySelector("[data-sec=problem]")?.textContent).toContain("名册里还没有写");
  expect(container.querySelector("[data-sec=flow]")?.textContent).toContain("快照：看拼图");
  state.rosterFails = false;
});

it("links each category name on the checklist page to its category page; reviewer chips still open the detail page", async () => {
  const { ReviewRunPage } = await import("../src/components/ReviewRunPage");
  const { container } = render(<MemoryRouter initialEntries={[reviewRunHref(dir)]}><ReviewRunPage /></MemoryRouter>);
  await waitFor(() => expect(container.querySelectorAll("tbody tr")).toHaveLength(2));
  const row = container.querySelector("tbody tr")!;
  expect(row.querySelector("th a")?.getAttribute("href")).toBe(reviewLawHref(dir, "physics"));
  expect([...row.querySelectorAll(".rr-agent")].map(a => a.getAttribute("href"))).toEqual([
    `/review-run/item?${new URLSearchParams({ path: dir, item: "physics_A" })}`, `/review-run/item?${new URLSearchParams({ path: dir, item: "physics_B" })}`]);
});
