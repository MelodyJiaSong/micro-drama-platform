import { afterEach, describe, expect, it, vi } from "vitest";
import { render, screen, within } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { ProcessQcDramaPage, ProcessQcRepoPage } from "../src/components/ProcessQcPage";
import { byStage, promoteInstruction, type QcCheck } from "../src/lib/processQc";

const check = (id: string, stage: string, level: string, extra: Partial<QcCheck> = {}): QcCheck => ({
  id, stage, kind: "review", gate: true, auto: false, level, when: "", desc: `${id} 说明`, how: "", basis: "", sources: [], ...extra,
});
const health = { window_days: 7, followups: 5, logged: 4, duplicates: [45], pending: 1, last_number: 257 };
const REPO = {
  stages: ["ref_image", "video"],
  checks: [check("video.no_text", "video", "仓库级", { kind: "machine", basis: "共用规则：不烧字幕" })],
  dramas: [
    { drama: "ai_videos/dota_yingxiong", spec: "dota_yingxiong", enabled: true, drama_checks: 12, defects: 10, user_caught: 10, false_positives: 0, escape_rate: 1, renders_total: 0, followup: health },
    { drama: "ai_videos/quiet", spec: "quiet", enabled: false, drama_checks: 0, defects: 0, user_caught: 0, false_positives: 0, escape_rate: null, renders_total: 0, followup: { ...health, followups: 0, logged: 0, duplicates: [], pending: 0 } },
  ],
};
const DRAMA = {
  drama: "ai_videos/dota_yingxiong", spec: "dota_yingxiong", enabled: true, stages: ["ref_image", "video"],
  drama_checks: [check("video.scale", "video", "剧级", { sources: ["dota_yingxiong#245"] })],
  repo_checks: REPO.checks,
  defects: [{ ts: "", category: "video.scale", caught_by: "user", artifact: "", followup: "245", note: "体型要加大" }],
  escapes: [{ ts: "", category: "video.scale", caught_by: "user", artifact: "", followup: "245", note: "体型要加大", reason: "闸门建立前交付", action: "只计入基线", level: "剧级" }],
  escape_rate: 1, renders: [{ path: "ai_videos/dota_yingxiong/x/renders/20261026-130000_a", artifact: "a.mp4", verdicts: { "video.scale": "pass", "video.timeline": "未审" } }],
  renders_total: 1, followup: health,
};

function mockFetch(): void {
  vi.stubGlobal("fetch", vi.fn(async (url: string) => new Response(JSON.stringify(url.includes("/drama") ? DRAMA : REPO), { status: 200 })));
}
afterEach(() => vi.unstubAllGlobals());

describe("流程与自检：两层分开", () => {
  it("仓库级页只列仓库级检查，并按剧汇总；没有记录的剧不出现", async () => {
    mockFetch();
    render(<MemoryRouter><ProcessQcRepoPage /></MemoryRouter>);
    expect(await screen.findByText("video.no_text")).toBeTruthy();
    expect(screen.getByText(/对所有剧生效，影响面大/)).toBeTruthy();
    expect(screen.getByText("共用依据：共用规则：不烧字幕")).toBeTruthy();
    expect(screen.queryByText("video.scale")).toBeNull();                       // 剧级检查不混进仓库级页
    const table = screen.getByRole("table");
    expect(within(table).getByRole("link", { name: "dota_yingxiong" }).getAttribute("href")).toBe("/qc?drama=ai_videos%2Fdota_yingxiong");
    expect(within(table).queryByText("quiet")).toBeNull();
    expect(within(table).getByText(/撞号 45/)).toBeTruthy();
  });

  it("剧级页把本剧检查与继承自仓库级的分开，并给出逃逸原因与可复制的指令", async () => {
    mockFetch();
    render(<MemoryRouter initialEntries={["/qc?drama=ai_videos%2Fdota_yingxiong"]}><Routes><Route path="/qc" element={<ProcessQcDramaPage />} /></Routes></MemoryRouter>);
    expect(await screen.findByText(/只对本剧生效/)).toBeTruthy();
    const inherited = screen.getByText(/继承自仓库级/).closest("details")!;
    expect(within(inherited).getByText("video.no_text")).toBeTruthy();          // 仓库级只在「继承」折叠区里
    expect(within(inherited).queryByText("video.scale")).toBeNull();           // 剧级检查不进继承区
    expect(screen.getAllByText("video.scale")).toHaveLength(2);                // 本剧检查列表 + 逃逸分析
    expect(screen.getByText("闸门建立前交付")).toBeTruthy();
    expect(screen.getByRole("button", { name: /复制给代理/ })).toBeTruthy();
    expect(screen.getByRole("button", { name: /提议升仓库级/ })).toBeTruthy();
    expect(screen.getByText(/video.timeline 未审/)).toBeTruthy();
  });
});

describe("processQc 纯函数", () => {
  it("按流程顺序分组，未知环节排在最后不被吞掉", () => {
    const groups = byStage([check("a", "video", "剧级"), check("b", "mystery", "剧级"), check("c", "ref_image", "剧级")], ["ref_image", "video"]);
    expect(groups.map(([s]) => s)).toEqual(["ref_image", "video", "mystery"]);
  });

  it("升仓库级的指令要求先拿证据、用户明确同意前不改仓库级", () => {
    const text = promoteInstruction("ai_videos/dota_yingxiong", check("video.scale", "video", "剧级"));
    expect(text).toContain("明确同意之前不要改");
    expect(text).toContain(".agents/references/project/qc_checks.toml");
  });
});

describe("逃逸指令按层级分开", () => {
  it("仓库级检查的逃逸要先征得同意，剧级的只改剧级", async () => {
    const { escapeInstruction } = await import("../src/lib/processQc");
    const base = { ts: "", category: "video.subject_count", caught_by: "user", artifact: "", followup: "084", note: "", reason: "检查放过了", action: "收紧" };
    expect(escapeInstruction("ai_videos/dota_yingxiong", { ...base, level: "仓库级" })).toContain("征得我同意后才改");
    const local = escapeInstruction("ai_videos/dota_yingxiong", { ...base, level: "剧级" });
    expect(local).toContain("不要动仓库级");
    expect(local).not.toContain("征得我同意");
  });
});
