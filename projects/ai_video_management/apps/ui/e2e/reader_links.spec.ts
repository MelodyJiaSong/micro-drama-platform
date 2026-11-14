import { test, expect } from "@playwright/test";

const folder = "ai_videos/link_test/background/bg37";
const card = `${folder}/bg37.md`;
const image = `${folder}/views/正面.png`;

test("image links work before navigation loads, and missing links are checked afterwards", async ({ page }) => {
  let release!: () => void;
  const pending = new Promise<void>(done => { release = done; });
  await page.route("**/api/tree?lazy=1", async route => {
    await pending;
    await route.fulfill({ json: { type: "section", name: "root", path: "", children: [
      { type: "file", name: "bg37.md", path: card }, { type: "image", name: "正面.png", path: image },
    ] } });
  });
  await page.route("**/api/file?*", route => route.fulfill({ json: {
    path: card, content: "[正面图](views/正面.png)\n\n[缺失图](missing.png)", encoding: "utf-8", bytes: 1, mtime: 1, mtime_http: "",
  } }));
  await page.route("**/api/media?*", route => route.fulfill({ contentType: "image/png",
    body: Buffer.from("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII=", "base64"),
  }));
  try {
    await page.goto(`/file/${encodeURIComponent(card)}`);
    await expect(page.locator(".sidebar-loading")).toBeVisible();
    await page.getByRole("link", { name: "正面图", exact: true }).click({ timeout: 5000 });
    const preview = page.getByAltText("正面.png", { exact: true });
    await expect(preview).toBeVisible();
    await expect.poll(() => preview.evaluate((img: HTMLImageElement) => img.naturalWidth)).toBeGreaterThan(0);
    expect(new URL(await preview.getAttribute("src") ?? "", page.url()).searchParams.get("path")).toBe(image);
  } finally { release(); }
  await page.goto(`/file/${encodeURIComponent(card)}`);
  await expect(page.locator(".sidebar-loading")).toHaveCount(0);
  await expect(page.getByRole("link", { name: "正面图", exact: true })).toBeVisible();
  await expect(page.locator(".broken-link", { hasText: "缺失图" })).toBeVisible();
});
