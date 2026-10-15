// @vitest-environment node
/**
 * The Vite dev proxy rewrites only the dev page's own Origin (follow-up 239).
 *
 * The backend refuses any write whose Origin is not its own. The proxy used to
 * stamp the backend's Origin on EVERY request, so a foreign page could POST to
 * 127.0.0.1:5174/api/… (no preflight needed) and reach the backend looking
 * same-origin — the dev server was an open relay around the gate.
 */
import { describe, expect, it, vi } from "vitest";
import type { ProxyOptions } from "vite";
import { forwardedOrigin } from "../devProxyOrigin";
import config from "../vite.config";

const BACKEND = "http://127.0.0.1:8766";

describe("forwardedOrigin", () => {
  it("rewrites the dev page's own Origin to the backend's", () => {
    expect(forwardedOrigin("http://127.0.0.1:5174", 5174, BACKEND)).toBe(BACKEND);
    expect(forwardedOrigin("http://localhost:5174", 5174, BACKEND)).toBe(BACKEND);
  });

  it("follows the port the dev server actually listens on", () => {
    expect(forwardedOrigin("http://127.0.0.1:5199", 5199, BACKEND)).toBe(BACKEND);
    expect(forwardedOrigin("http://127.0.0.1:5174", 5199, BACKEND)).toBe("http://127.0.0.1:5174");
  });

  it("forwards any other Origin unchanged, so the backend refuses it", () => {
    for (const foreign of ["https://evil.example", "null", "http://127.0.0.1:3000", "http://127.0.0.1:5174.evil.example"]) {
      expect(forwardedOrigin(foreign, 5174, BACKEND)).toBe(foreign);
    }
  });

  it("leaves a missing Origin missing", () => {
    expect(forwardedOrigin(undefined, 5174, BACKEND)).toBeUndefined();
  });
});

describe("vite.config.ts /api proxy hook", () => {
  const options = config.server?.proxy?.["/api"] as ProxyOptions;
  const target = options.target as string;

  function forward(origin: string | undefined): ReturnType<typeof vi.fn> {
    const handlers: Record<string, (...args: unknown[]) => void> = {};
    const proxy = { on: (event: string, handler: (...args: unknown[]) => void) => { handlers[event] = handler; } };
    options.configure?.(proxy as never, options);
    const setHeader = vi.fn();
    handlers.proxyReq({ setHeader }, { headers: origin === undefined ? {} : { origin }, socket: { localPort: 5174 } });
    return setHeader;
  }

  it("targets the backend and rewrites Host to it", () => {
    expect(target).toMatch(/^http:\/\/127\.0\.0\.1:\d+$/);
    expect(options.changeOrigin).toBe(true);
  });

  it("gives the dev page's own requests the backend's Origin", () => {
    expect(forward("http://127.0.0.1:5174")).toHaveBeenCalledWith("origin", target);
  });

  it("keeps a foreign page's Origin", () => {
    const setHeader = forward("https://evil.example");
    expect(setHeader).not.toHaveBeenCalledWith("origin", target);
    expect(setHeader.mock.calls.every(([, value]) => value === "https://evil.example")).toBe(true);
  });

  it("adds no Origin when the request had none", () => {
    expect(forward(undefined)).not.toHaveBeenCalled();
  });
});
