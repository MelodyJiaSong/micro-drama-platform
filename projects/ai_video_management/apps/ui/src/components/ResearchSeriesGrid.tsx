/** 系列 Grid — the browsing + triage surface for the ranked candidate series.
 * Filters and sort live here (client-side; the dataset is 10 rows), the decision
 * controls live on each card and write straight through `onMark`. */
import { useMemo, useState } from "react";
import { ORIENTATION_LABEL, ResearchSeriesGridCard } from "./ResearchSeriesGridCard";
import {
  flattenVideos,
  quadrantOf,
  sortSeries,
  STATUS_LABEL,
  STATUS_ORDER,
  thresholds,
  type ResearchDataset,
  type ResearchSort,
  type ResearchWorkspace,
  type SeriesMark,
  type SeriesStatus,
} from "../lib/researchApi";

type GridSort = ResearchSort | "rating";

const SORTS: Array<{ id: GridSort; label: string }> = [
  { id: "balanced", label: "综合推荐" },
  { id: "views", label: "播放量" },
  { id: "like_rate", label: "点赞率" },
  { id: "replication", label: "翻拍易度" },
  { id: "rating", label: "我的评分" },
];

const SCORES: number[] = [1, 2, 3, 4, 5];

interface Filters {
  q: string;
  orientation: string;
  market: string;
  minScore: number;
  status: SeriesStatus | "all";
  bothOnly: boolean;
}

const EMPTY: Filters = { q: "", orientation: "all", market: "", minScore: 1, status: "all", bothOnly: false };

/** Log-ish scalers shared by every card, so bar heights compare across cards.
 * The 0.08 floor keeps the weakest sample a visible stub instead of nothing. */
function useScales(data: ResearchDataset): {
  viewScale: (views: number) => number;
  rateScale: (rate: number) => number;
} {
  return useMemo(() => {
    const videos = flattenVideos(data);
    const views = videos.map((v) => Math.max(1, v.view_count));
    const rates = videos.map((v) => v.like_rate);
    const lo = Math.log10(1 + Math.min(...views, 1));
    const hi = Math.log10(1 + Math.max(...views, 1));
    const rLo = Math.min(...rates, 0);
    const rHi = Math.max(...rates, 0);
    const clamp = (x: number): number => (Number.isFinite(x) ? Math.min(1, Math.max(0, x)) : 0);
    return {
      viewScale: (n: number) =>
        hi > lo ? 0.08 + 0.92 * clamp((Math.log10(1 + Math.max(1, n)) - lo) / (hi - lo)) : 0.5,
      rateScale: (r: number) => (rHi > rLo ? clamp((r - rLo) / (rHi - rLo)) : 0.5),
    };
  }, [data]);
}

export interface ResearchSeriesGridProps {
  data: ResearchDataset;
  workspace: ResearchWorkspace;
  onOpenSeries: (slug: string) => void;
  onMark: (slug: string, patch: SeriesMark) => void;
  selected: string[];
  onToggleSelect: (slug: string) => void;
}

export function ResearchSeriesGrid({
  data,
  workspace,
  onOpenSeries,
  onMark,
  selected,
  onToggleSelect,
}: ResearchSeriesGridProps): JSX.Element {
  const [filters, setFilters] = useState<Filters>(EMPTY);
  const [sort, setSort] = useState<GridSort>("balanced");

  const th = useMemo(() => thresholds(data), [data]);
  const { viewScale, rateScale } = useScales(data);
  const orientations = useMemo(
    () => Array.from(new Set(data.series.map((s) => s.orientation))),
    [data],
  );

  const patch = (next: Partial<Filters>): void => setFilters((f) => ({ ...f, ...next }));
  const dirty =
    filters.q !== "" ||
    filters.orientation !== "all" ||
    filters.market !== "" ||
    filters.minScore !== 1 ||
    filters.status !== "all" ||
    filters.bothOnly;

  const shown = useMemo(() => {
    const q = filters.q.trim().toLowerCase();
    const market = filters.market.trim().toLowerCase();
    const kept = data.series.filter((s) => {
      if (q && !`${s.name_zh} ${s.name_en} ${s.description}`.toLowerCase().includes(q)) return false;
      if (filters.orientation !== "all" && s.orientation !== filters.orientation) return false;
      if (market && !s.market.toLowerCase().includes(market)) return false;
      if (s.replication.score < filters.minScore) return false;
      if (filters.status !== "all" && (workspace.series[s.slug]?.status ?? "none") !== filters.status) {
        return false;
      }
      if (filters.bothOnly && quadrantOf(s, th) !== "both") return false;
      return true;
    });
    if (sort !== "rating") return sortSeries(kept, sort);
    return [...kept].sort(
      (a, b) =>
        (workspace.series[b.slug]?.rating ?? 0) - (workspace.series[a.slug]?.rating ?? 0) ||
        a.rank - b.rank,
    );
  }, [data, filters, sort, th, workspace]);

  return (
    <div className="research-sg">
      <div className="research-sg-filters">
        <label className="research-sg-field research-sg-search">
          <span>搜索名称 / 描述</span>
          <input
            type="search"
            value={filters.q}
            placeholder="如：短剧、纪录片、music"
            onChange={(e) => patch({ q: e.target.value })}
          />
        </label>

        <label className="research-sg-field">
          <span>形态</span>
          <select value={filters.orientation} onChange={(e) => patch({ orientation: e.target.value })}>
            <option value="all">全部</option>
            {orientations.map((o) => (
              <option key={o} value={o}>
                {ORIENTATION_LABEL[o] ?? o}
              </option>
            ))}
          </select>
        </label>

        <label className="research-sg-field">
          <span>市场关键词</span>
          <input
            type="text"
            value={filters.market}
            placeholder="如：英语、南亚、美国"
            onChange={(e) => patch({ market: e.target.value })}
          />
        </label>

        <label className="research-sg-field">
          <span>翻拍易度 ≥</span>
          <select
            value={String(filters.minScore)}
            onChange={(e) => patch({ minScore: Number(e.target.value) })}
          >
            {SCORES.map((n) => (
              <option key={n} value={n}>
                {n === 1 ? "不限" : `${n} 星以上`}
              </option>
            ))}
          </select>
        </label>

        <label className="research-sg-field">
          <span>状态</span>
          <select
            value={filters.status}
            onChange={(e) => patch({ status: e.target.value as SeriesStatus | "all" })}
          >
            <option value="all">全部</option>
            {STATUS_ORDER.map((s) => (
              <option key={s} value={s}>
                {STATUS_LABEL[s]}
              </option>
            ))}
          </select>
        </label>

        <button
          type="button"
          className="research-sg-toggle"
          aria-pressed={filters.bothOnly}
          onClick={() => patch({ bothOnly: !filters.bothOnly })}
        >
          只看两项都过
        </button>

        <span className="research-sg-spacer" />

        <span className="research-sg-count" aria-live="polite">
          <b>{shown.length}</b> / {data.series.length} 个系列
          {selected.length > 0 ? ` · 已选 ${selected.length} 个对比` : ""}
        </span>

        <button
          type="button"
          className="research-sg-clear"
          disabled={!dirty}
          onClick={() => setFilters(EMPTY)}
        >
          清除筛选
        </button>
      </div>

      <div className="research-sg-sortbar" role="group" aria-label="排序">
        <span>排序：</span>
        {SORTS.map((s) => (
          <button
            key={s.id}
            type="button"
            className="research-sg-sort"
            aria-pressed={sort === s.id}
            onClick={() => setSort(s.id)}
          >
            {s.label}
          </button>
        ))}
      </div>

      {shown.length === 0 ? (
        <p className="research-sg-empty">没有系列符合当前筛选条件。试试放宽翻拍易度，或清除筛选。</p>
      ) : (
        <div className="research-sg-cards">
          {shown.map((s) => (
            <ResearchSeriesGridCard
              key={s.slug}
              series={s}
              mark={workspace.series[s.slug] ?? {}}
              quadrant={quadrantOf(s, th)}
              selected={selected.includes(s.slug)}
              viewScale={viewScale}
              rateScale={rateScale}
              viewsThreshold={th.views}
              onOpenSeries={onOpenSeries}
              onMark={onMark}
              onToggleSelect={onToggleSelect}
            />
          ))}
        </div>
      )}
    </div>
  );
}
