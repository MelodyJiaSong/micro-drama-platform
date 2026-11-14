import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { fetchProcessQc, fetchProcessQcDrama } from "../api";
import {
  PROCESS_QC_REPO_PATH, dramaRegistry, escapeInstruction, percent, processQcDramaUrl, promoteInstruction,
  reviewRepoInstruction, type ProcessQcDrama, type ProcessQcRepo,
} from "../lib/processQc";
import { REVIEW_STRATEGY_PATH } from "../lib/reviewStrategy";
import { CheckList, CopyButton, HealthLine, LevelBanner, LevelBadge, Pipeline } from "./ProcessQcParts";
import "./ProcessQcPage.css";

const LOOP = [
  ["记缺陷", "你每次退回或纠正，代理用 qc.py defect 记一条：哪个产物、哪个环节、谁发现的。"],
  ["问为什么没抓到", "没这条检查 → 新增；有但太松 → 收紧；有但没跑 → 改成闸门；审稿看错 → 改清单。"],
  ["攒回归样本", "改检查必须抓得到历史缺陷、又不误伤你已通过的成品。"],
  ["看指标", "逃逸率 = 你发现的 ÷ 全部缺陷，目标趋近 0。"],
  ["晋升与淘汰", "新检查先放剧级；两部以上的剧反复出现再提议升仓库级（须你同意）；长期零命中的复审。"],
];

function useLoad<T>(load: () => Promise<T>, key: string): { data: T | null; error: string } {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<string>("");
  useEffect(() => {
    let live = true;
    setData(null); setError("");
    load().then(d => { if (live) setData(d); }).catch(e => { if (live) setError(String(e)); });
    return () => { live = false; };
  }, [key]); // eslint-disable-line react-hooks/exhaustive-deps
  return { data, error };
}

export function ProcessQcRepoPage(): JSX.Element {
  const { data, error } = useLoad<ProcessQcRepo>(fetchProcessQc, "repo");
  return <div className="process-qc">
    <h1>自检与进化 <LevelBadge level="仓库级" /></h1>
    <LevelBanner level="仓库级" />
    <p className="qc-notice">审查机制的全貌（六道关、按法则分工的独立审稿人、结论分类、漏网案例）见 <Link to={REVIEW_STRATEGY_PATH}>审查机制与审查单</Link>。</p>
    {error ? <p role="alert">读取失败：{error}</p> : !data ? <p role="status">加载中…</p> : <>
      <h2>流程环节</h2><Pipeline checks={data.checks} stages={data.stages} />
      <h2>仓库级检查 <span className="qc-count">{data.checks.length}</span></h2>
      <CheckList checks={data.checks} stages={data.stages} action={c => <CopyButton text={reviewRepoInstruction(c)} label="复制：复核这条" />} />
      <h2>各剧体检</h2>
      <table className="qc-table"><thead><tr><th>剧</th><th>自检闸门</th><th>剧级检查</th><th>缺陷（你抓到 / 全部）</th><th>误报</th><th>逃逸率</th><th>出片结论</th><th>日志</th></tr></thead>
        <tbody>{data.dramas.filter(d => d.enabled || d.defects || d.followup.followups).map(d => <tr key={d.drama}>
          <td><Link to={processQcDramaUrl(d.drama)}>{d.drama.replace("ai_videos/", "")}</Link></td>
          <td>{d.enabled ? "已启用" : <span className="qc-muted">未启用</span>}</td>
          <td>{d.drama_checks}</td><td>{d.user_caught} / {d.defects}</td><td>{d.false_positives}</td>
          <td className={d.escape_rate && d.escape_rate > 0.5 ? "qc-bad" : ""}>{percent(d.escape_rate)}</td>
          <td>{d.renders_total}</td><td><HealthLine f={d.followup} /></td>
        </tr>)}</tbody></table>
      <p className="qc-muted">只列启用了自检、或近 7 天有记录的剧。点剧名进入该剧的剧级页面。</p>
      <h2>怎么进化</h2>
      <ol className="qc-loop">{LOOP.map(([t, d]) => <li key={t}><strong>{t}</strong>：{d}</li>)}</ol>
    </>}
  </div>;
}

export function ProcessQcDramaPage(): JSX.Element {
  const [params] = useSearchParams();
  const drama = params.get("drama") ?? "";
  const { data, error } = useLoad<ProcessQcDrama>(() => fetchProcessQcDrama(drama), drama);
  const name = drama.replace("ai_videos/", "");
  return <div className="process-qc">
    <p><Link to={PROCESS_QC_REPO_PATH}>← 自检与进化（仓库级）</Link> · <Link to={`/drama?drama=${encodeURIComponent(drama)}`}>回到剧页</Link></p>
    <h1>{name} · 流程与自检 <LevelBadge level="剧级" /></h1>
    <LevelBanner level="剧级" />
    <p className="qc-muted">全流程怎么审：<Link to={REVIEW_STRATEGY_PATH}>审查机制与审查单</Link></p>
    {error ? <p role="alert">读取失败：{error}</p> : !data ? <p role="status">加载中…</p> : <>
      {!data.enabled ? <p className="qc-notice">本剧还没有剧级登记表，没启用自检闸门。
        <CopyButton text={`为 ${drama} 建剧级自检登记表 ${dramaRegistry(drama)}：从本剧近期用户的纠正意见里整理检查（带 follow-up 来源），只放剧级，不改仓库级；用 followup.py 记录。`} label="复制：为本剧启用" /></p> : null}
      <div className="qc-stats">
        <div><strong>{percent(data.escape_rate)}</strong><span>逃逸率（你发现的 ÷ 全部）</span></div>
        <div><strong>{data.defects.filter(d => d.caught_by !== "override").length}</strong><span>缺陷：你 {data.defects.filter(d => d.caught_by === "user").length} · 机检 {data.defects.filter(d => d.caught_by === "machine").length} · 审稿 {data.defects.filter(d => d.caught_by === "review").length}</span></div>
        <div><strong>{data.defects.filter(d => d.caught_by === "override").length}</strong><span>误报（闸门拦了、你放行了）</span></div>
        <div><strong>{data.renders_total}</strong><span>有检查结论的出片</span></div>
        <div><HealthLine f={data.followup} /></div>
      </div>
      <h2>流程环节</h2><Pipeline checks={[...data.drama_checks, ...data.repo_checks]} stages={data.stages} />
      <h2>本剧检查 <LevelBadge level="剧级" /> <span className="qc-count">{data.drama_checks.length}</span></h2>
      <CheckList checks={data.drama_checks} stages={data.stages} action={c => <CopyButton text={promoteInstruction(drama, c)} label="复制：提议升仓库级" />} />
      <details className="qc-inherited"><summary>继承自仓库级 <LevelBadge level="仓库级" /> {data.repo_checks.length} 项（对所有剧生效，改动须你同意）</summary>
        <CheckList checks={data.repo_checks} stages={data.stages} /></details>
      <h2>逃逸分析：为什么检查没抓到</h2>
      {data.escapes.length ? <ul className="qc-escapes">{data.escapes.map((e, i) => <li key={`${e.category}-${i}`}>
        <div><code>{e.category}</code> <span className="qc-muted">{e.level} · follow-up {e.followup || "-"}</span></div>
        {e.note ? <p>{e.note}</p> : null}
        <p><strong>{e.reason}</strong> → {e.action}</p>
        <CopyButton text={escapeInstruction(drama, e)} label="复制给代理" />
      </li>)}</ul> : <p className="qc-empty">没有你抓到的缺陷。</p>}
      <h2>最近出片的检查结论</h2>
      {data.renders.length ? <table className="qc-table"><thead><tr><th>出片</th><th>结论</th></tr></thead><tbody>{data.renders.map(r => <tr key={r.path}>
        <td><Link to={`/file/${encodeURIComponent(r.path + "/qc.json")}`}>{r.path.split("/").slice(-3).join("/")}</Link></td>
        <td>{Object.entries(r.verdicts).map(([k, v]) => <span key={k} className={`qc-v qc-v-${v === "pass" ? "pass" : v === "fail" ? "fail" : "none"}`}>{k} {v === "pass" ? "✓" : v === "fail" ? "✗" : "未审"}</span>)}</td>
      </tr>)}</tbody></table> : <p className="qc-empty">还没有记过检查结论的出片（qc.json）。规则从今天起只管新出片。</p>}
    </>}
  </div>;
}
