import { describe, expect, it } from "vitest";
import { matchesNavigation, globalSourceUrl, sourceAdaptations, type GlobalCatalog } from "../src/lib/globalWorkflow";
import { WORKFLOW_NAV_TREE, workflowNavigation } from "../src/lib/workflowData";
import registry from "../../../../../.agents/references/project/workflow_catalog.json";
import type { TreeNode } from "../src/types";

describe("global workflow navigation", () => {
  it("lists only catalog sources under a settings group", () => {
    const tree = workflowNavigation({ groups: [{ id: "production", title: "制作、服务与资源", description: "" }], sources: [] });
    expect(tree.children?.[0].children?.[0].children).toEqual([]);
  });
  it("numbers every workflow entry contiguously from the repository catalog", () => {
    const catalog: GlobalCatalog = {
      groups: registry.groups, categories: registry.categories,
      sources: Object.entries(registry.source_numbers).map(([id, number]) => {
        const [scope, path] = [id.slice(0, id.indexOf(":")), id.slice(id.indexOf(":") + 1)];
        const listed = registry.sources.find(source => source.path === path);
        const group = listed?.group ?? registry.groups.find(entry => number.startsWith(`${entry.number}.`))!.id;
        const parent = (listed as { parent?: string } | undefined)?.parent;
        return { id, path, title: listed?.title ?? path, group, scope: scope as "repo" | "user", view: "document", status: "available" as const, historical: false, number, ...(parent ? { parent: `repo:${parent}` } : {}) };
      }).sort((a, b) => a.number.localeCompare(b.number, undefined, { numeric: true })),
    };
    const unnumbered: string[] = [];
    const visit = (node: TreeNode, depth: number): void => {
      if (depth > 0 && !/^\d+(\.\d+)*_/.test(node.name)) unnumbered.push(node.name);
      node.children?.forEach(child => visit(child, depth + 1));
    };
    visit(workflowNavigation(catalog), 0);
    expect(unnumbered).toEqual([]);
    for (const category of registry.categories) {
      const groups = registry.groups.filter(group => group.category === category.id && !(group as { overview?: boolean }).overview).map(group => group.number);
      expect(groups).toEqual(groups.map((_, index) => `${category.number}.${index + 1}`));
    }
    for (const container of [...registry.groups.map(group => ({ id: undefined as string | undefined, group: group.id, number: group.number })),
      ...catalog.sources.map(source => ({ id: source.id, group: source.group, number: source.number! }))]) {
      const numbers = catalog.sources.filter(source => source.group === container.group && source.parent === container.id).map(source => source.number);
      expect(numbers, container.number).toEqual(numbers.map((_, index) => `${container.number}.${index + 1}`));
    }
    const story = workflowNavigation(catalog).children?.[0].children?.find(node => node.path === "/workflow/story");
    const structure = story?.children?.[0];
    expect(structure?.children?.length).toBeGreaterThan(0);
    expect(structure?.children?.every(node => node.name.startsWith(`${structure.name.split("_")[0]}.`))).toBe(true);
  });
  it("keeps the overview and the modules available without the settings API", () => {
    expect(workflowNavigation(null)).toBe(WORKFLOW_NAV_TREE);
    expect(WORKFLOW_NAV_TREE.children?.slice(0, 2).map(node => node.name)).toEqual(["1_AI Video", "2_系统与代码"]);
    expect(WORKFLOW_NAV_TREE.children?.[0].children?.slice(0, 4).map(node => node.path)).toEqual(["/workflow/settings/overview", "/workflow/story", "/workflow/filming", "/workflow/prompts"]);
  });
  it("selects source identity precisely when the pathname is shared", () => {
    const first = globalSourceUrl("repo:AGENTS.md");
    expect(matchesNavigation(first, "/workflow/source", "?source_id=repo%3AAGENTS.md&other=x")).toBe(true);
    expect(matchesNavigation(first, "/workflow/source", "?source_id=repo%3ACONVENTIONS.md")).toBe(false);
    expect(matchesNavigation(first, "/workflow/story", "?source_id=repo%3AAGENTS.md")).toBe(false);
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
  it("lists every format page that adapts a shared principle", () => {
    const base = { scope: "repo" as const, view: "document", status: "available" as const, historical: false, group: "story" };
    const catalog: GlobalCatalog = {
      groups: [{ id: "story", title: "故事创作", description: "", number: "1.1", category: "ai-video" }],
      categories: [{ id: "ai-video", title: "AI Video", description: "", number: "1" }],
      formats: [{ id: "film", title: "电影" }, { id: "series", title: "连续剧" }],
      sources: [
        { ...base, id: "repo:acts.md", path: "acts.md", title: "三幕", number: "1.1.1" },
        { ...base, id: "repo:film.md", path: "film.md", title: "电影", number: "1.1.2", formats: ["film"], adapts: [{ source_id: "repo:acts.md", section: "节点位置" }] },
        { ...base, id: "repo:series.md", path: "series.md", title: "连续剧", number: "1.1.3", formats: ["series"], adapts: [{ source_id: "repo:acts.md", section: "三幕放在哪一层" }] },
      ],
    };
    expect(workflowNavigation(catalog).children?.[0].children?.[0].children?.map(node => node.name)).toEqual(["1.1.1_三幕", "1.1.2_电影", "1.1.3_连续剧"]);
    expect(sourceAdaptations(catalog, "repo:acts.md").map(entry => [entry.source.id, entry.section])).toEqual([["repo:film.md", "节点位置"], ["repo:series.md", "三幕放在哪一层"]]);
    expect(sourceAdaptations(catalog, "repo:film.md")).toEqual([]);
  });
});
