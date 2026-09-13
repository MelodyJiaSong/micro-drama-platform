/** Filter bar for the 样本库 explorer. Owns the filter *shape* (so the table and
 * the toolbar agree on it) but no data — the explorer does all the matching. */
import { Rich } from "./ResearchText";
import { formatCount, type ResearchDataset } from "../lib/researchApi";

export type LayoutFilter = "all" | "vertical" | "horizontal";

export interface ExplorerFilters {
  query: string;
  series: string[];
  layout: LayoutFilter;
  bookmarkedOnly: boolean;
  minViews: number;
  minLikeRate: string;
  from: string;
  to: string;
}

export const EMPTY_FILTERS: ExplorerFilters = {
  query: "",
  series: [],
  layout: "all",
  bookmarkedOnly: false,
  minViews: 0,
  minLikeRate: "",
  from: "",
  to: "",
};

export function filtersActive(f: ExplorerFilters): boolean {
  return (
    f.query.trim() !== "" ||
    f.series.length > 0 ||
    f.layout !== "all" ||
    f.bookmarkedOnly ||
    f.minViews > 0 ||
    f.minLikeRate.trim() !== "" ||
    f.from !== "" ||
    f.to !== ""
  );
}

/** The slider is cubic, not linear: a linear one spends 90% of its travel on the
 * handful of outlier videos above a million views and is useless below that. */
const STEPS = 100;

export function sliderToViews(pos: number, max: number): number {
  return pos <= 0 ? 0 : Math.round(max * (pos / STEPS) ** 3);
}

function viewsToSlider(views: number, max: number): number {
  if (views <= 0 || max <= 0) return 0;
  return Math.min(STEPS, Math.round(STEPS * Math.cbrt(views / max)));
}

const LAYOUTS: { key: LayoutFilter; label: string }[] = [
  { key: "all", label: "全部" },
  { key: "vertical", label: "只看竖屏" },
  { key: "horizontal", label: "只看横屏" },
];

export interface ResearchVideoExplorerToolbarProps {
  data: ResearchDataset;
  filters: ExplorerFilters;
  seriesCounts: Record<string, number>;
  shown: number;
  total: number;
  maxViews: number;
  dateBounds: { from: string; to: string };
  onChange: (patch: Partial<ExplorerFilters>) => void;
  onReset: () => void;
}

export function ResearchVideoExplorerToolbar({
  data,
  filters,
  seriesCounts,
  shown,
  total,
  maxViews,
  dateBounds,
  onChange,
  onReset,
}: ResearchVideoExplorerToolbarProps): JSX.Element {
  const toggleSeries = (slug: string): void => {
    onChange({
      series: filters.series.includes(slug)
        ? filters.series.filter((s) => s !== slug)
        : [...filters.series, slug],
    });
  };

  return (
    <div className="research-vx-toolbar">
      <div className="research-vx-line">
        <input
          type="search"
          className="research-vx-input research-vx-search"
          placeholder="搜索标题或频道…"
          aria-label="搜索标题或频道"
          value={filters.query}
          onChange={(e) => onChange({ query: e.target.value })}
        />
        <span className="research-vx-count" aria-live="polite">
          <b>{shown}</b> / {total} 条
        </span>
        <button
          type="button"
          className="research-vx-clear"
          onClick={onReset}
          disabled={!filtersActive(filters)}
        >
          清除
        </button>
      </div>

      <div className="research-vx-line">
        <span className="research-vx-label">系列</span>
        <div className="research-vx-chips" role="group" aria-label="按系列筛选">
          {data.series.map((s) => {
            const on = filters.series.includes(s.slug);
            return (
              <button
                key={s.slug}
                type="button"
                className={on ? "research-vx-chip research-vx-chip-on" : "research-vx-chip"}
                aria-pressed={on}
                title={`#${s.rank} ${s.name_zh}`}
                onClick={() => toggleSeries(s.slug)}
              >
                <span className="research-vx-chip-rank">#{s.rank}</span>
                <span className="research-vx-chip-name">
                  <Rich text={s.name_zh} />
                </span>
                <span className="research-vx-chip-count">{seriesCounts[s.slug] ?? 0}</span>
              </button>
            );
          })}
        </div>
      </div>

      <div className="research-vx-line">
        <div className="research-vx-seg" role="group" aria-label="版式筛选">
          {LAYOUTS.map((l) => (
            <button
              key={l.key}
              type="button"
              className={filters.layout === l.key ? "research-vx-seg-on" : undefined}
              aria-pressed={filters.layout === l.key}
              onClick={() => onChange({ layout: l.key })}
            >
              {l.label}
            </button>
          ))}
        </div>

        <button
          type="button"
          className={
            filters.bookmarkedOnly ? "research-vx-toggle research-vx-toggle-on" : "research-vx-toggle"
          }
          aria-pressed={filters.bookmarkedOnly}
          onClick={() => onChange({ bookmarkedOnly: !filters.bookmarkedOnly })}
        >
          ★ 只看已收藏
        </button>

        <label className="research-vx-label" htmlFor="research-vx-minviews">
          最低播放
          <input
            id="research-vx-minviews"
            type="range"
            className="research-vx-slider"
            min={0}
            max={STEPS}
            step={1}
            value={viewsToSlider(filters.minViews, maxViews)}
            aria-label={`最低播放量 ${formatCount(filters.minViews)}`}
            onChange={(e) => onChange({ minViews: sliderToViews(Number(e.target.value), maxViews) })}
          />
          <input
            type="number"
            className="research-vx-input research-vx-numinput"
            min={0}
            step={1000}
            placeholder="0"
            aria-label="最低播放量（精确值）"
            value={filters.minViews === 0 ? "" : String(filters.minViews)}
            onChange={(e) => {
              const n = Number(e.target.value);
              onChange({ minViews: Number.isFinite(n) && n > 0 ? Math.round(n) : 0 });
            }}
          />
          <span className="research-vx-readout">{formatCount(filters.minViews)}</span>
        </label>

        <label className="research-vx-label" htmlFor="research-vx-minrate">
          最低赞率
          <input
            id="research-vx-minrate"
            type="number"
            className="research-vx-input research-vx-numinput"
            min={0}
            max={100}
            step={0.1}
            placeholder="0"
            value={filters.minLikeRate}
            onChange={(e) => onChange({ minLikeRate: e.target.value })}
          />
          %
        </label>

        <label className="research-vx-label" htmlFor="research-vx-from">
          发布
          <input
            id="research-vx-from"
            type="date"
            className="research-vx-input research-vx-date"
            min={dateBounds.from}
            max={dateBounds.to}
            aria-label="发布日期起"
            value={filters.from}
            onChange={(e) => onChange({ from: e.target.value })}
          />
          <span aria-hidden="true">→</span>
          <input
            type="date"
            className="research-vx-input research-vx-date"
            min={dateBounds.from}
            max={dateBounds.to}
            aria-label="发布日期止"
            value={filters.to}
            onChange={(e) => onChange({ to: e.target.value })}
          />
        </label>
      </div>
    </div>
  );
}
