import { act, cleanup, fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, expect, it, vi } from "vitest";
import { DevPreviewPage } from "../src/components/DevPreviewPage";
import { devPreviewHref, isFrameworkRoot, limitOver, pageTitle, parseSections } from "../src/lib/devPreview";
import { abilityChart, buildModel, conflictChart, parseTable, peopleChart, secretsByStage, splitMermaid, worldChart } from "../src/lib/devDiagrams";
import { fetchFile, fetchSubtree } from "../src/api";

vi.mock("../src/api", async original => ({ ...await original<typeof import("../src/api")>(), fetchFile: vi.fn(), fetchSubtree: vi.fn() }));
vi.mock("../src/lib/fileEvents", () => ({ useFileChanges: () => undefined }));
// jsdom 量不了 SVG 文字尺寸；这里只验证图源被交给 mermaid。
vi.mock("mermaid", () => ({ default: { initialize: vi.fn(), render: vi.fn(async (_id: string, src: string) => ({ svg: `<svg><desc>${src.split("\n")[0]}</desc></svg>` })) } }));
afterEach(() => { cleanup(); vi.clearAllMocks(); });

const dir = "ai_videos/xihuan/framework/examples/lotr";
const lib = "ai_videos/_shared/xihuan/library.json";
const pages = {
  "01_主题": "# 01 主题 · 指环王\n## 一句话\n权力会腐蚀每一个想用它行善的人。\n## 英文 logline\nA hobbit must destroy a ring.\n## 一段\n一段话。\n## 一页\n一页。\n",
  "02_世界": "# 02 世界\n## 舞台\n中土。\n## 种族与势力\n| 名称 | 库 | 一句话 |\n|---|---|---|\n| 精灵 | RC02 | 正在离开 |\n| 魔多 | 原创 | 想要戒指 |\n## 关系\n| 从 | 关系 | 到 |\n|---|---|---|\n| 精灵 | 世仇 | 魔多 |\n",
  "04_人物": "# 04 人物\n## 人物\n| 编号 | 名字 | 身份 | 想要 | 缺陷 |\n|---|---|---|---|---|\n| P01 | 弗罗多 | 持戒人 | 回家 | 天真 |\n| **P02** | 山姆 | 园丁 | 守护 | 胆小 |\n## 能力\n| 编号 | 外在 | 外 | 内在 | 内 |\n|---|---|---|---|---|\n| P01 | 体弱 | 1 | 扛得住戒指 | 5 |\n| P02 | 能打 | 1 | 忠心 | 5 |\n## 关系\n| 从 | 关系 | 到 |\n|---|---|---|\n| P02 | 誓死追随 | P01 |\n",
  "05_矛盾": "# 05 矛盾\n## 主要矛盾\nP01 与魔多争夺戒指。\n## 矛盾图\n| 一方 | 争什么 | 另一方 | 主次 |\n|---|---|---|---|\n| P01 | 戒指 | 魔多 | 主 |\n| P01 | 信任 | P02 | 次 |\n## 内在矛盾\n放下与占有。\n",
};
const files: Record<string, string> = {
  ...Object.fromEntries(Object.entries(pages).map(([k, v]) => [`${dir}/${k}.md`, v])),
  [lib]: JSON.stringify({ title: "西幻", version: "1.1", assets: [{ id: "RC02", name: "精灵", image: { anchor: "entries/rc02/anchor_v2.png", status: "reviewed" } }] }),
  [`${dir}/_check.json`]: JSON.stringify({ generated: "2026-11-08T10:00:00+00:00", ok: false, errors: ["缺页：03_力量.md"], warnings: ["06_秘密与伏笔「戒指」的「何时揭开」没写故事阶段"],
    pages: { "01_主题": { exists: true, required: true, missing_sections: [], limits: { "一句话": { chars: 17, limit: 40 } } },
      "03_力量": { exists: false, required: true }, "06_秘密与伏笔": { exists: false, required: false } } }),
  [`${dir}/_反馈.md`]: "## 反馈\n人物页最好填。\n",
};

async function mount(url: string): Promise<void> {
  vi.mocked(fetchFile).mockImplementation(async (path: string) => {
    if (!(path in files)) throw new Error("404");
    return { path, content: files[path] } as Awaited<ReturnType<typeof fetchFile>>;
  });
  vi.mocked(fetchSubtree).mockResolvedValue({ type: "directory", name: "examples", path: "ai_videos/xihuan/framework/examples",
    children: [{ type: "directory", name: "lotr", path: dir }] });
  render(<MemoryRouter initialEntries={[url]}><DevPreviewPage /></MemoryRouter>);
  for (let i = 0; i < 3; i += 1) await act(async () => { await new Promise(r => setTimeout(r, 0)); });
}

it("parses sections and titles the same way check.py does", () => {
  expect(parseSections("# t\n## 一句话\n甲\n## 一段\n乙\n")).toEqual({ "一句话": "甲", "一段": "乙" });
  expect(pageTitle("# 01 主题 · 指环王\n", "x")).toBe("指环王");
  expect(isFrameworkRoot("ai_videos/xihuan/framework")).toBe(true);
  expect(isFrameworkRoot(dir)).toBe(false);
  expect(limitOver({ chars: 41, limit: 40 })).toBe(true);
  expect(devPreviewHref(dir, { tab: "review" })).toBe(`/dev-preview?path=${encodeURIComponent(dir)}&tab=review`);
  expect(parseTable("| a | b |\n|---|---|\n")).toEqual([]);
});

it("turns tables into diagrams: names instead of IDs, main conflicts thick, protagonist highlighted", () => {
  const m = buildModel(pages);
  expect(worldChart(m)).toContain('n0 -->|"世仇"| n1');
  const people = peopleChart(m)!;
  expect(people).toContain('("山姆")');
  expect(people).toMatch(/class n\d hero/);
  const conflict = conflictChart(m)!;
  expect(conflict).toContain('{{"魔多"}}');
  expect(conflict).toContain('===|"戒指"|');
  expect(conflict).toContain('-.-|"信任"|');
  expect(conflict).toContain("linkStyle 0 stroke:#b03a2e");
  const quad = abilityChart(m)!;
  expect(quad).toContain('"弗罗多": [0.10, 0.90] radius: 9, color: #b7791f');
  expect(quad).toContain('"山姆": [0.05, 0.90] radius: 6');
  expect(abilityChart(buildModel({}))).toBeNull();
  const ring = buildModel({ ...pages, "03_力量": "## 力量源\n| 力量 | 库 | 谁拥有 | 代价 |\n|---|---|---|---|\n| 魔戒 | IT26 | P01 | 腐蚀 |\n",
    "05_矛盾": "## 矛盾图\n| 一方 | 争什么 | 另一方 | 主次 |\n|---|---|---|---|\n| P01 | 放下 | 魔戒 | 主 |\n" });
  expect(conflictChart(ring)).toContain('(["魔戒"])');
  expect(secretsByStage([{ secret: "s", who: "P01", when: "中点前后", change: "c" }]).find(l => l.stage === "中点")?.items).toHaveLength(1);
  expect(splitMermaid("a\n```mermaid\nflowchart LR\n```\nb").map(p => p.kind)).toEqual(["md", "mermaid", "md"]);
});

it("previews a dev folder: overview board first, then per-page pictures with the source folded", async () => {
  await mount(devPreviewHref(dir));
  expect(screen.getByRole("heading", { name: "指环王" })).toBeTruthy();
  expect(screen.getByRole("tab", { name: "全景" }).getAttribute("aria-selected")).toBe("true");
  expect(screen.getByLabelText("全景 · 主题").textContent).toContain("权力会腐蚀每一个想用它行善的人。");
  expect(screen.getByRole("img", { name: "矛盾图" }).innerHTML).toContain("flowchart LR");
  fireEvent.click(screen.getByRole("tab", { name: "世界" }));
  expect(document.querySelector(".dev-callout")?.textContent).toBe("舞台中土。");
  expect(screen.getByRole("img", { name: "RC02 精灵" }).getAttribute("src")).toContain(encodeURIComponent("ai_videos/_shared/xihuan/entries/rc02/anchor_v2.png"));
  expect(screen.getByText("原文")).toBeTruthy();
  fireEvent.click(screen.getByRole("tab", { name: "人物" }));
  expect(screen.getByLabelText("人物").textContent).toContain("主角");
  expect(screen.getByLabelText("人物").textContent).toContain("扛得住戒指");
  expect(screen.getAllByRole("img", { name: "内在 5/5" })).toHaveLength(2);
  expect((await screen.findByRole("img", { name: "内外能力象限图" })).innerHTML).toContain("quadrantChart");
  fireEvent.click(screen.getByRole("tab", { name: "其他 · 秘密与伏笔" }));
  expect(screen.getByText("这一页可以之后再补。")).toBeTruthy();
  fireEvent.click(screen.getByRole("tab", { name: "力量" }));
  expect(screen.getByText("这一页还没写。")).toBeTruthy();
});

it("reviews a dev folder: check result, per-page limits and feedback", async () => {
  await mount(devPreviewHref(dir, { tab: "review" }));
  expect(screen.getByLabelText("形式检查").textContent).toContain("形式检查未通过 · 1 处");
  expect(screen.getByText("缺页：03_力量.md")).toBeTruthy();
  expect(screen.getByLabelText("形式检查").textContent).toContain("一句话 17/40 字");
  expect(screen.getByLabelText("形式检查").textContent).toContain("未写（可选）");
  expect(screen.getByText("人物页最好填。")).toBeTruthy();
});

it("shows the framework root with its flow diagram and links to every worked example", async () => {
  files["ai_videos/xihuan/framework/README.md"] = "# 西幻新剧开发框架\n```mermaid\nflowchart LR\n  T --> W\n```\n五页。\n";
  files["ai_videos/xihuan/framework/templates/01_主题.md"] = "# 01 主题\n## 必填小节\n### 一句话\n";
  await mount(devPreviewHref("ai_videos/xihuan/framework"));
  expect(screen.getByRole("heading", { name: "新剧开发框架" })).toBeTruthy();
  expect(screen.getByRole("img", { name: "流程图" })).toBeTruthy();
  expect(screen.getByText("五页。")).toBeTruthy();
  expect(screen.getByRole("link", { name: "试套 · 指环王" }).getAttribute("href")).toBe(devPreviewHref(dir));
  fireEvent.click(screen.getByRole("tab", { name: "试套评估" }));
  expect(screen.getByText(/试套评估还没写/)).toBeTruthy();
});
