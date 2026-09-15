import { useCallback, useEffect, useRef, useState } from "react";
import { type ApiError, toApiError } from "../api";

export type Resource<T> =
  | { status: "loading"; data: T | null; error: null }
  | { status: "error"; data: T | null; error: ApiError }
  | { status: "ready"; data: T; error: null };

export interface ResourceHandle<T> {
  resource: Resource<T>;
  reload: () => Promise<void>;
  refresh: () => Promise<void>;
  setData: (data: T) => void;
}

export function useResource<T>(loader: () => Promise<T>, deps: readonly unknown[]): ResourceHandle<T> {
  const [resource, setResource] = useState<Resource<T>>({ status: "loading", data: null, error: null });
  const sequence = useRef(0);
  const mounted = useRef(true);
  const loaderRef = useRef(loader);
  loaderRef.current = loader;

  const run = useCallback(async (silent: boolean) => {
    const current = ++sequence.current;
    if (!silent) setResource((previous) => ({ status: "loading", data: previous.data, error: null }));
    try {
      const data = await loaderRef.current();
      if (mounted.current && current === sequence.current) setResource({ status: "ready", data, error: null });
    } catch (error) {
      if (!mounted.current || current !== sequence.current) return;
      setResource((previous) =>
        silent && previous.data !== null ? previous : { status: "error", data: previous.data, error: toApiError(error) },
      );
    }
  }, []);

  const reload = useCallback(() => run(false), [run]);
  const refresh = useCallback(() => run(true), [run]);

  const setData = useCallback((data: T) => {
    sequence.current += 1;
    setResource({ status: "ready", data, error: null });
  }, []);

  useEffect(() => {
    mounted.current = true;
    void run(false);
    return () => {
      mounted.current = false;
    };
  }, deps);

  return { resource, reload, refresh, setData };
}
