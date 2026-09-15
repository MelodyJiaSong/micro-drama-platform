import { useEffect, useRef } from "react";

/** Runs `task` every `intervalMs` after the previous run settles, so polls never overlap; stops on unmount. */
export function usePoll(task: () => Promise<void>, intervalMs: number, enabled: boolean): void {
  const taskRef = useRef(task);
  taskRef.current = task;

  useEffect(() => {
    if (!enabled) return;
    let cancelled = false;
    let timer: ReturnType<typeof setTimeout> | null = null;
    const schedule = () => {
      timer = setTimeout(async () => {
        try {
          await taskRef.current();
        } finally {
          if (!cancelled) schedule();
        }
      }, intervalMs);
    };
    schedule();
    return () => {
      cancelled = true;
      if (timer !== null) clearTimeout(timer);
    };
  }, [intervalMs, enabled]);
}
