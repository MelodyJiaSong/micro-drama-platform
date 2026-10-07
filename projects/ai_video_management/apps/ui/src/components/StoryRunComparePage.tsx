import { useSearchParams } from "react-router-dom";
import { StoryRunPage } from "./StoryRunPage";
import { StoryRunCompare } from "./StoryRunCompare";

export function StoryRunComparePage(): JSX.Element {
  const [params, setParams] = useSearchParams();
  const compare = params.get("compare_run_id") || "";
  return <StoryRunPage document="compare">{({ run, runs }) => <StoryRunCompare run={run} runs={runs} compareId={compare}
    onCompare={id => { const next = new URLSearchParams(params); next.set("compare_run_id", id); setParams(next); }}
    onPrimary={id => { const next = new URLSearchParams(params); if (id === compare) next.set("compare_run_id", run.run_id); next.set("run_id", id); setParams(next); }} />}</StoryRunPage>;
}
