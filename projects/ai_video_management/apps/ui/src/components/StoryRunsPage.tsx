import { Navigate, useSearchParams } from "react-router-dom";
import { STORY_RUN_PAGES, storyRunUrl, type StoryRunDocument } from "../lib/storyRunRoutes";

export function StoryRunsPage(): JSX.Element {
  const [params] = useSearchParams();
  const requested = params.get("view") || (params.get("compare_run_id") ? "compare" : "output");
  const document = Object.keys(STORY_RUN_PAGES).includes(requested) ? requested as StoryRunDocument : "output";
  return <Navigate replace to={storyRunUrl(document, params.get("episode_path") || "", params.get("run_id") || undefined, params.get("compare_run_id") || undefined)} />;
}
