/** 开发稿可视化（框架 v0.4）：每页一张图，字少。表格 → Mermaid 关系图 / 阶梯 / 资料库概念图卡片。 */
import { useEffect, useState } from "react";
import {
  STAGES, abilityChart, conflictChart, counterChart, humanize, libIds, peopleChart, secretsByStage, worldChart, type DevModel,
} from "../lib/devDiagrams";

export type LibIndex = Map<string, { name: string; image: string | null }>;

type MermaidApi = { initialize: (c: Record<string, unknown>) => void; render: (id: string, src: string) => Promise<{ svg: string }> };
let mermaidReady: Promise<MermaidApi> | null = null;
let seq = 0;
function loadMermaid(): Promise<MermaidApi> {
  if (!mermaidReady) {
    mermaidReady = import("mermaid").then(mod => {
      const m = mod.default as unknown as MermaidApi;
      m.initialize({ startOnLoad: false, securityLevel: "strict", theme: "base", fontFamily: "inherit",
        themeVariables: { primaryColor: "#edf5f1", primaryBorderColor: "#6c9a8b", primaryTextColor: "#273c3b", lineColor: "#5b746d", fontSize: "15px",
          // 象限图：base 主题推导出的点颜色是 hsl(…NaN%)，这里全部写死；颜色与人物卡的外在（橙）/ 内在（紫）一致
          quadrant1Fill: "#e2f3e9", quadrant2Fill: "#efe9f7", quadrant3Fill: "#f3f5f4", quadrant4Fill: "#fbefdf",
          quadrant1TextFill: "#275d42", quadrant2TextFill: "#5b3f8c", quadrant3TextFill: "#64736d", quadrant4TextFill: "#9a5b13",
          quadrantPointFill: "#2b7a66", quadrantPointTextFill: "#273c3b", quadrantXAxisTextFill: "#4b625b", quadrantYAxisTextFill: "#4b625b",
          quadrantInternalBorderStrokeFill: "#c8d8d1", quadrantExternalBorderStrokeFill: "#c8d8d1", quadrantTitleFill: "#273c3b" },
        flowchart: { curve: "basis", padding: 12 } });
      return m;
    });
  }
  return mermaidReady;
}

/** mermaid.render 不可重入：同时画几张图会互相覆盖，所以排队一张一张画。 */
let renderQueue: Promise<unknown> = Promise.resolve();
function renderChart(chart: string): Promise<string> {
  seq += 1;
  const id = `dev-mermaid-${seq}`;
  const job = renderQueue.then(() => loadMermaid()).then(m => m.render(id, chart)).then(r => r.svg);
  renderQueue = job.catch(() => undefined);
  return job;
}

export function Mermaid({ chart, label }: { chart: string; label: string }): JSX.Element {
  const [svg, setSvg] = useState<string | null>(null);
  const [failed, setFailed] = useState(false);
  useEffect(() => {
    let alive = true;
    setFailed(false);
    renderChart(chart).then(s => { if (alive) { if (s) setSvg(s); else setFailed(true); } }).catch(() => { if (alive) setFailed(true); });
    return () => { alive = false; };
  }, [chart]);
  if (failed) return <pre className="dev-diagram-fallback" aria-label={label}>{chart}</pre>;
  return svg ? <figure className="dev-diagram" role="img" aria-label={label} dangerouslySetInnerHTML={{ __html: svg }} />
    : <div className="dev-diagram dev-muted" aria-label={label}>正在画图…</div>;
}

function Empty({ what }: { what: string }): JSX.Element {
  return <p className="dev-muted dev-empty">（{what}还没填）</p>;
}

function LibThumb({ text, title, lib }: { text: string; title: string; lib: LibIndex }): JSX.Element {
  const hit = libIds(text).map(id => ({ id, ...lib.get(id) })).find(x => x.name);
  const [broken, setBroken] = useState(false);
  if (hit?.image && !broken) return <img className="dev-thumb" src={hit.image} alt={`${hit.id} ${hit.name}`} loading="lazy" onError={() => setBroken(true)} />;
  return <div className="dev-thumb dev-thumb-blank" aria-hidden="true">{title.slice(0, 1)}</div>;
}

function LibTag({ text, lib }: { text: string; lib: LibIndex }): JSX.Element {
  const ids = libIds(text);
  if (!ids.length) return <span className="dev-tag original">{/原创|库外/.test(text) ? "原创" : text || "—"}</span>;
  return <span className="dev-tag">{ids.map(id => `${id} ${lib.get(id)?.name ?? ""}`.trim()).join(" · ")}{text.includes("≈") ? " · 改造" : ""}</span>;
}

/** 01 主题：一句话 → 一段 → 一页，三级放大。 */
export function ThemeZoom({ m, compact = false }: { m: DevModel; compact?: boolean }): JSX.Element {
  const t = m.theme;
  return <section className="dev-zoom" aria-label="主题摘要">
    <div className="dev-zoom-l1"><span className="dev-zoom-mark">一句话</span><p className="dev-oneline">{t["一句话"] || "（还没有一句话）"}</p>
      {t["英文 logline"] ? <p className="dev-logline" lang="en">{t["英文 logline"]}</p> : null}</div>
    {!compact && t["一段"] ? <div className="dev-zoom-l2"><span className="dev-zoom-mark">一段</span><p className="dev-paragraph">{t["一段"]}</p></div> : null}
    {!compact && t["一页"] ? <details className="dev-zoom-l3"><summary>一页（展开）</summary><p className="dev-paragraph">{t["一页"]}</p></details> : null}
  </section>;
}

function Callout({ label, text, tone }: { label: string; text: string; tone?: "main" | "inner" }): JSX.Element | null {
  return text ? <p className={`dev-callout ${tone ?? ""}`}><span>{label}</span>{text}</p> : null;
}

/** 02 世界：种族与势力卡片（配资料库概念图）+ 关系图。 */
export function WorldBoard({ m, lib, compact = false }: { m: DevModel; lib: LibIndex; compact?: boolean }): JSX.Element {
  const chart = worldChart(m);
  return <div className="dev-board">
    {!compact ? <Callout label="舞台" text={m.world.stage} /> : null}
    {m.world.groups.length ? <ul className={compact ? "dev-cards mini" : "dev-cards"} aria-label="种族与势力">{m.world.groups.map(g =>
      <li key={g.name} className="dev-card"><LibThumb text={g.lib} title={g.name} lib={lib} />
        <div><strong>{g.name}</strong>{!compact ? <><LibTag text={g.lib} lib={lib} /><p>{g.line}</p></> : null}</div></li>)}</ul> : <Empty what="种族与势力" />}
    {chart ? <Mermaid chart={chart} label="世界关系图" /> : <Empty what="关系" />}
    {!compact ? <Callout label="正在发生的变化" text={m.world.change} /> : null}
  </div>;
}

function Ladder({ m }: { m: DevModel }): JSX.Element {
  const rows = m.power.ladder;
  if (!rows.length) return <Empty what="强弱阶梯" />;
  return <ol className="dev-ladder" aria-label="强弱阶梯">{rows.map((r, i) =>
    <li key={i} style={{ width: `${rows.length > 1 ? 52 + (48 * i) / (rows.length - 1) : 100}%` }}>
      <strong>{r.tier}</strong><span>{humanize(r.who, m.people.list)}</span></li>)}</ol>;
}

/** 03 力量：力量卡（谁拥有 · 代价）+ 强弱阶梯 + 克制图。 */
export function PowerBoard({ m, lib, compact = false }: { m: DevModel; lib: LibIndex; compact?: boolean }): JSX.Element {
  const chart = counterChart(m);
  if (compact) return <div className="dev-board"><Ladder m={m} /></div>;
  return <div className="dev-board">
    {m.power.sources.length ? <ul className="dev-cards" aria-label="力量源">{m.power.sources.map(s =>
      <li key={s.name} className="dev-card"><LibThumb text={s.lib} title={s.name} lib={lib} />
        <div><strong>{s.name}</strong><LibTag text={s.lib} lib={lib} />
          <p><span className="dev-k">谁拥有</span>{humanize(s.who, m.people.list)}</p>
          <p className="dev-cost"><span className="dev-k">代价</span>{s.cost}</p></div></li>)}</ul> : <Empty what="力量源" />}
    <div className="dev-split">
      <div><h3>强弱阶梯</h3><Ladder m={m} /></div>
      <div><h3>克制</h3>{chart ? <Mermaid chart={chart} label="克制图" /> : <Empty what="克制" />}</div>
    </div>
  </div>;
}

function Dots({ n, label }: { n: number | null; label: string }): JSX.Element | null {
  if (!n) return null;
  return <span className="dev-dots" role="img" aria-label={`${label} ${n}/5`}>{[1, 2, 3, 4, 5].map(i => <i key={i} className={i <= n ? "on" : undefined} />)}</span>;
}

/** 04 人物：人物卡（想要 / 缺陷 / 外在与内在能力）+ 内外能力象限图 + 关系图。 */
export function PeopleBoard({ m, compact = false }: { m: DevModel; compact?: boolean }): JSX.Element {
  const chart = peopleChart(m);
  const abilities = abilityChart(m);
  return <div className="dev-board">
    {!compact ? (m.people.list.length ? <ul className="dev-people" aria-label="人物">{m.people.list.map((p, i) =>
      <li key={p.id} className={i === 0 ? "hero" : undefined}>
        <div className="dev-avatar" aria-hidden="true">{p.name.slice(0, 1)}</div>
        <div><strong>{p.name}</strong> <span className="dev-muted">{p.id}{i === 0 ? " · 主角" : ""}</span><p className="dev-muted">{p.role}</p>
          <p><span className="dev-k want">想要</span>{p.want}</p><p><span className="dev-k flaw">缺陷</span>{p.flaw}</p>
          {p.ability ? <div className="dev-ability">
            <p><span className="dev-k outer">外在</span><Dots n={p.ability.outerScore} label="外在" />{p.ability.outer}</p>
            <p><span className="dev-k inner">内在</span><Dots n={p.ability.innerScore} label="内在" />{p.ability.inner}</p>
          </div> : null}</div></li>)}</ul>
      : <Empty what="人物" />) : null}
    {!compact ? <div className="dev-split">
      <div><h3>内外能力</h3>{abilities ? <Mermaid chart={abilities} label="内外能力象限图" /> : <Empty what="能力" />}</div>
      <div><h3>关系</h3>{chart ? <Mermaid chart={chart} label="人物关系图" /> : <Empty what="人物关系" />}</div>
    </div> : chart ? <Mermaid chart={chart} label="人物关系图" /> : <Empty what="人物关系" />}
  </div>;
}

/** 05 矛盾：主要矛盾 + 矛盾图（主粗次细）+ 内在矛盾。 */
export function ConflictBoard({ m, compact = false }: { m: DevModel; compact?: boolean }): JSX.Element {
  const chart = conflictChart(m);
  return <div className="dev-board">
    <Callout label="主要矛盾" text={humanize(m.conflict.main, m.people.list)} tone="main" />
    {chart ? <Mermaid chart={chart} label="矛盾图" /> : <Empty what="矛盾图" />}
    {!compact ? <><p className="dev-legend"><span className="main" />主要矛盾<span className="minor" />次要矛盾</p>
      <Callout label="内在矛盾" text={humanize(m.conflict.inner, m.people.list)} tone="inner" /></> : null}
  </div>;
}

/** 06 秘密与伏笔：按故事阶段排的时间线。 */
export function SecretsBoard({ m }: { m: DevModel }): JSX.Element {
  if (!m.secrets.length) return <Empty what="秘密" />;
  return <ol className="dev-timeline" aria-label="秘密时间线">{secretsByStage(m.secrets).map(l =>
    <li key={l.stage} className={l.items.length ? undefined : "idle"}><span className="dev-stage">{l.stage}</span>
      {l.items.map((x, i) => <div key={i} className="dev-secret"><strong>{humanize(x.secret, m.people.list)}</strong>
        <p className="dev-muted">谁知道：{humanize(x.who, m.people.list)}</p><p>→ {humanize(x.change, m.people.list)}</p></div>)}</li>)}</ol>;
}

/** 07 观众与爽点。 */
export function AudienceBoard({ m }: { m: DevModel }): JSX.Element {
  return <div className="dev-board">
    <Callout label="核心体验" text={m.audience.core} tone="main" />
    {m.audience.hooks.length ? <ul className="dev-hooks">{m.audience.hooks.map((h, i) =>
      <li key={i}><strong>{h.kind}</strong><p>{humanize(h.look, m.people.list)}</p></li>)}</ul> : <Empty what="爽点" />}
  </div>;
}

export function PageBoard({ page, m, lib }: { page: string; m: DevModel; lib: LibIndex }): JSX.Element | null {
  switch (page) {
    case "01_主题": return <ThemeZoom m={m} />;
    case "02_世界": return <WorldBoard m={m} lib={lib} />;
    case "03_力量": return <PowerBoard m={m} lib={lib} />;
    case "04_人物": return <PeopleBoard m={m} />;
    case "05_矛盾": return <ConflictBoard m={m} />;
    case "06_秘密与伏笔": return <SecretsBoard m={m} />;
    case "07_观众与爽点": return <AudienceBoard m={m} />;
    default: return null;
  }
}

/** 全景：一屏看完这部剧的核心 mental model。 */
export function Overview({ m, lib, open }: { m: DevModel; lib: LibIndex; open: (page: string) => void }): JSX.Element {
  const panel = (page: string, title: string, body: JSX.Element, wide = false): JSX.Element =>
    <section className={wide ? "dev-panel wide" : "dev-panel"} aria-label={`全景 · ${title}`}>
      <header><h2>{title}</h2><button type="button" onClick={() => open(page)}>细看 →</button></header>{body}</section>;
  return <div className="dev-overview">
    {panel("01_主题", "主题", <ThemeZoom m={m} compact />, true)}
    {panel("02_世界", "世界", <WorldBoard m={m} lib={lib} compact />)}
    {panel("03_力量", "力量", <PowerBoard m={m} lib={lib} compact />)}
    {panel("04_人物", "人物", <PeopleBoard m={m} compact />)}
    {panel("05_矛盾", "矛盾", <ConflictBoard m={m} compact />)}
    <p className="dev-muted dev-stages">故事阶段：{STAGES.join(" → ")}（季与集留给故事创作）</p>
  </div>;
}
