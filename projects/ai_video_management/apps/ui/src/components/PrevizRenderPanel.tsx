import { useCallback, useEffect, useRef, useState } from "react";

import { ApiError } from "../types";
import type { PrevizStatus } from "../types";
import { cancelPreviz, fetchPrevizStatus, renderPreviz } from "../api";

interface PrevizRenderPanelProps {
  path: string;
}

const POLL_MS = 2000;
const ACTIVE_STATES = new Set(["building", "probing", "rendering", "muxing"]);

function label(state: string): string {
  switch (state) {
    case "building": return "按配置重建 .blend…";
    case "probing": return "读取帧范围…";
    case "rendering": return "渲染中…";
    case "muxing": return "合成 MP4…";
    case "done": return "已完成";
    case "failed": return "失败";
    case "cancelled": return "已取消";
    default: return "待渲染";
  }
}

function clock(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}:${String(s).padStart(2, "0")}`;
}

/** Render the previz `.blend` in this folder to an MP4, on demand.
 *
 * Authoring the `.blend` (via `build_previz.py`) and rendering it are separate
 * steps: the build is seconds and gets re-run constantly while a shot is being
 * tuned, the render is 15–30 minutes. This button is the "the .blend is right
 * now, go make the MP4" trigger, so a dozen build iterations cost nothing. */
export function PrevizRenderPanel({ path }: PrevizRenderPanelProps): JSX.Element {
  const [status, setStatus] = useState<PrevizStatus | null>(null);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const timer = useRef<number | null>(null);

  const poll = useCallback(async () => {
    try {
      const next = await fetchPrevizStatus(path);
      setStatus(next);
      return next;
    } catch (e) {
      setErr(e instanceof ApiError ? `${e.detail?.kind ?? e.status}` : String(e));
      return null;
    }
  }, [path]);

  useEffect(() => {
    let alive = true;
    void (async () => {
      const first = await poll();
      // Only arm the poll loop when something is actually running — an idle
      // previz folder should not hold a timer open for the whole session.
      if (alive && first && ACTIVE_STATES.has(first.state)) {
        timer.current = window.setInterval(() => { void poll(); }, POLL_MS);
      }
    })();
    return () => {
      alive = false;
      if (timer.current !== null) { window.clearInterval(timer.current); timer.current = null; }
    };
  }, [poll]);

  useEffect(() => {
    if (status && !ACTIVE_STATES.has(status.state) && timer.current !== null) {
      window.clearInterval(timer.current);
      timer.current = null;
    }
  }, [status]);

  const start = async () => {
    if (busy) return;
    setBusy(true); setErr(null);
    try {
      setStatus(await renderPreviz(path));
      if (timer.current === null) {
        timer.current = window.setInterval(() => { void poll(); }, POLL_MS);
      }
    } catch (e) {
      setErr(
        e instanceof ApiError
          ? (e.detail?.kind === "previz_render_busy"
              ? "已有渲染在跑，一次只能跑一个"
              : e.detail?.kind === "blender_missing"
                ? "找不到 Blender —— 在 apps/api/.env 里设 BLENDER_EXE"
                : `${e.detail?.kind ?? e.status}`)
          : String(e),
      );
    } finally {
      setBusy(false);
    }
  };

  const stop = async () => {
    try { setStatus(await cancelPreviz(path)); } catch { /* status poll will catch up */ }
  };

  const active = status !== null && ACTIVE_STATES.has(status.state);
  const pct = status?.percent ?? 0;

  return (
    <section style={{ border: "1px solid var(--border)", borderRadius: 8, padding: 12, margin: "12px 0", background: "var(--bg-panel)", color: "var(--text)" }}>
      <div style={{ display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap" }}>
        <strong>🎬 Previz 出片</strong>
        <button type="button" className="drama-rename-btn" disabled={busy || active} onClick={start}>
          {active ? label(status!.state) : "生成 MP4"}
        </button>
        {active ? (
          <button type="button" className="drama-rename-btn" onClick={stop}>停止</button>
        ) : null}
        {status && active ? (
          <span style={{ fontSize: 12, color: "var(--text-muted)" }}>
            {pct}% · {status.rendered_frames}/{status.total_frames || "?"} 帧 · 用时 {clock(status.elapsed_seconds)}
          </span>
        ) : null}
        {status?.state === "done" ? (
          <span style={{ fontSize: 12, color: "#6cc26c" }}>{status.message}</span>
        ) : null}
        {status?.state === "failed" ? (
          <span style={{ fontSize: 12, color: "#e06c6c" }}>失败：{status.message}</span>
        ) : null}
        {err ? <span style={{ fontSize: 12, color: "#e06c6c" }}>错误：{err}</span> : null}
      </div>

      {active ? (
        <div style={{ marginTop: 10, height: 6, borderRadius: 3, background: "var(--border)", overflow: "hidden" }}>
          <div style={{ width: `${pct}%`, height: "100%", background: "#6cc26c", transition: "width .4s linear" }} />
        </div>
      ) : null}

      <div style={{ marginTop: 8, fontSize: 12, color: "var(--text-muted)" }}>
        改 <code>build_previz.py</code> 后先跑它重建 <code>.blend</code>（约 15 秒），改到满意再点这里出片（约 15–30 分钟）。
        {status?.mp4 ? (
          <>
            {" "}当前成片：<a href={`/api/media?path=${encodeURIComponent(status.mp4)}`} target="_blank" rel="noreferrer">{status.mp4.split("/").pop()}</a>
          </>
        ) : null}
      </div>
    </section>
  );
}
