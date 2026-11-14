import { useEffect, useRef, useState } from 'react';
import { Api } from './api';
import { statusNames, type AudioFile, type Generation, type Job } from './types';

function Track({ api, job, file, index, onError }: { api: Api; job: Job; file: AudioFile; index: number; onError: (e: unknown) => void }) {
  const [url, setUrl] = useState(''), [busy, setBusy] = useState(false);
  const current = useRef('');
  useEffect(() => () => { if (current.current) URL.revokeObjectURL(current.current); }, []);
  async function load() {
    setBusy(true);
    try { const next = await api.audio(job.id, file); current.current = next; setUrl(next); }
    catch (e) { onError(e); } finally { setBusy(false); }
  }
  return <div className="track"><div className="label-row"><strong>版本 {index + 1} · {job.format.toUpperCase()}</strong><span>{(file.bytes / 1048576).toFixed(1)} MB</span></div>
    {url ? <><audio controls preload="metadata" src={url} aria-label={`试听版本 ${index + 1}`}/><a className="text-link" href={url} download={file.name}>下载音频 ↓</a><small className="verified">SHA256 已核对</small></> : <button className="secondary" disabled={busy} onClick={() => void load()}>{busy ? '读取并校验音频…' : '加载试听 / 下载'}</button>}
  </div>;
}

export function JobPanel({ api, jobs, selected, setSelected, onRefresh, onCopy, onError, paused }: {
  api: Api; jobs: Job[]; selected: string; setSelected: (id: string) => void; onRefresh: () => Promise<void>; onCopy: (value: Partial<Generation>) => void; onError: (e: unknown) => void; paused: boolean;
}) {
  const [filter, setFilter] = useState(''), [urls, setUrls] = useState(''), [resuming, setResuming] = useState(false);
  const job = jobs.find(j => j.id === selected);
  const visible = jobs.filter(j => `${j.request.title ?? ''} ${j.prompt} ${j.id}`.toLowerCase().includes(filter.toLowerCase()));
  useEffect(() => setUrls(''), [selected]);
  async function resume() {
    if (!job) return;
    setResuming(true);
    try { await api.request(`/v1/jobs/${job.id}/resume`, { song_urls: urls.split(/\s+/).filter(Boolean) }); await onRefresh(); }
    catch (e) { onError(e); } finally { setResuming(false); }
  }
  return <section className="card library"><div className="section-head"><div><span className="eyebrow">LIBRARY</span><h2>我的任务 <span className="count">{jobs.length}</span></h2></div><button className="icon-button" aria-label="刷新任务" onClick={() => void onRefresh().catch(onError)}>↻</button></div>
    <input className="search" aria-label="搜索任务" placeholder="搜索标题、描述或任务 ID" value={filter} onChange={e => setFilter(e.target.value)}/>
    <div className="job-list">{visible.map(j => <button className={`job-row ${selected === j.id ? 'active' : ''}`} key={j.id} onClick={() => setSelected(j.id)}><span className="art">♫</span><span className="job-text"><strong>{j.request.title || j.prompt.slice(0, 30)}</strong><small>{new Date(j.created_at).toLocaleString('zh-CN', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })} · {j.request.mode ?? 'advanced'}</small></span><span className={`status status-${j.status}`}>{statusNames[j.status] ?? j.status}</span></button>)}</div>
    {!visible.length && <div className="empty"><span>♫</span><h3>{jobs.length ? '没有匹配的任务' : '给你的故事一段旋律'}</h3><p>{jobs.length ? '换个关键词试试。' : '从左侧开始创作，生成进度和音频会出现在这里。'}</p></div>}
    {job && <div className="job-detail"><div className="label-row"><h3>{job.request.title || '任务详情'}</h3><span className={`status status-${job.status}`}>{statusNames[job.status] ?? job.status}</span></div><p className="job-prompt">{job.prompt}</p><code className="job-id">{job.id}</code>
      {job.error && <div className="notice"><strong>{job.error.code}</strong><p>{job.error.message}</p></div>}
      {job.status === 'uncertain' && <p className="notice">可能已提交并消耗积分。请在 Suno 确认本任务歌曲，将链接填入下方，只补收下载。</p>}
      {job.files.map((file, i) => <Track key={`${job.id}-${file.name}`} api={api} job={job} file={file} index={i} onError={onError}/>)}
      {!job.files.length && <p className="muted">尚无已下载音频。任务每 4 秒自动刷新。</p>}
      {['needs_login', 'needs_attention', 'uncertain'].includes(job.status) && <details className="details"><summary>处理问题与恢复</summary><p className="muted">先解决错误原因。已确认歌曲只补下载；确定尚未提交的任务恢复后会首次生成。验证码暂停需在专用 Chrome 中人工处理。</p><label className="field"><span>本任务的 Suno 歌曲链接</span><textarea rows={2} value={urls} onChange={e => setUrls(e.target.value)} placeholder="每行一条，最多两条；未知提交时必填"/></label><button className="secondary" disabled={resuming || paused || (job.status === 'uncertain' && !urls.trim() && !job.song_urls.length)} onClick={() => void resume()}>{resuming ? '正在恢复…' : '恢复原任务'}</button></details>}
      <details className="details"><summary>请求、已应用选项与下一步</summary><pre>{JSON.stringify({ request: job.request, applied_options: job.applied_options, next_action: job.next_action }, null, 2)}</pre></details>
      {job.status === 'completed' && <button className="secondary" onClick={() => onCopy(job.request)}>使用这些设置创作新任务</button>}
    </div>}
  </section>;
}
