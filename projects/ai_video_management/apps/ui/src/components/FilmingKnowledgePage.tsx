import { Navigate } from "react-router-dom";
import { FILMING_SHOTS_SOURCE } from "../lib/workflowData";
import { globalSourceUrl } from "../lib/globalWorkflow";

/** Old knowledge URL (follow-up 213): shot design is now a set of catalog source pages. */
export function FilmingKnowledgePage(): JSX.Element {
  return <Navigate to={globalSourceUrl(FILMING_SHOTS_SOURCE)} replace />;
}
