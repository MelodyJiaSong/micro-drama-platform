/** Pure geometry for the dashboard scatter: the viewBox constants, the log-X /
 * linear-Y scales derived from the dataset itself, and the tick sets. Kept out
 * of the component so the plot's arithmetic reads on its own. */
import type { ResearchSeries, Thresholds } from "../lib/researchApi";

export const W = 640;
export const H = 420;
const PAD = { top: 24, right: 20, bottom: 54, left: 64 };
export const PW = W - PAD.left - PAD.right;
export const PH = H - PAD.top - PAD.bottom;
export const X0 = PAD.left;
export const X1 = X0 + PW;
export const Y0 = PAD.top;
export const Y1 = Y0 + PH;

/** An annotation anchored beside its dot, folded to stay inside the frame. */
export interface Callout {
  text: string;
  anchor: "start" | "end";
  x: number;
  y: number;
}

export interface Scale {
  sx: (views: number) => number;
  sy: (rate: number) => number;
  /** Where the two median crosshairs land. */
  tx: number;
  ty: number;
  xTicks: number[];
  yTicks: number[];
  callout: (text: string, x: number, y: number, r: number) => Callout;
}

/** 1 / 2 / 5 × 10^k values inside the padded log domain. */
function logTicks(lo: number, hi: number): number[] {
  const out: number[] = [];
  for (let e = Math.floor(Math.log10(lo)); e <= Math.ceil(Math.log10(hi)); e += 1) {
    for (const m of [1, 2, 5]) {
      const v = m * 10 ** e;
      if (v >= lo && v <= hi) out.push(v);
    }
  }
  return out;
}

function rateTicks(top: number): number[] {
  const step = top > 0.08 ? 0.02 : 0.01;
  const out: number[] = [];
  for (let v = 0; v <= top + 1e-9; v += step) out.push(Math.round(v * 10000) / 10000);
  return out;
}

/** Y stops at the next whole percent above the peak, with one more percent of
 * headroom when the peak would otherwise sit on the frame. */
function rateCeiling(peak: number): number {
  const base = Math.ceil(peak * 100) / 100;
  return peak / base > 0.94 ? base + 0.01 : base;
}

export function buildScale(series: ResearchSeries[], limits: Thresholds): Scale {
  const views = series.map((s) => s.stats.median_views);
  const rates = series.map((s) => s.stats.median_like_rate);
  const lgLo = Math.log10(Math.max(1, Math.min(...views, limits.views))) - 0.14;
  const lgHi = Math.log10(Math.max(...views, limits.views)) + 0.14;
  const yTop = rateCeiling(Math.max(...rates, limits.likeRate));

  const sx = (v: number): number =>
    X0 + ((Math.log10(Math.max(v, 1)) - lgLo) / (lgHi - lgLo)) * PW;
  const sy = (r: number): number => Y1 - (r / yTop) * PH;

  return {
    sx,
    sy,
    tx: sx(limits.views),
    ty: sy(limits.likeRate),
    xTicks: logTicks(10 ** lgLo, 10 ** lgHi),
    yTicks: rateTicks(yTop),
    callout: (text, x, y, r) => {
      const anchor: "start" | "end" = x > (X0 + X1) / 2 ? "end" : "start";
      return {
        text,
        anchor,
        x: anchor === "end" ? Math.min(x + r, X1) : Math.max(x - r, X0),
        y: y + r + 13 > Y1 - 4 ? y - r - 8 : y + r + 13,
      };
    },
  };
}
