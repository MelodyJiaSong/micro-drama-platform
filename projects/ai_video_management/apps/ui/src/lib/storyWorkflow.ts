import registry from "../../../../../../.agents/references/project/workflow_catalog.json";
import { globalSourceUrl, sourceTitle, storySectionUrl, storyTopicUrl, type GlobalCatalog } from "./globalWorkflow";
import type { TreeNode } from "../types";

export const STORY_SECTIONS = registry.story_navigation;
export type StorySection = typeof STORY_SECTIONS[number];
export type StoryTopic = StorySection["topics"][number];
export { storySectionUrl, storyTopicUrl } from "./globalWorkflow";

export function findStoryTopic(sourceId: string, topicId: string): { section: StorySection; topic: StoryTopic } | undefined {
  const section = STORY_SECTIONS.find(entry => entry.source_id === sourceId);
  const topic = section?.topics.find(entry => entry.id === topicId);
  return section && topic ? { section, topic } : undefined;
}

export function storyTopicContent(content: string, title: string): string | null {
  const lines = content.split(/\r?\n/);
  let start = -1;
  let fence = "";
  for (let index = 0; index < lines.length; index++) {
    const marker = lines[index].match(/^\s*(`{3,}|~{3,})/);
    if (marker) { fence = fence ? "" : marker[1][0]; continue; }
    if (fence || !lines[index].startsWith("## ")) continue;
    if (start >= 0) return lines.slice(start + 1, index).join("\n").trim();
    if (lines[index] === `## ${title}`) start = index;
  }
  return start < 0 ? null : lines.slice(start + 1).join("\n").trim();
}

export function storyNavigation(catalog: GlobalCatalog | null): TreeNode[] {
  return STORY_SECTIONS.map(section => ({
    type: "directory", name: section.title, path: storySectionUrl(section.id), navigation_href: storySectionUrl(section.id),
    children: [
      ...section.topics.map(topic => ({ type: "file" as const, name: topic.title, path: storyTopicUrl(section, topic), navigation_href: storyTopicUrl(section, topic) })),
      ...(section.id === "execution" ? (catalog?.sources || []).filter(source => source.group === "story").map(source => ({
        type: "file" as const, name: sourceTitle(source), path: `/workflow/source/${encodeURIComponent(source.id)}`, navigation_href: globalSourceUrl(source.id),
      })) : []),
    ],
  }));
}
