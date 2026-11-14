import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { MemoryRouter } from "react-router-dom";
import { expect, it, vi } from "vitest";
import {
  REVIEW_CORRECTIONS_ROUTE, correctionsCommand, correctionsStep, countBy, diffKind, groupCorrections, reviewCorrectionsHref, shotTouched,
  type CorrectionsDoc,
} from "../src/lib/reviewCorrections";
import { reviewRunHref, type ReviewRun } from "../src/lib/reviewRun";
import { reviewIssuesHref } from "../src/lib/reviewV5";

// 修复页（用户 2026-11-08「每一次审计的结果应该 link 到另一个 page……correction，基于 review，我们修复了那些……两边是关联的」）。
// fixture 由 tools/review_run.py 在临时目录真跑出来（test/fixtures/review-corrections/make_fixture.py）：第 1 轮各类都报 s1_st1 物理重出，
// 严重的都 fix 了（带 --file），首帧重画（旧图归档 _r1）、分镜改了一句；第 2 轮物理仍报 s1_st1，别的类干净。
vi.setConfig({ testTimeout: 30000 });

const read = (f: string): string => readFileSync(resolve(__dirname, "fixtures/review-corrections", f), "utf-8");
const doc = JSON.parse(read("r1_corrections.json")) as CorrectionsDoc;
const r1 = JSON.parse(read("r1_checklist.json")) as ReviewRun;
const r2 = JSON.parse(read("r2_checklist.json")) as ReviewRun;
const dir = doc.dir;
const bareDir = "ai_videos/demo/reviews/ep01_20261108-090000_pregen_r1";

// 审查页经 /api/review-runs/checklist 读单（v5 单常超 /api/file 的 1 MiB 上限）；测试里沿用同一份 fetchFile 数据。
const { withChecklist } = vi.hoisted(() => ({
  withChecklist: <T extends { fetchFile: (p: string) => Promise<{ content: string }> }>(m: T) =>
    ({ ...m, fetchReviewChecklist: async (d: string) => JSON.parse((await m.fetchFile(`${d}/checklist.json`)).content) }),
}));
vi.mock("../src/api", () => withChecklist({
  fetchFile: (path: string) => {
    const ok = (content: string) => Promise.resolve({ path, content, encoding: "utf-8", bytes: 1, mtime: 0, mtime_http: "" });
    if (path === `${dir}/checklist.json`) return ok(JSON.stringify(r1));
    if (path === `${dir}/corrections.json`) return ok(JSON.stringify(doc));
    if (path === `${bareDir}/checklist.json`) return ok(JSON.stringify({ ...r1, id: "bare", child: "", parent: "" }));
    if (path.endsWith("checklist.json")) return ok(JSON.stringify(r2));
    return Promise.reject(new Error(`404 ${path}`));
  },
  mediaUrl: (path: string, v?: number) => `/api/media?path=${encodeURIComponent(path)}&v=${v ?? 0}`,
  fetchReviewRuns: () => Promise.resolve({ runs: [] }),
}));

it("reads the corrections doc: grouping by scene → shot, counts, filters, diff lines and loop step", () => {
  expect(doc.child).toBe(r1.child);
  expect(doc.summary).toMatchObject({ frames_changed: 1, specs_changed: 1 });
  const c = countBy(doc.corrections);
  expect(c.level.critical).toBe(doc.corrections.length);
  expect(c.verify).toMatchObject({ 复核仍有问题: 1, 待复核: 0 });
  const g = groupCorrections(doc, {});
  expect(g.map(x => x.scene)).toEqual(["s1"]);                         // s2 什么都没改：不列
  expect(g[0].shots.map(s => s.shot.key)).toEqual(["s1_st1"]);
  expect(g[0].shots[0].corrections[0].law).toBe("physics");             // 同级按编号：I1 物理在前
  expect(groupCorrections(doc, { verify: "复核仍有问题" })[0].shots[0].corrections.map(x => x.law)).toEqual(["physics"]);
  expect(groupCorrections(doc, { level: "minor" })).toEqual([]);
  expect(groupCorrections(doc, { scene: "s2" })).toEqual([]);
  expect(shotTouched(doc.shots.find(s => s.key === "s2_st1")!)).toBe(false);
  expect(["@@ -1 +1 @@", "+新", "-旧", " 同"].map(diffKind)).toEqual(["hunk", "add", "del", "ctx"]);
  expect(correctionsStep(doc)).toBe(2);
  expect(correctionsStep({ ...doc, child: "" })).toBe(1);
  expect(correctionsStep(null)).toBe(0);
  expect(reviewCorrectionsHref(dir, { level: "critical" })).toBe(`${REVIEW_CORRECTIONS_ROUTE}?${new URLSearchParams({ path: dir, level: "critical" })}`);
});

it("renders the corrections page: loop links both ways, before/after first frames, solutions, files, verification, spec diff", async () => {
  const { ReviewCorrectionsPage } = await import("../src/components/ReviewCorrectionsPage");
  const { container } = render(<MemoryRouter initialEntries={[reviewCorrectionsHref(dir)]}><ReviewCorrectionsPage /></MemoryRouter>);
  await waitFor(() => expect(container.querySelector('[data-shot="s1_st1"]')).toBeTruthy());
  const href = (name: RegExp) => screen.getByRole("link", { name }).getAttribute("href");
  expect(href(/← 本轮审查单/)).toBe(reviewRunHref(dir));
  expect(href(/← 问题清单/)).toBe(reviewIssuesHref(dir));
  expect(href(/→ 下一轮审查单/)).toBe(reviewRunHref(r1.child!));
  expect(container.querySelector(".rv-loop")!.textContent).toContain("本轮审查修复下一轮复核");
  expect(container.querySelector(".rv-loop-now")!.textContent).toBe("下一轮复核");
  const card = container.querySelector('[data-shot="s1_st1"]') as HTMLElement;
  expect(card.textContent).toContain("首帧换了");
  expect(card.textContent).toContain("分镜改了 1 处");
  const imgs = [...card.querySelectorAll(".rc-frames img")] as HTMLImageElement[];
  expect(imgs).toHaveLength(2);
  expect(decodeURIComponent(imgs[0].src)).toContain("planning/_r1/st1_first_frame.png");
  expect(decodeURIComponent(imgs[1].src)).toContain("planning/st1_first_frame.png");
  expect(within(card).getByText("修复前")).toBeTruthy();
  expect(within(card).getByText("修复后")).toBeTruthy();
  const issues = card.querySelectorAll(".rc-issue");
  expect(issues).toHaveLength(doc.corrections.length);
  const phys = card.querySelector('.rc-issue[data-issue="I1"]') as HTMLElement;
  expect(phys.textContent).toContain("改分镜、重画首帧");
  expect(phys.querySelector(".rv-level-critical")).toBeTruthy();
  expect(phys.querySelector(".rc-files a")!.getAttribute("href")).toContain("filming.json");
  const chip = phys.querySelector(".rc-v")!;
  expect(chip.textContent).toBe("复核仍有问题");
  fireEvent.click(chip);
  expect(phys.querySelector(".rc-verify")!.textContent).toContain("可剪");
  expect(card.querySelector('.rc-issue[data-issue="I6"] .rc-v')!.textContent).toBe("已复核通过");
  // 分镜 diff：可折叠，删的红、加的绿
  const diff = card.querySelector(".rc-diff") as HTMLDetailsElement;
  expect(diff.open).toBe(false);
  expect(diff.querySelector(".rc-d-del")!.textContent).toContain("她站着。");
  expect(diff.querySelector(".rc-d-add")!.textContent).toContain("她转身。");
  // 筛选：只看复核仍有问题的
  fireEvent.change(screen.getByLabelText("复核"), { target: { value: "复核仍有问题" } });
  await waitFor(() => expect(container.querySelectorAll(".rc-issue")).toHaveLength(1));
  expect(screen.getByText("显示 1 镜")).toBeTruthy();
  fireEvent.change(screen.getByLabelText("级别"), { target: { value: "minor" } });
  await waitFor(() => expect(screen.getByText("没有符合筛选的修复。")).toBeTruthy());
});

it("shows how to generate the page when corrections.json is missing", async () => {
  const { ReviewCorrectionsPage } = await import("../src/components/ReviewCorrectionsPage");
  render(<MemoryRouter initialEntries={[reviewCorrectionsHref(bareDir)]}><ReviewCorrectionsPage /></MemoryRouter>);
  await waitFor(() => expect(screen.getAllByText(/还没生成修复记录/).length).toBeGreaterThan(0));
  expect(screen.getByText(correctionsCommand(bareDir))).toBeTruthy();
  expect(screen.getByRole("link", { name: /← 本轮审查单/ }).getAttribute("href")).toBe(reviewRunHref(bareDir));
  expect(screen.getByText("下一轮还没开")).toBeTruthy();
});

it("links the checklist page and the issues page to the corrections page", async () => {
  const { ReviewRunPage } = await import("../src/components/ReviewRunPage");
  const { unmount } = render(<MemoryRouter initialEntries={[reviewRunHref(dir)]}><ReviewRunPage /></MemoryRouter>);
  await waitFor(() => expect(screen.getByRole("link", { name: /修复页/ })).toBeTruthy());
  expect(screen.getByRole("link", { name: /修复页/ }).getAttribute("href")).toBe(reviewCorrectionsHref(dir));
  unmount();
  const { ReviewIssuesPage } = await import("../src/components/ReviewIssuesPage");
  render(<MemoryRouter initialEntries={[reviewIssuesHref(dir)]}><ReviewIssuesPage /></MemoryRouter>);
  await waitFor(() => expect(screen.getByRole("link", { name: /修复页/ })).toBeTruthy());
  expect(screen.getByRole("link", { name: /修复页/ }).getAttribute("href")).toBe(reviewCorrectionsHref(dir));
});
