import { test, expect } from "@playwright/test";

test.use({ channel: process.env.PLAYWRIGHT_CHANNEL });

test("请求日志页按范围审查完整请求，不提交生成", async ({ page }) => {
  const episode = "ai_videos/test-fixture/episodes/ep01/request_log.md";
  const characters = "ai_videos/test-fixture/characters/request_log.md";
  const calls: string[] = [];
  const errors: string[] = [];
  page.on("pageerror", error => errors.push(error.message));
  await page.route("**/api/tree", route => route.fulfill({ json: { type: "directory", name: "fixture", path: "", children: [] } }));
  await page.route("**/api/request-log*", async route => {
    const request = route.request();
    expect(request.method()).toBe("GET");
    calls.push(request.url());
    const url = new URL(request.url());
    const listing = url.pathname === "/api/request-logs";
    const body = listing
      ? { logs: [episode, characters].map(path => ({ path, bytes: 512, modified_at: 1 })), entries: [], total: 2 }
      : { logs: [], entries: [{ request_id: "mock-only", time: "2026-10-03T01:00:00Z", provider: "dreamina",
          operation: "text2image", event: "request", target: url.searchParams.get("path"),
          request: { prompt: "模拟请求：完整画面描述\n第二行", model_version: "5.0", ratio: "9:16" } }], total: 75 };
    await route.fulfill({ json: body });
  });
  await page.goto("/");
  await expect(page.getByRole("button", { name: /请求日志/ })).toBeVisible();
  const baselineErrors = new Set(errors);
  if (baselineErrors.size) test.info().annotations.push({ type: "existing-home-page-errors", description: [...baselineErrors].join("\n") });
  errors.length = 0;
  await page.goto("/request-logs");
  await expect(page.getByRole("heading", { name: "外部服务请求日志" })).toBeVisible();
  await page.locator(".request-log-entry summary").click();
  await expect(page.locator(".request-log-entry pre")).toContainText("模拟请求：完整画面描述");
  await page.getByRole("combobox").selectOption(characters);
  await expect(page.locator(".request-log-entry")).toContainText(characters);
  await page.getByRole("button", { name: "下一页" }).click();
  await expect.poll(() => calls.some(url => url.includes("offset=50"))).toBe(true);
  await page.getByRole("button", { name: "刷新", exact: true }).click();
  await expect(page.getByRole("link", { name: "查看原始 Markdown" })).toHaveAttribute("href", `/file/${encodeURIComponent(characters)}`);
  expect(errors.filter(error => !baselineErrors.has(error))).toEqual([]);
});
