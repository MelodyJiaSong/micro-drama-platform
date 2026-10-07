export const GLOBAL_SOURCE_PATH = "/workflow/source";
export const GLOBAL_COVERAGE_PATH = "/workflow/settings/coverage";
export const globalSourceUrl = (sourceId: string): string => `${GLOBAL_SOURCE_PATH}?${new URLSearchParams({ source_id: sourceId })}`;
export const globalGroupUrl = (group: string): string => `/workflow/settings/${encodeURIComponent(group)}`;
export const storySectionUrl = (id: string): string => `/workflow/story/${id}`;
export const storyTopicUrl = (section: { source_id: string }, topic: { id: string }): string => `${globalSourceUrl(section.source_id)}&${new URLSearchParams({ section: topic.id })}`;

export interface GlobalSource {
  id: string; path: string; title: string; group: string; scope: "repo" | "user";
  view: string; status: "available" | "missing" | "unavailable"; historical: boolean;
  number?: string;
}
export interface GlobalGroup { id: string; title: string; description: string; number?: string; category?: string; }
export interface GlobalCategory { id: string; title: string; description: string; number: string; }
export interface GlobalSourceDetail extends GlobalSource {
  content: string; format: "markdown" | "json" | "code" | "text"; sha256: string | null; redacted?: boolean;
}
export interface GlobalCatalog {
  groups: GlobalGroup[]; sources: GlobalSource[]; categories?: GlobalCategory[];
}
export interface GlobalCoverage {
  inventory?: {
    total: number; available: number; historical: number; numbered: number;
    issues: { source_id: string; path: string; kind: string; note: string }[];
    references: { source_id: string; path: string; historical: boolean }[];
  };
  links: { episode_path: string; run_id: string; item_id: string; source_id: string; source_path: string; source_hash: string | null; status: string; source_number?: string; source_title?: string }[];
  gaps: { episode_path: string; status: string; note: string }[]; note: string;
}
export const GLOBAL_STATUS = { available: "可查看", missing: "未配置 / 不存在", unavailable: "无法安全读取" };
export const numberedTitle = (entry: { title: string; number?: string }): string => entry.number ? `${entry.number}_${entry.title}` : entry.title;
export const sourceTitle = (entry: Pick<GlobalSource, "title" | "number">): string => entry.number ? numberedTitle(entry) : `待编号_${entry.title}`;

export async function loadGlobal<T>(path: string, signal: AbortSignal): Promise<T> {
  const response = await fetch(path, { signal, cache: "no-store" });
  if (!response.ok) throw new Error(`全局工作流加载失败（HTTP ${response.status}）`);
  return response.json() as Promise<T>;
}

export function matchesNavigation(href: string | undefined, pathname: string, search: string): boolean {
  if (!href) return false;
  const target = new URL(href, "http://workflow.local");
  if (target.pathname !== pathname) return false;
  const params = new URLSearchParams(search);
  if (target.pathname === GLOBAL_SOURCE_PATH && params.get("section") !== target.searchParams.get("section")) return false;
  if (target.pathname === "/drama" && ["scene", "shot"].some(key => params.get(key) !== target.searchParams.get(key))) return false;
  return [...target.searchParams].every(([key, value]) => params.get(key) === value);
}
