import type { TreeNode } from "../types";

/** One page per hero (follow-up 312): portrait, intro video, views, each skill's
 *  latest render plus history, and the demo cuts — so a review needs one link. */
export const HERO_PREVIEW_ROUTE = "/hero-preview";

export interface PreviewItem { name: string; path: string; kind: "image" | "video" | "audio" | "file" }
export interface RenderGroup { name: string; items: PreviewItem[]; review: string | null }
export interface SkillPreview {
  name: string; path: string; card: string | null;
  latest: RenderGroup | null; history: RenderGroup[];
  images: PreviewItem[]; planning: PreviewItem[];
}
export interface HeroPreview {
  name: string; path: string; card: string | null; portrait: PreviewItem | null;
  intro: PreviewItem[]; views: PreviewItem[]; otherImages: PreviewItem[];
  skills: SkillPreview[]; demo: PreviewItem[]; demoNotes: PreviewItem[];
}

/** Folders that hold research, backups or prompt packs, not reviewable output. */
const SKIP_DIRS = new Set(["ref", "source", "icon", "资料包", ".pending"]);
const skipDir = (name: string): boolean => SKIP_DIRS.has(name) || name.startsWith("_") || name.startsWith(".");

export function heroPreviewHref(path: string): string {
  return `${HERO_PREVIEW_ROUTE}?${new URLSearchParams({ path })}`;
}

function kindOf(node: TreeNode): PreviewItem["kind"] | null {
  if (node.type === "image" || node.type === "video" || node.type === "audio") return node.type;
  return node.type === "file" ? "file" : null;
}
const item = (node: TreeNode): PreviewItem => ({ name: node.name, path: node.path, kind: kindOf(node) ?? "file" });
const dirs = (node: TreeNode | undefined): TreeNode[] => (node?.children ?? []).filter(c => c.children !== undefined || c.type === "directory");
const child = (node: TreeNode | undefined, name: string): TreeNode | undefined => node?.children?.find(c => c.name === name);
const media = (node: TreeNode | undefined, kinds: PreviewItem["kind"][] = ["image", "video", "audio"]): PreviewItem[] =>
  (node?.children ?? []).filter(c => { const k = kindOf(c); return k !== null && kinds.includes(k); }).map(item);
const byName = (a: { name: string }, b: { name: string }): number => a.name.localeCompare(b.name, "zh");

/** Every media file below `node`, skipping backup folders; newest path first. */
function deepMedia(node: TreeNode | undefined, kinds: PreviewItem["kind"][]): PreviewItem[] {
  if (!node) return [];
  const out = media(node, kinds);
  for (const d of dirs(node)) if (!skipDir(d.name)) out.push(...deepMedia(d, kinds));
  return out.sort((a, b) => b.path.localeCompare(a.path));
}

/** Demo cuts, finished product first: `edit/final` before `edit/draft` before anything else
 *  (review packs, previews), and within a folder the highest `_vN` first. Path order alone put
 *  `demo/review_*` packs ahead of `demo/edit/final/` (follow-up 314). */
function demoCuts(node: TreeNode | undefined): PreviewItem[] {
  const rank = (p: string): number => (p.includes("/edit/final/") ? 0 : p.includes("/edit/draft/") ? 1 : 2);
  const version = (name: string): number => Number(/_v(\d+)\.[^.]+$/.exec(name)?.[1] ?? -1);
  return deepMedia(node, ["video"]).sort((a, b) =>
    rank(a.path) - rank(b.path) || version(b.name) - version(a.name) || b.path.localeCompare(a.path));
}

function skillPreview(node: TreeNode): SkillPreview {
  // Render folders are named `YYYYMMDD-HHMMSS_<task>`, so name order is time order.
  const renders = dirs(child(node, "renders")).filter(d => !skipDir(d.name))
    .map(d => ({ name: d.name, items: media(d).sort((a, b) => (a.kind === "video" ? -1 : 0) - (b.kind === "video" ? -1 : 0)),
      review: d.children?.find(c => c.type === "file" && c.name === "review.md")?.path ?? null }))
    .filter(g => g.items.length > 0)
    .sort((a, b) => b.name.localeCompare(a.name));
  const card = node.children?.find(c => c.type === "file" && c.name === `${node.name}.md`);
  return {
    name: node.name, path: node.path, card: card?.path ?? null,
    latest: renders[0] ?? null, history: renders.slice(1),
    // The current peak (`<skill>_peak.png`) leads; dated variants follow.
    images: media(node, ["image", "video"]).sort((a, b) => Number(b.name === `${node.name}_peak.png`) - Number(a.name === `${node.name}_peak.png`) || byName(a, b)),
    planning: media(child(node, "planning"), ["image", "video"]).sort((a, b) => b.name.localeCompare(a.name)),
  };
}

export function buildHeroPreview(root: TreeNode): HeroPreview {
  const rootMedia = media(root);
  const portrait = rootMedia.find(m => m.kind === "image" && m.name === `${root.name}.png`) ?? null;
  const card = root.children?.find(c => c.type === "file" && c.name === `${root.name}.md`);
  const skills = dirs(child(root, "skills")).filter(d => !skipDir(d.name)).map(skillPreview).sort(byName);
  const demoDir = child(root, "demo");
  return {
    name: root.name, path: root.path, card: card?.path ?? null, portrait,
    intro: [...rootMedia.filter(m => m.kind === "video" || m.kind === "audio"), ...media(child(root, "views"), ["audio"])],
    views: media(child(root, "views"), ["image"]).sort(byName),
    otherImages: rootMedia.filter(m => m.kind === "image" && m !== portrait).sort(byName),
    skills,
    demo: demoCuts(demoDir),
    demoNotes: (demoDir?.children ?? []).filter(c => c.type === "file" && c.name.endsWith(".md")).map(item),
  };
}
