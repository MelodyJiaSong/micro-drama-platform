/** ResearchPage: the 选题调研 module — ranked AIGC content series with the real
 * YouTube metrics behind each ranking. Datasets live at ai_videos/_research/. */
import { useCallback, useEffect, useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { ResearchSeriesCard } from "./ResearchSeriesCard";
import { Rich } from "./ResearchText";
import {
  fetchResearchDataset,
  fetchResearchDatasets,
  sortSeries,
  type ResearchDataset,
  type ResearchDatasetSummary,
  type ResearchSort,
} from "../lib/researchApi";

const SORTS: Array<{ id: ResearchSort; label: string }> = [
  { id: "balanced", label: "综合推荐" },
  { id: "views", label: "播放量" },
  { id: "like_rate", label: "点赞率" },
  { id: "replication", label: "翻拍易度" },
];

export function ResearchPage(): JSX.Element {
  const [searchParams, setSearchParams] = useSearchParams();
  const [summaries, setSummaries] = useState<ResearchDatasetSummary[]>([]);
  const [data, setData] = useState<ResearchDataset | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [openSlug, setOpenSlug] = useState<string | null>(null);

  const dataset = searchParams.get("dataset");
  const sort = (searchParams.get("sort") as ResearchSort | null) ?? "balanced";

  useEffect(() => {
    void (async () => {
      try {
        const listed = await fetchResearchDatasets();
        setSummaries(listed.datasets);
        if (!dataset && listed.datasets.length > 0) {
          setSearchParams({ dataset: listed.datasets[0].dataset, sort }, { replace: true });
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : String(err));
      }
    })();
  }, [dataset, setSearchParams, sort]);

  useEffect(() => {
    if (!dataset) return;
    void (async () => {
      try {
        setData(await fetchResearchDataset(dataset));
        setError(null);
      } catch (err) {
        setData(null);
        setError(err instanceof Error ? err.message : String(err));
      }
    })();
  }, [dataset]);

  const ordered = useMemo(() => (data ? sortSeries(data.series, sort) : []), [data, sort]);

  const onSort = useCallback(
    (id: ResearchSort) => {
      setSearchParams({ dataset: dataset ?? "", sort: id });
    },
    [dataset, setSearchParams],
  );

  if (error) {
    return (
      <div className="research-page">
        <h1>选题调研</h1>
        <div role="alert" className="research-error">
          读取调研数据失败：{error}
          <p className="muted">
            数据集应位于 <code>ai_videos/_research/*.json</code>，由 <code>tools/yt_research.py</code> 实测生成。
          </p>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="research-page">
        <h1>选题调研</h1>
        <p className="muted">{summaries.length === 0 ? "暂无调研数据集。" : "加载中…"}</p>
      </div>
    );
  }

  return (
    <div className="research-page">
      <header className="research-header">
        <h1>{data.title}</h1>
        <p className="muted">
          窗口 {data.window.from} – {data.window.to} · 生成于 {data.generated_at} · {data.series.length} 个系列 ·
          {" "}{data.series.reduce((n, s) => n + s.videos.length, 0)} 条实测样本
        </p>
        <p className="research-method"><Rich text={data.method} /></p>
        <ul className="research-criteria">
          {data.criteria.map((c, i) => <li key={i}><Rich text={c} /></li>)}
        </ul>
        {summaries.length > 1 ? (
          <div className="research-datasets">
            {summaries.map((s) => (
              <button
                key={s.dataset}
                type="button"
                className={s.dataset === dataset ? "research-tab research-tab-active" : "research-tab"}
                onClick={() => setSearchParams({ dataset: s.dataset, sort })}
              >
                {s.title}
              </button>
            ))}
          </div>
        ) : null}
        <div className="research-sorts" role="group" aria-label="排序">
          <span className="muted">排序：</span>
          {SORTS.map((s) => (
            <button
              key={s.id}
              type="button"
              aria-pressed={sort === s.id}
              className={sort === s.id ? "research-sort research-sort-active" : "research-sort"}
              onClick={() => onSort(s.id)}
            >
              {s.label}
            </button>
          ))}
        </div>
      </header>

      <div className="research-list">
        {ordered.map((s) => (
          <ResearchSeriesCard
            key={s.slug}
            series={s}
            open={openSlug === s.slug}
            onToggle={() => setOpenSlug(openSlug === s.slug ? null : s.slug)}
          />
        ))}
      </div>

      {data.rejected && data.rejected.length > 0 ? (
        <section className="research-footnote">
          <h3>被淘汰的候选（及原因）</h3>
          <ul>{data.rejected.map((r, i) => <li key={i}><Rich text={r} /></li>)}</ul>
        </section>
      ) : null}
      {data.caveats && data.caveats.length > 0 ? (
        <section className="research-footnote">
          <h3>数据说明与局限</h3>
          <ul>{data.caveats.map((c, i) => <li key={i}><Rich text={c} /></li>)}</ul>
        </section>
      ) : null}
    </div>
  );
}
