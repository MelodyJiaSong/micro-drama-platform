import type { TreeNode } from "../types";

export interface DramaChoice {
  path: string;
  name: string;
  characters: string[];
}

/** Every drama root in the tree — flat ones and series members alike. Walks by
 *  the backend's `is_drama` flag, never by path depth (a series member is three
 *  segments deep). */
export function collectDramaNodes(tree: TreeNode | null): TreeNode[] {
  if (!tree) return [];
  const out: TreeNode[] = [];
  const queue: TreeNode[] = [tree];
  while (queue.length > 0) {
    const node = queue.shift()!;
    if (node.is_drama === true && node.path?.startsWith("ai_videos/")) {
      out.push(node);
      continue; // a drama never nests another drama
    }
    for (const c of node.children ?? []) queue.push(c);
  }
  return out;
}

/** The drama root path that owns `filePath` (`ai_videos/hy1` or
 *  `ai_videos/huangye_shenghuo/hy2`), or null when it belongs to none. */
export function dramaRootOf(tree: TreeNode | null, filePath: string | null): string | null {
  if (!filePath) return null;
  let best: string | null = null;
  for (const drama of collectDramaNodes(tree)) {
    const root = drama.path;
    if (filePath === root || filePath.startsWith(root + "/")) {
      if (best === null || root.length > best.length) best = root;
    }
  }
  return best;
}

export function extractDramas(tree: TreeNode | null): DramaChoice[] {
  if (!tree) return [];
  const out: DramaChoice[] = [];
  for (const drama of collectDramaNodes(tree)) {
    if (drama.name.startsWith("_")) continue;
    const characters: string[] = [];
    const chDir = findAssetDir(drama, "characters");
    if (chDir) {
      for (const c of chDir.children ?? []) {
        if (c.type === "directory" && /^c\d+(_.*)?$/.test(c.name)) {
          characters.push(c.name);
        }
      }
    }
    out.push({ path: drama.path, name: drama.name, characters });
  }
  return out;
}

export interface DramaAssets {
  /** Character display names (folder name with the `cN_` prefix stripped). */
  characters: string[];
  /** Scene display names (folder name with the `sN_` prefix stripped). */
  scenes: string[];
}

const _CHAR_DIR_RE = /^c\d+(?:_(.*))?$/;
const _SCENE_DIR_RE = /^s\d+(?:_(.*))?$/;

function _stripPrefix(folder: string, re: RegExp): string {
  const m = re.exec(folder);
  return m && m[1] ? m[1] : folder;
}

function _findDramaNode(tree: TreeNode | null, filePath: string): TreeNode | null {
  const dramaPath = dramaRootOf(tree, filePath);
  if (dramaPath === null) return null;
  return collectDramaNodes(tree).find((d) => d.path === dramaPath) ?? null;
}

/** List the characters + scenes (display names) of the drama that `filePath`
 *  belongs to. Returns empty arrays when the drama or its asset folders are
 *  absent. Display names are written verbatim into prompt `人物:` / `场景:`
 *  lines, so the `cN_` / `sN_` folder prefix is stripped. */
export function extractDramaAssets(tree: TreeNode | null, filePath: string | null): DramaAssets {
  if (!tree || !filePath) return { characters: [], scenes: [] };
  const drama = _findDramaNode(tree, filePath);
  if (!drama) return { characters: [], scenes: [] };
  const characters: string[] = [];
  const scenes: string[] = [];
  const chDir = findAssetDir(drama, "characters");
  if (chDir) {
    for (const c of chDir.children ?? []) {
      if (c.type === "directory" && _CHAR_DIR_RE.test(c.name)) {
        characters.push(_stripPrefix(c.name, _CHAR_DIR_RE));
      }
    }
  }
  const scDir = findAssetDir(drama, "scenes");
  if (scDir) {
    for (const s of scDir.children ?? []) {
      if (s.type === "directory" && _SCENE_DIR_RE.test(s.name)) {
        scenes.push(_stripPrefix(s.name, _SCENE_DIR_RE));
      }
    }
  }
  return { characters, scenes };
}

export function findChild(node: TreeNode, name: string): TreeNode | null {
  for (const c of node.children ?? []) {
    if (c.name === name) return c;
  }
  return null;
}

/** Find a drama asset folder (`characters` / `scenes`) that may sit at the
 *  drama root (legacy) or under the staged-pipeline stage folder
 *  `2_世界观人设/`. */
export function findAssetDir(drama: TreeNode, name: string): TreeNode | null {
  const direct = findChild(drama, name);
  if (direct) return direct;
  const world = findChild(drama, "2_世界观人设");
  return world ? findChild(world, name) : null;
}
