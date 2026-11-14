/** 新剧开发稿：预览 + 评审（xihuan follow-up 001 / 003）。
 * 框架目录：框架说明（含流程图）、模板、试套总评。开发稿目录：「全景」一屏看核心 mental model，
 * 逐页以图为主（表格自动画成关系图 / 阶梯 / 资料库概念图卡片），原文折叠在下面；
 * 评审页显示 check.py --json 写的 _check.json、试套反馈 _反馈.md、评估 _评估.md。只读。 */
import { useCallback, useEffect, useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { fetchFile, fetchSubtree, mediaUrl } from "../api";
import { useFileChanges } from "../lib/fileEvents";
import {
  CHECK_FILE, DEV_PAGES, FEEDBACK_FILE, REVIEW_FILE, devPreviewHref, isFrameworkRoot, join, limitOver, pageTitle,
  type CheckReport, type DevPageId,
} from "../lib/devPreview";
import { buildModel, splitMermaid } from "../lib/devDiagrams";
import { loadSharedLibrary } from "../lib/sharedAssets";
import { Renderer } from "../markdown/renderer";
import { Mermaid, Overview, PageBoard, type LibIndex } from "./DevDiagrams";
import "./DevPreviewPage.css";

const UNLOADED = ["ai_videos", ".agents"];
const LIBRARY_ROOT = "ai_videos/_shared/xihuan";
const OVERVIEW = "overview";

let libraryIndex: Promise<LibIndex> | null = null;
/** 西幻公共资料库：ID → 名称与概念图（读不到就只显示 ID）。 */
function loadLibraryIndex(): Promise<LibIndex> {
  if (!libraryIndex) {
    libraryIndex = loadSharedLibrary(LIBRARY_ROOT).then(lib => new Map(lib.assets.map(a => [a.id, {
      name: a.name, image: a.image.anchor && !["planned", "failed_or_unknown"].includes(a.image.status) ? mediaUrl(`${LIBRARY_ROOT}/${a.image.anchor}`) : null,
    }])), () => { libraryIndex = null; return new Map(); });
  }
  return libraryIndex;
}

async function readText(path: string): Promise<string | null> {
  try { return (await fetchFile(path)).content; } catch { return null; }
}

interface DevDocs { pages: Partial<Record<DevPageId, string>>; check: CheckReport | null; feedback: string | null; review: string | null; lib: LibIndex }
interface FrameworkDocs { readme: string | null; templates: Partial<Record<DevPageId, string>>; review: string | null; folders: { name: string; path: string; title: string }[] }

async function loadDev(dir: string): Promise<DevDocs> {
  const pages: Partial<Record<DevPageId, string>> = {};
  await Promise.all(DEV_PAGES.map(async p => { const t = await readText(join(dir, `${p.id}.md`)); if (t !== null) pages[p.id] = t; }));
  const checkText = await readText(join(dir, CHECK_FILE));
  return { pages, check: checkText ? JSON.parse(checkText) as CheckReport : null, feedback: await readText(join(dir, FEEDBACK_FILE)),
    review: await readText(join(dir, REVIEW_FILE)), lib: await loadLibraryIndex() };
}

async function loadFramework(dir: string): Promise<FrameworkDocs> {
  const templates: Partial<Record<DevPageId, string>> = {};
  await Promise.all(DEV_PAGES.map(async p => { const t = await readText(join(dir, `templates/${p.id}.md`)); if (t !== null) templates[p.id] = t; }));
  const examples = await fetchSubtree(join(dir, "examples"), 1).catch(() => null);
  const folders = await Promise.all((examples?.children ?? []).filter(c => c.type === "directory").map(async c => {
    const theme = await readText(join(c.path, "01_主题.md"));
    return theme === null ? null : { name: c.name, path: c.path, title: pageTitle(theme, c.name) };
  }));
  return { readme: await readText(join(dir, "README.md")), templates, review: await readText(join(dir, `examples/${REVIEW_FILE}`)),
    folders: folders.filter((f): f is NonNullable<typeof f> => f !== null) };
}

function Md({ text, path }: { text: string; path: string }): JSX.Element {
  return <>{splitMermaid(text).map((part, i) => part.kind === "mermaid"
    ? <Mermaid key={i} chart={part.text} label="流程图" />
    : <Renderer key={i} content={part.text} currentPath={path} knownPaths={[]} unloadedDirs={UNLOADED} />)}</>;
}

function Tabs<T extends string>({ value, options, onChange, label }: { value: T; options: { id: T; label: string; missing?: boolean }[]; onChange: (v: T) => void; label: string }): JSX.Element {
  return <div className="dev-tabs" role="tablist" aria-label={label}>{options.map(o =>
    <button key={o.id} type="button" role="tab" aria-selected={o.id === value} className={o.missing ? "missing" : undefined}
      onClick={() => onChange(o.id)}>{o.label}</button>)}</div>;
}

function CheckPanel({ check }: { check: CheckReport | null }): JSX.Element {
  if (!check) return <p className="dev-muted">还没有检查结果：运行 <code>python ai_videos/xihuan/framework/check.py &lt;目录&gt; --json</code>。</p>;
  return <section aria-label="形式检查">
    <p><span className={check.ok ? "dev-pill ok" : "dev-pill bad"}>{check.ok ? "形式检查通过" : `形式检查未通过 · ${check.errors.length} 处`}</span>
      <span className="dev-muted"> 生成于 {check.generated}（改稿后需重跑检查）</span></p>
    {check.errors.length ? <ul className="dev-errors">{check.errors.map((e, i) => <li key={i}>{e}</li>)}</ul> : null}
    {check.warnings?.length ? <><p className="dev-muted">提示（不拦）：</p><ul className="dev-warnings">{check.warnings.map((w, i) => <li key={i}>{w}</li>)}</ul></> : null}
    <table className="dev-table"><thead><tr><th>页</th><th>状态</th><th>篇幅</th><th>缺小节</th></tr></thead><tbody>
      {DEV_PAGES.map(p => { const s = check.pages[p.id]; return <tr key={p.id}>
        <td>{p.id}</td>
        <td>{!s?.exists ? (s?.required ? "缺页" : "未写（可选）") : "已写"}</td>
        <td>{Object.entries(s?.limits ?? {}).map(([k, v]) => <span key={k} className={limitOver(v) ? "dev-over" : undefined}>{k} {v.chars ?? v.words}/{v.limit}{v.words !== undefined ? " 词" : " 字"} </span>)}</td>
        <td>{s?.missing_sections?.join("、") || "—"}</td></tr>; })}
    </tbody></table>
  </section>;
}

function DevFolderView({ dir }: { dir: string }): JSX.Element {
  const [params, setParams] = useSearchParams();
  const [docs, setDocs] = useState<DevDocs | null>(null);
  const load = useCallback(() => { void loadDev(dir).then(setDocs); }, [dir]);
  useEffect(load, [load]);
  useFileChanges(dir, load, 800);
  const tab = (params.get("tab") === "review" ? "review" : "preview") as "preview" | "review";
  const page = DEV_PAGES.find(p => p.id === params.get("page"))?.id ?? OVERVIEW;
  const set = (key: string, value: string): void => { const next = new URLSearchParams(params); next.set(key, value); setParams(next, { replace: true }); };
  const model = useMemo(() => buildModel(docs?.pages ?? {}), [docs]);
  if (!docs) return <p role="status">正在读取开发稿…</p>;
  const title = pageTitle(docs.pages["01_主题"] ?? "", dir.split("/").slice(-1)[0]);
  return <div className="dev-page">
    <header className="dev-heading"><div><p className="dev-eyebrow">西幻 · 新剧开发稿</p><h1>{title}</h1></div>
      {docs.check ? <span className={docs.check.ok ? "dev-pill ok" : "dev-pill bad"}>{docs.check.ok ? "形式检查通过" : "形式检查未通过"}</span> : null}</header>
    <Tabs label="预览或评审" value={tab} onChange={v => set("tab", v)} options={[{ id: "preview", label: "预览" }, { id: "review", label: "评审" }]} />
    {tab === "preview" ? <>
      <Tabs label="开发稿页" value={page as string} onChange={v => set("page", v)}
        options={[{ id: OVERVIEW, label: "全景" }, ...DEV_PAGES.map(p => ({ id: p.id as string, label: p.label, missing: !docs.pages[p.id] }))]} />
      {page === OVERVIEW ? <Overview m={model} lib={docs.lib} open={p => set("page", p)} />
        : docs.pages[page as DevPageId] ? <article className="dev-doc" aria-label={page}>
          <PageBoard page={page} m={model} lib={docs.lib} />
          <details className="dev-source"><summary>原文</summary><Md text={docs.pages[page as DevPageId]!} path={join(dir, `${page}.md`)} /></details>
        </article>
        : <article className="dev-doc" aria-label={page}><p className="dev-muted">{DEV_PAGES.find(p => p.id === page)?.optional ? "这一页可以之后再补。" : "这一页还没写。"}</p></article>}
    </> : <div className="dev-review">
      <CheckPanel check={docs.check} />
      {docs.review ? <section aria-label="评估"><h2>评估</h2><Md text={docs.review} path={join(dir, REVIEW_FILE)} /></section> : null}
      <section aria-label="试套反馈"><h2>使用反馈</h2>{docs.feedback ? <Md text={docs.feedback} path={join(dir, FEEDBACK_FILE)} /> : <p className="dev-muted">没有反馈文件（{FEEDBACK_FILE}）。</p>}</section>
    </div>}
  </div>;
}

function FrameworkView({ dir }: { dir: string }): JSX.Element {
  const [params, setParams] = useSearchParams();
  const [docs, setDocs] = useState<FrameworkDocs | null>(null);
  const load = useCallback(() => { void loadFramework(dir).then(setDocs); }, [dir]);
  useEffect(load, [load]);
  useFileChanges(dir, load, 800);
  const tab = (["guide", "templates", "review"].includes(params.get("tab") ?? "") ? params.get("tab") : "guide") as "guide" | "templates" | "review";
  const page = (DEV_PAGES.find(p => p.id === params.get("page"))?.id ?? "01_主题") as DevPageId;
  const set = (key: string, value: string): void => { const next = new URLSearchParams(params); next.set(key, value); setParams(next, { replace: true }); };
  if (!docs) return <p role="status">正在读取开发框架…</p>;
  return <div className="dev-page">
    <header className="dev-heading"><div><p className="dev-eyebrow">西幻 · 系列级试点</p><h1>新剧开发框架</h1></div></header>
    {docs.folders.length ? <nav className="dev-folders" aria-label="开发稿">{docs.folders.map(f =>
      <Link key={f.path} to={devPreviewHref(f.path)}>试套 · {f.title}</Link>)}</nav> : null}
    <Tabs label="框架内容" value={tab} onChange={v => set("tab", v)} options={[{ id: "guide", label: "框架说明" }, { id: "templates", label: "模板" }, { id: "review", label: "试套评估" }]} />
    {tab === "guide" ? <article className="dev-doc">{docs.readme ? <Md text={docs.readme} path={join(dir, "README.md")} /> : null}</article> : null}
    {tab === "templates" ? <>
      <Tabs label="模板页" value={page} onChange={v => set("page", v)} options={DEV_PAGES.map(p => ({ id: p.id, label: p.label, missing: !docs.templates[p.id] }))} />
      <article className="dev-doc">{docs.templates[page] ? <Md text={docs.templates[page]!} path={join(dir, `templates/${page}.md`)} /> : null}</article>
    </> : null}
    {tab === "review" ? <article className="dev-doc">{docs.review ? <Md text={docs.review} path={join(dir, `examples/${REVIEW_FILE}`)} /> : <p className="dev-muted">试套评估还没写（examples/{REVIEW_FILE}）。</p>}</article> : null}
  </div>;
}

export function DevPreviewPage(): JSX.Element {
  const [params] = useSearchParams();
  const path = params.get("path") ?? "";
  if (!path) return <p role="alert">缺少 path 参数：链接形如 /dev-preview?path=ai_videos/xihuan/framework</p>;
  return isFrameworkRoot(path) ? <FrameworkView dir={path} /> : <DevFolderView dir={path} />;
}
