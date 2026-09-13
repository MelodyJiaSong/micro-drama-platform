/** ResearchPage: the 选题调研 workspace shell.
 *
 * Owns everything the five views share — the dataset, the persisted workspace
 * (status / rating / notes), the compare selection, and which series the detail
 * panel is showing. The views themselves are pure: they render what they are
 * given and call back. All writes funnel through `mark*` here so a single failed
 * PUT surfaces in one place instead of five. */
import { useCallback, useEffect, useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { ResearchDashboard } from "./ResearchDashboard";
import { ResearchSeriesGrid } from "./ResearchSeriesGrid";
import { ResearchSeriesDetail } from "./ResearchSeriesDetail";
import { ResearchVideoExplorer } from "./ResearchVideoExplorer";
import { ResearchCompare } from "./ResearchCompare";
import { ResearchRevenue } from "./ResearchRevenue";
import {
  fetchResearchDataset,
  fetchResearchDatasets,
  fetchWorkspace,
  markSeries,
  markVideo,
  type ResearchDataset,
  type ResearchDatasetSummary,
  type ResearchWorkspace,
  type SeriesMark,
  type VideoMark,
} from "../lib/researchApi";

const EMPTY_WORKSPACE: ResearchWorkspace = { dataset: "", series: {}, videos: {} };
const MAX_COMPARE = 4;

type TabId = "dashboard" | "series" | "videos" | "revenue" | "compare";

const TABS: Array<{ id: TabId; label: string; hint: string }> = [
  { id: "dashboard", label: "总览", hint: "两项硬标准的分布与象限" },
  { id: "series", label: "系列", hint: "筛选、评分、定状态" },
  { id: "videos", label: "样本库", hint: "全部实测样本" },
  { id: "revenue", label: "收益预估", hint: "半年能赚多少 · 含 YPP 变现门槛" },
  { id: "compare", label: "对比", hint: "并排看几个候选" },
];

export function ResearchPage(): JSX.Element {
  const [searchParams, setSearchParams] = useSearchParams();
  const [summaries, setSummaries] = useState<ResearchDatasetSummary[]>([]);
  const [data, setData] = useState<ResearchDataset | null>(null);
  const [workspace, setWorkspace] = useState<ResearchWorkspace>(EMPTY_WORKSPACE);
  const [error, setError] = useState<string | null>(null);
  const [saveError, setSaveError] = useState<string | null>(null);
  const [selected, setSelected] = useState<string[]>([]);

  const dataset = searchParams.get("dataset");
  const tab = (searchParams.get("tab") as TabId | null) ?? "dashboard";
  const openSlug = searchParams.get("series");

  const setParam = useCallback(
    (patch: Record<string, string | null>) => {
      setSearchParams((prev) => {
        const next = new URLSearchParams(prev);
        for (const [k, v] of Object.entries(patch)) {
          if (v === null) next.delete(k);
          else next.set(k, v);
        }
        return next;
      });
    },
    [setSearchParams],
  );

  useEffect(() => {
    void (async () => {
      try {
        const listed = await fetchResearchDatasets();
        setSummaries(listed.datasets);
        if (!dataset && listed.datasets.length > 0) {
          setParam({ dataset: listed.datasets[0].dataset });
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : String(err));
      }
    })();
  }, [dataset, setParam]);

  useEffect(() => {
    if (!dataset) return;
    void (async () => {
      try {
        const [d, w] = await Promise.all([
          fetchResearchDataset(dataset),
          fetchWorkspace(dataset),
        ]);
        setData(d);
        setWorkspace(w);
        setError(null);
      } catch (err) {
        setData(null);
        setError(err instanceof Error ? err.message : String(err));
      }
    })();
  }, [dataset]);

  const onMarkSeries = useCallback(
    (slug: string, patch: SeriesMark) => {
      if (!dataset) return;
      void (async () => {
        try {
          setWorkspace(await markSeries(dataset, slug, patch));
          setSaveError(null);
        } catch (err) {
          setSaveError(err instanceof Error ? err.message : String(err));
        }
      })();
    },
    [dataset],
  );

  const onMarkVideo = useCallback(
    (videoId: string, patch: VideoMark) => {
      if (!dataset) return;
      void (async () => {
        try {
          setWorkspace(await markVideo(dataset, videoId, patch));
          setSaveError(null);
        } catch (err) {
          setSaveError(err instanceof Error ? err.message : String(err));
        }
      })();
    },
    [dataset],
  );

  const onToggleSelect = useCallback((slug: string) => {
    setSelected((prev) =>
      prev.includes(slug)
        ? prev.filter((s) => s !== slug)
        : prev.length >= MAX_COMPARE
          ? prev
          : [...prev, slug],
    );
  }, []);

  const onOpenSeries = useCallback((slug: string) => setParam({ series: slug }), [setParam]);

  useEffect(() => {
    if (!openSlug) return;
    const onKey = (e: KeyboardEvent): void => {
      if (e.key === "Escape") setParam({ series: null });
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [openSlug, setParam]);

  const openIndex = useMemo(
    () => (data && openSlug ? data.series.findIndex((s) => s.slug === openSlug) : -1),
    [data, openSlug],
  );
  const openSeries = openIndex >= 0 && data ? data.series[openIndex] : null;

  const step = useCallback(
    (delta: number) => {
      if (!data || openIndex < 0) return;
      const next = (openIndex + delta + data.series.length) % data.series.length;
      setParam({ series: data.series[next].slug });
    },
    [data, openIndex, setParam],
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

  const shortlisted = Object.values(workspace.series).filter((m) => m.status === "shortlist").length;

  return (
    <div className="research-page research-workspace">
      <header className="research-header">
        <div className="research-titlebar">
          <h1>{data.title}</h1>
          {shortlisted > 0 ? (
            <span className="research-shortlist-badge">短名单 {shortlisted}</span>
          ) : null}
        </div>
        <p className="muted">
          窗口 {data.window.from} – {data.window.to} · 生成于 {data.generated_at} · {data.series.length} 个系列 ·
          {" "}{data.series.reduce((n, s) => n + s.videos.length, 0)} 条实测样本
        </p>
        {summaries.length > 1 ? (
          <div className="research-datasets">
            {summaries.map((s) => (
              <button
                key={s.dataset}
                type="button"
                aria-pressed={s.dataset === dataset}
                className={s.dataset === dataset ? "research-tab research-tab-active" : "research-tab"}
                onClick={() => setParam({ dataset: s.dataset, series: null })}
              >
                {s.title}
              </button>
            ))}
          </div>
        ) : null}
        <nav className="research-tabs" role="tablist" aria-label="调研视图">
          {TABS.map((t) => (
            <button
              key={t.id}
              type="button"
              role="tab"
              aria-selected={tab === t.id}
              title={t.hint}
              className={tab === t.id ? "research-viewtab research-viewtab-on" : "research-viewtab"}
              onClick={() => setParam({ tab: t.id })}
            >
              {t.label}
              {t.id === "compare" && selected.length > 0 ? (
                <span className="research-viewtab-count">{selected.length}</span>
              ) : null}
            </button>
          ))}
        </nav>
      </header>

      {saveError ? (
        <div role="alert" className="research-save-error">
          保存失败：{saveError}
          <button type="button" onClick={() => setSaveError(null)} aria-label="关闭">×</button>
        </div>
      ) : null}

      {openSeries ? (
        <div className="research-viewbody research-detailhost">
          <ResearchSeriesDetail
            series={openSeries}
            mark={workspace.series[openSeries.slug] ?? {}}
            videoMarks={workspace.videos}
            onMark={(patch) => onMarkSeries(openSeries.slug, patch)}
            onMarkVideo={onMarkVideo}
            onClose={() => setParam({ series: null })}
            onPrev={() => step(-1)}
            onNext={() => step(1)}
          />
        </div>
      ) : (
      <div className="research-viewbody">
        {tab === "dashboard" ? (
          <ResearchDashboard data={data} workspace={workspace} onOpenSeries={onOpenSeries} />
        ) : null}
        {tab === "series" ? (
          <ResearchSeriesGrid
            data={data}
            workspace={workspace}
            onOpenSeries={onOpenSeries}
            onMark={onMarkSeries}
            selected={selected}
            onToggleSelect={onToggleSelect}
          />
        ) : null}
        {tab === "videos" ? (
          <ResearchVideoExplorer
            data={data}
            workspace={workspace}
            onMarkVideo={onMarkVideo}
            onOpenSeries={onOpenSeries}
          />
        ) : null}
        {tab === "revenue" ? (
          <ResearchRevenue data={data} onOpenSeries={onOpenSeries} />
        ) : null}
        {tab === "compare" ? (
          <ResearchCompare
            data={data}
            workspace={workspace}
            selected={selected}
            onToggleSelect={onToggleSelect}
            onOpenSeries={onOpenSeries}
          />
        ) : null}
      </div>
      )}

    </div>
  );
}
