import { useState } from "react";
import { api } from "../api";

export function CreateDrama(props: { onCreated: (dramaId: string) => void }) {
  const [dramaId, setDramaId] = useState("");
  const [title, setTitle] = useState("");
  const [accepted, setAccepted] = useState(false);
  const [gateA, setGateA] = useState(false);
  const [gateB, setGateB] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const submit = () =>
    api.createDrama({
      drama_id: dramaId, title, declaration_accepted: accepted,
      declared_by: "operator", gate_a_enabled: gateA, gate_b_enabled: gateB,
    })
      .then(() => { setMessage("已创建"); props.onCreated(dramaId); })
      .catch((e) => setMessage(String(e)));

  return (
    <div className="form-card" data-view="create">
      <h2>高级新建（手动配置闸口）</h2>
      <label>项目 ID（英文 slug）</label>
      <input type="text" value={dramaId} onChange={(e) => setDramaId(e.target.value)} />
      <label>中文标题</label>
      <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} />
      <label>
        <input type="checkbox" checked={gateA} onChange={(e) => setGateA(e.target.checked)} /> 启用闸口A（剧本确认）
      </label>
      <label>
        <input type="checkbox" checked={gateB} onChange={(e) => setGateB(e.target.checked)} /> 启用闸口B（prompt 确认）
      </label>
      <label>
        <input type="checkbox" checked={accepted} onChange={(e) => setAccepted(e.target.checked)} data-testid="declaration" />
        我声明对上传素材拥有版权或已获翻拍/改编授权（必选，记录留存）
      </label>
      <div className="toolbar">
        <button onClick={submit} disabled={!dramaId || !title}>创建</button>
      </div>
      {message && <p className="notice">{message}</p>}
      <p className="notice">日常流程用左侧「上传并新建主体」即可；此表单仅在需要预设闸口 A/B 时使用，创建后在主体页「追加上传」提交 MP4。</p>
    </div>
  );
}
