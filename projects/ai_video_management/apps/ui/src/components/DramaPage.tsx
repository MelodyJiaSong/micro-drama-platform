/** DramaPage — the drama-level main page.
 *
 * Opened by clicking a drama node in the left nav (→ `/drama?drama={path}`),
 * which also toggles the nav dropdown. It is the home of the drama-wide
 * actions that do not belong to one file:
 *  - 📥 导入: move recent Downloads into the drama — a shot render by its full
 *    `ep{N}_s{N}_st{N}` key into `renders/<条>/`, an asset view by its
 *    `bg` / `p` / `e` / `c` key — then the folder-name rename pass.
 *  - 🎭 角色画廊: every character's turntable + one-click three-view extraction.
 * A six-module drama (`workflow.json: three-module-v1`) with a module selected
 * shows its episode workflow below the actions; the actions stay reachable
 * there because downloaded takes only reach the shot pages through 导入.
 * A drama marked obsolete (`OBSOLETE.md` on it or its series) shows the
 * 「已过时」badge. (The old production console — takes, concat, subtitles,
 * production export, per-episode masters — went with follow-up 233.) */
import { useCallback, useMemo, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { importFromDownloads } from "../api";
import { ApiError, type TreeNode } from "../types";
import { announceToast } from "../lib/announce";
import { EpisodeWorkflowPage } from "./EpisodeWorkflowPage";
import { ObsoleteBadge } from "./ObsoleteBadge";

export interface DramaPageProps {
  tree: TreeNode | null;
  onChange: () => void;
}

function findNodeByPath(tree: TreeNode | null, path: string): TreeNode | null {
  if (!tree) return null;
  const queue: TreeNode[] = [tree];
  while (queue.length > 0) {
    const node = queue.shift()!;
    if (node.path === path) return node;
    for (const c of node.children ?? []) queue.push(c);
  }
  return null;
}

export function DramaPage({ tree, onChange }: DramaPageProps): JSX.Element {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const dramaPath = searchParams.get("drama") ?? "";
  const [importBusy, setImportBusy] = useState<boolean>(false);
  // Bumped after an import so the episode workflow reloads and lists the new takes.
  const [imports, setImports] = useState<number>(0);

  const dramaNode = useMemo(() => findNodeByPath(tree, dramaPath), [tree, dramaPath]);
  const obsolete = dramaNode?.obsolete === true;

  const onImportClick = useCallback(async () => {
    if (importBusy) return;
    if (obsolete && !window.confirm("本剧已过时（见 OBSOLETE.md）。仍要把 Downloads 里匹配的文件导入到这部旧剧吗？")) return;
    setImportBusy(true);
    try {
      const result = await importFromDownloads(dramaPath);
      const errorCount = result.errors.length + result.rename.errors.length;
      announceToast(
        `已导入 ${result.moved.length} / 未导入 ${result.unmatched.length} ` +
          `/ 已重命名 ${result.rename.renamed.length} / 失败 ${errorCount}`,
      );
      setImports((n) => n + 1);
      onChange();
    } catch (err) {
      const kind = err instanceof ApiError ? (err.detail?.kind ?? `HTTP ${err.status}`) : String(err);
      announceToast(`导入失败: ${kind}`);
    } finally {
      setImportBusy(false);
    }
  }, [dramaPath, importBusy, obsolete, onChange]);

  if (!tree) return <div className="drama-page" role="status">加载剧集…</div>;

  if (!dramaPath || !dramaNode) {
    return (
      <div className="drama-page">
        <div className="drama-page-header">
          <h1>剧集主页</h1>
        </div>
        <div className="drama-page-empty">没有找到该剧集。请从左侧选择一部剧。</div>
      </div>
    );
  }

  const title = dramaNode.display_name || dramaNode.name;
  const actions = (
    <div className="drama-page-actions" role="group" aria-label="资源管理">
      <button
        type="button"
        className="drama-page-action-btn"
        onClick={onImportClick}
        disabled={importBusy}
        title="从 Downloads 导入近 7 天的图片 / 视频：镜头条按完整 key（ep1_s1_st1）归位到该镜头的 renders/<条>/，资产图按 bg / p / e / c 键归位；随后按文件夹名整理资产图文件名。匹配不上的文件留在 Downloads。"
      >
        {importBusy ? "⏳ 导入中…" : "📥 导入"}
      </button>
      <button
        type="button"
        className="drama-page-action-btn"
        onClick={() => navigate(`/characters?drama=${encodeURIComponent(dramaPath)}`)}
        title="角色画廊：所有角色的建立视频 + 一键重提三视图 / 音频 / 前 2 秒"
      >
        🎭 角色画廊
      </button>
      {obsolete && dramaNode.obsolete_note ? (
        <button
          type="button"
          className="drama-page-link-btn"
          onClick={() => navigate(`/file/${encodeURIComponent(dramaNode.obsolete_note!)}`)}
          title="打开 OBSOLETE.md：为什么过时、之后怎么处理"
        >
          📄 过时说明
        </button>
      ) : null}
    </div>
  );

  if (dramaNode.workflow === "three-module-v1" && searchParams.get("module")) {
    return (
      <div className="drama-page-workflow">
        <div className="drama-page-toolbar">
          {obsolete ? <ObsoleteBadge note={dramaNode.obsolete_note} /> : null}
          {actions}
        </div>
        <EpisodeWorkflowPage key={`${dramaPath}#${imports}`} dramaPath={dramaPath} title={title} />
      </div>
    );
  }

  return (
    <div className="drama-page">
      <div className="drama-page-header">
        <h1>{title}</h1>
        {obsolete ? <ObsoleteBadge note={dramaNode.obsolete_note} /> : null}
        <button
          type="button"
          className="drama-page-link-btn"
          onClick={() => navigate(`/file/${encodeURIComponent(`${dramaPath}/README.md`)}`)}
          title="打开本剧 README.md"
        >
          📖 打开 README
        </button>
      </div>
      {obsolete ? (
        <p className="drama-page-obsolete-note" role="note">
          本剧由已删除的旧流程制作或只服务旧流程，内容原样保留、只作参考；等用新流程重做时再更新。
        </p>
      ) : null}
      <section className="drama-page-section" aria-label="资源管理">
        <h2 className="drama-page-section-title">资源管理</h2>
        {actions}
      </section>
      {dramaNode.workflow === "three-module-v1" ? (
        <p className="drama-page-hint">从左侧展开 stage，选择要查看的集与模块。</p>
      ) : null}
    </div>
  );
}
