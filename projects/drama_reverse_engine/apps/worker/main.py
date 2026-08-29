from __future__ import annotations

import argparse
import time
import uuid

from apps.api.container import Container
from libs.common.enums import PipelineStage


def main() -> None:
    parser = argparse.ArgumentParser(description="drama_reverse_engine pipeline worker")
    parser.add_argument("--poll-seconds", type=float, default=5.0)
    parser.add_argument("--once", action="store_true", help="single scan pass (for smoke tests)")
    args = parser.parse_args()

    container = Container()
    worker_id = f"worker-{uuid.uuid4().hex[:8]}"
    states_r = container.state_reader()
    states_w = container.state_writer()
    pipeline = container.pipeline_command()
    print(f"[{worker_id}] scanning workspace…")

    while True:
        progressed = False
        for drama_id in states_r.list_drama_ids():
            for ep_dir in states_r.list_episode_dirs(drama_id):
                state = states_r.read(ep_dir) or {}
                if (state.get("stage") == PipelineStage.DONE.value or state.get("failed_reason")
                        or state.get("gate_hold")):
                    continue
                if not states_w.try_claim(ep_dir, worker_id):
                    continue
                try:
                    states_w.heartbeat(ep_dir)
                    new_state = pipeline.step(drama_id, ep_dir)
                    progressed = True
                    print(f"[{worker_id}] {ep_dir} -> {new_state.get('stage')}"
                          + (f" FAILED: {new_state.get('failed_reason')}" if new_state.get("failed_reason") else ""))
                finally:
                    states_w.release(ep_dir)
        if args.once:
            break
        if not progressed:
            time.sleep(args.poll_seconds)


if __name__ == "__main__":
    main()
