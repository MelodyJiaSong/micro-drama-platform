import { useState } from "react";
import type { StoryRun } from "../lib/storyRuns";
import { StoryRunPage } from "./StoryRunPage";
import { RunIoLinks } from "./StoryRunItemPage";
import { Frame, Notes, Sources, Evidence, RUN_STATUS as STATUS } from "./StoryRunDisplay";

export function StoryRunInputPage(): JSX.Element {
  return <StoryRunPage document="input">{({ run }) => <Input key={run.run_id} shown={run} />}</StoryRunPage>;
}
function Input({ shown }: { shown: StoryRun }): JSX.Element {
  const [notice, setNotice] = useState("");
  const raw = JSON.stringify(shown.input, null, 2);
  const copy = (value: string, message: string): void => {
    void navigator.clipboard.writeText(value).then(() => setNotice(message)).catch(() => setNotice("复制失败，请手动选择文本。"));
  };
  const download = (): void => {
    const url = URL.createObjectURL(new Blob([raw], { type: "application/json;charset=utf-8" }));
    const link = document.createElement("a"); link.href = url; link.download = `${shown.run_id}-input.json`; link.click(); URL.revokeObjectURL(url);
  };
  return <>{notice ? <p role="status">{notice}</p> : null}<RunIoLinks run={shown} kind="input" /><section><h2>输入快照 <span className="story-run-count">本次运行冻结版本</span></h2><p className="story-run-prose">{shown.input.brief || "未记录故事方向"}</p><Frame frame={shown.input.frame} />
            <h3>本次假设</h3><Notes values={shown.input.assumptions} empty="没有额外假设。" />
            <p className="story-run-muted">长期事实只取明确选用的来源；本轮假设、候选正文、候选状态变化与意见均属于本次运行。</p>
            <Sources label="共享事实来源 · Persistent 源 / 本 run 冻结版本" values={shown.input.sources} />
            <Evidence label="此前已确定集的状态输入" value={shown.input.prior_accepted_state ?? []} />
            <Sources label="共享流程规则 · Persistent 源 / 本 run 冻结版本" values={shown.input.rules} />
            {shown.input.criteria?.length ? <Evidence label="本次判断标准" value={shown.input.criteria} /> : null}
            <Evidence label="本次输入与其他运行的隔离边界" value={shown.input.independence} />
            <details className="story-run-detail"><summary>输入指纹</summary><code>{shown.input.input_hash}</code></details>
          </section><><section><h2>历史文件登记</h2><p className="story-run-muted">原始登记可能包含后续整理文件，不代表它们都用于本次生成。实际采用范围见上方输入与规则清单。</p>
            {!shown.artifacts.length ? <p>尚未登记文件。</p> : <div className="story-run-table-scroll"><table className="story-run-files" aria-label="历史文件登记"><thead><tr><th>文件</th><th>类别</th><th>范围与生命周期</th><th>状态</th></tr></thead>
              <tbody>{shown.artifacts.filter(item => item.kind === "input").map(item => <tr key={item.id}><td><strong>{item.name}</strong><code>{item.path}</code>
                {item.sha256 ? <details><summary>SHA256</summary><code>{item.sha256}</code></details> : null}</td>
                <td>{{ input: "输入", output: "产出", process: "过程" }[item.kind] || item.kind}</td>
                <td>{{ run: "本次 run · Transient，历史留存", shared: "共享源 · Persistent，跨 run 复用", canonical: "故事工作区 · Persistent，是否确定见状态" }[item.scope] || item.scope}</td>
                <td>{STATUS[item.status || ""] || item.status || "未记录"}</td></tr>)}</tbody></table></div>}
          </section>
          <section><h2>完整输入快照</h2>
            <Evidence label="输入来源记录" value={shown.artifacts.filter(item => item.kind === "input")} />
            <details className="story-run-detail"><summary>原始 JSON</summary><div className="story-run-actions">
              <button type="button" onClick={() => copy(raw, "已复制输入快照。")}>复制 JSON</button>
              <button type="button" onClick={download}>下载 JSON</button></div><pre>{raw}</pre></details>
          </section></></>;
}
