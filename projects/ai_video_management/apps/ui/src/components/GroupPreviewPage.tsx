import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { fetchFile, fetchSubtree, mediaUrl } from "../api";
import { useFileChanges } from "../lib/fileEvents";
import { groupFiles, groupSpec, parseGroupPath, reviewStatus, type CompiledRef, type GroupFiles, type GroupSpec,
  type GroupTake } from "../lib/groupPreview";
import "./HeroPreviewPage.css";
import "./GroupPreviewPage.css";

const fileHref = (path: string): string => `/file/${encodeURIComponent(path)}`;

async function text(path: string | null): Promise<string | null> {
  if (!path) return null;
  try { return (await fetchFile(path)).content; } catch { return null; }
}
async function json<T>(path: string): Promise<T | null> {
  const t = await text(path);
  try { return t ? JSON.parse(t) as T : null; } catch { return null; }
}

interface Loaded { files: GroupFiles; spec: GroupSpec; prompt: string | null; promptSource: string;
  invalid: string | null; statuses: Record<string, string> }

function Ref({ r, revision }: { r: CompiledRef; revision: number }): JSX.Element {
  const src = mediaUrl(r.path, revision);
  return <figure className="hero-preview-media group-ref">
    {r.kind === "image" && <a href={src} target="_blank" rel="noreferrer"><img src={src} alt={r.key} loading="lazy" /></a>}
    {r.kind === "audio" && <audio controls preload="none" src={src} />}
    {r.kind === "video" && <video controls preload="none" src={src} />}
    <figcaption><strong>{r.role}</strong><br /><Link to={fileHref(r.path)}>{r.key}</Link></figcaption>
  </figure>;
}

function Take({ take, status, revision }: { take: GroupTake; status: string; revision: number }): JSX.Element {
  return <article className="group-take">
    {take.video ? <video controls preload="metadata" src={mediaUrl(take.video.path, revision)} />
      : <p className="hero-preview-empty">这一条没有视频文件。</p>}
    <p className="hero-preview-meta">
      <span>{take.stage === "draft" ? "草稿" : "正式条"} {take.name}</span>
      <span className={status.startsWith("通过") ? "group-ok" : "group-pending"}>{status || "未记状态"}</span>
      {take.review && <Link to={fileHref(take.review)}>审核记录</Link>}
      {take.prompt && <Link to={fileHref(take.prompt)}>提交时的 prompt</Link>}
      {take.generation && <Link to={fileHref(take.generation)}>生成记录</Link>}
      {take.video && <Link to={fileHref(take.video.path)}>视频文件</Link>}
    </p>
  </article>;
}

export function GroupPreviewPage(): JSX.Element {
  const [params] = useSearchParams();
  const path = (params.get("path") ?? "").replace(/\/+$/, "");
  const loc = parseGroupPath(path);
  const [data, setData] = useState<Loaded | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [revision, refresh] = useState(Date.now);
  useFileChanges(loc ? `${loc.episodePath}` : null, () => refresh(Date.now()));
  useEffect(() => {
    let cancelled = false;
    setError(null);
    if (!loc) { setError("链接形如 /group-preview?path=ai_videos/<剧>/episodes/ep01/scenes/s1/groups/g2"); return; }
    (async () => {
      const [node, filming, prompts] = await Promise.all([
        fetchSubtree(path, 0).catch(() => ({ type: "directory", name: loc.group, path, children: [] }) as never),
        json<{ content: { scenes: never[] } }>(`${loc.episodePath}/filming.json`),
        json<{ content: { scenes: never[] } }>(`${loc.episodePath}/prompts.json`),
      ]);
      const files = groupFiles(node);
      const spec = groupSpec(loc, filming?.content ?? null, prompts?.content ?? null);
      const packed = await text(files.packPrompt);
      const invalid = await text(files.packInvalid);
      const reviews = await Promise.all(files.takes.map(t => text(t.review)));
      const statuses = Object.fromEntries(files.takes.map((t, i) => [t.name, reviewStatus(reviews[i] ?? "")]));
      const prompt = packed ?? spec.compiled?.text ?? null;
      if (!cancelled) setData({ files, spec, prompt, invalid, statuses,
        promptSource: packed ? "资料包（已填上传编号）" : spec.compiled ? "prompts.json（编译结果）" : "" });
    })().catch(reason => { if (!cancelled) setError(reason instanceof Error ? reason.message : String(reason)); });
    return () => { cancelled = true; };
  }, [path, revision]);   // eslint-disable-line react-hooks/exhaustive-deps
  if (error) return <section className="hero-preview-page"><h1>镜组预览</h1><p role="alert">{error}</p></section>;
  if (!data || !loc) return <p role="status">加载镜组预览…</p>;
  const { files, spec } = data;
  const range = spec.members.length ? `${spec.members[0].shot.id}–${spec.members[spec.members.length - 1].shot.id}` : "";
  return <section className="hero-preview-page group-preview-page">
    <header>
      <h1>镜组 {loc.key}</h1>
      <p className="hero-preview-meta">
        {spec.scene && <span>{loc.scene} · {spec.scene.location} · {spec.scene.time}</span>}
        {range && <span>镜头 {range}（{spec.members.length} 镜）</span>}
        <span>总长 {spec.total} 秒</span>
        <span>{files.takes.length} 条出片</span>
      </p>
      {spec.problem && <p role="alert" className="group-alert">{spec.problem}</p>}
      {data.invalid && <details className="group-alert" open><summary>资料包已失效，不能拿去出片</summary><pre>{data.invalid}</pre></details>}
      <nav>
        <a href="#board">镜组板</a><a href="#takes">出片</a><a href="#shots">镜头分解</a><a href="#prompt">Prompt</a><a href="#refs">参考</a>
        <Link to={fileHref(`${loc.episodePath}/filming.json`)}>filming.json</Link>
        <Link to={fileHref(path)}>镜组目录</Link>
      </nav>
    </header>

    <h2 id="board">镜组板</h2>
    {files.board
      ? <div className="hero-preview-hero"><figure className="hero-preview-media">
        <a href={mediaUrl(files.board.path, revision)} target="_blank" rel="noreferrer">
          <img src={mediaUrl(files.board.path, revision)} alt="镜组板" /></a>
        <figcaption><Link to={fileHref(files.board.path)}>{files.board.name}</Link>：格子从左到右、从上到下对应镜头 1 到镜头 {spec.members.length}</figcaption>
      </figure></div>
      : <p className="hero-preview-empty">还没有镜组板（{path}/board.png）。</p>}
    {files.otherImages.length > 0 && <details className="hero-preview-fold"><summary>镜组板的其他版本（{files.otherImages.length}）</summary>
      <div className="hero-preview-thumbs">{files.otherImages.map(i => <figure key={i.path} className="hero-preview-media">
        <img src={mediaUrl(i.path, revision)} alt={i.name} loading="lazy" /><figcaption><Link to={fileHref(i.path)}>{i.name}</Link></figcaption>
      </figure>)}</div></details>}

    <h2 id="takes">出片</h2>
    {files.takes.length > 0
      ? <div className="group-takes">{files.takes.map((t, i) => i === 0
        ? <Take key={t.name} take={t} status={data.statuses[t.name]} revision={revision} />
        : null)}</div>
      : <p className="hero-preview-empty">还没有出片。</p>}
    {files.takes.length > 1 && <details className="hero-preview-fold"><summary>更早的出片（{files.takes.length - 1}）</summary>
      <div className="group-takes">{files.takes.slice(1).map(t => <Take key={t.name} take={t} status={data.statuses[t.name]} revision={revision} />)}</div>
    </details>}

    <h2 id="shots">镜头分解</h2>
    <ol className="group-shots">
      {spec.members.map((m, i) => <li key={m.shot.id} className="group-shot">
        <div className="group-shot-overhead">
          <img src={mediaUrl(m.overhead, revision)} alt={`${m.shot.id} 俯视站位图`} loading="lazy" />
          <Link to={fileHref(m.overhead)}>俯视站位图</Link>
        </div>
        <div>
          <h3>镜头 {i + 1} · {m.shot.id} · 第 {m.start}–{m.end} 秒（{m.shot.duration} 秒）</h3>
          <dl>
            <dt>画面</dt><dd>{m.shot.action}</dd>
            {m.shot.blocking && <><dt>走位</dt><dd>{m.shot.blocking}</dd></>}
            <dt>动作</dt><dd>{m.shot.beats}</dd>
            <dt>镜头</dt><dd>{m.shot.camera}</dd>
            <dt>光线</dt><dd>{m.shot.lighting}</dd>
            <dt>台词</dt><dd>{m.shot.dialogue || "无"}</dd>
            <dt>人物 / 道具</dt><dd>{[...m.shot.cast, ...(m.shot.props ?? [])].join("、") || "无"}</dd>
          </dl>
        </div>
      </li>)}
    </ol>

    <h2 id="prompt">Prompt</h2>
    {data.prompt
      ? <><p className="hero-preview-meta"><span>来源：{data.promptSource}</span><span>{data.prompt.length} 字</span>
        {files.packPrompt && <Link to={fileHref(files.packPrompt)}>资料包 prompt.txt</Link>}
        {files.packManifest && <Link to={fileHref(files.packManifest)}>manifest.json</Link>}</p>
        <pre className="group-prompt">{data.prompt}</pre></>
      : <p className="hero-preview-empty">还没有编译出这个镜组的 prompt。</p>}

    <h2 id="refs">参考（按上传顺序）</h2>
    {spec.compiled
      ? <div className="hero-preview-thumbs">{spec.compiled.refs.map(r => <Ref key={r.key} r={r} revision={revision} />)}</div>
      : <p className="hero-preview-empty">编译后列出。</p>}
  </section>;
}
