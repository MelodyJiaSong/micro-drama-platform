/** The evidence sparkline on a 系列 card: one bar per measured video, sorted by
 *播放量 desc. Two encodings, no chart library and no thumbnails (CSP blocks
 * external images anyway): bar height = 播放量 on a log-ish scale shared by the
 * whole dataset (so cards compare, and the floor is still a visible stub), and
 * the dot under each bar = that video's 点赞率. The dashed line is the dataset's
 * 播放量 threshold — bars above it cleared the bar the quadrant uses. */
import { formatCount, formatDate, formatRate, type ResearchVideo } from "../lib/researchApi";

export interface ResearchSeriesGridSparkProps {
  videos: ResearchVideo[];
  /** dataset-wide 播放量 scaler → 0..1 (already carries the visible floor) */
  viewScale: (views: number) => number;
  /** dataset-wide 点赞率 scaler → 0..1 */
  rateScale: (rate: number) => number;
  /** dataset median of series median 播放量, drawn as the reference line */
  viewsThreshold: number;
}

const WIDTH = 240;
const BAR_H = 42;
const DOT_H = 9;
const GAP = 3;

export function ResearchSeriesGridSpark({
  videos,
  viewScale,
  rateScale,
  viewsThreshold,
}: ResearchSeriesGridSparkProps): JSX.Element {
  if (videos.length === 0) {
    return <p className="research-sg-spark-empty">该系列暂无实测样本。</p>;
  }
  const ordered = [...videos].sort((a, b) => b.view_count - a.view_count);
  const top = ordered[0];
  const floor = ordered[ordered.length - 1];
  const barW = (WIDTH - GAP * (ordered.length - 1)) / ordered.length;
  const refY = BAR_H - Math.min(BAR_H, viewScale(viewsThreshold) * BAR_H);

  return (
    <div className="research-sg-spark-wrap">
      <svg
        className="research-sg-spark"
        viewBox={`0 0 ${WIDTH} ${BAR_H + DOT_H}`}
        role="img"
        aria-label={`${ordered.length} 条实测样本：播放量从 ${formatCount(top.view_count)} 到 ${formatCount(
          floor.view_count,
        )}，柱高为播放量、柱下圆点为点赞率，虚线为全表播放量门槛 ${formatCount(viewsThreshold)}`}
      >
        <line
          className="research-sg-spark-ref"
          x1={0}
          y1={refY}
          x2={WIDTH}
          y2={refY}
        />
        {ordered.map((v, i) => {
          const h = Math.max(2, viewScale(v.view_count) * BAR_H);
          const rate = rateScale(v.like_rate);
          const x = i * (barW + GAP);
          return (
            <g key={v.video_id}>
              <title>
                {`${v.title}\n${formatCount(v.view_count)} 播放 · ${formatRate(v.like_rate)} 点赞率 · ${formatDate(
                  v.upload_date,
                )}`}
              </title>
              <rect
                className="research-sg-spark-bar"
                x={x}
                y={BAR_H - h}
                width={barW}
                height={h}
                fillOpacity={0.32 + 0.68 * rate}
              />
              <circle
                className="research-sg-spark-dot"
                cx={x + barW / 2}
                cy={BAR_H + DOT_H / 2}
                r={1 + 2.4 * rate}
              />
            </g>
          );
        })}
      </svg>
      <p className="research-sg-spark-legend">
        <span>高 {formatCount(top.view_count)}</span>
        <span className="research-sg-spark-legend-mid">柱＝播放量 · 点＝点赞率</span>
        <span>低 {formatCount(floor.view_count)}</span>
      </p>
    </div>
  );
}
