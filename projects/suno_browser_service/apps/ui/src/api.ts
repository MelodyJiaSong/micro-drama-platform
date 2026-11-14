import type { AudioFile } from './types';

export class ApiError extends Error {
  constructor(message: string, public status = 0) { super(message); }
}

export class Api {
  constructor(private token: string) {}
  async request<T>(path: string, body?: unknown, key?: string): Promise<T> {
    const headers: Record<string, string> = { Authorization: `Bearer ${this.token}` };
    if (key) headers['Idempotency-Key'] = key;
    if (body && !(body instanceof FormData)) headers['Content-Type'] = 'application/json';
    let response: Response;
    try {
      response = await fetch(path, { method: body === undefined ? 'GET' : 'POST', headers, body: body instanceof FormData ? body : body === undefined ? undefined : JSON.stringify(body), signal: AbortSignal.timeout(30000) });
    } catch { throw new ApiError('无法连接本机服务。提交超时时保留原请求与任务键，重试会查询或提交同一任务。'); }
    const data = await response.json();
    if (!response.ok) throw new ApiError(data.error ? `${data.error.code}：${data.error.message}` : Array.isArray(data.detail) ? data.detail.map((d: {loc: string[]; msg: string}) => `${d.loc.join('.')}：${d.msg}`).join('\n') : '请求失败', response.status);
    return data as T;
  }
  async audio(job: string, file: AudioFile): Promise<string> {
    const response = await fetch(`/v1/jobs/${encodeURIComponent(job)}/files/${encodeURIComponent(file.name)}`, { headers: { Authorization: `Bearer ${this.token}` }, signal: AbortSignal.timeout(60000) });
    if (!response.ok) throw new ApiError('音频读取失败，请刷新任务后重试。', response.status);
    const bytes = await response.arrayBuffer();
    const digest = await crypto.subtle.digest('SHA-256', bytes);
    const sha = Array.from(new Uint8Array(digest), b => b.toString(16).padStart(2, '0')).join('');
    if (bytes.byteLength !== file.bytes || sha !== file.sha256) throw new ApiError('音频大小或 SHA256 校验失败，未提供试听或下载。');
    return URL.createObjectURL(new Blob([bytes], { type: file.name.endsWith('.wav') ? 'audio/wav' : 'audio/mpeg' }));
  }
}
