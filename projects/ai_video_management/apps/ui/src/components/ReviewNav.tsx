/** 左侧导航「审查单」一类（follow-up 333）：剧 → 集 → 范围（场一 · 出片前）→ 每张审查单，新的在前。
 *
 * 同一范围里最新的一张标「最新」，其余变灰、悬停看「已被 <最新那张> 取代」（用户 2026-11-08：看不出哪个是最新的）。
 *
 * 数据来自 `/api/review-runs`（只读摘要）；点剧或集打开该范围的审查单列表，点一张单打开审查单页。 */
import { useEffect, useMemo, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { fetchReviewRuns, type ReviewRunSummary } from "../api";
import { reviewCorrectionsHref } from "../lib/reviewCorrections";
import { REVIEW_RUN_ROUTE, displayState, navGroups, navLabel, reviewRunHref } from "../lib/reviewRun";
import "./ReviewRunPage.css";

// 「已收轮」是中性的绿点（每轮审查不等用户 review，用户 2026-11-08）；旧单的「待用户确认」按「已收轮」显示。
const STATE_DOT: Record<string, string> = {
  进行中: "rn-dot-run", 已完成: "rn-dot-ok", 已作废: "rn-dot-void", 已收轮: "rn-dot-ok", 用户已确认出片: "rn-dot-go",
};
// 导航宽度有限：常态（已完成 / 已收轮）只用绿点表示、状态字放悬停提示，把位置留给开单时间；进行中、作废、已确认出片照样写出来。
const QUIET_STATES = new Set(["已完成", "已收轮"]);
const indent = (depth: number): { paddingLeft: string } => ({ paddingLeft: `${8 + depth * 14}px` });

export function ReviewNav(): JSX.Element | null {
  const navigate = useNavigate();
  const location = useLocation();
  const [runs, setRuns] = useState<ReviewRunSummary[] | null>(null);
  const [closed, setClosed] = useState<Record<string, boolean>>({});
  const onReviewPage = location.pathname.startsWith(REVIEW_RUN_ROUTE);

  useEffect(() => {
    let live = true;
    fetchReviewRuns().then(r => { if (live) setRuns(Array.isArray(r?.runs) ? r.runs : []); }).catch(() => { if (live) setRuns([]); });
    return () => { live = false; };
    // 打开审查页时重读一次：新出的审查单、新打的勾马上出现在导航里。
  }, [onReviewPage]);

  const groups = useMemo(() => navGroups(runs ?? []), [runs]);
  if (!runs || runs.length === 0) return null;

  const active = new URLSearchParams(location.search).get("path") ?? "";
  const isOpen = (key: string): boolean => closed[key] !== true;
  const toggle = (key: string): void => setClosed(c => ({ ...c, [key]: !c[key] }));

  const row = (key: string, depth: number, label: JSX.Element | string, href: string,
    opts: { branch?: boolean; dot?: string; count?: string; fix?: { href: string; ready: boolean }; latest?: boolean; old?: boolean; tip?: string; noSelect?: boolean } = {}): JSX.Element => {
    const selected = !opts.noSelect && onReviewPage && active === new URLSearchParams(href.split("?")[1]).get("path");
    return (
      <div key={key} role="treeitem" tabIndex={-1} aria-level={depth + 1} aria-selected={selected}
        aria-expanded={opts.branch ? isOpen(key) : undefined}
        className={["tree-item", opts.branch ? "tree-branch" : "tree-leaf", selected ? "tree-active" : "", opts.old ? "rn-old" : ""].filter(Boolean).join(" ")}
        style={indent(depth)} title={opts.tip} onClick={() => navigate(href)}>
        {opts.branch ? <button type="button" className="tree-disclosure" aria-label={isOpen(key) ? "Collapse" : "Expand"}
          onClick={e => { e.stopPropagation(); toggle(key); }}>{isOpen(key) ? "▾" : "▸"}</button>
          : <span className="tree-disclosure" aria-hidden="true" />}
        {opts.dot ? <i className={`rn-dot ${opts.dot}`} aria-hidden="true" /> : null}
        <span className="tree-label">{label}</span>
        {opts.latest ? <span className="rn-latest">最新</span> : null}
        {opts.fix ? <button type="button" className="rn-fix" title={opts.fix.ready ? "这一轮的修复页" : "修复页（还没生成修复记录）"}
          style={opts.fix.ready ? undefined : { opacity: 0.55 }} onClick={e => { e.stopPropagation(); navigate(opts.fix!.href); }}>修复</button> : null}
        {opts.count ? <small className="rn-count">{opts.count}</small> : null}
      </div>
    );
  };

  const rootKey = "review-nav";
  const all = groups.flatMap(g => g.episodes.flatMap(e => e.runs)).length;
  return (
    <div role="tree" aria-label="审查单" className="tree review-nav">
      <div role="treeitem" tabIndex={-1} aria-level={1} aria-expanded={isOpen(rootKey)} className="tree-item tree-branch rn-root"
        style={indent(0)} onClick={() => toggle(rootKey)}>
        <button type="button" className="tree-disclosure" aria-label={isOpen(rootKey) ? "Collapse" : "Expand"}
          onClick={e => { e.stopPropagation(); toggle(rootKey); }}>{isOpen(rootKey) ? "▾" : "▸"}</button>
        <span className="tree-label">☑ 审查单</span><small className="rn-count">{all}</small>
      </div>
      {isOpen(rootKey) ? groups.map(g => {
        const dk = `rn:${g.drama}`;
        return <div key={dk} role="group">
          {row(dk, 1, g.name, reviewRunHref(g.drama), { branch: true, count: String(g.episodes.reduce((n, e) => n + e.runs.length, 0)) })}
          {isOpen(dk) ? g.episodes.map(e => {
            const ek = `${dk}/${e.episode}`;
            return <div key={ek} role="group">
              {row(ek, 2, e.episode, reviewRunHref(`${g.drama}/episodes/${e.episode}`), { branch: true, count: String(e.runs.length) })}
              {isOpen(ek) ? e.scopes.map(s => {
                const sk = `${ek}/${s.key}`;
                // 范围行点开的是这一范围最新的一张
                return <div key={sk} role="group">
                  {row(sk, 3, `${s.label} · ${s.stage}`, reviewRunHref(s.latest.dir), { branch: true, count: String(s.runs.length), tip: `最新：${s.latest.title}`, noSelect: true })}
                  {isOpen(sk) ? s.runs.map(({ run: r, latest, supersededBy }) => row(r.dir, 4, navLabel(r), reviewRunHref(r.dir),
                    { dot: STATE_DOT[displayState(r.state)] ?? "", count: QUIET_STATES.has(displayState(r.state)) ? undefined : displayState(r.state), latest, old: !latest,
                      tip: [r.title, displayState(r.state), supersededBy ? `已被「${supersededBy.title}」取代` : "本范围最新"].join(" · "),
                      fix: { href: reviewCorrectionsHref(r.dir), ready: Boolean(r.corrections) } })) : null}
                </div>;
              }) : null}
            </div>;
          }) : null}
        </div>;
      }) : null}
    </div>
  );
}
