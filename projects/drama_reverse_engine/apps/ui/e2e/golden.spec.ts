import { expect, Page, test } from "@playwright/test";

const consoleErrors: string[] = [];

function watchConsole(page: Page) {
  consoleErrors.length = 0;
  page.on("console", (msg) => {
    if (msg.type() === "error") consoleErrors.push(msg.text());
  });
}

async function openSeedDrama(page: Page) {
  await page.locator(".entry-list").getByRole("button", { name: "种子剧" }).click();
  await expect(page.locator('[data-view="drama"]')).toBeVisible();
}

test("left nav lists seeded entry and opens its episode list", async ({ page }) => {
  watchConsole(page);
  await page.goto("/");
  await expect(page.locator(".sidebar h1")).toHaveText("短剧逆向引擎");
  await expect(page.locator('[data-view="upload-new"]')).toBeVisible();
  await openSeedDrama(page);
  await expect(page.locator(".episode-list li")).toHaveCount(1);
  expect(consoleErrors).toEqual([]);
});

test("left nav expands selected entry with episode progress and artifact links", async ({ page }) => {
  watchConsole(page);
  await page.goto("/");
  await openSeedDrama(page);
  const nav = page.locator(".nav-eps");
  await expect(nav.getByRole("button", { name: /ep01/ })).toBeVisible();
  await expect(nav.getByText(/done 8\/8/)).toBeVisible();
  await nav.getByRole("button", { name: "小说" }).click();
  await expect(page.locator('[data-view="artifact"]')).toBeVisible();
  await expect(page.locator("pre.artifact")).toContainText("他回来了");
  expect(consoleErrors).toEqual([]);
});

test("upload-first: new entry upload posts multipart and reports creation", async ({ page }) => {
  watchConsole(page);
  await page.route("**/api/uploads", async (route) => {
    expect(route.request().headers()["content-type"]).toContain("multipart/form-data");
    await route.fulfill({ json: { drama_id: "e2e_new", title: "新片", episodes: ["e2e_new/ep01"] } });
  });
  await page.goto("/");
  await page.getByTestId("upload-new-input").setInputFiles({
    name: "新片.mp4", mimeType: "video/mp4",
    buffer: Buffer.from("0000001c667479706d70343200000000", "hex"),
  });
  await page.getByTestId("upload-new-declaration").check();
  await page.getByRole("button", { name: "上传并新建主体" }).click();
  await expect(page.getByText(/已建立「新片」，切出 1 集/)).toBeVisible();
  expect(consoleErrors).toEqual([]);
});

test("advanced create with gates still works and lands in left nav", async ({ page }) => {
  watchConsole(page);
  await page.goto("/");
  await page.getByRole("button", { name: "高级新建（闸口）" }).click();
  await expect(page.locator('[data-view="create"]')).toBeVisible();
  const suffix = test.info().project.name === "prod-static" ? "p" : "d";
  await page.locator('.form-card input[type="text"]').first().fill(`e2e_drama_${suffix}`);
  await page.locator('.form-card input[type="text"]').nth(1).fill("端到端剧");
  await page.getByTestId("declaration").check();
  await page.getByRole("button", { name: "创建" }).click();
  await expect(page.locator('[data-view="drama"]')).toBeVisible();
  await expect(page.locator(".entry-list").getByRole("button", { name: "端到端剧" }).first()).toBeVisible();
  expect(consoleErrors).toEqual([]);
});

test("episode view renders stage chips and action toolbar", async ({ page }) => {
  watchConsole(page);
  await page.goto("/");
  await openSeedDrama(page);
  await page.getByRole("button", { name: "seed1/ep01" }).click();
  await expect(page.locator('[data-view="episode"]')).toBeVisible();
  await expect(page.getByRole("button", { name: "自动跑完" })).toBeVisible();
  await expect(page.locator(".main .badge.stage")).toHaveCount(8);
  expect(consoleErrors).toEqual([]);
});

test("artifact render mode: script markdown opens and shows verbatim dialogue", async ({ page }) => {
  watchConsole(page);
  await page.goto("/");
  await openSeedDrama(page);
  await page.getByRole("button", { name: "seed1/ep01" }).click();
  await page.locator(".main").getByRole("button", { name: "剧本" }).click();
  await expect(page.locator('[data-view="artifact"]')).toBeVisible();
  await expect(page.locator("pre.artifact")).toContainText("你还敢回来？");
  expect(consoleErrors).toEqual([]);
});

test("artifact render mode: shot prompt file opens from shot list", async ({ page }) => {
  watchConsole(page);
  await page.goto("/");
  await openSeedDrama(page);
  await page.getByRole("button", { name: "seed1/ep01" }).click();
  await page.getByRole("button", { name: "shot01.md" }).click();
  await expect(page.locator("pre.artifact")).toContainText("视频 prompt");
  expect(consoleErrors).toEqual([]);
});

test("artifact edit mode saves a version", async ({ page }) => {
  watchConsole(page);
  await page.goto("/");
  await openSeedDrama(page);
  await page.getByRole("button", { name: "seed1/ep01" }).click();
  await page.locator(".main").getByRole("button", { name: "台词" }).click();
  await page.getByRole("button", { name: "编辑" }).click();
  await page.locator("textarea.editor").fill("# 台词表 — 人工批注版\n");
  await page.getByRole("button", { name: "保存（自动存版本）" }).click();
  await expect(page.getByText(/已保存/)).toBeVisible();
  expect(consoleErrors).toEqual([]);
});
