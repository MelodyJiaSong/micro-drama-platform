/** 系列详情：从任意入口打开的深读面板。顶部常驻排名 / 名称 / 三项指标 / 状态 /
 * 评分 / 翻页，下面五个子页：概览 · 翻拍流程 · 实测样本 · 风险与变现 · 我的笔记。 */
import { useEffect, useState } from "react";
import { Rich } from "./ResearchText";
import { ResearchSeriesDetailNotes } from "./ResearchSeriesDetailNotes";
import { ResearchSeriesDetailReplication } from "./ResearchSeriesDetailReplication";
import { ResearchSeriesDetailSamples } from "./ResearchSeriesDetailSamples";
import {
  formatCount,
  formatDate,
  formatRate,
  STATUS_LABEL,
  STATUS_ORDER,
  type ResearchSeries,
  type SeriesMark,
  type VideoMark,
} from "../lib/researchApi";

export interface ResearchSeriesDetailProps {
  series: ResearchSeries;
  mark: SeriesMark;
  videoMarks: Record<string, VideoMark>;
  onMark: (patch: SeriesMark) => void;
  onMarkVideo: (videoId: string, patch: VideoMark) => void;
  onClose: () => void;
  onPrev: () => void;
  onNext: () => void;
}

type DetailTab = "overview" | "howto" | "samples" | "risk" | "notes";

const TABS: Array<{ id: DetailTab; label: string }> = [
  { id: "overview", label: "概览" },
  { id: "howto", label: "翻拍流程" },
  { id: "samples", label: "实测样本" },
  { id: "risk", label: "风险与变现" },
  { id: "notes", label: "我的笔记" },
];

const STARS: number[] = [1, 2, 3, 4, 5];

/** 样本播放量按发布时间排开 —— 这条赛道最要紧的一件事是方差，柱子高低一眼看得出。 */
function ViewsSpark({ series }: { series: ResearchSeries }): JSX.Element | null {
  const ordered = [...series.videos].sort((a, b) => a.upload_date.localeCompare(b.upload_date));
  if (ordered.length === 0) return null;
  const max = Math.max(...ordered.map((v) => v.view_count), 1);
  const width = 320;
  const height = 52;
  const gap = 3;
  const bar = (width - gap * (ordered.length - 1)) / ordered.length;
  const medianY = height - (Math.min(series.stats.median_views, max) / max) * height;
  return (
    <svg
      className="research-detail-spark"
      viewBox={`0 0 ${width} ${height}`}
      preserveAspectRatio="none"
      role="img"
      aria-label={`${ordered.length} 条样本按发布时间排列的播放量，最高 ${formatCount(max)}，中位 ${formatCount(series.stats.median_views)}`}
    >
      {ordered.map((v, i) => {
        const h = Math.max(2, (v.view_count / max) * height);
        const cls = v.vertical
          ? "research-detail-spark-bar research-detail-spark-vertical"
          : "research-detail-spark-bar";
        return (
          <rect key={v.video_id} x={i * (bar + gap)} y={height - h} width={bar} height={h} className={cls}>
            <title>{`${formatDate(v.upload_date)} · ${formatCount(v.view_count)} 播放 · ${formatRate(v.like_rate)}`}</title>
          </rect>
        );
      })}
      <line x1="0" y1={medianY} x2={width} y2={medianY} className="research-detail-spark-median" />
    </svg>
  );
}

export function ResearchSeriesDetail(props: ResearchSeriesDetailProps): JSX.Element {
  const { series, mark, videoMarks, onMark, onMarkVideo, onClose, onPrev, onNext } = props;
  const [tab, setTab] = useState<DetailTab>("overview");
  const status = mark.status ?? "none";
  const rating = mark.rating ?? 0;
  const bookmarked = series.videos.filter((v) => videoMarks[v.video_id]?.bookmarked).length;

  useEffect(() => {
    const onKey = (event: KeyboardEvent): void => {
      const node = event.target as HTMLElement | null;
      const tag = node?.tagName ?? "";
      if (tag === "INPUT" || tag === "TEXTAREA" || node?.isContentEditable) return;
      if (event.key === "Escape") onClose();
      else if (event.key === "ArrowLeft") onPrev();
      else if (event.key === "ArrowRight") onNext();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose, onNext, onPrev]);

  return (
    <section className="research-detail" aria-label={`系列详情：${series.name_zh}`}>
      <header className="research-detail-head">
        <div className="research-detail-headrow">
          <span className="research-detail-rank">#{series.rank}</span>
          <div className="research-detail-titles">
            <h2>{series.name_zh}</h2>
            <p>{series.name_en}</p>
          </div>
          <div className="research-detail-metrics">
            <span className="research-metric">
              <b>{formatCount(series.stats.median_views)}</b>
              <small>播放中位</small>
            </span>
            <span className="research-metric">
              <b className="research-rate">{formatRate(series.stats.median_like_rate)}</b>
              <small>点赞率中位</small>
            </span>
            <span className="research-metric">
              <b>{"★".repeat(series.replication.score)}{"☆".repeat(5 - series.replication.score)}</b>
              <small>翻拍易度</small>
            </span>
          </div>
          <div className="research-detail-nav">
            <button type="button" className="research-detail-navbtn" onClick={onPrev} aria-label="上一个系列">← 上一个</button>
            <button type="button" className="research-detail-navbtn" onClick={onNext} aria-label="下一个系列">下一个 →</button>
            <button type="button" className="research-detail-close" onClick={onClose} aria-label="关闭详情">✕</button>
          </div>
        </div>

        <div className="research-detail-marks">
          <div className="research-detail-markgroup" role="group" aria-label="我的状态">
            <span className="research-detail-label">状态</span>
            {STATUS_ORDER.map((s) => (
              <button
                key={s}
                type="button"
                data-status={s}
                aria-pressed={status === s}
                className={status === s ? "research-detail-status research-detail-status-on" : "research-detail-status"}
                onClick={() => onMark({ status: s })}
              >
                {STATUS_LABEL[s]}
              </button>
            ))}
          </div>
          <div className="research-detail-markgroup" role="group" aria-label="我的评分">
            <span className="research-detail-label">评分</span>
            <span className="research-detail-stars">
              {STARS.map((n) => (
                <button
                  key={n}
                  type="button"
                  aria-pressed={rating >= n}
                  aria-label={`打 ${n} 分`}
                  className={rating >= n ? "research-detail-star research-detail-star-on" : "research-detail-star"}
                  onClick={() => onMark({ rating: rating === n ? 0 : n })}
                >
                  {rating >= n ? "★" : "☆"}
                </button>
              ))}
            </span>
            <span className="research-detail-starval">{rating > 0 ? `${rating}/5` : "未评分"}</span>
          </div>
        </div>

        <nav className="research-detail-tabs" role="tablist" aria-label="详情分页">
          {TABS.map((t) => (
            <button
              key={t.id}
              type="button"
              role="tab"
              id={`research-tabbtn-${t.id}`}
              aria-selected={tab === t.id}
              aria-controls={`research-panel-${t.id}`}
              className={tab === t.id ? "research-detail-tab research-detail-tab-on" : "research-detail-tab"}
              onClick={() => setTab(t.id)}
            >
              {t.label}
              {t.id === "samples" ? <span className="research-detail-badge">{series.videos.length}</span> : null}
              {t.id === "samples" && bookmarked > 0 ? (
                <span className="research-detail-badge research-detail-badge-star">★{bookmarked}</span>
              ) : null}
              {t.id === "notes" && (mark.note ?? "").trim() !== "" ? (
                <span className="research-detail-badge research-detail-badge-dot" aria-hidden="true" />
              ) : null}
            </button>
          ))}
        </nav>
      </header>

      <div
        className="research-detail-body"
        role="tabpanel"
        id={`research-panel-${tab}`}
        aria-labelledby={`research-tabbtn-${tab}`}
        tabIndex={-1}
      >
        {tab === "overview" ? (
          <div className="research-detail-panel">
            <p className="research-detail-lead"><Rich text={series.description} /></p>
            <dl className="research-detail-facts">
              <div><dt>取向</dt><dd><Rich text={series.orientation} /></dd></div>
              <div><dt>市场</dt><dd><Rich text={series.market} /></dd></div>
              <div><dt>常见时长</dt><dd><Rich text={series.typical_length} /></dd></div>
            </dl>
            <section className="research-block">
              <h4>为什么有人看（爽点机制）</h4>
              <p className="research-detail-prose"><Rich text={series.why_it_works} /></p>
            </section>
            <section className="research-block research-detail-verdict">
              <h4>结论</h4>
              <p className="research-detail-prose"><Rich text={series.verdict} /></p>
            </section>
            <section className="research-block">
              <h4>样本播放量（按发布时间，横线＝中位）</h4>
              <ViewsSpark series={series} />
              <p className="research-detail-sparkcap">
                {series.stats.videos} 条样本 · 合计 {formatCount(series.stats.total_views)} · 最高{" "}
                {formatCount(series.stats.max_views)} · 中位 {formatCount(series.stats.median_views)} · 中位点赞率{" "}
                <span className="research-rate">{formatRate(series.stats.median_like_rate)}</span> · 深色柱＝竖屏
              </p>
            </section>
          </div>
        ) : null}

        {tab === "howto" ? <ResearchSeriesDetailReplication replication={series.replication} /> : null}

        {tab === "samples" ? (
          <ResearchSeriesDetailSamples
            key={series.slug}
            videos={series.videos}
            videoMarks={videoMarks}
            onMarkVideo={onMarkVideo}
          />
        ) : null}

        {tab === "risk" ? (
          <div className="research-detail-panel">
            <section className="research-block">
              <h4>变现</h4>
              <p className="research-detail-prose"><Rich text={series.monetization} /></p>
            </section>
            <section className="research-block">
              <h4>风险</h4>
              <p className="research-risk research-detail-prose"><Rich text={series.risk} /></p>
            </section>
          </div>
        ) : null}

        {tab === "notes" ? (
          <ResearchSeriesDetailNotes
            key={series.slug}
            note={mark.note ?? ""}
            onSave={(note) => onMark({ note })}
          />
        ) : null}
      </div>
    </section>
  );
}
