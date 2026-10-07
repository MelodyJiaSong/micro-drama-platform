import { useEffect, useRef, useState } from "react";

export interface InterviewQuestion {
  id: string;
  dimension: string;
  title: string;
  options: { value: string; label: string }[];
  multiple: boolean;
}
export interface InterviewAnswer { choice: string; note: string }

interface Props {
  questions: InterviewQuestion[];
  answers: Record<string, InterviewAnswer>;
  onSave: (question: string, answer: InterviewAnswer) => Promise<void>;
}

export function QuestionWizard({ questions, answers, onSave }: Props): JSX.Element {
  const [index, setIndex] = useState(() => {
    const first = questions.findIndex(q => !answers[q.id]);
    return first < 0 ? questions.length : first;
  });
  const [custom, setCustom] = useState(false);
  const [note, setNote] = useState("");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inFlight = useRef(false);
  const question = questions[index];
  const heading = useRef<HTMLHeadingElement>(null);
  const answered = questions.filter(q => answers[q.id]).length;

  useEffect(() => {
    setCustom(answers[question?.id]?.choice === "custom");
    setNote(answers[question?.id]?.note ?? "");
    setError(null);
    heading.current?.focus();
  }, [question?.id]);

  const submit = async (choice: string): Promise<void> => {
    if (!question || inFlight.current || (choice === "custom" && !note.trim())) return;
    inFlight.current = true;
    setSaving(true);
    setError(null);
    try {
      await onSave(question.id, { choice, note: note.trim() });
      setIndex(value => value + 1);
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      inFlight.current = false;
      setSaving(false);
    }
  };

  useEffect(() => {
    const onKey = (event: KeyboardEvent): void => {
      const target = event.target as HTMLElement;
      if (event.repeat || event.ctrlKey || event.metaKey || event.altKey || target.closest("input,textarea,select,[contenteditable=true]")) return;
      const option = question?.options.find(o => o.value.toLowerCase() === event.key.toLowerCase());
      if (option && !custom) { event.preventDefault(); void submit(option.value); }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [question, note, custom, onSave]);

  return <section className="qa-wizard" aria-label="人物访谈">
    <div className="qa-progress"><span>已保存 {answered} / {questions.length}</span><progress max={questions.length} value={answered} /></div>
    {question ? <>
      <p className="qa-dimension">{question.dimension} · 第 {index + 1} 题</p>
      <h2 ref={heading} tabIndex={-1}>{question.title}</h2>
      <p className="qa-hint">点击选项或按字母键，保存后自动进入下一题。</p>
      <div className="qa-options">
        {question.options.map(option => <button key={option.value} disabled={saving} className={answers[question.id]?.choice === option.value ? "qa-option selected" : "qa-option"} onClick={() => void submit(option.value)}>
          <strong>{option.value}</strong><span>{option.label}</span>{answers[question.id]?.choice === option.value && <small>已选</small>}
        </button>)}
        <button disabled={saving} className="qa-option" onClick={() => setCustom(!custom)}><strong>✎</strong><span>写自己的答案</span></button>
      </div>
      <label className="qa-note">{custom ? "你的答案" : "补充具体经历或例外（可选）"}<textarea value={note} disabled={saving} maxLength={5000} onChange={event => setNote(event.target.value)} placeholder="例如：被朋友关心时先开玩笑，独处时才回头替对方做件事。" /></label>
      {custom && <button className="qa-primary" disabled={saving || !note.trim()} onClick={() => void submit("custom")}>保存并继续 →</button>}
      <div className="qa-controls"><button disabled={saving || index === 0} onClick={() => setIndex(i => i-1)}>← 上一题</button>{answers[question.id] && <button disabled={saving} onClick={() => setIndex(i => i+1)}>保留答案，下一题 →</button>}<span role="status">{saving ? "保存中…" : "选项不会自动提交默认值"}</span></div>
    </> : <>
      <h2 ref={heading} tabIndex={-1}>本轮访谈已完成</h2><p>答案已保存。可以返回修改，或切换下一位人物。</p><button onClick={() => setIndex(0)}>从第一题检查</button>
    </>}
    {error && <p className="qa-error" role="alert">{error}（尚未跳题，请重试）</p>}
  </section>;
}
