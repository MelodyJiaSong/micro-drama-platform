/** One triage card in the 系列 Grid: the numbers that decide, the evidence
 * sparkline, and every decision control (状态 / 评分 / 对比 / 详情) inline — so the
 * user never has to open a series to rule it in or out. */
import { Rich } from "./ResearchText";
import { ResearchSeriesGridSpark } from "./ResearchSeriesGridSpark";
import {
  formatCount,
  formatRate,
  QUADRANT_LABEL,
  STATUS_LABEL,
  STATUS_ORDER,
  type Quadrant,
  type ResearchSeries,
  type SeriesMark,
  type SeriesStatus,
} from "../lib/researchApi";

export const ORIENTATION_LABEL: Record<string, string> = {
  longform: "长视频",
  shorts: "竖屏 Shorts",
  both: "长视频 + 竖屏",
};

const RATING_STARS: number[] = [1, 2, 3, 4, 5];

export interface ResearchSeriesGridCardProps {
  series: ResearchSeries;
  mark: SeriesMark;
  quadrant: Quadrant;
  selected: boolean;
  viewScale: (views: number) => number;
  rateScale: (rate: number) => number;
  viewsThreshold: number;
  onOpenSeries: (slug: string) => void;
  onMark: (slug: string, patch: SeriesMark) => void;
  onToggleSelect: (slug: string) => void;
}

export function ResearchSeriesGridCard({
  series,
  mark,
  quadrant,
  selected,
  viewScale,
  rateScale,
  viewsThreshold,
  onOpenSeries,
  onMark,
  onToggleSelect,
}: ResearchSeriesGridCardProps): JSX.Element {
  const { slug, stats, replication } = series;
  const status: SeriesStatus = mark.status ?? "none";
  const rating = mark.rating ?? 0;
  const className = [
    "research-sg-card",
    `research-sg-card-${status}`,
    selected ? "research-sg-card-selected" : "",
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <article className={className} aria-label={`第 ${series.rank} 名 ${series.name_zh}`}>
      <header className="research-sg-head">
        <span className="research-sg-rank">#{series.rank}</span>
        <span className="research-sg-names">
          <span className="research-sg-zh">{series.name_zh}</span>
          <span className="research-sg-en" title={series.name_en}>{series.name_en}</span>
        </span>
        <label className="research-sg-compare">
          <input
            type="checkbox"
            checked={selected}
            onChange={() => onToggleSelect(slug)}
            aria-label={`把「${series.name_zh}」加入对比`}
          />
          对比
        </label>
      </header>

      <div className="research-sg-metrics">
        <span className="research-sg-metric">
          <b>{formatCount(stats.median_views)}</b>
          <small>播放中位</small>
        </span>
        <span className="research-sg-metric">
          <b className="research-sg-green">{formatRate(stats.median_like_rate)}</b>
          <small>点赞率中位</small>
        </span>
        <span className="research-sg-metric">
          <b className="research-sg-score" aria-label={`翻拍易度 ${replication.score} / 5`}>
            {"★".repeat(replication.score)}
            {"☆".repeat(5 - replication.score)}
          </b>
          <small>翻拍易度</small>
        </span>
      </div>

      <div className="research-sg-chips">
        <span className={`research-sg-chip research-sg-q-${quadrant}`}>{QUADRANT_LABEL[quadrant]}</span>
        <span className="research-sg-chip">{ORIENTATION_LABEL[series.orientation] ?? series.orientation}</span>
        <span className="research-sg-chip research-sg-chip-trunc" title={series.market}>
          <Rich text={series.market} />
        </span>
        <span className="research-sg-chip research-sg-chip-trunc" title={series.typical_length}>
          <Rich text={series.typical_length} />
        </span>
        <span
          className="research-sg-chip research-sg-chip-trunc research-sg-chip-hours"
          title={replication.hours_per_episode}
        >
          <Rich text={replication.hours_per_episode} />
        </span>
      </div>

      <ResearchSeriesGridSpark
        videos={series.videos}
        viewScale={viewScale}
        rateScale={rateScale}
        viewsThreshold={viewsThreshold}
      />

      <p className="research-sg-desc">
        <Rich text={series.description} />
      </p>

      <div className="research-sg-foot">
        <span className="research-sg-statuses" role="group" aria-label={`「${series.name_zh}」的状态`}>
          {STATUS_ORDER.map((s) => (
            <button
              key={s}
              type="button"
              className={`research-sg-status research-sg-status-${s}`}
              aria-pressed={status === s}
              onClick={() => onMark(slug, { status: s })}
            >
              {STATUS_LABEL[s]}
            </button>
          ))}
        </span>

        <span className="research-sg-stars" role="group" aria-label={`「${series.name_zh}」的评分`}>
          {RATING_STARS.map((n) => (
            <button
              key={n}
              type="button"
              className={n <= rating ? "research-sg-star research-sg-star-on" : "research-sg-star"}
              aria-pressed={n <= rating}
              aria-label={n === rating ? `清除评分（当前 ${rating} 星）` : `评 ${n} 星`}
              onClick={() => onMark(slug, { rating: n === rating ? 0 : n })}
            >
              {n <= rating ? "★" : "☆"}
            </button>
          ))}
        </span>

        {mark.note ? (
          <span className="research-sg-note" title={mark.note}>
            ✎ {mark.note}
          </span>
        ) : null}

        <button
          type="button"
          className="research-sg-open"
          onClick={() => onOpenSeries(slug)}
          aria-label={`查看「${series.name_zh}」详情`}
        >
          详情 →
        </button>
      </div>
    </article>
  );
}
