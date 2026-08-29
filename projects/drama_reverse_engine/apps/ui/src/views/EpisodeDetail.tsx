import { useEffect, useState } from "react";
import { api, EpisodeStatus } from "../api";

const STAGES = ["ingest", "extract", "assets", "understand", "compose", "gate_a", "gate_b", "done"];

const EXPORTABLES: Array<[keyof EpisodeStatus["artifacts"], string]> = [
  ["novel", "小说"],
  ["script", "剧本"],
  ["dialogue", "台词"],
  ["prompts", "分镜prompt"],
];

export function EpisodeDetail(props: {
  dramaId: string;
  episode: EpisodeStatus;
  onRefresh: () => void;
  onOpenArtifact: (rel: string) => void;
}) {
  const { dramaId, episode } = props;
  const [shotFiles, setShotFiles] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [exportSel, setExportSel] = useState<Record<string, boolean>>({ novel: true, script: true, dialogue: true, prompts: true });
  const [exportFmt, setExportFmt] = useState<"md" | "docx">("docx");

  const exportKeys = EXPORTABLES.filter(([k]) => exportSel[k] && episode.artifacts[k]).map(([k]) => k);
  const exportUrl = `/api/episodes/export-artifacts?episode_rel_dir=${encodeURIComponent(episode.episode_rel_dir)}` +
    `&artifacts=${exportKeys.join(",")}&format=${exportFmt}`;

  useEffect(() => {
    api.shotFiles(episode.episode_rel_dir).then((r) => setShotFiles(r.shot_files)).catch(() => setShotFiles([]));
  }, [episode.episode_rel_dir]);

  const act = (fn: () => Promise<unknown>) => () =>
    fn().then(props.onRefresh).catch((e) => setError(String(e)));

  return (
    <div data-view="episode">
      <h2>{episode.episode_rel_dir}</h2>
      <p>
        {STAGES.map((s) => (
          <span key={s} className="badge stage"
            style={s === episode.stage ? { background: "#1456d6", color: "#fff" } : undefined}>
            {s}
          </span>
        ))}
      </p>
      {episode.failed_reason && <p className="error">失败：{episode.failed_reason}</p>}
      {episode.degradations.length > 0 && <p className="notice">降级：{episode.degradations.join("、")}</p>}
      <div className="toolbar">
        <button onClick={act(() => api.step(dramaId, episode.episode_rel_dir))}>走一步</button>
        <button onClick={act(() => api.run(dramaId, episode.episode_rel_dir))}>自动跑完</button>
        {episode.gate_hold && (
          <button onClick={act(() => api.releaseGate(dramaId, episode.episode_rel_dir))}>放行闸口</button>
        )}
        <button className="secondary" onClick={act(() => api.rerunStage(dramaId, episode.episode_rel_dir, "compose"))}>
          重跑 compose
        </button>
        <button className="secondary" onClick={act(() => api.rerunStage(dramaId, episode.episode_rel_dir, "understand"))}>
          重跑 understand
        </button>
      </div>
      <div className="toolbar">
        <button className="secondary" onClick={() => props.onOpenArtifact(`${episode.episode_rel_dir}/script.md`)}>
          剧本
        </button>
        <button className="secondary" onClick={() => props.onOpenArtifact(`${episode.episode_rel_dir}/dialogue.md`)}>
          台词
        </button>
        <button className="secondary" onClick={() => props.onOpenArtifact(`${episode.episode_rel_dir}/novel.md`)}>
          小说
        </button>
        <button className="secondary"
          onClick={() => props.onOpenArtifact(`${episode.episode_rel_dir}/all_shot_prompts.md`)}>
          全镜 prompt
        </button>
      </div>
      <div className="export-panel" data-view="export">
        <span className="export-title">一键导出：</span>
        {EXPORTABLES.map(([key, label]) => (
          <label key={key} className={episode.artifacts[key] ? "check" : "check disabled"}>
            <input type="checkbox" disabled={!episode.artifacts[key]}
              checked={Boolean(exportSel[key]) && episode.artifacts[key]}
              onChange={(e) => setExportSel({ ...exportSel, [key]: e.target.checked })} />
            {label}
          </label>
        ))}
        <label className="check">
          <input type="radio" name="export-fmt" checked={exportFmt === "docx"} onChange={() => setExportFmt("docx")} />
          docx
        </label>
        <label className="check">
          <input type="radio" name="export-fmt" checked={exportFmt === "md"} onChange={() => setExportFmt("md")} />
          md
        </label>
        {exportKeys.length > 0 ? (
          <a href={exportUrl} download><button>导出{exportKeys.length > 1 ? "（zip）" : ""}</button></a>
        ) : (
          <button disabled>导出</button>
        )}
      </div>
      {shotFiles.length > 0 && (
        <>
          <h3>分镜（{shotFiles.length}）</h3>
          <ul className="episode-list">
            {shotFiles.map((f) => (
              <li key={f}>
                <button className="linklike" onClick={() => props.onOpenArtifact(f)}>{f.split("/").pop()}</button>
              </li>
            ))}
          </ul>
        </>
      )}
      {error && <p className="error">{error}</p>}
    </div>
  );
}
