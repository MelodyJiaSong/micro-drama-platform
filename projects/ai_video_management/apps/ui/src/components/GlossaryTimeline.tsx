import { categoryOf, termById, type Glossary, type GlossaryTimeline as Timeline } from "../lib/glossary";

const LABEL_W = 132;
const WIDTH = 1000;
const ROW_H = 34;
const TOP = 34;
const CHAR_W = 12;

/** Intervals on one time axis: nested and misaligned boundaries are the point. */
export function GlossaryTimeline({ glossary, timeline, selected, onSelect }: {
  glossary: Glossary; timeline: Timeline; selected: string; onSelect: (id: string) => void;
}): JSX.Element {
  const plot = WIDTH - LABEL_W - 12;
  const x = (value: number): number => LABEL_W + (value / timeline.length) * plot;
  const height = TOP + timeline.rows.length * ROW_H + 18;
  const format = (value: number): string => timeline.unit !== "秒" ? String(value)
    : timeline.length <= 120 ? `${value}s` : `${Math.floor(value / 60)}:${String(Math.round(value % 60)).padStart(2, "0")}`;
  return <figure className="glossary-timeline">
    <figcaption><strong>{timeline.zh}</strong><span>{timeline.note}</span></figcaption>
    <svg viewBox={`0 0 ${WIDTH} ${height}`} role="img" aria-label={`${timeline.zh}：${timeline.rows.map(row => termById(glossary, row.term)?.zh).join("、")}在同一时间轴上的区间`}>
      {timeline.ticks.map(tick => <g key={tick}>
        <line x1={x(tick)} x2={x(tick)} y1={TOP - 6} y2={height - 14} className="glossary-tick" />
        <text x={x(tick)} y={TOP - 12} textAnchor="middle" className="glossary-tick-label">{format(tick)}</text>
      </g>)}
      {timeline.rows.map((row, index) => {
        const term = termById(glossary, row.term);
        const color = term ? categoryOf(glossary, term)?.color || "#475569" : "#475569";
        const y = TOP + index * ROW_H;
        const active = selected === row.term;
        return <g key={row.term}>
          {active ? <rect x={2} y={y + 1} width={WIDTH - 4} height={ROW_H - 2} rx={5} className="glossary-row-active" /> : null}
          <g className="glossary-row-label" role="button" tabIndex={0} aria-label={`选择术语：${term?.zh}`}
            onClick={() => onSelect(row.term)} onKeyDown={event => { if (event.key === "Enter" || event.key === " ") onSelect(row.term); }}>
            <text x={8} y={y + ROW_H / 2 + 1} dominantBaseline="middle"><tspan fontWeight={600}>{term?.zh}</tspan><tspan dx={6} className="glossary-row-en">{term?.en}</tspan></text>
          </g>
          {row.spans.map(([start, end, label], spanIndex) => {
            const width = Math.max(x(end) - x(start) - 2, 1);
            return <g key={spanIndex}>
              <rect x={x(start) + 1} y={y + 5} width={width} height={ROW_H - 10} rx={4}
                fill={color} fillOpacity={row.example ? 0.12 : 0.18} stroke={color} strokeDasharray={row.example ? "4 3" : undefined} />
              {label && label.length * CHAR_W < width - 6 ? <text x={x(start) + 6} y={y + ROW_H / 2 + 1} dominantBaseline="middle" className="glossary-span-label">{label}</text> : null}
              <title>{`${term?.zh}${label ? `「${label}」` : ""}：${format(start)}–${format(end)}${row.example ? "（示意）" : ""}`}</title>
            </g>;
          })}
          {row.partial ? <text x={WIDTH - 12} y={y + ROW_H / 2 + 1} textAnchor="end" dominantBaseline="middle" className="glossary-row-note">{row.partial}</text> : null}
        </g>;
      })}
      {timeline.markers.map(marker => <g key={`${marker.zh}-${marker.at}`} className="glossary-marker">
        <line x1={x(marker.at)} x2={x(marker.at)} y1={TOP} y2={height - 14} />
        <circle cx={x(marker.at)} cy={TOP} r={4} />
        <text x={x(marker.at) + 5} y={height - 4}>{marker.zh}</text>
        <title>{`${termById(glossary, marker.term)?.zh}：${marker.zh}`}</title>
      </g>)}
    </svg>
  </figure>;
}
