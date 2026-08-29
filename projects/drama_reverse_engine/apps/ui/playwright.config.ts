import { defineConfig } from "@playwright/test";
import path from "path";
import { fileURLToPath } from "url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const PY = "C:/workspace/spec_coding/.venv/Scripts/python.exe";
const PROJECT_ROOT = path.resolve(HERE, "../..");
const WS = path.resolve(HERE, ".e2e_ws");

export default defineConfig({
  testDir: "./e2e",
  globalSetup: "./e2e/global-setup.ts",
  timeout: 30000,
  use: { headless: true },
  projects: [
    { name: "prod-static", use: { baseURL: "http://127.0.0.1:8622" } },
    { name: "dev-vite", use: { baseURL: "http://127.0.0.1:5620" } },
  ],
  webServer: [
    {
      command: `"${PY}" -m apps.api.main --serve-static --port 8622`,
      cwd: PROJECT_ROOT,
      env: { DRE_WORKSPACE: WS },
      url: "http://127.0.0.1:8622/api/health",
      reuseExistingServer: false,
    },
    {
      command: `"${PY}" -m apps.api.main --port 8620`,
      cwd: PROJECT_ROOT,
      env: { DRE_WORKSPACE: WS },
      url: "http://127.0.0.1:8620/api/health",
      reuseExistingServer: false,
    },
    {
      command: "npm run dev",
      cwd: HERE,
      url: "http://127.0.0.1:5620",
      reuseExistingServer: false,
      timeout: 120000,
    },
  ],
});
