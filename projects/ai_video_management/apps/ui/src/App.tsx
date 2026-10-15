import { useCallback, useEffect, useMemo, useState } from "react";
import { Routes, Route, Navigate, useLocation, useNavigate } from "react-router-dom";
import { Sidebar } from "./components/Sidebar";
import { Reader } from "./components/Reader";
import { Home } from "./components/Home";
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
import { bumpMediaCacheBuster, fetchTree } from "./api";
import { collectFilePaths } from "./lib/linkResolver";
import type { TreeNode } from "./types";
import { TypedLocalStorage } from "./localStorage";

const sidebarCollapsedStore = new TypedLocalStorage<boolean>("aivm.sidebarCollapsed", false);

export default function App(): JSX.Element {
  const [tree, setTree] = useState<TreeNode | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [refreshKey, setRefreshKey] = useState<number>(0);
  const [sidebarCollapsed, setSidebarCollapsed] = useState<boolean>(() => sidebarCollapsedStore.read());
  const navigate = useNavigate();
  const location = useLocation();

  const loadTree = useCallback(async () => {
    bumpMediaCacheBuster();
    try {
      const t = await fetchTree();
      setTree(t);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    }
  }, []);

  useEffect(() => {
    void loadTree();
  }, [loadTree, refreshKey]);

  const knownPaths = useMemo(() => (tree ? collectFilePaths(tree) : []), [tree]);

  const currentPath = useMemo<string>(() => {
    if (!location.pathname.startsWith("/file/")) return "";
    const encoded = location.pathname.slice("/file/".length);
    try {
      return decodeURIComponent(encoded);
    } catch {
      return "";
    }
  }, [location.pathname]);

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
    <GlobalWorkflowProvider><div className={sidebarCollapsed ? "app-root app-root-sidebar-collapsed" : "app-root"}>
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
      />
      <main id="main" className="main-pane" aria-label="Main content">
        <div className="a11y-live-region" aria-live="polite" id="aria-live-toast" />
        <Routes>
          <Route path="/request-logs" element={<RequestLogsPage />} />
          <Route path="/" element={<Home tree={tree} />} />
          <Route
            path="/file/*"
            element={<Reader knownPaths={knownPaths} onSaved={() => setRefreshKey((k) => k + 1)} />}
          />
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
          <Route path="/research" element={<ResearchPage />} />
          <Route
            path="/deleted"
            element={<DeletedView tree={tree} onChange={() => setRefreshKey((k) => k + 1)} />}
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div></GlobalWorkflowProvider>
  );
}
