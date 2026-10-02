# -*- coding: utf-8 -*-
"""把 sk2 每张人物卡的 turntable prompt 送进即梦 image2video，出 4 秒建立视频。

立绘定**脸**，turntable 定**体型 + 服装 + 随身物 + 站姿 + 声音**；两者一起喂 Seedance 人物 entity
（rule 12.5 / `ai_video.md` §22.2）。prompt 由 `gen_turntables_sk2.py` 写进卡里，本文件只负责出片。

为什么走官方 `dreamina` CLI 而不是 ElevenLabs
--------------------------------------------
ElevenLabs 的 ByteDance 通道是 **Enterprise-only**（本账号 Pro，报 `model_access_denied`），
而即梦是字节自家产品、CLI 已在本机登录，直连即可（2026-09-19 实测，见 `ai_video.md` §25）。

用法（仓库根目录）：
    python tools/gen_turntable_videos_sk2.py              # 全部（跳过已存在的）
    python tools/gen_turntable_videos_sk2.py --only c31,c24
    python tools/gen_turntable_videos_sk2.py --force      # 已存在也重出
    python tools/gen_turntable_videos_sk2.py --dry-run    # 只打印要发什么，不花积分

纪律
----
· **串行**：即梦有并发上限（实测 `ret=1310 ExceedConcurrencyLimit`），一次只跑一条。
· **断点续跑**：已有 `c{N}-2.mp4` 默认跳过，中断后重跑不会重复花积分。
· 一条视频 **75 积分**（实测）；跑之前打印余额，不足就停。
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent.parent
CHARS = REPO / "ai_videos" / "shikong_lvxing" / "sk2" / "2_世界观人设" / "characters"
CLI = Path.home() / "bin" / "dreamina.exe"

MODEL = "seedance2.0"
DURATION = 4              # rule 12.5：turntable 固定 4 秒
RESOLUTION = "720p"
CREDIT_PER_CLIP = 75
POLL_EVERY = 10
POLL_MAX = 900            # 15 分钟还没好就判失败，继续下一条
DROP = ("参考:", "参考用法:")


def cli(*args: str, timeout: int = 300) -> dict | None:
    p = subprocess.run([str(CLI), *args], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=timeout)
    raw = (p.stdout or "") + (p.stderr or "")
    i = raw.find("{")
    if i < 0:
        return None
    try:
        return json.loads(raw[i:raw.rfind("}") + 1])
    except json.JSONDecodeError:
        return None


def credits() -> int:
    d = cli("user_credit", timeout=60) or {}
    return int(d.get("total_credit", 0))


def cards() -> list[tuple[str, Path, Path, str]]:
    """[(key, 立绘 png, 落点 mp4, prompt)]，按 key 排序。"""
    out = []
    for d in sorted(CHARS.iterdir()):
        if not d.is_dir():
            continue
        md = d / (d.name + ".md")
        if not md.exists():
            continue
        key = d.name.split("_")[0]
        png = d / f"{key}-1.png"
        if not png.exists():
            print(f"· {key} 没有立绘 {png.name}，跳过")
            continue
        m = re.search(r"```text\n(" + key + r"-2_.*?)```", md.read_text(encoding="utf-8"), re.S)
        if not m:
            print(f"· {key} 卡里没有 turntable prompt，跳过")
            continue
        body = "\n".join(l for l in m.group(1).split("\n")[1:]
                         if not l.startswith(DROP)).strip()
        out.append((key, png, d / f"{key}-2.mp4", body))
    return sorted(out, key=lambda x: int(x[0][1:]))


LEDGER = CHARS / ".turntable_jobs.json"


def ledger(sid: str | None = None, key: str | None = None) -> dict[str, str]:
    """submit_id -> 角色键。提交时写，`--harvest` 时读。

    为什么需要它：视频生成比轮询上限慢是常态，超时 ≠ 没生成——积分已经扣了、
    服务端也照常出片，缺的只是「谁去取」。没有账本就认不出哪条是谁的。
    """
    d = {}
    if LEDGER.exists():
        try:
            d = json.loads(LEDGER.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            d = {}
    if sid and key:
        d[sid] = key
        LEDGER.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    return d


def rebuild_ledger() -> dict[str, str]:
    """账本缺失时，按 **prompt 回显** 反查每个任务属于谁。

    `query_result` 会把提交时的 prompt 原样回显，而每张卡的 turntable prompt 是唯一的，
    所以拿盘上的 prompt 前 60 字去匹配就能认回来——不必依赖提交时有没有记账。
    （这条是被一次真实事故逼出来的：首批 17 条是用加账本之前的脚本起的。）
    """
    tasks = cli("list_task", timeout=180)
    if not isinstance(tasks, list):
        p = subprocess.run([str(CLI), "list_task"], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=180)
        raw = (p.stdout or "") + (p.stderr or "")
        i = raw.find("[")
        tasks = json.loads(raw[i:raw.rfind("]") + 1]) if i >= 0 else []
    heads = {key: prompt[:60] for key, _png, _dst, prompt in cards()}
    found = {}
    for t in tasks:
        if t.get("gen_task_type") != "image2video":
            continue
        sid = t.get("submit_id")
        if not sid:
            continue
        r = cli("query_result", f"--submit_id={sid}", timeout=120) or {}
        pr = (r.get("prompt") or "").replace("\r", "")
        for key, head in heads.items():
            if head and head[:40] in pr:
                found[sid] = key
                break
    for sid, key in found.items():
        ledger(sid, key)
    print(f"账本重建：认回 {len(found)} 条")
    return ledger()


def harvest() -> None:
    """把账本里已经 success、但本地还没落盘的视频收回来。"""
    jobs = ledger()
    cards_n = len(cards())
    if len(jobs) < cards_n:
        # 账本不全就重建：旧版脚本提交的那些没记账，但 prompt 回显认得出来
        print(f"账本 {len(jobs)} 条 < 角色 {cards_n} 个，按 prompt 回显重建…")
        jobs = rebuild_ledger()
    if not jobs:
        print("没有可补收的任务")
        return
    got = miss = 0
    for sid, key in jobs.items():
        d = next((p for p in CHARS.iterdir() if p.is_dir() and p.name.split("_")[0] == key), None)
        if not d:
            continue
        dst = d / f"{key}-2.mp4"
        if dst.exists():
            continue
        r = cli("query_result", f"--submit_id={sid}", timeout=120) or {}
        if r.get("gen_status") != "success":
            print(f"· {key} {sid[:8]} 还是 {r.get('gen_status')}")
            miss += 1
            continue
        vids = (r.get("result_json") or {}).get("videos") or []
        url = vids[0].get("video_url") if vids else None
        if not url:
            print(f"· {key} success 但没有 url")
            miss += 1
            continue
        kb = download(url, dst) // 1024
        print(f"OK {key} 补收 {kb} KB")
        got += 1
    print(f"\n补收：成功 {got} · 仍缺 {miss}")


def download(url: str, dst: Path) -> int:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=300) as r, dst.open("wb") as f:
        while chunk := r.read(1 << 20):
            f.write(chunk)
    return dst.stat().st_size


def one(key: str, png: Path, dst: Path, prompt: str, dry: bool) -> str:
    if dry:
        print(f"  [dry] {key} image={png.name} prompt={len(prompt)} 字符")
        return "dry"
    sub = cli("image2video", "--image", str(png), f"--prompt={prompt}",
              "--duration", str(DURATION), "--video_resolution", RESOLUTION,
              "--model_version", MODEL, "--poll", "0", timeout=600)
    sid = (sub or {}).get("submit_id")
    if not sid:
        return f"提交失败：{str(sub)[:120]}"
    ledger(sid, key)                      # 记账本：轮询超时后还能补收

    waited = 0
    while waited < POLL_MAX:
        time.sleep(POLL_EVERY)
        waited += POLL_EVERY
        r = cli("query_result", f"--submit_id={sid}", timeout=120) or {}
        st = r.get("gen_status")
        if st == "success":
            vids = (r.get("result_json") or {}).get("videos") or []
            url = vids[0].get("video_url") if vids else None
            if not url:
                return f"成功但没拿到 url：{str(r)[:120]}"
            kb = download(url, dst) // 1024
            return f"OK {kb} KB（{waited}s）"
        if st == "fail":
            return f"生成失败：{str(r.get('fail_reason'))[:160]}"
    return f"超时 {POLL_MAX}s（submit_id={sid}，可用 query_result 手查）"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="", help="逗号分隔的 cNN")
    ap.add_argument("--force", action="store_true", help="已存在也重出")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--harvest", action="store_true",
                    help="不提交新任务，只把账本里已生成好的视频收回来")
    args = ap.parse_args()

    if args.harvest:
        harvest()
        return

    keep = {x.strip() for x in args.only.split(",") if x.strip()}
    todo = [c for c in cards() if not keep or c[0] in keep]
    if not args.force:
        todo = [c for c in todo if not c[2].exists()]

    if not args.dry_run:
        bal = credits()
        need = len(todo) * CREDIT_PER_CLIP
        print(f"余额 {bal} 积分；本批 {len(todo)} 条 × {CREDIT_PER_CLIP} = {need}")
        if bal < need:
            print(f"⚠️ 余额不足，只会跑到用完为止")

    ok = fail = 0
    for i, (key, png, dst, prompt) in enumerate(todo, 1):
        print(f"[{i}/{len(todo)}] {key} …", flush=True)
        res = one(key, png, dst, prompt, args.dry_run)
        print(f"        {res}", flush=True)
        if res.startswith("OK") or res == "dry":
            ok += 1
        else:
            fail += 1
    print(f"\n合计：成功 {ok} · 失败 {fail}")


if __name__ == "__main__":
    main()
