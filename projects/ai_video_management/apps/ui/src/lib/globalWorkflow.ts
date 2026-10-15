export const GLOBAL_SOURCE_PATH = "/workflow/source";
export const GLOBAL_COVERAGE_PATH = "/workflow/settings/coverage";
export const globalSourceUrl = (sourceId: string): string => `${GLOBAL_SOURCE_PATH}?${new URLSearchParams({ source_id: sourceId })}`;
export const globalGroupUrl = (group: string): string => `/workflow/settings/${encodeURIComponent(group)}`;

export interface GlobalSource {
  id: string; path: string; title: string; group: string; scope: "repo" | "user";
  view: string; status: "available" | "missing" | "unavailable"; historical: boolean;
  number?: string; parent?: string;
  /** Formats this source applies to; empty = shared by every format. */
  formats?: string[];
  /** Shared sources this format page adapts, with the heading in this page. */
  adapts?: { source_id: string; section: string }[];
}
export interface GlobalFormat { id: string; title: string; description?: string; }
export interface GlobalGroup { id: string; title: string; description: string; number?: string; category?: string; }
export interface GlobalCategory { id: string; title: string; description: string; number: string; }
export interface GlobalSourceDetail extends GlobalSource {
  content: string; format: "markdown" | "json" | "code" | "text"; sha256: string | null; redacted?: boolean;
}
export interface GlobalCatalog {
  groups: GlobalGroup[]; sources: GlobalSource[]; categories?: GlobalCategory[]; formats?: GlobalFormat[];
}
export interface GlobalCoverage {
  inventory?: {
    total: number; available: number; historical: number; numbered: number;
    issues: { source_id: string; path: string; kind: string; note: string }[];
    references: { source_id: string; path: string; historical: boolean }[];
  };
}
export const GLOBAL_STATUS = { available: "可查看", missing: "未配置 / 不存在", unavailable: "无法安全读取" };
export const numberedTitle = (entry: { title: string; number?: string }): string => entry.number ? `${entry.number}_${entry.title}` : entry.title;
export const sourceTitle = (entry: Pick<GlobalSource, "title" | "number">): string => entry.number ? numberedTitle(entry) : `待编号_${entry.title}`;

export const formatLabels = (catalog: GlobalCatalog | null, source: Pick<GlobalSource, "formats">): string[] =>
  (source.formats || []).map(id => catalog?.formats?.find(entry => entry.id === id)?.title || id);
/** Format pages that adapt `sourceId`, with the section in each page. */
export const sourceAdaptations = (catalog: GlobalCatalog | null, sourceId: string): { source: GlobalSource; section: string }[] =>
  (catalog?.sources || [])
    .flatMap(source => (source.adapts || []).filter(entry => entry.source_id === sourceId).map(entry => ({ source, section: entry.section })));

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
