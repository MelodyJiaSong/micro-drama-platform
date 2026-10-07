import { useEffect, useState } from "react";
import { QuestionWizard, type InterviewAnswer, type InterviewQuestion } from "./QuestionWizard";
import "./WritersRoomPage.css";

interface Seed { slug: string; characters: {id: string; name: string}[] }
interface Answers { revision: number; characters: Record<string, Record<string, InterviewAnswer>> }
interface Detail { seed: Seed; questions: InterviewQuestion[]; answers: Answers }

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`/api/writers-room${path}`, init);
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail?.message ?? data.detail?.kind ?? `HTTP ${response.status}`);
  return data as T;
}

export function WritersRoomPage(): JSX.Element {
  const [stories, setStories] = useState<Seed[]>([]);
  const [slug, setSlug] = useState("");
  const [detail, setDetail] = useState<Detail | null>(null);
  const [character, setCharacter] = useState("");
  const [error, setError] = useState<string | null>(null);
  useEffect(() => { let disposed = false; void request<Seed[]>("").then(data => { if (!disposed) { setStories(data); setSlug(data[0]?.slug ?? ""); } }).catch(err => { if (!disposed) setError(String(err)); }); return () => { disposed = true; }; }, []);
  useEffect(() => {
    let disposed = false;
    setDetail(null);
    setError(null);
    if (slug) void request<Detail>(`/${slug}`).then(data => { if (!disposed) { setDetail(data); setCharacter(data.seed.characters[0]?.id ?? ""); } }).catch(err => { if (!disposed) setError(String(err)); });
    return () => { disposed = true; };
  }, [slug]);
  const save = async (question: string, answer: InterviewAnswer): Promise<void> => {
    if (!detail) return;
    const next = await request<Answers>(`/${slug}/answers`, {method: "PUT", headers: {"Content-Type": "application/json"}, body: JSON.stringify({character, question_id: question, ...answer, expected_revision: detail.answers.revision})});
    setDetail(old => old?.seed.slug === slug ? {...old, answers: next} : old);
  };
  return <div className="writers-room-page"><h1>编剧室 · 人物访谈</h1><p>一次确定一个具体选择，逐步建立人物的行为和声口。</p>
    <div className="qa-selectors"><label>剧目<select value={slug} onChange={e => setSlug(e.target.value)}>{stories.map(s => <option key={s.slug} value={s.slug}>{s.slug}</option>)}</select></label>{detail && <label>人物<select value={character} onChange={e => setCharacter(e.target.value)}>{detail.seed.characters.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}</select></label>}</div>
    {error && <p role="alert" className="qa-error">{error}</p>}
    {!slug && !error && <p>暂无已创建的编剧室。</p>}
    {slug && !detail && !error && <p role="status">正在加载人物问题…</p>}
    {detail && character && <QuestionWizard key={`${slug}:${character}`} questions={detail.questions} answers={detail.answers.characters[character] ?? {}} onSave={save} />}
  </div>;
}
