import { useState } from "react";

// 审查页共用的小文字组件：行内 `代码`、长文截断展开（审查大类页与问题清单页共用）。

/** 行内 `代码` 渲染成 <code>，其余原样。 */
export function Inline({ text }: { text: string }): JSX.Element {
  return <>{text.split(/(`[^`]+`)/).map((p, i) => p.startsWith("`") && p.endsWith("`") && p.length > 2 ? <code key={i}>{p.slice(1, -1)}</code> : p)}</>;
}

export function Clip({ text, max = 70 }: { text: string; max?: number }): JSX.Element {
  const [open, setOpen] = useState(false);
  if (text.length <= max) return <Inline text={text} />;
  return <>{open ? <Inline text={text} /> : `${text.replace(/`/g, "").slice(0, max)}…`}
    <button type="button" className="rl-more" onClick={() => setOpen(!open)}>{open ? "收起" : "展开"}</button></>;
}
