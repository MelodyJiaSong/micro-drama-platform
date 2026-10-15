import { Link } from "react-router-dom";
import { GLOSSARY_PATH, OVERVIEW_PATH, WORKFLOW_PATH } from "../lib/workflowData";

/** Shared header of the 总览 group: one level above the individual modules. */
export function OverviewTabs({ active, source }: { active: "map" | "glossary"; source: string }): JSX.Element {
  return <>
    <nav aria-label="总览导航"><Link to={WORKFLOW_PATH}>工作流</Link><span> / 总览</span></nav>
    <header className="glossary-header">
      <div><h1>总览 <span lang="en">Overview</span></h1></div>
      <Link to={source}>源数据 →</Link>
    </header>
    <div className="glossary-tabs" role="tablist" aria-label="总览">
      <Link role="tab" aria-selected={active === "map"} to={OVERVIEW_PATH}>工作流全景</Link>
      <Link role="tab" aria-selected={active === "glossary"} to={GLOSSARY_PATH}>术语表</Link>
    </div>
  </>;
}
