import { describe, expect, it } from "vitest";
import { matchesNavigation, globalSourceUrl, type GlobalCatalog } from "../src/lib/globalWorkflow";
import { WORKFLOW_NAV_TREE, workflowNavigation } from "../src/lib/workflowData";
import { STORY_SECTIONS, storyTopicUrl, storyTopicContent } from "../src/lib/storyWorkflow";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

describe("global workflow navigation", () => {
  it("keeps the retired music library out of global resources", () => {
    const tree = workflowNavigation({ groups: [{ id: "resources", title: "资源", description: "" }], sources: [] });
    expect(tree.children?.[0].children?.[0].children?.map(node => node.navigation_href)).toEqual(["/actors", "/research"]);
  });
  it("keeps three modules available without the settings API", () => {
    expect(workflowNavigation(null)).toBe(WORKFLOW_NAV_TREE);
    expect(WORKFLOW_NAV_TREE.children?.slice(0, 2).map(node => node.name)).toEqual(["1_AI Video", "2_Claude Code与Codex"]);
    expect(WORKFLOW_NAV_TREE.children?.[0].children?.slice(0, 3).map(node => node.path)).toEqual(["/workflow/story", "/workflow/filming", "/workflow/prompts"]);
  });
  it("selects source identity precisely when the pathname is shared", () => {
    const first = globalSourceUrl("repo:AGENTS.md");
    expect(matchesNavigation(first, "/workflow/source", "?source_id=repo%3AAGENTS.md&other=x")).toBe(true);
    expect(matchesNavigation(first, "/workflow/source", "?source_id=repo%3ACONVENTIONS.md")).toBe(false);
    expect(matchesNavigation(first, "/workflow/story", "?source_id=repo%3AAGENTS.md")).toBe(false);
  });
  it("separates content and execution even when the catalog is unavailable", () => {
    const story = WORKFLOW_NAV_TREE.children?.[0].children?.[0];
    expect(story?.children?.map(node => node.name)).toEqual(["A_故事内容 · Content", "B_执行与验证 · Execution & Mechanics"]);
    expect(story?.children?.map(node => node.children?.length)).toEqual([6, 6]);
  });
  it("selects only one topic when several links share a source file", () => {
    const section = STORY_SECTIONS[0];
    const selected = new URL(storyTopicUrl(section, section.topics[0]), "http://workflow.local");
    expect(matchesNavigation(selected.pathname + selected.search, selected.pathname, selected.search)).toBe(true);
    expect(matchesNavigation(globalSourceUrl(section.source_id), selected.pathname, selected.search)).toBe(false);
    expect(matchesNavigation(storyTopicUrl(section, section.topics[1]), selected.pathname, selected.search)).toBe(false);
  });
  it("opens each registered topic from the current canonical document", () => {
    for (const section of STORY_SECTIONS) {
      const path = section.source_id.slice("repo:".length);
      const text = readFileSync(resolve(process.cwd(), "../../../..", path), "utf8");
      for (const topic of section.topics) {
        const content = storyTopicContent(text, topic.title);
        expect(content, topic.title).not.toBeNull();
        expect(content).not.toContain("\n## ");
      }
    }
  });
  it("keeps headings inside fenced commands and reports missing topics", () => {
    const text = "## First\n\n```bash\n## command comment\n```\n\nKeep this.\n\n## Second\nOther text.";
    expect(storyTopicContent(text, "First")).toContain("Keep this.");
    expect(storyTopicContent(text, "First")).not.toContain("Other text.");
    expect(storyTopicContent(text, "Missing")).toBeNull();
  });
  it("adds discovered settings to the corresponding module or global branch", () => {
    const catalog: GlobalCatalog = {
      groups: [{ id: "story", title: "故事创作", description: "" }, { id: "agents", title: "代理与执行设置", description: "" }],
      sources: [{ id: "repo:AGENTS.md", title: "共用入口", path: "AGENTS.md", group: "agents", scope: "repo", view: "document", status: "available", historical: false }],
    };
    const tree = workflowNavigation(catalog);
    const settings = tree.children?.find(node => node.path === "/workflow/category/agents")?.children?.[0];
    expect(settings?.children?.[0].navigation_href).toBe(globalSourceUrl("repo:AGENTS.md"));
    expect(tree.children?.[0].children?.[0].path).toBe("/workflow/story");
  });
});
