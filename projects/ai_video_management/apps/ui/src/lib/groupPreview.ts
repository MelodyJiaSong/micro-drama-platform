import type { TreeNode } from "../types";
import type { PreviewItem } from "./heroPreview";

/** One page per 镜组 (follow-up 331): the board, every take, each member shot's filming fields and overhead, the
 *  compiled prompt and its references — so reviewing a group needs one link. */
export const GROUP_PREVIEW_ROUTE = "/group-preview";

/** `…/episodes/ep01/scenes/s1/groups/g2` */
const GROUP_PATH_RE = /^(.*\/episodes\/(ep\d+))\/scenes\/(s\d+)\/groups\/(g\d+)$/;

export interface GroupLocation { episodePath: string; episode: string; scene: string; group: string; key: string }

export function groupPreviewHref(path: string): string {
  return `${GROUP_PREVIEW_ROUTE}?${new URLSearchParams({ path })}`;
}

export function parseGroupPath(path: string): GroupLocation | null {
  const m = GROUP_PATH_RE.exec(path.replace(/\/+$/, ""));
  if (!m) return null;
  const [, episodePath, episode, scene, group] = m;
  return { episodePath, episode, scene, group, key: `ep${Number(episode.slice(2))}_${scene}_${group}` };
}

export interface GroupTake {
  name: string; stage: "draft" | "final";
  video: PreviewItem | null; review: string | null; prompt: string | null; generation: string | null;
}
export interface GroupFiles {
  board: PreviewItem | null; otherImages: PreviewItem[]; takes: GroupTake[];
  packPrompt: string | null; packManifest: string | null; packInvalid: string | null;
}

const kindOf = (node: TreeNode): PreviewItem["kind"] =>
  node.type === "image" || node.type === "video" || node.type === "audio" ? node.type : "file";
const item = (node: TreeNode): PreviewItem => ({ name: node.name, path: node.path, kind: kindOf(node) });
const child = (node: TreeNode | undefined, name: string): TreeNode | undefined => node?.children?.find(c => c.name === name);
const isDir = (node: TreeNode): boolean => node.children !== undefined || node.type === "directory";

function takes(node: TreeNode | undefined, stage: GroupTake["stage"]): GroupTake[] {
  // Take folders are `YYYYMMDD-HHMMSS_<submit id>`, so name order is time order; `.pending` holds unfinished submits.
  return (node?.children ?? []).filter(d => isDir(d) && !d.name.startsWith(".")).map(d => {
    const file = (name: string): string | null => child(d, name)?.path ?? null;
    const video = (d.children ?? []).find(c => c.type === "video");
    return { name: d.name, stage, video: video ? item(video) : null,
      review: file("review.md"), prompt: file("prompt.txt"), generation: file("generation.json") };
  });
}

export function groupFiles(root: TreeNode): GroupFiles {
  const images = (root.children ?? []).filter(c => c.type === "image").map(item);
  const pack = child(root, "资料包");
  return {
    board: images.find(i => i.name === "board.png") ?? null,
    otherImages: images.filter(i => i.name !== "board.png").sort((a, b) => b.name.localeCompare(a.name)),
    takes: [...takes(child(root, "renders"), "final"), ...takes(child(root, "drafts"), "draft")]
      .sort((a, b) => b.name.localeCompare(a.name)),
    packPrompt: child(pack, "prompt.txt")?.path ?? null,
    packManifest: child(pack, "manifest.json")?.path ?? null,
    packInvalid: child(pack, "_失效.md")?.path ?? null,
  };
}

export interface FilmingShot {
  id: string; duration: number; action: string; blocking: string; beats: string; camera: string; lighting: string;
  dialogue: string; cast: string[]; props?: string[];
}
export interface FilmingScene { id: string; location: string; time: string; purpose: string; background: string;
  shots: FilmingShot[]; groups?: { id: string; shots: string[] }[] }
export interface CompiledRef { key: string; kind: "image" | "video" | "audio"; role: string; path: string }
export interface CompiledGroup { id: string; shots: string[]; text: string; refs: CompiledRef[] }

export interface GroupMember { shot: FilmingShot; start: number; end: number; overhead: string }
export interface GroupSpec {
  scene: FilmingScene | null; members: GroupMember[]; total: number;
  compiled: CompiledGroup | null; problem: string | null;
}

/** The group as written in filming.json (members with their time range) and as compiled in prompts.json. */
export function groupSpec(loc: GroupLocation, filming: { scenes: FilmingScene[] } | null,
  prompts: { scenes: { id: string; groups?: CompiledGroup[] }[] } | null): GroupSpec {
  const scene = filming?.scenes.find(s => s.id === loc.scene) ?? null;
  const group = scene?.groups?.find(g => g.id === loc.group);
  const compiled = prompts?.scenes.find(s => s.id === loc.scene)?.groups?.find(g => g.id === loc.key) ?? null;
  if (!scene || !group) {
    return { scene, members: [], total: 0, compiled, problem: `filming.json 的 ${loc.scene} 里没有镜组 ${loc.group}` };
  }
  let start = 0;
  const members = group.shots.flatMap(id => {
    const shot = scene.shots.find(s => s.id === id);
    if (!shot) return [];
    const m = { shot, start, end: start + shot.duration,
      overhead: `${loc.episodePath}/scenes/${loc.scene}/shots/${id}/planning/${id}_overhead.png` };
    start = m.end;
    return [m];
  });
  const fullKeys = group.shots.map(id => `ep${Number(loc.episode.slice(2))}_${loc.scene}_${id}`);
  const problem = !compiled ? "还没编译：分镜确定后在「Prompt 编译与出片」编译"
    : compiled.shots.join() !== fullKeys.join() ? "编译结果的镜头和分镜不一致：重新编译" : null;
  return { scene, members, total: start, compiled, problem };
}

/** `状态：…` line of a take's review.md; empty when absent. */
export function reviewStatus(text: string): string {
  return text.split(/\r?\n/).find(l => l.startsWith("状态："))?.slice(3).trim() ?? "";
}
