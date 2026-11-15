import { cleanup, render, screen, within } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { afterEach, expect, it, vi } from "vitest";
import { fetchFile } from "../src/api";
import { EpisodePreviewPage } from "../src/components/EpisodePreviewPage";
import { StoryboardPreviewPage } from "../src/components/StoryboardPreviewPage";
import { audioPreviewHref, previewFile } from "../src/lib/episodePreview";

vi.mock("../src/api", async importOriginal => ({ ...await importOriginal<typeof import("../src/api")>(), fetchFile: vi.fn() }));
afterEach(() => { cleanup(); vi.clearAllMocks(); });

const TOPIC = "edu_videos/tansuo/t01_inside_a_chip";
const file = (content: unknown) => ({ path: "x", content: JSON.stringify(content), etag: "e", size: 1, mtime: 1 }) as unknown as Awaited<ReturnType<typeof fetchFile>>;

it("names the audio preview file and link per language (follow-up 359)", () => {
  expect(previewFile(TOPIC, null, true)).toBe(`${TOPIC}/audio_preview.json`);
  expect(previewFile(TOPIC, "en", true)).toBe(`${TOPIC}/audio_preview.en.json`);
  expect(previewFile(TOPIC, "en")).toBe(`${TOPIC}/preview.en.json`);
  expect(audioPreviewHref(TOPIC)).toBe(`/episode-preview?path=${encodeURIComponent(TOPIC)}&audio=1`);
  expect(audioPreviewHref(TOPIC, "en")).toContain("&lang=en");
});

it("plays the audio preview with scene and shot bars, the current board image and the spoken line", async () => {
  vi.mocked(fetchFile).mockImplementation(async path => {
    if (path === `${TOPIC}/audio_preview.json`) return file({
      title: "t01 · 音频预览", audio: `${TOPIC}/audio/preview/preview.m4a`, duration: 12,
      chapters: [{ id: "b1", title: "1 冷开场", t: 0 }, { id: "b2", title: "2 黑壳", t: 7 }],
      items: [{ t: 0, end: 7, title: "P01 · 冷开场", chapter: "b1", image: `${TOPIC}/storyboard/P01.png`, subtitle: "阿凯：就这么一片？" },
              { t: 7, end: 12, title: "P03 · 黑壳", chapter: "b2", image: `${TOPIC}/storyboard/P03.png` }],
      cues: [{ t: 0.6, end: 3, who: "阿凯", text: "就这么一片？" }],
    });
    throw new Error(`unexpected ${path}`);
  });
  const { container } = render(<MemoryRouter initialEntries={[`/episode-preview?path=${TOPIC}&audio=1`]}>
    <Routes><Route path="/episode-preview" element={<EpisodePreviewPage />} /></Routes></MemoryRouter>);
  expect(await screen.findByText(/音频预览 · tansuo · t01_inside_a_chip/)).toBeTruthy();
  expect(container.querySelector("audio")?.getAttribute("src")).toContain("preview.m4a");
  expect(container.querySelector("video")).toBeNull();
  expect(container.querySelectorAll(".ep-timeline .ep-seg")).toHaveLength(2);
  expect(screen.getAllByRole("tab").map(t => t.textContent)).toEqual(["0:00 1 冷开场", "0:07 2 黑壳"]);
  // 播放前第 0 秒：大图是第一镜的故事板
  expect(container.querySelector(".ep-audio-frame img")?.getAttribute("src")).toContain("P01.png");
});

it("says how to build the audio preview when there is none", async () => {
  vi.mocked(fetchFile).mockRejectedValue(new Error("404"));
  render(<MemoryRouter initialEntries={[`/episode-preview?path=${TOPIC}&audio=1`]}>
    <Routes><Route path="/episode-preview" element={<EpisodePreviewPage />} /></Routes></MemoryRouter>);
  expect((await screen.findByRole("alert")).textContent).toContain("tools/audio_preview.py build");
});

it("lays out a non-drama storyboard like the filming page: scenes, cards, durations and a link to the audio preview", async () => {
  vi.mocked(fetchFile).mockImplementation(async path => {
    if (path === `${TOPIC}/storyboard/storyboard.json`) return file({
      title: "芯片 t01", lang: "zh", notes: ["台词是草稿"],
      scenes: [{ id: "b1", location: "冷开场", time: "比例尺 1 cm", purpose: "抛出问题", question: "放得下吗？", total: 13, shots: [
        { id: "P01", key: "P01", duration: 7, cast: ["林", "凯"], dialogue: [{ speaker: "阿凯", direction: "", text: "就这么一片？" }], action: "冷开场", beats: "", camera: "", blocking: "",
          image: { path: `${TOPIC}/storyboard/P01.png`, mtime: 5 }, framePrompt: "", packPrompt: "", shotDir: "" },
        { id: "P02", key: "P02", duration: 6, cast: [], dialogue: [], action: "缩小", beats: "", camera: "", blocking: "", image: null, framePrompt: "", packPrompt: "", shotDir: "" },
      ] }],
    });
    throw new Error(`unexpected ${path}`);
  });
  render(<MemoryRouter initialEntries={[`/storyboard-preview?path=${TOPIC}`]}>
    <Routes><Route path="/storyboard-preview" element={<StoryboardPreviewPage />} /></Routes></MemoryRouter>);
  const scene = await screen.findByRole("region", { name: "场次 b1" });
  expect(within(scene).getByText("问：放得下吗？")).toBeTruthy();
  const cards = within(scene).getAllByRole("listitem", { name: /^镜头 / });
  expect(cards.map(c => c.getAttribute("aria-label"))).toEqual(["镜头 P01", "镜头 P02"]);
  expect(within(cards[0]).getByText("7 秒")).toBeTruthy();
  expect(within(cards[1]).getByText("首帧待出")).toBeTruthy();
  expect(screen.getByRole("link", { name: "音频预览" }).getAttribute("href")).toContain("audio=1");
});
