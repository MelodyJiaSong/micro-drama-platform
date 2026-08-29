import { useEffect, useState } from "react";
import { api } from "../api";

const SCENE_RE = /^\d+-\d+\s+[日夜]\s+[内外]\s+/;
const DIALOGUE_RE = /^(?!△)([^：（【\s]{1,12})(（[^）]*）)?\s*：/;

function classifyScriptLine(line: string): string {
  if (SCENE_RE.test(line)) return "sc-scene";
  if (/^第\d+集：/.test(line)) return "sc-ep";
  if (line.startsWith("分集大纲：")) return "sc-outline";
  if (line === "正文：") return "sc-ep";
  if (line.startsWith("人物：")) return "sc-cast";
  if (line.startsWith("△")) return "sc-action";
  if (line.startsWith("【")) return "sc-insert";
  const m = DIALOGUE_RE.exec(line);
  if (m) {
    if ((m[2] ?? "").includes("内心独白") || m[1] === "旁白" || (m[2] ?? "").includes("旁白")) return "sc-os";
    return "sc-line";
  }
  return "sc-plain";
}

function ScriptView(props: { content: string }) {
  return (
    <div className="artifact script-view">
      {props.content.split("\n").map((line, i) => (
        <div key={i} className={line.trim() ? classifyScriptLine(line) : "sc-blank"}>
          {line || " "}
        </div>
      ))}
    </div>
  );
}

export function ArtifactView(props: { relPath: string; episodeRelDir: string; onBack: () => void }) {
  const [content, setContent] = useState<string>("");
  const [editing, setEditing] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    api.artifact(props.relPath).then((r) => setContent(r.content)).catch((e) => setMessage(String(e)));
  }, [props.relPath]);

  const save = () =>
    api.editArtifact(props.episodeRelDir, props.relPath, content)
      .then((r: any) => setMessage(`已保存（旧版本：${r.versioned_as}${r.needs_recompose ? "；已标记需重新合成" : ""}）`))
      .catch((e) => setMessage(String(e)));

  return (
    <div data-view="artifact">
      <div className="toolbar">
        <button className="secondary" onClick={props.onBack}>← 返回</button>
        <button className="secondary" onClick={() => setEditing(!editing)}>{editing ? "预览" : "编辑"}</button>
        {editing && <button onClick={save}>保存（自动存版本）</button>}
      </div>
      <h2>{props.relPath}</h2>
      {editing ? (
        <textarea className="editor" value={content} onChange={(e) => setContent(e.target.value)} />
      ) : props.relPath.endsWith("script.md") ? (
        <ScriptView content={content} />
      ) : (
        <pre className="artifact">{content}</pre>
      )}
      {message && <p className="notice">{message}</p>}
    </div>
  );
}
