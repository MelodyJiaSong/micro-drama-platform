import { useRef, useState } from 'react';
import { Api } from './api';
import { Options } from './Options';
import type { Capabilities, Generation, Mode, Plan } from './types';

export function Composer({ api, capabilities, value, setValue, locked, busy, plan, onPlan, onCreate, onError }: {
  api: Api; capabilities: Capabilities; value: Generation; setValue: (g: Generation) => void; locked: boolean; busy: boolean; plan: Plan | null; onPlan: () => void; onCreate: () => void; onError: (e: unknown) => void;
}) {
  const [rights, setRights] = useState(false), [uploading, setUploading] = useState(false), [url, setUrl] = useState('');
  const [names, setNames] = useState<Record<string, string>>({});
  const fileInput = useRef<HTMLInputElement>(null);
  const patch = (data: Partial<Generation>) => setValue({ ...value, ...data });
  function mode(next: Mode) { patch({ mode: next, options: {}, references: [], lyrics: undefined, instrumental: true }); }
  async function upload(files: FileList | null) {
    if (!files?.length || locked || busy || uploading) return;
    setUploading(true);
    try {
      if (files.length + value.references.length > 8) throw new Error('最多添加 8 个参考。');
      const added = [...value.references];
      for (const file of Array.from(files)) {
        if (file.size > capabilities.uploads.max_bytes) throw new Error(`${file.name} 超过 64 MiB。`);
        const form = new FormData(); form.append('file', file); form.append('rights_confirmed', String(rights));
        const asset = await api.request<{ id: string; name: string }>('/v1/assets', form);
        if (!added.some(r => r.asset_id === asset.id)) added.push({ asset_id: asset.id });
        setNames(old => ({ ...old, [asset.id]: asset.name }));
        patch({ references: [...added] });
      }
    } catch (e) { onError(e); } finally { setUploading(false); if (fileInput.current) fileInput.current.value = ''; }
  }
  function addUrl() {
    const clean = url.trim();
    if (!/^https:\/\/suno\.com\/(song|playlist)\/[0-9a-fA-F-]{36}$/.test(clean)) return onError(new Error('请输入 Suno 歌曲或歌单的完整 URL。'));
    if (value.references.length >= 8 || value.references.some(r => r.url === clean)) return onError(new Error('参考已存在或数量已达上限。'));
    patch({ references: [...value.references, { url: clean }] }); setUrl('');
  }
  return <section className="card composer"><div className="section-head"><div><span className="eyebrow">CREATE</span><h2>创作声音</h2></div><span className="pill">本机工作台</span></div>
    <fieldset disabled={locked || busy || uploading}>
      <div className="modes" role="group" aria-label="创作模式">{(['simple', 'advanced', 'sounds'] as Mode[]).map(m => <button key={m} type="button" aria-pressed={value.mode === m} className={value.mode === m ? 'selected' : ''} onClick={() => mode(m)}>{({ simple: '灵感 · Simple', advanced: '自定义 · Advanced', sounds: '音效 · Sounds' })[m]}</button>)}</div>
      <p className="muted">{value.mode === 'advanced' ? '分开控制风格与歌词，适合精确的配乐需求。' : value.mode === 'simple' ? '用一句话描述想法，也可以加入音频、图片或视频参考。' : '制作单次音效或循环环境声，按需设置时长和节奏。'}</p>
      <label className="field"><span>{value.mode === 'advanced' ? '音乐风格' : value.mode === 'sounds' ? '声音描述' : '你的创作想法'}</span><textarea aria-label={value.mode === 'advanced' ? '音乐风格' : value.mode === 'sounds' ? '声音描述' : '你的创作想法'} rows={4} maxLength={2000} value={value.prompt} onChange={e => patch({ prompt: e.target.value })} placeholder="黄昏的森林，温暖钢琴与轻柔弦乐，克制而充满希望。不要人声。"/><small className="counter">{value.prompt.length} / 2000</small></label>
      <div className="two-col"><label className="field"><span>作品标题 <em>可选</em></span><input aria-label="作品标题" value={value.title ?? ''} maxLength={80} onChange={e => patch({ title: e.target.value || undefined })} placeholder="例如：森林的来信"/></label><label className="field"><span>下载格式</span><select aria-label="下载格式" value={value.format} onChange={e => patch({ format: e.target.value as 'mp3' | 'wav' })}><option value="mp3">MP3</option><option value="wav">WAV</option></select></label></div>
      {value.mode !== 'sounds' && <label className="check"><input type="checkbox" checked={value.instrumental} onChange={e => { const options = { ...value.options }; if (e.target.checked) { delete options.voice_name; delete options.vocal_gender; if (!value.references.length) delete options.audio_influence; } patch({ instrumental: e.target.checked, lyrics: undefined, options }); }}/><span>纯音乐 <small>不加入人声</small></span></label>}
      {value.mode === 'advanced' && !value.instrumental && <label className="field"><span>歌词 <em>必填</em></span><textarea rows={5} maxLength={5000} value={value.lyrics ?? ''} onChange={e => patch({ lyrics: e.target.value })} placeholder="[Verse]\n在这里填写歌词…"/></label>}
      {value.mode !== 'sounds' && <div className="references"><div className="label-row"><strong>参考素材</strong><span>{value.references.length} / 8</span></div>
        <label className="check"><input type="checkbox" checked={rights} onChange={e => setRights(e.target.checked)}/><span>我有权使用接下来上传的素材</span></label>
        <button type="button" className="dropzone" onClick={() => fileInput.current?.click()} onDragOver={e => e.preventDefault()} onDrop={e => { e.preventDefault(); void upload(e.dataTransfer.files); }}>＋ {uploading ? '正在保存参考…' : '选择或拖入参考文件'}<small>{value.mode === 'advanced' ? '音频' : '音频 · 图片 · 视频'} · 每个最多 64 MiB · 先保存在本机</small></button>
        <input ref={fileInput} type="file" className="hidden-input" aria-label="参考文件" multiple accept={value.mode === 'advanced' ? '.wav,.mp3,.flac,.m4a,.ogg' : capabilities.uploads.extensions.join(',')} onChange={e => void upload(e.target.files)}/>
        <div className="inline"><input aria-label="Suno 参考链接" value={url} onChange={e => setUrl(e.target.value)} placeholder="粘贴 Suno 歌曲 / 歌单链接"/><button type="button" className="secondary" onClick={addUrl}>添加</button></div>
        <ul className="ref-list">{value.references.map((ref, i) => <li key={ref.asset_id ?? ref.url}><span>{ref.asset_id ? names[ref.asset_id] ?? `已上传 · ${ref.asset_id.slice(0, 12)}` : ref.url}</span><button type="button" aria-label={`移除参考 ${i + 1}`} onClick={() => { const refs = value.references.filter((_, n) => n !== i); const options = { ...value.options }; if (!refs.length && !options.voice_name) delete options.audio_influence; patch({ references: refs, options }); }}>×</button></li>)}</ul>
      </div>}
      <details className="details"><summary>更多选项 <span>{Object.keys(value.options).length || '按需设置'}</span></summary><p className="muted">留空沿用网页设置；显式值会在生成前核对。账号和模型可能不提供某些控件。</p><Options value={value} capabilities={capabilities} onChange={setValue}/></details>
      <details className="details"><summary>制作归属与请求预览</summary><label className="field"><span>请求日志归属目录 <em>可选</em></span><input value={value.target ?? ''} onChange={e => patch({ target: e.target.value || undefined })} placeholder="ai_videos/剧目录/episodes/ep01"/><small>使用已有剧 / 集 / 资产目录；独立创作留空。</small></label><pre>{JSON.stringify(value, null, 2)}</pre></details>
    </fieldset>
    {plan && <div className="plan-result" role="status"><strong>预检通过</strong><p>参数与本机参考检查通过，尚未生成。网页可用性仍在执行时核验。</p>{value.options.max_mode && <p>Max Mode 可能增加积分消耗。</p>}</div>}
    {locked && <p className="notice">上次提交尚未获得明确回执，原请求已保留。重试使用同一个任务键，避免重复扣费。</p>}
    <div className="actions"><button className="secondary" onClick={onPlan} disabled={busy || uploading || locked || !value.prompt.trim()}>预检 · 不收费</button><button className="primary" onClick={onCreate} disabled={busy || uploading || (!locked && (capabilities.automation_paused || !value.prompt.trim()))}>{busy ? '正在处理…' : locked ? '重试同一请求' : '生成音乐 ↗'}</button></div>
    <p className="fine">生成将使用 Suno 账号积分及下载额度。预检、查看任务和取回本机成品不收费。</p>
  </section>;
}
