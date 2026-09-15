# -*- coding: utf-8 -*-
"""把 S 档 previz 的机位按 shot md 的 `景别档` 反解到位（rule 4h ②／③：数值只写 TOML，审计左移）。

问题：`景别档: {起幅景别}{人占画高} → {落幅景别}{人占画高}` 是排镜阶段的第一约束（切口判定与 K31 都用它），
但 S 档 previz 的机位是手写坐标，没人回头对账——2026-09-15 实测 29 个 S 档镜里只有 3 个两端都落在 spec 的
±40% 内，最离谱的差 18 倍（人几乎贴在镜头上）。白模是给 Seedance 的运动与构图参考，框错了就等于没给参考。

办法：`人占画高 ∝ 焦距 / 距离`。本工具读 shot md 的 spec 与上一次渲染的量测报告
（`shotNN_previz_report.txt`，没有就退回 `scratchpad/logs/shotNN_build.log` 里的 CAMKEY 行），
按比例改**首末两个** `[["机位"]]` 关键帧的 `焦距` 与 `位置`（中间关键帧不动）：
  · 室内（配置里有 `[["布景"]]`）**只改焦距**，夹在 14–120 mm——机位往后退会退到墙外去；
  · 室外先沿视线拉远 / 推近（最多 2.5 倍），差额再交给焦距。
夹不住的差额如实报出来（那是 md 里「50 mm 近景」与房间尺寸本身矛盾，得改分镜，不是改机位）。

用法：
    python tools/previz_frame_fix.py ai_videos/shikong_lvxing/sk1            # 只报告
    python tools/previz_frame_fix.py ai_videos/shikong_lvxing/sk1 --apply    # 写回 TOML
    python tools/previz_frame_fix.py ... --apply --shots shot07,shot09       # 只改这几镜
"""
from __future__ import annotations

import argparse
import io
import math
import os
import re
import sys
from dataclasses import dataclass

LENS_MIN, LENS_MAX = 14.0, 120.0
MOVE_MAX, MOVE_MIN = 2.5, 0.4          # 室外机位最多拉远 / 推近的倍数
TOL_LO, TOL_HI = 0.7, 1.45             # 量测 / spec 落在这个区间就算对上了
SPEC_RE = re.compile(r"景别档: \D*?([\d.]+) → \D*?([\d.]+)（机位")
CAMKEY_RE = re.compile(r"CAMKEY f=(\d+) t=([\d.]+) pos=\(([-\d.]+),([-\d.]+),([-\d.]+)\) lens=([\d.]+)"
                       r"(?: 林问 frac=([\d.]+))?")
CAM_BLOCK_RE = re.compile(r'\[\["机位"\]\]\n(?:[^\[\n][^\n]*\n|\n)*', re.M)
NUM = r"[-+]?\d+(?:\.\d+)?"


@dataclass
class Key:
    start: int
    end: int
    text: str
    t: float
    lens: float
    pos: tuple[float, float, float] | None
    look: tuple[float, float, float] | None
    same_frame: bool


def _read(path: str) -> str:
    return io.open(path, encoding="utf-8").read()


def _vec_tail(line: str) -> tuple[list[str], tuple[float, float, float]] | None:
    """`"位置" = ["布景", "客店房间", -1.0, -2.25, 1.5]` → (前缀 token 列表, 三个数)。"""
    m = re.search(r"=\s*\[(.*)\]", line)
    if m is None:
        return None
    items = [x.strip() for x in m.group(1).split(",")]
    head = [x for x in items if x.startswith('"')]
    nums = [x for x in items if not x.startswith('"')]
    if len(nums) != 3:
        return None
    try:
        return head, (float(nums[0]), float(nums[1]), float(nums[2]))
    except ValueError:
        return None


def cam_keys(cfg: str) -> list[Key]:
    keys: list[Key] = []
    for m in CAM_BLOCK_RE.finditer(cfg):
        block = m.group(0)
        t = float(re.search(r"^t = (%s)" % NUM, block, re.M).group(1)) if re.search(r"^t = ", block, re.M) else 0.0
        lens_m = re.search(r'^"焦距" = (%s)' % NUM, block, re.M)
        pos_line = re.search(r'^"位置" = .*$', block, re.M)
        look_line = re.search(r'^"看向" = .*$', block, re.M)
        pos = _vec_tail(pos_line.group(0)) if pos_line else None
        look = _vec_tail(look_line.group(0)) if look_line else None
        keys.append(Key(start=m.start(), end=m.end(), text=block, t=t,
                        lens=float(lens_m.group(1)) if lens_m else 0.0,
                        pos=pos[1] if pos else None, look=look[1] if look else None,
                        same_frame=bool(pos and look and pos[0] == look[0])))
    return keys


def measured(shot_dir: str, sid: str) -> list[tuple[int, float, float]]:
    """[(帧, 焦距, 林问占画高)]，取本镜报告或回退日志里的 CAMKEY 行。"""
    report = os.path.join(shot_dir, sid + "_previz_report.txt")
    text = ""
    if os.path.exists(report):
        text = _read(report)
    else:
        log = os.path.join(os.environ.get("PREVIZ_LOG_DIR", ""), sid + "_build.log")
        if log and os.path.exists(log):
            text = io.open(log, encoding="utf-8", errors="replace").read()
    out = []
    for m in CAMKEY_RE.finditer(text):
        if m.group(7) is None:
            continue
        out.append((int(m.group(1)), float(m.group(6)), float(m.group(7))))
    return out


def solve(ratio: float, lens: float, interior: bool) -> tuple[float, float, float]:
    """(焦距倍数 a, 机位距离倍数 b, 残差)；frac 变化 ＝ a / b，目标 a / b ＝ 1 / ratio。"""
    if interior:
        b = 1.0
    else:
        b = min(MOVE_MAX, ratio) if ratio > 1 else max(MOVE_MIN, ratio)
    a = b / ratio
    a = max(LENS_MIN / lens, min(LENS_MAX / lens, a)) if lens else a
    residual = (a / b) * ratio          # 1.0 ＝ 正好落在 spec
    return a, b, residual


def patch_block(block: str, a: float, b: float) -> str:
    def lens_sub(m: re.Match) -> str:
        return '"焦距" = %.1f' % max(LENS_MIN, min(LENS_MAX, float(m.group(1)) * a))
    out = re.sub(r'"焦距" = (%s)' % NUM, lens_sub, block)
    if abs(b - 1.0) < 1e-6:
        return out
    look = _vec_tail(re.search(r'^"看向" = .*$', out, re.M).group(0))
    pos_line = re.search(r'^"位置" = .*$', out, re.M)
    pos = _vec_tail(pos_line.group(0))
    lx, ly, lz = look[1]
    px, py, pz = pos[1]
    new = (lx + (px - lx) * b, ly + (py - ly) * b, lz + (pz - lz) * b)
    head = ", ".join(pos[0])
    body = ", ".join("%.2f" % v for v in new)
    return out.replace(pos_line.group(0), '"位置" = [%s%s%s]' % (head, ", " if head else "", body))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("drama_dir")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--shots", default="")
    ap.add_argument("--log-dir", default="", help="回退日志目录（没有 previz 报告时用）")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    if args.log_dir:
        os.environ["PREVIZ_LOG_DIR"] = args.log_dir
    only = {s.strip() for s in args.shots.split(",") if s.strip()}
    shots_root = os.path.join(args.drama_dir, "5_6_分镜与prompt", "shots")
    print("shot    spec(起→落)  量测(起→落)    动作                                    残差")
    changed = 0
    for sid in sorted(os.listdir(shots_root)):
        if not re.fullmatch(r"shot\d+", sid) or (only and sid not in only):
            continue
        d = os.path.join(shots_root, sid)
        md = os.path.join(d, sid + ".md")
        cfg_path = os.path.join(d, "previz_config.toml")
        if not (os.path.exists(md) and os.path.exists(cfg_path)):
            continue
        spec = SPEC_RE.search(_read(md))
        if spec is None:
            continue
        spec_in, spec_out = float(spec.group(1)), float(spec.group(2))
        cfg = _read(cfg_path)
        keys = cam_keys(cfg)
        if len(keys) < 2:
            print("%-7s %-12s %-14s %s" % (sid, "%.2f→%.2f" % (spec_in, spec_out), "-", "A 档引擎（占画高自解算），跳过"))
            continue
        marks = measured(d, sid)
        if not marks:
            print("%-7s %-12s %-14s %s" % (sid, "%.2f→%.2f" % (spec_in, spec_out), "-", "没有量测报告，先渲一次"))
            continue
        got_in, got_out = marks[0][2], marks[-1][2]
        interior = '[["布景"]]' in cfg
        acts, residuals = [], []
        edits: list[tuple[Key, float, float]] = []
        for label, spec_v, got_v, key in (("起", spec_in, got_in, keys[0]), ("落", spec_out, got_out, keys[-1])):
            ratio = got_v / spec_v if spec_v else 1.0
            if TOL_LO <= ratio <= TOL_HI:
                acts.append(label + ":OK")
                residuals.append(1.0)
                continue
            a, b, res = solve(ratio, key.lens, interior or not key.same_frame)
            acts.append("%s:%.0fmm→%.0fmm%s" % (label, key.lens, key.lens * a, "" if abs(b - 1) < 1e-6 else " ×%.2f距" % b))
            residuals.append(res)
            edits.append((key, a, b))
        worst = max(residuals, key=lambda r: abs(math.log(r)))
        print("%-7s %-12s %-14s %-40s %s" % (
            sid, "%.2f→%.2f" % (spec_in, spec_out), "%.2f→%.2f" % (got_in, got_out), " ".join(acts),
            "OK" if abs(math.log(worst)) < 0.2 else "%.2fx" % worst))
        if args.apply and edits:
            out = cfg
            for key, a, b in sorted(edits, key=lambda e: -e[0].start):
                out = out[:key.start] + patch_block(key.text, a, b) + out[key.end:]
            io.open(cfg_path, "w", encoding="utf-8", newline="\n").write(out)
            changed += 1
    if args.apply:
        print("\n改了 %d 个 previz_config.toml —— 逐镜重渲后再跑一遍本工具复核。" % changed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
