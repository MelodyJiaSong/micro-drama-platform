import { useEffect, useState } from 'react';
import { Api, ApiError } from './api';
import { Composer } from './Composer';
import { JobPanel } from './JobPanel';
import { newRequest, type Capabilities, type Generation, type Job, type Pending, type Plan } from './types';

const pendingKey = 'suno-pending-request-v1';
function readPending(): Pending | null {
  try { const p = JSON.parse(sessionStorage.getItem(pendingKey) ?? 'null'); return p && typeof p.key === 'string' && p.request?.prompt ? p : null; } catch { return null; }
}

export default function App() {
  const [api, setApi] = useState<Api | null>(null), [token, setToken] = useState('');
  const [capabilities, setCapabilities] = useState<Capabilities | null>(null), [jobs, setJobs] = useState<Job[]>([]), [selected, setSelected] = useState('');
  const [pending, setPending] = useState<Pending | null>(readPending), [value, setValue] = useState<Generation>(() => readPending()?.request ?? newRequest());
  const [plan, setPlan] = useState<Plan | null>(null), [error, setError] = useState(''), [busy, setBusy] = useState(false), [notice, setNotice] = useState('');
  const [view, setView] = useState<'create' | 'library'>('create');
  function fail(e: unknown) { setError(e instanceof Error ? e.message : String(e)); }
  function change(g: Generation) { if (!pending) { setValue(g); setPlan(null); setNotice(''); } }
  async function connect() {
    setBusy(true); setError('');
    try {
      const client = new Api(token.trim());
      const [caps, list] = await Promise.all([client.request<Capabilities>('/v1/capabilities'), client.request<Job[]>('/v1/jobs')]);
      setCapabilities(caps); setJobs(list); setSelected(list[0]?.id ?? ''); setApi(client); setToken('');
    } catch (e) { fail(e); } finally { setBusy(false); }
  }
  async function refresh() {
    if (!api) return;
    const [caps, list] = await Promise.all([api.request<Capabilities>('/v1/capabilities'), api.request<Job[]>('/v1/jobs')]);
    setCapabilities(caps); setJobs(list);
    setSelected(old => old || list[0]?.id || '');
  }
  useEffect(() => {
    if (!api) return;
    let stopped = false;
    const timer = window.setInterval(() => { if (!stopped) void refresh().catch(fail); }, 4000);
    return () => { stopped = true; clearInterval(timer); };
  }, [api]);
  async function preflight() {
    if (!api) return;
    setBusy(true); setError('');
    try { setPlan(await api.request<Plan>('/v1/plan', value)); } catch (e) { fail(e); } finally { setBusy(false); }
  }
  async function create() {
    if (!api) return;
    setBusy(true); setError(''); setNotice('');
    let intent = pending;
    try {
      if (!intent) {
        const result = await api.request<Plan>('/v1/plan', value); setPlan(result);
        if (result.automation_paused) throw new Error('Suno 自动化当前暂停，请先完成人工验证。可以继续预检和查看已有任务。');
        intent = { key: `ui-${crypto.randomUUID()}`, request: structuredClone(value) };
        sessionStorage.setItem(pendingKey, JSON.stringify(intent)); setPending(intent);
      }
      const job = await api.request<Job>('/v1/jobs', intent.request, intent.key);
      sessionStorage.removeItem(pendingKey); setPending(null); setSelected(job.id);
      setJobs(old => [job, ...old.filter(j => j.id !== job.id)]);
      setNotice('任务已接受。请在右侧查看进度；生成尚未完成。');
      setValue(newRequest()); setPlan(null);
    } catch (e) {
      if (e instanceof ApiError && [401, 413, 422].includes(e.status)) { sessionStorage.removeItem(pendingKey); setPending(null); }
      fail(e);
    } finally { setBusy(false); }
  }
  return <div className="app"><aside className="sidebar"><a className="brand" href="/ui/"><span className="brand-mark">∿</span><span>Suno<span className="brand-light"> Studio</span></span></a><span className="local-label">LOCAL WORKSPACE</span><nav><button className={view === 'create' ? 'current' : ''} onClick={() => setView('create')}>＋　创作工作台</button><button className={view === 'library' ? 'current' : ''} onClick={() => setView('library')}>♫　任务与音乐</button></nav><div className="sidebar-bottom"><p>从一个想法<br/>到一段声音。</p><a href="/docs" target="_blank" rel="noreferrer">API 文档 ↗</a><a href="/redoc" target="_blank" rel="noreferrer">接口参考 ↗</a><span>本地工具 · 非 Suno 官方客户端</span></div></aside>
    <main><header className="topbar"><span>音乐与声音 / {view === 'create' ? '创作' : '任务库'}</span><div><span className={`connection ${api ? 'online' : ''}`}>{api ? '本机服务已连接' : '等待连接'}</span>{api && <button className="link-button" onClick={() => { setApi(null); setJobs([]); setCapabilities(null); }}>断开</button>}</div></header>
      <div className="page"><div className="page-heading"><div><span className="eyebrow">YOUR NEXT SOUND</span><h1>{view === 'create' ? '让下一幕，拥有声音。' : '把灵感留在这里。'}</h1><p>音乐、氛围与细节声音，在一个工作台完成。</p></div><div className="wave" aria-hidden="true">▂ ▅ ▃ █ ▆ ▃ ▅ ▂</div></div>
        {error && <div className="error" role="alert"><span>{error}</span><button aria-label="关闭错误" onClick={() => setError('')}>×</button></div>}
        {notice && <div className="success" role="status">{notice}</div>}
        {!api || !capabilities ? <section className="card connect-card"><span className="eyebrow">CONNECT</span><h2>连接你的本机服务</h2><p>使用本机服务访问令牌进入工作台。这里不需要 Suno 密码。</p><form onSubmit={e => { e.preventDefault(); void connect(); }}><label className="field"><span>服务访问令牌</span><input type="password" autoComplete="off" value={token} onChange={e => setToken(e.target.value)} placeholder="粘贴本机 service-token.txt 的内容" required/></label><button className="primary" disabled={busy || !token.trim()}>{busy ? '正在连接…' : '进入工作台 →'}</button></form><details className="details"><summary>在哪里找到令牌？</summary><p>在本机仓库根目录运行下面的 PowerShell 命令，然后粘贴到上方。令牌只保存在当前页面内存，刷新页面后需重新输入。</p><pre>Get-Content .audit/service_requests/suno_browser_service/service-token.txt -Raw | Set-Clipboard</pre><p>如果服务未启动，先运行 projects/suno_browser_service/start.ps1。</p></details></section> : <>
          {capabilities.automation_paused && <div className="pause-banner"><span className="pause-icon">Ⅱ</span><div><strong>Suno 自动化已暂停</strong><p>验证码或访问问题需要在专用 Chrome 中人工处理。你仍可以编辑、预检和取回已有音频。</p><details><summary>查看恢复步骤</summary><p>在仓库根依次运行 stop.ps1、login.ps1、start.ps1（均位于 projects/suno_browser_service/）。在普通 Chrome 中完成验证后关闭窗口，等待登录校验成功。未知提交的任务仍需核对歌曲链接。</p></details></div></div>}
          <div className={`workspace ${view === 'library' ? 'library-view' : ''}`}>
            {view === 'create' && <Composer api={api} capabilities={capabilities} value={value} setValue={change} locked={!!pending} busy={busy} plan={plan} onPlan={() => void preflight()} onCreate={() => void create()} onError={fail}/>}
            <JobPanel api={api} jobs={jobs} selected={selected} setSelected={setSelected} onRefresh={refresh} onCopy={g => { if (pending) return fail(new Error('先取得上次提交的明确回执，再开始新任务。')); change({ ...newRequest(), ...g }); setView('create'); }} onError={fail} paused={capabilities.automation_paused}/>
          </div><p className="boundary">当前模式与更多选项已实现；真实 Suno 新控件、官方下载及 Browserless 仍待验收。此工作台不提供声音注册、模型训练、公开发布或 Studio 时间线剪辑。</p>
        </>}
      </div><footer>LOCAL FIRST <span>同一套 API · Web / MCP / CLI</span></footer>
    </main></div>;
}
