import { useCallback, useMemo, useState } from "react";
import type { ReactNode } from "react";
import ReactMarkdown from "react-markdown";
import rehypeSanitize from "rehype-sanitize";
import rehypeHighlight from "rehype-highlight";
import remarkGfm from "remark-gfm";
import { useNavigate } from "react-router-dom";
import { resolveLink } from "../lib/linkResolver";
import { knownPredicate } from "../lib/lazyTree";
import { BrokenLink } from "../components/BrokenLink";

/** Read-only markdown view: internal links resolve against the tree, fenced
 * blocks get field-label highlighting and a verbatim copy button. (Per-block
 * prompt editing, the AI rewrite suggestions, the locked-descriptor / `{ref_…}`
 * pills and novel-prose quote highlighting went with the old pipeline in
 * follow-up 233.) */
export interface RendererProps {
  content: string;
  currentPath: string;
  knownPaths: string[];
  /** Folders the lazy tree has not loaded (follow-up 280): links into them count as known. */
  unloadedDirs?: string[];
}

/** Field labels in a prompt body that get highlighted as key headers (the
 * compiled episode-workflow prompt and any fenced prompt block in markdown).
 */
const FIELD_LABEL_RE = /^(角色|场景|镜头|动作|台词(?: ?\/ ?字幕)?|节奏|光线(?: ?\/ ?色调)?|渲染样式|比例|时长|负向|负面词|主体定义|姿态(（[^）]*）)?|参考用法|参考|画幅|情节|走位|画面|声音|要求)([:：])(\s*)/;
/** First line of a compiled episode-workflow prompt: the full shot key (`ep1_s4_st1`). */
const SHOT_KEY_LINE_RE = /^ep\d+_s\d+_st\d+$/;

/** Walk a React node tree to extract its plain text content (used to render highlighted spans
 * while preserving the original text shape for `innerText` clipboard reads).
 */
function extractText(node: ReactNode): string {
  if (node === null || node === undefined || typeof node === "boolean") return "";
  if (typeof node === "string" || typeof node === "number") return String(node);
  if (Array.isArray(node)) return node.map(extractText).join("");
  if (typeof node === "object" && "props" in node) {
    return extractText((node as { props: { children?: ReactNode } }).props.children);
  }
  return "";
}

/** Render plain code-block text with per-line field-label highlighting.
 * The output is a sequence of React nodes whose innerText equals the original plain text,
 * so the copy button still reads cleanly via `preRef.current.innerText`.
 */
export function renderHighlightedLines(text: string): ReactNode {
  const lines = text.split("\n");
  return lines.map((line, idx) => {
    const m = line.match(FIELD_LABEL_RE);
    let content: ReactNode;
    if (m) {
      const label = m[1];
      const colon = m[m.length - 2];
      const spaces = m[m.length - 1] ?? "";
      const rest = line.slice(m[0].length);
      content = (
        <>
          <span className="field-label">{label}</span>
          {colon}
          {spaces}
          {rest}
        </>
      );
    } else if (SHOT_KEY_LINE_RE.test(line)) {
      content = <span className="shot-key-line">{line}</span>;
    } else {
      content = line;
    }
    return (
      <span key={idx}>
        {content}
        {idx < lines.length - 1 ? "\n" : null}
      </span>
    );
  });
}

interface CopyableCodeProps {
  children: ReactNode;
}

function CopyableCode({ children }: CopyableCodeProps): JSX.Element {
  const [copied, setCopied] = useState(false);
  // Extract the plain text of children, then re-render with field-label
  // highlighting. Copy uses the raw `trimmedBody` below (NOT innerText), so the
  // copied prompt keeps whitespace/newlines verbatim.
  const plain = useMemo(() => extractText(children), [children]);
  const trimmedBody = useMemo(() => plain.replace(/\r\n/g, "\n").replace(/\n+$/, ""), [plain]);
  const highlighted = useMemo(() => renderHighlightedLines(plain), [plain]);

  const handleCopy = useCallback(async () => {
    // Copy the code block's EXACT source text — every space and newline
    // preserved verbatim. We deliberately do NOT read the <pre>'s innerText:
    // innerText is layout-normalized and can collapse runs of whitespace /
    // alter newlines depending on CSS + the per-line <span> highlighting,
    // which garbles the prompt's structure for downstream models.
    try {
      await navigator.clipboard.writeText(trimmedBody);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1600);
    } catch {
      // clipboard API unavailable — graceful fallback: nothing to do
    }
  }, [trimmedBody]);

  return (
    <div className="code-block-wrapper">
      <div className="code-block-actions">
        <button
          type="button"
          className={`copy-btn${copied ? " copied" : ""}`}
          onClick={handleCopy}
          aria-label={copied ? "已复制" : "复制 prompt"}
        >
          {copied ? "已复制 ✓" : "复制 Copy"}
        </button>
      </div>
      <pre><code>{highlighted}</code></pre>
    </div>
  );
}

export function Renderer({ content, currentPath, knownPaths, unloadedDirs }: RendererProps): JSX.Element {
  const navigate = useNavigate();
  const isKnown = useMemo(() => knownPredicate(knownPaths, unloadedDirs ?? []), [knownPaths, unloadedDirs]);
  return (
    <div className="markdown-view" lang="zh-Hans">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeSanitize, rehypeHighlight]}
        components={{
          a: ({ href, children, ...rest }) => {
            if (typeof href !== "string") return <span>{children}</span>;
            const resolved = resolveLink({ currentFile: currentPath, href, isKnown });
            if (resolved.kind === "external") return <a href={resolved.href} target="_blank" rel="noopener noreferrer" {...rest}>{children}</a>;
            if (resolved.kind === "anchor") return <a href={resolved.hash} {...rest}>{children}</a>;
            if (resolved.kind === "internal") {
              const target = `/file/${encodeURIComponent(resolved.path)}${resolved.hash ?? ""}`;
              return <a href={target} onClick={(e) => { e.preventDefault(); navigate(target); }}>{children}</a>;
            }
            return <BrokenLink href={resolved.href} title={resolved.title}>{children}</BrokenLink>;
          },
          pre: ({ children }) => <CopyableCode>{children}</CopyableCode>,
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
