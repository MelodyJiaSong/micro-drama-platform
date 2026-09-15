/// <reference types="vitest" />
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { resolve } from "path";

export default defineConfig({
  plugins: [react()],
  build: { outDir: resolve(__dirname, "..", "api", "static"), emptyOutDir: true, sourcemap: false },
  test: {
    environment: "jsdom",
    environmentOptions: { jsdom: { url: "http://127.0.0.1:8790" } },
    globals: true,
    setupFiles: ["./test/setup.ts"],
    include: ["test/**/*.test.{ts,tsx}"],
    pool: "forks",
  },
});
