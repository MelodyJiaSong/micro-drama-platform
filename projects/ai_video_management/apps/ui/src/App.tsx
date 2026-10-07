import { useCallback, useEffect, useMemo, useState } from "react";
import { Routes, Route, Navigate, useLocation, useNavigate } from "react-router-dom";
import { Sidebar } from "./components/Sidebar";
import { Reader } from "./components/Reader";
import { Home } from "./components/Home";
import { ActorGrid } from "./components/ActorGrid";
import { CharacterGrid } from "./components/CharacterGrid";
import { DramaPage } from "./components/DramaPage";
import { DeletedView } from "./components/DeletedView";
import { WorkflowPage } from "./components/WorkflowPage";
import { FilmingKnowledgePage } from "./components/FilmingKnowledgePage";
import { GlobalWorkflowProvider } from "./components/GlobalWorkflowContext";
import { GlobalWorkflowCategoryPage, GlobalWorkflowGroupPage, GlobalWorkflowSourcePage } from "./components/GlobalWorkflowPage";
import { GLOBAL_SOURCE_PATH } from "./lib/globalWorkflow";
import { FILMING_KNOWLEDGE_PATH, WORKFLOW_PATH } from "./lib/workflowData";
import { ResearchPage } from "./components/ResearchPage";
import { WritersRoomPage } from "./components/WritersRoomPage";
import { RequestLogsPage } from "./components/RequestLogsPage";
import { StoryRunsPage } from "./components/StoryRunsPage";
import { StoryRunStoryPage } from "./components/StoryRunStoryPage";
import { StoryRunStatePage } from "./components/StoryRunStatePage";
import { StoryRunInputPage } from "./components/StoryRunInputPage";
import { StoryRunItemPage } from "./components/StoryRunItemPage";
import { StoryRunProcessPage } from "./components/StoryRunProcessPage";
import { StoryRunComparePage } from "./components/StoryRunComparePage";
import { STORY_RUN_PAGES } from "./lib/storyRunRoutes";
import { SharedStoryInputPage } from "./components/SharedStoryInputPage";
import { bumpMediaCacheBuster, fetchTree } from "./api";
import { collectFilePaths } from "./lib/linkResolver";
import type { TreeNode } from "./types";

export default function App(): JSX.Element {
  const [tree, setTree] = useState<TreeNode | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [refreshKey, setRefreshKey] = useState<number>(0);
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

  const onSkipToMain = (e: React.MouseEvent<HTMLAnchorElement>): void => {
    e.preventDefault();
    const main = document.getElementById("main");
    if (main) {
      main.setAttribute("tabindex", "-1");
      main.focus();
    }
  };

  return (
    <GlobalWorkflowProvider><div className="app-root">
      <a className="skip-link" href="#main" onClick={onSkipToMain}>
        Skip to main content
      </a>
      <Sidebar
        tree={tree}
        currentPath={currentPath}
        onSelect={onSelect}
        loadError={error}
        onTreeReload={() => setRefreshKey((k) => k + 1)}
      />
      <main id="main" className="main-pane" aria-label="Main content">
        <div className="a11y-live-region" aria-live="polite" id="aria-live-toast" />
        <Routes>
          <Route path="/story-runs" element={<StoryRunsPage />} />
          <Route path={STORY_RUN_PAGES.output.path} element={<StoryRunStoryPage />} />
          <Route path={STORY_RUN_PAGES.state.path} element={<StoryRunStatePage />} />
          <Route path={STORY_RUN_PAGES.input.path} element={<StoryRunInputPage />} />
          <Route path={STORY_RUN_PAGES.item.path} element={<StoryRunItemPage />} />
          <Route path={STORY_RUN_PAGES.process.path} element={<StoryRunProcessPage />} />
          <Route path={STORY_RUN_PAGES.compare.path} element={<StoryRunComparePage />} />
          <Route path="/story-input" element={<SharedStoryInputPage />} />
          <Route path="/request-logs" element={<RequestLogsPage />} />
          <Route path="/" element={<Home tree={tree} />} />
          <Route
            path="/file/*"
            element={<Reader tree={tree} knownPaths={knownPaths} onSaved={() => setRefreshKey((k) => k + 1)} />}
          />
          <Route
            path="/actors"
            element={<ActorGrid tree={tree} onChange={() => setRefreshKey((k) => k + 1)} />}
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
          <Route path="/research" element={<ResearchPage />} />
          <Route path="/writers-room" element={<WritersRoomPage />} />
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
