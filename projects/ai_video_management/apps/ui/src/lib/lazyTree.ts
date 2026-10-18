/**
 * Lazy sidebar tree (follow-up 280).
 *
 * `/api/tree?lazy=1` returns the navigation skeleton plus the first folder
 * levels; deeper folders are `lazy` stubs. Each opened folder's contents come
 * from `/api/tree/subtree` and are kept in a cache keyed by folder path; the tree
 * the app renders is always `applyLoaded(base, cache)`, so refetching the base or
 * one folder never loses what else was opened.
 */
import type { TreeNode } from "../types";

export interface LoadedDir {
  children: TreeNode[];
  /** Folder levels the fetch expanded (0 = everything below). */
  depth: number;
}

export type LoadedDirs = ReadonlyMap<string, LoadedDir>;

const isUnder = (path: string, dir: string): boolean => path.startsWith(`${dir}/`);

/** Fill every lazy stub whose folder has been loaded with that folder's
 * contents. A real folder can appear in more than one place (a shot folder sits
 * under both 影视改编 and Prompt 编译), so every occurrence is filled. A folder
 * the first load already listed is left as the server built it — a drama root's
 * children are navigation, not its raw listing — unless it was loaded in full
 * (`depth` 0, the recycle bin). Filling is recursive, so a stub inside a filled
 * folder takes its own load. */
export function applyLoaded(base: TreeNode, loaded: LoadedDirs): TreeNode {
  if (loaded.size === 0) return base;
  const fill = (node: TreeNode): TreeNode => {
    const entry = node.type === "directory" ? loaded.get(node.path) : undefined;
    const hit = entry && (node.lazy || entry.depth === 0) ? entry : undefined;
    const children = hit ? hit.children : node.children;
    if (!children) return node;
    const next = children.map(fill);
    if (!hit && next.every((child, i) => child === children[i])) return node;
    const out: TreeNode = { ...node, children: next };
    if (hit) delete out.lazy;
    return out;
  };
  return fill(base);
}

/** Lazy folders in `tree` that lie on the way to `path` (outermost first). */
export function lazyAncestors(tree: TreeNode | null, path: string): string[] {
  if (!tree) return [];
  const found = new Set<string>();
  const walk = (node: TreeNode): void => {
    if (node.lazy && node.path && isUnder(path, node.path)) found.add(node.path);
    for (const child of node.children ?? []) walk(child);
  };
  walk(tree);
  return [...found].sort((a, b) => a.length - b.length);
}

/** Every still-lazy folder path (links into them cannot be checked yet). */
export function lazyDirs(tree: TreeNode | null): string[] {
  const out: string[] = [];
  const walk = (node: TreeNode): void => {
    if (node.lazy && node.path) out.push(node.path);
    for (const child of node.children ?? []) walk(child);
  };
  if (tree) walk(tree);
  return [...new Set(out)];
}

/** What a batch of changed files makes stale: the base tree when a change lands
 * outside every lazy stub of it (navigation, decision records, new takes in a
 * listed folder…), and each loaded folder that contains a changed path. */
export function staleAfter(base: TreeNode | null, loaded: LoadedDirs, changed: readonly string[]):
  { base: boolean; dirs: string[] } {
  const stubs = lazyDirs(base);
  const baseStale = changed.some(p => p === "*" || !stubs.some(dir => isUnder(p, dir)));
  const dirs = [...loaded.keys()].filter(dir => changed.some(p => p === "*" || isUnder(p, dir)));
  return { base: baseStale, dirs };
}

/** `isKnown` for link checking: a path is known when the loaded tree lists it,
 * or when it lies inside a folder that has not been loaded yet. */
export function knownPredicate(knownPaths: readonly string[], unloaded: readonly string[]): (path: string) => boolean {
  const known = new Set(knownPaths);
  return (path: string) => known.has(path) || unloaded.some(dir => isUnder(path, dir));
}
