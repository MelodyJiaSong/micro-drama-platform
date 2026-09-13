/** The dashboard's centrepiece: every candidate series plotted as
 * 中位播放 (log X) × 中位点赞率 (linear Y), cut by the dataset's own medians into the
 * four decision quadrants. The picture it has to make is that the highest-view
 * series are NOT the high-like-rate ones — so the two extremes are annotated
 * in place and the crosshairs are labelled with their actual values. */
import {
  H,
  PH,
  PW,
  W,
  X0,
  X1,
  Y0,
  Y1,
  buildScale,
  type Callout,
} from "./ResearchScatterScale";
import {
  QUADRANT_LABEL,
  STATUS_LABEL,
  formatCount,
  formatRate,
  quadrantOf,
  type Quadrant,
  type ResearchSeries,
  type ResearchWorkspace,
  type SeriesStatus,
  type Thresholds,
} from "../lib/researchApi";

const QUAD_FILL: Record<Quadrant, string> = {
  both: "var(--tint-a)",
  views_only: "var(--bg-toolbar)",
  likes_only: "var(--tint-q)",
  neither: "var(--bg-sidebar)",
};

const LEGEND_STATUS: SeriesStatus[] = ["shortlist", "doing", "none", "rejected"];

interface Dot {
  slug: string;
  rank: number;
  status: SeriesStatus;
  quadrant: Quadrant;
  x: number;
  y: number;
  r: number;
  tip: string;
  callout: Callout | null;
}

export interface ResearchScatterProps {
  series: ResearchSeries[];
  workspace: ResearchWorkspace;
  limits: Thresholds;
  onOpenSeries: (slug: string) => void;
}

export function ResearchScatter({
  series,
  workspace,
  limits,
  onOpenSeries,
}: ResearchScatterProps): JSX.Element {
  if (series.length === 0) return <p className="muted">该数据集没有可作图的系列。</p>;

  const g = buildScale(series, limits);
  const topViews = series.reduce((a, b) => (b.stats.median_views > a.stats.median_views ? b : a));
  const topRate = series.reduce((a, b) =>
    b.stats.median_like_rate > a.stats.median_like_rate ? b : a,
  );
  const same = topViews.slug === topRate.slug;

  const noteFor = (s: ResearchSeries): string | null => {
    if (same && s.slug === topViews.slug) return "播放·赞率双第一";
    if (s.slug === topViews.slug) return `播放最高 ${formatCount(s.stats.median_views)}`;
    if (s.slug === topRate.slug) return `赞率最高 ${formatRate(s.stats.median_like_rate)}`;
    return null;
  };

  const dots: Dot[] = series.map((s) => {
    const status = workspace.series[s.slug]?.status ?? "none";
    const quadrant = quadrantOf(s, limits);
    const x = g.sx(s.stats.median_views);
    const y = g.sy(s.stats.median_like_rate);
    const r = 4.5 + s.replication.score * 2;
    const note = noteFor(s);
    return {
      slug: s.slug,
      rank: s.rank,
      status,
      quadrant,
      x,
      y,
      r,
      tip:
        `#${s.rank} ${s.name_zh}｜中位播放 ${formatCount(s.stats.median_views)}` +
        `｜中位赞率 ${formatRate(s.stats.median_like_rate)}｜复刻 ${s.replication.score}/5` +
        `｜${QUADRANT_LABEL[quadrant]}｜${STATUS_LABEL[status]}`,
      callout: note ? g.callout(note, x, y, r) : null,
    };
  });

  const counts = dots.reduce<Record<Quadrant, number>>(
    (acc, d) => ({ ...acc, [d.quadrant]: acc[d.quadrant] + 1 }),
    { both: 0, views_only: 0, likes_only: 0, neither: 0 },
  );

  const quads: Array<{ q: Quadrant; box: [number, number, number, number]; lx: number; ly: number; anchor: "start" | "end" }> = [
    { q: "likes_only", box: [X0, Y0, g.tx - X0, g.ty - Y0], lx: X0 + 8, ly: Y0 + 15, anchor: "start" },
    { q: "both", box: [g.tx, Y0, X1 - g.tx, g.ty - Y0], lx: X1 - 8, ly: Y0 + 15, anchor: "end" },
    { q: "neither", box: [X0, g.ty, g.tx - X0, Y1 - g.ty], lx: X0 + 8, ly: Y1 - 8, anchor: "start" },
    { q: "views_only", box: [g.tx, g.ty, X1 - g.tx, Y1 - g.ty], lx: X1 - 8, ly: Y1 - 8, anchor: "end" },
  ];

  return (
    <div className="research-scatter">
      <div className="research-scatter-plot">
        <svg
          viewBox={`0 0 ${W} ${H}`}
          className="research-scatter-svg"
          role="img"
          aria-label={`中位播放 × 中位点赞率 四象限散点图，共 ${series.length} 个系列；播放中位线 ${formatCount(limits.views)}，赞率中位线 ${formatRate(limits.likeRate)}。`}
        >
          {quads.map((q) => (
            <g key={q.q}>
              <rect
                x={q.box[0]}
                y={q.box[1]}
                width={q.box[2]}
                height={q.box[3]}
                fill={QUAD_FILL[q.q]}
                fillOpacity={0.62}
              />
              <text x={q.lx} y={q.ly} textAnchor={q.anchor} className="research-scatter-quad">
                {QUADRANT_LABEL[q.q]} · {counts[q.q]}
              </text>
            </g>
          ))}

          {g.xTicks.map((t) => (
            <g key={`x${t}`}>
              <line x1={g.sx(t)} y1={Y0} x2={g.sx(t)} y2={Y1} className="research-scatter-grid" />
              <text x={g.sx(t)} y={Y1 + 16} textAnchor="middle" className="research-scatter-tick">
                {formatCount(t)}
              </text>
            </g>
          ))}
          {g.yTicks.map((t) => (
            <g key={`y${t}`}>
              <line x1={X0} y1={g.sy(t)} x2={X1} y2={g.sy(t)} className="research-scatter-grid" />
              <text x={X0 - 8} y={g.sy(t) + 4} textAnchor="end" className="research-scatter-tick">
                {formatRate(t)}
              </text>
            </g>
          ))}

          <line x1={g.tx} y1={Y0} x2={g.tx} y2={Y1} className="research-scatter-median" />
          <line x1={X0} y1={g.ty} x2={X1} y2={g.ty} className="research-scatter-median" />
          <text x={g.tx} y={Y1 + 34} textAnchor="middle" className="research-scatter-medlabel">
            中位播放 {formatCount(limits.views)}
          </text>
          <text x={X1 - 2} y={g.ty - 6} textAnchor="end" className="research-scatter-medlabel">
            中位赞率 {formatRate(limits.likeRate)}
          </text>
          <rect x={X0} y={Y0} width={PW} height={PH} fill="none" className="research-scatter-frame" />

          {dots.map((d) => (
            <g key={d.slug} className={`research-dot research-dot-${d.status}`}>
              <title>{d.tip}</title>
              <circle cx={d.x} cy={d.y} r={d.r} />
              <text x={d.x} y={d.y + 3.5} textAnchor="middle" className="research-dot-rank">
                {d.rank}
              </text>
              {d.callout ? (
                <text
                  x={d.callout.x}
                  y={d.callout.y}
                  textAnchor={d.callout.anchor}
                  className="research-scatter-callout"
                >
                  {d.callout.text}
                </text>
              ) : null}
            </g>
          ))}

          <text x={X0 + PW / 2} y={H - 6} textAnchor="middle" className="research-scatter-axis">
            中位播放（对数轴）
          </text>
          <text
            x={-(Y0 + PH / 2)}
            y={14}
            transform="rotate(-90)"
            textAnchor="middle"
            className="research-scatter-axis"
          >
            中位点赞率
          </text>
        </svg>

        {dots.map((d) => (
          <button
            key={d.slug}
            type="button"
            className="research-dot-hit"
            style={{
              left: `${(d.x / W) * 100}%`,
              top: `${(d.y / H) * 100}%`,
              width: `${((d.r * 2) / W) * 100}%`,
              height: `${((d.r * 2) / H) * 100}%`,
            }}
            title={d.tip}
            aria-label={`打开 ${d.tip}`}
            onClick={() => onOpenSeries(d.slug)}
          />
        ))}
      </div>

      <ul className="research-scatter-legend">
        {LEGEND_STATUS.map((s) => (
          <li key={s}>
            <span className={`research-dot-swatch research-dot-${s}`} aria-hidden="true" />
            {STATUS_LABEL[s]}
          </li>
        ))}
        <li className="research-scatter-legend-size">
          <span className="research-dot-swatch research-dot-size-s" aria-hidden="true" />
          <span className="research-dot-swatch research-dot-size-l" aria-hidden="true" />
          圆点大小 = 复刻可行度 1–5
        </li>
      </ul>
    </div>
  );
}
