# -*- coding: utf-8 -*-
"""每次生成一个「条」目录（follow-up 230）：视频、生成记录、当时的 prompt 与审核放在一起。

    python tools/shot_take.py submit <集目录> <镜头key> [<镜头key> …]               # 依次提交 → 查询 → 下载建条目录（会扣积分，只在用户决定生成后跑）
    python tools/shot_take.py poll   <集目录> <镜头key> <submit_id> [--credits N]   # 查询直到出结果，下载并建条目录
    python tools/shot_take.py record <集目录> <镜头key> <submit_id> --video <已下载的视频> [--credits N]

条目录 ＝ `{镜头目录}/renders/{YYYYMMDD-HHMMSS}_{submit_id 前 8 位}/`：
    {镜头key}_{原文件名}.mp4   生成的视频（文件名带镜头 key，导入与选条都认它）
    generation.json            submit_id、模型、时长、比例、分辨率、积分、时间、参考清单（每个文件的 key 与 sha256）
    prompt.txt                 提交时的 prompt 原文（资料包里填好上传编号的那一份）
    review.md                  审核：Vision / 对的 / 不对的 / 结论 / 怎么看的。先写待审核模板，看片后填写（Vision 一项 2026-10-12 起必填，follow-up 249）
提交与查询都经 `tools/service_call.py` 先记请求日志；`submit` 只在用户决定生成后运行（生成视频永远人点）。
提交用资料包 `upload/` 里的副本、绝对路径（follow-up 229 实测：相对路径传不上，大文件在 VPN 下超时）；
上传阶段失败不扣费，最多重试 UPLOAD_RETRIES 次；回执带 submit_id 就不再重提（重提会重复扣费）。
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
from tools import shot_pack  # noqa: E402

REVIEW_TEMPLATE = """# 审核：{key} · {take}

状态：待审核

Vision：

## 对的

-

## 不对的

-

## 结论

（保留 / 重出 / 改分镜后重出，写清原因）

## 怎么看的

（逐秒抽帧、全分辨率局部、与参考图并排、音量；判断「没有」之前先看全分辨率）
"""


def shot_info(ep_dir: Path, key: str) -> tuple[dict, Path]:
    shots, _ = shot_pack.episode_problems(ep_dir)
    shot = next((s for s in shots if s["id"] == key), None)
    if shot is None:
        raise SystemExit("prompts.json 里没有 %s" % key)
    return shot, shot_pack.shot_dir(ep_dir, shot["scene"], key)


def make_take(ep_dir: Path, key: str, sid: str, video: Path, credits: int | None, model: str | None,
              sent: tuple[str, dict] | None = None) -> Path:
    """`sent` ＝ 提交那一刻的（prompt 原文, manifest）。等出片期间资料包可能已重编译（follow-up 231 实测 st12），
    条目录必须记提交时的版本；poll / record 补收时拿不到，才退回资料包当前版本。"""
    shot, sd = shot_info(ep_dir, key)
    pack = sd / shot_pack.PACK
    manifest = json.loads((pack / shot_pack.MANIFEST).read_text(encoding="utf-8")) if (pack / shot_pack.MANIFEST).is_file() else {}
    if sent is not None:
        manifest = sent[1]
    settings = shot_pack.es.settings(shot_pack.es.drama_root(ep_dir)).get("prompt", {})
    take = "%s_%s" % (datetime.now().strftime("%Y%m%d-%H%M%S"), sid[:8])
    folder = sd / "renders" / take
    folder.mkdir(parents=True)
    dst = folder / (video.name if key in video.name else "%s_%s" % (key, video.name))
    shutil.copyfile(video, dst)
    duration = next((int(ln[3:-1]) for ln in shot["text"].splitlines() if ln.startswith("时长：")), None)
    record = {"key": key, "take": take, "submit_id": sid, "model": model or settings.get("model", "seedance2.5"),
              "duration_s": duration, "ratio": settings.get("ratio", "16:9"), "resolution": settings.get("resolution", "720p"), "credits": credits,
              "downloaded_at": datetime.now().isoformat(timespec="seconds"), "video": dst.name,
              "request_log": (ep_dir / "request_log.md").relative_to(REPO).as_posix(),
              "prompt_sha256": manifest.get("prompt_sha256"),
              "refs": [{k: r.get(k) for k in ("tag", "key", "kind", "role", "src", "sha256")} for r in manifest.get("refs", [])]}
    (folder / "generation.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    prompt = pack / "prompt.txt"
    text = sent[0] if sent is not None else prompt.read_text(encoding="utf-8") if prompt.is_file() else shot["text"] + "\n"
    (folder / "prompt.txt").write_text(text, encoding="utf-8", newline="\n")
    (folder / "review.md").write_text(REVIEW_TEMPLATE.format(key=key, take=take), encoding="utf-8", newline="\n")
    return folder


def query(ep_dir: Path, sid: str, download_dir: Path | None) -> dict:
    cmd = [sys.executable, str(REPO / "tools" / "service_call.py"), "--target", ep_dir.relative_to(REPO).as_posix(), "--",
           "dreamina", "query_result", "--submit_id=%s" % sid]
    if download_dir is not None:
        download_dir.mkdir(parents=True, exist_ok=True)
        cmd.append("--download_dir=%s" % download_dir)
    r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace")
    try:
        return json.loads(r.stdout)
    except ValueError:
        return {"gen_status": "unparsed", "raw": (r.stdout + r.stderr)[-500:]}


UPLOAD_RETRIES = 3
DOWNLOAD_RETRIES = 3


def media_problem(video: Path, want_s: float | None = None) -> str:
    """'' when the file decodes end to end (and, if given, lasts about want_s); otherwise what is wrong.
    A download cut off mid-file still opens and reports a duration, so only a full decode catches it
    (2026-10-11: s2 st8 / st12 / st16 were truncated and recorded as takes)."""
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-f", "null", "-"], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    err = r.stderr.strip()
    if r.returncode != 0 or err:
        return "解码出错：" + (err.splitlines()[0][:160] if err else "ffmpeg rc=%d" % r.returncode)
    if want_s is not None:
        p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
                           capture_output=True, text=True)
        try:
            dur = float(p.stdout.strip())
        except ValueError:
            return "读不出时长"
        if abs(dur - float(want_s)) > 0.5:
            return "时长 %.2f 秒，应为 %s 秒" % (dur, want_s)
    return ""


PENDING = ".pending"      # renders/.pending/{submit_id}.json：提交时的 prompt 与 manifest，poll 补收时用


def pending_file(ep_dir: Path, key: str, sid: str) -> Path:
    return shot_info(ep_dir, key)[1] / "renders" / PENDING / ("%s.json" % sid)


def submit(ep_dir: Path, key: str) -> tuple[str, int | None, tuple[str, dict]] | None:
    """提交一镜：返回 (submit_id, 积分, 提交时的 (prompt, manifest))；上传阶段失败重试；其他失败返回 None。"""
    shot, sd = shot_info(ep_dir, key)
    pack = sd / shot_pack.PACK
    if shot_pack.state(pack, shot) != "ok" or (pack / shot_pack.INVALID).is_file():
        print("  ✗ %s 资料包不是最新：先跑 python tools/shot_pack.py sync" % key)
        return None
    man = json.loads((pack / shot_pack.MANIFEST).read_text(encoding="utf-8"))
    sent_text = (pack / "prompt.txt").read_text(encoding="utf-8")
    settings = shot_pack.es.settings(shot_pack.es.drama_root(ep_dir)).get("prompt", {})
    duration = next(int(ln[3:-1]) for ln in shot["text"].splitlines() if ln.startswith("时长："))
    args = [x for r in man["refs"] for x in (shot_pack.FLAG[r["kind"]], str((pack / r["upload"]).resolve()))]
    cmd = [sys.executable, str(REPO / "tools" / "service_call.py"), "--target", ep_dir.relative_to(REPO).as_posix(), "--",
           "dreamina", "multimodal2video", *args, "--prompt=%s" % sent_text.rstrip("\n"),
           "--duration=%d" % duration, "--ratio=%s" % settings.get("ratio", "16:9"), "--video_resolution=%s" % settings.get("resolution", "720p"),
           "--model_version=%s" % settings.get("model", "seedance2.5"), "--poll=0"]
    for attempt in range(1, UPLOAD_RETRIES + 1):
        r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace")
        try:
            d = json.loads(r.stdout)
        except ValueError:
            print("  ✗ %s 回执读不出：%s" % (key, (r.stdout + r.stderr)[-300:]))
            return None
        reason = d.get("fail_reason", "")
        if d.get("gen_status") != "fail":
            print("  ✓ %s 已提交 %s（积分 %s，第 %d 次）" % (key, d.get("submit_id"), d.get("credit_count"), attempt), flush=True)
            pend = pending_file(ep_dir, key, d["submit_id"])
            pend.parent.mkdir(parents=True, exist_ok=True)
            pend.write_text(json.dumps({"prompt": sent_text, "manifest": man}, ensure_ascii=False) + "\n", encoding="utf-8")
            return d["submit_id"], d.get("credit_count"), (sent_text, man)
        if "upload phase" not in reason and "upload resource" not in reason:  # apply / commit 阶段的上传失败也未扣费
            print("  ✗ %s 提交失败（非上传阶段，不重试）：%s" % (key, reason[:300]))
            return None
        print("  · %s 上传阶段失败（不扣费），重试 %d/%d：%s" % (key, attempt, UPLOAD_RETRIES, reason[-120:]), flush=True)
    return None


def wait_and_record(ep_dir: Path, key: str, sid: str, credits: int | None, model: str | None, interval: int, tries: int,
                    sent: tuple[str, dict] | None = None) -> int:
    pend = pending_file(ep_dir, key, sid)
    if sent is None and pend.is_file():
        saved = json.loads(pend.read_text(encoding="utf-8"))
        sent = (saved["prompt"], saved["manifest"])
    tmp = Path(tempfile.mkdtemp(prefix="dreamina_%s_" % sid[:8]))
    for _ in range(tries):
        d = query(ep_dir, sid, None)
        st = d.get("gen_status")
        print(time.strftime("%H:%M:%S"), key, st, (d.get("queue_info") or {}).get("queue_status", ""), d.get("fail_reason", ""), flush=True)
        if st == "success":
            videos: list[Path] = []
            want = next((float(ln[3:-1]) for ln in (sent[0] if sent else "").splitlines() if ln.startswith("时长：")), None)
            for attempt in range(1, DOWNLOAD_RETRIES + 1):  # 下载偶发超时（VPN 下 vlabvod），已扣费，只重下不重提
                query(ep_dir, sid, tmp)
                videos = sorted(p for p in tmp.rglob("*.mp4"))
                problems = [(v, media_problem(v, want)) for v in videos]
                if videos and not any(why for _, why in problems):
                    break
                for v, why in problems:          # 截断的文件删掉重下，不进条目录
                    if why:
                        print("  · %s 下载的文件不完整（%s），删掉重下" % (key, why), flush=True)
                        v.unlink(missing_ok=True)
                videos = []
                print("  · %s 下载失败，重试 %d/%d" % (key, attempt, DOWNLOAD_RETRIES), flush=True)
                time.sleep(10)
            if not videos:
                print("  ✗ 显示成功但没下载到视频：%s；稍后跑 poll %s（不会重复提交）" % (tmp, sid))
                return 1
            for v in videos:
                print("→ %s" % make_take(ep_dir, key, sid, v, credits, model, sent).relative_to(REPO).as_posix(), flush=True)
            shutil.rmtree(tmp, ignore_errors=True)
            pend.unlink(missing_ok=True)
            return 0
        if st in ("fail", "failed"):
            print(json.dumps(d, ensure_ascii=False)[:800])
            return 1
        time.sleep(interval)
    print("  ✗ %s 查询 %d 次仍未完成；稍后跑 poll %s（不会重复提交）" % (key, tries, sid))
    return 1


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="生成记录：每次生成一个条目录")
    ap.add_argument("action", choices=["submit", "poll", "record"])
    ap.add_argument("episode", type=Path)
    ap.add_argument("key")
    ap.add_argument("rest", nargs="*", help="poll / record：submit_id；submit：更多镜头 key")
    ap.add_argument("--video", type=Path)
    ap.add_argument("--credits", type=int)
    ap.add_argument("--model")
    ap.add_argument("--interval", type=int, default=60)
    ap.add_argument("--max", type=int, default=40, help="最多查询几次")
    a = ap.parse_args()
    ep_dir = a.episode.resolve()
    if a.action == "submit":
        rc = 0
        for key in [a.key, *a.rest]:
            got = submit(ep_dir, key)
            if got is None:
                rc = 1
                print("  ✗ %s 未提交，跳到下一镜" % key, flush=True)
                continue
            rc |= wait_and_record(ep_dir, key, got[0], got[1], a.model, a.interval, a.max, got[2])
        return rc
    sid = a.rest[0]
    if a.action == "record":
        print("→ %s" % make_take(ep_dir, a.key, sid, a.video.resolve(), a.credits, a.model).relative_to(REPO).as_posix())
        return 0
    return wait_and_record(ep_dir, a.key, sid, a.credits, a.model, a.interval, a.max)


if __name__ == "__main__":
    sys.exit(main())
