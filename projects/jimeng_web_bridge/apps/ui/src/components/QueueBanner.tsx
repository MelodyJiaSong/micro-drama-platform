import { Link } from "react-router-dom";
import { useSession } from "../context/SessionContext";
import { label } from "../labels";

export function QueueBanner() {
  const session = useSession().resource.data;
  const paused = session?.queues.filter((queue) => queue.state === "paused") ?? [];
  if (paused.length === 0) return null;
  return (
    <div role="alert" className="queue-banner">
      {paused.map((queue) => {
        const hint = label.queuePauseHint(queue.reason);
        return (
          <p key={queue.backend}>
            <span aria-hidden="true">⏸ </span>
            <strong>{label.backend(queue.backend)} 队列已暂停</strong>：{label.reason(queue.reason)}
            {hint ? `。${hint}` : ""}
          </p>
        );
      })}
      <p className="banner-links">
        <Link to="/">前往会话页恢复队列</Link>
        <Link to="/queue">前往队列看板</Link>
      </p>
    </div>
  );
}
