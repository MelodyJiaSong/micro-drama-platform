import { useEffect, useRef, useState, type RefObject } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { mediaUrl } from "../api";
import { CUT_STAGES, CUT_STAGE_LABEL, EPISODE_CUT, cutClock, loadSceneCuts, type CutStage, type CutVersion, type EpisodeCuts,
  type EpisodeJoin, type Gallery } from "../lib/sceneCuts";

const STAGE_NOTE: Record<CutStage, string> = {
  draft: "用各镜 480p 草稿条剪，看结构、节奏和缺哪些镜头；只用来改上游，不进锁片。",
  final: "用各镜 720p 正式条剪（草稿在界面标「通过」后才出正式条），一路剪到锁片。",
};
const EMPTY: Record<CutStage, string> = {
  draft: "还没有草稿剪辑。",
  final: "还没有正片剪辑：等各镜草稿标了「通过」、出了 720p 正式条再剪。",
};

/** 一版剪辑：成片（干净版 / 标注版）、时间线（点起点跳到那一段）、备注与有意违例。 */
function CutVersionView({ cut }: { cut: CutVersion }): JSX.Element {
  const [labeled, setLabeled] = useState(false);
  const player = useRef<HTMLVideoElement>(null);
  const video = labeled && cut.labeled_video ? cut.labeled_video : cut.video;
  const seek = (start: number): void => {
    if (!player.current) return;
    player.current.currentTime = start + 0.01;
    void player.current.play?.();
  };
  return <article className="edit-cut" aria-label={`${CUT_STAGE_LABEL[cut.stage]} v${cut.version}`}>
    <p className="workflow-pack-path">
      v{cut.version}{cut.phase && ` · ${cut.phase}`}{cut.status && ` · ${cut.status}`}{cut.approved_by && `（${cut.approved_by} 批准）`}
      {" · "}{cut.duration.toFixed(1)} 秒 · {cut.shots} 段{cut.placeholders ? `，缺镜占位 ${cut.placeholders}` : ""}
      {cut.rendered_at && ` · 渲染于 ${cut.rendered_at}`}{cut.base_version != null && ` · 基于 v${cut.base_version}`}
      {" · "}<Link to={`/file/${encodeURIComponent(cut.path)}`}>剪辑决定</Link>
    </p>
    {cut.error && <p role="alert" className="workflow-error">{cut.error}</p>}
    {video ? <>
      <div className="edit-player-toggle" role="group" aria-label="版本">
        <button type="button" aria-pressed={!labeled} onClick={() => setLabeled(false)}>干净版</button>
        <button type="button" aria-pressed={labeled} disabled={!cut.labeled_video} onClick={() => setLabeled(true)}>标注版（镜号 · 条 · 入出点）</button>
      </div>
      <video ref={player} key={video} src={mediaUrl(video)} controls preload="metadata" className="workflow-take-video" aria-label="剪辑成片" />
    </> : !cut.error && <p className="workflow-note">还没渲染：运行 <code>python tools/scene_cut.py render {cut.path}</code>。</p>}
    {cut.events.length > 0 && <table className="edit-timeline" aria-label="时间线">
      <thead><tr><th>起点</th><th>镜头</th><th>条</th><th>入–出</th><th>时长</th><th>理由与备注</th></tr></thead>
      <tbody>{cut.events.map((event, index) => <tr key={`${event.shot}-${index}`} className={event.placeholder ? "edit-placeholder" : undefined}>
        <td>{video ? <button type="button" onClick={() => seek(event.start)}>{cutClock(event.start)}</button> : cutClock(event.start)}</td>
        <td>{event.shot}</td>
        <td>{event.placeholder ? "缺镜占位" : <code>{event.take.slice(-8)}</code>}</td>
        <td>{event.placeholder ? "—" : `${event.cut_in?.toFixed(2)}–${event.cut_out?.toFixed(2)}`}
          {event.audio_in != null && <><br /><span className="edit-audio">声 {event.audio_in.toFixed(2)}–{event.audio_out?.toFixed(2)}</span></>}</td>
        <td>{event.duration.toFixed(1)}s</td>
        <td>{event.reason}{event.notes.length > 0 && <ul>{event.notes.map(note => <li key={note}>{note}</li>)}</ul>}
          {event.placeholder && event.text.length > 0 && <ul>{event.text.map(line => <li key={line}>{line}</li>)}</ul>}</td>
      </tr>)}</tbody>
    </table>}
    {cut.notes.length > 0 && <section aria-label="备注"><h4>备注</h4><ul>{cut.notes.map(note => <li key={note}>{note}</li>)}</ul></section>}
    {cut.violations.length > 0 && <section aria-label="有意违例"><h4>有意违例（{cut.violations.length}）</h4>
      <ul>{cut.violations.map((v, index) => <li key={index}><strong>{v.shot}</strong>：{v.what}{v.why && <span className="workflow-pack-path"> —— {v.why}</span>}</li>)}</ul></section>}
  </article>;
}

/** 播放器 + 跳转：点时间就从那里放。 */
function useSeek(): [RefObject<HTMLVideoElement>, (start: number) => void] {
  const player = useRef<HTMLVideoElement>(null);
  return [player, (start: number): void => {
    if (!player.current) return;
    player.current.currentTime = start + 0.01;
    void player.current.play?.();
  }];
}

/** 一版集级剪辑（follow-up 278）：整集成片、各场位置、转场与理由、独立审稿结论。 */
function EpisodeJoinView({ cut, sceneHref }: { cut: EpisodeJoin; sceneHref: (scene: string, version: number) => string }): JSX.Element {
  const [player, seek] = useSeek();
  const at = (start: number): JSX.Element => cut.video ? <button type="button" onClick={() => seek(start)}>{cutClock(start)}</button> : <>{cutClock(start)}</>;
  return <article className="edit-cut" aria-label={`整集 v${cut.version}`}>
    <p className="workflow-pack-path">
      v{cut.version}{cut.phase && ` · ${cut.phase}`}{cut.status && ` · ${cut.status}`}{cut.approved_by && `（${cut.approved_by} 批准）`}
      {" · "}{cut.duration.toFixed(1)} 秒 · {cut.segments.length} 场 · 片头{cut.head} · 片尾{cut.tail}
      {cut.rendered_at && ` · 渲染于 ${cut.rendered_at}`}{cut.base_version != null && ` · 基于 v${cut.base_version}`}
      {" · "}<Link to={`/file/${encodeURIComponent(cut.path)}`}>剪辑决定</Link>
    </p>
    {cut.error && <p role="alert" className="workflow-error">{cut.error}</p>}
    {cut.note && <p className="workflow-note">{cut.note}</p>}
    {cut.video ? <video ref={player} key={cut.video} src={mediaUrl(cut.video)} controls preload="metadata" className="workflow-take-video" aria-label="整集成片" />
      : !cut.error && <p className="workflow-note">还没渲染：运行 <code>python tools/episode_cut.py join {cut.path}</code>。</p>}
    <section aria-label="独立审稿">
      <h4>独立审稿</h4>
      {cut.review_stale ? <p className="workflow-error">审稿结论审的是另一版成片，这一版还没审。</p>
        : cut.review_verdict ? <><p><strong>{cut.review_verdict}</strong>（结论绑定这一版成片的 sha256）</p>
          {cut.review_items.length > 0 && <ul>{cut.review_items.map(item => <li key={item}>{item}</li>)}</ul>}</>
        : <p className="workflow-note">还没有独立审稿。</p>}
    </section>
    <table className="edit-timeline" aria-label="各场与转场">
      <thead><tr><th>起点</th><th>内容</th><th>时长</th><th>说明</th></tr></thead>
      <tbody>{cut.segments.map((segment, index) => {
        const tr = index ? cut.transitions[index - 1] : undefined;
        return [tr && <tr key={`t${index}`} className="edit-transition">
          <td>{at(Math.max(0, tr.at - 1.5))}</td>
          <td>转场 · <strong>{tr.name}</strong> <code>{tr.type}</code></td>
          <td>{tr.duration ? `${tr.duration.toFixed(1)}s 重叠` : "—"}</td>
          <td>{tr.reason}{tr.audio_j != null && <><br /><span className="edit-audio">J：下一场声音提前 {tr.audio_j.toFixed(2)} 秒</span></>}
            {tr.audio_l != null && <><br /><span className="edit-audio">L：上一场声音拖后 {tr.audio_l.toFixed(2)} 秒</span></>}
            <br /><span className="workflow-pack-path">点起点从转场前 1.5 秒开始放</span></td>
        </tr>,
        <tr key={`s${index}`}>
          <td>{at(segment.start)}</td>
          <td><Link to={sceneHref(segment.scene, segment.cut_version)}>{segment.scene}</Link> · 场剪辑 v{segment.cut_version}</td>
          <td>{segment.duration.toFixed(1)}s</td><td />
        </tr>];
      })}</tbody>
    </table>
    {cut.changes.length > 0 && <section aria-label="相对上一版的改动"><h4>相对上一版的改动</h4><ul>{cut.changes.map(item => <li key={item}>{item}</li>)}</ul></section>}
  </article>;
}

/** 转场样片：两场交界处每种转场各一段，点名字跳到那一段。 */
function GalleryView({ gallery }: { gallery: Gallery }): JSX.Element {
  const [player, seek] = useSeek();
  return <article className="edit-cut" aria-label={`转场样片 ${gallery.from_scene}→${gallery.to_scene}`}>
    <h4>转场样片：{gallery.from_scene} → {gallery.to_scene}</h4>
    <p className="workflow-note">同一个交界用每种转场各出一段（画面下方写着名字），挑中了告诉 Claude Code / Codex 写进集级剪辑决定。</p>
    <video ref={player} key={gallery.video} src={mediaUrl(gallery.video)} controls preload="metadata" className="workflow-take-video" aria-label="转场样片" />
    <ol className="edit-gallery-index">{gallery.entries.map(entry => <li key={entry.start}>
      <button type="button" onClick={() => seek(entry.start)}>{cutClock(entry.start)}</button> {entry.label}</li>)}</ol>
  </article>;
}

/** 剪辑模块（follow-up 269）：一集各场的草稿剪辑 / 正片剪辑，选场次、选版本，看成片与时间线。只读。 */
export function EditStagePanel({ episodePath, refresh }: { episodePath: string; refresh: number }): JSX.Element {
  const [params] = useSearchParams();
  const stage: CutStage = params.get("cut") === "final" ? "final" : "draft";
  const scene = params.get("scene");
  const [cuts, setCuts] = useState<EpisodeCuts | null>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    let cancelled = false;
    setError("");
    void loadSceneCuts(episodePath).then(data => { if (!cancelled) setCuts(data); }).catch(err => { if (!cancelled) setError(String(err)); });
    return () => { cancelled = true; };
  }, [episodePath, refresh]);
  const href = (changes: Record<string, string | null>): string => {
    const next = new URLSearchParams(params);
    for (const [key, value] of Object.entries(changes)) { if (value === null) next.delete(key); else next.set(key, value); }
    return `?${next.toString()}`;
  };
  const current = cuts?.episode_path === episodePath ? cuts : null;
  const selected = current?.scenes.find(item => item.scene === scene);
  const versions = selected?.[stage] || [];
  const wanted = Number(params.get("v"));
  const cut = versions.find(item => item.version === wanted) || versions[0];
  const joinedVersions = current?.joined?.[stage] || [];
  const join = joinedVersions.find(item => item.version === wanted) || joinedVersions[0];
  const count = (id: CutStage): number => current?.scenes.filter(item => item[id].length).length || 0;
  return <section className="workflow-content" aria-label="剪辑">
    <div className="workflow-content-heading"><h2>剪辑</h2><span className="workflow-status draft">试行</span><p>选条、粗剪、精剪到锁片。草稿剪辑与正片剪辑分开。</p></div>
    <nav className="workflow-scene-tabs" role="tablist" aria-label="剪辑阶段">
      {CUT_STAGES.map(id => <Link key={id} role="tab" aria-selected={stage === id} to={href({ cut: id === "draft" ? null : id, v: null })}>
        {CUT_STAGE_LABEL[id]}{current ? `（${count(id)} 场）` : ""}</Link>)}
    </nav>
    <p className="workflow-note">{STAGE_NOTE[stage]}</p>
    {error && <p role="alert" className="workflow-error">{error}</p>}
    {!current && !error && <p role="status">加载中…</p>}
    {current && !scene && <ol className="edit-scene-list" aria-label="场次">
      {(current.joined?.[stage]?.length || current.galleries?.[stage]?.length) ? <li key={EPISODE_CUT}>
        <Link to={href({ scene: EPISODE_CUT, v: null })}>整集 · 场与场接起来、转场</Link>
        <span>{current.joined[stage][0] ? ` v${current.joined[stage][0].version} · ${current.joined[stage][0].phase} · ${current.joined[stage][0].duration.toFixed(1)} 秒`
          : ""}{current.galleries[stage].length ? ` · 转场样片 ${current.galleries[stage].length} 条` : ""}</span></li> : null}
      {current.scenes.map(item => {
        const latest = item[stage][0];
        return <li key={item.scene}><Link to={href({ scene: item.scene, v: null })}>{item.scene} · {item.label}</Link>
          <span>{latest ? ` v${latest.version} · ${latest.phase} · ${latest.duration.toFixed(1)} 秒${latest.placeholders ? ` · 缺镜 ${latest.placeholders}` : ""}${latest.video ? "" : " · 未渲染"}`
            : ` · ${stage === "draft" ? "还没有草稿剪辑" : "还没有正片剪辑"}`}</span></li>;
      })}
    </ol>}
    {current && scene === EPISODE_CUT && <>
      <nav className="workflow-shot-nav" aria-label="场次导航"><Link to={href({ scene: null, v: null })}>← 全部场次</Link><span /><span /></nav>
      <h3>整集 · 场与场接起来、转场</h3>
      {joinedVersions.length > 1 && <div className="edit-player-toggle" role="group" aria-label="整集版本">
        {joinedVersions.map(item => <Link key={item.version} to={href({ v: String(item.version) })} aria-current={item === join ? "true" : undefined}>v{item.version}</Link>)}
      </div>}
      {join ? <EpisodeJoinView key={join.path} cut={join} sceneHref={(id, version) => href({ scene: id, v: String(version) })} /> : <p className="workflow-note">还没有整集剪辑。</p>}
      {(current.galleries?.[stage] || []).map(gallery => <GalleryView key={gallery.video} gallery={gallery} />)}
    </>}
    {current && scene && scene !== EPISODE_CUT && !selected && <p role="alert">找不到场次 {scene}，请从导航重新选择。</p>}
    {selected && <>
      <nav className="workflow-shot-nav" aria-label="场次导航"><Link to={href({ scene: null, v: null })}>← 全部场次</Link><span /><span /></nav>
      <h3>{selected.scene} · {selected.label}</h3>
      {versions.length > 1 && <div className="edit-player-toggle" role="group" aria-label="剪辑版本">
        {versions.map(item => <Link key={item.version} to={href({ v: String(item.version) })} aria-current={item === cut ? "true" : undefined}>v{item.version}</Link>)}
      </div>}
      {cut ? <CutVersionView key={cut.path} cut={cut} /> : <p className="workflow-note">{EMPTY[stage]}</p>}
    </>}
  </section>;
}
