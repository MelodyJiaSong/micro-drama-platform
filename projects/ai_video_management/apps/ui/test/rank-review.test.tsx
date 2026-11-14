import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, expect, it, vi } from "vitest";
import { RankPreviewPage } from "../src/components/RankPreviewPage";
import { fetchFile, fetchSubtree } from "../src/api";
import { rankPreviewHref } from "../src/lib/rankPreview";
import { defaultVideo, formatDuration, type RankEpisode, type RankEpisodeCard, type RankImage, type RankVideo } from "../src/lib/rankReview";

vi.mock("../src/api", async original => ({ ...await original<typeof import("../src/api")>(), fetchFile: vi.fn(), fetchSubtree: vi.fn() }));
vi.mock("../src/lib/fileEvents", () => ({ useFileChanges: vi.fn(), subscribeFileChanges: vi.fn(() => () => undefined) }));
afterEach(() => { cleanup(); vi.clearAllMocks(); vi.unstubAllGlobals(); });

const SERIES = "ai_videos/paihangbang";
const EP = `${SERIES}/episodes/ep12_area`;
const stats = { items: 2, with_image: 2, missing: 0, risk: 1, alt: 1, ai: 1 };
const card = (key: string, number: number, extra: Partial<RankEpisodeCard> = {}): RankEpisodeCard => ({
  key, number, path: `${SERIES}/episodes/${key}`, title: `Title ${number}`, n: 2, champion: "Russia", duration_s: 301.4,
  thumbnail: "", verdict: "", music: null, videos: 1, stats, error: "", mode: "rank", first: "", last: "", list_order: "", ...extra,
});
const NO_COMPANY = { corner: "", logo: null, logo_bg: "", person: null, image_alt_credit: "", secondary_display: "", notes: "" };
const video = (name: string, extra: Partial<RankVideo> = {}): RankVideo => ({
  name, path: `${EP}/render/${name}`, label: name, risk: false, music: false, duration_s: 300, complete: true, recommended: false, ...extra,
});
const episode: RankEpisode = {
  card: card("ep12_area", 12, { verdict: "结论：可发布" }), kicker: "TOP 2", theme: "atlas", metric_label: "Area",
  period_label: "Data as of 2026", source_line: "Sources: UN", scope_note: "Land + water.",
  videos: [video("ep12_area_master.mp4", { label: "默认母版 · 无配乐" }),
    video("ep12_area_master_with-risk-images.mp4", { label: "风险图版 · 配乐", risk: true, music: true, recommended: true })],
  verdict_excerpt: "## 结论：可发布\n\n- 小修", qc: { path: `${EP}/qc.md`, text: "# 全文\n## 结论：可发布" },
  publish: { path: "", text: "" }, handoff: { path: `${EP}/_build/handoff.md`, text: "待用户决定：换图" },
  items: [{ rank: 1, name: "Russia", subtitle: "", country_iso2: "RU", country_name: "Russia", flag: `${SERIES}/_assets/flags/ru.png`,
    value_display: "17.1M km²", badge: "", image_risk: "FoP", image_alt: { path: `${EP}/assets/a.jpg`, declared: "assets/a.jpg", licence: "AI-generated (Codex image_gen)", author: "", source: "", ai: true },
    image: { path: `${EP}/assets/r.jpg`, declared: "assets/r.jpg", licence: "CC BY 2.0", author: "Ann", source: "https://x/1", ai: false },
    ...NO_COMPANY }],
  insights: [{ after_rank: 5, text: "Canada has the most lakes." }],
};

function stubApi(body: unknown): void {
  vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify(body), { status: 200 })));
}

it("picks the recommended cut and formats durations", () => {
  expect(defaultVideo(episode.videos)?.name).toBe("ep12_area_master_with-risk-images.mp4");
  expect(defaultVideo([video("a.mp4", { complete: false }), video("b.mp4")])?.name).toBe("b.mp4");
  expect(formatDuration(301.6)).toBe("5:02");
  expect(formatDuration(null)).toBe("—");
});

it("lists the series with ep11–ep20 first and links into each episode", async () => {
  stubApi({ kind: "series", episode: null, series: { path: SERIES, focus: [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    episodes: [card("ep02_peaks", 2, { music: true, verdict: "结论：可发布（静音画面版）" }), card("ep12_area", 12, { videos: 0 })] } });
  render(<MemoryRouter initialEntries={[rankPreviewHref(SERIES)]}><RankPreviewPage /></MemoryRouter>);
  expect(await screen.findByRole("heading", { name: /重点：ep11–ep20（1）/ })).toBeTruthy();
  expect(screen.getByRole("heading", { name: /其他各期（1）/ })).toBeTruthy();
  expect(screen.getByText("成片尚未生成")).toBeTruthy();
  expect(screen.getByText("审片：可发布（静音画面版）")).toBeTruthy();
  expect(screen.getByRole("link", { name: /Title 12/ }).getAttribute("href")).toBe(rankPreviewHref(`${SERIES}/episodes/ep12_area`));
  expect(fetchSubtree).not.toHaveBeenCalled();
});

it("shows the review sections even before data.json exists", async () => {
  vi.mocked(fetchFile).mockRejectedValue(new Error("not found"));
  vi.mocked(fetchSubtree).mockRejectedValue(new Error("not found"));
  stubApi({ kind: "episode", series: null, episode });
  render(<MemoryRouter initialEntries={[rankPreviewHref(EP)]}><RankPreviewPage /></MemoryRouter>);
  expect(await screen.findByText(/data.json 尚未生成或读不了/)).toBeTruthy();
  expect(await screen.findByText("推荐审看")).toBeTruthy();
  const tabs = screen.getAllByRole("tab");
  expect(tabs.map(t => t.getAttribute("aria-selected"))).toEqual(["false", "true"]);
  fireEvent.click(tabs[0]);
  expect(document.querySelector("video")?.getAttribute("src")).toContain(encodeURIComponent("ep12_area_master.mp4"));
  expect(screen.getByText("待用户决定：换图")).toBeTruthy();
  expect(screen.getByText("Land + water.")).toBeTruthy();
  expect(screen.getByText("publish.md 尚未生成。")).toBeTruthy();
  expect(screen.getByText("Canada has the most lakes.")).toBeTruthy();
});

it("renders the card table with flag, both images and risk / AI marks", async () => {
  vi.mocked(fetchFile).mockImplementation(async path => ({ path, content: path.endsWith("data.json")
    ? JSON.stringify({ title: "T", items: [{ rank: 1, name: "Russia" }] }) : "[]" } as Awaited<ReturnType<typeof fetchFile>>));
  vi.mocked(fetchSubtree).mockResolvedValue({ type: "directory", name: "x", path: EP, children: [] });
  stubApi({ kind: "episode", series: null, episode });
  render(<MemoryRouter initialEntries={[rankPreviewHref(EP)]}><RankPreviewPage /></MemoryRouter>);
  expect(await screen.findByRole("heading", { name: /卡片明细/ })).toBeTruthy();
  const row = document.querySelector(".rank-review-row-risk");
  expect(row?.textContent).toContain("⚠ FoP");
  expect(row?.querySelector(".rank-review-flag")?.getAttribute("alt")).toBe("RU");
  expect(row?.querySelector(".rank-review-thumb-ai")).toBeTruthy();
  expect(row?.textContent).toContain("CC BY 2.0 · Ann");
  expect(screen.getByRole("link", { name: "← 系列总览" })).toBeTruthy();
  // follow-up 321：排名期不变——名次列、冠军照旧，没有公司卡字段就不出空列
  const headers = Array.from(document.querySelectorAll(".rank-review-table th")).map(th => th.textContent);
  expect(headers[0]).toBe("名次");
  expect(headers.some(h => /corner|Logo|person|notes/.test(h ?? ""))).toBe(false);
  expect(row?.querySelector("td")?.textContent).toBe("#1");
  expect(screen.getByText("冠军：Russia")).toBeTruthy();
});

const LIST_EP = `${SERIES}/episodes/ep03_ai`;
const img = (declared: string, extra: Partial<RankImage> = {}): RankImage => ({
  path: `${LIST_EP}/${declared}`, declared, licence: "", author: "", source: "", ai: false, ...extra,
});
const listEpisode: RankEpisode = {
  ...episode,
  card: card("ep03_ai", 3, { mode: "list", champion: "", first: "DeepMind", last: "OpenAI", list_order: "成立年份" }),
  insights: [{ after_rank: 1, text: "DeepMind came first." }],
  items: [
    { ...NO_COMPANY, rank: 1, name: "DeepMind", subtitle: "London", country_iso2: "GB", country_name: "United Kingdom", flag: "",
      value_display: "Google-owned", badge: "", corner: "EST. 2010", logo: img("assets/logo/dm.png"), logo_bg: "#0d0b26",
      person: { name: "Demis Hassabis", role: "Co-founder & Chair", image: img("assets/person/dm.jpg"), image_risk: "licence unknown", credit: "" },
      image: img("assets/img/01.jpg"), image_risk: "news-agency photo (Getty/Reuters/AP): highest takedown risk",
      image_alt: img("assets/img/01_alt.jpg", { licence: "AI-generated", ai: true }), image_alt_credit: "AI-generated illustration",
      secondary_display: "since 2014", notes: "Subsidiary: no standalone valuation. Merged with Google Brain Apr 2023." },
    { ...NO_COMPANY, rank: 2, name: "OpenAI", subtitle: "", country_iso2: "US", country_name: "United States", flag: "",
      value_display: "$852B", badge: "", corner: "EST. 2015", image: null, image_alt: null, image_risk: "licence unknown",
      person: { name: "Sam Altman", role: "", image: null, image_risk: "", credit: "" } },
  ],
};

it("list episodes show order, not a champion, plus logo / founder / risk / notes", async () => {
  vi.mocked(fetchFile).mockImplementation(async path => ({ path, content: path.endsWith("data.json")
    ? JSON.stringify({ title: "T", mode: "list", items: [{ rank: 1, name: "DeepMind" }] }) : "[]" } as Awaited<ReturnType<typeof fetchFile>>));
  vi.mocked(fetchSubtree).mockResolvedValue({ type: "directory", name: "x", path: LIST_EP, children: [] });
  stubApi({ kind: "episode", series: null, episode: listEpisode });
  render(<MemoryRouter initialEntries={[rankPreviewHref(LIST_EP)]}><RankPreviewPage /></MemoryRouter>);
  expect(await screen.findByRole("heading", { name: /卡片明细/ })).toBeTruthy();
  expect(screen.queryByText(/冠军/)).toBeNull();
  expect(screen.getAllByText("列表期 · 按成立年份，不排名").length).toBeGreaterThan(0);
  expect(screen.getByText("首个：DeepMind · 末个：OpenAI")).toBeTruthy();
  const headers = Array.from(document.querySelectorAll(".rank-review-table th")).map(th => th.textContent);
  expect(headers).toEqual(["序", "角标 corner", "名称", "Logo", "创始人 person", "国家", "数值", "徽章", "主图 image", "替代图 image_alt", "备注 notes"]);
  const [dm, oa] = Array.from(document.querySelectorAll(".rank-review-table tbody tr"));
  expect(dm.querySelector("td")?.textContent).toBe("1");
  expect(dm.querySelector(".rank-review-corner")?.textContent).toBe("EST. 2010");
  const logo = dm.querySelector<HTMLElement>(".rank-review-logo");
  expect(logo?.style.background).toBe("rgb(13, 11, 38)");
  expect(logo?.querySelector("img")?.getAttribute("src")).toContain(encodeURIComponent(`${LIST_EP}/assets/logo/dm.png`));
  expect(dm.querySelector(".rank-review-avatar-risk")?.getAttribute("src")).toContain(encodeURIComponent(`${LIST_EP}/assets/person/dm.jpg`));
  expect(dm.textContent).toContain("⚠ 头像：licence unknown");
  expect(dm.querySelector(".rank-review-news")?.textContent).toContain("news-agency photo");
  expect(dm.querySelector(".rank-review-credit.rank-review-ai-tag")?.textContent).toBe("署名：AI-generated illustration");
  expect(dm.textContent).toContain("since 2014");
  expect(dm.querySelector(".rank-review-notes details summary")?.textContent).toMatch(/…$/);
  expect(oa.querySelector("td")?.textContent).toBe("2");
  expect(oa.querySelector(".rank-review-initials")?.textContent).toBe("SA");
  expect(oa.querySelector(".rank-review-news")).toBeNull();
  expect(oa.querySelector(".rank-review-risk-text")?.textContent).toBe("⚠ licence unknown");
  expect(oa.querySelector(".rank-review-notes")?.textContent).toBe("—");
  expect(screen.getByText(/序 1 之后/)).toBeTruthy();
});

it("series cards say list period instead of champion", async () => {
  stubApi({ kind: "series", episode: null, series: { path: SERIES, focus: [11],
    episodes: [card("ep02_peaks", 2), card("ep03_ai", 3, { mode: "list", champion: "", first: "DeepMind" })] } });
  render(<MemoryRouter initialEntries={[rankPreviewHref(SERIES)]}><RankPreviewPage /></MemoryRouter>);
  expect(await screen.findByText("列表期 · 不排名")).toBeTruthy();
  expect(screen.getAllByText(/冠军：/)).toHaveLength(1);
});
