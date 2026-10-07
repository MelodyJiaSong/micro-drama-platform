import { expect, test } from "@playwright/test";

test("workflow shows three modules and independent support", async ({ page }) => {
  await page.goto("/workflow");
  await expect(page.getByRole("heading", { name: "全局工作流", exact: true })).toBeVisible();
  await expect(page.locator(".workflow-overview section")).toHaveCount(3);
  await expect(page.getByText("独立支持：Research · 人物、场景与物件资产")).toBeVisible();
  await expect(page.getByText("六阶段", { exact: false })).toHaveCount(0);
  await expect(page.getByRole("button", { name: "打开工具", exact: true })).toHaveCount(0);
  await expect(page.getByText("公共音乐库", { exact: true })).toHaveCount(0);
  await expect(page.locator('[data-path="ai_videos/_bgm"]')).toHaveCount(0);
});

test("global workflow is an expandable navigation tree with nested knowledge", async ({ page }, testInfo) => {
  await page.goto("/");
  const root = page.locator('.tree-item[data-path="/workflow"]');
  await expect(root).toHaveAttribute("aria-level", "1");
  await expect(root).toHaveAttribute("aria-expanded", "false");
  await expect(page.getByRole("button", { name: "查看 AI 短剧端到端工作流" })).toHaveCount(0);
  await expect(page.getByRole("button", { name: "查看影视改编全局知识" })).toHaveCount(0);
  await root.click();
  await expect(root).toHaveAttribute("aria-expanded", "true");
  for (const module of ["story", "filming", "prompts"]) {
    await expect(page.locator(`.tree-item[data-path="/workflow/${module}"]`)).toHaveAttribute("aria-level", "2");
  }
  const filming = page.locator('.tree-item[data-path="/workflow/filming"]');
  await filming.getByRole("button", { name: "Expand", exact: true }).click();
  const knowledge = page.locator('.tree-item[data-path="/workflow/filming/shot-sizes"]');
  await expect(knowledge).toHaveAttribute("aria-level", "3");
  await knowledge.click();
  await expect(page).toHaveURL(/\/workflow\/filming\/shot-sizes$/);
  await expect(knowledge).toHaveAttribute("aria-selected", "true");
  await expect(page.locator(".filming-knowledge article")).toBeVisible();
  await testInfo.attach("workflow-navigation", { body: await page.screenshot(), contentType: "image/png" });
  await page.reload();
  await expect(knowledge).toBeVisible();
  await expect(knowledge).toHaveAttribute("aria-selected", "true");
  await filming.click();
  await expect(filming).toHaveAttribute("aria-expanded", "true");
  await filming.getByRole("button", { name: "Collapse", exact: true }).click();
  await expect(knowledge).toHaveCount(0);
  const story = page.locator('.tree-item[data-path="/workflow/story"]');
  await story.focus();
  await story.press("Enter");
  await expect(page).toHaveURL(/\/workflow\/story$/);
  await expect(story).toHaveAttribute("aria-selected", "true");
  await expect(page.getByRole("heading", { name: "故事创作", level: 1 })).toBeVisible();
  await page.locator('.tree-item[data-path="/workflow/prompts"]').click();
  await expect(page.getByRole("heading", { name: "Prompt 编译", level: 1 })).toBeVisible();
  await page.getByRole("button", { name: "折叠全部", exact: true }).click();
  await expect(root).toHaveAttribute("aria-expanded", "false");
  await expect(story).toHaveCount(0);
  await root.focus();
  await root.press("ArrowRight");
  await expect(story).toBeVisible();
});

test("EP1 exposes read-only modules and independent support", async ({ page }, testInfo) => {
  test.setTimeout(120_000);
  const errors: string[] = [];
  page.on("pageerror", error => errors.push(error.message));
  await page.goto("/drama?drama=ai_videos%2Fshengji_zhilu&module=story&episode=ep01");
  await expect(page.getByRole("heading", { name: "魔兽世界", exact: true })).toBeVisible({ timeout: 45_000 });
  await expect(page.getByLabel("故事正文")).toBeVisible();
  await expect(page.locator(".episode-workflow textarea, .episode-workflow input")).toHaveCount(0);
  await page.locator('.tree-item[data-path="ai_videos/shengji_zhilu"]').click();
  for (const label of ["0_research", "1_资产库", "2_故事", "3_影视改编", "4_prompt编译"]) {
    await expect(page.getByText(label, { exact: true })).toBeVisible();
  }
  await expect(page.getByText("EP1 创作", { exact: true })).toHaveCount(0);
  for (const [module, heading] of [["filming", "影视改编"], ["prompts", "Prompt 编译"]]) {
    const stage = page.locator(`.tree-item[data-path="ai_videos/shengji_zhilu/stages/${module}"]`);
    const url = page.url();
    await expect(stage).toHaveAttribute("aria-expanded", "false");
    await stage.click();
    await expect(stage).toHaveAttribute("aria-expanded", "true");
    expect(page.url()).toBe(url);
    await page.locator(`.tree-item[data-path="ai_videos/shengji_zhilu/episodes/ep01/${module}.json"]`).click();
    await expect(page.getByRole("heading", { name: heading, exact: true })).toBeVisible();
    await expect(page.getByRole("button", { name: /保存草稿|确定版本|编译 Prompt|添加镜头/ })).toHaveCount(0);
    await stage.click();
    await expect(stage).toHaveAttribute("aria-expanded", "false");
    await expect(page.locator(`.tree-item[data-path="ai_videos/shengji_zhilu/episodes/ep01/${module}.json"]`)).toHaveCount(0);
    await stage.click();
  }
  const dramaBranch = page.locator('.tree-item[data-path^="ai_videos/shengji_zhilu/"]');
  await expect(dramaBranch.filter({ hasText: "3_大纲" })).toHaveCount(0);
  await page.goto("/file/" + encodeURIComponent("ai_videos/shengji_zhilu/episodes/ep01/state_changes.md"));
  await expect(page.getByRole("heading", { name: "EP1 · 状态变化", exact: true })).toBeVisible({ timeout: 45_000 });
  await expect(page.getByText("1_资产库", { exact: true })).toBeVisible({ timeout: 45_000 });
  await expect(page.getByRole("button", { name: "立即评分", exact: true })).toHaveCount(0);
  await expect(page.getByRole("group", { name: "出片三步：定版 → 拼接 → 整集字幕", exact: true })).toHaveCount(0);
  await expect(page.getByText("承接：EP1无前集，初始状态随故事确定。", { exact: false })).toBeVisible();
  await expect(page.getByRole("button", { name: "Edit file", exact: true })).toHaveCount(0);
  await page.getByText("1_资产库", { exact: true }).click();
  await page.getByText("世界规则", { exact: true }).click();
  await expect(page.getByRole("heading", { name: "世界规则", exact: true })).toBeVisible();
  await expect(page.getByRole("button", { name: "Edit file", exact: true })).toHaveCount(0);
  for (const path of ["ai_videos/shengji_zhilu/stages/story", "ai_videos/shengji_zhilu/stages/story/ep01"]) {
    const folder = page.locator(`.tree-item[data-path="${path}"]`);
    if (await folder.getAttribute("aria-expanded") === "false") await folder.click();
  }
  await page.locator('.tree-item[data-path="ai_videos/shengji_zhilu/episodes/ep01/current"]').click();
  await expect(page.locator(".story-run-story")).toContainText("米洛");
  expect(errors).toEqual([]);
  await testInfo.attach("ep01-workspace", { body: await page.screenshot({ fullPage: true }), contentType: "image/png" });
});
