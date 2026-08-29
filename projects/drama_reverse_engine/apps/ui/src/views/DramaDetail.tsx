import { useState } from "react";
import { api, DramaNode } from "../api";

function AppendUpload(props: { dramaId: string; onUploaded: () => void }) {
  const [file, setFile] = useState<File | null>(null);
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState<string | null>(null);
  const [seq, setSeq] = useState(0);

  const upload = () => {
    if (!file) return;
    setBusy(true);
    setMsg(null);
    api.uploadSource(props.dramaId, file)
      .then((r) => {
        setMsg(`已上传，切出 ${r.episodes.length} 集：${r.episodes.join("、")}`);
        setFile(null);
        setSeq((s) => s + 1);
        props.onUploaded();
      })
      .catch((e) => setMsg(String(e)))
      .finally(() => setBusy(false));
  };

  return (
    <div className="toolbar">
      <input key={seq} type="file" accept=".mp4,.mov,video/mp4,video/quicktime"
        data-testid={`upload-input-${props.dramaId}`}
        onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
      <button onClick={upload} disabled={!file || busy}>{busy ? "上传中…" : "追加上传（续集）"}</button>
      {msg && <span className="notice">{msg}</span>}
    </div>
  );
}

export function DramaDetail(props: {
  drama: DramaNode;
  onRefresh: () => void;
  onOpenEpisode: (ep: string) => void;
}) {
  const d = props.drama;
  return (
    <div data-view="drama">
      <h2>
        {d.title} <span className="badge stage">{d.drama_id}</span>
        {d.gate_a_enabled && <span className="badge hold">闸口A</span>}
        {d.gate_b_enabled && <span className="badge hold">闸口B</span>}
      </h2>
      {d.children.length === 0 && <p className="notice">尚无集——下方追加上传，或等待上传切集完成。</p>}
      <ul className="episode-list">
        {d.children.map((e) => (
          <li key={e.episode_rel_dir}>
            <button className="linklike" onClick={() => props.onOpenEpisode(e.episode_rel_dir)}>
              {e.episode_rel_dir}
            </button>
            <span className="badge stage">{e.stage}</span>
            {e.gate_hold && <span className="badge hold">待放行</span>}
            {e.failed_reason && <span className="badge failed">失败</span>}
            {e.degradations.length > 0 && <span className="badge red">降级{e.degradations.length}</span>}
          </li>
        ))}
      </ul>
      <AppendUpload dramaId={d.drama_id} onUploaded={props.onRefresh} />
    </div>
  );
}
