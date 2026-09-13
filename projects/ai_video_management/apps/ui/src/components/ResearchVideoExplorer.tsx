/** 样本库 — every verified video in the dataset as one queryable table.
 * The series cards argue; this view lets the user check the evidence, mark the
 * samples worth copying, and jump back to whichever series a row came from. */
import { useMemo, useState } from "react";
import {
  flattenVideos,
  formatCount,
  formatRate,
  median,
  type ResearchDataset,
  type ResearchWorkspace,
  type VideoMark,
} from "../lib/researchApi";
import {
  EMPTY_FILTERS,
  ResearchVideoExplorerToolbar,
  type ExplorerFilters,
} from "./ResearchVideoExplorerToolbar";
import {
  COLUMNS,
  matches,
  parseFilters,
  sortRows,
  topDecile,
  type Column,
  type SortDir,
  type SortKey,
} from "./ResearchVideoExplorerModel";
import { EXPLORER_COLUMN_COUNT, ResearchVideoRow } from "./ResearchVideoRow";

function isoBounds(dates: string[]): { from: string; to: string } {
  const valid = dates.filter((d) => /^\d{8}$/.test(d)).sort();
  if (valid.length === 0) return { from: "", to: "" };
  const iso = (d: string): string => `${d.slice(0, 4)}-${d.slice(4, 6)}-${d.slice(6, 8)}`;
  return { from: iso(valid[0]), to: iso(valid[valid.length - 1]) };
}

export interface ResearchVideoExplorerProps {
  data: ResearchDataset;
  workspace: ResearchWorkspace;
  onMarkVideo: (videoId: string, patch: VideoMark) => void;
  onOpenSeries: (slug: string) => void;
}

export function ResearchVideoExplorer({
  data,
  workspace,
  onMarkVideo,
  onOpenSeries,
}: ResearchVideoExplorerProps): JSX.Element {
  const [filters, setFilters] = useState<ExplorerFilters>(EMPTY_FILTERS);
  const [sortKey, setSortKey] = useState<SortKey>("views");
  const [sortDir, setSortDir] = useState<SortDir>("desc");

  const all = useMemo(() => flattenVideos(data), [data]);
  const marks = workspace.videos;
  const parsed = useMemo(() => parseFilters(filters), [filters]);

  const rows = useMemo(
    () => sortRows(all.filter((v) => matches(v, filters, parsed, marks, false)), sortKey, sortDir, marks),
    [all, filters, parsed, marks, sortKey, sortDir],
  );

  const seriesCounts = useMemo(() => {
    const counts: Record<string, number> = {};
    for (const s of data.series) counts[s.slug] = 0;
    for (const v of all) {
      if (matches(v, filters, parsed, marks, true)) counts[v.series_slug] += 1;
    }
    return counts;
  }, [all, data, filters, parsed, marks]);

  const maxViews = useMemo(() => Math.max(0, ...all.map((v) => v.view_count)), [all]);
  const dateBounds = useMemo(() => isoBounds(all.map((v) => v.upload_date)), [all]);
  const barMax = rows.length > 0 ? Math.max(...rows.map((v) => v.view_count)) : 0;
  const hotFloor = useMemo(() => topDecile(rows.map((v) => v.like_rate)), [rows]);
  const totalViews = rows.reduce((sum, v) => sum + v.view_count, 0);
  const bookmarked = rows.filter((v) => marks[v.video_id]?.bookmarked === true).length;

  const onSort = (col: Column): void => {
    if (col.key === sortKey) {
      setSortDir(sortDir === "asc" ? "desc" : "asc");
      return;
    }
    setSortKey(col.key);
    setSortDir(col.descFirst ? "desc" : "asc");
  };

  const header = (col: Column): JSX.Element => {
    const active = col.key === sortKey;
    return (
      <th
        key={col.key}
        scope="col"
        className={col.cls}
        aria-sort={active ? (sortDir === "asc" ? "ascending" : "descending") : "none"}
      >
        <button
          type="button"
          className={active ? "research-vx-sortbtn research-vx-sortbtn-on" : "research-vx-sortbtn"}
          aria-label={`按${col.key === "bookmark" ? "收藏" : col.label}排序`}
          onClick={() => onSort(col)}
        >
          <span>{col.label}</span>
          <span
            className={active ? "research-vx-arrow" : "research-vx-arrow research-vx-arrow-off"}
            aria-hidden="true"
          >
            {active ? (sortDir === "asc" ? "▲" : "▼") : "↕"}
          </span>
        </button>
      </th>
    );
  };

  return (
    <section className="research-vx">
      <ResearchVideoExplorerToolbar
        data={data}
        filters={filters}
        seriesCounts={seriesCounts}
        shown={rows.length}
        total={all.length}
        maxViews={maxViews}
        dateBounds={dateBounds}
        onChange={(patch) => setFilters({ ...filters, ...patch })}
        onReset={() => setFilters(EMPTY_FILTERS)}
      />

      <div className="research-vx-scroll">
        <table className="research-vx-table" aria-label="调研样本库">
          <thead>
            <tr>
              {header(COLUMNS[0])}
              <th scope="col" className="research-vx-idx">
                #
              </th>
              {COLUMNS.slice(1).map(header)}
            </tr>
          </thead>
          <tbody>
            {rows.map((v, i) => (
              <ResearchVideoRow
                key={v.video_id}
                video={v}
                index={i + 1}
                mark={marks[v.video_id]}
                maxViews={barMax}
                hot={v.like_rate >= hotFloor}
                onMarkVideo={onMarkVideo}
                onOpenSeries={onOpenSeries}
              />
            ))}
            {rows.length === 0 ? (
              <tr>
                <td className="research-vx-empty" colSpan={EXPLORER_COLUMN_COUNT}>
                  没有符合条件的样本 —— 放宽筛选条件，或点右上角「清除」。
                </td>
              </tr>
            ) : null}
          </tbody>
        </table>
      </div>

      <div className="research-vx-footer">
        <span className="research-vx-sum">
          合计播放<b>{formatCount(totalViews)}</b>
        </span>
        <span className="research-vx-sum">
          中位播放<b>{formatCount(median(rows.map((v) => v.view_count)))}</b>
        </span>
        <span className="research-vx-sum">
          中位赞率
          <b className="research-vx-green">{formatRate(median(rows.map((v) => v.like_rate)))}</b>
        </span>
        <span className="research-vx-sum">
          已收藏<b>{bookmarked}</b>
        </span>
        <span className="research-vx-hint">
          绿底行 ＝ 当前筛选集点赞率前 10%；播放量底纹按当前筛选集的最高播放归一。
        </span>
      </div>
    </section>
  );
}
