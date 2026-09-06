/** One candidate series: headline metrics collapsed, full replication brief +
 * evidence table expanded. */
import { ResearchVideoTable } from "./ResearchVideoTable";
import { Rich } from "./ResearchText";
import { formatCount, formatRate, type ResearchSeries } from "../lib/researchApi";

export interface ResearchSeriesCardProps {
  series: ResearchSeries;
  open: boolean;
  onToggle: () => void;
}

const SCORE_LABEL: Record<number, string> = {
  5: "极易 · 单人半天",
  4: "容易 · 单人 1-2 天",
  3: "中等 · 需搭流水线",
  2: "偏难 · 手工量大",
  1: "很难 · 接近团队活",
};

export function ResearchSeriesCard({ series, open, onToggle }: ResearchSeriesCardProps): JSX.Element {
  const { stats, replication } = series;
  return (
    <section className={open ? "research-card research-card-open" : "research-card"}>
      <button
        type="button"
        className="research-card-head"
        aria-expanded={open}
        onClick={onToggle}
      >
        <span className="research-rank">#{series.rank}</span>
        <span className="research-titles">
          <span className="research-name-zh">{series.name_zh}</span>
          <span className="research-name-en">{series.name_en}</span>
        </span>
        <span className="research-headline">
          <span className="research-metric">
            <b>{formatCount(stats.median_views)}</b>
            <small>播放中位</small>
          </span>
          <span className="research-metric">
            <b className="research-rate">{formatRate(stats.median_like_rate)}</b>
            <small>点赞率中位</small>
          </span>
          <span className="research-metric">
            <b>{"★".repeat(replication.score)}{"☆".repeat(5 - replication.score)}</b>
            <small>翻拍易度</small>
          </span>
        </span>
        <span className="research-chevron" aria-hidden="true">{open ? "▾" : "▸"}</span>
      </button>

      <div className="research-card-tags">
        <span className="research-pill">{series.orientation}</span>
        <span className="research-pill"><Rich text={series.market} /></span>
        <span className="research-pill"><Rich text={series.typical_length} /></span>
        <span className="research-pill research-pill-hours"><Rich text={replication.hours_per_episode} /></span>
      </div>

      {open ? (
        <div className="research-card-body">
          <p className="research-desc"><Rich text={series.description} /></p>

          <div className="research-grid">
            <div className="research-block">
              <h4>为什么有人看（爽点机制）</h4>
              <p><Rich text={series.why_it_works} /></p>
            </div>
            <div className="research-block">
              <h4>结论</h4>
              <p><Rich text={series.verdict} /></p>
            </div>
            <div className="research-block">
              <h4>单人可行性 · {SCORE_LABEL[replication.score] ?? "—"}</h4>
              <p><Rich text={replication.stack_fit} /></p>
              <p className="research-blockers"><b>卡点：</b><Rich text={replication.blockers} /></p>
              <ul className="research-tools">
                {replication.tools.map((t) => (
                  <li key={t} className="research-pill research-pill-tool">{t}</li>
                ))}
              </ul>
            </div>
            <div className="research-block">
              <h4>变现 / 风险</h4>
              <p><Rich text={series.monetization} /></p>
              <p className="research-risk"><b>风险：</b><Rich text={series.risk} /></p>
            </div>
          </div>

          <div className="research-block">
            <h4>翻拍流程（一个人怎么做出一集）</h4>
            <ol className="research-howto">
              {replication.how_to.map((step, i) => <li key={i}><Rich text={step} /></li>)}
            </ol>
          </div>

          <div className="research-block">
            <h4>
              实测样本 · {stats.videos} 条
              <span className="muted">
                {" "}· 合计 {formatCount(stats.total_views)} 播放 · 最高 {formatCount(stats.max_views)}
              </span>
            </h4>
            <ResearchVideoTable videos={series.videos} />
          </div>
        </div>
      ) : null}
    </section>
  );
}
