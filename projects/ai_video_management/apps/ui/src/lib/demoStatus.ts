/**
 * 英雄 demo 定版标记（follow-up 315）：后端 `GET /api/demo-status` 列出 demo 已定版的人物
 * （`demo/edit/final/cut_v*.json` 的 status 以「定版」/「锁片」开头，取最高版本）和发布文案状态。
 * 整个页面共用一份：第一次用时取，`ai_videos/` 下任何 `/demo/` 文件变了重取。
 */
import { useEffect, useState } from "react";
import { subscribeFileChanges } from "./fileEvents";

export interface DemoStatus {
  hero: string; folder: string; version: number; cut: string; video: string; status: string;
  /** 定版之后又剪、还没定的版本。 */
  newer: number[];
  publish: string; publish_video: string;
  publish_state: "ok" | "stale" | "missing";
}
export type DemoStatusMap = ReadonlyMap<string, DemoStatus>;

const EMPTY: DemoStatusMap = new Map();
let current: DemoStatusMap = EMPTY;
let pending: Promise<void> | null = null;
const listeners = new Set<(map: DemoStatusMap) => void>();
let unsubscribe: (() => void) | null = null;
let timer: ReturnType<typeof setTimeout> | null = null;

function load(): Promise<void> {
  pending ??= fetch("/api/demo-status", { cache: "no-store" })
    .then(r => (r.ok ? r.json() : { heroes: [] }))
    .then((data: { heroes?: DemoStatus[] }) => {
      current = new Map((data.heroes ?? []).map(h => [h.hero, h]));
      for (const listener of [...listeners]) listener(current);
    })
    .catch(() => undefined)
    .finally(() => { pending = null; });
  return pending;
}

function watch(): void {
  if (unsubscribe) return;
  unsubscribe = subscribeFileChanges(paths => {
    if (!paths.some(p => p === "*" || p.includes("/demo/"))) return;
    if (timer) clearTimeout(timer);
    timer = setTimeout(() => { timer = null; void load(); }, 500);
  });
}

/** 人物目录 → 定版信息；没有定版的人物不在表里。 */
export function useDemoStatus(): DemoStatusMap {
  const [map, setMap] = useState<DemoStatusMap>(current);
  useEffect(() => {
    listeners.add(setMap);
    watch();
    if (current === EMPTY) void load(); else setMap(current);
    return () => {
      listeners.delete(setMap);
      if (listeners.size === 0 && unsubscribe) { unsubscribe(); unsubscribe = null; }
    };
  }, []);
  return map;
}

const PUBLISH_NOTE: Record<DemoStatus["publish_state"], string> = {
  ok: "发布文案已按定版成片写好",
  stale: "发布文案写的不是定版成片，需要更新",
  missing: "还没有发布文案 demo/publish.md",
};

export function demoStatusTitle(s: DemoStatus): string {
  return [
    `Demo 定版 v${s.version}：${s.status}`,
    s.video ? `成片 ${s.video.split("/").pop()}` : "定版成片文件不在",
    s.newer.length ? `之后还有未定的 v${s.newer.join(" / v")}` : "",
    PUBLISH_NOTE[s.publish_state] + (s.publish_state === "stale" && s.publish_video ? `（写的是 ${s.publish_video}）` : ""),
  ].filter(Boolean).join("\n");
}

/** 发布文案对得上定版成片才算交付齐。 */
export const publishReady = (s: DemoStatus): boolean => s.publish_state === "ok" && Boolean(s.video);

/** 测试用：清掉共用缓存。 */
export function resetDemoStatusForTest(): void {
  current = EMPTY; pending = null; listeners.clear();
  if (unsubscribe) { unsubscribe(); unsubscribe = null; }
}
