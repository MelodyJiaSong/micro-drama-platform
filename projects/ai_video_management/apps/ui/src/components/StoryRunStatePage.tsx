import { StoryRunPage } from "./StoryRunPage";
import { Notes } from "./StoryRunDisplay";

export function StoryRunStatePage(): JSX.Element {
  return <StoryRunPage document="state">{({ run: shown }) => <section><h2>候选状态变化 <span className="story-run-count">产出 · Transient</span></h2>
            <p className="story-run-muted">仅属于本次 run，不自动写成 EP1 已发生的状态；选用正文草稿也不代表这些变化已被确定。</p>
            {shown.candidate.title ? <h3>{shown.candidate.title}</h3> : null}
            <Notes values={shown.candidate.state_changes} empty="尚未记录状态变化。" />
          </section>}</StoryRunPage>;
}
