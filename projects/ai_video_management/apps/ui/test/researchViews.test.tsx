/** Integration smoke: every research view renders against the REAL shipped
 * dataset. These views are assembled from many parts, so a wiring or contract
 * regression is far more likely than a logic bug — and would otherwise only
 * show up in the browser. */
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it, vi } from "vitest";
import { render, fireEvent, within } from "@testing-library/react";
import { ResearchDashboard } from "../src/components/ResearchDashboard";
import { ResearchSeriesGrid } from "../src/components/ResearchSeriesGrid";
import { ResearchSeriesDetail } from "../src/components/ResearchSeriesDetail";
import { ResearchVideoExplorer } from "../src/components/ResearchVideoExplorer";
import { ResearchCompare } from "../src/components/ResearchCompare";
import { ResearchRevenue } from "../src/components/ResearchRevenue";
import type { ResearchDataset, ResearchWorkspace } from "../src/lib/researchApi";

const DATASET_PATH = resolve(__dirname, "../../../../../ai_videos/_research/2026-09.json");
const data = JSON.parse(readFileSync(DATASET_PATH, "utf-8")) as ResearchDataset;

const workspace: ResearchWorkspace = {
  dataset: "2026-09",
  series: {
    "slow-english-longform-story-serial": { status: "shortlist", rating: 5 },
    "us-senior-benefits-explainer": { status: "doing" },
    "hindi-veggie-anthropomorphic-melodrama": { status: "rejected" },
  },
  videos: {},
};

const noop = (): void => {};

it("the shipped dataset is the shape the views expect", () => {
  expect(data.series.length).toBeGreaterThanOrEqual(5);
  expect(data.series.every((s) => s.videos.length >= 8)).toBe(true);
  expect(data.series.every((s) => s.videos.every((v) => v.upload_date >= "20260306"))).toBe(true);
});

describe("Dashboard", () => {
  it("renders a dot per series and opens one on click", () => {
    const onOpen = vi.fn();
    const { container } = render(
      <ResearchDashboard data={data} workspace={workspace} onOpenSeries={onOpen} />,
    );
    expect(container.querySelectorAll("circle").length).toBeGreaterThanOrEqual(data.series.length);
    expect(container.querySelectorAll("img")).toHaveLength(0); // CSP: img-src 'self'
    expect(container.textContent).not.toContain("**"); // all prose через Rich
  });
});

describe("SeriesGrid", () => {
  it("filters by search text and reports the count", () => {
    const { container } = render(
      <ResearchSeriesGrid
        data={data} workspace={workspace} onOpenSeries={noop}
        onMark={noop} selected={[]} onToggleSelect={noop}
      />,
    );
    const before = container.querySelectorAll(".research-grid-card, .research-sg-card").length;
    expect(before).toBe(data.series.length);
    const search = container.querySelector("input[type='search'], input[type='text']");
    expect(search).not.toBeNull();
    fireEvent.change(search as HTMLInputElement, { target: { value: "英语" } });
    const after = container.querySelectorAll(".research-grid-card, .research-sg-card").length;
    expect(after).toBeLessThan(before);
    expect(after).toBeGreaterThan(0);
  });

  it("reports a status change through onMark", () => {
    const onMark = vi.fn();
    render(
      <ResearchSeriesGrid
        data={data} workspace={workspace} onOpenSeries={noop}
        onMark={onMark} selected={[]} onToggleSelect={noop}
      />,
    );
    const statusBar = document.querySelector(".research-sg-statuses");
    expect(statusBar).not.toBeNull();
    fireEvent.click(within(statusBar as HTMLElement).getByText("短名单"));
    expect(onMark).toHaveBeenCalled();
    const [, patch] = onMark.mock.calls[0];
    expect(patch).toHaveProperty("status");
  });
});

describe("SeriesDetail", () => {
  it("shows the replication steps for the opened series", () => {
    const series = data.series[0];
    const { container } = render(
      <ResearchSeriesDetail
        series={series} mark={{}} videoMarks={{}} onMark={noop}
        onMarkVideo={noop} onClose={noop} onPrev={noop} onNext={noop}
      />,
    );
    expect(container.textContent).toContain(series.name_zh);
    expect(container.querySelectorAll("img")).toHaveLength(0);
  });
});

describe("VideoExplorer", () => {
  it("lists all 100 samples and narrows on search", () => {
    const { container } = render(
      <ResearchVideoExplorer
        data={data} workspace={workspace} onMarkVideo={noop} onOpenSeries={noop}
      />,
    );
    const rows = () => container.querySelectorAll("tbody tr:not(.research-vx-noterow)");
    const total = data.series.reduce((n, s) => n + s.videos.length, 0);
    expect(rows().length).toBe(total);
    const search = container.querySelector("input[type='search'], .research-vx-search");
    fireEvent.change(search as HTMLInputElement, { target: { value: "Senior" } });
    expect(rows().length).toBeLessThan(total);
  });

  it("every sample links to a real youtube watch url", () => {
    const { container } = render(
      <ResearchVideoExplorer
        data={data} workspace={workspace} onMarkVideo={noop} onOpenSeries={noop}
      />,
    );
    const links = Array.from(
      container.querySelectorAll<HTMLAnchorElement>("a[href*='watch?v=']"),
    );
    expect(links.length).toBe(data.series.reduce((n, s) => n + s.videos.length, 0));
    expect(links.every((a) => a.rel.includes("noreferrer"))).toBe(true);
  });
});

describe("Compare", () => {
  it("shows an empty state under two picks and a matrix at two", () => {
    const { container, rerender } = render(
      <ResearchCompare
        data={data} workspace={workspace} selected={[]}
        onToggleSelect={noop} onOpenSeries={noop}
      />,
    );
    expect(container.querySelectorAll("table")).toHaveLength(0);
    rerender(
      <ResearchCompare
        data={data} workspace={workspace}
        selected={[data.series[0].slug, data.series[1].slug]}
        onToggleSelect={noop} onOpenSeries={noop}
      />,
    );
    const table = container.querySelector("table");
    expect(table).not.toBeNull();
    expect(within(table as HTMLElement).getAllByText(/最佳/).length).toBeGreaterThan(0);
  });
});

describe("Revenue", () => {
  it("every series carries a projection whose gate logic is self-consistent", () => {
    for (const s of data.series) {
      expect(s.revenue).toBeDefined();
      for (const key of ["low", "mid", "high"] as const) {
        const sc = s.revenue!.scenarios[key];
        // $0 exactly when the YPP gate never clears inside the window
        if (sc.ypp_cleared_month === null) {
          expect(sc.monetized_views).toBe(0);
          expect(sc.adsense_usd_high).toBe(0);
        }
        // money can never be claimed on views that were never monetized
        expect(sc.monetized_views).toBeLessThanOrEqual(sc.views_6mo);
      }
      // more views can never earn less
      const { low, high } = s.revenue!.scenarios;
      expect(high.views_6mo).toBeGreaterThanOrEqual(low.views_6mo);
      expect(high.adsense_usd_high).toBeGreaterThanOrEqual(low.adsense_usd_high);
    }
  });

  it("renders the table and leads with the gate, not with RPM", () => {
    const { container } = render(<ResearchRevenue data={data} onOpenSeries={noop} />);
    expect(container.querySelectorAll("tbody tr").length).toBeGreaterThanOrEqual(data.series.length);
    expect(container.textContent).toContain("YPP");
    expect(container.querySelectorAll("img")).toHaveLength(0);
  });
});
