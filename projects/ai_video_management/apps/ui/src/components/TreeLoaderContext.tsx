/**
 * Lazy tree loading (follow-up 280). The app shell owns the tree; pages that
 * need a folder the first load left as a `lazy` stub (the character gallery,
 * the recycle bin) ask for it through this context instead of the whole tree
 * being shipped up front.
 */
import { createContext, useContext } from "react";
import type { TreeNode } from "../types";

export interface TreeLoader {
  /** Load one folder `depth` levels deep (0 = everything below it). */
  ensureLoaded: (path: string, depth?: number) => void;
  /** Load every still-lazy child folder of `node`, one level each. */
  ensureChildrenLoaded: (node: TreeNode | null | undefined) => void;
}

const noop: TreeLoader = { ensureLoaded: () => undefined, ensureChildrenLoaded: () => undefined };

export const TreeLoaderContext = createContext<TreeLoader>(noop);

export function useTreeLoader(): TreeLoader {
  return useContext(TreeLoaderContext);
}
