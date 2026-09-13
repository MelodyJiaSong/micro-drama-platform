/** 详情页「实测样本」子页：该系列每一条实测视频，播放量以条形表示相对本系列
 * 最高值的量级（CSP 禁外链图，缩略图一律不取）。可按播放 / 点赞率 / 日期排序，
 * 每行可加星标与自己的备注。 */
import { useMemo, useState } from "react";
import { Rich } from "./ResearchText";
import {
  formatCount,
  formatDate,
  formatDuration,
  formatRate,
  type ResearchVideo,
  type VideoMark,
} from "../lib/researchApi";

export interface ResearchSeriesDetailSamplesProps {
  videos: ResearchVideo[];
  videoMarks: Record<string, VideoMark>;
  onMarkVideo: (videoId: string, patch: VideoMark) => void;
}

type SampleSort = "index" | "views" | "like_rate" | "date";
type SortDir = "asc" | "desc";

export function ResearchSeriesDetailSamples({
  videos,
  videoMarks,
  onMarkVideo,
}: ResearchSeriesDetailSamplesProps): JSX.Element {
  const [sort, setSort] = useState<SampleSort>("index");
  const [dir, setDir] = useState<SortDir>("desc");
  const [drafts, setDrafts] = useState<Record<string, string>>({});

  const maxViews = useMemo(() => Math.max(1, ...videos.map((v) => v.view_count)), [videos]);

  const rows = useMemo(() => {
    const indexed = videos.map((v, i) => ({ v, i }));
    if (sort === "index") return indexed;
    const sign = dir === "asc" ? 1 : -1;
    return [...indexed].sort((a, b) => {
      if (sort === "views") return sign * (a.v.view_count - b.v.view_count);
      if (sort === "like_rate") return sign * (a.v.like_rate - b.v.like_rate);
      return sign * a.v.upload_date.localeCompare(b.v.upload_date);
    });
  }, [videos, sort, dir]);

  if (videos.length === 0) {
    return <p className="research-detail-empty muted">该系列暂无实测样本。</p>;
  }

  const toggleSort = (key: SampleSort): void => {
    if (key === sort) setDir(dir === "desc" ? "asc" : "desc");
    else {
      setSort(key);
      setDir("desc");
    }
  };

  const savedNote = (id: string): string => videoMarks[id]?.note ?? "";
  const draftNote = (id: string): string => drafts[id] ?? savedNote(id);
  const commitNote = (id: string): void => {
    const next = draftNote(id);
    if (next !== savedNote(id)) onMarkVideo(id, { note: next });
  };

  const sortableHead = (key: SampleSort, label: string): JSX.Element => (
    <th
      scope="col"
      className="research-col-num"
      aria-sort={sort === key ? (dir === "asc" ? "ascending" : "descending") : "none"}
    >
      <button
        type="button"
        className={sort === key ? "research-detail-sortbtn research-detail-sortbtn-on" : "research-detail-sortbtn"}
        aria-label={`按${label}排序`}
        onClick={() => toggleSort(key)}
      >
        {label}
        <span aria-hidden="true">{sort === key ? (dir === "asc" ? " ▲" : " ▼") : " ↕"}</span>
      </button>
    </th>
  );

  return (
    <div className="research-detail-panel">
      <p className="research-detail-sampleshint muted">
        共 {videos.length} 条实测样本；条形长度＝相对本系列最高播放（{formatCount(maxViews)}）。
        {sort !== "index" ? (
          <button type="button" className="research-detail-sortreset" onClick={() => setSort("index")}>
            恢复原序
          </button>
        ) : null}
      </p>
      <div className="research-table-wrap">
        <table className="research-table research-detail-videos">
          <thead>
            <tr>
              <th scope="col" className="research-col-idx">#</th>
              <th scope="col" className="research-detail-star-col"><span className="research-detail-srhead">星标</span></th>
              <th scope="col">标题 / 频道 / 备注</th>
              {sortableHead("views", "播放量")}
              <th scope="col" className="research-col-num">点赞</th>
              {sortableHead("like_rate", "点赞率")}
              {sortableHead("date", "发布")}
              <th scope="col" className="research-col-num">时长</th>
            </tr>
          </thead>
          <tbody>
            {rows.map(({ v, i }) => {
              const marked = videoMarks[v.video_id]?.bookmarked === true;
              const pct = Math.max(1, Math.round((v.view_count / maxViews) * 100));
              return (
                <tr key={v.video_id} className={marked ? "research-detail-vrow-on" : undefined}>
                  <td className="research-col-idx">{i + 1}</td>
                  <td className="research-detail-star-col">
                    <button
                      type="button"
                      aria-pressed={marked}
                      aria-label={`星标《${v.title}》`}
                      className={marked ? "research-detail-star research-detail-star-on" : "research-detail-star"}
                      onClick={() => onMarkVideo(v.video_id, { bookmarked: !marked })}
                    >
                      {marked ? "★" : "☆"}
                    </button>
                  </td>
                  <td>
                    <a className="research-video-link" href={v.url} target="_blank" rel="noreferrer noopener">
                      {v.title}
                    </a>
                    <div className="research-detail-vmeta">
                      {v.channel_url ? (
                        <a className="research-channel" href={v.channel_url} target="_blank" rel="noreferrer noopener">
                          {v.channel}
                        </a>
                      ) : (
                        <span className="research-channel">{v.channel}</span>
                      )}
                      <span className={v.vertical ? "research-pill research-pill-shorts" : "research-pill"}>
                        {v.vertical ? "竖屏 Shorts" : "横屏"}
                      </span>
                    </div>
                    {v.note ? (
                      <p className="research-detail-vnote-data"><Rich text={v.note} /></p>
                    ) : null}
                    <input
                      type="text"
                      className="research-detail-vnote"
                      value={draftNote(v.video_id)}
                      placeholder="我的备注…"
                      aria-label={`《${v.title}》的我的备注`}
                      onChange={(e) => setDrafts({ ...drafts, [v.video_id]: e.target.value })}
                      onBlur={() => commitNote(v.video_id)}
                      onKeyDown={(e) => {
                        if (e.key === "Enter") e.currentTarget.blur();
                      }}
                    />
                  </td>
                  <td className="research-col-num research-detail-views-cell">
                    <span className="research-detail-views-num">{formatCount(v.view_count)}</span>
                    <span className="research-detail-bar" aria-hidden="true">
                      <span style={{ width: `${pct}%` }} />
                    </span>
                  </td>
                  <td className="research-col-num">{formatCount(v.like_count)}</td>
                  <td className="research-col-num research-rate">{formatRate(v.like_rate)}</td>
                  <td className="research-col-num">{formatDate(v.upload_date)}</td>
                  <td className="research-col-num">{formatDuration(v.duration)}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
