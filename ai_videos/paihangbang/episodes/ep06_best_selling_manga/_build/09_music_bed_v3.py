# -*- coding: utf-8 -*-
"""ep06 配乐底轨 v3：Suno 任务 b3cf1124（2026-11-04，用户说 Suno 恢复后重做）只用一首 A3（2:54.5，约 155 BPM，无停顿；结尾满电平急停，靠渲染器 3 s 淡出收）。

为什么不再拼两首（08_music_bed.py）：旧底轨是两首不同 BPM（154 / 159）的歌 0.4 s 硬接，接点换速；
v3 这次的第二首只有 103 BPM，更接不上。改为在 A3 内部找一个跳回点：播 A3[0:t2]，再从 t1 接着播到 A3 结尾
—— 中段多放一遍，结尾仍是原曲最后的高潮。

找点（需要系统 Python 的 librosa；仓库 .venv 没装）：
1. librosa 节拍跟踪得到每拍时刻；跳回点只落在拍点上，t2 - t1 取 4 拍的整数倍（保持小节相位）。
2. 每拍聚合 chroma（和声）与 MFCC（音色），比较 t1、t2 前后各 8 拍的余弦相似度，取最高分。
   （先试过不限整小节的频谱相似度、起音包络、拍相位，均噪声太大或挑出错拍的点，见 qc.md「配乐 v3」。）
3. 波形互相关在 ±3 ms 内微调，30 ms 等功率交叉淡化（两侧对齐到同一时刻）。
4. 总长超出视频时从开头裁掉多余（渲染器开头 1 s 本来就淡入）。
验证：对输出底轨重新跑节拍跟踪，看接点前后的拍间隔与全曲是否一致。

    python ai_videos/paihangbang/episodes/ep06_best_selling_manga/_build/09_music_bed_v3.py
    python -m rank_scroll render <ep> [--allow-risk-images] --music <ep>/assets/music/ep06_music_bed_v3.wav
"""
import json
import subprocess
from pathlib import Path

import librosa
import numpy as np

EP = Path(__file__).resolve().parents[1]
SRC = EP / "assets" / "music" / "v3" / "6904ff75-7d62-43b1-8fb1-24dce0a4c1b6.mp3"
OUT = EP / "assets" / "music" / "ep06_music_bed_v3.wav"
VIDEO_S = 217.467          # 时间线总长（13048 帧 / 60）
SR_A, HOP = 22050, 512
SR = 48000
XFADE = 0.03
CTX = 8                    # 比较跳回点前后各几拍
T1_RANGE = (20.0, 125.0)   # 跳回目标只在前中段，保住最后一分钟的高潮
MAX_EXTRA = 8.0            # 最多比需要多重复几秒（多出的从开头裁掉）


def load(sr: int, mono: bool) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(SRC), "-ac", "1" if mono else "2", "-ar", str(sr),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32)
    return x if mono else x.reshape(-1, 2).copy()


def beat_track(y: np.ndarray) -> tuple[float, np.ndarray]:
    tempo, beats = librosa.beat.beat_track(y=y, sr=SR_A, hop_length=HOP, start_bpm=155, tightness=400)
    return float(np.atleast_1d(tempo)[0]), beats


def beat_features(y: np.ndarray, beats: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    chroma = librosa.feature.chroma_cqt(y=y, sr=SR_A, hop_length=HOP)
    mfcc = librosa.feature.mfcc(y=y, sr=SR_A, hop_length=HOP, n_mfcc=20)[1:]
    def sync(f):
        s = librosa.util.sync(f, beats, aggregate=np.median).T
        s = s - s.mean(1, keepdims=True) if f is mfcc else s
        return s / (np.linalg.norm(s, axis=1, keepdims=True) + 1e-9)
    return sync(chroma), sync(mfcc)


def main() -> None:
    y = load(SR_A, True)
    src_s = len(y) / SR_A
    need = VIDEO_S - src_s
    tempo, beats = beat_track(y)
    bt = librosa.frames_to_time(beats, sr=SR_A, hop_length=HOP)
    ch, mf = beat_features(y, beats)          # sync 后第 k 行 = 第 k-1 拍到第 k 拍之间（第 0 行是首拍之前）
    nb = len(bt)

    def score(i: int, j: int) -> float:
        a, b = ch[i - CTX + 1:i + CTX + 1], ch[j - CTX + 1:j + CTX + 1]
        c, d = mf[i - CTX + 1:i + CTX + 1], mf[j - CTX + 1:j + CTX + 1]
        return 0.5 * float(np.einsum("ij,ij->i", a, b).mean()) + 0.5 * float(np.einsum("ij,ij->i", c, d).mean())

    cands, base = [], []
    for i in range(CTX, nb - CTX - 1):
        if not T1_RANGE[0] <= bt[i] <= T1_RANGE[1]:
            continue
        for j in range(i + 4, nb - CTX - 1, 4):
            gap = bt[j] - bt[i]
            if gap < need:
                if gap > 8:
                    base.append(score(i, j))
                continue
            if gap > need + MAX_EXTRA:
                break
            cands.append((score(i, j), i, j))
    cands.sort(reverse=True)
    s, i, j = cands[0]
    t1, t2 = float(bt[i]), float(bt[j])

    x = load(SR, False)
    m = x.mean(1)
    a, b = int(round(t1 * SR)), int(round(t2 * SR))
    w, r = int(0.05 * SR), int(0.003 * SR)
    ref = m[b - w:b + w]
    cc = [float(np.dot(ref, m[a + k - w:a + k + w])) / (np.linalg.norm(m[a + k - w:a + k + w]) + 1e-9)
          for k in range(-r, r + 1)]
    a += int(np.argmax(cc)) - r

    n = int(XFADE * SR)
    ph = np.linspace(0, np.pi / 2, n, dtype=np.float32)[:, None]
    joined = np.concatenate([x[:b - n], x[b - n:b] * np.cos(ph) + x[a - n:a] * np.sin(ph), x[a:]])
    surplus = len(joined) / SR - VIDEO_S
    if surplus > 0:
        joined = joined[int(round(surplus * SR)):]
    joined = joined[:int(round(VIDEO_S * SR))]
    splice_out = b / SR - max(surplus, 0)

    pcm = (np.clip(joined, -1, 1) * 32767).astype("<i2").tobytes()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", "-",
                    "-c:a", "pcm_s16le", str(OUT)], input=pcm, check=True)

    # 验证：输出底轨重新跟拍，接点前后各 6 拍的拍间隔与全曲中位数比
    yo = librosa.resample(joined.mean(1), orig_sr=SR, target_sr=SR_A)
    _, bo = beat_track(yo)
    bto = librosa.frames_to_time(bo, sr=SR_A, hop_length=HOP)
    ioi = np.diff(bto)
    med = float(np.median(ioi))
    k = int(np.searchsorted(bto, splice_out))
    near = ioi[max(k - 6, 0):k + 6]
    info = {"source": SRC.name, "source_s": round(src_s, 3), "tempo_bpm": round(tempo, 2),
            "jump_from_s": round(t2, 3), "jump_to_s": round(a / SR, 3), "repeat_s": round(t2 - a / SR, 3),
            "repeat_beats": int(j - i), "score": round(s, 4),
            "score_baseline_median": round(float(np.median(base)), 4), "score_baseline_p99": round(float(np.percentile(base, 99)), 4),
            "next_best": [[round(c[0], 4), round(float(bt[c[1]]), 2), round(float(bt[c[2]]), 2)] for c in cands[1:4]],
            "trim_start_s": round(max(surplus, 0), 3), "splice_in_output_s": round(splice_out, 3),
            "verify_ioi_median_s": round(med, 4),
            "verify_ioi_near_splice_max_dev_ms": round(float(np.max(np.abs(near - med))) * 1000, 1),
            "verify_ioi_overall_p95_dev_ms": round(float(np.percentile(np.abs(ioi - med), 95)) * 1000, 1),
            "out_s": round(len(joined) / SR, 3), "out": OUT.name}
    print(json.dumps(info, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
