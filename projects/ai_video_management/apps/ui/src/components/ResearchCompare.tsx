/** 对比 Compare — a transposed decision matrix: rows are attributes, columns are
 * the series the user picked. The transpose is the point — reading 翻拍易度
 * across four candidates IS the decision; reading one series top-to-bottom is
 * what the card list already does. Row model lives in ResearchCompareRows.tsx. */
import { Fragment, useCallback, useMemo, useState } from "react";
import {
  COMPARE_ROWS,
  MAX_COMPARE,
  NumericCell,
  ProseCell,
  type CellCtx,
} from "./ResearchCompareRows";
import {
  formatCount,
  formatRate,
  thresholds,
  type ResearchDataset,
  type ResearchSeries,
  type ResearchWorkspace,
} from "../lib/researchApi";

export interface ResearchCompareProps {
  data: ResearchDataset;
  workspace: ResearchWorkspace;
  selected: string[];
  onToggleSelect: (slug: string) => void;
  onOpenSeries: (slug: string) => void;
}

export function ResearchCompare({
  data,
  workspace,
  selected,
  onToggleSelect,
  onOpenSeries,
}: ResearchCompareProps): JSX.Element {
  const [expanded, setExpanded] = useState<Record<string, boolean>>({});
  const limits = useMemo(() => thresholds(data), [data]);
  const picker = useMemo(() => [...data.series].sort((a, b) => a.rank - b.rank), [data]);
  const columns = useMemo(() => {
    const bySlug = new Map(data.series.map((s) => [s.slug, s] as const));
    return selected
      .map((slug) => bySlug.get(slug))
      .filter((s): s is ResearchSeries => s !== undefined)
      .slice(0, MAX_COMPARE);
  }, [data, selected]);

  const toggleCell = useCallback((key: string) => {
    setExpanded((prev) => ({ ...prev, [key]: !prev[key] }));
  }, []);

  const full = columns.length >= MAX_COMPARE;
  const ctx: CellCtx = { workspace, limits };
  let group = "";

  return (
    <section className="research-compare">
      <div className="research-compare-head">
        <h2>对比</h2>
        <span className="research-compare-count">
          已选 {columns.length} / {MAX_COMPARE}
          {full ? " · 已满，先移除一列再添加" : ""}
        </span>
        {columns.length > 0 ? (
          <button
            type="button"
            className="research-compare-clear"
            onClick={() => columns.forEach((s) => onToggleSelect(s.slug))}
          >
            清空
          </button>
        ) : null}
      </div>

      <div className="research-compare-picker" role="group" aria-label="选择要对比的系列">
        {picker.map((s) => {
          const on = columns.some((c) => c.slug === s.slug);
          const blocked = !on && full;
          return (
            <button
              key={s.slug}
              type="button"
              aria-pressed={on}
              aria-disabled={blocked}
              title={blocked ? `最多同时对比 ${MAX_COMPARE} 个系列，先移除一列` : s.name_en}
              className={on ? "research-compare-chip research-compare-chip-on" : "research-compare-chip"}
              onClick={() => {
                if (!blocked) onToggleSelect(s.slug);
              }}
            >
              <span className="research-compare-chip-rank">#{s.rank}</span>
              {s.name_zh}
            </button>
          );
        })}
      </div>

      {columns.length < 2 ? (
        <div className="research-compare-empty">
          <p className="research-compare-empty-lead">
            <b>选 2–4 个系列，并排看同一批属性。</b>
            对比把系列转成列、属性转成行：横着读一行，就是在同一把尺子下比候选。
          </p>
          <ul className="research-compare-empty-rows">
            <li>
              <b>回报</b> — 播放中位 / 点赞率中位 / 最高播放 / 样本数：数值行标出「最佳」，并按行内最大值画条。
            </li>
            <li>
              <b>成本</b> — 翻拍易度 / 每集工时：工时原文按 6 行折叠，逐格展开。
            </li>
            <li>
              <b>定位</b> — 版式 / 市场 / 典型时长 / 象限（象限对齐本数据集自身的中位线）。
            </li>
            <li>
              <b>判断与你的决定</b> — 变现 / 风险 / 结论，和你自己标的状态、评分并排读。
            </li>
          </ul>
          <p className="research-compare-empty-hint">
            {columns.length === 1 ? "已选 1 个，再选一个即可开始对比。" : "点上面任意两个系列名开始。"}
          </p>
        </div>
      ) : (
        <>
          <div className="research-compare-scroll">
            <table className="research-compare-table">
              <caption className="research-compare-caption">
                {columns.length} 个系列逐属性对比；四个数值行标出该行最佳，并按行内最大值画条。
              </caption>
              <thead>
                <tr>
                  <th scope="col" className="research-compare-corner">
                    对比项
                  </th>
                  {columns.map((s) => (
                    <th key={s.slug} scope="col" className="research-compare-colhead">
                      <button
                        type="button"
                        className="research-compare-open"
                        onClick={() => onOpenSeries(s.slug)}
                        title={`打开「${s.name_zh}」详情`}
                      >
                        <span className="research-compare-colrank">#{s.rank}</span>
                        <span className="research-compare-colname">{s.name_zh}</span>
                        <span className="research-compare-colen">{s.name_en}</span>
                      </button>
                      <button
                        type="button"
                        className="research-compare-drop"
                        aria-label={`从对比中移除「${s.name_zh}」`}
                        onClick={() => onToggleSelect(s.slug)}
                      >
                        ×
                      </button>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {COMPARE_ROWS.map((row) => {
                  const head = row.group !== group ? row.group : null;
                  group = row.group;
                  const max = row.kind === "numeric" ? Math.max(...columns.map((s) => row.pick(s))) : 0;
                  return (
                    <Fragment key={row.id}>
                      {head ? (
                        <tr className="research-compare-group">
                          <th scope="colgroup" colSpan={columns.length + 1}>
                            {head}
                          </th>
                        </tr>
                      ) : null}
                      <tr>
                        <th scope="row" className="research-compare-rowhead">
                          {row.label}
                        </th>
                        {columns.map((s) => {
                          if (row.kind === "numeric") {
                            return (
                              <NumericCell
                                key={s.slug}
                                row={row}
                                series={s}
                                max={max}
                                best={max > 0 && row.pick(s) === max}
                              />
                            );
                          }
                          if (row.kind === "prose") {
                            const key = `${row.id}:${s.slug}`;
                            return (
                              <ProseCell
                                key={s.slug}
                                text={row.text(s)}
                                label={row.label}
                                name={s.name_zh}
                                open={expanded[key] === true}
                                onToggle={() => toggleCell(key)}
                              />
                            );
                          }
                          return (
                            <td key={s.slug} className="research-compare-cell">
                              {row.cell(s, ctx)}
                            </td>
                          );
                        })}
                      </tr>
                    </Fragment>
                  );
                })}
              </tbody>
            </table>
          </div>
          <p className="research-compare-note">
            「象限」阈值取自本数据集自身的中位线：播放 {formatCount(limits.views)} / 点赞率{" "}
            {formatRate(limits.likeRate)}。「最佳」只在当前选中的列之间比较，换一组列会重算；列多时表格横向滚动，正文不压缩。
          </p>
        </>
      )}
    </section>
  );
}
