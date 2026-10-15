import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { isPlaceholderStage, loadWorkflow, type EpisodeWorkflow, type ModuleId, type FilmingScene, type PromptScene } from "../lib/episodeWorkflow";
import { Link } from "react-router-dom";
import { WORKFLOW_MODULES, workflowModulePath } from "../lib/workflowData";
import { renderHighlightedLines } from "../markdown/renderer";
import { mediaUrl } from "../api";
import type { ShotPack, ShotTake } from "../lib/episodeWorkflow";
import { Renderer } from "../markdown/renderer";
import "./EpisodeWorkflowPage.css";

const STATUS = { empty: "待开始", draft: "草稿", approved: "已确定", stale: "待更新", blocked: "等待上游" };
/** One-line preview for the scene's shot list: the picture line (画面 in compiler v4, 画面与表演 in v3). */
function promptSummary(text: string): string {
  const line = text.split("\n").find(item => /^画面(与表演)?：/.test(item)) || "";
  const body = line.replace(/^画面(与表演)?：/, "");
  return body.length > 60 ? `${body.slice(0, 60)}…` : body;
}
const PACK_STATUS = { ok: "与源文件一致", stale: "源文件有变，等待更新", invalid: "已失效", missing: "还没建" };
/** The shot's 资料包: every file the prompt references, copied and numbered in upload order (follow-up 229). */
function PackPanel({ pack }: { pack?: ShotPack }): JSX.Element {
  if (!pack) return <p className="workflow-note">还没有资料包信息。</p>;
  return <section className="workflow-pack" aria-label="资料包">
    <h4>资料包 <span className={`workflow-pack-status ${pack.status}`}>{PACK_STATUS[pack.status]}</span></h4>
    <p className="workflow-pack-path"><code>{pack.path}</code>{pack.prompt && <> · <Link to={`/file/${encodeURIComponent(pack.prompt)}`}>prompt.txt（已填上传编号）</Link></>}</p>
    {pack.status === "invalid" && <pre className="workflow-note">{pack.reason}</pre>}
    {pack.status === "missing" && <p className="workflow-note">编译后运行 <code>python tools/shot_pack.py sync</code>（Claude 每回合自动运行）。</p>}
    {pack.files.length > 0 && <ol className="workflow-pack-files">{pack.files.map(file => <li key={file.path}>
      <div className="workflow-pack-media">{file.kind === "image" ? <img src={mediaUrl(file.path)} alt={file.role} loading="lazy" />
        : file.kind === "video" ? <video src={mediaUrl(file.path)} controls preload="none" />
        : <audio src={mediaUrl(file.path)} controls preload="none" />}</div>
      <div><strong>{file.tag}</strong> <code>{file.key}</code><br />{file.role}<br />
        <Link to={`/file/${encodeURIComponent(file.path)}`}>打开副本</Link> · <Link to={`/file/${encodeURIComponent(file.src)}`}>源文件</Link></div>
    </li>)}</ol>}
  </section>;
}
/** The shot's generations (renders/), newest first: video preview, generation record and review (follow-up 230). */
function RendersPanel({ takes }: { takes?: ShotTake[] }): JSX.Element {
  return <section className="workflow-renders" aria-label="生成记录">
    <h4>生成记录（renders） <span className="workflow-pack-path">{takes?.length ? `${takes.length} 条` : "还没有生成"}</span></h4>
    {(takes || []).map(take => <article key={take.path} className="workflow-take">
      <header><strong>{take.id}</strong> <span className="workflow-take-status">{take.review_status}</span>
        {take.generation.model && <span className="workflow-pack-path"> · {take.generation.model} · {take.generation.duration_s}秒 · {take.generation.resolution} · {take.generation.credits ?? "?"} 积分 · {take.generation.downloaded_at}</span>}
      </header>
      {take.videos.map(video => <video key={video} src={mediaUrl(video)} controls preload="metadata" className="workflow-take-video" />)}
      <p className="workflow-pack-path">{take.prompt_path && <><Link to={`/file/${encodeURIComponent(take.prompt_path)}`}>提交时的 prompt</Link> · </>}
        {take.review_path && <Link to={`/file/${encodeURIComponent(take.review_path)}`}>review.md</Link>}</p>
      {take.review ? <div className="workflow-take-review"><Renderer content={take.review} currentPath={take.review_path} knownPaths={[]} /></div>
        : <p className="workflow-note">这一条还没有审核。</p>}
    </article>)}
  </section>;
}
const PURPOSE = { story: "先把故事写好。", filming: "把已确定的故事设计成可拍的镜头。", prompts: "按固定规则编译已确定的分镜，再生成各镜头的条。" };

export function EpisodeWorkflowPage({ dramaPath, title }: { dramaPath: string; title: string }): JSX.Element {
  const [params] = useSearchParams();
  const episode = /^ep\d+$/.test(params.get("episode") || "") ? params.get("episode")! : "ep01";
  const path = `${dramaPath}/episodes/${episode}`;
  const requested = params.get("module");
  const placeholder = isPlaceholderStage(requested) ? WORKFLOW_MODULES.find(entry => entry.id === requested) : undefined;
  const active: ModuleId = requested === "filming" ? "filming" : requested === "prompts" ? "prompts" : "story";
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
  // Prompt module: one page per shot (follow-up 226), reached from the navigation tree or the scene list.
  const promptOrder = promptScenes.flatMap(scene => scene.shots.map(shot => ({ scene: scene.id, shot: shot.id })));
  const selectedIndex = active === "prompts" && selectedShot ? promptOrder.findIndex(item => item.shot === selectedShot) : -1;
  const selectedPrompt = selectedIndex < 0 ? null : (() => {
    const scene = promptScenes.find(item => item.id === promptOrder[selectedIndex].scene)!;
    return { scene, shot: scene.shots.find(item => item.id === selectedShot)! };
  })();
  const promptNeighbours = { previous: selectedIndex > 0 ? promptOrder[selectedIndex - 1] : null,
    next: selectedIndex >= 0 && selectedIndex < promptOrder.length - 1 ? promptOrder[selectedIndex + 1] : null };
  const shotHref = ({ scene, shot }: { scene: string; shot?: string }): string => {
    const next = new URLSearchParams(params);
    next.set("scene", scene);
    if (shot) next.set("shot", shot); else next.delete("shot");
    return `?${next.toString()}`;
  };
  const filmingSource = (current?.modules.find(m => m.id === "filming")?.content.scenes || []) as FilmingScene[];
  const sceneLabel = (id: string): string => {
    const scene = filmingSource.find(item => item.id === id);
    return scene ? `${scene.location} · ${scene.time}` : "场次";
  };
  const copy = (text: string): void => {
    void navigator.clipboard.writeText(text).then(() => setMessage("已复制")).catch(() => setError("复制失败，请手动选择文本"));
  };
  return <div className="episode-workflow">
    <header><div><p className="workflow-eyebrow">创作工作台 · EP{Number(episode.slice(2))}</p><h1>{title}</h1></div>
      <button type="button" onClick={() => setRefresh(value => value + 1)}>刷新</button></header>
    <p className="workflow-note">只读展示。通过 Claude Code / Codex 修改文件后刷新。</p>
    {error && <p role="alert" className="workflow-error">{error}</p>}
    {message && <p role="status" className="workflow-message">{message}</p>}
    {placeholder ? <section className="workflow-content" aria-label={placeholder.title}>
      <div className="workflow-content-heading"><h2>{placeholder.title}</h2><span className="workflow-status empty">待设计</span><p>{placeholder.purpose}</p></div>
      <dl className="workflow-placeholder"><dt>输入</dt><dd>{placeholder.input}</dd><dt>输出</dt><dd>{placeholder.output}</dd></dl>
      <p className="workflow-note">这个模块还没有设计，本集暂无内容。模块定位见 <Link to={workflowModulePath(placeholder.id)}>工作流 · {placeholder.title}</Link>。</p>
    </section> : <>
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
        <h3>故事方向</h3><p className="workflow-prose">{module.content.brief || "尚未填写。"}</p>
        <h3>故事正文</h3><p className="workflow-prose" aria-label="故事正文">{module.content.text || "尚未生成。"}</p>
        {module.content.text && <button type="button" onClick={() => copy(module.content.text!)}>复制正文</button>}
      </div>}
      {active === "filming" && <div className="workflow-prompts">
        {filmingScenes.filter(scene => !selectedScene || scene.id === selectedScene).map(scene => <section key={scene.id} aria-label={`场次 ${scene.id}`}>
          <h3>{scene.id} · {scene.location} · {scene.time}</h3><p>环境资产：{scene.background || "未绑定"}</p><p>本场目标与变化：{scene.purpose}</p>
          {scene.shots.filter(shot => !selectedShot || current?.shot_keys[scene.id]?.[shot.id] === selectedShot).map(shot => <article key={shot.id}>
            <h4>{current?.shot_keys[scene.id]?.[shot.id]} · {shot.duration}秒</h4>
            <dl><dt>出场人物</dt><dd>{shot.cast?.length ? shot.cast.join("、") : "无"}</dd>{shot.props?.length ? <><dt>道具</dt><dd>{shot.props.join("、")}</dd></> : null}<dt>行动</dt><dd>{shot.action}</dd>
              <dt>走位</dt><dd>{shot.blocking || "—"}</dd><dt>动作分拍</dt><dd>{shot.beats || "—"}</dd><dt>拍摄</dt><dd>{shot.camera}</dd>
              <dt>光线</dt><dd>{shot.lighting || "—"}</dd><dt>对白</dt><dd>{shot.dialogue || "无对白"}</dd></dl></article>)}
        </section>)}
        {!module.content.scenes?.length && <p>尚无分镜。</p>}
      </div>}
      {active === "prompts" && <div className="workflow-prompts">
        {selectedPrompt ? <article className="workflow-shot-page" aria-label={`镜头 ${selectedPrompt.shot.id}`}>
          <nav className="workflow-shot-nav" aria-label="相邻镜头">
            {promptNeighbours.previous ? <Link to={shotHref(promptNeighbours.previous)}>← {promptNeighbours.previous.shot}</Link> : <span />}
            <Link to={shotHref({ scene: selectedPrompt.scene.id })}>{selectedPrompt.scene.id} · {sceneLabel(selectedPrompt.scene.id)}</Link>
            {promptNeighbours.next ? <Link to={shotHref(promptNeighbours.next)}>{promptNeighbours.next.shot} →</Link> : <span />}
          </nav>
          <div className="workflow-shot-heading"><h3>{selectedPrompt.shot.id}</h3>
            <button type="button" onClick={() => copy(selectedPrompt.shot.text)}>复制 prompt</button></div>
          <p className="workflow-note">{selectedPrompt.shot.text.length} 字 · 第一行是镜头编号，下载的文件靠它归位。</p>
          <div className="markdown-view"><div className="code-block-wrapper"><pre aria-label="视频 prompt"><code>{renderHighlightedLines(selectedPrompt.shot.text)}</code></pre></div></div>
          <RendersPanel takes={current?.renders?.[selectedPrompt.shot.id]} />
          {selectedPrompt.shot.refs?.length ? <PackPanel pack={current?.packs?.[selectedPrompt.shot.id]} />
            : <p className="workflow-note">这条 prompt 由旧版编译器生成，没有参考资料；重新编译后列出。</p>}
        </article> : promptScenes.filter(scene => !selectedScene || scene.id === selectedScene).map(scene => <section key={scene.id} aria-label={`场次 ${scene.id}`}>
          <h3>{scene.id} · {sceneLabel(scene.id)}</h3>
          <ol className="workflow-shot-list">{scene.shots.map(shot => <li key={shot.id}>
            <Link to={shotHref({ scene: scene.id, shot: shot.id })}>{shot.id}</Link>
            <span>{promptSummary(shot.text)}{current?.renders?.[shot.id]?.length ? ` · 已生成 ${current.renders[shot.id].length} 条` : ""}</span>
          </li>)}</ol>
        </section>)}
        {!module.content.scenes?.length && <p>尚无编译结果。</p>}
      </div>}
    </section>}
    </>}
  </div>;
}
