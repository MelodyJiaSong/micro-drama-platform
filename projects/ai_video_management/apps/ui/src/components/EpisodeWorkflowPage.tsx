import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { loadWorkflow, type EpisodeWorkflow, type ModuleId, type FilmingScene, type PromptScene } from "../lib/episodeWorkflow";
import "./EpisodeWorkflowPage.css";

const STATUS = { empty: "待开始", draft: "草稿", approved: "已确定", stale: "待更新", blocked: "等待上游" };
const PURPOSE = { story: "先把故事写好。", filming: "把已确定的故事设计成可拍的镜头。", prompts: "按固定规则编译已确定的分镜。" };

export function EpisodeWorkflowPage({ dramaPath, title }: { dramaPath: string; title: string }): JSX.Element {
  const [params] = useSearchParams();
  const episode = /^ep\d+$/.test(params.get("episode") || "") ? params.get("episode")! : "ep01";
  const path = `${dramaPath}/episodes/${episode}`;
  const active: ModuleId = params.get("module") === "filming" ? "filming" : params.get("module") === "prompts" ? "prompts" : "story";
  const selectedScene = params.get("scene");
  const selectedShot = params.get("shot");
  const [workflow, setWorkflow] = useState<EpisodeWorkflow | null>(null);
  const [refresh, setRefresh] = useState(0);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  useEffect(() => {
    let cancelled = false;
    setWorkflow(null); setError(""); setMessage("");
    void loadWorkflow(path).then(data => {
      if (!cancelled) setWorkflow(data);
    }).catch(err => { if (!cancelled) setError(String(err)); });
    return () => { cancelled = true; };
  }, [path, refresh]);
  const current = workflow?.episode_path === path ? workflow : null;
  const module = current?.modules.find(m => m.id === active);
  const filmingScenes = (module?.content.scenes || []) as FilmingScene[];
  const promptScenes = (module?.content.scenes || []) as PromptScene[];
  const scenes = (module?.content.scenes || []).filter(scene => !selectedScene || scene.id === selectedScene);
  const missingSelection = Boolean(selectedScene && !scenes.length) || Boolean(selectedShot && !scenes.some(scene => scene.shots.some(shot =>
    active === "filming" ? current?.shot_keys[scene.id]?.[shot.id] === selectedShot : shot.id === selectedShot)));
  const copy = (text: string): void => {
    void navigator.clipboard.writeText(text).then(() => setMessage("已复制")).catch(() => setError("复制失败，请手动选择文本"));
  };
  return <div className="episode-workflow">
    <header><div><p className="workflow-eyebrow">创作工作台 · EP{Number(episode.slice(2))}</p><h1>{title}</h1></div>
      <button type="button" onClick={() => setRefresh(value => value + 1)}>刷新</button></header>
    <p className="workflow-note">只读展示。通过 Claude Code / Codex 修改文件后刷新。</p>
    {error && <p role="alert" className="workflow-error">{error}</p>}
    {message && <p role="status" className="workflow-message">{message}</p>}
    {!current && !error && <p role="status">加载中…</p>}
    {module && <section className="workflow-content" aria-label={module.label}>
      <div className="workflow-content-heading"><h2>{module.label}</h2><span className={`workflow-status ${module.status}`}>{STATUS[module.status]}</span><p>{PURPOSE[active]}</p></div>
      {active !== "story" && <details className="workflow-source"><summary>查看上游内容</summary>
        {active === "filming" ? <p className="workflow-prose">{current?.modules[0].content.text || "故事尚未开始。"}</p>
          : <div>{(current?.modules[1].content.scenes as FilmingScene[] || []).map(scene => <section key={scene.id}><h3>{scene.id} · {scene.location} · {scene.time}</h3>
            <p>{scene.purpose}</p>{scene.shots.map(shot => <p key={shot.id}>{current?.shot_keys[scene.id]?.[shot.id]} · {shot.duration}秒<br />{shot.action}<br />{shot.camera}<br />{shot.dialogue || "无对白"}</p>)}</section>)}</div>}
      </details>}
      {module.status === "stale" && <p className="workflow-note">上游版本已改变，请通过 Claude Code / Codex 核对并更新。</p>}
      {module.status === "blocked" && <p className="workflow-note">等待上游版本确定。</p>}
      {missingSelection && <p role="alert">找不到指定场次或镜头，请从导航重新选择。</p>}
      {active === "story" && <div className="workflow-story">
        <p className="workflow-note">产出 · 当前故事工作区。草稿尚未确定；每次候选和过程保存在各自 run 中。</p>
        <Link to={`/story-runs?episode_path=${encodeURIComponent(path)}`}>查看创作记录</Link>
        <h3>故事方向</h3><p className="workflow-prose">{module.content.brief || "尚未填写。"}</p>
        <h3>故事正文</h3><p className="workflow-prose" aria-label="故事正文">{module.content.text || "尚未生成。"}</p>
        {module.content.text && <button type="button" onClick={() => copy(module.content.text!)}>复制正文</button>}
      </div>}
      {active === "filming" && <div className="workflow-prompts">
        {filmingScenes.filter(scene => !selectedScene || scene.id === selectedScene).map(scene => <section key={scene.id} aria-label={`场次 ${scene.id}`}>
          <h3>{scene.id} · {scene.location} · {scene.time}</h3><p>环境资产：{scene.background || "未绑定"}</p><p>本场目标与变化：{scene.purpose}</p>
          {scene.shots.filter(shot => !selectedShot || current?.shot_keys[scene.id]?.[shot.id] === selectedShot).map(shot => <article key={shot.id}>
            <h4>{current?.shot_keys[scene.id]?.[shot.id]} · {shot.duration}秒</h4>
            <dl><dt>行动</dt><dd>{shot.action}</dd><dt>拍摄</dt><dd>{shot.camera}</dd><dt>对白</dt><dd>{shot.dialogue || "无对白"}</dd></dl></article>)}
        </section>)}
        {!module.content.scenes?.length && <p>尚无分镜。</p>}
      </div>}
      {active === "prompts" && <div className="workflow-prompts">
        {promptScenes.filter(scene => !selectedScene || scene.id === selectedScene).map(scene => <section key={scene.id} aria-label={`场次 ${scene.id}`}>
          <h3>{scene.id} · 场次</h3>{scene.shots.filter(shot => !selectedShot || shot.id === selectedShot).map(shot => <article key={shot.id}>
            <div className="workflow-shot-heading"><h4>{shot.id}</h4><button type="button" onClick={() => copy(shot.text)}>复制</button></div><pre>{shot.text}</pre>
          </article>)}
        </section>)}
        {!module.content.scenes?.length && <p>尚无编译结果。</p>}
      </div>}
    </section>}
  </div>;
}
