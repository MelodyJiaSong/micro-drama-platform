import { test, expect as browserExpect } from "@playwright/test";
import { globalSourceUrl, storySectionUrl, storyTopicUrl } from "../src/lib/globalWorkflow";
import { storyRunUrl } from "../src/lib/storyRunRoutes";
import type { StorySection } from "../src/lib/storyWorkflow";
import { readFileSync } from "node:fs";
const STORY_SECTIONS: StorySection[] = JSON.parse(readFileSync(new URL("../../../../../.agents/references/project/workflow_catalog.json", import.meta.url), "utf8")).story_navigation;
const expect = browserExpect.configure({ timeout: 15_000 });
test.setTimeout(60_000);

test("global sources use nested navigation and precise source selection", async ({ page }, testInfo) => {
  await page.route("**/api/tree", route => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ type: "section", name: "文件", path: "", children: [] }) }));
  const errors: string[] = [];
  const writes: string[] = [];
  page.on("pageerror", error => errors.push(error.message));
  page.on("request", request => { if (!["GET", "HEAD"].includes(request.method())) writes.push(request.url()); });
  await page.goto(globalSourceUrl("repo:AGENTS.md"));
  await expect(page.getByRole("heading", { name: /Claude \/ Codex 共用入口/, level: 1 })).toBeVisible();
  const item = page.locator(`[data-path="/workflow/source/${encodeURIComponent("repo:AGENTS.md")}"]`);
  await expect(item).toHaveAttribute("aria-level", "4");
  await expect(item).toHaveAttribute("aria-selected", "true");
  await expect(page.locator('[data-path="/workflow/settings/agents"]')).toHaveAttribute("aria-expanded", "true");
  await page.locator('.tree-item[data-path="/workflow/category/ai-video"]').click();
  await expect(page.locator('.tree-item[data-path="/workflow/story"]')).toBeVisible();
  await item.click();
  await page.reload();
  await expect(item).toHaveAttribute("aria-selected", "true");
  const userConfig = page.locator(`[data-path="/workflow/source/${encodeURIComponent("user:.codex/config.toml")}"]`);
  await userConfig.click();
  await expect(page.getByRole("heading", { name: /Codex 用户配置/, level: 1 })).toBeVisible();
  await expect(userConfig).toHaveAttribute("aria-selected", "true");
  await expect(item).toHaveAttribute("aria-selected", "false");
  await expect(page.locator(".global-source-content")).toContainText('"model"');
  await expect(page.getByText("配置中的密钥、环境变量值、请求头及启动参数已隐藏", { exact: false })).toBeVisible();
  await page.screenshot({ path: `../../../../.audit/adhoc_agents/2026-10-05/global-workflow-settings/${testInfo.project.name}-config.png` });
  expect(errors).toEqual([]); expect(writes).toEqual([]);
});

test("both WOW run inputs link to current global rules while frozen versions remain visible", async ({ page }) => {
  await page.route("**/api/tree", route => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ type: "section", name: "文件", path: "", children: [] }) }));
  const episode = "ai_videos/shengji_zhilu/episodes/ep01";
  for (const run of ["story-run-20261003-214907-dd638b81", "story-run-20261003-144640-85f316d4"]) {
    await page.goto(storyRunUrl("item", episode, run, undefined, "rules-0"));
    await expect(page.getByRole("heading", { name: "本次实际使用的记录", exact: true })).toBeVisible();
    await expect(page.getByText("源文件已变化；本页保留当时版本", { exact: true })).toBeVisible();
    await page.getByRole("link", { name: "在工作流中查看当前全局源 ↗" }).click();
    await expect(page.getByRole("heading", { name: /三模块共用编排/, level: 1 })).toBeVisible();
    await expect(page.getByText("当前全局版本 · 只读。", { exact: false })).toBeVisible();
  }
  await page.goto("/workflow/settings/coverage");
  await expect(page.getByRole("heading", { name: "工作流覆盖核对", level: 1 })).toBeVisible();
  await expect(page.getByRole("heading", { name: "当前全局目录覆盖", level: 2 })).toBeVisible();
  await expect(page.getByText(/共用文档中的现存文件引用：0 个未登记；0 个源待编号，0 个源无法读取或导航/)).toBeVisible();
  await expect(page.locator(".global-coverage-scroll tbody tr")).toHaveCount(6);
  await expect(page.getByText("当前显示 6 个历史关联，0 个尚未登记；0 个集索引无法核验。", { exact: true })).toBeVisible();
});

test("global catalog failure is explicit and leaves the three modules accessible", async ({ page }) => {
  await page.route("**/api/global-workflow", route => route.fulfill({ status: 503, contentType: "application/json", body: "{}" }));
  await page.route("**/api/tree", route => route.fulfill({ status: 503, contentType: "application/json", body: "{}" }));
  await page.goto("/workflow");
  await expect(page.locator(".global-workflow [role=alert]")).toContainText("全局目录尚未核验");
  await page.locator('.tree-item[data-path="/workflow/category/ai-video"]').click();
  for (const module of ["story", "prompts"]) {
    await page.locator(`.tree-item[data-path="/workflow/${module}"]`).click();
    await expect(page).toHaveURL(new RegExp(`/workflow/${module}$`));
  }
});

test("story topics separate content from mechanics and survive direct links and refresh", async ({ page }, testInfo) => {
  await page.route("**/api/tree", route => route.fulfill({ status: 503, contentType: "application/json", body: "{}" }));
  const errors: string[] = [];
  const writes: string[] = [];
  page.on("pageerror", error => errors.push(error.message));
  page.on("request", request => { if (!["GET", "HEAD"].includes(request.method())) writes.push(request.url()); });
  await page.goto("/workflow/story");
  for (const section of STORY_SECTIONS) {
    await expect(page.locator(`.tree-item[data-path="${storySectionUrl(section.id)}"]`)).toBeVisible();
    await page.locator(`.tree-item[data-path="${storySectionUrl(section.id)}"]`).click();
    await expect(page.getByRole("heading", { name: section.title, level: 1, exact: true })).toBeVisible();
    for (const topic of section.topics) {
      await page.locator(`.tree-item[data-path="${storyTopicUrl(section, topic)}"]`).click();
      await expect(page.getByRole("heading", { name: topic.title, level: 1, exact: true })).toBeVisible();
      await expect(page.locator(".markdown-view")).not.toBeEmpty();
      await expect(page.locator('.tree-item[aria-selected="true"]')).toHaveCount(1);
      if (section.id === "content") await expect(page.locator(".markdown-view")).not.toContainText("python tools/story_run.py");
      await page.getByRole("link", { name: section.title, exact: true }).click();
    }
  }
  const section = STORY_SECTIONS[1];
  const topic = section.topics[4];
  await page.goto(storyTopicUrl(section, topic));
  await page.reload();
  await expect(page.getByRole("heading", { name: "验证与比较", level: 1, exact: true })).toBeVisible();
  await expect(page.locator(`.tree-item[data-path="${storySectionUrl(section.id)}"]`)).toHaveAttribute("aria-expanded", "true");
  await expect(page.locator(".markdown-view")).toContainText("UNVERIFIED");
  await expect(page.locator(".markdown-view")).not.toContainText("python tools/story_run.py begin");
  await page.getByRole("link", { name: /查看完整原文/ }).click();
  await expect(page.getByRole("heading", { name: /1\.1\.2_独立创作/, level: 1 })).toBeVisible();
  await expect(page.locator(".markdown-view")).toContainText("python tools/story_run.py begin");
  await page.goto(storyTopicUrl(STORY_SECTIONS[0], STORY_SECTIONS[0].topics[0]));
  await expect(page.locator(".markdown-view")).toContainText("R03");
  await page.screenshot({ path: `../../../../.audit/adhoc_agents/2026-10-06/story-content-execution/${testInfo.project.name}-content.png` });
  await page.setViewportSize({ width: 390, height: 844 });
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
  await page.screenshot({ path: `../../../../.audit/adhoc_agents/2026-10-06/story-content-execution/${testInfo.project.name}-narrow.png` });
  expect(errors).toEqual([]); expect(writes).toEqual([]);
});
