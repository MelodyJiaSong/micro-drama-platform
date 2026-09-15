import { useCallback, useEffect, useRef, useState } from "react";
import { api, type ApiError, toApiError } from "../api";
import type { OperationCdto, OperationQdto } from "../types";

export const OPERATION_POLL_MS = 1000;

export interface OperationTracker {
  operation: OperationQdto | OperationCdto | null;
  running: boolean;
  error: ApiError | null;
  start: (launch: () => Promise<OperationCdto>) => Promise<OperationQdto | null>;
}

function finished(state: string): boolean {
  return state === "succeeded" || state === "failed";
}

export function useOperation(): OperationTracker {
  const [operation, setOperation] = useState<OperationQdto | OperationCdto | null>(null);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState<ApiError | null>(null);
  const alive = useRef(true);
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    alive.current = true;
    return () => {
      alive.current = false;
      if (timer.current !== null) clearTimeout(timer.current);
    };
  }, []);

  const start = useCallback(async (launch: () => Promise<OperationCdto>): Promise<OperationQdto | null> => {
    setError(null);
    setRunning(true);
    try {
      const created = await launch();
      if (!alive.current) return null;
      setOperation(created);
      let current: OperationQdto | null = null;
      while (alive.current) {
        await new Promise<void>((resolve) => {
          timer.current = setTimeout(resolve, OPERATION_POLL_MS);
        });
        if (!alive.current) return null;
        current = await api.operation(created.operation_id);
        if (!alive.current) return null;
        setOperation(current);
        if (finished(current.state)) break;
      }
      return current;
    } catch (caught) {
      if (alive.current) setError(toApiError(caught));
      return null;
    } finally {
      if (alive.current) setRunning(false);
    }
  }, []);

  return { operation, running, error, start };
}

export function operationSummary(operation: OperationQdto | OperationCdto | null): string {
  if (operation === null) return "";
  const state = operation.state;
  if (state === "succeeded") return "已完成";
  if (state === "failed") {
    const detail = "error_message" in operation && operation.error_message ? `：${operation.error_message}` : "";
    return `失败${detail}`;
  }
  return state === "running" ? "执行中…" : "等待执行…";
}
