/**
 * 人物卡的「样片与正片」（follow-up 286）：人物详情页顶部，一处看完这个人物的全部技能视频。
 * 正片＝人物视频＋每个技能最新的正式条（Q W E R）；样片＝每个技能全部草稿（新的在前）与峰值图；
 * 剪辑拼接＝接进了这个人物素材的成片，正片剪辑在前、草稿剪辑在后。只读；没有技能视频的人物不显示。
 */
import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { mediaUrl } from "../api";
import { hasSkillVideos, loadCharacterReel, type CharacterReel, type ReelClip, type ReelCut, type SkillReel } from "../lib/characterReel";
import { CUT_STAGE_LABEL, type CutStage } from "../lib/sceneCuts";

// 人物页先看正片剪辑，草稿剪辑在后（follow-up 287）；剪辑模块页仍按 CUT_STAGES 的草稿 → 正片
const REEL_CUT_ORDER: CutStage[] = ["final", "draft"];
import { useFileChanges } from "../lib/fileEvents";
import { useDemoStatus, type DemoStatus } from "../lib/demoStatus";
import { DemoFinalBadge } from "./DemoFinalBadge";

type Tab = "finals" | "drafts" | "cuts";

const when = (stamp: string): string => stamp.replace("T", " ").slice(0, 16);
const seconds = (value: number | null): string => value === null ? "" : `${value.toFixed(1)} 秒`;
const fileHref = (path: string): string => `/file/${encodeURIComponent(path)}`;

/** 一条可播放的视频；generation.json 没写时长就用播放器读到的。 */
function ReelVideo({ video, label, duration }: { video: string; label: string; duration: number | null }): JSX.Element {
  const [probed, setProbed] = useState<number | null>(null);
  const length = duration ?? probed;
  return <>
    <video src={mediaUrl(video)} controls preload="metadata" playsInline aria-label={label} className="character-reel-video"
      onLoadedMetadata={event => { const d = event.currentTarget.duration; if (Number.isFinite(d)) setProbed(d); }} />
    {length !== null && <span className="character-reel-meta">{seconds(length)}</span>}
  </>;
}

function clipMeta(clip: ReelClip): string {
  return [when(clip.generated_at), clip.submit_id, clip.credits !== null ? `${clip.credits} 积分` : "", clip.resolution]
    .filter(Boolean).join(" · ");
}

function SkillHead({ skill }: { skill: SkillReel }): JSX.Element {
  return <span className="character-reel-skill">
    {skill.icon ? <img src={mediaUrl(skill.icon)} alt={`${skill.key} 图标`} className="character-reel-icon" /> : <span className="character-reel-icon none" aria-hidden="true" />}
    <strong>{skill.title}</strong> <code>{skill.key}</code>
  </span>;
}

function Finals({ reel }: { reel: CharacterReel }): JSX.Element {
  return <ul className="character-reel-grid" aria-label="正片">
    <li className="character-reel-card">
      <span className="character-reel-skill"><strong>人物视频</strong></span>
      {reel.turntable ? <ReelVideo video={reel.turntable.video} label="人物视频" duration={reel.turntable.duration} />
        : <p className="character-reel-empty">还没有 {reel.name}_turntable.mp4</p>}
    </li>
    {reel.skills.map(skill => <li key={skill.key} className="character-reel-card">
      <SkillHead skill={skill} />
      {skill.final ? <>
        <ReelVideo video={skill.final.video} label={`${skill.key} 正片`} duration={skill.final.duration} />
        <span className="character-reel-meta">{clipMeta(skill.final)}{skill.finals.length > 1 ? ` · 共 ${skill.finals.length} 条正式条，这是最新的` : ""}</span>
      </> : <p className="character-reel-empty">还没有正式条</p>}
    </li>)}
  </ul>;
}

function Drafts({ reel }: { reel: CharacterReel }): JSX.Element {
  return <>{reel.skills.map(skill => <section key={skill.key} className="character-reel-group" aria-label={`${skill.key} 样片`}>
    <h4><SkillHead skill={skill} /> <span className="character-reel-meta">{skill.drafts.length} 条草稿</span></h4>
    <ul className="character-reel-grid">
      {skill.peak && <li className="character-reel-card">
        <span className="character-reel-meta">峰值图</span>
        <Link to={fileHref(skill.peak)}><img src={mediaUrl(skill.peak)} alt={`${skill.key} 峰值图`} className="character-reel-peak" loading="lazy" /></Link>
      </li>}
      {skill.drafts.map(draft => <li key={draft.id} className="character-reel-card">
        <ReelVideo video={draft.video} label={`${skill.key} 草稿 ${draft.id}`} duration={draft.duration} />
        <span className="character-reel-meta">{clipMeta(draft)}</span>
      </li>)}
      {skill.drafts.length === 0 && <li className="character-reel-empty">还没有草稿</li>}
    </ul>
  </section>)}</>;
}

function Cut({ cut, demo }: { cut: ReelCut; demo?: DemoStatus }): JSX.Element {
  const isFinal = Boolean(demo && cut.own && cut.path === demo.cut);
  return <li className={isFinal ? "character-reel-card wide demo-final" : "character-reel-card wide"}>
    <span className="character-reel-skill"><strong>{cut.own ? "人物 demo" : cut.episode} · v{cut.version}</strong>
      <span className="character-reel-meta">{[cut.phase, cut.status, seconds(cut.duration)].filter(Boolean).join(" · ")}</span>
      {isFinal && <DemoFinalBadge status={demo} long />}
      <Link to={fileHref(cut.path)}>剪辑决定</Link></span>
    {cut.error && <p role="alert" className="character-reel-empty">{cut.error}</p>}
    {cut.video ? <ReelVideo video={cut.video} label={`${CUT_STAGE_LABEL[cut.stage]} v${cut.version}`} duration={null} />
      : !cut.error && <p className="character-reel-empty">还没渲染</p>}
    {cut.note && <p className="character-reel-note">{cut.note}</p>}
  </li>;
}

function Cuts({ reel, demo }: { reel: CharacterReel; demo?: DemoStatus }): JSX.Element {
  return <>{REEL_CUT_ORDER.map(stage => <section key={stage} className="character-reel-group" aria-label={CUT_STAGE_LABEL[stage]}>
    <h4>{CUT_STAGE_LABEL[stage]}（{reel.cuts[stage].length}）</h4>
    {reel.cuts[stage].length ? <ul className="character-reel-grid">{reel.cuts[stage].map(cut => <Cut key={cut.path} cut={cut} demo={demo} />)}</ul>
      : <p className="character-reel-empty">还没有{CUT_STAGE_LABEL[stage]}</p>}
  </section>)}</>;
}

export function CharacterReelPanel({ dir }: { dir: string }): JSX.Element | null {
  const [reel, setReel] = useState<CharacterReel | null>(null);
  const [tab, setTab] = useState<Tab>("finals");
  const demo = useDemoStatus().get(dir);
  const load = useCallback(() => {
    let cancelled = false;
    void loadCharacterReel(dir).then(data => { if (!cancelled) setReel(data); }).catch(() => { if (!cancelled) setReel(null); });
    return () => { cancelled = true; };
  }, [dir]);
  useEffect(() => { setReel(null); return load(); }, [load]);
  useFileChanges(dir, () => { load(); });
  useFileChanges(reel?.watch[1] ?? null, () => { load(); });
  if (!reel || reel.path !== dir || !hasSkillVideos(reel)) return null;
  const finals = reel.skills.filter(skill => skill.final).length + (reel.turntable ? 1 : 0);
  const drafts = reel.skills.reduce((n, skill) => n + skill.drafts.length, 0);
  const cuts = reel.cuts.draft.length + reel.cuts.final.length;
  const tabs: [Tab, string][] = [["finals", `正片（${finals}）`], ["drafts", `样片（${drafts}）`], ["cuts", `剪辑拼接（${cuts}）`]];
  return <section className="character-reel" aria-label="样片与正片">
    <h3>样片与正片<DemoFinalBadge status={demo} long /></h3>
    <div role="tablist" aria-label="样片与正片" className="character-reel-tabs">
      {tabs.map(([id, label]) => <button key={id} type="button" role="tab" aria-selected={tab === id} onClick={() => setTab(id)}>{label}</button>)}
    </div>
    {tab === "finals" && <Finals reel={reel} />}
    {tab === "drafts" && <Drafts reel={reel} />}
    {tab === "cuts" && <Cuts reel={reel} demo={demo} />}
  </section>;
}
