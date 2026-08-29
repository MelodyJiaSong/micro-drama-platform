/** EvalConfigView: edit ai_video_eval's runtime settings (eval_config.yaml).
 * Non-result settings only — runs/ artifacts are never writable from the UI. */
import { useEffect, useState } from "react";
import { fetchEvalConfig, putEvalConfig } from "../lib/evalApi";

export function EvalConfigView(): JSX.Element {
  const [content, setContent] = useState<string>("");
  const [loaded, setLoaded] = useState<boolean>(false);
  const [dirty, setDirty] = useState<boolean>(false);
  const [status, setStatus] = useState<{ kind: "ok" | "err"; text: string } | null>(null);

  useEffect(() => {
    fetchEvalConfig()
      .then((r) => {
        setContent(r.content);
        setLoaded(true);
      })
      .catch((err: Error) => setStatus({ kind: "err", text: err.message }));
  }, []);

  const onSave = async (): Promise<void> => {
    setStatus(null);
    try {
      const result = await putEvalConfig(content);
      setDirty(false);
      setStatus({ kind: "ok", text: `已保存（${result.output}）` });
    } catch (err) {
      setStatus({ kind: "err", text: err instanceof Error ? err.message : String(err) });
    }
  };

  return (
    <section className="eval-card">
      <h2>运行设置 · config/eval_config.yaml</h2>
      <p className="muted">
        评审引擎 / 模型 / 样本数 / 并发 / 预算 / grounding 上限 / 项目豁免。保存前做 YAML 解析校验。
      </p>
      {loaded ? (
        <>
          <textarea
            className="eval-editor"
            value={content}
            spellCheck={false}
            onChange={(e) => {
              setContent(e.target.value);
              setDirty(true);
            }}
            rows={28}
            aria-label="eval_config.yaml 编辑器"
          />
          <div className="eval-editor-bar">
            <button type="button" className="eval-btn" disabled={!dirty} onClick={() => void onSave()}>
              保存
            </button>
            {status ? (
              <span className={status.kind === "ok" ? "eval-status-ok" : "eval-status-err"}>
                {status.text}
              </span>
            ) : null}
          </div>
        </>
      ) : status ? (
        <p className="eval-status-err">{status.text}</p>
      ) : (
        <p className="muted">加载中…</p>
      )}
    </section>
  );
}
