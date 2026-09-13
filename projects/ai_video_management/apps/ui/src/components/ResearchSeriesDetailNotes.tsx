/** 详情页「我的笔记」子页：显式点保存才写回工作区（不逐键上报），
 * 未保存时按钮与状态字都会提示。 */
import { useState } from "react";

export interface ResearchSeriesDetailNotesProps {
  note: string;
  onSave: (note: string) => void;
}

export function ResearchSeriesDetailNotes({ note, onSave }: ResearchSeriesDetailNotesProps): JSX.Element {
  const [draft, setDraft] = useState<string>(note);
  const dirty = draft !== note;

  return (
    <div className="research-detail-panel research-detail-notes">
      <label className="research-detail-label" htmlFor="research-detail-note-input">
        我的笔记
      </label>
      <textarea
        id="research-detail-note-input"
        className="research-detail-notearea"
        value={draft}
        rows={14}
        placeholder="为什么想做（或不做）这条？打算先试哪个命题？第一集准备砍掉哪一步？"
        onChange={(e) => setDraft(e.target.value)}
      />
      <div className="research-detail-noteactions">
        <button
          type="button"
          className="research-detail-save"
          disabled={!dirty}
          onClick={() => onSave(draft)}
        >
          保存
        </button>
        <button
          type="button"
          className="research-detail-revert"
          disabled={!dirty}
          onClick={() => setDraft(note)}
        >
          还原
        </button>
        <span className={dirty ? "research-detail-savedstate research-detail-savedstate-dirty" : "research-detail-savedstate"}>
          {dirty ? "有未保存的修改" : note === "" ? "还没写笔记" : "已保存"}
        </span>
      </div>
      <p className="research-detail-hint">
        笔记和状态、评分一起存在工作区里，跟数据集分开存放 —— 重新跑一遍调研、数据刷新之后依然保留。
      </p>
    </div>
  );
}
