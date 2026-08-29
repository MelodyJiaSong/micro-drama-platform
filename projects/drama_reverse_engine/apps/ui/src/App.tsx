import { useCallback, useEffect, useState } from "react";
import { api, DramaNode, EpisodeStatus } from "./api";
import { ArtifactView } from "./views/ArtifactView";
import { CreateDrama } from "./views/CreateDrama";
import { DramaDetail } from "./views/DramaDetail";
import { EpisodeDetail } from "./views/EpisodeDetail";

type Route =
  | { view: "home" }
  | { view: "create" }
  | { view: "drama"; dramaId: string }
  | { view: "episode"; dramaId: string; ep: string }
  | { view: "artifact"; dramaId: string; ep: string; rel: string };

const DECLARATION_KEY = "dre.declaration.v1";
const STAGES = ["ingest", "extract", "assets", "understand", "compose", "gate_a", "gate_b", "done"];

function UploadNewEntry(props: { onCreated: (dramaId: string) => void }) {
  const [file, setFile] = useState<File | null>(null);
  const [title, setTitle] = useState("");
  const [accepted, setAccepted] = useState(() => localStorage.getItem(DECLARATION_KEY) === "1");
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState<string | null>(null);
  const [seq, setSeq] = useState(0);

  const upload = () => {
    if (!file) return;
    setBusy(true);
    setMsg(null);
    api.uploadNewDrama(file, accepted, title)
      .then((r) => {
        setMsg(`已建立「${r.title}」，切出 ${r.episodes.length} 集`);
        setFile(null);
        setTitle("");
        setSeq((s) => s + 1);
        props.onCreated(r.drama_id);
      })
      .catch((e) => setMsg(String(e)))
      .finally(() => setBusy(false));
  };

  return (
    <div className="upload-panel" data-view="upload-new">
      <input key={seq} type="file" accept=".mp4,.mov,video/mp4,video/quicktime"
        data-testid="upload-new-input"
        onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
      <input type="text" placeholder="标题（默认取文件名）" value={title}
        onChange={(e) => setTitle(e.target.value)} />
      <label className="check">
        <input type="checkbox" checked={accepted} data-testid="upload-new-declaration"
          onChange={(e) => {
            setAccepted(e.target.checked);
            localStorage.setItem(DECLARATION_KEY, e.target.checked ? "1" : "0");
          }} />
        我声明对上传素材拥有版权或已获翻拍/改编授权（记录留存）
      </label>
      <button onClick={upload} disabled={!file || !accepted || busy}>
        {busy ? "上传中…" : "上传并新建主体"}
      </button>
      {busy && <p className="notice">上传 + 校验 + 切集处理中（大文件需几分钟），完成后主体自动出现…</p>}
      {msg && <p className="notice">{msg}</p>}
    </div>
  );
}

export function App() {
  const [dramas, setDramas] = useState<DramaNode[]>([]);
  const [route, setRoute] = useState<Route>({ view: "home" });
  const [loadError, setLoadError] = useState<string | null>(null);

  const refresh = useCallback(() => {
    api.tree().then((r) => { setDramas(r.dramas); setLoadError(null); }).catch((e) => setLoadError(String(e)));
  }, []);

  useEffect(() => {
    refresh();
    const timer = setInterval(refresh, 4000);
    return () => clearInterval(timer);
  }, [refresh]);

  const findEpisode = (dramaId: string, ep: string): EpisodeStatus | undefined =>
    dramas.find((d) => d.drama_id === dramaId)?.children.find((e) => e.episode_rel_dir === ep);

  const selectedDramaId =
    route.view === "drama" || route.view === "episode" || route.view === "artifact" ? route.dramaId : null;

  return (
    <div className="layout">
      <aside className="sidebar">
        <h1>短剧逆向引擎</h1>
        <UploadNewEntry onCreated={(dramaId) => { refresh(); setRoute({ view: "drama", dramaId }); }} />
        {loadError && <p className="error">{loadError}</p>}
        <ul className="entry-list">
          {dramas.map((d) => (
            <li key={d.drama_id}>
              <button className={d.drama_id === selectedDramaId ? "selected" : undefined}
                onClick={() => { refresh(); setRoute({ view: "drama", dramaId: d.drama_id }); }}>
                {d.children.some((e) => e.busy) && <span className="spin">⟳</span>}
                {d.title}
                {d.children.some((e) => e.failed_reason) && <span className="badge failed">失败</span>}
                {d.children.some((e) => e.gate_hold) && <span className="badge hold">待放行</span>}
              </button>
              {d.drama_id === selectedDramaId && (
                <ul className="nav-eps">
                  {d.children.map((e) => (
                    <li key={e.episode_rel_dir}>
                      <button className="nav-ep"
                        onClick={() => setRoute({ view: "episode", dramaId: d.drama_id, ep: e.episode_rel_dir })}>
                        {e.busy && <span className="spin">⟳</span>}
                        {e.episode_rel_dir.split("/").pop()}
                        <span className="badge stage">
                          {e.stage} {Math.max(1, STAGES.indexOf(e.stage) + 1)}/8
                        </span>
                        {e.failed_reason && <span className="badge failed">失败</span>}
                        {e.gate_hold && <span className="badge hold">待放行</span>}
                      </button>
                      <div className="nav-artifacts">
                        {e.artifacts.script && (
                          <button className="linklike" onClick={() =>
                            setRoute({ view: "artifact", dramaId: d.drama_id, ep: e.episode_rel_dir, rel: `${e.episode_rel_dir}/script.md` })}>
                            剧本
                          </button>
                        )}
                        {e.artifacts.dialogue && (
                          <button className="linklike" onClick={() =>
                            setRoute({ view: "artifact", dramaId: d.drama_id, ep: e.episode_rel_dir, rel: `${e.episode_rel_dir}/dialogue.md` })}>
                            台词
                          </button>
                        )}
                        {e.artifacts.novel && (
                          <button className="linklike" onClick={() =>
                            setRoute({ view: "artifact", dramaId: d.drama_id, ep: e.episode_rel_dir, rel: `${e.episode_rel_dir}/novel.md` })}>
                            小说
                          </button>
                        )}
                        {e.artifacts.prompts && (
                          <button className="linklike" onClick={() =>
                            setRoute({ view: "artifact", dramaId: d.drama_id, ep: e.episode_rel_dir, rel: `${e.episode_rel_dir}/all_shot_prompts.md` })}>
                            分镜prompt
                          </button>
                        )}
                        {e.shot_count > 0 && <span className="notice">{e.shot_count}镜</span>}
                        {!e.artifacts.script && !e.failed_reason && e.stage !== "done" && (
                          <span className="notice">生成中…</span>
                        )}
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </li>
          ))}
        </ul>
        {dramas.length === 0 && <p className="notice">还没有主体——上面选个 MP4 上传即可。</p>}
        <div className="divider" />
        <div className="toolbar">
          <button className="secondary" onClick={() => setRoute({ view: "create" })}>高级新建（闸口）</button>
        </div>
      </aside>
      <main className="main">
        {route.view === "home" && (
          <div data-view="home">
            <h2>短剧逆向引擎</h2>
            <p className="notice">左侧上传一个 MP4 即会建立一个主体（entry）：视频归档到主体目录，
              逆向出的小说 / 剧本 / 分镜 prompt 全部绑定该主体。点击左侧主体查看进度与产物。</p>
          </div>
        )}
        {route.view === "create" && <CreateDrama onCreated={(dramaId) => { refresh(); setRoute({ view: "drama", dramaId }); }} />}
        {route.view === "drama" && (() => {
          const drama = dramas.find((d) => d.drama_id === route.dramaId);
          return drama ? (
            <DramaDetail drama={drama} onRefresh={refresh}
              onOpenEpisode={(ep) => setRoute({ view: "episode", dramaId: route.dramaId, ep })} />
          ) : <p className="notice">主体不存在或已删除，请刷新。</p>;
        })()}
        {route.view === "episode" && (() => {
          const episode = findEpisode(route.dramaId, route.ep);
          return episode ? (
            <EpisodeDetail dramaId={route.dramaId} episode={episode} onRefresh={refresh}
              onOpenArtifact={(rel) => setRoute({ view: "artifact", dramaId: route.dramaId, ep: route.ep, rel })} />
          ) : <p className="notice">集不存在，请刷新。</p>;
        })()}
        {route.view === "artifact" && (
          <ArtifactView relPath={route.rel} episodeRelDir={route.ep}
            onBack={() => setRoute({ view: "episode", dramaId: route.dramaId, ep: route.ep })} />
        )}
      </main>
    </div>
  );
}
