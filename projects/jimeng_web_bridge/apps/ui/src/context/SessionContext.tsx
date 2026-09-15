import { createContext, type ReactNode, useContext } from "react";
import { api } from "../api";
import { usePoll } from "../hooks/usePoll";
import { type ResourceHandle, useResource } from "../hooks/useResource";
import type { SessionStatusQdto } from "../types";

export const SESSION_POLL_MS = 10_000;

const SessionContext = createContext<ResourceHandle<SessionStatusQdto> | null>(null);

export function SessionProvider({ children }: { children: ReactNode }) {
  const handle = useResource(() => api.session(), []);
  usePoll(handle.refresh, SESSION_POLL_MS, true);
  return <SessionContext.Provider value={handle}>{children}</SessionContext.Provider>;
}

export function useSession(): ResourceHandle<SessionStatusQdto> {
  const handle = useContext(SessionContext);
  if (handle === null) throw new Error("SessionProvider missing");
  return handle;
}
