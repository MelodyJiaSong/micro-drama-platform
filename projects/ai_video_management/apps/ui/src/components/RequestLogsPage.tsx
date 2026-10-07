import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "./RequestLogsPage.css";

interface LogFile { path: string; bytes: number; modified_at: number; }
interface LogEvent { request_id?: string; time?: string; provider?: string; operation?: string; event?: string; target?: string; [key: string]: unknown; }
interface LogResponse { logs: LogFile[]; entries: LogEvent[]; total: number; }
const PAGE_SIZE = 50;

export function RequestLogsPage(): JSX.Element {
  const [logs, setLogs] = useState<LogFile[]>([]);
  const [path, setPath] = useState("");
  const [entries, setEntries] = useState<LogEvent[]>([]);
  const [total, setTotal] = useState(0);
  const [offset, setOffset] = useState(0);
  const [error, setError] = useState("");
  const [refresh, setRefresh] = useState(0);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const controller = new AbortController();
    void fetch("/api/request-logs", { signal: controller.signal }).then(async r => {
      if (!r.ok) throw new Error(`请求日志列表读取失败 (${r.status})`);
      return r.json() as Promise<LogResponse>;
    }).then(r => { setLogs(r.logs); setPath(p => p || r.logs[0]?.path || ""); })
      .catch(e => { if (e.name !== "AbortError") setError(String(e.message)); });
    return () => controller.abort();
  }, [refresh]);

  useEffect(() => {
    if (!path) return;
    const controller = new AbortController();
    setLoading(true); setError(""); setEntries([]);
    void fetch(`/api/request-log?path=${encodeURIComponent(path)}&offset=${offset}&limit=${PAGE_SIZE}`, { signal: controller.signal })
      .then(async r => { if (!r.ok) throw new Error(`请求日志读取失败 (${r.status})`); return r.json() as Promise<LogResponse>; })
      .then(r => { setEntries(r.entries); setTotal(r.total); })
      .catch(e => { if (e.name !== "AbortError") setError(String(e.message)); })
      .finally(() => { if (!controller.signal.aborted) setLoading(false); });
    return () => controller.abort();
  }, [path, offset, refresh]);

  return <section className="request-logs-page">
    <h1>外部服务请求日志</h1>
    <p>每集各一份，人物、场景、道具、装备等按资产目录共用。请求先记录，再执行；结果与请求用同一个 ID 关联。</p>
    <div className="request-log-toolbar">
      <label>日志范围 <select value={path} onChange={e => { setPath(e.target.value); setOffset(0); }}>
        {logs.map(log => <option key={log.path} value={log.path}>{log.path.replace(/^ai_videos\//, "").replace(/\/request_log\.md$/, "")}</option>)}
      </select></label>
      <button onClick={() => setRefresh(n => n + 1)}>刷新</button>
      {path && <Link to={`/file/${encodeURIComponent(path)}`}>查看原始 Markdown</Link>}
    </div>
    {error && <p role="alert">{error}</p>}
    {!logs.length && !error && <p>暂无记录。接入日志的服务首次调用时会创建 request_log.md。</p>}
    {loading && <p role="status">正在读取…</p>}
    <p>{total} 条事件；最新在前。费用以服务返回值为准，未返回费用时按未知处理。</p>
    {entries.map((entry, index) => <details key={`${entry.request_id}-${entry.event}-${index}`} className="request-log-entry">
      <summary><time>{entry.time ? new Date(entry.time).toLocaleString("zh-CN") : "时间未知"}</time> · {entry.provider} · {entry.operation} · <strong>{entry.event}</strong></summary>
      <p>{entry.target}</p><p>请求 ID：{entry.request_id}</p>
      <pre>{JSON.stringify(entry, null, 2)}</pre>
    </details>)}
    <nav aria-label="日志分页"><button disabled={!offset || loading} onClick={() => setOffset(n => Math.max(0, n - PAGE_SIZE))}>上一页</button>
      <button disabled={offset + PAGE_SIZE >= total || loading} onClick={() => setOffset(n => n + PAGE_SIZE)}>下一页</button></nav>
  </section>;
}
