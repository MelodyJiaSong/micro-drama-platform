/** The example-video evidence table for one research series. Every row is a
 * real YouTube video whose metrics were measured, not estimated. */
import {
  formatCount,
  formatDate,
  formatDuration,
  formatRate,
  type ResearchVideo,
} from "../lib/researchApi";

export interface ResearchVideoTableProps {
  videos: ResearchVideo[];
}

export function ResearchVideoTable({ videos }: ResearchVideoTableProps): JSX.Element {
  if (videos.length === 0) {
    return <p className="muted">该系列暂无实测样本。</p>;
  }
  return (
    <div className="research-table-wrap">
      <table className="research-table">
        <thead>
          <tr>
            <th scope="col" className="research-col-idx">#</th>
            <th scope="col">标题 / 频道</th>
            <th scope="col" className="research-col-num">播放量</th>
            <th scope="col" className="research-col-num">点赞</th>
            <th scope="col" className="research-col-num">点赞率</th>
            <th scope="col" className="research-col-num">发布</th>
            <th scope="col" className="research-col-num">时长</th>
          </tr>
        </thead>
        <tbody>
          {videos.map((v, i) => (
            <tr key={v.video_id}>
              <td className="research-col-idx">{i + 1}</td>
              <td>
                <a className="research-video-link" href={v.url} target="_blank" rel="noreferrer noopener">
                  {v.title}
                </a>
                <div className="research-video-meta">
                  <span className="research-channel">{v.channel}</span>
                  <span className={v.vertical ? "research-pill research-pill-shorts" : "research-pill"}>
                    {v.vertical ? "竖屏 Shorts" : "横屏"}
                  </span>
                  {v.note ? <span className="research-video-note">{v.note}</span> : null}
                </div>
              </td>
              <td className="research-col-num">{formatCount(v.view_count)}</td>
              <td className="research-col-num">{formatCount(v.like_count)}</td>
              <td className="research-col-num research-rate">{formatRate(v.like_rate)}</td>
              <td className="research-col-num">{formatDate(v.upload_date)}</td>
              <td className="research-col-num">{formatDuration(v.duration)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
