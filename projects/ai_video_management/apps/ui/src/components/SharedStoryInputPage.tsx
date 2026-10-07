import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { loadStoryInput, type SharedStoryInput } from "../lib/storyRuns";
import { Frame, Notes, Sources, Evidence, Markdown, format } from "./StoryRunDisplay";
import "./StoryRunsPage.css";

export function SharedStoryInputPage(): JSX.Element {
  const [params, setParams] = useSearchParams();
  const episode = params.get("episode_path") || "";
  const profile = params.get("profile_id") || "";
  const rulesView = params.get("view") === "rules";
  const [data, setData] = useState<SharedStoryInput | null>(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [refresh, setRefresh] = useState(0);
  const shown = data?.episode_path === episode && (!profile || data.profile_id === profile) ? data : null;
  useEffect(() => {
    const controller = new AbortController();
    setData(null); setError("");
    if (!episode) return () => controller.abort();
    setBusy(true);
    void loadStoryInput(episode, profile, controller.signal).then(value => {
      if (controller.signal.aborted) return;
      if (value.episode_path !== episode || (profile && value.profile_id !== profile)) throw new Error("共享输入归属或版本不匹配");
      setData(value);
    }).catch(err => {
      if (!controller.signal.aborted) setError(`读取共享输入失败：${err instanceof Error ? err.message : String(err)}`);
    }).finally(() => { if (!controller.signal.aborted) setBusy(false); });
    return () => controller.abort();
  }, [episode, profile, refresh]);
  const changeProfile = (id: string): void => {
    setData(null);
    const next = new URLSearchParams(params); next.set("profile_id", id); setParams(next);
  };
  const currentProfile = shown?.profiles.find(item => item.id === shown.profile_id);
  return <div className="story-runs-page shared-story-input">
    <header className="story-runs-header"><div><p className="story-run-eyebrow">{episode.split("/").at(-1)?.toUpperCase() || "故事"} · Persistent</p>
      <h1>{rulesView ? "创作规则" : "共享创作输入"}</h1><p>{rulesView ? "跨 run 复用的创作规则，正文按所选版本展示。" : "跨 run 复用的创作方向、人物与背景选用。"}每次创作会冻结所选版本。</p>
      <p className="story-run-muted">本页只读。通过 Claude Code/Codex 修改，刷新查看。切换版本仅用于查看，不改变后续运行或当前 EP1。</p></div>
      <button type="button" disabled={!episode || busy} onClick={() => setRefresh(value => value + 1)}>刷新查看</button></header>
    {!episode ? <p role="alert">请从故事目录打开共享创作输入。</p> : null}
    {error ? <p role="alert" className="story-run-error">{error}</p> : null}
    {busy ? <p role="status">读取共享输入…</p> : null}
    {shown ? <div className="story-run-content">
      <section><div className="story-run-item-heading"><h2>输入与规则版本</h2><label>查看版本 <select value={shown.profile_id} onChange={event => changeProfile(event.target.value)}>
        {shown.profiles.map(item => <option key={item.id} value={item.id}>{item.label}</option>)}</select></label></div>
        <p>{currentProfile?.label || shown.profile_id}</p>
        <p className="story-run-muted">共享配置选择：{shown.profiles.find(item => item.id === shown.selected_profile)?.label || shown.selected_profile}；实际使用哪个版本，以每个 run 的冻结输入为准。</p>
        <Evidence label="输入与规则路径、版本指纹" value={currentProfile} />
      </section>
      {!rulesView ? <><section><h2>故事方向</h2><p className="story-run-prose">{shown.input.brief || "尚未确定"}</p><Frame frame={shown.input.frame} /></section>
      <section><h2>暂定假设</h2><Notes values={shown.input.assumptions} empty="没有额外假设。" />
        <p className="story-run-muted">假设不等于已接受的长期事实；每个 run 保留自己的采用记录。</p></section>
      <section><h2>背景选用</h2>
        <Sources label="背景资料与明确选用范围" values={shown.input.sources} frozen={false} />
        <Evidence label="跨 run 隔离边界与前集状态输入" value={{ independence: shown.input.independence, prior_accepted_state: shown.input.prior_accepted_state ?? [] }} />
      </section></> : <section><h2>所选版本的规则正文</h2><p className="story-run-muted">以下是此共享版本保存的规则副本；不自动读取源文件的最新内容。两次 run 使用哪个版本，以各自冻结输入为准。</p>
        {shown.input.rules.map((value, index) => {
          const rule = value && typeof value === "object" && !Array.isArray(value) ? value as Record<string, unknown> : null;
          return <article className="story-run-source" key={index}>
            <Markdown text={rule && typeof rule.content === "string" ? rule.content : format(value)} />
            {rule ? <Evidence label="规则来源路径与冻结版本证据" value={{ path: rule.path, sha256: rule.sha256, selection: rule.selection }} /> : null}
          </article>;
        })}
        {!shown.input.rules.length ? <p>尚未选用规则。</p> : null}
        {shown.input.criteria?.length ? <><h3>检查问题</h3><Notes values={shown.input.criteria} empty="尚未记录" /></> : null}
      </section>}
      <p><Link to={`/story-input?${new URLSearchParams({ episode_path: episode, profile_id: shown.profile_id, view: rulesView ? "input" : "rules" })}`}>{rulesView ? "查看共享创作输入" : "查看创作规则"}</Link></p>
      <Link to={`/story-runs?episode_path=${encodeURIComponent(episode)}`}>查看独立创作记录与对比</Link>
    </div> : null}
  </div>;
}
