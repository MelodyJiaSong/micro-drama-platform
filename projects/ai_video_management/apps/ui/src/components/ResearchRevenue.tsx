/** 收益 view: the 6-month solo-creator revenue projection.
 *
 * The dominant term is the YouTube Partner Program gate, not RPM — a format
 * whose realistic 6-month view total sits below 1,000 subs + 4,000 watch hours
 * earns exactly $0 however good its RPM is. The table therefore leads with the
 * gate month and shows `views x RPM` only where the gate actually clears. */
import { useState } from "react";
import { Rich } from "./ResearchText";
import {
  formatCount,
  formatUsd,
  type ResearchDataset,
  type ResearchSeries,
  type RevenueScenario,
} from "../lib/researchApi";

export interface ResearchRevenueProps {
  data: ResearchDataset;
  onOpenSeries: (slug: string) => void;
}

const COLS: Array<{ id: "low" | "mid" | "high"; label: string; hint: string }> = [
  { id: "low", label: "悲观", hint: "实测到的地板频道：管线全跑完，但命题/审美没校准" },
  { id: "mid", label: "中位", hint: "同期同行归一化后的中位数" },
  { id: "high", label: "乐观", hint: "今天开号仍打得通的最好实测样本，非历史天花板" },
];

function Cell({ s }: { s: RevenueScenario }): JSX.Element {
  const earns = s.monetized_views > 0;
  return (
    <div className={earns ? "research-rev-cell research-rev-earns" : "research-rev-cell"}>
      <div className="research-rev-money">
        {earns ? `${formatUsd(s.adsense_usd_low)} – ${formatUsd(s.adsense_usd_high)}` : "$0"}
      </div>
      <div className="research-rev-sub">
        {formatCount(s.views_6mo)} 播放 · 约 {formatCount(s.subs_estimate)} 订阅
      </div>
      <div className="research-rev-gate">
        {s.ypp_cleared_month === null
          ? "6 个月内过不了 YPP 门槛"
          : `第 ${s.ypp_cleared_month} 个月过门槛`}
        {earns && !s.reaches_payout_floor ? " · 未到 $100 起付线" : ""}
      </div>
    </div>
  );
}

function Row({ series, onOpen }: { series: ResearchSeries; onOpen: () => void }): JSX.Element | null {
  const [open, setOpen] = useState(false);
  const r = series.revenue;
  if (!r) return null;
  return (
    <>
      <tr>
        <td className="research-rev-rank">#{series.rank}</td>
        <td>
          <button type="button" className="research-rev-name" onClick={onOpen}>
            {series.name_zh}
          </button>
          <div className="research-rev-market">
            {r.market_label} · RPM ${r.rpm_low}–{r.rpm_high} · 可持续 {r.sustainable_uploads_per_month} 条/月
          </div>
          <button
            type="button"
            className="research-rev-why"
            aria-expanded={open}
            onClick={() => setOpen(!open)}
          >
            {open
              ? "收起依据"
              : r.new_channels_measured > 0
                ? `依据 · 实测 ${r.new_channels_measured} 个新号`
                : "查看依据（播放量 / RPM / 广告友好度）"}
          </button>
        </td>
        {COLS.map((c) => (
          <td key={c.id}>
            <Cell s={r.scenarios[c.id]} />
          </td>
        ))}
      </tr>
      {open ? (
        <tr className="research-rev-detailrow">
          <td colSpan={5}>
            <div className="research-rev-basis">
              <h4>播放量怎么来的</h4>
              <p><Rich text={r.views_basis} /></p>
              <h4>RPM 怎么来的</h4>
              <p><Rich text={r.rpm_basis} /></p>
              <h4>广告友好度</h4>
              <p><Rich text={r.ad_friendliness} /></p>
              <h4>AdSense 之外（前 6 个月）</h4>
              <p><Rich text={r.off_adsense_6mo} /></p>
              <p className="research-rev-conf"><b>置信度：</b><Rich text={r.confidence} /></p>
            </div>
          </td>
        </tr>
      ) : null}
    </>
  );
}

export function ResearchRevenue({ data, onOpenSeries }: ResearchRevenueProps): JSX.Element {
  const [showGate, setShowGate] = useState(false);
  const withRevenue = data.series.filter((s) => s.revenue);
  const zeroAtMid = withRevenue.filter((s) => s.revenue!.scenarios.mid.monetized_views === 0).length;
  const earnsAtHigh = withRevenue.filter((s) => s.revenue!.scenarios.high.monetized_views > 0).length;

  if (withRevenue.length === 0) {
    return <p className="muted">这份数据集还没有收益模型（由 tools/yt_revenue_model.py 生成）。</p>;
  }

  const a = withRevenue[0].revenue!.assumptions;

  return (
    <div className="research-rev">
      <div className="research-rev-headline">
        <strong>
          {zeroAtMid === 0
            ? `这 ${withRevenue.length} 个系列在中位情形下都能在 6 个月内赚到钱`
            : `按中位情形，${withRevenue.length} 个系列里有 ${zeroAtMid} 个在 6 个月内的广告收入是 $0`}
        </strong>
        —— 决定这件事的不是 RPM，是<strong>能不能在第 4 个月前过 YouTube 的变现门槛</strong>
        （{a.ypp_subs} 订阅 ＋ {a.ypp_watch_hours} 小时观看）。门槛之前，任何播放量的 AdSense
        收入都严格等于 $0；过了门槛，也只有其后的播放才开始计费。
        {zeroAtMid === 0
          ? `本表已按此标准剔除 6 个月回报低于 $${a.payout_floor_usd} 的系列。`
          : `只有在乐观情形下才有 ${earnsAtHigh} 个系列开始产生收入。`}
      </div>

      <div className="research-rev-tablewrap">
        <table className="research-rev-table">
          <thead>
            <tr>
              <th scope="col" className="research-rev-rank">#</th>
              <th scope="col">系列 / 市场</th>
              {COLS.map((c) => (
                <th key={c.id} scope="col" title={c.hint}>
                  {c.label}
                  <span className="research-rev-hint">{c.hint}</span>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {withRevenue.map((s) => (
              <Row key={s.slug} series={s} onOpen={() => onOpenSeries(s.slug)} />
            ))}
          </tbody>
        </table>
      </div>

      <section className="research-rev-model">
        <h3>模型是怎么算的（可复核）</h3>
        <ul>
          <li>
            <b>播放量</b>：不取本数据集的中位数（那些来自已有几十万订阅的号），而是实测这些赛道里
            <b>近 10 个月内从零开号</b>的频道，按单人可持续产能归一化后取低/中/高。
          </li>
          <li>
            <b>订阅换算</b>：每 {a.views_per_sub} 次播放约 1 个订阅——这是从本轮实测的新号里量出来的比例，不是行业均值。
          </li>
          <li>
            <b>观看小时</b>：播放量 × 该系列样本时长中位 × {Math.round(a.retention * 100)}% 完播率。
          </li>
          <li>
            <b>爬升形状</b>：按实测，前两个月几乎为零（累计占比 {a.ramp_share_by_month.slice(0, 2).map((x) => `${Math.round(x * 100)}%`).join(" / ")}），
            绝大部分播放产生在第 3–6 个月。
          </li>
          <li>
            <b>只有过门槛之后的播放才计入收入</b>，再加 {a.review_lag_months} 个月审核期；
            算出来不足 ${a.payout_floor_usd} 起付线的会标出来——那笔钱当期拿不到。
          </li>
        </ul>
      </section>

      {data.revenue_gate ? (
        <section className="research-rev-model">
          <button
            type="button"
            className="research-rev-toggle"
            aria-expanded={showGate}
            onClick={() => setShowGate(!showGate)}
          >
            {showGate ? "▾" : "▸"} 变现门槛与政策原文（含 2027-02-01 门槛翻倍）
          </button>
          {showGate ? (
            <div className="research-rev-gatebody">
              <p><Rich text={data.revenue_gate} /></p>
              {data.revenue_caveats ? <p><Rich text={data.revenue_caveats} /></p> : null}
            </div>
          ) : null}
        </section>
      ) : null}
    </div>
  );
}
