import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import type { TreeNode, TreeNodeType } from "../types";
import { ResearchNav } from "./ResearchNav";
import { workflowNavigation } from "../lib/workflowData";
import { matchesNavigation } from "../lib/globalWorkflow";
import { useGlobalWorkflow } from "./GlobalWorkflowContext";
import { ObsoleteBadge } from "./ObsoleteBadge";

/** Node types that open a file in the reader when clicked. One source — adding
 * a leaf type (e.g. `model` for .glb) must not mean editing five predicates. */
const FILE_LEAF_TYPES: ReadonlySet<TreeNodeType> = new Set<TreeNodeType>([
  "file", "image", "video", "audio", "pdf", "model",
]);
/** Plus the episode-workflow leaves, which open a module page and never expand. */
const LEAF_TYPES: ReadonlySet<TreeNodeType> = new Set<TreeNodeType>([
  ...FILE_LEAF_TYPES, "workflow",
]);
const isFileLeaf = (type: TreeNodeType): boolean => FILE_LEAF_TYPES.has(type);
const isLeafType = (type: TreeNodeType): boolean => LEAF_TYPES.has(type);
const workflowUrl = (node: TreeNode): string => `/drama?drama=${encodeURIComponent(node.drama_path!)}&module=${node.workflow_module}&episode=${node.workflow_episode}`;

export interface SidebarProps {
  tree: TreeNode | null;
  currentPath: string;
  onSelect: (path: string) => void;
  loadError?: string | null;
  /** Collapsed to a thin rail; tree state stays mounted so expansion survives. */
  collapsed?: boolean;
  onToggleCollapsed?: () => void;
  /** Load a `lazy` folder's contents once it is opened (follow-up 280). */
  onExpandLazy?: (path: string) => void;
}

interface FlatNode { node: TreeNode; depth: number; parentPath: string | null; }

export function Sidebar({ tree, currentPath, onSelect, loadError, collapsed = false, onToggleCollapsed, onExpandLazy }: SidebarProps): JSX.Element {
  const navigate = useNavigate();
  const location = useLocation();
  const { catalog, error: globalError } = useGlobalWorkflow();
  const workflowTree = useMemo(() => workflowNavigation(catalog), [catalog]);
  const selection = new URLSearchParams(location.search);
  const treeRef = useRef<HTMLDivElement>(null);
  const [expanded, setExpanded] = useState<Record<string, boolean>>({});
  const [focusedPath, setFocusedPath] = useState<string | null>(null);

  useEffect(() => {
    const accum: Record<string, boolean> = {};
    const walk = (node: TreeNode): void => {
      if (isLeafType(node.type)) return;
      if (node.path) accum[node.path] = false;
      for (const c of node.children ?? []) walk(c);
    };
    walk(workflowTree);
    if (tree) walk(tree);
    setExpanded((prev) => ({ ...accum, ...prev }));
  }, [tree, workflowTree]);

  useEffect(() => {
    const opened: Record<string, boolean> = {};
    const walk = (node: TreeNode, ancestors: string[]): boolean => {
      if (matchesNavigation(node.navigation_href, location.pathname, location.search)) {
        for (const path of ancestors) opened[path] = true;
        if (node.children?.length) opened[node.path] = true;
        return true;
      }
      return (node.children ?? []).some(child => walk(child, [...ancestors, node.path]));
    };
    walk(workflowTree, []);
    if (tree) walk(tree, []);
    setExpanded(prev => ({ ...prev, ...opened }));
  }, [location.pathname, location.search, workflowTree, tree]);

  useEffect(() => {
    if (!currentPath) return;
    const parts = currentPath.split("/").slice(0, -1);
    const accum: Record<string, boolean> = {};
    let acc = "";
    for (const p of parts) {
      acc = acc ? `${acc}/${p}` : p;
      accum[acc] = true;
    }
    setExpanded((prev) => ({ ...prev, ...accum }));
  }, [currentPath]);

  // An opened folder that is still a lazy stub — opened by a click, a keyboard
  // toggle or the auto-expansion to the current page — gets its contents loaded.
  useEffect(() => {
    if (!tree || !onExpandLazy) return;
    const walk = (node: TreeNode): void => {
      if (node.lazy && expanded[node.path]) onExpandLazy(node.path);
      for (const child of node.children ?? []) walk(child);
    };
    walk(tree);
  }, [tree, expanded, onExpandLazy]);

  useEffect(() => {
    const handler = (event: KeyboardEvent): void => {
      if ((event.ctrlKey || event.metaKey) && event.shiftKey && (event.key === "E" || event.key === "e")) {
        event.preventDefault();
        if (collapsed) { onToggleCollapsed?.(); return; }
        const root = treeRef.current;
        if (!root) return;
        const first = root.querySelector<HTMLElement>('[role="treeitem"]');
        if (first) {
          first.focus();
          const path = first.getAttribute("data-path");
          if (path) setFocusedPath(path);
        }
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [collapsed, onToggleCollapsed]);

  const flat = useMemo<FlatNode[]>(() => {
    const out: FlatNode[] = [];
    const walk = (node: TreeNode, depth: number, parentPath: string | null): void => {
      out.push({ node, depth, parentPath });
      const isOpen = (depth === 0 && !node.navigation_href) || expanded[node.path] === true;
      if (isOpen && node.children && node.children.length) {
        for (const child of node.children) walk(child, depth + 1, node.path);
      }
    };
    walk(workflowTree, 0, null);
    if (tree?.type === "section" && (tree.path === "" || !tree.path)) {
      for (const top of tree.children ?? []) walk(top, 0, null);
    } else if (tree) {
      walk(tree, 0, null);
    }
    return out;
  }, [tree, expanded, workflowTree]);

  const toggle = useCallback((path: string) => {
    setExpanded((prev) => ({ ...prev, [path]: !prev[path] }));
  }, []);

  const onCollapseAll = useCallback(() => {
    const accum: Record<string, boolean> = {};
    const walk = (node: TreeNode): void => {
      if (isLeafType(node.type)) return;
      if (node.path) accum[node.path] = false;
      for (const c of node.children ?? []) walk(c);
    };
    walk(workflowTree);
    if (tree) walk(tree);
    setExpanded(accum);
    setFocusedPath(null);
  }, [tree, workflowTree]);

  const onItemKeyDown = (event: React.KeyboardEvent<HTMLDivElement>, item: FlatNode): void => {
    const items = flat;
    const index = items.findIndex((i) => i.node.path === item.node.path);
    const isLeaf = isFileLeaf(item.node.type) || ((item.node.children ?? []).length === 0 && !item.node.lazy);
    const isOpen = expanded[item.node.path] === true;
    if (event.key === "ArrowDown") {
      event.preventDefault();
      const next = items[index + 1];
      if (next) focusByPath(treeRef.current, next.node.path, setFocusedPath);
    } else if (event.key === "ArrowUp") {
      event.preventDefault();
      const prev = items[index - 1];
      if (prev) focusByPath(treeRef.current, prev.node.path, setFocusedPath);
    } else if (event.key === "ArrowRight") {
      event.preventDefault();
      if (!isLeaf && !isOpen) toggle(item.node.path);
    } else if (event.key === "ArrowLeft") {
      event.preventDefault();
      if (!isLeaf && isOpen) toggle(item.node.path);
      else if (item.parentPath) focusByPath(treeRef.current, item.parentPath, setFocusedPath);
    } else if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      if (item.node.navigation_href) {
        navigate(item.node.navigation_href);
        if (!isLeaf) toggle(item.node.path);
      }
      else if (item.node.type === "workflow") navigate(workflowUrl(item.node));
      else if (isFileLeaf(item.node.type)) onSelect(item.node.path);
      else toggle(item.node.path);
    }
  };

  const globalNavigation = (
      <div className="sidebar-toolbar">
        <button type="button" className="sidebar-nav-link" aria-label="查看外部服务请求日志" onClick={() => navigate("/request-logs")}>
          📋 请求日志
        </button>
        <button
          type="button"
          className="sidebar-nav-link"
          aria-label="查看选题调研"
          title="选题调研 · YouTube AIGC 系列排行 / 实测播放与点赞率 / 单人翻拍难度"
          onClick={() => navigate("/research")}
        >
          📊 调研
        </button>
        <button
          type="button"
          className="sidebar-collapse-all"
          aria-label="折叠全部"
          title="折叠全部 · Collapse all folders"
          onClick={onCollapseAll}
        >
          ⊟
        </button>
        {onToggleCollapsed ? (
          <button
            type="button"
            className="sidebar-collapse-all"
            aria-label="收起导航"
            aria-expanded={true}
            title="收起导航 · Collapse sidebar"
            onClick={onToggleCollapsed}
          >
            «
          </button>
        ) : null}
      </div>
  );

  if (collapsed) {
    return (
      <nav className="sidebar sidebar-collapsed" aria-label="File tree">
        <button
          type="button"
          className="sidebar-collapse-all"
          aria-label="展开导航"
          aria-expanded={false}
          title="展开导航 · Expand sidebar (Ctrl+Shift+E)"
          onClick={onToggleCollapsed}
        >
          »
        </button>
      </nav>
    );
  }

  return (
    <nav className="sidebar" aria-label="File tree">
      {globalNavigation}
      {globalError ? <p role="status" className="sidebar-toast sidebar-toast-err">全局目录加载失败，可在工作流页刷新。</p> : null}
      <div ref={treeRef} role="tree" aria-label="File tree" className="tree">
        {flat.map((item) => {
          const isLeaf = isLeafType(item.node.type);
          const hasChildren = (item.node.children ?? []).length > 0 || item.node.lazy === true;
          const isOpen = expanded[item.node.path] === true || (item.depth === 0 && !item.node.navigation_href);
          const isActive = matchesNavigation(item.node.navigation_href, location.pathname, location.search) || (Boolean(currentPath) && currentPath === item.node.path) || (item.node.type === "workflow" && location.pathname === "/drama"
            && selection.get("drama") === item.node.drama_path && (selection.get("module") || "story") === item.node.workflow_module
            && (selection.get("episode") || "ep01") === item.node.workflow_episode && !selection.get("scene") && !selection.get("shot"));
          const isFocused = focusedPath === item.node.path;
          const dramaPathParts = item.node.path ? item.node.path.split("/") : [];
          const isAiVideoChild = item.node.type === "directory" && dramaPathParts.length === 2 && dramaPathParts[0] === "ai_videos";
          // A drama root is 2 segments when flat and 3 inside a series — the
          // backend flags it so the sidebar never has to guess from depth.
          const isDrama = item.node.is_drama === true;
          const isDeletedRoot = isAiVideoChild && dramaPathParts[1] === "_deleted";
          const isResearchRoot = isAiVideoChild && dramaPathParts[1] === "_research";
          const treeItem = (
            <div
              // Link leaves carry their TARGET as `path`, and several blocks can
              // link one library asset — the manifest path is what is unique.
              key={item.node.link_at || item.node.path || item.node.name}
              role="treeitem"
              tabIndex={isFocused || (focusedPath === null && item === flat[0]) ? 0 : -1}
              data-path={item.node.path}
              aria-level={item.depth + 1}
              aria-expanded={isLeaf ? undefined : isOpen}
              aria-selected={isActive}
              className={["tree-item", isLeaf ? "tree-leaf" : "tree-branch", isActive ? "tree-active" : ""].filter(Boolean).join(" ")}
              style={{ paddingLeft: `${8 + item.depth * 14}px` }}
              onFocus={() => setFocusedPath(item.node.path)}
              onKeyDown={(e) => onItemKeyDown(e, item)}
              onClick={(e) => {
                e.stopPropagation();
                if (item.node.navigation_href) {
                  navigate(item.node.navigation_href);
                  if (hasChildren) toggle(item.node.path);
                  return;
                }
                if (item.node.type === "workflow") { navigate(workflowUrl(item.node)); return; }
                if (isLeaf) { onSelect(item.node.path); return; }
                // A drama node does double duty: open its main page on the right
                // AND toggle the dropdown (per follow-up — "不仅是 dropdown"). The
                // research library folder likewise opens its own main page.
                if (isDrama) navigate(`/drama?drama=${encodeURIComponent(item.node.path)}`);
                else if (isResearchRoot) navigate("/research");
                if (hasChildren) toggle(item.node.path);
              }}
            >
              {!isLeaf && hasChildren ? (
                <button type="button" className="tree-disclosure" aria-label={isOpen ? "Collapse" : "Expand"}
                  onClick={(e) => { e.stopPropagation(); toggle(item.node.path); }}>
                  {isOpen ? "▾" : "▸"}
                </button>
              ) : item.node.navigation_href ? <span className="tree-disclosure" aria-hidden="true" /> : null}
              {item.node.is_link ? (
                <span aria-hidden="true" className="tree-icon" title={item.node.link_note ?? "跨片复用的快捷链接"}>🔗</span>
              ) : null}
              {item.node.type === "image" ? <span aria-hidden="true" className="tree-icon">🖼</span> : null}
              {item.node.type === "video" ? <span aria-hidden="true" className="tree-icon">🎬</span> : null}
              {item.node.type === "audio" ? <span aria-hidden="true" className="tree-icon">🎵</span> : null}
              {item.node.type === "pdf" ? <span aria-hidden="true" className="tree-icon">📄</span> : null}
              {item.node.type === "model" ? <span aria-hidden="true" className="tree-icon" title="3D 白模 — 点开可在浏览器里转着看">🧊</span> : null}
              <span className="tree-label">{item.node.display_name || item.node.name}</span>
              {item.node.lifetime === "persistent" && ["0_research", "1_资产库"].includes(item.node.display_name || item.node.name) ? <small className="tree-lifetime-badge">Persistent</small> : null}
              {item.node.obsolete ? <ObsoleteBadge note={item.node.obsolete_note} /> : null}
              {/* Drama-level actions (📥 导入 / 🎭 角色画廊) live on the drama main
                  page (DramaPage), opened by clicking the drama node. Keeps the
                  nav uncluttered. */}
              {isDeletedRoot ? (
                <button
                  type="button"
                  className="drama-rename-btn"
                  aria-label="打开回收站清理视图"
                  title="多选 + 永久删除 _deleted/ 下的 media 文件"
                  onClick={(e) => { e.stopPropagation(); navigate("/deleted"); }}
                >
                  🧹 永久清理
                </button>
              ) : null}
            </div>
          );
          // The research categories are series inside a dataset, not files, so the
          // 调研结果 › 月份 › 分类 subtree is rendered from the research API instead.
          if (!isResearchRoot || !isOpen) return treeItem;
          return (
            <div key={item.node.path} className="research-nav-host">
              {treeItem}
              <ResearchNav depth={item.depth} />
            </div>
          );
        })}
      </div>
      {loadError ? <div role="alert" className="sidebar-error">Failed to load tree: {loadError}</div>
        : !tree ? <div className="sidebar-loading">Loading…</div> : null}
    </nav>
  );
}

function focusByPath(root: HTMLDivElement | null, path: string, setFocused: (p: string) => void): void {
  if (!root) return;
  const el = root.querySelector<HTMLElement>(`[data-path="${cssEscape(path)}"]`);
  if (el) { el.focus(); setFocused(path); }
}

function cssEscape(value: string): string {
  if (typeof CSS !== "undefined" && typeof CSS.escape === "function") return CSS.escape(value);
  return value.replace(/["\\]/g, "\\$&");
}
