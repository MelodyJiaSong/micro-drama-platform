/**
 * Live file changes (follow-up 280): one shared `EventSource` on `/api/events`.
 * The server sends `change` events whose data is `{"paths": [...]}` — repo-
 * relative paths under `ai_videos/` (`"*"` means "too many, refresh what you
 * show"). Listeners get debounced batches; the connection opens with the first
 * listener and closes with the last. The browser reconnects by itself.
 */
import { useEffect, useRef } from "react";

export type ChangeListener = (paths: string[]) => void;

const listeners = new Set<ChangeListener>();
let source: EventSource | null = null;

function open(): void {
  if (source || typeof EventSource === "undefined") return;
  source = new EventSource("/api/events");
  source.addEventListener("change", (event) => {
    let paths: string[] = [];
    try {
      const data = JSON.parse((event as MessageEvent<string>).data) as { paths?: unknown };
      if (Array.isArray(data.paths)) paths = data.paths.filter((p): p is string => typeof p === "string");
    } catch {
      return;
    }
    if (!paths.length) return;
    for (const listener of [...listeners]) listener(paths);
  });
}

export function subscribeFileChanges(listener: ChangeListener): () => void {
  listeners.add(listener);
  open();
  return () => {
    listeners.delete(listener);
    if (listeners.size === 0 && source) {
      source.close();
      source = null;
    }
  };
}

/** Whether a batch touches `prefix` (a folder, without trailing slash) or is a reset. */
export function touches(paths: readonly string[], prefix: string): boolean {
  return paths.some(p => p === "*" || p === prefix || p.startsWith(`${prefix}/`));
}

/** Call `onChange` (debounced) when files under `prefix` change. */
export function useFileChanges(prefix: string | null, onChange: (paths: string[]) => void, delayMs = 400): void {
  const callback = useRef(onChange);
  callback.current = onChange;
  useEffect(() => {
    if (!prefix) return undefined;
    let pending: string[] = [];
    let timer: ReturnType<typeof setTimeout> | null = null;
    const unsubscribe = subscribeFileChanges((paths) => {
      if (!touches(paths, prefix)) return;
      pending = pending.concat(paths);
      if (timer) clearTimeout(timer);
      timer = setTimeout(() => {
        const batch = pending;
        pending = [];
        timer = null;
        callback.current(batch);
      }, delayMs);
    });
    return () => {
      if (timer) clearTimeout(timer);
      unsubscribe();
    };
  }, [prefix, delayMs]);
}
