import { useCallback, useState } from "react";
import { type ApiError, toApiError } from "../api";
import type { ConfigSaveBody } from "../types";

export interface ConfigSaveState {
  saving: boolean;
  error: ApiError | null;
  conflict: boolean;
  unsavedAfterConflict: boolean;
}

const IDLE: ConfigSaveState = { saving: false, error: null, conflict: false, unsavedAfterConflict: false };

export function useConfigSave<T>(save: (body: ConfigSaveBody) => Promise<T>) {
  const [state, setState] = useState<ConfigSaveState>(IDLE);

  const submit = useCallback(
    async (body: ConfigSaveBody): Promise<T | null> => {
      setState({ ...IDLE, saving: true });
      try {
        const result = await save(body);
        setState(IDLE);
        return result;
      } catch (caught) {
        const error = toApiError(caught);
        const conflict = error.status === 409 && error.body.error_code === "config_conflict";
        setState({ saving: false, error: conflict ? null : error, conflict, unsavedAfterConflict: false });
        return null;
      }
    },
    [save],
  );

  const keepEditing = useCallback(() => setState({ ...IDLE, unsavedAfterConflict: true }), []);
  const fail = useCallback((error: ApiError) => setState({ ...IDLE, error }), []);

  return { state, submit, keepEditing, fail };
}
