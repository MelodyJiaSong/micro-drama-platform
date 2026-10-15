import { test, expect } from "@playwright/test";

/** Golden-path e2e — single-section AI Videos focus: the home page, the
 * Origin/Host gate and the sandbox. (The old shot / shotlist / Seedream /
 * locked-block / project-type views and their wukong_juexing fixtures went
 * with follow-up 233.)
 */

test.beforeEach(async ({ page }) => {
  page.on("pageerror", (err) => {
    throw new Error(`React reconciliation threw: ${err.message}`);
  });
  page.on("console", (msg) => {
    if (msg.type() === "error") throw new Error(`console.error: ${msg.text()}`);
  });
});

test("home page renders with single AI Videos sidebar section", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("navigation", { name: "File tree" })).toBeVisible();
  await expect(page.getByText("AI Videos")).toBeVisible();
});

test("Origin/Host gate: PUT from foreign Origin returns 403", async ({ request }) => {
  const r = await request.put("/api/file", {
    headers: {
      Origin: "http://evil.example.com",
      "If-Unmodified-Since": new Date().toUTCString(),
    },
    data: { path: "ai_videos/shengji_zhilu/README.md", content: "test" },
  });
  expect(r.status()).toBe(403);
});

test("Out-of-sandbox paths return 404", async ({ request }) => {
  // Anything not under ai_videos/ is invisible to the sandbox.
  const probes = ["node_modules/anything.md", "../escape.md", "random_top_level/file.md"];
  for (const probe of probes) {
    const r = await request.get(`/api/file?path=${encodeURIComponent(probe)}`);
    expect(r.status()).toBe(404);
  }
});
