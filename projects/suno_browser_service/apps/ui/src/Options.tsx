import type { Capabilities, Generation, SchemaField } from './types';

const labels: Record<string, string> = { model: '模型', exclude_styles: '排除风格', vocal_gender: '人声性别', weirdness: '探索程度 · Weirdness', style_influence: '风格影响', audio_influence: '参考音频影响', variety: '变化程度 · Variety', duration_seconds: '时长（秒）', max_mode: 'Max Mode', my_taste: 'My Taste', voice_name: '已有 Voice / Persona', inspiration_name: '灵感歌单', sound_type: '声音类型', bpm: '速度 · BPM' };
const choices: Record<string, string> = { male: '男性', female: '女性', one_shot: '单次 · One Shot', loop: '循环 · Loop' };

export function Options({ value, capabilities, onChange }: { value: Generation; capabilities: Capabilities; onChange: (value: Generation) => void }) {
  const fields = capabilities.request_schema.$defs.GenerationOptions.properties;
  const entries = Object.entries(fields).filter(([name]) => value.mode === 'sounds' ? ['sound_type', 'bpm'].includes(name) : !['sound_type', 'bpm'].includes(name));
  function set(name: string, val: string | boolean | number | undefined) {
    const options = { ...value.options };
    if (val === undefined) delete options[name]; else options[name] = val;
    onChange({ ...value, options });
  }
  return <div className="option-grid">{entries.map(([name, field]) => {
    const schema: SchemaField = field.anyOf?.find(f => f.type !== 'null') ?? field;
    const disabled = (value.instrumental && ['voice_name', 'vocal_gender'].includes(name)) || (name === 'audio_influence' && !value.references.length && !value.options.voice_name);
    const current = value.options[name];
    return <label className="option" key={name}><span>{labels[name] ?? name}</span>
      {schema.enum || schema.type === 'boolean' ? <select disabled={disabled} value={current === undefined ? '' : String(current)} onChange={e => set(name, e.target.value === '' ? undefined : schema.type === 'boolean' ? e.target.value === 'true' : e.target.value)}>
        <option value="">沿用页面设置</option>{schema.type === 'boolean' ? <><option value="true">开启</option><option value="false">关闭</option></> : schema.enum?.map(v => <option key={v} value={v}>{choices[v] ?? v}</option>)}
      </select> : <input disabled={disabled} type={['integer', 'number'].includes(schema.type ?? '') ? 'number' : 'text'} min={schema.minimum} max={schema.maximum} step={schema.type === 'integer' ? 1 : 'any'} maxLength={schema.maxLength} value={current === undefined ? '' : String(current)} placeholder="沿用页面设置" onChange={e => set(name, e.target.value === '' ? undefined : ['integer', 'number'].includes(schema.type ?? '') ? Number(e.target.value) : e.target.value)} />}
      <small>{field.description}</small></label>;
  })}</div>;
}
