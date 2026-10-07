import { expect, test } from "@playwright/test";

test("current EP is a single soft link to the selected run", async ({ page, request }) => {
  test.setTimeout(60_000);
  const episode = "ai_videos/shengji_zhilu/episodes/ep01";
  const index = await request.get(`/api/story-runs?episode_path=${encodeURIComponent(episode)}`);
  const list = await index.json();
  const selected = list.selection.run_id;
  const number = list.runs.findIndex((run: { run_id: string }) => run.run_id === selected) + 1;
  const other = list.runs.find((run: { run_id: string }) => run.run_id !== selected);
  await page.goto(`/story-runs/story?episode_path=${encodeURIComponent(episode)}&run_id=${other.run_id}`);
  const link = page.locator(`.tree-item[data-path="${episode}/current"]`);
  await expect(link).toBeVisible({ timeout: 45_000 });
  await expect(link).toContainText(`当前 EP1 → run${number}`);
  await expect(link).not.toHaveAttribute("aria-expanded");
  await expect(page.locator(`.tree-item[data-path^="${episode}/current/"]`)).toHaveCount(0);
  await link.click();
  await expect(page).toHaveURL(new RegExp(`run_id=${selected}`));
  await expect(page.locator("h1")).toHaveText("候选故事");
  await expect(page.locator(".story-run-meta")).toContainText(selected);
  await expect(page.locator(`.tree-item[data-path="${episode}/runs/${selected}/output.json"]`)).toHaveAttribute("aria-selected", "true");
  await expect(link).toHaveAttribute("aria-selected", "false");
  await page.screenshot({ path: "../../../../.audit/adhoc_agents/2026-10-04/current-ep-link/current-link.png", fullPage: true });
});

test("story navigation opens an independent story page and legacy links redirect", async ({ page, request }) => {
  test.setTimeout(90_000);
  const episode = "ai_videos/shengji_zhilu/episodes/ep01";
  const index = await request.get(`/api/story-runs?episode_path=${encodeURIComponent(episode)}`);
  expect(index.ok()).toBe(true);
  const list = await index.json();
  const selected = list.runs[0].run_id;
  const detail = await request.get(`/api/story-runs/detail?episode_path=${encodeURIComponent(episode)}&run_id=${selected}`);
  const run = await detail.json();
  const errors: string[] = [];
  page.on("pageerror", error => errors.push(error.message));
  await page.goto(`/story-runs?episode_path=${encodeURIComponent(episode)}&run_id=${selected}`);
  await expect(page).toHaveURL(/\/story-runs\/story\?/);
  await expect(page.locator("h1")).toHaveText("候选故事");
  await expect(page.locator(".story-run-story")).toHaveText(run.candidate.text);
  await expect(page.locator(".story-run-tabs, .story-runs-history")).toHaveCount(0);
  await expect(page.getByRole("heading", { name: /^实际参与者/ })).toHaveCount(0);
  await expect(page.getByRole("button", { name: /保存草稿|确定版本|编译 Prompt|Edit file/ })).toHaveCount(0);
  const leaf = page.locator(`.tree-item[data-path="${episode}/runs/${selected}/output.json"]`);
  await expect(leaf).toBeVisible({ timeout: 45_000 });
  await expect(leaf).toHaveAttribute("aria-selected", "true");
  await page.reload();
  await expect(page.locator("h1")).toHaveText("候选故事");
  await expect(leaf).toHaveAttribute("aria-selected", "true", { timeout: 45_000 });
  expect(errors).toEqual([]);
  await page.screenshot({ path: "../../../../.audit/adhoc_agents/2026-10-04/story-document-pages/story-page.png", fullPage: true });
});

test("EP1 navigation has run folders with their own documents and friendly shared input", async ({ page, request }) => {
  test.setTimeout(90_000);
  const episode = "ai_videos/shengji_zhilu/episodes/ep01";
  const index = await request.get(`/api/story-runs?episode_path=${encodeURIComponent(episode)}`);
  expect(index.ok()).toBe(true);
  const list = await index.json();
  expect(list.runs.length).toBeGreaterThanOrEqual(2);
  await page.goto(`/story-runs?episode_path=${encodeURIComponent(episode)}&run_id=${encodeURIComponent(list.runs[0].run_id)}`);
  const root = page.locator('.tree-item[data-path="ai_videos/shengji_zhilu"]');
  await expect(root).toBeVisible({ timeout: 45_000 });
  if (await root.getAttribute("aria-expanded") === "false") await root.getByRole("button", { name: "Expand", exact: true }).click();
  for (const path of ["ai_videos/shengji_zhilu/stages/story", "ai_videos/shengji_zhilu/stages/story/ep01", `${episode}/runs`]) {
    const directory = page.locator(`.tree-item[data-path="${path}"]`);
    const before = page.url();
    if (await directory.getAttribute("aria-expanded") === "false") await directory.click();
    expect(page.url()).toBe(before);
  }
  await expect(page.locator(`.tree-item[data-path="${episode}/runs"]`)).toContainText("runs · Transient");
  await expect(page.locator(`.tree-item[data-path="${episode}/current"]`)).toContainText("当前 EP1");
  for (const item of list.runs.slice(0, 2)) {
    const folder = page.locator(`.tree-item[data-path="${episode}/runs/${item.run_id}"]`);
    const before = page.url();
    await expect(folder).toBeVisible();
    if (await folder.getAttribute("aria-expanded") === "false") await folder.click();
    expect(page.url()).toBe(before);
    for (const subfolder of ["inputs", "outputs", "process_documents"]) {
      const category = page.locator(`.tree-item[data-path="${episode}/runs/${item.run_id}/${subfolder}"]`);
      const location = page.url();
      if (await category.getAttribute("aria-expanded") === "false") await category.click();
      expect(page.url()).toBe(location);
    }
    const leaf = page.locator(`.tree-item[data-path="${episode}/runs/${item.run_id}/output.json"]`);
    await leaf.click();
    await expect(leaf).toHaveAttribute("aria-selected", "true");
    const detail = await request.get(`/api/story-runs/detail?episode_path=${encodeURIComponent(episode)}&run_id=${encodeURIComponent(item.run_id)}`);
    const run = await detail.json();
    await expect(page.locator("h1")).toHaveText("候选故事");
    await expect(page).toHaveURL(/\/story-runs\/story\?/);
    await expect(page.locator(".story-run-story")).toHaveText(run.candidate.text);
    await expect(page.getByRole("heading", { name: /^实际参与者/ })).toHaveCount(0);
    await page.locator(`.tree-item[data-path="${episode}/runs/${item.run_id}/state.json"]`).click();
    await expect(page.locator("h1")).toHaveText("候选状态变化");
    await expect(page).toHaveURL(/\/story-runs\/state\?/);
    await expect(page.locator(".story-run-story")).toHaveCount(0);
    await expect(leaf).toHaveAttribute("aria-selected", "false");
    for (const [view, heading] of [["input", /^输入快照/], ["process", /^实际参与者/]] as const) {
      const document = page.locator(`.tree-item[data-path="${episode}/runs/${item.run_id}/${view}.json"]`);
      await document.click();
      await expect(document).toHaveAttribute("aria-selected", "true");
      await expect(page.getByRole("heading", { name: heading, level: 2 })).toBeVisible();
      await expect(page.locator("h1")).toHaveText(view === "input" ? "输入快照" : "创作过程");
      await expect(page).toHaveURL(new RegExp(`/story-runs/${view}\\?`));
      await expect(page.locator(".story-run-tabs, .story-runs-history, .story-run-story")).toHaveCount(0);
      await expect(page.locator(".story-run-meta")).toContainText(item.run_id);
    }
  }
  const processLeaf = page.locator(`.tree-item[data-path="${episode}/runs/${list.runs[1].run_id}/process.json"]`);
  await processLeaf.click();
  await page.getByLabel("筛选").selectOption("rejected");
  await page.locator("main").evaluate(element => { element.scrollTop = 300; });
  await page.locator(`.tree-item[data-path="${episode}/runs/${list.runs[1].run_id}/output.json"]`).click();
  await expect(page.locator("h1")).toHaveText("候选故事");
  expect(await page.locator("main").evaluate(element => element.scrollTop)).toBe(0);
  await page.goBack();
  await expect(page.locator("h1")).toHaveText("创作过程");
  await expect(page.getByLabel("筛选")).toHaveValue("all");
  await expect(processLeaf).toHaveAttribute("aria-selected", "true");
  await page.screenshot({ path: "../../../../.audit/adhoc_agents/2026-10-04/story-document-pages/process-page.png", fullPage: true });
  const shared = page.locator(`.tree-item[data-path="${episode}/shared"]`);
  await expect(shared).toContainText("共享配置 · Persistent");
  if (await shared.getAttribute("aria-expanded") === "false") await shared.click();
  await page.locator(`.tree-item[data-path="${episode}/shared/index.json"]`).click();
  await expect(page.getByRole("heading", { name: "共享创作输入", exact: true })).toBeVisible();
  await expect(page.getByLabel("查看版本")).toBeVisible();
  const ruleLeaf = page.locator(`.tree-item[data-path="${episode}/shared/rules-view.json"]`);
  await ruleLeaf.click();
  await expect(page.getByRole("heading", { name: "创作规则", exact: true })).toBeVisible();
  await expect(ruleLeaf).toHaveAttribute("aria-selected", "true");
  await expect(page.locator(`.tree-item[data-path="${episode}/shared/index.json"]`)).toHaveAttribute("aria-selected", "false");
});

test("each run exposes frozen inputs, rules and actual tasks through individual soft links", async ({ page, request }) => {
  test.setTimeout(150_000);
  const episode = "ai_videos/shengji_zhilu/episodes/ep01";
  const list = await (await request.get(`/api/story-runs?episode_path=${encodeURIComponent(episode)}`)).json();
  for (const summary of list.runs.slice(0, 2)) {
    const run = await (await request.get(`/api/story-runs/detail?${new URLSearchParams({ episode_path: episode, run_id: summary.run_id })}`)).json();
    expect(run.io.items.filter((item: { kind: string }) => item.kind === "input").length).toBeGreaterThan(10);
    const task = run.io.items.find((entry: { group: string }) => entry.group === "tasks");
    const inputUrl = `/story-runs/input?${new URLSearchParams({ episode_path: episode, run_id: summary.run_id })}`;
    await page.goto(inputUrl);
    for (const id of ["rules-0", task.id, "runtime", "file-review_packet-json", "file-spawns-writer-output-json", "candidate"]) {
      const item = run.io.items.find((entry: { id: string }) => entry.id === id);
      expect(item).toBeDefined();
      if (item.kind === "output") {
        const folder = page.locator(`.tree-item[data-path="${episode}/runs/${summary.run_id}/outputs"]`);
        if (await folder.getAttribute("aria-expanded") === "false") await folder.click();
        await page.locator(`.tree-item[data-path="${episode}/runs/${summary.run_id}/links/${id}.json"]`).click();
      } else await page.getByRole("link", { name: `${item.name} ↗`, exact: true }).click();
      await expect(page).toHaveURL(new RegExp(`item_id=${id}`));
      await expect(page.locator("h1")).toHaveText(item.name);
      const leaf = page.locator(`.tree-item[data-path="${episode}/runs/${summary.run_id}/links/${id}.json"]`);
      await expect(leaf).toHaveAttribute("aria-selected", "true", { timeout: 45_000 });
      await page.screenshot({ path: `../../../../.audit/adhoc_agents/2026-10-04/run-explicit-io/${summary.run_id}-${id}.png` });
      await expect(page.locator('.tree-item[aria-selected="true"]')).toHaveCount(1);
      if (id === "rules-0") await expect(page.getByText("源文件已变化；本页保留当时版本", { exact: true })).toBeVisible();
      if (id === "runtime") await expect(page.getByText("未记录", { exact: true }).first()).toBeVisible();
      if (id === "candidate") {
        const refreshed = await page.reload();
        expect(refreshed?.status(), page.url()).toBe(200);
        await expect(page.locator("h1")).toHaveText(item.name);
        await expect(leaf).toHaveAttribute("aria-selected", "true", { timeout: 45_000 });
      } else await page.getByRole("link", { name: "查看本run完整输入清单", exact: true }).click();
    }
  }
  await page.screenshot({ path: "../../../../.audit/adhoc_agents/2026-10-04/run-explicit-io/candidate.png", fullPage: true });
});

test("shared profiles and two independent candidates can be compared without write actions", async ({ page, request }) => {
  const episode = "ai_videos/shengji_zhilu/episodes/ep01";
  const index = await request.get(`/api/story-runs?episode_path=${encodeURIComponent(episode)}`);
  expect(index.ok()).toBe(true);
  const list = await index.json();
  expect(list.runs.length).toBeGreaterThanOrEqual(2);
  const [first, second] = list.runs;
  const errors: string[] = [];
  page.on("pageerror", error => errors.push(error.message));
  const writes: string[] = [];
  page.on("request", event => { if (event.method() !== "GET" && event.method() !== "HEAD") writes.push(event.url()); });
  await page.goto(`/story-runs/compare?episode_path=${encodeURIComponent(episode)}&run_id=${encodeURIComponent(first.run_id)}&compare_run_id=${encodeURIComponent(second.run_id)}`);
  await expect(page.locator("h1")).toHaveText("候选对比");
  await expect(page.locator(".story-run-tabs")).toHaveCount(0);
  await expect(page.getByText("输入指纹相同（覆盖规则）", { exact: true })).toBeVisible();
  await expect(page.getByText("冻结规则快照相同", { exact: true })).toBeVisible();
  await expect(page.getByLabel("A 候选")).toContainText(first.run_id);
  await expect(page.getByLabel("B 候选")).toContainText(second.run_id);
  await expect(page.getByRole("button", { name: /编辑|保存|执行选用/ })).toHaveCount(0);
  await page.screenshot({ path: "../../../../.audit/adhoc_agents/2026-10-04/story-document-pages/story-run-comparison.png", fullPage: true });
  await page.goto(`/story-runs/story?episode_path=${encodeURIComponent(episode)}&run_id=${first.run_id}`);
  await expect(page.getByRole("button", { name: "复制选用命令", exact: true })).toBeVisible();
  await page.getByRole("link", { name: "查看共享输入与规则版本", exact: true }).click();
  await expect(page.getByRole("heading", { name: "共享创作输入", exact: true })).toBeVisible();
  await expect(page.getByText("谁 · Who", { exact: true })).toBeVisible();
  await expect(page.getByRole("textbox")).toHaveCount(0);
  await page.getByLabel("查看版本").selectOption("workflow-v2");
  await expect(page.getByLabel("查看版本")).toHaveValue("workflow-v2");
  await expect(page.getByText("后续流程版本（本次未使用）", { exact: true }).last()).toBeVisible();
  await page.getByRole("link", { name: "查看创作规则", exact: true }).click();
  await expect(page.getByRole("heading", { name: "创作规则", exact: true })).toBeVisible();
  expect(await page.locator(".story-run-markdown").count()).toBeGreaterThan(0);
  await page.screenshot({ path: "../../../../.audit/adhoc_agents/2026-10-04/story-document-pages/story-input-ui.png", fullPage: true });
  expect(writes).toEqual([]);
  expect(errors).toEqual([]);
});
