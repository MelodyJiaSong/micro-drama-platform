import { useMemo, useState } from "react";
import { GlossaryGraph } from "./GlossaryGraph";
import { GlossaryTimeline } from "./GlossaryTimeline";
import { GLOSSARY, GLOSSARY_SOURCE, categoryOf, relationType, relationsOf, termById, type Glossary } from "../lib/glossary";
import { globalSourceUrl } from "../lib/globalWorkflow";
import { OverviewTabs } from "./OverviewTabs";
import "./GlossaryPage.css";
import "./WorkflowMapPage.css";

type View = "graph" | "timeline" | "list";
const VIEWS: { id: View; zh: string }[] = [{ id: "graph", zh: "关系图" }, { id: "timeline", zh: "时间轴" }, { id: "list", zh: "术语列表" }];

function TermDetail({ glossary, id, onSelect }: { glossary: Glossary; id: string; onSelect: (id: string) => void }): JSX.Element {
  const term = termById(glossary, id);
  if (!term) {
    return <aside className="glossary-detail" aria-label="术语详情">
      <h2>结构一览</h2>
      <p>{glossary.summary.zh}</p>
      <p lang="en" className="glossary-en">{glossary.summary.en}</p>
      <p className="glossary-hint">点关系图里的术语、时间轴的行名或列表里的一行，查看定义与关联。</p>
    </aside>;
  }
  const category = categoryOf(glossary, term);
  return <aside className="glossary-detail" aria-label="术语详情">
    <p className="glossary-chip" style={{ color: category?.color, borderColor: category?.color }}>{category?.zh} · {category?.en}</p>
    <h2>{term.zh} <span lang="en">{term.en}</span></h2>
    {term.zh_alt ? <p className="glossary-alt">也叫：{term.zh_alt}</p> : null}
    <p>{term.def_zh}</p>
    <p lang="en" className="glossary-en">{term.def_en}</p>
    {term.notes?.length ? <><h3>区分与分歧</h3><ul className="glossary-notes">{term.notes.map(note => <li key={note}>{note}</li>)}</ul></> : null}
    <dl>
      <dt>所在模块</dt><dd>{term.module}</dd>
      <dt>在仓库里</dt><dd>{term.where}</dd>
    </dl>
    <h3>关联</h3>
    <ul className="glossary-relations">
      {relationsOf(glossary, term.id).map(({ relation, other, outgoing }) => {
        const type = relationType(glossary, relation.type);
        const otherTerm = termById(glossary, other);
        return <li key={`${relation.from}-${relation.to}-${relation.type}`}>
          <span className="glossary-card" style={{ color: type?.color, borderColor: type?.color }}>{relation.card || type?.zh}</span>
          <button type="button" onClick={() => onSelect(other)}>{outgoing ? "→" : "←"} {otherTerm?.zh}</button>
          <span>{relation.zh}</span>
        </li>;
      })}
    </ul>
    {term.sources?.length ? <><h3>来源</h3><ul className="glossary-sources">{term.sources.map(url => <li key={url}><a href={url} target="_blank" rel="noreferrer">{decodeURI(url).replace(/^https?:\/\/(www\.)?/, "")}</a></li>)}</ul></> : null}
    <button type="button" className="glossary-clear" onClick={() => onSelect("")}>回到结构一览</button>
  </aside>;
}

function Legend({ glossary, hidden, onToggle }: { glossary: Glossary; hidden: Set<string>; onToggle: (id: string) => void }): JSX.Element {
  return <div className="glossary-legend">
    <div role="group" aria-label="术语类别">
      {glossary.categories.map(category => <span key={category.id} className="glossary-legend-item">
        <i style={{ background: category.color }} />{category.zh}
      </span>)}
    </div>
    <div role="group" aria-label="关系类型（点击显示或隐藏）">
      {glossary.relation_types.map(type => <button key={type.id} type="button" aria-pressed={!hidden.has(type.id)} onClick={() => onToggle(type.id)}>
        <svg width="28" height="8" aria-hidden="true"><line x1="0" y1="4" x2="28" y2="4" stroke={type.color} strokeWidth="2" strokeDasharray={type.dash || undefined} /></svg>
        {type.zh}
      </button>)}
    </div>
  </div>;
}

export function GlossaryPage(): JSX.Element {
  const glossary = GLOSSARY;
  const [view, setView] = useState<View>("graph");
  const [selected, setSelected] = useState("scene");
  const [hidden, setHidden] = useState<Set<string>>(new Set());
  const [query, setQuery] = useState("");
  const toggle = (id: string): void => setHidden(previous => {
    const next = new Set(previous);
    if (next.has(id)) next.delete(id); else next.add(id);
    return next;
  });
  const filtered = useMemo(() => {
    const needle = query.trim().toLowerCase();
    return glossary.terms.filter(term => !needle || [term.zh, term.en, term.zh_alt || "", term.def_zh, term.def_en].some(text => text.toLowerCase().includes(needle)));
  }, [glossary, query]);

  return <div className="episode-workflow glossary-page">
    <OverviewTabs active="glossary" source={globalSourceUrl(GLOSSARY_SOURCE)} />
    <p className="map-summary">{glossary.summary.zh}</p>
    <div className="glossary-tabs glossary-views" role="tablist" aria-label="视图">
      {VIEWS.map(entry => <button key={entry.id} type="button" role="tab" aria-selected={view === entry.id} onClick={() => setView(entry.id)}>{entry.zh}</button>)}
    </div>
    <div className="glossary-body">
      <section className="glossary-main" role="tabpanel" aria-label={VIEWS.find(entry => entry.id === view)?.zh}>
        {view === "graph" ? <>
          <Legend glossary={glossary} hidden={hidden} onToggle={toggle} />
          <GlossaryGraph glossary={glossary} selected={selected} hidden={hidden} onSelect={setSelected} />
          <p className="glossary-hint">实线是树（包含），虚线是两棵树之间或时间区间上的多对多；连线上标着基数。图里只放结构单位，镜头类型和具体转折点见术语列表。可拖动节点；用左上角按钮或触控板缩放；点空白处取消选择。</p>
        </> : null}
        {view === "timeline" ? glossary.timelines.map(timeline => <GlossaryTimeline key={timeline.id} glossary={glossary} timeline={timeline} selected={selected} onSelect={setSelected} />) : null}
        {view === "list" ? <>
          <input className="glossary-search" type="search" placeholder="搜索中文、英文或定义" aria-label="搜索术语" value={query} onChange={event => setQuery(event.target.value)} />
          <div className="glossary-table-wrap">
            <table className="glossary-table">
              <thead><tr><th>术语</th><th>Term</th><th>类别</th><th>定义</th><th>Definition</th></tr></thead>
              <tbody>{filtered.map(term => {
                const category = categoryOf(glossary, term);
                return <tr key={term.id} className={term.id === selected ? "is-selected" : ""} onClick={() => setSelected(term.id)}>
                  <th scope="row"><button type="button" onClick={() => setSelected(term.id)}>{term.zh}</button>{term.zh_alt ? <small className="glossary-alt">{term.zh_alt}</small> : null}</th>
                  <td lang="en">{term.en}</td>
                  <td><span className="glossary-dot" style={{ background: category?.color }} />{category?.zh}</td>
                  <td>{term.def_zh}</td>
                  <td lang="en">{term.def_en}</td>
                </tr>;
              })}</tbody>
            </table>
          </div>
        </> : null}
      </section>
      <TermDetail glossary={glossary} id={selected} onSelect={setSelected} />
    </div>
  </div>;
}
