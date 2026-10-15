import { describe, expect, it, beforeAll } from "vitest";
import { fireEvent, render, screen, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { GLOSSARY, glossaryProblems, inGraph, relationsOf, type Glossary } from "../src/lib/glossary";
import { GlossaryPage } from "../src/components/GlossaryPage";

beforeAll(() => {
  // React Flow measures its container; jsdom has no layout engine.
  globalThis.ResizeObserver ??= class { observe(): void {} unobserve(): void {} disconnect(): void {} } as unknown as typeof ResizeObserver;
});

describe("glossary data", () => {
  it("has no dangling relations, unknown categories or bad timeline spans", () => {
    expect(glossaryProblems(GLOSSARY)).toEqual([]);
  });
  it("defines every term in both languages and keeps the graph to structural units", () => {
    for (const term of GLOSSARY.terms) expect([term.zh, term.en, term.def_zh, term.def_en].every(text => text.length > 0)).toBe(true);
    const graphIds = new Set(GLOSSARY.terms.filter(inGraph).map(term => term.id));
    for (const id of ["series", "season", "episode", "act", "sequence", "scene", "shot", "cue", "beat"]) expect(graphIds.has(id)).toBe(true);
    expect(graphIds.has("master")).toBe(false);
  });
  it("answers the structure question: two trees share the scene, and they cross many-to-many", () => {
    const scene = relationsOf(GLOSSARY, "scene");
    expect(scene.some(entry => entry.other === "episode" && entry.relation.type === "contains")).toBe(true);
    expect(scene.some(entry => entry.other === "sequence" && entry.relation.type === "contains")).toBe(true);
    const crosses = GLOSSARY.relations.filter(relation => relation.type === "crosses").map(relation => `${relation.from}-${relation.to}:${relation.card}`);
    expect(crosses).toEqual(expect.arrayContaining(["episode-act:N:M", "episode-sequence:N:M"]));
  });
  it("reports broken data", () => {
    const broken: Glossary = { ...GLOSSARY, relations: [...GLOSSARY.relations, { from: "scene", to: "nope", type: "contains", card: "1:N", zh: "" }] };
    expect(glossaryProblems(broken)).toContain("dangling relation scene→nope");
  });
});

describe("glossary page", () => {
  const renderPage = () => render(<MemoryRouter><GlossaryPage /></MemoryRouter>);

  it("opens on the graph with the shared scene selected", () => {
    renderPage();
    const detail = screen.getByLabelText("术语详情");
    expect(within(detail).getByRole("heading", { level: 2 })).toHaveTextContent("场");
    expect(within(detail).getByText("区分与分歧")).toBeInTheDocument();
    expect(screen.getByLabelText("术语关系图")).toBeInTheDocument();
  });

  it("shows both timelines and selects a term from a row label", () => {
    renderPage();
    fireEvent.click(screen.getByRole("tab", { name: "时间轴" }));
    expect(screen.getAllByRole("img").length).toBe(GLOSSARY.timelines.length);
    fireEvent.click(screen.getAllByRole("button", { name: "选择术语：配乐提示" })[0]);
    expect(within(screen.getByLabelText("术语详情")).getByRole("heading", { level: 2 })).toHaveTextContent("配乐提示");
  });

  it("lists every term, including ones kept off the graph, and filters by search", () => {
    renderPage();
    fireEvent.click(screen.getByRole("tab", { name: "术语列表" }));
    expect(screen.getAllByRole("row")).toHaveLength(GLOSSARY.terms.length + 1);
    fireEvent.change(screen.getByLabelText("搜索术语"), { target: { value: "coverage" } });
    const rows = screen.getAllByRole("row").slice(1);
    expect(rows.length).toBeGreaterThan(0);
    expect(rows.some(row => within(row).queryByText("覆盖"))).toBe(true);
    fireEvent.click(within(rows.find(row => within(row).queryByText("覆盖"))!).getByRole("button", { name: "覆盖" }));
    expect(within(screen.getByLabelText("术语详情")).getByRole("heading", { level: 2 })).toHaveTextContent("覆盖");
  });
});
