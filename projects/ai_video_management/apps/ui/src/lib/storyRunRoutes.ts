export const STORY_RUN_PAGES = {
  output: { path: "/story-runs/story", title: "候选故事", category: "产出" },
  state: { path: "/story-runs/state", title: "候选状态变化", category: "产出" },
  input: { path: "/story-runs/input", title: "输入快照", category: "输入" },
  item: { path: "/story-runs/item", title: "运行关联文档", category: "运行资料" },
  process: { path: "/story-runs/process", title: "创作过程", category: "过程" },
  compare: { path: "/story-runs/compare", title: "候选对比", category: "对比" },
} as const;
export type StoryRunDocument = keyof typeof STORY_RUN_PAGES;
export function storyRunUrl(document: StoryRunDocument, episode: string, run?: string, compare?: string, item?: string): string {
  const params = new URLSearchParams({ episode_path: episode });
  if (run) params.set("run_id", run);
  if (compare) params.set("compare_run_id", compare);
  if (item) params.set("item_id", item);
  return `${STORY_RUN_PAGES[document].path}?${params}`;
}
export function storyRunDocument(pathname: string): StoryRunDocument | undefined {
  return (Object.keys(STORY_RUN_PAGES) as StoryRunDocument[]).find(key => STORY_RUN_PAGES[key].path === pathname);
}
