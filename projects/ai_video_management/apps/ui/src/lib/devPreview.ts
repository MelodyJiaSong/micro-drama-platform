/** 西幻新剧开发框架的预览与评审页（xihuan follow-up 001）。后端在系列节点下挂「新剧开发框架」，
 * 链接到 DEV_PREVIEW_ROUTE?path=<框架目录 | 某个开发稿目录>。页名与 ai_videos/xihuan/framework/check.py 一致（v0.4：五页核心 + 其他）。 */
export const DEV_PREVIEW_ROUTE = "/dev-preview";

export const DEV_PAGES = [
  { id: "01_主题", label: "主题", optional: false },
  { id: "02_世界", label: "世界", optional: false },
  { id: "03_力量", label: "力量", optional: false },
  { id: "04_人物", label: "人物", optional: false },
  { id: "05_矛盾", label: "矛盾", optional: false },
  { id: "06_秘密与伏笔", label: "其他 · 秘密与伏笔", optional: true },
  { id: "07_观众与爽点", label: "其他 · 观众与爽点", optional: true },
] as const;
export type DevPageId = typeof DEV_PAGES[number]["id"];

export const CHECK_FILE = "_check.json";
export const FEEDBACK_FILE = "_反馈.md";
export const REVIEW_FILE = "_评估.md";

export interface LimitStat { chars?: number; words?: number; limit: number }
export interface PageStat { exists: boolean; required: boolean; missing_sections?: string[]; limits?: Record<string, LimitStat> }
export interface CheckReport { generated: string; ok: boolean; errors: string[]; warnings?: string[]; pages: Record<string, PageStat> }

export const join = (dir: string, name: string): string => `${dir.replace(/\/+$/, "")}/${name}`;
export const isFrameworkRoot = (path: string): boolean => /(^|\/)framework\/?$/.test(path);
export const devPreviewHref = (path: string, extra: Record<string, string> = {}): string =>
  `${DEV_PREVIEW_ROUTE}?${new URLSearchParams({ path, ...extra }).toString()}`;

/** `## 标题` 小节 → 正文，与 check.py 的 sections() 同一规则。 */
export function parseSections(text: string): Record<string, string> {
  const out: Record<string, string> = {};
  const parts = text.split(/^## (.+?)\s*$/m);
  for (let i = 1; i < parts.length - 1; i += 2) out[parts[i].trim()] = parts[i + 1].trim();
  return out;
}

export function pageTitle(text: string, fallback: string): string {
  const h1 = /^# (.+)$/m.exec(text)?.[1]?.trim();
  return h1 ? h1.split(/[·・]/).pop()!.trim() || h1 : fallback;
}

export function limitOver(stat: LimitStat): boolean {
  return (stat.chars ?? stat.words ?? 0) > stat.limit;
}
