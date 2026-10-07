import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, expect, it, vi } from "vitest";
import { RequestLogsPage } from "../src/components/RequestLogsPage";

afterEach(() => { cleanup(); vi.unstubAllGlobals(); });

it("按归属查看完整请求并分页，不发起生成", async () => {
  const calls: string[] = [];
  const fetch = vi.fn(async (url: string) => {
    calls.push(url);
    const body = url === "/api/request-logs"
      ? { logs: [{ path: "ai_videos/demo/episodes/ep01/request_log.md", bytes: 9, modified_at: 1 }], entries: [], total: 1 }
      : { logs: [], entries: [{ request_id: "r1", event: "request", provider: "dreamina", operation: "text2image", request: { prompt: "完整对白\n真实请求" } }], total: 75 };
    return { ok: true, json: async () => body };
  });
  vi.stubGlobal("fetch", fetch);
  render(<MemoryRouter><RequestLogsPage /></MemoryRouter>);
  await screen.findByText(/请求 ID：r1/);
  expect(screen.getByText(/完整对白/)).toBeInTheDocument();
  fireEvent.click(screen.getByRole("button", { name: "下一页" }));
  await waitFor(() => expect(calls.some(url => url.includes("offset=50"))).toBe(true));
  expect(calls.every(url => url.startsWith("/api/request-log"))).toBe(true);
});

it("读取失败时显示明确错误", async () => {
  vi.stubGlobal("fetch", vi.fn(async () => ({ ok: false, status: 500 })));
  render(<MemoryRouter><RequestLogsPage /></MemoryRouter>);
  expect(await screen.findByRole("alert")).toHaveTextContent("读取失败");
});
