/** EvalPage: the ai_video_eval module — read-only verdict browsing + editable
 * rubric/settings. Eval runs are triggered from the CLI only, never from here. */
import { useSearchParams } from "react-router-dom";
import { EvalRunsView } from "./EvalRunsView";
import { EvalRubricView } from "./EvalRubricView";
import { EvalConfigView } from "./EvalConfigView";

const TABS: Array<{ id: string; label: string }> = [
  { id: "runs", label: "评测结果" },
  { id: "rubric", label: "Rubric" },
  { id: "config", label: "设置" },
];

export function EvalPage(): JSX.Element {
  const [searchParams, setSearchParams] = useSearchParams();
  const tab = searchParams.get("tab") ?? "runs";

  return (
    <div className="eval-page">
      <header className="eval-header">
        <h1>评测中心 · ai_video_eval</h1>
        <p className="muted">
          评测由 CLI 触发（<code>projects/ai_video_eval</code>），此处只读结果；Rubric 与运行设置可编辑。
        </p>
        <div className="eval-tabs" role="tablist">
          {TABS.map((t) => (
            <button
              key={t.id}
              type="button"
              role="tab"
              aria-selected={tab === t.id}
              className={tab === t.id ? "eval-tab eval-tab-active" : "eval-tab"}
              onClick={() => setSearchParams({ tab: t.id })}
            >
              {t.label}
            </button>
          ))}
        </div>
      </header>
      {tab === "rubric" ? <EvalRubricView /> : tab === "config" ? <EvalConfigView /> : <EvalRunsView />}
    </div>
  );
}
