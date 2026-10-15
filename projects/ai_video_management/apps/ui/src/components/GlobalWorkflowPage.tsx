import { Children, useEffect, useState } from "react";
import type { ReactNode } from "react";
import { Link, useLocation, useParams, useSearchParams } from "react-router-dom";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeSanitize from "rehype-sanitize";
import { useGlobalWorkflow } from "./GlobalWorkflowContext";
import { GLOBAL_COVERAGE_PATH, GLOBAL_STATUS, formatLabels, globalGroupUrl, globalSourceUrl, loadGlobal, numberedTitle, sourceAdaptations, sourceTitle, type GlobalCoverage, type GlobalSourceDetail } from "../lib/globalWorkflow";
import { OVERVIEW_PATH, WORKFLOW_MODULES, WORKFLOW_PATH, workflowModulePath, categoryUrl, workflowCategories, workflowGroups } from "../lib/workflowData";
import type { StageId } from "../lib/episodeWorkflow";
import "./GlobalWorkflowPage.css";

export function GlobalWorkflowOverview({ group, category }: { group?: string; category?: string }): JSX.Element {
  const { catalog, error, refresh } = useGlobalWorkflow();
  const groups = workflowGroups(catalog).filter(entry => group ? entry.id === group : entry.category === category);
  return <section className="global-workflow"><header><h2>{group ? "当前共用源" : "全局设置与规则"}</h2><button onClick={refresh}>刷新目录</button></header>
    <p>这里的源跨剧适用。具体是否生效由任务、剧内声明和运行环境决定；用户配置属于当前电脑。</p>
    {error ? <p role="alert">{error}。三大模块仍可使用；全局目录尚未核验。</p> : !catalog ? <p role="status">正在加载全局目录…</p> : null}
    {!group && !category ? workflowCategories(catalog).map(entry => <section key={entry.id}><h3><Link to={categoryUrl(entry.id)}>{numberedTitle(entry)}</Link></h3><p>{entry.description}</p></section>) : null}
    {groups.map(entry => <section key={entry.id}><h3><Link to={WORKFLOW_MODULES.some(module => module.id === entry.id) ? workflowModulePath(entry.id as StageId) : entry.id === "overview" ? OVERVIEW_PATH : globalGroupUrl(entry.id)}>{numberedTitle(entry)}</Link></h3><p>{entry.description}</p>
      {!group ? <p>{catalog ? `${catalog.sources.filter(source => source.group === entry.id).length} 份共用源` : "目录待核验"} · 展开左侧分类或点击标题查看</p> : <ul className="global-source-list">{catalog?.sources.filter(source => source.group === entry.id).map(source => <li key={source.id}>
        <Link to={globalSourceUrl(source.id)}>{sourceTitle(source)}</Link><span>{source.scope === "user" ? "用户级" : "仓库级"} · {GLOBAL_STATUS[source.status]}{source.historical ? " · 历史参考" : ""}</span>
        <code>{source.scope === "user" ? "~/" : ""}{source.path}</code>
      </li>)}</ul>}</section>)}
    {!group ? <Link to={GLOBAL_COVERAGE_PATH}>工作流覆盖核对 →</Link> : null}
  </section>;
}

export function GlobalWorkflowCategoryPage(): JSX.Element {
  const { category } = useParams();
  const { catalog } = useGlobalWorkflow();
  const selected = workflowCategories(catalog).find(entry => entry.id === category);
  return <div className="episode-workflow"><Link to={WORKFLOW_PATH}>工作流</Link><h1>{selected ? numberedTitle(selected) : "未知全局分类"}</h1>
    {selected ? <GlobalWorkflowOverview category={category} /> : <p role="alert">全局目录中没有此分类。</p>}</div>;
}

export function GlobalWorkflowGroupPage(): JSX.Element {
  const { group } = useParams();
  const { catalog } = useGlobalWorkflow();
  if (group === "coverage") return <GlobalCoveragePage />;
  const selected = catalog?.groups.find(entry => entry.id === group);
  return <div className="episode-workflow"><Link to={WORKFLOW_PATH}>工作流</Link><h1>{selected ? numberedTitle(selected) : "全局设置"}</h1>
    {catalog && !selected ? <p role="alert">全局目录中没有此分类。</p> : <GlobalWorkflowOverview group={group} />}</div>;
}

// Heading text doubles as the anchor, so `adapts[].section` can deep-link into a page.
const headingId = (children: ReactNode): string => Children.toArray(children).map(child => typeof child === "string" || typeof child === "number" ? String(child) : "").join("").trim();

export function GlobalWorkflowSourcePage(): JSX.Element {
  const [params] = useSearchParams();
  const identity = params.get("source_id") || "";
  const { catalog, refresh } = useGlobalWorkflow();
  const location = useLocation();
  const [source, setSource] = useState<GlobalSourceDetail | null>(null);
  const [error, setError] = useState("");
  const [version, setVersion] = useState(0);
  useEffect(() => {
    const controller = new AbortController();
    setSource(null); setError("");
    loadGlobal<GlobalSourceDetail>(`/api/global-workflow/source?${new URLSearchParams({ source_id: identity })}`, controller.signal)
      .then(value => { if (!controller.signal.aborted) setSource(value); })
      .catch((reason: unknown) => { if (!controller.signal.aborted) setError(reason instanceof Error ? reason.message : String(reason)); });
    return () => controller.abort();
  }, [identity, version]);
  const resolveLocal = (href: string): string | undefined => {
    if (!source || /^(?:[a-z][a-z\d+.-]*:|\/\/)/i.test(href)) return undefined;
    if (href.startsWith("#")) return href;
    try {
      const target = new URL(href, `https://source.invalid/${source.path}`);
      const path = decodeURIComponent(target.pathname.slice(1));
      const entry = catalog?.sources.find(item => item.scope === source.scope && item.path === path);
      return entry ? globalSourceUrl(entry.id) : undefined;
    } catch { return undefined; }
  };
  const content = source?.content;
  useEffect(() => {
    if (content && location.hash) document.getElementById(decodeURIComponent(location.hash.slice(1)))?.scrollIntoView();
  }, [content, location.hash]);
  const adaptations = source && !source.formats?.length ? sourceAdaptations(catalog, source.id) : [];
  return <article className="episode-workflow global-workflow"><nav><Link to={WORKFLOW_PATH}>工作流</Link>{source ? <> / <Link to={globalGroupUrl(source.group)}>{catalog?.groups.find(group => group.id === source.group)?.title || source.group}</Link></> : null}</nav>
    <header><h1>{source ? sourceTitle(source) : "全局源文档"}</h1><button onClick={() => { setVersion(value => value + 1); refresh(); }}>刷新源文件</button></header>
    {error ? <p role="alert">{error}。此链接未核验，不能作为已纳入的全局源。</p> : !source ? <p role="status">正在加载源文件…</p> : <>
      {adaptations.length ? <nav className="format-adaptations" aria-label="片种适配"><span>片种适配</span>
        {adaptations.map(({ source: entry, section }) => <Link key={`${entry.id}#${section}`} to={`${globalSourceUrl(entry.id)}${section ? `#${encodeURIComponent(section)}` : ""}`}>
          {formatLabels(catalog, entry).join(" / ") || entry.title}{section ? ` · ${section}` : ""}</Link>)}
      </nav> : null}
      {source.redacted ? <p>配置中的密钥、环境变量值、请求头及启动参数已隐藏；工具配置只展示源码声明，不执行代码。</p> : null}
      {source.format === "markdown" ? <div className="markdown-view"><ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeSanitize]} components={{
        h1: ({ children }) => <h2 id={headingId(children)}>{children}</h2>,
        h2: ({ children }) => <h3 id={headingId(children)}>{children}</h3>,
        h3: ({ children }) => <h4 id={headingId(children)}>{children}</h4>,
        a: ({ href, children }) => {
          const local = href ? resolveLocal(href) : undefined;
          return local?.startsWith("/workflow") ? <Link to={local}>{children}</Link> : local?.startsWith("#") ? <a href={local}>{children}</a> : href && /^https?:\/\//i.test(href) ? <a href={href} target="_blank" rel="noreferrer">{children}</a> : <span title={href ? `引用未纳入全局目录：${href}` : undefined}>{children}</span>;
        },
      }}>{content}</ReactMarkdown></div> : <pre className="global-source-content">{content}</pre>}
    </>}
  </article>;
}

function GlobalCoveragePage(): JSX.Element {
  const [coverage, setCoverage] = useState<GlobalCoverage | null>(null);
  const [error, setError] = useState("");
  const [version, setVersion] = useState(0);
  useEffect(() => {
    const controller = new AbortController();
    setCoverage(null); setError("");
    loadGlobal<GlobalCoverage>("/api/global-workflow/coverage", controller.signal).then(value => {
      if (!controller.signal.aborted) setCoverage(value);
    }).catch((reason: unknown) => { if (!controller.signal.aborted) setError(reason instanceof Error ? reason.message : String(reason)); });
    return () => controller.abort();
  }, [version]);
  return <article className="episode-workflow global-workflow"><Link to={WORKFLOW_PATH}>工作流</Link><header><h1>工作流覆盖核对</h1><button onClick={() => setVersion(value => value + 1)}>重新核对</button></header>
    {error ? <p role="alert">{error}</p> : !coverage ? <p role="status">正在核对目录…</p> : <>
      {coverage.inventory ? <section aria-label="当前全局目录覆盖"><h2>当前全局目录覆盖</h2>
        <p>已登记 {coverage.inventory.total} 份源，{coverage.inventory.available} 份可安全读取，{coverage.inventory.numbered} 份已编号；其中 {coverage.inventory.historical} 份为历史参考。</p>
        <p>共用文档中的现存文件引用：{coverage.inventory.references.length} 个未登记；{coverage.inventory.issues.filter(issue => issue.kind === "unnumbered").length} 个源待编号，{coverage.inventory.issues.filter(issue => issue.kind === "unavailable" || issue.kind === "ungrouped").length} 个源无法读取或导航。</p>
        <p>登记表示能从工作流查看，不表示本次全部加载。剧、季、集的局部设定仍在剧导航；秘密环境值、隐藏系统指令、外部插件内部状态不能由当前目录证明。静态默认值可能被实际运行配置覆盖。</p>
        <details><summary>未配置项目与其他目录问题（{coverage.inventory.issues.length}）</summary><p>未配置的可选设置不是执行失败；不会自动创建或填充。</p><ul>{coverage.inventory.issues.map(issue => <li key={`${issue.source_id}:${issue.kind}`}><Link to={globalSourceUrl(issue.source_id)}>{issue.path}</Link>：{issue.note}</li>)}</ul></details>
        {coverage.inventory.references.length ? <ul>{coverage.inventory.references.map(reference => <li key={`${reference.source_id}:${reference.path}`}><Link to={globalSourceUrl(reference.source_id)}>引用文档</Link> → <code>{reference.path}</code>{reference.historical ? "（历史参考）" : ""}：未登记</li>)}</ul> : null}
      </section> : <p role="alert">当前目录覆盖尚未核验，请刷新服务后重试。</p>}
    </>}
  </article>;
}
