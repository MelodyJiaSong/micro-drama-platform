import { useMemo, useState } from "react";
import {
  CASES, DEP_EDGES, DEP_NODES, LAWS, STAGES, closure, lawsAt,
  type DepNode, type LawId, type StageId,
} from "../lib/reviewStrategy";

/** 按字数折行（中英混排按字符数近似）。 */
export function wrap(text: string, n: number): string[] {
  const out: string[] = [];
  let cur = "";
  for (const ch of Array.from(text)) {
    cur += ch;
    if (Array.from(cur).length >= n) { out.push(cur); cur = ""; }
  }
  if (cur) out.push(cur);
  return out;
}

function Lines({ x, y, lines, cls, lh = 14, anchor = "middle" }: {
  x: number; y: number; lines: string[]; cls?: string; lh?: number; anchor?: "start" | "middle" | "end";
}): JSX.Element {
  return <text x={x} y={y} className={cls} textAnchor={anchor}>
    {lines.map((l, i) => <tspan key={i} x={x} dy={i === 0 ? 0 : lh}>{l}</tspan>)}
  </text>;
}

function Arrows(): JSX.Element {
  const m = (id: string, color: string): JSX.Element => <marker key={id} id={id} viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill={color} />
  </marker>;
  return <defs><linearGradient id="rs-cost" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stopColor="#dcefed" /><stop offset="1" stopColor="#f6d5cf" /></linearGradient>{[m("rs-a", "#4b5563"), m("rs-a-red", "#b3372c"), m("rs-a-green", "#0e7a5f"), m("rs-a-blue", "#2563eb"), m("rs-a-amber", "#b45309"), m("rs-a-faint", "#cbd5e1")]}</defs>;
}

// ============ 1. 主流程：每关 产物 → 机检 → 审稿人 → 闸门 ============
const FX = (i: number): number => 40 + i * 200;
const F = { cost: 22, art: 62, artH: 56, mac: 150, macH: 40, rev: 214, revH: 48, gate: 312, gr: 26, human: 350, loop: 418 };

export function FlowDiagram({ selected, onSelect, highlightLaw }: {
  selected: StageId | null; onSelect: (s: StageId) => void; highlightLaw?: LawId | null;
}): JSX.Element {
  const W = FX(5) + 170 + 60;
  return <svg className="rs-svg" viewBox={`0 0 ${W} 470`} width={W} height={470} role="img" aria-label="六道关主流程图">
    <Arrows />
    <rect x={FX(0)} y={F.cost} width={FX(5) + 170 - FX(0)} height={20} rx={4} className="rs-costbar" />
    <text x={FX(0) + 6} y={F.cost + 14} className="rs-cost-l">返工便宜</text>
    <text x={FX(5) + 164} y={F.cost + 14} className="rs-cost-r" textAnchor="end">返工昂贵</text>
    {STAGES.map((s, i) => {
      const x = FX(i); const on = selected === s.id;
      const laws = lawsAt(s.id); const fresh = s.machine.filter(m => m.isNew).length + laws.filter(l => l.isNew).length;
      const next = i < STAGES.length - 1 ? FX(i + 1) : null;
      return <g key={s.id} className={`rs-col${on ? " rs-on" : ""}`} onClick={() => onSelect(s.id)} role="button" tabIndex={0}
        onKeyDown={e => { if (e.key === "Enter" || e.key === " ") onSelect(s.id); }} aria-label={`${s.no} ${s.name}`}>
        <rect x={x - 6} y={F.art - 8} width={182} height={F.human - F.art + 30} rx={10} className="rs-colbg" />
        {/* 产物 */}
        <rect x={x} y={F.art} width={170} height={F.artH} rx={8} className="rs-art" />
        <text x={x + 10} y={F.art + 22} className="rs-art-t">{s.no} {s.name}</text>
        <text x={x + 10} y={F.art + 42} className="rs-art-f">{s.file}</text>
        {fresh ? <g><rect x={x + 128} y={F.art + 8} width={34} height={16} rx={8} className="rs-new" /><text x={x + 145} y={F.art + 20} className="rs-new-t" textAnchor="middle">+{fresh}</text></g> : null}
        {/* 机检 */}
        <line x1={x + 95} y1={F.art + F.artH} x2={x + 95} y2={F.mac - 2} className="rs-e" markerEnd="url(#rs-a)" />
        <rect x={x + 20} y={F.mac} width={150} height={F.macH} rx={6} className="rs-mac" />
        <text x={x + 30} y={F.mac + 25} className="rs-mac-t">机检 {s.machine.length} 项{s.machine.some(m => m.isNew) ? `（新 ${s.machine.filter(m => m.isNew).length}）` : ""}</text>
        {/* 审稿人 */}
        <line x1={x + 95} y1={F.mac + F.macH} x2={x + 95} y2={F.rev - 2} className="rs-e" markerEnd="url(#rs-a)" />
        <rect x={x + 20} y={F.rev} width={150} height={F.revH} rx={6} className="rs-rev" />
        <text x={x + 30} y={F.rev + 19} className="rs-rev-t">独立审稿 {laws.length} 位</text>
        {laws.map((l, k) => <circle key={l.id} cx={x + 36 + k * 18} cy={F.rev + 34} r={6} fill={l.color}
          className={highlightLaw && highlightLaw !== l.id ? "rs-dim" : ""}><title>{l.name}</title></circle>)}
        {/* 闸门 */}
        <line x1={x + 95} y1={F.rev + F.revH} x2={x + 95} y2={F.gate - F.gr - 2} className="rs-e" markerEnd="url(#rs-a)" />
        <polygon points={`${x + 95},${F.gate - F.gr} ${x + 95 + F.gr + 10},${F.gate} ${x + 95},${F.gate + F.gr} ${x + 95 - F.gr - 10},${F.gate}`} className="rs-gate" />
        <text x={x + 95} y={F.gate + 4} className="rs-gate-t" textAnchor="middle">闸门</text>
        {/* 不过：回到本关产物（或更上游） */}
        <path d={`M${x + 95 - F.gr - 10},${F.gate} H${x + 8} V${F.art + F.artH + 2}`} className="rs-e rs-fail" markerEnd="url(#rs-a-red)" />
        <text x={x + 11} y={F.gate - 8} className="rs-fail-t">不过</text>
        {/* 人点 */}
        {s.human ? <g><rect x={x + 20} y={F.human - 2} width={150} height={22} rx={11} className="rs-human" />
          <text x={x + 95} y={F.human + 13} className="rs-human-t" textAnchor="middle">★ {s.human}</text></g> : null}
        {/* 过：进下一关 */}
        {next !== null ? <g>
          <path d={`M${x + 95 + F.gr + 10},${F.gate} H${x + 185} V${F.art + F.artH / 2} H${next - 2}`} className="rs-e rs-pass" markerEnd="url(#rs-a-green)" />
          <text x={x + 189} y={F.gate - 6} className="rs-pass-t">过</text>
        </g> : null}
      </g>;
    })}
    {/* 漏网回路 */}
    <g className="rs-loop">
      <rect x={FX(5)} y={F.loop} width={170} height={36} rx={8} className="rs-loopnode rs-loop-start" />
      <text x={FX(5) + 85} y={F.loop + 23} textAnchor="middle" className="rs-loop-t">用户 / 审片抓到漏网</text>
      <rect x={FX(3) + 20} y={F.loop} width={170} height={36} rx={8} className="rs-loopnode" />
      <text x={FX(3) + 105} y={F.loop + 23} textAnchor="middle" className="rs-loop-t">qc.py defect 记缺陷</text>
      <rect x={FX(2) - 30} y={F.loop} width={190} height={36} rx={8} className="rs-loopnode" />
      <text x={FX(2) + 65} y={F.loop + 23} textAnchor="middle" className="rs-loop-t">escapes：本该哪关抓到？</text>
      <line x1={FX(5) - 2} y1={F.loop + 18} x2={FX(3) + 192} y2={F.loop + 18} className="rs-e rs-loop-e" markerEnd="url(#rs-a-amber)" />
      <line x1={FX(3) + 18} y1={F.loop + 18} x2={FX(2) + 162} y2={F.loop + 18} className="rs-e rs-loop-e" markerEnd="url(#rs-a-amber)" />
      <path d={`M${FX(2) - 30},${F.loop + 18} H${FX(1) + 95} V${F.human + 24}`} className="rs-e rs-loop-e" markerEnd="url(#rs-a-amber)" />
      <text x={FX(1) + 101} y={F.loop - 4} className="rs-loop-l">回到最早该拦的那关补检查</text>
    </g>
  </svg>;
}

// ============ 2. 依赖图：点一个节点，看它依赖谁、改了它谁要重做或重审 ============
const DX = (c: number): number => 20 + c * 152;
const DY = (r: number): number => 20 + r * 72;
const NW = 128; const NH = 46;

function depPath(a: DepNode, b: DepNode, k: number): string {
  if (a.col === b.col) {
    const x = DX(a.col) + NW / 2; return `M${x},${DY(a.row) + NH} V${DY(b.row) - 2}`;
  }
  const x1 = DX(a.col) + NW; const y1 = DY(a.row) + NH / 2; const x2 = DX(b.col) - 2; const y2 = DY(b.row) + NH / 2;
  if (Math.abs(b.col - a.col) <= 1) return `M${x1},${y1} C${x1 + 14},${y1} ${x2 - 14},${y2} ${x2},${y2}`;
  const ch = DY(Math.min(a.row, b.row)) + NH + 13 + (k % 3) * 3;
  return `M${x1},${y1} C${x1 + 12},${y1} ${x1 + 12},${ch} ${x1 + 22},${ch} H${x2 - 22} C${x2 - 10},${ch} ${x2 - 12},${y2} ${x2},${y2}`;
}

export function DependencyDiagram(): JSX.Element {
  const [sel, setSel] = useState<string | null>("filming");
  const c = useMemo(() => (sel ? closure(sel) : null), [sel]);
  const byId = Object.fromEntries(DEP_NODES.map(n => [n.id, n]));
  const W = DX(7) + NW + 20;
  const state = (id: string): string => !c ? "" : id === sel ? " rs-d-sel" : c.down.has(id) ? " rs-d-down" : c.up.has(id) ? " rs-d-up" : " rs-dim";
  const node = sel ? byId[sel] : null;
  const downList = c ? DEP_NODES.filter(n => c.down.has(n.id)) : [];
  return <div>
    <div className="rs-scroll">
      <svg className="rs-svg" viewBox={`0 0 ${W} 330`} width={W} height={330} role="img" aria-label="产物依赖图">
        <Arrows />
        <text x={DX(0)} y={DY(4) + 18} className="rs-band">输入资产</text>
        <text x={DX(4)} y={DY(4) + 18} className="rs-band">结论（绑定产物哈希，产物一变就作废）</text>
        {DEP_EDGES.map((e, k) => {
          const a = byId[e.from]; const b = byId[e.to];
          const lit = !c ? "" : (e.from === sel || c.down.has(e.from)) && c.down.has(e.to) ? " rs-de-down"
            : c.up.has(e.from) && (c.up.has(e.to) || e.to === sel) ? " rs-de-up" : " rs-de-dim";
          const marker = e.kind === "gates" ? "url(#rs-a-green)" : lit === " rs-de-down" ? "url(#rs-a-amber)" : lit === " rs-de-up" ? "url(#rs-a-blue)" : "url(#rs-a)";
          return <path key={k} d={depPath(a, b, k)} className={`rs-de rs-de-${e.kind}${lit}`} markerEnd={marker} />;
        })}
        {DEP_NODES.map(n => <g key={n.id} className={`rs-dn rs-dn-${n.kind}${state(n.id)}`} onClick={() => setSel(n.id === sel ? null : n.id)}
          role="button" tabIndex={0} onKeyDown={e => { if (e.key === "Enter" || e.key === " ") setSel(n.id === sel ? null : n.id); }}>
          <rect x={DX(n.col)} y={DY(n.row)} width={NW} height={NH} rx={n.kind === "verdict" ? 18 : 7} />
          <text x={DX(n.col) + NW / 2} y={DY(n.row) + 19} textAnchor="middle" className="rs-dn-t">{n.label}</text>
          <text x={DX(n.col) + NW / 2} y={DY(n.row) + 35} textAnchor="middle" className="rs-dn-s">{n.sub}</text>
          {n.isNew ? <text x={DX(n.col) + NW - 4} y={DY(n.row) - 4} textAnchor="end" className="rs-newmark">NEW</text> : null}
        </g>)}
      </svg>
    </div>
    <p className="rs-caption" aria-live="polite">{node
      ? <>改了<strong>「{node.label}」</strong>，要重做或重审：{downList.length ? downList.map(n => n.label).join(" → ") : "（没有下游）"}。它依赖：{c && c.up.size ? DEP_NODES.filter(n => c.up.has(n.id)).map(n => n.label).join("、") : "（无）"}。</>
      : "点任意节点，看它依赖谁、改了它哪些产物和结论要重来。"}</p>
  </div>;
}

// ============ 3. 审稿人泳道：谁在哪几关上岗 ============
export function LaneDiagram({ selected, onSelect }: { selected: LawId | null; onSelect: (l: LawId | null) => void }): JSX.Element {
  const L = 170; const CW = 140; const RH = 38; const top = 44;
  const W = L + STAGES.length * CW + 20; const H = top + LAWS.length * RH + 12;
  const cx = (i: number): number => L + i * CW + CW / 2;
  return <svg className="rs-svg" viewBox={`0 0 ${W} ${H}`} width={W} height={H} role="img" aria-label="审稿人泳道图">
    {STAGES.map((s, i) => <g key={s.id}>
      <text x={cx(i)} y={22} textAnchor="middle" className="rs-lane-h">{s.no} {s.name}</text>
      <line x1={cx(i)} y1={32} x2={cx(i)} y2={H - 8} className="rs-lane-grid" />
    </g>)}
    {LAWS.map((l, r) => {
      const y = top + r * RH + RH / 2; const idx = l.stages.map(s => STAGES.findIndex(st => st.id === s));
      const lo = Math.min(...idx); const hi = Math.max(...idx); const on = selected === l.id;
      return <g key={l.id} className={`rs-lane${on ? " rs-on" : ""}${selected && !on ? " rs-dim" : ""}`}
        onClick={() => onSelect(on ? null : l.id)} role="button" tabIndex={0}
        onKeyDown={e => { if (e.key === "Enter" || e.key === " ") onSelect(on ? null : l.id); }}>
        <rect x={4} y={y - RH / 2 + 3} width={W - 8} height={RH - 6} rx={6} className="rs-lane-bg" />
        <circle cx={18} cy={y} r={6} fill={l.color} />
        <text x={32} y={y + 5} className="rs-lane-n">{l.name}{l.isNew ? " ·新" : ""}</text>
        <line x1={cx(lo)} y1={y} x2={cx(hi)} y2={y} stroke={l.color} strokeWidth={3} strokeOpacity={0.35} />
        {STAGES.map((s, i) => idx.includes(i)
          ? <circle key={s.id} cx={cx(i)} cy={y} r={9} fill={l.color}><title>{`${l.name} @ ${s.name}`}</title></circle>
          : <circle key={s.id} cx={cx(i)} cy={y} r={2.5} className="rs-lane-off" />)}
      </g>;
    })}
  </svg>;
}

// ============ 4. 结论判定树：多严重 → 本该哪关 → 怎么处理 ============
function Diamond({ cx, cy, lines, w = 70, h = 32 }: { cx: number; cy: number; lines: string[]; w?: number; h?: number }): JSX.Element {
  return <g><polygon points={`${cx},${cy - h} ${cx + w},${cy} ${cx},${cy + h} ${cx - w},${cy}`} className="rs-q" />
    <Lines x={cx} y={cy + (lines.length === 1 ? 4 : -3)} lines={lines} cls="rs-q-t" lh={14} /></g>;
}
function Box({ x, y, w, h, lines, cls }: { x: number; y: number; w: number; h: number; lines: string[]; cls: string }): JSX.Element {
  return <g><rect x={x} y={y} width={w} height={h} rx={7} className={cls} />
    <Lines x={x + w / 2} y={y + h / 2 + (lines.length === 1 ? 4 : -3)} lines={lines} cls="rs-box-t" lh={14} /></g>;
}
function Edge({ d, label, lx, ly, cls = "" }: { d: string; label?: string; lx?: number; ly?: number; cls?: string }): JSX.Element {
  return <g><path d={d} className={`rs-e ${cls}`} markerEnd="url(#rs-a)" />{label ? <text x={lx} y={ly} className="rs-yn">{label}</text> : null}</g>;
}

export function VerdictTree(): JSX.Element {
  return <svg className="rs-svg" viewBox="0 0 1290 330" width={1290} height={330} role="img" aria-label="结论判定树">
    <Arrows />
    <text x={20} y={22} className="rs-band">一 · 多严重</text>
    <text x={760} y={22} className="rs-band">二 · 本该哪关抓到 → 怎么处理</text>
    <Box x={10} y={146} w={112} h={44} lines={["一条发现", "带秒数 / 格子证据"]} cls="rs-box" />
    <Edge d="M122,168 H146" />
    <Box x={148} y={146} w={112} h={44} lines={["归到一条法则", "物理 / 人物 / …"]} cls="rs-box" />
    <Edge d="M260,168 H292" />
    <Diamond cx={364} cy={168} lines={["画面或动作", "错了？"]} />
    <Edge d="M364,136 V80 H420" label="是" lx={370} ly={110} />
    <Diamond cx={492} cy={80} lines={["剪掉后", "拍点还在？"]} />
    <Edge d="M364,200 V256 H420" label="否" lx={370} ly={232} />
    <Diamond cx={492} cy={256} lines={["观众会看错", "或看不懂？"]} />
    <Edge d="M562,80 H580 V46 H596" label="是" lx={566} ly={60} />
    <Box x={598} y={30} w={96} h={34} lines={["可剪"]} cls="rs-sev rs-sev-cut" />
    <Edge d="M562,80 H580 V114 H596" label="否" lx={566} ly={106} />
    <Box x={598} y={98} w={96} h={34} lines={["重出"]} cls="rs-sev rs-sev-redo" />
    <Edge d="M562,256 H580 V222 H596" label="是" lx={566} ly={236} />
    <Box x={598} y={206} w={96} h={34} lines={["重出 / 改上游"]} cls="rs-sev rs-sev-redo" />
    <Edge d="M562,256 H580 V290 H596" label="否" lx={566} ly={282} />
    <Box x={598} y={274} w={96} h={34} lines={["记录"]} cls="rs-sev rs-sev-note" />
    {[47, 115, 223, 291].map(y => <path key={y} d={`M694,${y} C720,${y} 706,168 736,168`} className="rs-e rs-faint" />)}
    <Edge d="M736,168 H748" />
    <Diamond cx={822} cy={168} lines={["上游文字里", "就有这个错？"]} w={72} />
    <Edge d="M822,136 V70 H900" label="是" lx={828} ly={104} />
    <Box x={902} y={46} w={196} h={48} lines={["本该 ① 故事稿 / ② 分镜抓到", "→ 改故事或分镜，再重出"]} cls="rs-box rs-origin" />
    <Edge d="M894,168 H940" label="否" lx={904} ly={160} />
    <Diamond cx={1012} cy={168} lines={["prompt / 首帧", "有歧义？"]} w={72} />
    <Edge d="M1012,200 V250 H1040" label="否" lx={1018} ly={232} />
    <Box x={1042} y={226} w={200} h={48} lines={["④ 模型随机出错", "→ 只重出这一条"]} cls="rs-box rs-origin" />
    <Edge d="M1084,168 H1110 V128 H1124" label="是" lx={1090} ly={154} />
    <Box x={1126} y={104} w={150} h={48} lines={["本该 ③ 抓到", "→ 改 prompt 再重出"]} cls="rs-box rs-origin" />
    <text x={902} y={316} className="rs-caption-svg">每条结论都写进 qc.json：法则 · 严重度 · 本该哪关 · 处理 · 证据 · 审稿人（模型）</text>
  </svg>;
}

// ============ 5. 漏网案例追踪 ============
export function CaseDiagram(): JSX.Element {
  const [id, setId] = useState(CASES[0].id);
  const k = CASES.find(c => c.id === id) ?? CASES[0];
  const cols: (StageId | "user")[] = [...STAGES.map(s => s.id), "user"];
  const CW = 168; const X = (i: number): number => 30 + i * CW + CW / 2;
  const W = 30 + cols.length * CW + 10;
  const oi = cols.indexOf(k.origin); const ci = cols.indexOf(k.caughtAt);
  const firstCatch = cols.findIndex(c => c !== "user" && k.newCatch[c as StageId]);
  const yR = 92; const yG = 256;
  return <div>
    <div className="rs-tabs" role="tablist">{CASES.map(c => <button key={c.id} role="tab" aria-selected={c.id === id} className={c.id === id ? "rs-tab rs-tab-on" : "rs-tab"} onClick={() => setId(c.id)}>
      {c.title}<small>{c.shot}</small></button>)}</div>
    <div className="rs-scroll">
      <svg className="rs-svg" viewBox={`0 0 ${W} 360`} width={W} height={360} role="img" aria-label={`案例：${k.title}`}>
        <Arrows />
        {cols.map((c, i) => {
          const st = STAGES.find(s => s.id === c);
          return <g key={c}><text x={X(i)} y={24} textAnchor="middle" className="rs-lane-h">{st ? `${st.no} ${st.name}` : "用户"}</text>
            <line x1={X(i)} y1={34} x2={X(i)} y2={340} className="rs-lane-grid" /></g>;
        })}
        <text x={10} y={yR - 30} className="rs-band rs-red-t">现在：错误从哪关进来、闯过了哪几关</text>
        <path d={`M${X(oi)},${yR} H${X(ci) - 16}`} className="rs-e rs-trace" markerEnd="url(#rs-a-red)" />
        <circle cx={X(oi)} cy={yR} r={13} className="rs-origin-dot" /><text x={X(oi)} y={yR + 5} textAnchor="middle" className="rs-x">✕</text>
        <Lines x={X(oi)} y={yR + 32} lines={wrap(k.originWhy, 11)} cls="rs-why rs-red-t" />
        {cols.map((c, i) => i > oi && i < ci && c !== "user" && k.passed[c as StageId] ? <g key={c}>
          <circle cx={X(i)} cy={yR} r={8} className="rs-pass-dot" />
          <Lines x={X(i)} y={yR + 28} lines={wrap(k.passed[c as StageId] as string, 11)} cls="rs-why" />
        </g> : null)}
        <circle cx={X(ci)} cy={yR} r={14} className="rs-caught-dot" />
        <text x={X(ci)} y={yR + 5} textAnchor="middle" className="rs-x rs-x-dark">!</text>
        <Lines x={X(ci)} y={yR + 34} lines={wrap(`被${k.caughtBy}抓到`, 9)} cls="rs-why rs-strong" />
        <line x1={20} y1={yG - 72} x2={W - 10} y2={yG - 72} className="rs-split" />
        <text x={10} y={yG - 52} className="rs-band rs-green-t">改进后：新检查在哪关拦下（最早那关返工最便宜）</text>
        {cols.map((c, i) => c !== "user" && k.newCatch[c as StageId] ? <g key={c}>
          <circle cx={X(i)} cy={yG} r={i === firstCatch ? 14 : 9} className={i === firstCatch ? "rs-catch-dot rs-catch-first" : "rs-catch-dot"} />
          <text x={X(i)} y={yG + 5} textAnchor="middle" className="rs-x">✓</text>
          <Lines x={X(i)} y={yG + 32} lines={wrap(k.newCatch[c as StageId] as string, 11)} cls="rs-why rs-green-t" />
          {i === firstCatch ? <text x={X(i)} y={yG - 22} textAnchor="middle" className="rs-first">最早拦截点</text> : null}
        </g> : null)}
      </svg>
    </div>
  </div>;
}
