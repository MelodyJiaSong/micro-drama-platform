import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { MemoryRouter, Route, Routes, useLocation } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";
import { DramaPage } from "../src/components/DramaPage";
import { Home } from "../src/components/Home";
import { Sidebar } from "../src/components/Sidebar";
import { importFromDownloads } from "../src/api";
import { loadWorkflow, type EpisodeWorkflow } from "../src/lib/episodeWorkflow";
import type { TreeNode } from "../src/types";

vi.mock("../src/api", async importOriginal => ({ ...await importOriginal<typeof import("../src/api")>(), importFromDownloads: vi.fn() }));
vi.mock("../src/lib/episodeWorkflow", async importOriginal => ({ ...await importOriginal<typeof import("../src/lib/episodeWorkflow")>(), loadWorkflow: vi.fn() }));
afterEach(() => { cleanup(); vi.clearAllMocks(); vi.restoreAllMocks(); });

const OLD_NOTE = "ai_videos/old_drama/OBSOLETE.md";
const SERIES_NOTE = "ai_videos/old_series/OBSOLETE.md";
const tree: TreeNode = {
  type: "section", name: "root", path: "", children: [{
    type: "section", name: "AI Videos", path: "", children: [
      { type: "directory", name: "new_drama", path: "ai_videos/new_drama", is_drama: true, workflow: "three-module-v1", display_name: "新剧",
        children: [{ type: "directory", name: "2_世界观人设", path: "ai_videos/new_drama/2_世界观人设", display_name: "1_资产库", children: [] }] },
      { type: "directory", name: "old_drama", path: "ai_videos/old_drama", is_drama: true, obsolete: true, obsolete_note: OLD_NOTE, display_name: "旧剧",
        children: [{ type: "file", name: "OBSOLETE.md", path: OLD_NOTE }] },
      { type: "series", name: "old_series", path: "ai_videos/old_series", obsolete: true, obsolete_note: SERIES_NOTE, display_name: "旧系列",
        children: [
          { type: "directory", name: "ep1", path: "ai_videos/old_series/ep1", is_drama: true, obsolete: true, obsolete_note: SERIES_NOTE,
            children: [{ type: "file", name: "README.md", path: "ai_videos/old_series/ep1/README.md" }] },
          { type: "file", name: "OBSOLETE.md", path: SERIES_NOTE },
        ] },
    ],
  }],
};

const importResult = { moved: [{ from: "~/Downloads/ep1_s1_st1.mp4", to: "x", kind: "shot" }], unmatched: [], errors: [],
  rename: { renamed: [], skipped: [], errors: [] } };

function LocationProbe(): JSX.Element {
  const location = useLocation();
  return <p data-testid="location">{location.pathname + location.search}</p>;
}

function dramaPage(search: string, onChange = vi.fn()): void {
  render(
    <MemoryRouter initialEntries={[`/drama?${search}`]}>
      <Routes>
        <Route path="/drama" element={<DramaPage tree={tree} onChange={onChange} />} />
        <Route path="*" element={<LocationProbe />} />
      </Routes>
    </MemoryRouter>,
  );
}

function row(container: HTMLElement, path: string): HTMLElement {
  const el = container.querySelector<HTMLElement>(`[data-path="${path}"]`);
  if (!el) throw new Error(`no tree row for ${path}`);
  return el;
}

describe("obsolete badge in the sidebar", () => {
  it("marks obsolete dramas, series and inherited members, and nothing else", () => {
    const { container } = render(<MemoryRouter><Sidebar tree={tree} currentPath="" onSelect={() => {}} /></MemoryRouter>);
    expect(within(row(container, "ai_videos/old_drama")).getByText("已过时")).toHaveAttribute("title", `已过时 — 说明见 ${OLD_NOTE}`);
    expect(within(row(container, "ai_videos/old_series")).getByText("已过时")).toBeInTheDocument();
    expect(within(row(container, "ai_videos/new_drama")).queryByText("已过时")).toBeNull();
    // A series member inherits its series' mark.
    fireEvent.click(within(row(container, "ai_videos/old_series")).getByRole("button", { name: "Expand" }));
    expect(within(row(container, "ai_videos/old_series/ep1")).getByText("已过时")).toHaveAttribute("title", `已过时 — 说明见 ${SERIES_NOTE}`);
  });

  it("drops the old library and project-type affordances", () => {
    const { container } = render(<MemoryRouter><Sidebar tree={tree} currentPath="" onSelect={() => {}} /></MemoryRouter>);
    expect(container.querySelector(".subtype-badge")).toBeNull();
    expect(screen.queryByText(/导入检验视频/)).toBeNull();
  });
});

describe("drama page", () => {
  it("keeps 导入 and 角色画廊 on a six-module drama's landing page", async () => {
    vi.mocked(importFromDownloads).mockResolvedValue(importResult);
    const onChange = vi.fn();
    dramaPage("drama=ai_videos%2Fnew_drama", onChange);
    expect(screen.getByRole("heading", { name: "新剧" })).toBeInTheDocument();
    expect(screen.queryByText("已过时")).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "📥 导入" }));
    await waitFor(() => expect(onChange).toHaveBeenCalled());
    expect(importFromDownloads).toHaveBeenCalledWith("ai_videos/new_drama");
    fireEvent.click(screen.getByRole("button", { name: "🎭 角色画廊" }));
    expect(screen.getByTestId("location")).toHaveTextContent("/characters?drama=ai_videos%2Fnew_drama");
  });

  it("keeps both entries above the episode workflow and reloads it after an import", async () => {
    vi.mocked(loadWorkflow).mockResolvedValue({ episode_path: "ai_videos/new_drama/episodes/ep01", shot_keys: {}, modules: [] } as unknown as EpisodeWorkflow);
    vi.mocked(importFromDownloads).mockResolvedValue(importResult);
    dramaPage("drama=ai_videos%2Fnew_drama&module=prompts&episode=ep01");
    expect(await screen.findByText(/创作工作台/)).toBeInTheDocument();
    expect(loadWorkflow).toHaveBeenCalledTimes(1);
    expect(screen.getByRole("button", { name: "🎭 角色画廊" })).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "📥 导入" }));
    await waitFor(() => expect(loadWorkflow).toHaveBeenCalledTimes(2));
    expect(importFromDownloads).toHaveBeenCalledWith("ai_videos/new_drama");
  });

  it("shows the badge on an obsolete drama, links its note, and confirms before importing into it", () => {
    const confirm = vi.spyOn(window, "confirm").mockReturnValue(false);
    dramaPage("drama=ai_videos%2Fold_drama");
    expect(screen.getByRole("heading", { name: "旧剧" })).toBeInTheDocument();
    expect(screen.getByText("已过时")).toBeInTheDocument();
    expect(screen.queryByText(/剧集制作台|分集总览|导出 production/)).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "📥 导入" }));
    expect(confirm).toHaveBeenCalled();
    expect(importFromDownloads).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole("button", { name: "📄 过时说明" }));
    expect(screen.getByTestId("location")).toHaveTextContent(`/file/${encodeURIComponent(OLD_NOTE)}`);
  });

  it("treats a series member as obsolete through its series' note", () => {
    dramaPage("drama=ai_videos%2Fold_series%2Fep1");
    expect(screen.getByText("已过时")).toHaveAttribute("title", `已过时 — 说明见 ${SERIES_NOTE}`);
  });
});

describe("home page", () => {
  it("lists every drama with its obsolete mark", () => {
    render(<MemoryRouter><Home tree={tree} /></MemoryRouter>);
    const items = screen.getAllByRole("listitem");
    expect(items.map(item => item.textContent)).toEqual(["新剧 · 六模块", "旧剧已过时", "ep1已过时"]);
  });
});
