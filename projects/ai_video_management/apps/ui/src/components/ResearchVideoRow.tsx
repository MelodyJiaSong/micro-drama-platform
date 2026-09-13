/** One sample row of the 样本库 explorer, plus its collapsible 备注 editor.
 * Kept apart from the table so the row's local draft state re-renders alone. */
import { useState } from "react";
import { Rich } from "./ResearchText";
import {
  formatCount,
  formatDate,
  formatDuration,
  formatRate,
  type FlatVideo,
  type VideoMark,
} from "../lib/researchApi";

export const EXPLORER_COLUMN_COUNT = 10;

export interface ResearchVideoRowProps {
  video: FlatVideo;
  index: number;
  mark: VideoMark | undefined;
  maxViews: number;
  hot: boolean;
  onMarkVideo: (videoId: string, patch: VideoMark) => void;
  onOpenSeries: (slug: string) => void;
}

export function ResearchVideoRow({
  video,
  index,
  mark,
  maxViews,
  hot,
  onMarkVideo,
  onOpenSeries,
}: ResearchVideoRowProps): JSX.Element {
  const saved = mark?.note ?? "";
  const [open, setOpen] = useState(false);
  const [draft, setDraft] = useState(saved);
  const bookmarked = mark?.bookmarked === true;
  const share = maxViews > 0 ? Math.max(2, (video.view_count / maxViews) * 100) : 0;

  const commit = (): void => {
    if (draft !== saved) onMarkVideo(video.video_id, { note: draft });
  };

  return (
    <>
      <tr className={hot ? "research-vx-hotrow" : undefined}>
        <td className="research-vx-star-cell">
          <button
            type="button"
            className={bookmarked ? "research-vx-star research-vx-star-on" : "research-vx-star"}
            aria-pressed={bookmarked}
            aria-label={bookmarked ? `取消收藏 ${video.title}` : `收藏 ${video.title}`}
            onClick={() => onMarkVideo(video.video_id, { bookmarked: !bookmarked })}
          >
            {bookmarked ? "★" : "☆"}
          </button>
        </td>
        <td className="research-vx-idx">{index}</td>
        <td className="research-vx-title-cell">
          <a
            className="research-vx-link"
            href={video.url}
            target="_blank"
            rel="noreferrer noopener"
          >
            <Rich text={video.title} />
          </a>
          <div className="research-vx-meta">
            {video.channel_url ? (
              <a
                className="research-vx-channel"
                href={video.channel_url}
                target="_blank"
                rel="noreferrer noopener"
              >
                {video.channel}
              </a>
            ) : (
              <span className="research-vx-channel">{video.channel}</span>
            )}
            <button
              type="button"
              className={saved ? "research-vx-note-btn research-vx-note-btn-on" : "research-vx-note-btn"}
              aria-expanded={open}
              aria-label={`编辑 ${video.title} 的备注`}
              onClick={() => {
                setDraft(saved);
                setOpen(!open);
              }}
            >
              {saved ? "备注 ✎" : "备注 ＋"}
            </button>
          </div>
          {video.note ? (
            <div className="research-vx-datanote">
              <Rich text={video.note} />
            </div>
          ) : null}
        </td>
        <td>
          <button
            type="button"
            className="research-vx-series-btn"
            title={`打开系列 #${video.series_rank} ${video.series_name}`}
            onClick={() => onOpenSeries(video.series_slug)}
          >
            <span className="research-vx-chip-rank">#{video.series_rank}</span>
            <span className="research-vx-series-name">
              <Rich text={video.series_name} />
            </span>
          </button>
        </td>
        <td className="research-vx-viewcell">
          <span className="research-vx-bar" style={{ width: `${share}%` }} aria-hidden="true" />
          <span className="research-vx-val">{formatCount(video.view_count)}</span>
        </td>
        <td className="research-vx-num">{formatCount(video.like_count)}</td>
        <td className="research-vx-num research-vx-ratecell">
          <span className="research-vx-ratev">{formatRate(video.like_rate)}</span>
          {hot ? (
            <span className="research-vx-hotbadge" title="点赞率位于当前筛选集前 10%">
              前10%
            </span>
          ) : null}
        </td>
        <td className="research-vx-num">{formatDate(video.upload_date)}</td>
        <td className="research-vx-num">{formatDuration(video.duration)}</td>
        <td>
          <span className={video.vertical ? "research-pill research-pill-shorts" : "research-pill"}>
            {video.vertical ? "竖屏" : "横屏"}
          </span>
        </td>
      </tr>
      {open ? (
        <tr className="research-vx-noterow">
          <td colSpan={EXPLORER_COLUMN_COUNT}>
            <textarea
              className="research-vx-note-input"
              rows={2}
              placeholder="记下这条样本值得抄的地方（失焦即保存）"
              aria-label={`${video.title} 的备注`}
              value={draft}
              onChange={(e) => setDraft(e.target.value)}
              onBlur={commit}
            />
          </td>
        </tr>
      ) : null}
    </>
  );
}
