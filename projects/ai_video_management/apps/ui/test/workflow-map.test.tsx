import { describe, expect, it, beforeAll } from "vitest";
import { fireEvent, render, screen, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { WORKFLOW_MAP, workflowMapProblems } from "../src/lib/workflowMap";
import { WorkflowMapPage } from "../src/components/WorkflowMapPage";
import { WORKFLOW_MODULES, workflowNavigation } from "../src/lib/workflowData";
import registry from "../../../../../.agents/references/project/workflow_catalog.json";
import type { GlobalCatalog } from "../src/lib/globalWorkflow";

beforeAll(() => {
  globalThis.ResizeObserver ??= class { observe(): void {} unobserve(): void {} disconnect(): void {} } as unknown as typeof ResizeObserver;
});

describe("workflow map data", () => {
  it("is consistent and lists the same six modules as the UI, in order", () => {
    expect(workflowMapProblems(WORKFLOW_MAP)).toEqual([]);
    expect(WORKFLOW_MAP.modules.map(module => module.id)).toEqual(WORKFLOW_MODULES.map(module => module.id));
    const placeholders = WORKFLOW_MODULES.filter(module => module.placeholder).map(module => module.id);
    expect(WORKFLOW_MAP.modules.filter(module => module.status === "placeholder").map(module => module.id)).toEqual(placeholders);
  });
});

describe("overview navigation", () => {
  it("puts 总览 above the modules with the map and glossary as its pages", () => {
    const catalog = { groups: registry.groups, categories: registry.categories, sources: [] } as unknown as GlobalCatalog;
    const aiVideo = workflowNavigation(catalog).children?.[0];
    expect(aiVideo?.children?.[0].name).toBe("1.0_总览");
    expect(aiVideo?.children?.[0].children?.map(node => [node.name, node.navigation_href])).toEqual([["1.0.1_工作流全景", "/workflow/overview"], ["1.0.2_术语表", "/workflow/glossary"],
      ["1.0.3_决策记录", "/workflow/source?source_id=repo%3A.agents%2Fskills%2Fai-videos-pipeline%2Fmodules%2Fdecisions.md"]]);
    expect(aiVideo?.children?.slice(1, 7).map(node => node.path)).toEqual(WORKFLOW_MODULES.map(module => `/workflow/${module.id}`));
  });
});

describe("workflow map page", () => {
  it("shows the module table and details a module on selection", () => {
    render(<MemoryRouter><WorkflowMapPage /></MemoryRouter>);
    expect(screen.getByRole("tab", { name: "工作流全景" })).toHaveAttribute("aria-selected", "true");
    const table = screen.getByRole("table", { name: "模块一览" });
    expect(within(table).getAllByRole("row")).toHaveLength(WORKFLOW_MAP.modules.length + 1);
    fireEvent.click(within(table).getByRole("button", { name: "剪辑" }));
    const detail = screen.getByLabelText("节点详情");
    expect(within(detail).getByRole("heading", { level: 2 })).toHaveTextContent("剪辑");
    expect(within(detail).getByText("待设计")).toBeInTheDocument();
    expect(within(detail).getByText("锁片（用户批准）")).toBeInTheDocument();
  });
});
