import { useMemo } from "react";
import {
  Background, Controls, Handle, MarkerType, MiniMap, Position, ReactFlow,
  type Edge, type Node, type NodeProps,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { categoryOf, inGraph, relationType, type Glossary, type GlossaryTerm } from "../lib/glossary";

type TermNodeData = { term: GlossaryTerm; color: string; dimmed: boolean; selected: boolean };
type TermNode = Node<TermNodeData, "term">;

const SIDES = [Position.Top, Position.Right, Position.Bottom, Position.Left];
const NODE_W = 150;
const NODE_H = 58;

function TermNodeView({ data }: NodeProps<TermNode>): JSX.Element {
  return <div className={["glossary-node", data.dimmed ? "is-dimmed" : "", data.selected ? "is-selected" : ""].join(" ")}
    style={{ borderColor: data.color, ["--term-color" as string]: data.color }}>
    {SIDES.map(side => <Handle key={`s-${side}`} id={`s-${side}`} type="source" position={side} isConnectable={false} />)}
    {SIDES.map(side => <Handle key={`t-${side}`} id={`t-${side}`} type="target" position={side} isConnectable={false} />)}
    <strong>{data.term.zh}</strong>
    <span>{data.term.en}</span>
  </div>;
}

const nodeTypes = { term: TermNodeView };

/** Pick the facing sides so edges leave and enter nodes along the shorter axis. */
function sides(from: GlossaryTerm, to: GlossaryTerm): [Position, Position] {
  const dx = to.x - from.x;
  const dy = to.y - from.y;
  if (Math.abs(dy) >= Math.abs(dx) * 0.6) return dy > 0 ? [Position.Bottom, Position.Top] : [Position.Top, Position.Bottom];
  return dx > 0 ? [Position.Right, Position.Left] : [Position.Left, Position.Right];
}

export function GlossaryGraph({ glossary, selected, hidden, onSelect }: {
  glossary: Glossary; selected: string; hidden: Set<string>; onSelect: (id: string) => void;
}): JSX.Element {
  const terms = useMemo(() => glossary.terms.filter(inGraph), [glossary]);
  const visible = useMemo(() => {
    const ids = new Set(terms.map(term => term.id));
    return glossary.relations.filter(relation => !hidden.has(relation.type) && ids.has(relation.from) && ids.has(relation.to));
  }, [glossary, terms, hidden]);
  const neighbours = useMemo(() => new Set([selected, ...visible.filter(r => r.from === selected || r.to === selected).flatMap(r => [r.from, r.to])]), [selected, visible]);

  const nodes: TermNode[] = useMemo(() => terms.map(term => ({
    id: term.id, type: "term" as const, position: { x: term.x, y: term.y },
    width: NODE_W, height: NODE_H, draggable: true,
    data: { term, color: categoryOf(glossary, term)?.color || "#475569", dimmed: Boolean(selected) && !neighbours.has(term.id), selected: term.id === selected },
  })), [glossary, terms, selected, neighbours]);

  const edges: Edge[] = useMemo(() => visible.map(relation => {
    const from = glossary.terms.find(term => term.id === relation.from)!;
    const to = glossary.terms.find(term => term.id === relation.to)!;
    const [sourceSide, targetSide] = sides(from, to);
    const type = relationType(glossary, relation.type);
    const touching = relation.from === selected || relation.to === selected;
    const color = type?.color || "#64748b";
    const twoWay = relation.card === "N:M";
    return {
      id: `${relation.from}-${relation.to}-${relation.type}`,
      source: relation.from, target: relation.to,
      sourceHandle: `s-${sourceSide}`, targetHandle: `t-${targetSide}`,
      label: relation.card || undefined, animated: touching && relation.type !== "contains",
      style: { stroke: color, strokeWidth: touching ? 2.4 : 1.4, strokeDasharray: type?.dash || undefined, opacity: selected && !touching ? 0.15 : 1 },
      labelStyle: { fill: color, fontWeight: 700, fontSize: 13 },
      labelBgStyle: { fill: "#ffffff", fillOpacity: selected && !touching ? 0.2 : 0.9 },
      labelBgPadding: [4, 2] as [number, number], labelBgBorderRadius: 4,
      markerEnd: { type: MarkerType.ArrowClosed, color, width: 14, height: 14 },
      ...(twoWay ? { markerStart: { type: MarkerType.ArrowClosed, color, width: 14, height: 14 } } : {}),
      ariaLabel: `${from.zh} ${relation.zh}（${relation.card}）${to.zh}`,
    };
  }), [glossary, visible, selected]);

  return <div className="glossary-graph" aria-label="术语关系图">
    <ReactFlow
      nodes={nodes} edges={edges} nodeTypes={nodeTypes}
      onNodeClick={(_, node) => onSelect(node.id)}
      onPaneClick={() => onSelect("")}
      fitView fitViewOptions={{ padding: 0.05 }} minZoom={0.3} maxZoom={2}
      zoomOnScroll={false} panOnScroll={false} preventScrolling={false} zoomOnPinch zoomOnDoubleClick
      nodesConnectable={false} elementsSelectable proOptions={{ hideAttribution: true }}
    >
      <Background gap={24} color="#e2e8f0" />
      <MiniMap position="bottom-left" pannable zoomable style={{ width: 150, height: 110 }} nodeColor={node => (node.data as TermNodeData).color} nodeStrokeWidth={2} />
      <Controls position="top-left" showInteractive={false} />
    </ReactFlow>
  </div>;
}
