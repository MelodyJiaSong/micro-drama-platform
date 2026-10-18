/** Lazy sidebar tree and live file changes (follow-up 280). */
import { act, render, screen, fireEvent } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";
import { applyLoaded, knownPredicate, lazyAncestors, lazyDirs, staleAfter, type LoadedDir } from "../src/lib/lazyTree";
import { subscribeFileChanges, touches } from "../src/lib/fileEvents";
import { Sidebar } from "../src/components/Sidebar";
import { GlobalWorkflowProvider } from "../src/components/GlobalWorkflowContext";
import type { TreeNode } from "../src/types";

const stub = (path: string): TreeNode => ({ type: "directory", name: path.split("/").pop()!, path, children: [], lazy: true });
const file = (path: string): TreeNode => ({ type: "file", name: path.split("/").pop()!, path });

function base(): TreeNode {
  const shot = "ai_videos/d/episodes/ep01/scenes/s1/shots/st1";
  return {
    type: "section", name: "root", path: "", children: [{
      type: "section", name: "AI Videos", path: "", children: [{
        type: "directory", name: "d", path: "ai_videos/d", is_drama: true, children: [
          { type: "directory", name: "filming", path: "ai_videos/d/stages/filming", children: [
            { type: "directory", name: "st1", path: "x/filming/st1", children: [stub(`${shot}/renders`), file(`${shot}/prompt.txt`)] }] },
          { type: "directory", name: "prompts", path: "ai_videos/d/stages/prompts", children: [
            { type: "directory", name: "st1", path: "x/prompts/st1", children: [stub(`${shot}/renders`)] }] },
        ],
      }],
    }],
  };
}

const RENDERS = "ai_videos/d/episodes/ep01/scenes/s1/shots/st1/renders";

describe("lazyTree", () => {
  it("fills every occurrence of a loaded stub and keeps the rest untouched", () => {
    const loaded = new Map<string, LoadedDir>([[RENDERS, { depth: 1, children: [stub(`${RENDERS}/take1`)] }]]);
    const tree = applyLoaded(base(), loaded);
    const filled = (tree.children![0].children![0].children!).map(stage => stage.children![0].children![0]);
    expect(filled.map(n => [n.lazy, n.children!.map(c => c.path)])).toEqual([
      [undefined, [`${RENDERS}/take1`]], [undefined, [`${RENDERS}/take1`]]]);
    expect(lazyDirs(tree)).toEqual([`${RENDERS}/take1`]);
  });

  it("does not replace a folder the first load already listed unless loaded in full", () => {
    const listed = new Map<string, LoadedDir>([["ai_videos/d", { depth: 1, children: [file("ai_videos/d/raw.md")] }]]);
    expect(applyLoaded(base(), listed).children![0].children![0].children!.map(c => c.name)).toEqual(["filming", "prompts"]);
    const full = new Map<string, LoadedDir>([["ai_videos/d", { depth: 0, children: [file("ai_videos/d/raw.md")] }]]);
    expect(applyLoaded(base(), full).children![0].children![0].children!.map(c => c.name)).toEqual(["raw.md"]);
  });

  it("finds the lazy folders on the way to a file", () => {
    expect(lazyAncestors(base(), `${RENDERS}/take1/a.mp4`)).toEqual([RENDERS]);
    expect(lazyAncestors(base(), "ai_videos/d/README.md")).toEqual([]);
  });

  it("knows which part of the tree a batch of changes makes stale", () => {
    const loaded = new Map<string, LoadedDir>([[RENDERS, { depth: 1, children: [] }]]);
    expect(staleAfter(base(), loaded, [`${RENDERS}/take2/review.md`])).toEqual({ base: false, dirs: [RENDERS] });
    expect(staleAfter(base(), loaded, ["ai_videos/d/episodes/ep01/filming.json"])).toEqual({ base: true, dirs: [] });
    expect(staleAfter(base(), loaded, ["*"])).toEqual({ base: true, dirs: [RENDERS] });
  });

  it("treats links into unloaded folders as known", () => {
    const isKnown = knownPredicate(["ai_videos/d/README.md"], [RENDERS]);
    expect(isKnown("ai_videos/d/README.md")).toBe(true);
    expect(isKnown(`${RENDERS}/take1/review.md`)).toBe(true);
    expect(isKnown("ai_videos/d/missing.md")).toBe(false);
  });
});

class FakeEventSource {
  static last: FakeEventSource | null = null;
  listeners: Record<string, ((e: MessageEvent<string>) => void)[]> = {};
  closed = false;
  constructor(public url: string) { FakeEventSource.last = this; }
  addEventListener(type: string, fn: (e: MessageEvent<string>) => void): void { (this.listeners[type] ||= []).push(fn); }
  close(): void { this.closed = true; }
  emit(paths: string[]): void { for (const fn of this.listeners.change ?? []) fn({ data: JSON.stringify({ paths }) } as MessageEvent<string>); }
}

describe("fileEvents", () => {
  afterEach(() => { vi.unstubAllGlobals(); });

  it("shares one /api/events stream and closes it with the last listener", () => {
    vi.stubGlobal("EventSource", FakeEventSource);
    const seen: string[][] = [];
    const a = subscribeFileChanges(paths => seen.push(paths));
    const b = subscribeFileChanges(() => undefined);
    const src = FakeEventSource.last!;
    expect(src.url).toBe("/api/events");
    src.emit(["ai_videos/d/x.md"]);
    expect(seen).toEqual([["ai_videos/d/x.md"]]);
    a(); expect(src.closed).toBe(false);
    b(); expect(src.closed).toBe(true);
  });

  it("matches a folder prefix, the folder itself and a reset", () => {
    expect(touches(["ai_videos/d/ep01/story.json"], "ai_videos/d/ep01")).toBe(true);
    expect(touches(["ai_videos/d/ep010/story.json"], "ai_videos/d/ep01")).toBe(false);
    expect(touches(["*"], "ai_videos/d/ep01")).toBe(true);
  });
});

describe("Sidebar with lazy folders", () => {
  it("shows a lazy folder as expandable and asks for its contents when opened", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify({ groups: [], sources: [], categories: [] }), { status: 200 })));
    const onExpandLazy = vi.fn();
    const tree: TreeNode = { type: "section", name: "root", path: "", children: [{ type: "section", name: "AI Videos", path: "", children: [
      { type: "directory", name: "old", path: "ai_videos/old", children: [stub("ai_videos/old/assets")] }] }] };
    render(<MemoryRouter><GlobalWorkflowProvider><Sidebar tree={tree} currentPath="" onSelect={() => undefined} onExpandLazy={onExpandLazy} /></GlobalWorkflowProvider></MemoryRouter>);
    await act(async () => { fireEvent.click(screen.getByText("old")); });
    const folder = screen.getByText("assets").closest('[role="treeitem"]')!;
    expect(folder.getAttribute("aria-expanded")).toBe("false");
    await act(async () => { fireEvent.click(screen.getByText("assets")); });
    expect(onExpandLazy).toHaveBeenCalledWith("ai_videos/old/assets");
    vi.unstubAllGlobals();
  });
});
