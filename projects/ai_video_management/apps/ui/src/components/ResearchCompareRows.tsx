/** The row model behind 对比 — one entry per attribute, in the order the matrix
 * shows them, plus the two cell renderers that carry local state or geometry.
 * Kept beside ResearchCompare.tsx so the view file stays about layout only. */
import { Rich } from "./ResearchText";
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

export const MAX_COMPARE = 4;
/** Under this length a prose cell fits inside the 6-line clamp, so no 展开 button. */
const CLAMP_MIN_CHARS = 110;

const ORIENTATION_LABEL: Record<string, string> = {
  longform: "横屏长视频",
  both: "长视频 ＋ 竖版切片",
  vertical: "竖屏 Shorts",
  short: "短视频",
};

const QUADRANT_TONE: Record<Quadrant, string> = {
  both: "pass",
  views_only: "half",
  likes_only: "half",
  neither: "fail",
};

export function stars(score: number): string {
  const n = Math.max(0, Math.min(5, Math.round(score)));
  return "★".repeat(n) + "☆".repeat(5 - n);
}

export interface CellCtx {
  workspace: ResearchWorkspace;
  limits: Thresholds;
}

interface RowBase {
  id: string;
  label: string;
  /** Section heading printed above the first row of each run. */
  group: string;
}

export interface NumericRow extends RowBase {
  kind: "numeric";
  accent: "views" | "rate" | "score";
  pick: (s: ResearchSeries) => number;
  format: (n: number) => string;
}

export interface TextRow extends RowBase {
  kind: "text";
  cell: (s: ResearchSeries, ctx: CellCtx) => JSX.Element;
}

export interface ProseRow extends RowBase {
  kind: "prose";
  text: (s: ResearchSeries) => string;
}

export type CompareRow = NumericRow | TextRow | ProseRow;

export const COMPARE_ROWS: CompareRow[] = [
  {
    kind: "text",
    id: "rank",
    label: "排名",
    group: "概览",
    cell: (s) => <b className="research-compare-rank">#{s.rank}</b>,
  },
  {
    kind: "numeric",
    id: "views",
    label: "播放中位",
    group: "回报",
    accent: "views",
    pick: (s) => s.stats.median_views,
    format: formatCount,
  },
  {
    kind: "numeric",
    id: "rate",
    label: "点赞率中位",
    group: "回报",
    accent: "rate",
    pick: (s) => s.stats.median_like_rate,
    format: formatRate,
  },
  {
    kind: "numeric",
    id: "max",
    label: "最高播放",
    group: "回报",
    accent: "views",
    pick: (s) => s.stats.max_views,
    format: formatCount,
  },
  {
    kind: "text",
    id: "samples",
    label: "样本数",
    group: "回报",
    cell: (s) => <span className="research-compare-plain">{s.stats.videos} 条实测</span>,
  },
  {
    kind: "numeric",
    id: "score",
    label: "翻拍易度",
    group: "成本",
    accent: "score",
    pick: (s) => s.replication.score,
    format: (n) => `${stars(n)} ${n}/5`,
  },
  { kind: "prose", id: "hours", label: "每集工时", group: "成本", text: (s) => s.replication.hours_per_episode },
  {
    kind: "text",
    id: "orientation",
    label: "版式",
    group: "定位",
    cell: (s) => (
      <span className="research-compare-tag">{ORIENTATION_LABEL[s.orientation] ?? s.orientation}</span>
    ),
  },
  { kind: "prose", id: "market", label: "市场", group: "定位", text: (s) => s.market },
  {
    kind: "text",
    id: "length",
    label: "典型时长",
    group: "定位",
    cell: (s) => (
      <span className="research-compare-plain">
        <Rich text={s.typical_length} />
      </span>
    ),
  },
  {
    kind: "text",
    id: "quadrant",
    label: "象限",
    group: "定位",
    cell: (s, ctx) => {
      const q = quadrantOf(s, ctx.limits);
      return (
        <span className={`research-compare-tag research-compare-q-${QUADRANT_TONE[q]}`}>
          {QUADRANT_LABEL[q]}
        </span>
      );
    },
  },
  {
    kind: "text",
    id: "status",
    label: "我的状态",
    group: "我的决定",
    cell: (s, ctx) => {
      const status: SeriesStatus = ctx.workspace.series[s.slug]?.status ?? "none";
      return (
        <span className={`research-compare-tag research-compare-st-${status}`}>{STATUS_LABEL[status]}</span>
      );
    },
  },
  {
    kind: "text",
    id: "rating",
    label: "我的评分",
    group: "我的决定",
    cell: (s, ctx) => {
      const rating = ctx.workspace.series[s.slug]?.rating ?? 0;
      return rating > 0 ? (
        <span className="research-compare-stars">
          {stars(rating)} <small>{rating}/5</small>
        </span>
      ) : (
        <span className="research-compare-none">未评分</span>
      );
    },
  },
  { kind: "prose", id: "monetization", label: "变现", group: "判断", text: (s) => s.monetization },
  { kind: "prose", id: "risk", label: "风险", group: "判断", text: (s) => s.risk },
  { kind: "prose", id: "verdict", label: "结论", group: "判断", text: (s) => s.verdict },
];

export interface NumericCellProps {
  row: NumericRow;
  series: ResearchSeries;
  max: number;
  best: boolean;
}

/** Value ＋ 最佳 badge ＋ a bar scaled to the row max, so magnitude reads across
 * columns without parsing digits. The bar is decorative; the number is the data. */
export function NumericCell({ row, series, max, best }: NumericCellProps): JSX.Element {
  const value = row.pick(series);
  const pct = max > 0 ? Math.max(3, Math.round((value / max) * 100)) : 0;
  const cls = best
    ? "research-compare-cell research-compare-num research-compare-best"
    : "research-compare-cell research-compare-num";
  return (
    <td className={cls}>
      <span className="research-compare-value">{row.format(value)}</span>
      {best ? <span className="research-compare-badge">最佳</span> : null}
      <span className={`research-compare-bar research-compare-bar-${row.accent}`} aria-hidden="true">
        <span style={{ width: `${pct}%` }} />
      </span>
    </td>
  );
}

export interface ProseCellProps {
  text: string;
  label: string;
  name: string;
  open: boolean;
  onToggle: () => void;
}

/** Long analysis prose, clamped to ~6 lines with a per-cell 展开/收起 so one
 * verbose 风险 paragraph can't push every other row off the screen. */
export function ProseCell({ text, label, name, open, onToggle }: ProseCellProps): JSX.Element {
  const long = text.length > CLAMP_MIN_CHARS;
  const cls = open || !long ? "research-compare-text" : "research-compare-text research-compare-clamp";
  return (
    <td className="research-compare-cell research-compare-prose">
      <div className={cls}>
        <Rich text={text} />
      </div>
      {long ? (
        <button
          type="button"
          className="research-compare-more"
          aria-expanded={open}
          aria-label={`${open ? "收起" : "展开"}「${name}」的${label}`}
          onClick={onToggle}
        >
          {open ? "收起 ▴" : "展开 ▾"}
        </button>
      ) : null}
    </td>
  );
}
