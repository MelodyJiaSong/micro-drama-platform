# -*- coding: utf-8 -*-
"""Generate every xianjian_yi reference image declared in the asset cards.

Scans `_series/{scenes,characters,props}/**/*.md` for fenced ```text blocks whose FIRST LINE
is a routing key (ai_video.md rule 4b-A), submits each to the official 即梦 `dreamina` CLI,
and lands the PNG next to its card as `{first line}.png` — so the prompt, the routing key and
the file stem are the same string end to end.

A card may steer one block with a `> gen:` line directly above the fence:

    > gen: ratio=16:9 res=2k model=5.0 ref=bg1_大堂/bg1-1_大堂.png

`ref` (repeatable, comma-separated) switches that block to image2image, which is how a
derivative anchor inherits the world's tone from the one free-generated anchor (rule 4e ②).

Hard rules enforced before anything is submitted, because a rejected submit costs a round
trip (it does NOT cost credits — measured 2026-09-19):
  * prompt length ≤ 1600 RAW characters, newlines included — the 即梦 server limit.
  * a block named `*-1_*` (an anchor) must also be ≥ 1500, per ai_video.md rule 4e ⑤.

Run (repo root):
  python tools/gen_images_xianjian.py --dry-run     # 只校验长度与清单，不出图不花积分
  python tools/gen_images_xianjian.py               # 生成所有缺失的图
  python tools/gen_images_xianjian.py --only bg2 c10
  python tools/gen_images_xianjian.py --force --only bg1-1
"""
from __future__ import annotations

import argparse
import json
import re
import ssl
import subprocess
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent.parent
SERIES = REPO / "ai_videos" / "xianjian_yi" / "_series"
CARD_ROOTS = ("scenes", "characters", "props")
DREAMINA = Path.home() / "bin" / "dreamina.exe"

PROMPT_MAX = 1600           # 服务端硬限，实测（ret=1046 / limited len: 1600）
ANCHOR_MIN = 1500           # rule 4e ⑤ 锚点下限
DEFAULTS = {"ratio": "16:9", "res": "2k", "model": "5.0", "out": ""}
# `> gen:` 行与围栏之间允许有空行（Markdown 里那样写更好读）
_FENCE = re.compile(r"(?:^> gen:(?P<gen>[^\n]*)\n\s*?\n?)?^```text\n(?P<body>.*?)\n^```",
                    re.M | re.S)
_KEY = re.compile(r"^[A-Za-z]+\d+(?:-\d+)?_")


@dataclass(frozen=True)
class Job:
    card: Path
    key: str
    stem: str
    prompt: str
    ratio: str
    res: str
    model: str
    refs: tuple[Path, ...]
    out: str

    @property
    def dest(self) -> Path:
        return self.card.parent / (self.out or f"{self.stem}.png")

    @property
    def is_free_anchor(self) -> bool:
        """≥1500 的下限只针对 **scenes/ 下、零参考的自由生成锚点**。

        rule 4e ⑤ 属于「场景」一节，理由是「锚点是全片视觉源头、且是唯一零参考的自由生成」。
        两类不适用：① 挂参考图继承世界基调的派生主体锚点（bg2 / bg3…），长相由参考图携带；
        ② 物件与角色锚点（props/ characters/），一件平铺道具写满 1500 字只会变成灌水。
        """
        return "-1_" in self.stem and not self.refs and "scenes" in self.card.parts


def parse_gen(raw: str | None, card: Path) -> tuple[str, str, str, tuple[Path, ...], str, bool]:
    """`skip` 标记非出图块（例如 turntable 视频 prompt）；`out=` 给落盘名与路由键不同的历史资产。"""
    opts = dict(DEFAULTS)
    refs: list[Path] = []
    skip = False
    for token in (raw or "").split():
        if token == "skip":
            skip = True
            continue
        if "=" not in token:
            continue
        k, v = token.split("=", 1)
        if k == "ref":
            refs.extend((SERIES / "scenes" / r).resolve() if not (card.parent / r).exists()
                        else (card.parent / r).resolve() for r in v.split(","))
        elif k in opts:
            opts[k] = v
    return opts["ratio"], opts["res"], opts["model"], tuple(refs), opts["out"], skip


def collect() -> list[Job]:
    jobs: list[Job] = []
    for root in CARD_ROOTS:
        for card in sorted((SERIES / root).rglob("*.md")):
            text = card.read_text(encoding="utf-8")
            for m in _FENCE.finditer(text):
                body = m.group("body")
                first = body.split("\n", 1)[0].strip()
                # 首行允许在路由键后跟说明文字；落盘名只取键那一个 token
                stem = first.split()[0].rstrip("，,。") if first else ""
                if not _KEY.match(stem):
                    continue
                ratio, res, model, refs, out, skip = parse_gen(m.group("gen"), card)
                if skip:
                    continue
                jobs.append(Job(card, stem.split("_", 1)[0], stem, body,
                                ratio, res, model, refs, out))
    return jobs


def validate(jobs: list[Job], enforced: set[str]) -> list[str]:
    problems: list[str] = []
    seen: dict[str, Path] = {}
    for j in jobs:
        n = len(j.prompt)
        tag = "✗" if j.stem in enforced else "⚠ 本轮不跑"
        if n > PROMPT_MAX:
            problems.append(f"{tag} {j.stem}: prompt {n} 字 > {PROMPT_MAX} 硬限（{j.card.name}）")
        if j.is_free_anchor and n < ANCHOR_MIN:
            problems.append(f"{tag} {j.stem}: 锚点 prompt {n} 字 < {ANCHOR_MIN} 下限（{j.card.name}）")
        if j.dest.name in seen:
            problems.append(f"✗ {j.dest.name}: 落盘名重复，另一处在 {seen[j.dest.name].name}")
        seen[j.dest.name] = j.card
        for r in j.refs:
            if not r.is_file():
                problems.append(f"{j.stem}: 参考图不存在 {r}")
    return problems


def task_ids() -> list[str]:
    """Newest-first submit_ids from `list_task`, used to recover a task whose submit call
    returned no parsable JSON."""
    res = subprocess.run([str(DREAMINA), "list_task"], capture_output=True, text=True,
                         encoding="utf-8", errors="replace")
    try:
        rows = json.loads(res.stdout[res.stdout.index("["):])
    except (ValueError, json.JSONDecodeError):
        return []
    return [str(r.get("submit_id")) for r in rows if r.get("submit_id")]


def credit() -> int:
    out = subprocess.run([str(DREAMINA), "user_credit"], capture_output=True, text=True,
                         encoding="utf-8", check=True).stdout
    return int(json.loads(out)["total_credit"])


def _payload(text: str) -> dict[str, object] | None:
    try:
        return json.loads(text[text.index("{"):])
    except (ValueError, json.JSONDecodeError):
        return None


def _url_of(payload: dict[str, object]) -> str | None:
    images = (payload.get("result_json") or {}).get("images") or []      # type: ignore[union-attr]
    return images[0]["image_url"] if images else None


def submit(job: Job, requery: int = 6) -> tuple[str | None, int]:
    """Submit, then never let a flaky poll strand a result we already paid for.

    即梦 charges at submit time, so a failed `--poll` (seen once as
    `get_history_by_ids failed: ret=1015`) burns credits and returns nothing. Whenever the
    submit call comes back without a URL we keep the submit_id and re-query it instead of
    resubmitting — resubmitting would pay twice for the same picture.
    """
    cmd = [str(DREAMINA)]
    if job.refs:
        cmd += ["image2image", "--images", ",".join(str(r) for r in job.refs)]
    else:
        cmd += ["text2image"]
    cmd += [f"--prompt={job.prompt}", f"--ratio={job.ratio}",
            f"--resolution_type={job.res}", f"--model_version={job.model}", "--poll=240"]
    before_ids = set(task_ids())
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    payload = _payload(res.stdout)
    submit_id = str(payload.get("submit_id")) if payload else None

    if payload and payload.get("gen_status") == "success":
        url = _url_of(payload)
        if url:
            return url, int(payload.get("credit_count") or 0)
    if payload and payload.get("gen_status") == "fail":
        print(f"  ! 生成失败：{str(payload.get('fail_reason'))[:220]}", flush=True)
        return None, 0
    if not submit_id:
        # CLI 有时连 JSON 都不返回（实测两次 `get_history_by_ids failed: ret=1015`），
        # 但即梦是提交即扣费——任务其实已经建起来了。拿提交前后的 list_task 差集把它找回来，
        # 这是唯一不重复付费的办法。
        print(f"  · 提交未返回 JSON（{res.stdout.strip()[:80]}），用 list_task 差集找回", flush=True)
        new_ids = [i for i in task_ids() if i not in before_ids]
        if not new_ids:
            print("  ! list_task 里没有新任务，判定为未提交（未扣费）", flush=True)
            return None, 0
        submit_id = new_ids[0]
        print(f"  · 找到 {submit_id}", flush=True)

    print(f"  · 轮询未取回结果，改用 submit_id 重查（积分已扣，不重新提交）：{submit_id}", flush=True)
    for attempt in range(1, requery + 1):
        q = subprocess.run([str(DREAMINA), "query_result", f"--submit_id={submit_id}"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        got = _payload(q.stdout)
        if got and got.get("gen_status") == "success":
            url = _url_of(got)
            if url:
                return url, int(got.get("credit_count") or 0)
        if got and got.get("gen_status") == "fail":
            print(f"  ! 生成失败：{str(got.get('fail_reason'))[:220]}", flush=True)
            return None, 0
        print(f"    重查 {attempt}/{requery} 仍在生成中 …", flush=True)
        subprocess.run([sys.executable, "-c", "import time; time.sleep(20)"], check=False)
    print(f"  ! 重查耗尽仍未完成，稍后用 dreamina query_result --submit_id={submit_id} 手动取回",
          flush=True)
    return None, 0


def download(url: str, dest: Path) -> int:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, context=ssl.create_default_context(), timeout=180) as r:
        data = r.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n" and data[:3] != b"\xff\xd8\xff":
        raise RuntimeError(f"下载内容不是图片：{dest.name}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return len(data)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--only", nargs="*", default=None)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    jobs = collect()
    if args.only:
        jobs = [j for j in jobs if any(tok in j.stem for tok in args.only)]
    todo = [j for j in jobs if args.force or not j.dest.exists()]
    problems = validate(jobs, {j.stem for j in todo})
    print(f"清单 {len(jobs)} 张")
    for p in problems:
        print(f"  {p}")
    if any(p.startswith("✗") for p in problems):
        print("先修掉 ✗ 的问题再出图（被拒的提交不扣积分，但会白跑一轮）")
        return 1
    for j in jobs:
        mark = "重生" if (args.force and j.dest.exists()) else ("待出" if j in todo else "已有")
        print(f"  [{mark}] {j.stem}  {len(j.prompt):>4}字  {j.ratio} {j.res} "
              f"{'i2i' if j.refs else 't2i'}  ← {j.card.parent.name}")
    if args.limit:
        todo = todo[: args.limit]
    if args.dry_run:
        print(f"dry-run：将生成 {len(todo)} 张，预计约 {len(todo) * 3} 积分")
        return 0
    if not todo:
        print("没有需要生成的图")
        return 0

    before = credit()
    print(f"余额 {before} 积分，开始生成 {len(todo)} 张", flush=True)
    spent_total = 0
    for i, j in enumerate(todo, 1):
        print(f"[{i}/{len(todo)}] {j.stem} ...", flush=True)
        url, spent = submit(j)
        if url is None:
            continue
        size = download(url, j.dest)
        spent_total += spent
        print(f"  ✓ {j.dest.relative_to(REPO)}  {size // 1024} KB  {spent} 积分", flush=True)
    after = credit()
    print(f"完成。报告消耗 {spent_total}，余额 {before} → {after}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
