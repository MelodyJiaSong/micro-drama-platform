import { fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { expect, it, vi } from "vitest";
import { CASES, DEP_EDGES, DEP_NODES, LAWS, STAGES, closure } from "../src/lib/reviewStrategy";
import { wrap } from "../src/components/ReviewStrategyDiagrams";

vi.mock("../src/api", () => ({ fetchProcessQc: () => Promise.reject(new Error("offline")) }));

it("keeps the strategy data self-consistent (follow-up 032)", () => {
  const ids = new Set(DEP_NODES.map(n => n.id));
  for (const e of DEP_EDGES) { expect(ids.has(e.from)).toBe(true); expect(ids.has(e.to)).toBe(true); }
  const stages = new Set(STAGES.map(s => s.id));
  for (const l of LAWS) for (const s of l.stages) expect(stages.has(s)).toBe(true);
  for (const c of CASES) {
    expect(stages.has(c.origin)).toBe(true);
    expect(Object.keys(c.newCatch).length).toBeGreaterThan(0);
  }
});

it("changing the storyboard invalidates everything downstream, not the inputs", () => {
  const { up, down } = closure("filming");
  expect([...down]).toEqual(expect.arrayContaining(["pack", "take", "cut", "ep", "v_pre", "v_take", "v_cut", "v_ep", "ff"]));
  expect(down.has("story")).toBe(false);
  expect([...up]).toEqual(expect.arrayContaining(["story", "bible", "props"]));
  expect(closure("ep").down.has("v_ep")).toBe(true);
});

it("wraps mixed text by character count", () => {
  expect(wrap("一二三四五六七", 3)).toEqual(["一二三", "四五六", "七"]);
  expect(wrap("", 3)).toEqual([]);
});

it("renders the diagrams and switches the stage panel and case", async () => {
  const { ReviewStrategyPage } = await import("../src/components/ReviewStrategyPage");
  render(<MemoryRouter><ReviewStrategyPage /></MemoryRouter>);
  expect(screen.getByRole("img", { name: "六道关主流程图" })).toBeTruthy();
  expect(screen.getByRole("img", { name: "产物依赖图" })).toBeTruthy();
  fireEvent.click(screen.getByRole("button", { name: "④ 单条出片" }));
  expect(screen.getByText("每秒 4 帧拼图 + 手和道具放大图")).toBeTruthy();
  fireEvent.click(screen.getByRole("tab", { name: /硬币凭空出现在鼻子上/ }));
  expect(screen.getByRole("img", { name: "案例：硬币凭空出现在鼻子上" })).toBeTruthy();
});
