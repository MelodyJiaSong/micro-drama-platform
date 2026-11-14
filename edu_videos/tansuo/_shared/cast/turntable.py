"""探索系列主角的建立视频（Seedance 全能参考，收费，生成一律人点）。

    python edu_videos/tansuo/_shared/cast/turntable.py lin --dry-run   # 只打印将提交的内容
    python edu_videos/tansuo/_shared/cast/turntable.py lin             # 提交 → 轮询 → 下载 lin/turntable.mp4
    python edu_videos/tansuo/_shared/cast/turntable.py lin --harvest   # 收回超时 / 下载断线的任务（不重提）

prompt 在 `<角色>/turntable.txt`（末行「比例：画幅 X:Y，时长 N 秒」），参考图 `<角色>/portrait.png`。
每次调用经 tools/gen_turntable_videos.cli → RequestLog 先记日志（日志落 edu_videos/tansuo/_shared/request_log.md）；
提交即记账 `<角色>/.turntable_jobs.json`，账里有在途任务时不重提。
"""
import argparse
import json
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO))
from tools.gen_turntable_videos import cli, video_url, POLL_EVERY, POLL_MAX, RESOLUTION  # noqa: E402
from tools.service_request import RequestLog  # noqa: E402

SPEC = re.compile(r"画幅\s*(\d+:\d+).*?时长\s*(\d+)\s*秒")


def ledger(d: Path, sid: str | None = None) -> list[str]:
    f = d / ".turntable_jobs.json"
    jobs = json.loads(f.read_text(encoding="utf-8")) if f.exists() else []
    if sid:
        jobs.append(sid)
        f.write_text(json.dumps(jobs), encoding="utf-8")
    return jobs


def download(sid: str, d: Path) -> str:
    t0 = time.time()
    while time.time() - t0 < POLL_MAX:
        r = cli("query_result", f"--submit_id={sid}", timeout=120, target=d) or {}
        st = r.get("gen_status") if isinstance(r, dict) else None
        if st == "success" and video_url(r):
            dst, part = d / "turntable.mp4", d / "turntable.part.mp4"
            RequestLog(dst).download("dreamina", video_url(r), part, timeout=300, attempt=1)
            if dst.exists():
                dst.replace(d / f"turntable_{time.strftime('%Y%m%d-%H%M%S')}.mp4")
            part.replace(dst)
            return f"已下载 {dst}（{dst.stat().st_size // 1024} KB，{time.time() - t0:.0f}s）"
        if st == "fail":
            return f"失败：{str(r.get('fail_reason'))[:300]}"
        time.sleep(POLL_EVERY)
    return f"超时（已记账 {sid[:8]}，稍后 --harvest）"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("role", choices=["lin", "kai"])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--harvest", action="store_true")
    ap.add_argument("--model", default="seedance2.5")
    a = ap.parse_args()
    d = HERE / a.role
    if a.harvest:
        jobs = ledger(d)
        print(download(jobs[-1], d) if jobs else "账里没有任务")
        return 0
    prompt = (d / "turntable.txt").read_text(encoding="utf-8").strip()
    ratio, dur = SPEC.search(prompt).groups()
    img = d / "portrait.png"
    if not img.exists():
        raise SystemExit(f"缺立绘 {img}")
    head = f"{a.role}: {img.name} · {ratio} · {dur}s · {a.model} · {RESOLUTION} · {len(prompt)} 字"
    if a.dry_run:
        print(head + "\n" + prompt)
        return 0
    if ledger(d):
        raise SystemExit(f"{a.role} 账里已有任务 {ledger(d)[-1][:8]}：先 --harvest 收回，确需重出再手动清账")
    sub = cli("multimodal2video", "--image", str(img), f"--prompt={prompt}", f"--duration={dur}", f"--ratio={ratio}",
              f"--video_resolution={RESOLUTION}", f"--model_version={a.model}", "--poll=0", timeout=600, target=d) or {}
    sid = sub.get("submit_id") if isinstance(sub, dict) else None
    if not sid or sub.get("gen_status") == "fail":
        print(f"提交失败：{str(sub)[:300]}")
        return 1
    ledger(d, sid)
    q = (cli("query_result", f"--submit_id={sid}", timeout=120, target=d) or {}).get("queue_info") or {}
    print(f"已提交 {sid[:8]}（{head}）· priority {q.get('priority')} · 排第 {q.get('queue_idx')} / {q.get('queue_length')}", flush=True)
    print(download(sid, d))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
