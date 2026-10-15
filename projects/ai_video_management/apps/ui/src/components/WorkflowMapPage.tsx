import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import {
  Background, Controls, Handle, MarkerType, Position, ReactFlow,
  type Edge, type Node, type NodeProps,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { WORKFLOW_MAP, WORKFLOW_MAP_SOURCE, isModule, mapNode, type MapModule, type MapPhase, type MapSupport, type WorkflowMap } from "../lib/workflowMap";
import { globalSourceUrl } from "../lib/globalWorkflow";
import { OverviewTabs } from "./OverviewTabs";
import "./GlossaryPage.css";
import "./WorkflowMapPage.css";

type ModuleNodeData = { module: MapModule; statusColor: string; statusZh: string; dimmed: boolean; selected: boolean };
type SupportNodeData = { support: MapSupport; dimmed: boolean; selected: boolean };
type PhaseNodeData = { phase: MapPhase };
type MapNode = Node<ModuleNodeData, "module"> | Node<SupportNodeData, "support"> | Node<PhaseNodeData, "phase">;

const SIDES = [Position.Top, Position.Right, Position.Bottom, Position.Left];
const Handles = (): JSX.Element => <>
  {SIDES.map(side => <Handle key={`s-${side}`} id={`s-${side}`} type="source" position={side} isConnectable={false} />)}
  {SIDES.map(side => <Handle key={`t-${side}`} id={`t-${side}`} type="target" position={side} isConnectable={false} />)}
</>;

function ModuleNode({ data }: NodeProps<Node<ModuleNodeData, "module">>): JSX.Element {
  const { module } = data;
  return <div className={["map-module", data.dimmed ? "is-dimmed" : "", data.selected ? "is-selected" : "", module.status === "placeholder" ? "is-placeholder" : ""].join(" ")}>
    <Handles />
    <header><strong>{module.zh}</strong><span className="map-status" style={{ color: data.statusColor, borderColor: data.statusColor }}>{data.statusZh}</span></header>
    <span className="map-en">{module.en}</span>
    <ol>{module.steps.map(step => <li key={step}>{step}</li>)}</ol>
    <p className="map-gate">关卡：{module.gate}</p>
    <p className="map-output">产出：{module.output}</p>
  </div>;
}

function SupportNode({ data }: NodeProps<Node<SupportNodeData, "support">>): JSX.Element {
  return <div className={["map-support", data.dimmed ? "is-dimmed" : "", data.selected ? "is-selected" : ""].join(" ")}>
    <Handles />
    <strong>{data.support.zh}</strong>
    <span className="map-en">{data.support.en}</span>
  </div>;
}

function PhaseNode({ data }: NodeProps<Node<PhaseNodeData, "phase">>): JSX.Element {
  return <div className="map-phase" style={{ width: data.phase.w, height: data.phase.h, background: data.phase.color }}>
    <span>{data.phase.zh} <small>{data.phase.en}</small></span>
  </div>;
}

const nodeTypes = { module: ModuleNode, support: SupportNode, phase: PhaseNode };
const MODULE_W = 220;
const SUPPORT_W = 160;

/** Snake layout: creation runs left→right on top, post-production returns right→left below. */
function handles(map: WorkflowMap, from: string, to: string, type: string): [string, string] {
  const source = mapNode(map, from)!;
  const target = mapNode(map, to)!;
  const sameRow = Math.abs(source.y - target.y) < 60;
  if (type === "handoff" && !sameRow) return [`s-${Position.Right}`, `t-${Position.Right}`];
  if (type === "feedback" && sameRow) return [`s-${Position.Top}`, `t-${Position.Top}`];
  if (!sameRow) return source.y > target.y ? [`s-${Position.Top}`, `t-${Position.Bottom}`] : [`s-${Position.Bottom}`, `t-${Position.Top}`];
  return source.x < target.x ? [`s-${Position.Right}`, `t-${Position.Left}`] : [`s-${Position.Left}`, `t-${Position.Right}`];
}

function Detail({ map, id, onSelect }: { map: WorkflowMap; id: string; onSelect: (id: string) => void }): JSX.Element {
  const entry = mapNode(map, id);
  if (!entry) {
    return <aside className="glossary-detail" aria-label="节点详情">
      <h2>工作流全景</h2>
      <p>{map.summary}</p>
      <p className="glossary-hint">点一个模块或支持层，查看输入、产出、关卡、文件与链接。</p>
    </aside>;
  }
  const related = map.edges.filter(edge => edge.from === id || edge.to === id);
  const status = isModule(entry) ? map.statuses.find(item => item.id === entry.status) : undefined;
  return <aside className="glossary-detail" aria-label="节点详情">
    {status ? <p className="glossary-chip" style={{ color: status.color, borderColor: status.color }}>{status.zh}</p> : <p className="glossary-chip">支持层</p>}
    <h2>{entry.zh} <span lang="en">{entry.en}</span></h2>
    <p>{entry.purpose}</p>
    {isModule(entry) ? <dl>
      <dt>输入</dt><dd>{entry.input}</dd>
      <dt>产出</dt><dd>{entry.output}</dd>
      <dt>关卡</dt><dd>{entry.gate}</dd>
      <dt>步骤</dt><dd>{entry.steps.join(" → ")}</dd>
    </dl> : null}
    {entry.files.length ? <><h3>文件</h3><ul className="glossary-sources">{entry.files.map(file => <li key={file}><code>{file}</code></li>)}</ul></> : null}
    <h3>连接</h3>
    <ul className="glossary-relations">
      {related.map(edge => {
        const type = map.edge_types.find(item => item.id === edge.type);
        const other = edge.from === id ? edge.to : edge.from;
        return <li key={`${edge.from}-${edge.to}-${edge.type}`}>
          <span className="glossary-card" style={{ color: type?.color, borderColor: type?.color }}>{type?.zh.split("（")[0]}</span>
          <button type="button" onClick={() => onSelect(other)}>{edge.from === id ? "→" : "←"} {mapNode(map, other)?.zh}</button>
          <span>{edge.zh}</span>
        </li>;
      })}
    </ul>
    {entry.nav ? <p><Link to={entry.nav}>打开 {entry.zh} →</Link></p> : null}
    <button type="button" className="glossary-clear" onClick={() => onSelect("")}>回到全景说明</button>
  </aside>;
}

export function WorkflowMapGraph({ map, selected, hidden, onSelect }: {
  map: WorkflowMap; selected: string; hidden: Set<string>; onSelect: (id: string) => void;
}): JSX.Element {
  const visible = useMemo(() => map.edges.filter(edge => !hidden.has(edge.type)), [map, hidden]);
  const neighbours = useMemo(() => new Set([selected, ...visible.filter(e => e.from === selected || e.to === selected).flatMap(e => [e.from, e.to])]), [selected, visible]);
  const nodes: MapNode[] = useMemo(() => [
    ...map.phases.map(phase => ({ id: `phase-${phase.id}`, type: "phase" as const, position: { x: phase.x, y: phase.y }, data: { phase },
      selectable: false, draggable: false, zIndex: -1, width: phase.w, height: phase.h })),
    ...map.modules.map(module => {
      const status = map.statuses.find(item => item.id === module.status);
      return { id: module.id, type: "module" as const, position: { x: module.x, y: module.y }, width: MODULE_W,
        data: { module, statusColor: status?.color || "#64748b", statusZh: status?.zh || "", dimmed: Boolean(selected) && !neighbours.has(module.id), selected: module.id === selected } };
    }),
    ...map.supports.map(support => ({ id: support.id, type: "support" as const, position: { x: support.x, y: support.y }, width: SUPPORT_W,
      data: { support, dimmed: Boolean(selected) && !neighbours.has(support.id), selected: support.id === selected } })),
  ], [map, selected, neighbours]);
  const edges: Edge[] = useMemo(() => visible.map(edge => {
    const type = map.edge_types.find(item => item.id === edge.type);
    const [sourceHandle, targetHandle] = handles(map, edge.from, edge.to, edge.type);
    const touching = edge.from === selected || edge.to === selected;
    const color = type?.color || "#334155";
    return {
      id: `${edge.from}-${edge.to}-${edge.type}`, source: edge.from, target: edge.to, sourceHandle, targetHandle,
      type: edge.type === "feedback" ? "default" : "smoothstep", label: edge.zh, animated: touching && edge.type === "handoff",
      style: { stroke: color, strokeWidth: edge.type === "handoff" ? 2.6 : 1.6, strokeDasharray: type?.dash || undefined, opacity: selected && !touching ? 0.15 : 1 },
      labelStyle: { fill: color, fontSize: 12, fontWeight: 600 }, labelBgStyle: { fill: "#ffffff", fillOpacity: selected && !touching ? 0.2 : 0.9 },
      labelBgPadding: [4, 2] as [number, number], labelBgBorderRadius: 4,
      markerEnd: { type: MarkerType.ArrowClosed, color, width: 14, height: 14 },
    };
  }), [map, visible, selected]);
  return <div className="glossary-graph map-graph" aria-label="工作流全景图">
    <ReactFlow nodes={nodes} edges={edges} nodeTypes={nodeTypes}
      onNodeClick={(_, node) => { if (node.type !== "phase") onSelect(node.id); }} onPaneClick={() => onSelect("")}
      fitView fitViewOptions={{ padding: 0.08 }} minZoom={0.3} maxZoom={2}
      zoomOnScroll={false} panOnScroll={false} preventScrolling={false} zoomOnPinch zoomOnDoubleClick
      nodesConnectable={false} proOptions={{ hideAttribution: true }}>
      <Background gap={24} color="#e2e8f0" />
      <Controls position="bottom-left" showInteractive={false} />
    </ReactFlow>
  </div>;
}

export function WorkflowMapPage(): JSX.Element {
  const map = WORKFLOW_MAP;
  const [selected, setSelected] = useState("");
  const [hidden, setHidden] = useState<Set<string>>(new Set());
  const toggle = (id: string): void => setHidden(previous => {
    const next = new Set(previous);
    if (next.has(id)) next.delete(id); else next.add(id);
    return next;
  });
  return <div className="episode-workflow glossary-page">
    <OverviewTabs active="map" source={globalSourceUrl(WORKFLOW_MAP_SOURCE)} />
    <p className="map-summary">{map.summary}</p>
    <div className="glossary-body">
      <section className="glossary-main" aria-label="工作流全景">
        <div className="glossary-legend">
          <div role="group" aria-label="模块状态">
            {map.statuses.map(status => <span key={status.id} className="glossary-legend-item"><i style={{ background: status.color }} />{status.zh}</span>)}
          </div>
          <div role="group" aria-label="连线类型（点击显示或隐藏）">
            {map.edge_types.map(type => <button key={type.id} type="button" aria-pressed={!hidden.has(type.id)} onClick={() => toggle(type.id)}>
              <svg width="28" height="8" aria-hidden="true"><line x1="0" y1="4" x2="28" y2="4" stroke={type.color} strokeWidth="2" strokeDasharray={type.dash || undefined} /></svg>
              {type.zh}
            </button>)}
          </div>
        </div>
        <WorkflowMapGraph map={map} selected={selected} hidden={hidden} onSelect={setSelected} />
        <table className="glossary-table map-table" aria-label="模块一览">
          <thead><tr><th>#</th><th>模块</th><th>状态</th><th>输入</th><th>产出</th><th>关卡</th></tr></thead>
          <tbody>{map.modules.map((module, index) => <tr key={module.id} className={module.id === selected ? "is-selected" : ""} onClick={() => setSelected(module.id)}>
            <td>{index + 1}</td>
            <th scope="row"><button type="button" onClick={() => setSelected(module.id)}>{module.zh}</button></th>
            <td>{map.statuses.find(status => status.id === module.status)?.zh}</td>
            <td>{module.input}</td><td>{module.output}</td><td>{module.gate}</td>
          </tr>)}</tbody>
        </table>
      </section>
      <Detail map={map} id={selected} onSelect={setSelected} />
    </div>
  </div>;
}
