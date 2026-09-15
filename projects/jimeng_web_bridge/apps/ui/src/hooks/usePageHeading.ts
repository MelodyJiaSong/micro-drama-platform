import { useEffect, useRef } from "react";

export const APP_NAME = "即梦桥接";

export function usePageHeading(title: string, detail?: string | null) {
  const ref = useRef<HTMLHeadingElement>(null);

  useEffect(() => {
    ref.current?.focus();
  }, []);

  useEffect(() => {
    document.title = detail ? `${title} · ${detail} · ${APP_NAME}` : `${title} · ${APP_NAME}`;
  }, [title, detail]);

  return ref;
}
