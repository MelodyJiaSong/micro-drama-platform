import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Routes, Route, Navigate, useLocation, useNavigate } from "react-router-dom";
import { Sidebar } from "./components/Sidebar";
import { Reader } from "./components/Reader";
import { Home } from "./components/Home";
import { AssetOverviewPage } from "./components/AssetOverviewPage";
import { BaseLayoutPage } from "./components/BaseLayoutPage";
import { MapRegionsPage } from "./components/MapRegionsPage";
import { MAP_REGIONS_ROUTE } from "./lib/mapRegions";
import { ShopItemsPage } from "./components/ShopItemsPage";
import { SHOP_ITEMS_ROUTE } from "./lib/shopItems";
import { BASE_LAYOUT_ROUTE } from "./lib/baseLayout";
import { HeroPreviewPage } from "./components/HeroPreviewPage";
import { RankPreviewPage } from "./components/RankPreviewPage";
import { GroupPreviewPage } from "./components/GroupPreviewPage";
import { CharacterReviewPage } from "./components/CharacterReviewPage";
import { CHARACTER_REVIEW_ROUTE } from "./lib/characterReview";
import { EpisodePreviewPage } from "./components/EpisodePreviewPage";
import { StoryboardPreviewPage, STORYBOARD_PREVIEW_ROUTE } from "./components/StoryboardPreviewPage";
import { SceneBoardPage } from "./components/SceneBoardPage";
import { HERO_PREVIEW_ROUTE } from "./lib/heroPreview";
import { RANK_PREVIEW_ROUTE } from "./lib/rankPreview";
import { DEV_PREVIEW_ROUTE } from "./lib/devPreview";
import { DevPreviewPage } from "./components/DevPreviewPage";
import { GROUP_PREVIEW_ROUTE } from "./lib/groupPreview";
import { EPISODE_PREVIEW_ROUTE } from "./lib/episodePreview";
import { SCENE_PREVIEW_ROUTE } from "./lib/sceneBoard";
import { CharacterGrid } from "./components/CharacterGrid";
import { DramaPage } from "./components/DramaPage";
import { DeletedView } from "./components/DeletedView";
import { WorkflowPage } from "./components/WorkflowPage";
import { FilmingKnowledgePage } from "./components/FilmingKnowledgePage";
import { GlossaryPage } from "./components/GlossaryPage";
import { WorkflowMapPage } from "./components/WorkflowMapPage";
import { GlobalWorkflowProvider } from "./components/GlobalWorkflowContext";
import { GlobalWorkflowCategoryPage, GlobalWorkflowGroupPage, GlobalWorkflowSourcePage } from "./components/GlobalWorkflowPage";
import { GLOBAL_SOURCE_PATH } from "./lib/globalWorkflow";
import { FILMING_KNOWLEDGE_PATH, GLOSSARY_PATH, OVERVIEW_PATH, WORKFLOW_PATH } from "./lib/workflowData";
import { ResearchPage } from "./components/ResearchPage";
import { RequestLogsPage } from "./components/RequestLogsPage";
import { bumpMediaCacheBuster, fetchSubtree, fetchTree } from "./api";
import { collectFilePaths } from "./lib/linkResolver";
import { applyLoaded, lazyAncestors, lazyDirs, staleAfter, type LoadedDir } from "./lib/lazyTree";
import { subscribeFileChanges } from "./lib/fileEvents";
import { TreeLoaderContext, type TreeLoader } from "./components/TreeLoaderContext";
import type { TreeNode } from "./types";
import { ProcessQcDramaPage, ProcessQcRepoPage } from "./components/ProcessQcPage";
import { PROCESS_QC_DRAMA_ROUTE, PROCESS_QC_REPO_PATH } from "./lib/processQc";
import { REVIEW_STRATEGY_PATH } from "./lib/reviewStrategy";
import { REVIEW_ITEM_ROUTE, REVIEW_RUN_ROUTE } from "./lib/reviewRun";
import { ReviewItemPage, ReviewRunPage } from "./components/ReviewRunPage";
import { ReviewLawPage } from "./components/ReviewLawPage";
import { REVIEW_LAW_ROUTE } from "./lib/reviewLaw";
import { REVIEW_ISSUES_ROUTE } from "./lib/reviewV5";
import { ReviewIssuesPage } from "./components/ReviewIssuesPage";
import { ReviewCorrectionsPage } from "./components/ReviewCorrectionsPage";
import { REVIEW_CORRECTIONS_ROUTE } from "./lib/reviewCorrections";
import { ReviewStrategyPage } from "./components/ReviewStrategyPage";
import { TypedLocalStorage } from "./localStorage";

const sidebarCollapsedStore = new TypedLocalStorage<boolean>("aivm.sidebarCollapsed", false);

export default function App(): JSX.Element {
  // Lazy tree (follow-up 280): `base` is the first load (navigation + first
  // folder levels); `loaded` holds each opened folder's contents; the rendered
  // tree is the two merged.
  const [base, setBase] = useState<TreeNode | null>(null);
  const [loaded, setLoaded] = useState<ReadonlyMap<string, LoadedDir>>(() => new Map());
  const tree = useMemo(() => (base ? applyLoaded(base, loaded) : null), [base, loaded]);
  const baseRef = useRef(base);
  baseRef.current = base;
  const loadedRef = useRef(loaded);
  loadedRef.current = loaded;
  const inflight = useRef(new Set<string>());
  const [error, setError] = useState<string | null>(null);
  const [refreshKey, setRefreshKey] = useState<number>(0);
  const [sidebarCollapsed, setSidebarCollapsed] = useState<boolean>(() => sidebarCollapsedStore.read());
  const navigate = useNavigate();
  const location = useLocation();

  const loadTree = useCallback(async (bustMedia = true) => {
    // Not on live updates: a new cache-buster changes every media URL and would
    // restart a video the user is watching.
    if (bustMedia) bumpMediaCacheBuster();
    try {
      const t = await fetchTree();
      setBase(t);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    }
  }, []);

  const loadDir = useCallback(async (path: string, depth: number, force = false) => {
    const have = loadedRef.current.get(path);
    if (!force && have && (have.depth === 0 || (depth !== 0 && have.depth >= depth))) return;
    const key = `${path}#${depth}`;
    if (inflight.current.has(key)) return;
    inflight.current.add(key);
    try {
      const node = await fetchSubtree(path, depth);
      setLoaded((prev) => new Map(prev).set(path, { children: node.children ?? [], depth }));
    } catch {
      // Gone since the stub was listed (deleted / renamed): drop it; the next tree refresh removes the stub.
      setLoaded((prev) => {
        if (!prev.has(path)) return prev;
        const next = new Map(prev);
        next.delete(path);
        return next;
      });
    } finally {
      inflight.current.delete(key);
    }
  }, []);

  const refreshLoaded = useCallback((dirs: readonly string[]) => {
    for (const dir of dirs) void loadDir(dir, loadedRef.current.get(dir)?.depth ?? 1, true);
  }, [loadDir]);

  useEffect(() => {
    void loadTree();
    // A save / delete / import (refreshKey) can touch any opened folder too.
    if (refreshKey) refreshLoaded([...loadedRef.current.keys()]);
  }, [loadTree, refreshKey, refreshLoaded]);

  // Live updates (follow-up 280): refetch only what a batch of changed files touches.
  // At most one base refetch runs at a time; changes that arrive meanwhile (a
  // tool writing a folder of files) fold into one more refetch after it.
  useEffect(() => {
    let pending: string[] = [];
    let timer: ReturnType<typeof setTimeout> | null = null;
    let baseBusy = false;
    let baseAgain = false;
    const refetchBase = (): void => {
      if (baseBusy) { baseAgain = true; return; }
      baseBusy = true;
      void loadTree(false).finally(() => {
        baseBusy = false;
        if (baseAgain) { baseAgain = false; setTimeout(refetchBase, 1500); }
      });
    };
    const unsubscribe = subscribeFileChanges((paths) => {
      pending = pending.concat(paths);
      if (timer) clearTimeout(timer);
      timer = setTimeout(() => {
        const batch = pending;
        pending = [];
        timer = null;
        const stale = staleAfter(baseRef.current, loadedRef.current, batch);
        if (stale.base) refetchBase();
        refreshLoaded(stale.dirs);
      }, 500);
    });
    return () => {
      if (timer) clearTimeout(timer);
      unsubscribe();
    };
  }, [loadTree, refreshLoaded]);

  const treeLoader = useMemo<TreeLoader>(() => ({
    ensureLoaded: (path, depth = 1) => { void loadDir(path, depth); },
    ensureChildrenLoaded: (node) => {
      for (const child of node?.children ?? []) if (child.lazy) void loadDir(child.path, 1);
    },
  }), [loadDir]);

  const knownPaths = useMemo(() => (tree ? collectFilePaths(tree) : []), [tree]);
  const unloadedDirs = useMemo(() => tree ? lazyDirs(tree) : ["ai_videos"], [tree]);

  const currentPath = useMemo<string>(() => {
    if (!location.pathname.startsWith("/file/")) return "";
    const encoded = location.pathname.slice("/file/".length);
    try {
      return decodeURIComponent(encoded);
    } catch {
      return "";
    }
  }, [location.pathname]);

  // Opening a file deep in the tree: load the lazy folders on the way to it, then
  // the file's own sub-folders (renders/, archive/, model folders) for the sibling panel.
  useEffect(() => {
    if (!currentPath || !tree) return;
    const chain = lazyAncestors(tree, currentPath);
    for (const dir of chain) void loadDir(dir, 1);
    if (chain.length) return;
    const parent = currentPath.slice(0, currentPath.lastIndexOf("/"));
    const find = (node: TreeNode): TreeNode | null => {
      if (node.path === parent && node.type === "directory") return node;
      for (const child of node.children ?? []) {
        const hit = find(child);
        if (hit) return hit;
      }
      return null;
    };
    const folder = find(tree);
    for (const child of folder?.children ?? []) if (child.lazy) void loadDir(child.path, 1);
  }, [currentPath, tree, loadDir]);

  const onSelect = useCallback(
    (path: string) => {
      navigate(`/file/${encodeURIComponent(path)}`);
    },
    [navigate],
  );

  const onToggleSidebar = useCallback(() => {
    setSidebarCollapsed((prev) => {
      sidebarCollapsedStore.write(!prev);
      return !prev;
    });
  }, []);

  const onSkipToMain = (e: React.MouseEvent<HTMLAnchorElement>): void => {
    e.preventDefault();
    const main = document.getElementById("main");
    if (main) {
      main.setAttribute("tabindex", "-1");
      main.focus();
    }
  };

  return (
    <GlobalWorkflowProvider><TreeLoaderContext.Provider value={treeLoader}><div className={sidebarCollapsed ? "app-root app-root-sidebar-collapsed" : "app-root"}>
      <a className="skip-link" href="#main" onClick={onSkipToMain}>
        Skip to main content
      </a>
      <Sidebar
        tree={tree}
        currentPath={currentPath}
        onSelect={onSelect}
        loadError={error}
        collapsed={sidebarCollapsed}
        onToggleCollapsed={onToggleSidebar}
        onExpandLazy={treeLoader.ensureLoaded}
      />
      <main id="main" className="main-pane" aria-label="Main content">
        <div className="a11y-live-region" aria-live="polite" id="aria-live-toast" />
        <Routes>
          <Route path="/request-logs" element={<RequestLogsPage />} />
          <Route path="/" element={<Home tree={tree} />} />
          <Route
            path="/file/*"
            element={<Reader knownPaths={knownPaths} unloadedDirs={unloadedDirs} onSaved={() => setRefreshKey((k) => k + 1)} />}
          />
          <Route path="/assets" element={<AssetOverviewPage />} />
          <Route path={BASE_LAYOUT_ROUTE} element={<BaseLayoutPage />} />
          <Route path={MAP_REGIONS_ROUTE} element={<MapRegionsPage />} />
          <Route path={SHOP_ITEMS_ROUTE} element={<ShopItemsPage />} />
          <Route path={HERO_PREVIEW_ROUTE} element={<HeroPreviewPage />} />
          <Route path={RANK_PREVIEW_ROUTE} element={<RankPreviewPage />} />
          <Route path={DEV_PREVIEW_ROUTE} element={<DevPreviewPage />} />
          <Route path={GROUP_PREVIEW_ROUTE} element={<GroupPreviewPage />} />
          <Route path={CHARACTER_REVIEW_ROUTE} element={<CharacterReviewPage />} />
          <Route path={EPISODE_PREVIEW_ROUTE} element={<EpisodePreviewPage />} />
          <Route path={STORYBOARD_PREVIEW_ROUTE} element={<StoryboardPreviewPage />} />
          <Route path={SCENE_PREVIEW_ROUTE} element={<SceneBoardPage />} />
          <Route
            path="/characters"
            element={<CharacterGrid tree={tree} onChange={() => setRefreshKey((k) => k + 1)} />}
          />
          <Route
            path="/drama"
            element={<DramaPage tree={tree} onChange={() => setRefreshKey((k) => k + 1)} />}
          />
          <Route path={WORKFLOW_PATH} element={<WorkflowPage />} />
          <Route path={GLOBAL_SOURCE_PATH} element={<GlobalWorkflowSourcePage />} />
          <Route path={`${WORKFLOW_PATH}/category/:category`} element={<GlobalWorkflowCategoryPage />} />
          <Route path={`${WORKFLOW_PATH}/settings/:group`} element={<GlobalWorkflowGroupPage />} />
          <Route path={`${WORKFLOW_PATH}/:module`} element={<WorkflowPage />} />
          <Route path={`${WORKFLOW_PATH}/:module/:storySection`} element={<WorkflowPage />} />
          <Route path={FILMING_KNOWLEDGE_PATH} element={<FilmingKnowledgePage />} />
          <Route path={GLOSSARY_PATH} element={<GlossaryPage />} />
          <Route path={OVERVIEW_PATH} element={<WorkflowMapPage />} />
          <Route path={PROCESS_QC_REPO_PATH} element={<ProcessQcRepoPage />} />
          <Route path={REVIEW_STRATEGY_PATH} element={<ReviewStrategyPage />} />
          <Route path={REVIEW_RUN_ROUTE} element={<ReviewRunPage />} />
          <Route path={REVIEW_ITEM_ROUTE} element={<ReviewItemPage />} />
          <Route path={REVIEW_LAW_ROUTE} element={<ReviewLawPage />} />
          <Route path={REVIEW_ISSUES_ROUTE} element={<ReviewIssuesPage />} />
          <Route path={REVIEW_CORRECTIONS_ROUTE} element={<ReviewCorrectionsPage />} />
          <Route path={PROCESS_QC_DRAMA_ROUTE} element={<ProcessQcDramaPage />} />
          <Route path="/research" element={<ResearchPage />} />
          <Route
            path="/deleted"
            element={<DeletedView tree={tree} onChange={() => setRefreshKey((k) => k + 1)} />}
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div></TreeLoaderContext.Provider></GlobalWorkflowProvider>
  );
}
