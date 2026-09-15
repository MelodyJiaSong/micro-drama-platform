import { useId } from "react";
import type { NeedsConfirmationQdto } from "../../types";

export function NeedsConfirmationList({ items }: { items: NeedsConfirmationQdto[] }) {
  const headingId = useId();
  if (items.length === 0) return null;
  return (
    <section className="panel pinned" aria-labelledby={headingId}>
      <h2 id={headingId}>
        <span aria-hidden="true">⚠ </span>
        {items.length} 项需要你确认
      </h2>
      <ul>
        {items.map((item) => {
          const reasonId = `${headingId}-${item.key}`;
          return (
            <li key={`${item.code}-${item.key}`} aria-describedby={reasonId}>
              <span className="badge badge-warning">
                <span aria-hidden="true">⚠ </span>需要你确认
              </span>{" "}
              <strong>{item.key}</strong>
              <span id={reasonId}>：{item.reason}</span>
              {item.suggestion ? <span>。建议：{item.suggestion}</span> : null}
              {item.config_key ? (
                <span>
                  。填写 <code>{item.config_key}</code>
                </span>
              ) : null}
              {item.shots.length > 0 ? <span>。涉及：{item.shots.join("、")}</span> : null}
            </li>
          );
        })}
      </ul>
    </section>
  );
}
