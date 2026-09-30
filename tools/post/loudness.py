# -*- coding: utf-8 -*-
"""整集响度：loudnorm 两遍、linear=true，第二遍前 alimiter 兜真峰值；loudnorm 报 dynamic 即报错（不许悄悄走动态压缩）。

量原片 → 预增益把整集推到目标之上 HEAD_DB、alimiter 在 TP_TARGET 削峰 → 量削过峰的信号 → 第二遍 loudnorm 按这次实测
做纯线性增益。线性增益 ≤ 0（只降不升）峰才不会被抬回去：峰值因数高的片子（ep01 原生混音 PLR ≈ 19 dB）削峰要吃掉
1–2 LU，增益转正、真峰值越线——这时按越线量抬高预增益再量（割线法），TRIES 次还不行即报错。
LRA 目标取 max(mux_av.LOUD_LRA, 实测 LRA)：本机 ffmpeg 实测 LRA 高于目标时 linear 也退成 dynamic；线性模式不拿 LRA 做任何处理。
"""
from __future__ import annotations

import json
import math
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

import post_common as pc
import mux_av        # tools/ 下的，post_common 已把 tools/ 加进 sys.path；LOUD_* 是交付响度的唯一出处

TP_TARGET = mux_av.LOUD_TP - mux_av.LOUD_CODEC_HEADROOM     # AAC 交付编码会把真峰值再抬一点，PCM 先压到这里
LIMIT = 10 ** (TP_TARGET / 20)                               # alimiter 的 limit 是线性幅度
HEAD_DB = 1.0
MARGIN_DB = 0.1
STEP_MAX_DB = 3.0
TRIES = 4
LRA_MAX = 50.0                                               # loudnorm 的 LRA 上限
LINEAR = "linear"
LIMITER = f"alimiter=limit={LIMIT:.6f}:level=0:latency=1"
STATS_RE = re.compile(r"\{[^{}]*\"input_i\"[^{}]*\}")
PARAMS = {"I": mux_av.LOUD_I, "TP": TP_TARGET, "LRA": mux_av.LOUD_LRA, "head": HEAD_DB, "margin": MARGIN_DB, "tries": TRIES,
          "step_max": STEP_MAX_DB, "lra_max": LRA_MAX, "limiter": LIMITER, "ar": pc.AR}   # 出片戳用：改了哪一个都要重出


@dataclass(frozen=True)
class Plan:
    af: str                  # 第二遍（套用）的 -af：预增益 + alimiter + loudnorm(linear) + 重采样
    pre_db: float            # 预增益
    raw: dict[str, str]      # 原片实测（loudnorm 第一遍 JSON）


def stats(err: str, what: str) -> dict[str, str]:
    """ffmpeg stderr 里 loudnorm 最后打印的那段 JSON。"""
    found = STATS_RE.findall(err)
    if not found:
        raise SystemExit(f"loudnorm 没打印统计（{what}）：{err[-500:]}")
    return json.loads(found[-1])


def measure(src: Path, pre: str = "") -> dict[str, str]:
    af = (pre + "," if pre else "") + f"loudnorm=I={mux_av.LOUD_I}:TP={TP_TARGET}:LRA={mux_av.LOUD_LRA}:print_format=json"
    r = subprocess.run([pc.FFMPEG, "-hide_banner", "-nostats", "-i", str(src), "-map", "0:a:0", "-vn", "-af", af,
                        "-f", "null", "-"], capture_output=True)
    err = r.stderr.decode("utf-8", "replace")
    if r.returncode != 0:
        raise SystemExit(f"量响度失败（{src.name}）：{err[-800:]}")
    s = stats(err, src.name)
    if s["input_i"] == "-inf":
        raise SystemExit(f"{src.name} 的音轨是静音，没法归一")
    return s


def _pre(db: float) -> str:
    return f"volume={db:.2f}dB,{LIMITER}"


def _over(m: dict[str, str]) -> float:
    """按这次实测做线性增益后，真峰值高出 TP_TARGET 多少（≤ 0 才走得了 linear，与 loudnorm 自己的判据相同）。"""
    return float(m["input_tp"]) + mux_av.LOUD_I - float(m["input_i"]) - TP_TARGET


def plan(src: Path) -> Plan:
    raw = measure(src)
    i0 = float(raw["input_i"])
    tried: list[tuple[float, float]] = []            # （head, 越线量）
    head = HEAD_DB
    for _ in range(TRIES):
        pre_db = mux_av.LOUD_I - i0 + head
        m = measure(src, _pre(pre_db))
        over = _over(m)
        if over <= 0:
            lra = min(LRA_MAX, max(mux_av.LOUD_LRA, math.ceil(float(m["input_lra"]) * 10) / 10))
            af = (f"{_pre(pre_db)},loudnorm=I={mux_av.LOUD_I}:TP={TP_TARGET}:LRA={lra:g}:measured_I={m['input_i']}:"
                  f"measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:"
                  f"offset={m['target_offset']}:linear=true:print_format=json,aresample={pc.AR}")
            return Plan(af, pre_db, raw)
        tried.append((head, over))
        slope = -1.0             # 越线量随 head 下降、斜率在 (−1, 0)：削峰吃掉的响度跟着 head 涨
        if len(tried) > 1:
            (h0, o0), (h1, o1) = tried[-2:]
            slope = min((o1 - o0) / (h1 - h0), -0.05)
        head += min(STEP_MAX_DB, -over / slope + MARGIN_DB)
    raise SystemExit(f"{src.name}：原片 {i0:.1f} LUFS、真峰值 {raw['input_tp']} dBTP（峰值因数 {float(raw['input_tp']) - i0:.1f} dB）——"
                     f"alimiter 在 {TP_TARGET:g} dBTP 削峰 {TRIES} 次都凑不出线性增益（"
                     + "、".join(f"预增益多给 {h:.2f} dB 仍越线 {o:.2f} dB" for h, o in tried)
                     + "）：先查混音里哪一段峰特别高（音效 / BGM），不许退成 dynamic")


def check(err: str, what: str) -> dict[str, str]:
    """套用那一遍 loudnorm 打印的 JSON：normalization_type 不是 linear 即报错。"""
    s = stats(err, what)
    if s.get("normalization_type") != LINEAR:
        raise SystemExit(f"{what}：loudnorm 实际走了 {s.get('normalization_type')!r}（要 {LINEAR}）——统计 {s}。"
                         "先查混音里过响的音效 / BGM 与长静场（LRA 过大），改完重跑 finish_ep")
    return s
