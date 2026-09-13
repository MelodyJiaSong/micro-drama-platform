/** 口径层: the dataset's own 评分标准 (criteria) rendered compactly — one line per
 * rule, its argument on demand — plus 方法 (method) behind a collapsible. Every
 * number on the dashboard is only readable next to these, so they ship with it. */
import { useState } from "react";
import { Rich } from "./ResearchText";

/** Criteria open with a bold lead clause; split it so the list can show one
 * headline per rule and keep the supporting argument collapsed. */
function splitLead(text: string): { lead: string; rest: string } {
  if (text.startsWith("**")) {
    const end = text.indexOf("**", 2);
    if (end > 0) return { lead: text.slice(2, end), rest: text.slice(end + 2).trim() };
  }
  const stop = text.indexOf("。");
  return stop > 0
    ? { lead: text.slice(0, stop + 1), rest: text.slice(stop + 1).trim() }
    : { lead: text, rest: "" };
}

interface CriterionProps {
  index: number;
  text: string;
}

function Criterion({ index, text }: CriterionProps): JSX.Element {
  const [open, setOpen] = useState(false);
  const { lead, rest } = splitLead(text);
  const bodyId = `research-criterion-${index}`;
  return (
    <li className="research-criterion">
      <span className="research-criterion-no" aria-hidden="true">
        {index + 1}
      </span>
      <div className="research-criterion-body">
        <p className="research-criterion-lead">
          <Rich text={lead} />
        </p>
        {rest ? (
          <>
            <button
              type="button"
              className="research-inline-toggle"
              aria-expanded={open}
              aria-controls={bodyId}
              onClick={() => setOpen(!open)}
            >
              {open ? "收起理由" : "展开理由"}
            </button>
            <p id={bodyId} className="research-criterion-rest" hidden={!open}>
              <Rich text={rest} />
            </p>
          </>
        ) : null}
      </div>
    </li>
  );
}

export interface ResearchDashboardMethodProps {
  criteria: string[];
  method: string;
  window: { from: string; to: string };
  generatedAt: string;
}

export function ResearchDashboardMethod({
  criteria,
  method,
  window: win,
  generatedAt,
}: ResearchDashboardMethodProps): JSX.Element {
  const [open, setOpen] = useState(false);
  return (
    <section className="research-dash-method" aria-label="口径与方法">
      <h3 className="research-dash-h3">
        排名口径
        <span className="research-dash-h3-note">这张表按什么排，先读这 {criteria.length} 条</span>
      </h3>
      <ol className="research-criteria-list">
        {criteria.map((c, i) => (
          <Criterion key={i} index={i} text={c} />
        ))}
      </ol>

      <button
        type="button"
        className="research-method-toggle"
        aria-expanded={open}
        aria-controls="research-method-body"
        onClick={() => setOpen(!open)}
      >
        <span className="research-method-caret" aria-hidden="true">
          {open ? "▾" : "▸"}
        </span>
        方法与口径
        <span className="research-method-meta">
          窗口 {win.from} – {win.to} · 生成于 {generatedAt}
        </span>
      </button>
      <div id="research-method-body" className="research-method-body" hidden={!open}>
        <p>
          <Rich text={method} />
        </p>
      </div>
    </section>
  );
}
