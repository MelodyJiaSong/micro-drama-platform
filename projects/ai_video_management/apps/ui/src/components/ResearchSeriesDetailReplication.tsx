/** 详情页「翻拍流程」子页：单集工时 → 工具栈（标出闲置的那几件）→ 栈匹配 →
 * 卡点 → 一个人怎么做出一集的分步流程。这是全模块最可执行的一页。 */
import { Rich } from "./ResearchText";
import type { ResearchReplication } from "../lib/researchApi";

export interface ResearchSeriesDetailReplicationProps {
  replication: ResearchReplication;
}

const SCORE_LABEL: Record<number, string> = {
  5: "极易 · 单人半天",
  4: "容易 · 单人 1-2 天",
  3: "中等 · 需搭流水线",
  2: "偏难 · 手工量大",
  1: "很难 · 接近团队活",
};

type ToolKind = "idle" | "add" | "have" | "plain";

const KIND_LABEL: Record<ToolKind, string> = {
  idle: "闲置",
  add: "需新增",
  have: "已有",
  plain: "",
};

interface ParsedTool {
  kind: ToolKind;
  head: string;
  tail: string;
}

/** 工具条目形如「Claude（已有）——…」「【完全用不上】Blender、Cascadeur」，
 * 前缀的方括号标签或括号里的「已有 / 需新增」决定它归哪一类。 */
function parseTool(raw: string): ParsedTool {
  const tag = /^【([^】]*)】/.exec(raw)?.[1] ?? "";
  const cut = raw.indexOf("——");
  const head = (cut >= 0 ? raw.slice(0, cut) : raw).trim();
  const tail = cut >= 0 ? raw.slice(cut + 2).trim() : "";
  let kind: ToolKind = "plain";
  if (/用不上|用不到|不用|零使用/.test(tag)) kind = "idle";
  else if (/必须|新买|新增|补/.test(tag)) kind = "add";
  else if (/已有/.test(head)) kind = "have";
  else if (/需新增|需要新买|必须买/.test(head)) kind = "add";
  return { kind, head, tail };
}

export function ResearchSeriesDetailReplication({
  replication,
}: ResearchSeriesDetailReplicationProps): JSX.Element {
  const tools = replication.tools.map(parseTool);
  const idle = tools.filter((t) => t.kind === "idle").length;
  const add = tools.filter((t) => t.kind === "add").length;

  return (
    <div className="research-detail-panel">
      <div className="research-detail-hours">
        <span className="research-detail-hours-label">单集工时</span>
        <p className="research-detail-prose"><Rich text={replication.hours_per_episode} /></p>
        <div className="research-detail-score">
          <span className="research-detail-scoredots" aria-hidden="true">
            {[1, 2, 3, 4, 5].map((n) => (
              <span
                key={n}
                className={n <= replication.score ? "research-detail-dot research-detail-dot-on" : "research-detail-dot"}
              />
            ))}
          </span>
          <span>翻拍易度 {replication.score}/5 · {SCORE_LABEL[replication.score] ?? "—"}</span>
        </div>
      </div>

      <section className="research-block">
        <h4>
          工具栈 · {tools.length} 件
          <span className="muted">
            {add > 0 ? ` · 需新增 ${add} 件` : ""}
            {idle > 0 ? ` · 闲置 ${idle} 件` : ""}
          </span>
        </h4>
        <ul className="research-detail-tools">
          {tools.map((t, i) => (
            <li key={i} className={`research-detail-tool research-detail-tool-${t.kind}`}>
              {KIND_LABEL[t.kind] !== "" ? (
                <span className="research-detail-tool-badge">{KIND_LABEL[t.kind]}</span>
              ) : (
                <span className="research-detail-tool-badge research-detail-tool-badge-blank" aria-hidden="true" />
              )}
              <span className="research-detail-tool-text">
                <b className="research-detail-tool-head"><Rich text={t.head} /></b>
                {t.tail !== "" ? (
                  <span className="research-detail-tool-tail"><Rich text={t.tail} /></span>
                ) : null}
              </span>
            </li>
          ))}
        </ul>
      </section>

      <section className="research-block">
        <h4>和现有栈的匹配</h4>
        <p className="research-detail-prose"><Rich text={replication.stack_fit} /></p>
      </section>

      <section className="research-block">
        <h4>卡点</h4>
        <p className="research-blockers research-detail-prose"><Rich text={replication.blockers} /></p>
      </section>

      <section className="research-block">
        <h4>一个人怎么做出一集 · {replication.how_to.length} 步</h4>
        <ol className="research-detail-steps">
          {replication.how_to.map((step, i) => (
            <li key={i}>
              <span className="research-detail-stepbody"><Rich text={step} /></span>
            </li>
          ))}
        </ol>
      </section>
    </div>
  );
}
