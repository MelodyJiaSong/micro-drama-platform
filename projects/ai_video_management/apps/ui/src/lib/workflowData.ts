import type { ModuleId } from "./episodeWorkflow";
import type { TreeNode } from "../types";
import { GLOBAL_COVERAGE_PATH, globalGroupUrl, globalSourceUrl, numberedTitle, sourceTitle, type GlobalCatalog, type GlobalCategory, type GlobalGroup } from "./globalWorkflow";
import registry from "../../../../../../.agents/references/project/workflow_catalog.json";
import { storyNavigation } from "./storyWorkflow";

export const WORKFLOW_PATH = "/workflow";
export const workflowModulePath = (id: ModuleId): string => `${WORKFLOW_PATH}/${id}`;
export const FILMING_KNOWLEDGE_PATH = `${workflowModulePath("filming")}/shot-sizes`;

export const WORKFLOW_MODULES: { id: ModuleId; title: string; purpose: string; input: string; output: string }[] = [
  { id: "story", title: "故事创作", purpose: "先写好故事，再考虑怎么拍。", input: "故事方向", output: "小说式故事稿" },
  { id: "filming", title: "影视改编", purpose: "设计观众能看见和听见的内容。", input: "已确定的故事", output: "可拍的分镜" },
  { id: "prompts", title: "Prompt 编译", purpose: "按固定规则准确表达分镜。", input: "已确定的分镜", output: "每镜 Prompt" },
];

export const categoryUrl = (id: string): string => `${WORKFLOW_PATH}/category/${id}`;
export const workflowCategories = (catalog: GlobalCatalog | null): GlobalCategory[] => catalog?.categories?.length ? catalog.categories : registry.categories;
export const workflowGroups = (catalog: GlobalCatalog | null): GlobalGroup[] => catalog ? catalog.groups.map(group => ({ ...registry.groups.find(entry => entry.id === group.id), ...group })) : registry.groups;

export function workflowNavigation(catalog: GlobalCatalog | null): TreeNode {
  if (!catalog) return WORKFLOW_NAV_TREE;
  return buildNavigation(catalog);
}

function buildNavigation(catalog: GlobalCatalog | null): TreeNode {
  const groups = workflowGroups(catalog);
  const children: TreeNode[] = workflowCategories(catalog).map(category => ({
    type: "directory", name: numberedTitle(category), path: categoryUrl(category.id), navigation_href: categoryUrl(category.id),
    children: [...groups.filter(group => group.category === category.id).map((group): TreeNode => {
    const module = WORKFLOW_MODULES.find(entry => entry.id === group.id);
    const href = module ? workflowModulePath(module.id) : globalGroupUrl(group.id);
    return { type: "directory", name: numberedTitle(group), path: href, navigation_href: href,
      children: group.id === "story" ? storyNavigation(catalog) : [...(group.id === "filming" && !catalog ? [{
        type: "file" as const, name: sourceTitle({ title: "镜头类型与景别", number: registry.source_numbers["repo:.agents/references/project/ai_video_shot_sizes.md"] }),
        path: FILMING_KNOWLEDGE_PATH, navigation_href: FILMING_KNOWLEDGE_PATH,
      }] : []), ...(catalog?.sources || []).filter(source => source.group === group.id).map(source => ({
        type: "file" as const, name: `${sourceTitle(source)}${source.scope === "user" ? " · 用户" : ""}${source.historical ? " · 历史参考" : ""}`,
        path: `/workflow/source/${encodeURIComponent(source.id)}`, navigation_href: globalSourceUrl(source.id),
      })), ...(group.id === "services" ? [{ type: "file" as const, name: "全局请求审计", path: "/workflow/request-logs", navigation_href: "/request-logs" }] : []),
      ...(group.id === "resources" ? [
        { type: "file" as const, name: "公共演员库", path: "/workflow/actors", navigation_href: "/actors" },
        { type: "file" as const, name: "调研库", path: "/workflow/research", navigation_href: "/research" },
      ] : [])],
    };
  }), ...(category.id === "ai-video" ? [{ type: "file" as const, name: "工作流覆盖核对", path: GLOBAL_COVERAGE_PATH, navigation_href: GLOBAL_COVERAGE_PATH }] : [])],
  }));
  return { type: "directory", name: "工作流", path: WORKFLOW_PATH, navigation_href: WORKFLOW_PATH, children };
}

export const WORKFLOW_NAV_TREE: TreeNode = buildNavigation(null);
