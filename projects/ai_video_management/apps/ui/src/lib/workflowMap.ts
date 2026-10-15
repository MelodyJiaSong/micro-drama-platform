import data from "../../../../../../.agents/references/project/ai_video_workflow_map.json";

export interface MapStatus { id: string; zh: string; color: string; }
export interface MapPhase { id: string; zh: string; en: string; color: string; x: number; y: number; w: number; h: number; }
export interface MapModule {
  id: string; zh: string; en: string; phase: string; status: string; x: number; y: number;
  purpose: string; steps: string[]; input: string; output: string; files: string[]; gate: string; nav: string;
}
export interface MapSupport { id: string; zh: string; en: string; x: number; y: number; purpose: string; files: string[]; nav: string; }
export interface MapEdgeType { id: string; zh: string; color: string; dash: string; }
export interface MapEdge { from: string; to: string; type: string; zh: string; }
export interface WorkflowMap {
  summary: string; statuses: MapStatus[]; phases: MapPhase[]; modules: MapModule[]; supports: MapSupport[];
  edge_types: MapEdgeType[]; edges: MapEdge[];
}

/** Single source: `.agents/references/project/ai_video_workflow_map.json` (bundled at build time). */
export const WORKFLOW_MAP = data as WorkflowMap;
export const WORKFLOW_MAP_SOURCE = "repo:.agents/references/project/ai_video_workflow_map.json";

export const mapNode = (map: WorkflowMap, id: string): MapModule | MapSupport | undefined =>
  map.modules.find(entry => entry.id === id) || map.supports.find(entry => entry.id === id);
export const isModule = (entry: MapModule | MapSupport): entry is MapModule => "steps" in entry;

export function workflowMapProblems(map: WorkflowMap): string[] {
  const ids = [...map.modules, ...map.supports].map(entry => entry.id);
  const problems: string[] = [];
  if (new Set(ids).size !== ids.length) problems.push("duplicate node id");
  const phases = new Set(map.phases.map(phase => phase.id));
  const statuses = new Set(map.statuses.map(status => status.id));
  const types = new Set(map.edge_types.map(type => type.id));
  for (const module of map.modules) {
    if (!phases.has(module.phase)) problems.push(`unknown phase on ${module.id}`);
    if (!statuses.has(module.status)) problems.push(`unknown status on ${module.id}`);
  }
  for (const edge of map.edges) {
    if (!ids.includes(edge.from) || !ids.includes(edge.to)) problems.push(`dangling edge ${edge.from}→${edge.to}`);
    if (!types.has(edge.type)) problems.push(`unknown edge type ${edge.type}`);
  }
  return problems;
}
