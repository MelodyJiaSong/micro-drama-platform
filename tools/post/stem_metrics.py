# -*- coding: utf-8 -*-
"""分轨能量指标（P2 试验）：没有真值，拿对齐缓存里实测的台词区间当尺子。tools/post/stems_trial.py 调；
走 B 路线时同一套也能量 ElevenLabs Voice Isolator 的输出（把它当一条对白候选传进 evaluate）。
帧：librosa 居中分帧（FRAME / HOP，44.1 kHz 下 46 ms / 23 ms），功率取各声道平均；台词区间外让 GUARD_S 才算「台词间隙」。
能量只说「多响」、不说「是什么」：减掉的是配乐还是吼叫、撞击，看 stem_tags（独立分类器）。
*(judgment call — 删掉上一版的色度残留指标 tonal_residue：它拿 Bandit 的音乐轨当「配乐长什么样」的尺子，而 Bandit 把吼叫、
  狗头人叽喳也分进了音乐轨，于是保住这些人声的 RoFormer 反被判成「串了 98% 的配乐」（shot06）——尺子本身有偏，结论就反了。
  同理删掉 speech_in_music_r（音乐轨跟着字起伏的相关）：被分进音乐轨的吼叫本来就跟着人声起伏，分不出是串音还是误分。)*
"""
from __future__ import annotations

from dataclasses import dataclass

import librosa
import numpy as np

FRAME, HOP = 2048, 1024
GUARD_S = 0.25                  # 起音与混响尾不算间隙
MIN_FRAMES = 20                 # 少于 ~0.5 s 的样本不下结论
EPS = 1e-12

INDICATORS = {
    "speech_vs_original_db": "台词区间里候选减原声的电平：对白候选明显低于 0 说明台词被削了；去音乐候选＝台词底下被减掉了多少"
                             "（台词下面本来有响配乐时自然为负）",
    "gap_vs_original_db": "台词间隙（离任何实测台词 ≥ 0.25 s）里候选减原声：去音乐候选＝底子降了多少——降得多不等于去得好，"
                          "被当音乐扔掉的吼叫、撞击也算在里面（对照 tags.*.removed_lost）；对白候选＝间隙里还剩多少别的声音",
    "removed_in_speech_db": "（任务给的指标：台词区间里音乐轨的能量）被减掉的那条（音乐估计）在台词区间的电平减原声：越低＝台词下面几乎没有要减的，"
                            "这里分离出错的代价也越小",
    "removed_in_gap_db": "被减掉的那条在台词间隙的电平减原声：≈ 0＝间隙几乎全被当音乐扔掉",
    "sum_residual_db": "Bandit 三轨相加与原声之差的能量（相对原声）：三轨都没接住的内容。去音乐一律「原声减音乐估计」，这部分保留、不会丢",
}

Spans = list[tuple[float, float]]


def merge(spans: Spans) -> Spans:
    out: Spans = []
    for a, b in sorted(spans):
        if out and a <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out


@dataclass(frozen=True)
class Axis:
    speech: np.ndarray      # bool：帧中心落在台词区间里
    gap: np.ndarray         # bool：帧中心离任何台词 ≥ GUARD_S
    fps: float


def axis(n: int, sr: int, spans: Spans) -> Axis:
    t = librosa.frames_to_time(np.arange(1 + n // HOP), sr=sr, hop_length=HOP)
    speech = np.zeros(t.shape, bool)
    near = np.zeros(t.shape, bool)
    for a, b in spans:
        speech |= (t >= a) & (t <= b)
        near |= (t >= a - GUARD_S) & (t <= b + GUARD_S)
    return Axis(speech, ~near, sr / HOP)


def power(x: np.ndarray) -> np.ndarray:
    """x：(n, ch) → 每帧各声道平均功率。"""
    return np.mean([librosa.feature.rms(y=np.ascontiguousarray(x[:, c]), frame_length=FRAME, hop_length=HOP)[0] ** 2
                    for c in range(x.shape[1])], axis=0)


def db(p: float) -> float:
    return float(10 * np.log10(p + EPS))


def level(p: np.ndarray, mask: np.ndarray) -> float | None:
    return db(float(p[mask].mean())) if mask.sum() >= MIN_FRAMES else None


def _diff(a: float | None, b: float | None) -> float | None:
    return None if a is None or b is None else round(a - b, 2)


def evaluate(sr: int, spans: Spans, original: np.ndarray, removed: dict[str, np.ndarray], dialogue: dict[str, np.ndarray],
             bandit_parts: list[np.ndarray]) -> dict:
    """original：(n, ch)。removed：去音乐配方 → 它的音乐估计（候选＝原声减它）；dialogue：只留人声的候选；
    bandit_parts：Bandit 的三轨（sum_residual_db）。"""
    ax = axis(len(original), sr, spans)
    po = power(original)
    o_sp, o_gap = level(po, ax.speech), level(po, ax.gap)

    def vs(x: np.ndarray) -> dict[str, float | None]:
        px = power(x)
        return {"speech_vs_original_db": _diff(level(px, ax.speech), o_sp), "gap_vs_original_db": _diff(level(px, ax.gap), o_gap)}

    music_removed = {}
    for k, m in removed.items():
        pm = power(m)
        music_removed[k] = vs(original - m) | {"removed_in_speech_db": _diff(level(pm, ax.speech), o_sp),
                                               "removed_in_gap_db": _diff(level(pm, ax.gap), o_gap)}
    resid = original - sum(bandit_parts)
    return {
        "speech_s": round(ax.speech.sum() / ax.fps, 2), "gap_s": round(ax.gap.sum() / ax.fps, 2),
        "original_speech_dbfs": None if o_sp is None else round(o_sp, 2),
        "original_gap_dbfs": None if o_gap is None else round(o_gap, 2),
        "music_removed": music_removed,
        "dialogue_only": {k: vs(x) for k, x in dialogue.items()},
        "sum_residual_db": round(db(float(np.mean(resid ** 2))) - db(float(np.mean(original ** 2))), 2),
    }
