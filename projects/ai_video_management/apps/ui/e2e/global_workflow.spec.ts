import { test, expect as browserExpect } from "@playwright/test";
import { globalSourceUrl } from "../src/lib/globalWorkflow";
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

