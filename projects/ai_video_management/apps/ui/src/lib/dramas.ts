import type { TreeNode } from "../types";
import { CHARACTER_DIR_RE } from "./characterDir";

export interface DramaChoice {
  path: string;
  name: string;
  characters: string[];
  /** The drama (or its series) is marked obsolete with an `OBSOLETE.md`. */
  obsolete: boolean;
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

export function extractDramas(tree: TreeNode | null): DramaChoice[] {
  if (!tree) return [];
  const out: DramaChoice[] = [];
  for (const drama of collectDramaNodes(tree)) {
    if (drama.name.startsWith("_")) continue;
    const characters: string[] = [];
    const chDir = findAssetDir(drama, "characters");
    if (chDir) {
      for (const c of chDir.children ?? []) {
        if (c.type === "directory" && CHARACTER_DIR_RE.test(c.name)) {
          characters.push(c.name);
        }
      }
    }
    out.push({ path: drama.path, name: drama.name, characters, obsolete: drama.obsolete === true });
  }
  return out;
}

export function findChild(node: TreeNode, name: string): TreeNode | null {
  for (const c of node.children ?? []) {
    if (c.name === name) return c;
  }
  return null;
}

/** Find a drama asset folder (`characters` / `background`) that may sit at the
 *  drama root (older dramas) or under `2_世界观人设/`. */
export function findAssetDir(drama: TreeNode, name: string): TreeNode | null {
  const direct = findChild(drama, name);
  if (direct) return direct;
  const world = findChild(drama, "2_世界观人设");
  return world ? findChild(world, name) : null;
}
