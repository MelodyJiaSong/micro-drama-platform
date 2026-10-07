import { createContext, useContext, useEffect, useState, useCallback } from "react";
import type { ReactNode } from "react";
import { loadGlobal, type GlobalCatalog } from "../lib/globalWorkflow";

const Context = createContext<{ catalog: GlobalCatalog | null; error: string; refresh: () => void }>({ catalog: null, error: "", refresh: () => {} });
export const useGlobalWorkflow = () => useContext(Context);

export function GlobalWorkflowProvider({ children }: { children: ReactNode }): JSX.Element {
  const [catalog, setCatalog] = useState<GlobalCatalog | null>(null);
  const [error, setError] = useState("");
  const [version, setVersion] = useState(0);
  const refresh = useCallback(() => setVersion(value => value + 1), []);
  useEffect(() => {
    const controller = new AbortController();
    setError("");
    loadGlobal<GlobalCatalog>("/api/global-workflow", controller.signal).then(value => {
      if (!controller.signal.aborted) setCatalog(value);
    }).catch((reason: unknown) => {
      if (!controller.signal.aborted) setError(reason instanceof Error ? reason.message : String(reason));
    });
    return () => controller.abort();
  }, [version]);
  return <Context.Provider value={{ catalog, error, refresh }}>{children}</Context.Provider>;
}
