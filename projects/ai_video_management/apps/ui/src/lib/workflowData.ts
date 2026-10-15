import type { StageId } from "./episodeWorkflow";
import type { TreeNode } from "../types";
import { globalGroupUrl, globalSourceUrl, numberedTitle, sourceTitle, type GlobalCatalog, type GlobalCategory, type GlobalGroup, type GlobalSource } from "./globalWorkflow";
import registry from "../../../../../../.agents/references/project/workflow_catalog.json";

export const WORKFLOW_PATH = "/workflow";
export const workflowModulePath = (id: StageId): string => `${WORKFLOW_PATH}/${id}`;
export const FILMING_KNOWLEDGE_PATH = `${workflowModulePath("filming")}/shot-sizes`;
export const GLOSSARY_PATH = `${WORKFLOW_PATH}/glossary`;
export const OVERVIEW_PATH = `${WORKFLOW_PATH}/overview`;
export const DECISIONS_SOURCE = "repo:.agents/skills/ai-videos-pipeline/modules/decisions.md";
export const FILMING_SHOTS_SOURCE = "repo:.agents/skills/ai-videos-pipeline/modules/filming-shots.md";

export const WORKFLOW_MODULES: { id: StageId; title: string; purpose: string; input: string; output: string; placeholder?: boolean }[] = [
  { id: "story", title: "故事创作", purpose: "先写好故事，再考虑怎么拍。", input: "故事方向", output: "小说式故事稿" },
  { id: "filming", title: "影视改编", purpose: "设计观众能看见和听见的内容。", input: "已确定的故事", output: "可拍的分镜" },
  { id: "prompts", title: "Prompt 编译与出片", purpose: "按固定规则准确表达分镜，再生成各镜头的条。", input: "已确定的分镜", output: "每镜 Prompt 与生成的条" },
  { id: "edit", title: "剪辑", purpose: "选条、粗剪、精剪到锁片。", input: "各镜头的条", output: "锁片版本", placeholder: true },
  { id: "sound", title: "声音与音乐", purpose: "对白、环境声与音效、音乐与混音。", input: "锁片版本", output: "混音与分轨", placeholder: true },
  { id: "delivery", title: "成片交付", purpose: "调色、字幕、AI 标识、质检与母版。", input: "锁片版本与终混", output: "平台母版", placeholder: true },
];

export const categoryUrl = (id: string): string => `${WORKFLOW_PATH}/category/${id}`;
export const workflowCategories = (catalog: GlobalCatalog | null): GlobalCategory[] => catalog?.categories?.length ? catalog.categories : registry.categories;
export const workflowGroups = (catalog: GlobalCatalog | null): GlobalGroup[] => catalog ? catalog.groups.map(group => ({ ...registry.groups.find(entry => entry.id === group.id), ...group })) : registry.groups;

export function workflowNavigation(catalog: GlobalCatalog | null): TreeNode {
  if (!catalog) return WORKFLOW_NAV_TREE;
  return buildNavigation(catalog);
}

function sourceNodes(sources: GlobalSource[], parent?: string): TreeNode[] {
  const ids = new Set(sources.map(source => source.id));
  return sources.filter(source => parent ? source.parent === parent : !source.parent || !ids.has(source.parent)).map(source => {
    const children = sourceNodes(sources, source.id);
    return {
      type: children.length ? "directory" as const : "file" as const,
      name: `${sourceTitle(source)}${source.scope === "user" ? " · 用户" : ""}${source.historical ? " · 历史参考" : ""}`,
      path: `/workflow/source/${encodeURIComponent(source.id)}`, navigation_href: globalSourceUrl(source.id),
      ...(children.length ? { children } : {}),
    };
  });
}

// 总览 shows its two views; its JSON sources stay registered and are reachable via 「源数据」.
const overviewNumber = (path: string): string | undefined => (registry.source_numbers as Record<string, string>)[`repo:.agents/references/project/${path}`];
const OVERVIEW_PAGES: TreeNode[] = [
  { type: "file", name: sourceTitle({ title: "工作流全景", number: overviewNumber("ai_video_workflow_map.json") }), path: OVERVIEW_PATH, navigation_href: OVERVIEW_PATH },
  { type: "file", name: sourceTitle({ title: "术语表", number: overviewNumber("ai_video_glossary.json") }), path: GLOSSARY_PATH, navigation_href: GLOSSARY_PATH },
  { type: "file", name: sourceTitle({ title: "决策记录", number: (registry.source_numbers as Record<string, string>)[DECISIONS_SOURCE] }),
    path: globalSourceUrl(DECISIONS_SOURCE), navigation_href: globalSourceUrl(DECISIONS_SOURCE) },
];

function buildNavigation(catalog: GlobalCatalog | null): TreeNode {
  const groups = workflowGroups(catalog);
  const children: TreeNode[] = workflowCategories(catalog).map(category => ({
    type: "directory", name: numberedTitle(category), path: categoryUrl(category.id), navigation_href: categoryUrl(category.id),
    children: [...groups.filter(group => group.category === category.id).map((group): TreeNode => {
    const module = WORKFLOW_MODULES.find(entry => entry.id === group.id);
    const href = module ? workflowModulePath(module.id) : group.id === "overview" ? OVERVIEW_PATH : globalGroupUrl(group.id);
    // 总览 is a pure grouping row: its pages own the URLs, so the row itself must not share one (duplicate key / double highlight).
    if (group.id === "overview") return { type: "directory", name: numberedTitle(group), path: globalGroupUrl(group.id), children: OVERVIEW_PAGES };
    return { type: "directory", name: numberedTitle(group), path: href, navigation_href: href,
      children: [...(group.id === "filming" && !catalog ? [{
        type: "file" as const, name: sourceTitle({ title: "镜头（shot）", number: (registry.source_numbers as Record<string, string>)[FILMING_SHOTS_SOURCE] }),
        path: FILMING_KNOWLEDGE_PATH, navigation_href: FILMING_KNOWLEDGE_PATH,
      }] : []), ...(group.id === "overview" ? OVERVIEW_PAGES : sourceNodes((catalog?.sources || []).filter(source => source.group === group.id)))],
    };
  })],
  }));
  return { type: "directory", name: "工作流", path: WORKFLOW_PATH, navigation_href: WORKFLOW_PATH, children };
}

export const WORKFLOW_NAV_TREE: TreeNode = buildNavigation(null);
