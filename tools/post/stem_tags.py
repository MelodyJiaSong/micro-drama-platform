# -*- coding: utf-8 -*-
"""独立的耳朵（P2 试验，tools/post/stems_trial.py 调）：AudioSet 声音分类器逐窗听一条音轨，回答「还听得见音乐吗」「扔掉的那条里有没有人声 / 动物 / 撞击」。

分离模型各有各的偏：实测 Bandit v2 把吼、尖叫、狗头人叽喳、乌鸦叫当音乐，BS-RoFormer 把乌鸦叫和一部分配乐当人声——
拿任何一个分离模型的输出当尺子去量另一个都是循环论证，所以用一个跟这两个训练目标无关的分类器当裁判。
模型：AST（MIT/ast-finetuned-audioset-10-10-0.4593，AudioSet 527 类，mAP 0.459，BSD-3-Clause），在 .venv-post 里跑（transformers），
权重首次用时从 Hugging Face 下（约 350 MB，缓存在 HF_HOME）。
窗：WIN_S 长、HOP_S 跳，16 kHz 单声道；模型原生吃 10.24 s，短窗由特征提取器补零。数字静音也有底分（Music ≈ 0.09），一律减掉静音底分再算。
*(judgment call — 窗取 2 s / 跳 1 s：1 s 窗太短、AST 分不清一声吼和一小节音乐；10 s 原生窗又太粗，一镜 22–28 s 只剩两三个窗，指不到秒。)*
"""
from __future__ import annotations

import functools
from dataclasses import dataclass

import numpy as np
import soxr

MODEL_ID = "MIT/ast-finetuned-audioset-10-10-0.4593"
MODEL_REV = "f826b80d28226b62986cc218e5cec390b1096902"      # 钉住 Hugging Face 上的版本：换了权重，分数就不能跟旧记录比
SR = 16000
WIN_S, HOP_S = 2.0, 1.0
EVENT_P = 0.30          # 扔掉的那条里，某窗非音乐类（去掉静音底分后）≥ 这个数＝听得出的非音乐内容被当音乐扔了
MUSIC_MIN = 0.02        # 原声整条的 music 分低于这个数＝本来就几乎没有音乐，「还剩几成」没有意义
CARD = {
    "file": f"{MODEL_ID}@{MODEL_REV[:7]}",
    "licence": "BSD-3-Clause（Hugging Face 模型卡）；transformers 代码 Apache-2.0",
    "why": "AudioSet 527 类里有 Music、Speech、Shout、Screaming、Grunt、Roar、Caw、Slam……一次就能问「还有没有音乐」和「扔掉的是不是人声 / 动物 / 撞击」；"
           "跟两个分离模型的训练目标无关，当裁判不循环",
}
INDICATORS = {
    "music": "整条的「音乐感」：各窗 AudioSet Music 概率减静音底分后的均值（2 s 窗 1 s 跳）。0＝分类器听不出音乐。"
             "标定（2026-09-30，shot03 的 Bandit 对白轨＋本镜 0–7 s 配乐循环铺满全条，按配乐比对白 RMS）：无配乐 0.000、−40 dB 0.19、"
             "−30 dB 0.38、−20 dB 0.44、0 dB 0.40——它测的是「有没有」而不是「多响」：低到 −40 dB 的残留也报得出，−25 dB 以上就饱和",
    "music_left": "去音乐候选的 music ÷ 原声的 music：还剩几成音乐感；原声本来几乎没有音乐（< MUSIC_MIN）时为 None",
    "removed_music": "被减掉的那条（音乐估计）的 music：高＝扔掉的确实是音乐",
    "removed_nonmusic": "被减掉的那条各窗非音乐分（说话 / 非言语人声 / 动物 / 撞击几组取最大，减静音底分）的均值：高＝有人声或音效被当音乐扔了",
    "removed_lost": "被减掉的那条里非音乐分 ≥ EVENT_P 的窗：时刻 + 最像的三类（原始概率）——这条配方会一起去掉的东西，逐条去听",
    "nonmusic": "（原声 / 只留人声的候选）各窗非音乐分的均值",
    "gated_bias": "逐秒择优（gated）就是拿这个分类器挑的，它自己的 music / music_left 偏乐观；它的独立检验是 ASR 与耳朵",
}
GROUPS = {              # AudioSet 类名 → 组；组分＝组内各类概率取最大
    "music": ("Music",),
    "speech": ("Speech",),
    "vocal": ("Shout", "Bellow", "Whoop", "Yell", "Battle cry", "Children shouting", "Screaming", "Grunt", "Groan", "Gasp",
              "Sigh", "Whimper", "Wail, moan", "Laughter", "Breathing", "Pant", "Snort", "Throat clearing"),
    "animal": ("Animal", "Roar", "Growling", "Howl", "Dog", "Canidae, dogs, wolves", "Squeak", "Rodents, rats, mice",
               "Wild animals", "Bird", "Caw", "Crow"),
    "impact": ("Slam", "Thump, thud", "Whack, thwack", "Smash, crash", "Bang", "Slap, smack", "Knock", "Wood",
               "Whoosh, swoosh, swish", "Walk, footsteps", "Crunch", "Scrape", "Breaking", "Clatter", "Thunk"),
}
NON_MUSIC = ("speech", "vocal", "animal", "impact")


@dataclass(frozen=True)
class Tags:
    t: np.ndarray                   # 各窗起点（秒）
    probs: np.ndarray               # (窗, 527) sigmoid 概率
    groups: dict[str, np.ndarray]   # 组 → (窗,) 组分，已减静音底分、截到 ≥ 0


class Tagger:
    """一个进程只加载一次模型。"""

    def __init__(self) -> None:
        import torch
        from transformers import ASTFeatureExtractor, ASTForAudioClassification
        self.torch = torch
        self.dev = "cuda" if torch.cuda.is_available() else "cpu"
        self.fe = ASTFeatureExtractor.from_pretrained(MODEL_ID, revision=MODEL_REV)
        self.model = ASTForAudioClassification.from_pretrained(MODEL_ID, revision=MODEL_REV).to(self.dev).eval()
        names = {v: int(k) for k, v in self.model.config.id2label.items()}
        missing = sorted(n for g in GROUPS.values() for n in g if n not in names)
        if missing:
            raise SystemExit(f"{MODEL_ID} 的类表里没有 {missing}：stem_tags.GROUPS 写错了类名")
        self.labels = self.model.config.id2label
        self.cols = {g: [names[n] for n in ns] for g, ns in GROUPS.items()}
        self.floor = {g: float(v[0]) for g, v in self._groups(self._probs(np.zeros(int(WIN_S * SR), np.float32))).items()}

    def _probs(self, y: np.ndarray) -> np.ndarray:
        n, h = int(WIN_S * SR), int(HOP_S * SR)
        starts = range(0, max(1, len(y) - n + 1), h)
        feats = self.fe([y[s:s + n] for s in starts], sampling_rate=SR, return_tensors="pt")["input_values"].to(self.dev)
        with self.torch.inference_mode():
            return self.torch.sigmoid(self.model(feats).logits).float().cpu().numpy()

    def _groups(self, p: np.ndarray) -> dict[str, np.ndarray]:
        return {g: p[:, c].max(axis=1) for g, c in self.cols.items()}

    def tags(self, x: np.ndarray, sr: int) -> Tags:
        """x：(n, ch) float32 → 逐窗标注。"""
        y = soxr.resample(np.ascontiguousarray(x.mean(axis=1)), sr, SR).astype(np.float32)
        p = self._probs(y)
        g = {k: np.clip(v - self.floor[k], 0.0, None) for k, v in self._groups(p).items()}
        return Tags(np.arange(len(p)) * HOP_S, p, g)

    def top(self, row: np.ndarray, k: int = 3) -> list[tuple[str, float]]:
        return [(self.labels[int(i)], round(float(row[i]), 2)) for i in np.argsort(-row)[:k]]


@functools.cache
def tagger() -> Tagger:
    return Tagger()


def music_score(tg: Tags) -> float:
    """整条的「音乐感」：各窗 Music 分（减静音底分）的均值。"""
    return round(float(tg.groups["music"].mean()), 3)


def nonmusic(tg: Tags) -> np.ndarray:
    """各窗非音乐内容分：人声 / 动物 / 撞击几组里最大的那组。"""
    return np.max([tg.groups[g] for g in NON_MUSIC], axis=0)


def lost_events(tg: Tags) -> list[dict]:
    """被当音乐扔掉的那条里，非音乐分 ≥ EVENT_P 的窗：时刻、最像的几类。"""
    nm = nonmusic(tg)
    tag = tagger()
    return [{"t": [float(tg.t[i]), float(tg.t[i] + WIN_S)], "p": round(float(nm[i]), 2), "top": tag.top(tg.probs[i])}
            for i in np.flatnonzero(nm >= EVENT_P)]
