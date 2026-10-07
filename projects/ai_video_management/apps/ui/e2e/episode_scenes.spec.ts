import { expect, test } from "@playwright/test";
import type { TreeNode } from "../src/types";

test("scene navigation opens the exact shot and survives reload", async ({ page }, testInfo) => {
  const drama = "ai_videos/demo";
  const episode = `${drama}/episodes/ep01`;
  const scenes = ["s10", "s1"].map(id => ({ id, background: "bg2", location: "交接棚", time: "白天", purpose: "争取差事",
    shots: [{ id: "st1", duration: 6, action: "递出袋子", camera: "固定中景", dialogue: "给你。" }] }));
  const href = (module: string, scene = "", shot = "") => `/drama?drama=${encodeURIComponent(drama)}&episode=ep01&module=${module}${scene ? `&scene=${scene}` : ""}${shot ? `&shot=${shot}` : ""}`;
  const stages: TreeNode[] = ["filming", "prompts"].map(module => ({ type: "directory", name: module,
    display_name: module === "filming" ? "3_影视改编" : "4_prompt编译", path: `${drama}/stages/${module}`,
    children: [{ type: "directory", name: "ep01", display_name: "EP1", path: `${episode}/${module}.json`, navigation_href: href(module),
      children: scenes.map(scene => ({ type: "directory", name: scene.id, display_name: `${scene.id} · 交接棚`,
        path: `${episode}/${module}.json/scenes/${scene.id}`, navigation_href: href(module, scene.id),
        children: [{ type: "directory", name: "st1", display_name: `ep1_${scene.id}_st1`,
          path: `${episode}/${module}.json/scenes/${scene.id}/shots/st1`, navigation_href: href(module, scene.id, `ep1_${scene.id}_st1`), children: [] }] })) }] }));
  const tree: TreeNode = { type: "section", name: "root", path: "", children: [{ type: "directory", name: "ai_videos", path: "ai_videos",
    children: [{ type: "directory", name: "demo", display_name: "示例剧", path: drama, is_drama: true, workflow: "three-module-v1", children: stages }] }] };
  await page.route("**/api/tree", route => route.fulfill({ json: tree }));
  await page.route("**/api/episode-workflow?*", route => route.fulfill({ json: {
    episode_path: episode, shot_keys: { s10: { st1: "ep1_s10_st1" }, s1: { st1: "ep1_s1_st1" } },
    modules: [
      { id: "story", label: "故事创作", content: { brief: "方向", text: "正文" } },
      { id: "filming", label: "影视改编", content: { scenes } },
      { id: "prompts", label: "Prompt 编译", content: { scenes: scenes.map(scene => ({ id: scene.id, shots: [{ id: `ep1_${scene.id}_st1`, text: `ep1_${scene.id}_st1\n时长：6秒。` }] })) } },
    ].map(module => ({ ...module, status: "approved", can_edit: false })) } }));
  await page.goto(href("filming", "s10", "ep1_s10_st1"));
  await expect(page.getByRole("heading", { name: "ep1_s10_st1 · 6秒" })).toBeVisible();
  const shot = page.locator(`.tree-item[data-path="${episode}/filming.json/scenes/s10/shots/st1"]`);
  await expect(shot).toBeVisible();
  await expect(shot).toHaveAttribute("aria-selected", "true");
  await page.reload();
  await expect(shot).toBeVisible();
  await expect(shot).toHaveAttribute("aria-selected", "true");
  const scene = page.locator(`.tree-item[data-path="${episode}/filming.json/scenes/s1"]`);
  await scene.click();
  await expect(page.getByRole("heading", { name: "ep1_s1_st1 · 6秒" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "ep1_s10_st1 · 6秒" })).toHaveCount(0);
  await page.goto(href("prompts", "s1", "ep1_s1_st1"));
  await expect(page.locator(".workflow-prompts pre")).toHaveText("ep1_s1_st1\n时长：6秒。");
  await expect(page.locator(".episode-workflow input, .episode-workflow textarea")).toHaveCount(0);
  await testInfo.attach("scene-shot-navigation", { body: await page.screenshot({ fullPage: true }), contentType: "image/png" });
});
