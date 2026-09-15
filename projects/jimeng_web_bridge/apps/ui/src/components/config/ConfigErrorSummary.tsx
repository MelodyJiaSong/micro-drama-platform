import { useState } from "react";
import { focusConfigKey } from "../../config/configDraft";

interface ConfigErrorSummaryProps {
  title: string;
  message: string;
  path: string | null;
  hint?: string | null;
  live: boolean;
}

export function ConfigErrorSummary({ title, message, path, hint, live }: ConfigErrorSummaryProps) {
  const [noControl, setNoControl] = useState(false);
  return (
    <div role={live ? "alert" : undefined} className="error-block">
      <p>
        <span aria-hidden="true">✕ </span>
        <strong>{title}</strong>：{message}
      </p>
      {hint ? <p>提示：{hint}</p> : null}
      {path ? (
        <p>
          字段 <code>{path}</code>{" "}
          <button type="button" onClick={() => setNoControl(!focusConfigKey(path))}>
            跳到字段 {path}
          </button>
          {noControl ? <span>（表单里没有这个字段的控件，请在原文 TOML 视图里修改完整路径 {path}）</span> : null}
        </p>
      ) : null}
    </div>
  );
}
