/** 「Demo 定版」标记（follow-up 315）：人物的 demo 已定版。发布文案没对上定版成片时标记变成警示色并写明。 */
import { demoStatusTitle, publishReady, type DemoStatus } from "../lib/demoStatus";

export function DemoFinalBadge({ status, long }: { status: DemoStatus | undefined; long?: boolean }): JSX.Element | null {
  if (!status) return null;
  const ready = publishReady(status);
  const label = long
    ? `Demo 定版 v${status.version}${ready ? " · 发布文案已就绪" : status.publish_state === "missing" ? " · 缺发布文案" : " · 发布文案待更新"}`
    : ready ? "定版" : "定版 · 文案待补";
  return <small className={`demo-final-badge${ready ? "" : " needs-publish"}`} title={demoStatusTitle(status)}
    aria-label={`Demo 定版 v${status.version}${ready ? "" : "，发布文案未就绪"}`}>
    ✓ {label}
  </small>;
}
