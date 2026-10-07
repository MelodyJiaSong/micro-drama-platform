import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, Routes, Route, Link } from "react-router-dom";
import { afterEach, expect, it, vi } from "vitest";
import { StoryRunsPage } from "../src/components/StoryRunsPage";
import { StoryRunStoryPage } from "../src/components/StoryRunStoryPage";
import { StoryRunStatePage } from "../src/components/StoryRunStatePage";
import { StoryRunInputPage } from "../src/components/StoryRunInputPage";
import { StoryRunItemPage } from "../src/components/StoryRunItemPage";
import { StoryRunProcessPage } from "../src/components/StoryRunProcessPage";
import { StoryRunComparePage } from "../src/components/StoryRunComparePage";
import { STORY_RUN_PAGES, storyRunUrl, type StoryRunDocument } from "../src/lib/storyRunRoutes";
import { SharedStoryInputPage } from "../src/components/SharedStoryInputPage";
import { Sidebar } from "../src/components/Sidebar";
import type { StoryRun } from "../src/lib/storyRuns";
import type { TreeNode } from "../src/types";

afterEach(() => { cleanup(); vi.unstubAllGlobals(); });
const episode = "ai_videos/demo/episodes/ep01";
const frame = { who: "学徒", what: "送信", why: "履行承诺", when: "黎明", where: "村口", how: "穿过树林" };
function fixture(id: string): StoryRun {
  return { schema_version: 1, run_id: id, episode_path: episode, created_at: "2026-10-03T10:00:00Z", status: "completed",
    input: { frame, brief: "本次独立输入", assumptions: ["新故事假设"], sources: [], rules: [], input_hash: id, independence: "不加载上一轮草稿" },
    participants: [{ id: "author", name: "故事作者", role: "作者", scope: "story", status: "completed", prompt: "真实分配任务", output: "真实返回内容" },
      { id: "ui", name: "UI开发", role: "展示实现", scope: "implementation", status: "completed", prompt: "开发展示", output: "已实现" }],
    events: [{ id: "e1", at: "2026-10-03T10:01:00Z", actor: "author", type: "proposal", title: "写作意见提交", body: "先明确动机", proposal_ids: ["p1"], artifact_refs: [] }],
    proposals: [{ id: "p1", agent_id: "author", title: "明确承诺", detail: "补充出发原因", reason: "动机不清", location: "开头", decision: "accepted", decision_reason: "有助于因果理解", decided_by: "author", criteria: ["因果清楚"], evidence: [], applied_in: "第一段" },
      { id: "p2", agent_id: "author", title: "加入新反派", detail: "追加角色", reason: "制造冲突", location: "结尾", decision: "rejected", decision_reason: "超出本次事件", decided_by: "author", criteria: [], evidence: [], applied_in: null }],
    candidate: { frame, brief: "候选方向", text: `候选正文-${id}`, state_changes: ["信已送达"] }, artifacts: [] };
}
function list(): unknown {
  return { episode_path: episode, runs: ["r1", "r2"].map(run_id => ({ run_id, created_at: "2026-10-03T10:00:00Z", status: "completed", participant_count: 2, proposal_count: 2, input_hash: run_id })) };
}
function response(body: unknown): Response { return { ok: true, json: async () => body } as Response; }
function page(document: StoryRunDocument = "output", runId?: string, itemId?: string): void {
  render(<MemoryRouter initialEntries={[storyRunUrl(document, episode, runId, undefined, itemId)]}>
    <Link to={storyRunUrl(document, episode, "r2")}>查看第二次 r2</Link>
    <Routes>
      <Route path="/story-runs" element={<StoryRunsPage />} />
      <Route path={STORY_RUN_PAGES.output.path} element={<StoryRunStoryPage />} />
      <Route path={STORY_RUN_PAGES.state.path} element={<StoryRunStatePage />} />
      <Route path={STORY_RUN_PAGES.input.path} element={<StoryRunInputPage />} />
      <Route path={STORY_RUN_PAGES.item.path} element={<StoryRunItemPage />} />
      <Route path={STORY_RUN_PAGES.process.path} element={<StoryRunProcessPage />} />
      <Route path={STORY_RUN_PAGES.compare.path} element={<StoryRunComparePage />} />
    </Routes>
  </MemoryRouter>);
}

it("展示真实参与者、完整任务、决定理由并筛选意见", async () => {
  const fetch = vi.fn(async (url: string) => response(url.includes("/detail?") ? fixture("r1") : list()));
  vi.stubGlobal("fetch", fetch); page("process");
  await screen.findByText("真实分配任务");
  expect(screen.queryByText("候选正文-r1")).not.toBeInTheDocument();
  expect(screen.queryByRole("navigation", { name: "创作记录视图" })).not.toBeInTheDocument();
  expect(screen.getByText("系统实现")).toBeInTheDocument();
  expect(screen.getByText("真实分配任务")).toBeInTheDocument();
  expect(screen.getByText("有助于因果理解")).toBeInTheDocument();
  expect(screen.getByText("超出本次事件")).toBeInTheDocument();
  expect(screen.getAllByText("未公开")).toHaveLength(4);
  fireEvent.change(screen.getByLabelText("筛选"), { target: { value: "rejected" } });
  expect(screen.queryByText("明确承诺")).not.toBeInTheDocument();
  expect(screen.getByText("加入新反派")).toBeInTheDocument();
  expect(fetch.mock.calls.every(([url]) => String(url).startsWith("/api/story-runs"))).toBe(true);
});

it("切换独立运行立即清空上一轮正文，拒绝晚到的上一轮响应", async () => {
  let resolveFirst: ((value: Response) => void) | undefined;
  vi.stubGlobal("fetch", vi.fn((url: string) => {
    if (url.includes("run_id=r1")) return new Promise<Response>(resolve => { resolveFirst = resolve; });
    return Promise.resolve(response(url.includes("/detail?") ? fixture("r2") : list()));
  })); page();
  await waitFor(() => expect(resolveFirst).toBeDefined());
  fireEvent.click(screen.getByRole("link", { name: /r2/ }));
  await screen.findByText("候选正文-r2");
  resolveFirst!(response(fixture("r1")));
  await waitFor(() => expect(screen.queryByText("候选正文-r1")).not.toBeInTheDocument());
  expect(screen.getByText("候选正文-r2")).toBeInTheDocument();
});

it("拒绝详情归属错误并显示可理解的错误", async () => {
  const wrong = { ...fixture("r1"), episode_path: "ai_videos/other/episodes/ep01" };
  vi.stubGlobal("fetch", vi.fn(async (url: string) => response(url.includes("/detail?") ? wrong : list())));
  page();
  expect(await screen.findByRole("alert")).toHaveTextContent("记录归属不匹配");
  expect(screen.queryByText("候选正文-r1")).not.toBeInTheDocument();
});

it("创作记录是可点击与键盘打开的独立导航叶子", async () => {
  const selected = vi.fn();
  const node: TreeNode = { type: "story_runs", name: "story_runs", display_name: "创作记录", path: `${episode}/story_runs.json`, episode_path: episode };
  render(<MemoryRouter><Sidebar tree={{ type: "section", name: "root", path: "", children: [node] }} currentPath="" onSelect={selected} /></MemoryRouter>);
  const item = screen.getByRole("treeitem", { name: "创作记录" });
  fireEvent.keyDown(item, { key: "Enter" });
  await waitFor(() => expect(item).toHaveAttribute("aria-selected", "true"));
  expect(selected).not.toHaveBeenCalled();
});

it("每个run文档按run和视图精确路由及高亮，目录只展开", async () => {
  const selected = vi.fn();
  const leaf = (view: "output" | "state"): TreeNode => ({ type: "story_runs", name: view, display_name: view === "output" ? "候选故事" : "候选状态变化",
    path: `${episode}/runs/r1/${view}.json`, episode_path: episode, story_run_id: "r1", story_run_view: view });
  const folder: TreeNode = { type: "directory", name: "r1", display_name: "run1", path: `${episode}/runs/r1`, children: [leaf("output"), leaf("state")] };
  render(<MemoryRouter><Sidebar tree={{ type: "section", name: "root", path: "", children: [{ type: "directory", name: "EP1", path: episode, children: [folder] }] }} currentPath="" onSelect={selected} /></MemoryRouter>);
  const root = screen.getByText("run1").closest('[role="treeitem"]')!; fireEvent.click(root);
  expect(root).toHaveAttribute("aria-expanded", "true");
  const output = screen.getByText("候选故事").closest('[role="treeitem"]')!;
  const state = screen.getByText("候选状态变化").closest('[role="treeitem"]')!;
  fireEvent.click(output); await waitFor(() => expect(output).toHaveAttribute("aria-selected", "true"));
  expect(state).toHaveAttribute("aria-selected", "false");
  fireEvent.keyDown(state, { key: "Enter" }); await waitFor(() => expect(state).toHaveAttribute("aria-selected", "true"));
  expect(output).toHaveAttribute("aria-selected", "false");
  expect(selected).not.toHaveBeenCalled();
});

it("区分共享源、冻结输入、本轮产出与过程文件，并保持只读", async () => {
  const run = fixture("r1");
  run.input.sources = [{ path: "ai_videos/demo/world_rules.md", sha256: "frozen-123", content: "本轮冻结的事实" }];
  run.artifacts = [
    { id: "input", kind: "input", scope: "shared", name: "共享创作输入", path: `${episode}/story_input.json`, status: "draft" },
    { id: "output", kind: "input", scope: "run", name: "冻结快照", path: ".audit/run1/input.json", sha256: "output-123" },
    { id: "process", kind: "process", scope: "run", name: "实际任务", path: ".audit/run1/spawns/author/prompt.md" },
  ];
  vi.stubGlobal("fetch", vi.fn(async (url: string) => response(url.includes("/detail?") ? run : list()))); page("input");
  await screen.findByText("本次独立输入");
  expect(screen.queryByText("候选正文-r1")).not.toBeInTheDocument();
  expect(screen.getByText(/本页只读。通过 Claude Code\/Codex 修改/)).toBeInTheDocument();
  expect(screen.getAllByText("本轮冻结的事实", { exact: false }).length).toBeGreaterThan(0);
  expect(screen.getAllByText("frozen-123", { exact: false }).length).toBeGreaterThan(0);
  expect(screen.getAllByText(/不代表当前最新文件/).length).toBeGreaterThan(0);
  expect(screen.getByRole("table", { name: "历史文件登记" })).toHaveTextContent("共享源 · Persistent，跨 run 复用");
  expect(screen.getByRole("table", { name: "历史文件登记" })).toHaveTextContent("本次 run · Transient，历史留存");
  expect(screen.queryByRole("textbox")).not.toBeInTheDocument();
  expect(screen.queryByRole("button", { name: /保存|编辑|确定版本/ })).not.toBeInTheDocument();
});

it("对比相同输入与实际冻结规则，复制选用命令不发写请求", async () => {
  const first = fixture("r1"); const second = fixture("r2");
  first.input.input_hash = second.input.input_hash = "same-input";
  first.input.rules = [{ path: "rules.md", content: "规则正文", sha256: "same" }];
  second.input.rules = [{ sha256: "same", content: "规则正文", path: "rules.md" }];
  const clipboard = { writeText: vi.fn(async () => {}) };
  vi.stubGlobal("navigator", { clipboard });
  const fetch = vi.fn(async (url: string, _options?: RequestInit) => response(url.includes("/detail?") ? new URL(url, "http://localhost").searchParams.get("run_id") === "r1" ? first : second : { ...list() as object, selection: { run_id: "r1", status: "selected" } }));
  vi.stubGlobal("fetch", fetch); page();
  await screen.findByText("候选正文-r1");
  expect(screen.getByText(/已选为故事草稿，尚未确定/)).toBeInTheDocument();
  fireEvent.click(screen.getByRole("button", { name: "复制选用命令" }));
  await waitFor(() => expect(clipboard.writeText).toHaveBeenCalledWith(`python tools/story_run.py promote --episode-path '${episode}' --run-id 'r1'`));
  fireEvent.click(screen.getByRole("link", { name: "对比其他候选" }));
  await screen.findByText("输入指纹相同（覆盖规则）");
  expect(screen.getByText("冻结规则快照相同")).toBeInTheDocument();
  expect(screen.getByLabelText("A 候选")).toHaveTextContent("候选正文-r1");
  expect(screen.getByLabelText("B 候选")).toHaveTextContent("候选正文-r2");
  expect(screen.getByText(/不足以证明规则造成质量变化/)).toBeInTheDocument();
  expect(fetch.mock.calls.every(call => call.length === 1 || !(call[1] as RequestInit)?.method)).toBe(true);
});

it("比较不同输入，并避免B切换后混入晚到旧运行", async () => {
  let resolveSecond: ((value: Response) => void) | undefined;
  const third = fixture("r3"); third.input.rules = ["改过的规则"];
  vi.stubGlobal("fetch", vi.fn((url: string) => {
    const runId = new URL(url, "http://localhost").searchParams.get("run_id");
    if (runId === "r2") return new Promise<Response>(resolve => { resolveSecond = resolve; });
    return Promise.resolve(response(runId ? runId === "r1" ? fixture("r1") : third : { ...list() as object, runs: ["r1", "r2", "r3"].map(run_id => ({ run_id, status: "candidate", created_at: "2026-10-03T10:00:00Z", participant_count: 1, proposal_count: 0, input_hash: run_id })) }));
  })); page();
  await screen.findByText("候选正文-r1");
  fireEvent.click(screen.getByRole("link", { name: "对比其他候选" }));
  await waitFor(() => expect(resolveSecond).toBeDefined());
  fireEvent.change(screen.getByLabelText("B · 对比查看"), { target: { value: "r3" } });
  await screen.findByText("输入指纹不同");
  expect(screen.getByText("冻结规则快照不同")).toBeInTheDocument();
  resolveSecond!(response(fixture("r2")));
  await waitFor(() => expect(screen.getByLabelText("B 候选")).toHaveTextContent("候选正文-r3"));
  expect(screen.queryByText("候选正文-r2")).not.toBeInTheDocument();
});

it("共享输入以六问、Markdown资料及版本切换呈现，不展示编码JSON", async () => {
  const fetch = vi.fn(async (url: string) => {
    const id = new URL(url, "http://localhost").searchParams.get("profile_id") || "baseline-v1";
    const input = fixture(id).input;
    input.brief = id === "baseline-v1" ? "两轮共用方向" : "后续方向";
    input.rules = [{ path: "rules.md", sha256: "rule-sha", content: "# 规则正文\n\n先明确人物动机。" }];
    input.sources = [{ path: "research.md", sha256: "source-sha", content: "选用北郡背景。", selection: "explicit_excerpt" }];
    return response({ episode_path: episode, selected_profile: "baseline-v1", profile_id: id,
      profiles: [{ id: "baseline-v1", label: "两次共用对照基线", input_path: "baseline/input.json", rules_path: "baseline/rules.json", input_hash: "base", rules_hash: "rule" },
        { id: "workflow-v2", label: "后续流程版本（本次未使用）", input_path: "v2/input.json", rules_path: "v2/rules.json", input_hash: "new", rules_hash: "rule-new" }], input });
  });
  vi.stubGlobal("fetch", fetch);
  render(<MemoryRouter initialEntries={[`/story-input?episode_path=${encodeURIComponent(episode)}`]}><SharedStoryInputPage /></MemoryRouter>);
  await screen.findByText("两轮共用方向");
  expect(screen.getByText("谁 · Who")).toBeInTheDocument();
  expect(screen.getByText("取用范围：明确选定摘录")).toBeInTheDocument();
  fireEvent.click(screen.getByRole("link", { name: "查看创作规则" }));
  await screen.findByRole("heading", { name: "创作规则" });
  expect(screen.getByRole("heading", { name: "规则正文" })).toBeInTheDocument();
  expect(screen.getByText("先明确人物动机。")).toBeInTheDocument();
  expect(screen.queryByText("谁 · Who")).not.toBeInTheDocument();
  expect(screen.queryByText(/\\n先明确/)).not.toBeInTheDocument();
  fireEvent.change(screen.getByLabelText("查看版本"), { target: { value: "workflow-v2" } });
  await waitFor(() => expect(screen.getByLabelText("查看版本")).toHaveValue("workflow-v2"));
  fireEvent.click(screen.getByRole("link", { name: "查看共享创作输入" }));
  await screen.findByText("后续方向");
  expect(screen.queryByText("两轮共用方向")).not.toBeInTheDocument();
  expect(screen.queryByRole("textbox")).not.toBeInTheDocument();
  expect(fetch.mock.calls.some(([url]) => url.includes("profile_id=workflow-v2"))).toBe(true);
});

it("共享配置的输入与规则两个导航文档单独高亮", async () => {
  const input: TreeNode = { type: "story_input", name: "input", display_name: "创作输入", path: `${episode}/shared/index.json`, episode_path: episode, story_input_view: "input" };
  const rules: TreeNode = { type: "story_input", name: "rules", display_name: "创作规则", path: `${episode}/shared/rules-view.json`, episode_path: episode, story_input_view: "rules" };
  render(<MemoryRouter initialEntries={[`/story-input?episode_path=${encodeURIComponent(episode)}&view=rules`]}>
    <Sidebar tree={{ type: "directory", name: "shared", display_name: "共享配置 · Persistent", path: `${episode}/shared`, children: [input, rules] }} currentPath="" onSelect={vi.fn()} />
  </MemoryRouter>);
  const inputNode = screen.getByText("创作输入").closest('[role="treeitem"]')!;
  const ruleNode = screen.getByText("创作规则").closest('[role="treeitem"]')!;
  expect(ruleNode).toHaveAttribute("aria-selected", "true");
  expect(inputNode).toHaveAttribute("aria-selected", "false");
  fireEvent.click(inputNode);
  await waitFor(() => expect(inputNode).toHaveAttribute("aria-selected", "true"));
  expect(ruleNode).toHaveAttribute("aria-selected", "false");
});

it("当前EP是单一快捷链接，点击展开并选中实际run文档", async () => {
  const target: TreeNode = { type: "story_runs", name: "output", display_name: "候选故事", path: `${episode}/runs/r2/output.json`, episode_path: episode, story_run_id: "r2", story_run_view: "output" };
  const alias: TreeNode = { ...target, name: "current", display_name: "当前 EP1 → run2", path: `${episode}/current`, is_link: true };
  render(<MemoryRouter><Sidebar tree={{ type: "section", name: "EP1", path: episode, children: [alias,
    { type: "directory", name: "run2", path: `${episode}/runs/r2`, children: [target] }] }} currentPath="" onSelect={vi.fn()} /></MemoryRouter>);
  const link = screen.getByText("当前 EP1 → run2").closest('[role="treeitem"]')!;
  expect(link).not.toHaveAttribute("aria-expanded");
  fireEvent.keyDown(link, { key: "Enter" });
  const document = await screen.findByText("候选故事");
  await waitFor(() => expect(document.closest('[role="treeitem"]')).toHaveAttribute("aria-selected", "true"));
  expect(link).toHaveAttribute("aria-selected", "false");
});


it("输入清单软链接打开本次规则快照，展示来源变化且不同资料不串页", async () => {
  const run = fixture("r1");
  const item = (id: string, name: string, value: string) => ({ id, group: "rules", group_label: "流程规则", name,
    value, target: `.audit/run1/run.json#/input/rules/${id}`, snapshot_hash: "snapshot-abc", note: "采用当时冻结版本",
    scope: "run", kind: "input" as const, source_path: ".agents/skills/ai-videos-pipeline/modules/story.md",
    source_hash: "old-sha", source_status: { status: "changed" as const, sha256: "new-sha" } });
  run.io = { items: [item("rules-0", "故事规则", "# 当时冻结的规则正文"), item("task-0", "作者任务", "实际任务附加约束")],
    audit_path: ".audit/run1/run.json", coverage: "未记录的采样参数无法补证" };
  vi.stubGlobal("fetch", vi.fn(async (url: string) => response(url.includes("/detail?") ? run : list())));
  page("input");
  fireEvent.click(await screen.findByRole("link", { name: "故事规则 ↗" }));
  await screen.findByRole("heading", { name: "故事规则", level: 1 });
  expect(screen.getByText("当时冻结的规则正文")).toBeInTheDocument();
  expect(screen.getAllByRole("heading", { level: 1 })).toHaveLength(1);
  expect(screen.getByText("源文件已变化；本页保留当时版本")).toBeInTheDocument();
  expect(screen.getByText("old-sha")).toBeInTheDocument();
  expect(screen.getByText("new-sha")).toBeInTheDocument();
  expect(screen.queryByText("候选正文-r1")).not.toBeInTheDocument();
  fireEvent.click(screen.getByRole("link", { name: "查看本run完整输入清单" }));
  fireEvent.click(await screen.findByRole("link", { name: "作者任务 ↗" }));
  await screen.findByRole("heading", { name: "作者任务", level: 1 });
  expect(screen.getByText("实际任务附加约束")).toBeInTheDocument();
  expect(screen.queryByText("当时冻结的规则正文")).not.toBeInTheDocument();
});

it("run软链接按item精确高亮并支持直接打开", async () => {
  const node = (id: string): TreeNode => ({ type: "story_runs", name: id, display_name: id,
    path: `${episode}/runs/r1/links/${id}.json`, episode_path: episode, story_run_id: "r1", story_run_view: "item",
    story_run_item_id: id, is_link: true });
  render(<MemoryRouter initialEntries={[storyRunUrl("item", episode, "r1", undefined, "rules-1")]}>
    <Sidebar tree={{ type: "section", name: "root", path: "", children: [node("rules-0"), node("rules-1")] }} currentPath="" onSelect={vi.fn()} />
  </MemoryRouter>);
  const first = screen.getByText("rules-0").closest('[role="treeitem"]')!;
  const second = screen.getByText("rules-1").closest('[role="treeitem"]')!;
  expect(first).toHaveAttribute("aria-selected", "false");
  expect(second).toHaveAttribute("aria-selected", "true");
  expect(screen.getAllByRole("treeitem", { selected: true })).toHaveLength(1);
  fireEvent.keyDown(first, { key: "Enter" });
  await waitFor(() => expect(first).toHaveAttribute("aria-selected", "true"));
  expect(second).toHaveAttribute("aria-selected", "false");
});

it("规则中的相对引用打开同run冻结版本，文件元数据单独展示", async () => {
  const run = fixture("r1");
  const common = { group: "rules", group_label: "流程规则", target: ".audit/run/run.json#/input/rules/0",
    snapshot_hash: "sha", scope: "run", kind: "input" as const, note: "" };
  run.io = { audit_path: ".audit/run/run.json", coverage: "历史冻结版本", items: [
    { ...common, id: "rules-0", name: "总入口", source_path: ".agents/skills/pipeline/SKILL.md",
      value: "---\nname: pipeline\ndescription: 原始元数据\n---\n# 正文\n\n[故事模块](modules/story.md)\n\n[其他模块](modules/absent.md)" },
    { ...common, id: "rules-1", name: "故事模块快照", source_path: ".agents/skills/pipeline/modules/story.md", value: "当时故事规则" },
  ] };
  vi.stubGlobal("fetch", vi.fn(async (url: string) => response(url.includes("/detail?") ? run : list())));
  page("item", "r1", "rules-0");
  await screen.findByRole("heading", { name: "总入口", level: 1 });
  expect(screen.getByText("文件元数据（原文）")).toBeInTheDocument();
  expect(screen.getByText(/name: pipeline/)).toHaveTextContent("description: 原始元数据");
  expect(screen.getByText("其他模块（未记录引用）")).toBeInTheDocument();
  expect(screen.queryByRole("link", { name: "其他模块" })).not.toBeInTheDocument();
  fireEvent.click(screen.getByRole("link", { name: /^故事模块$/ }));
  await screen.findByRole("heading", { name: "故事模块快照", level: 1 });
  expect(screen.getByText("当时故事规则")).toBeInTheDocument();
});
