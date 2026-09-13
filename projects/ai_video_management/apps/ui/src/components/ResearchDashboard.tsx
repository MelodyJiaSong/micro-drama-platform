/** 总览 Dashboard — the decision surface of the 选题调研 module: five KPI tiles, the
 * 播放 × 赞率 four-quadrant scatter, a per-quadrant readout, and the dataset's own
 * 口径 / 方法, so no number here is ever read without the caveat attached to it. */
import { useMemo } from "react";
import { ResearchDashboardMethod } from "./ResearchDashboardMethod";
import { ResearchScatter } from "./ResearchScatter";
import { Rich } from "./ResearchText";
import {
  QUADRANT_LABEL,
  STATUS_LABEL,
  flattenVideos,
  formatCount,
  formatRate,
  median,
  quadrantOf,
  thresholds,
  type Quadrant,
  type ResearchDataset,
  type ResearchSeries,
  type ResearchWorkspace,
  type SeriesStatus,
} from "../lib/researchApi";

const QUADRANT_ORDER: Quadrant[] = ["both", "views_only", "likes_only", "neither"];

const QUADRANT_HINT: Record<Quadrant, string> = {
  both: "播放与赞率同时站上全表中位——优先级最高的一档。",
  views_only: "有量没共鸣：播放过线、赞率在中位以下，观众看完不表态。",
  likes_only: "有共鸣没量：赞率过线、播放在中位以下，盘子小但粘性高。",
  neither: "两项都在中位以下；除非工时或护城河另有理由，先放一边。",
};

interface Tile {
  key: string;
  label: string;
  value: string;
  unit?: string;
  caption: string;
  tone?: "work";
}

function statusCounts(series: ResearchSeries[], workspace: ResearchWorkspace): Record<SeriesStatus, number> {
  const out: Record<SeriesStatus, number> = { none: 0, shortlist: 0, doing: 0, rejected: 0 };
  for (const s of series) out[workspace.series[s.slug]?.status ?? "none"] += 1;
  return out;
}

export interface ResearchDashboardProps {
  data: ResearchDataset;
  workspace: ResearchWorkspace;
  onOpenSeries: (slug: string) => void;
}

export function ResearchDashboard({
  data,
  workspace,
  onOpenSeries,
}: ResearchDashboardProps): JSX.Element {
  const limits = useMemo(() => thresholds(data), [data]);
  const flat = useMemo(() => flattenVideos(data), [data]);
  const marks = useMemo(() => statusCounts(data.series, workspace), [data.series, workspace]);

  const tiles = useMemo<Tile[]>(() => {
    const channels = new Set(flat.map((v) => v.channel)).size;
    const totalViews = data.series.reduce((n, s) => n + s.stats.total_views, 0);
    const peak = Math.max(...data.series.map((s) => s.stats.max_views));
    const rates = data.series.map((s) => s.stats.median_like_rate);
    const rejected = data.rejected?.length ?? 0;
    return [
      {
        key: "series",
        label: "系列数",
        value: String(data.series.length),
        unit: "个",
        caption: rejected > 0 ? `候选 ${data.series.length + rejected} 个，对抗校验淘汰 ${rejected} 个` : "进入排名的格式",
      },
      {
        key: "samples",
        label: "实测样本数",
        value: String(flat.length),
        unit: "条",
        caption: `覆盖 ${channels} 个频道，指标全部实测非估算`,
      },
      {
        key: "views",
        label: "合计播放",
        value: formatCount(totalViews),
        caption: `单条最高 ${formatCount(peak)}`,
      },
      {
        key: "rate",
        label: "全表中位赞率",
        value: formatRate(median(flat.map((v) => v.like_rate))),
        caption: `系列中位数的中位 ${formatRate(limits.likeRate)}（图中横线）；各系列 ${formatRate(Math.min(...rates))} – ${formatRate(Math.max(...rates))}`,
      },
      {
        key: "shortlist",
        label: "短名单",
        value: String(marks.shortlist),
        unit: "个",
        caption: `在做 ${marks.doing} · 已弃 ${marks.rejected} · 未定 ${marks.none}`,
        tone: "work",
      },
    ];
  }, [data, flat, limits, marks]);

  const readout = useMemo(() => {
    if (data.series.length === 0) return null;
    const byViews = [...data.series].sort((a, b) => b.stats.median_views - a.stats.median_views);
    const byRate = [...data.series].sort(
      (a, b) => b.stats.median_like_rate - a.stats.median_like_rate,
    );
    const n = data.series.length;
    const topV = byViews[0];
    const topR = byRate[0];
    return {
      topV,
      topR,
      topVRateRank: byRate.findIndex((s) => s.slug === topV.slug) + 1,
      topRViewRank: byViews.findIndex((s) => s.slug === topR.slug) + 1,
      n,
      both: data.series.filter((s) => quadrantOf(s, limits) === "both").length,
    };
  }, [data.series, limits]);

  const buckets = useMemo(() => {
    const out: Record<Quadrant, ResearchSeries[]> = {
      both: [],
      views_only: [],
      likes_only: [],
      neither: [],
    };
    for (const s of [...data.series].sort((a, b) => a.rank - b.rank)) {
      out[quadrantOf(s, limits)].push(s);
    }
    return out;
  }, [data.series, limits]);

  return (
    <div className="research-dash">
      <ul className="research-kpis">
        {tiles.map((t) => (
          <li
            key={t.key}
            className={t.tone === "work" ? "research-kpi research-kpi-work" : "research-kpi"}
          >
            <span className="research-kpi-label">{t.label}</span>
            <span className="research-kpi-value">
              {t.value}
              {t.unit ? <em className="research-kpi-unit">{t.unit}</em> : null}
            </span>
            <span className="research-kpi-caption">{t.caption}</span>
          </li>
        ))}
      </ul>

      <section className="research-dash-chart" aria-label="播放与赞率四象限">
        <h3 className="research-dash-h3">
          中位播放 × 中位点赞率
          <span className="research-dash-h3-note">
            两条虚线是这份数据自己的中位数；点击圆点打开该系列
          </span>
        </h3>
        {readout ? (
        <p className="research-dash-read">
          播放第一的<strong>{readout.topV.name_zh}</strong>，赞率只排第 {readout.topVRateRank}/
          {readout.n}（{formatRate(readout.topV.stats.median_like_rate)}）；赞率第一的
          <strong>{readout.topR.name_zh}</strong>，播放排第 {readout.topRViewRank}/{readout.n}（
          {formatCount(readout.topR.stats.median_views)}）。
          <span className="research-dash-read-punch">
            高播放与高赞率在这份数据里几乎不重叠——两条线都站上去的只有 {readout.both} 个系列。
          </span>
        </p>
        ) : null}
        <ResearchScatter
          series={data.series}
          workspace={workspace}
          limits={limits}
          onOpenSeries={onOpenSeries}
        />
      </section>

      <section className="research-quadrants" aria-label="象限归属">
        {QUADRANT_ORDER.map((q) => (
          <div key={q} className={`research-quad research-quad-${q}`}>
            <h4 className="research-quad-head">
              {QUADRANT_LABEL[q]}
              <span className="research-quad-count">{buckets[q].length}</span>
            </h4>
            <p className="research-quad-hint">{QUADRANT_HINT[q]}</p>
            {buckets[q].length === 0 ? (
              <p className="research-quad-empty">这一格是空的。</p>
            ) : (
              <ul className="research-quad-list">
                {buckets[q].map((s) => {
                  const status = workspace.series[s.slug]?.status ?? "none";
                  return (
                    <li key={s.slug}>
                      <button
                        type="button"
                        className="research-quad-item"
                        onClick={() => onOpenSeries(s.slug)}
                        aria-label={`打开 ${s.name_zh}，中位播放 ${formatCount(s.stats.median_views)}，中位赞率 ${formatRate(s.stats.median_like_rate)}`}
                      >
                        <span className="research-quad-rank">#{s.rank}</span>
                        <span className="research-quad-name">{s.name_zh}</span>
                        <span className="research-quad-nums">
                          {formatCount(s.stats.median_views)} · {formatRate(s.stats.median_like_rate)}
                        </span>
                        {status !== "none" ? (
                          <span className={`research-quad-status research-dot-${status}`}>
                            {STATUS_LABEL[status]}
                          </span>
                        ) : null}
                      </button>
                    </li>
                  );
                })}
              </ul>
            )}
          </div>
        ))}
      </section>

      {data.series.length > 0 ? (
        <p className="research-dash-verdict">
          <span className="research-dash-verdict-tag">榜首结论</span>
          <Rich text={[...data.series].sort((a, b) => a.rank - b.rank)[0].verdict} />
        </p>
      ) : null}

      <ResearchDashboardMethod
        criteria={data.criteria}
        method={data.method}
        window={data.window}
        generatedAt={data.generated_at}
      />
    </div>
  );
}
