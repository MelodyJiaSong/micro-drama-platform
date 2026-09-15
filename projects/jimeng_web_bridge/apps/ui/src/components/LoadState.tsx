import type { ReactNode } from "react";
import type { ApiError } from "../api";
import type { ResourceHandle } from "../hooks/useResource";

export function Loading({ label = "加载中…" }: { label?: string }) {
  return (
    <p role="status" aria-busy="true" className="loading">
      {label}
    </p>
  );
}

interface ErrorBlockProps {
  error: ApiError;
  title?: string;
  onRetry?: () => void;
}

export function ErrorBlock({ error, title = "加载失败", onRetry }: ErrorBlockProps) {
  return (
    <div role="alert" className="error-block">
      <p>
        <strong>{title}</strong>：{error.body.message}
      </p>
      {error.body.hint ? <p>提示：{error.body.hint}</p> : null}
      {error.body.config_key ? (
        <p>
          相关 config 键：<code>{error.body.config_key}</code>
        </p>
      ) : null}
      {onRetry ? (
        <button type="button" onClick={onRetry}>
          重试
        </button>
      ) : null}
    </div>
  );
}

export function Empty({ children }: { children: ReactNode }) {
  return <p className="empty">{children}</p>;
}

interface ResourceViewProps<T> {
  handle: ResourceHandle<T>;
  errorTitle?: string;
  loadingLabel?: string;
  children: (data: T) => ReactNode;
}

export function ResourceView<T>({ handle, errorTitle, loadingLabel, children }: ResourceViewProps<T>) {
  const { resource } = handle;
  const retry = () => void handle.reload();
  if (resource.data === null) {
    if (resource.status === "error") return <ErrorBlock error={resource.error} title={errorTitle} onRetry={retry} />;
    return <Loading label={loadingLabel} />;
  }
  return (
    <>
      {resource.status === "error" ? <ErrorBlock error={resource.error} title="刷新失败，显示的是上一次的数据" onRetry={retry} /> : null}
      {children(resource.data)}
    </>
  );
}
