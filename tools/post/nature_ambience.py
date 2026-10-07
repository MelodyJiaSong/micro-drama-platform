"""无对白建立镜的可追溯自然环境声；仅噪声和鸟啁啾，无外部录音。"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import wave
from pathlib import Path

import numpy as np


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def band_noise(rng, count, rate, low, high):
    signal = rng.standard_normal(count)
    spectrum = np.fft.rfft(signal)
    frequencies = np.fft.rfftfreq(count, 1 / rate)
    spectrum *= ((frequencies >= low) & (frequencies <= high))
    signal = np.fft.irfft(spectrum, n=count)
    return signal / max(float(np.std(signal)), 1e-9)


def synthesize(seconds: float, seed: int = 106, rate: int = 48000):
    rng = np.random.default_rng(seed)
    count = round(seconds * rate)
    t = np.arange(count) / rate
    channels = []
    for _ in range(2):
        # Distant stream and sparse leaf rustle, with no vocal/music samples.
        stream = band_noise(rng, count, rate, 250, 6500) * 0.003
        wind = band_noise(rng, count, rate, 80, 1400)
        wind *= 0.002 * (0.65 + 0.35 * np.sin(t * 0.73 + rng.uniform(0, 6)))
        channels.append(stream + wind)
    signal = np.column_stack(channels)
    events = []
    for start, length, f0, f1, pan in [(1.2, .14, 3100, 4400, .2), (1.49, .11, 3900, 2800, .2),
                                        (5.7, .19, 2700, 4700, .75), (9.1, .12, 4500, 3400, .35),
                                        (9.37, .09, 3300, 4800, .35), (13.2, .16, 2900, 4300, .7)]:
        if start + length >= seconds - 1:
            continue
        n = round(length * rate)
        u = np.arange(n) / rate
        phase = 2 * np.pi * (f0 * u + .5 * (f1 - f0) / length * u**2)
        chirp = np.sin(phase) * np.sin(np.pi * u / length)**2 * .009
        a = round(start * rate)
        signal[a:a+n, 0] += chirp * np.sqrt(1 - pan)
        signal[a:a+n, 1] += chirp * np.sqrt(pan)
        events.append({"start_s": start, "duration_s": length, "frequency_hz": [f0, f1], "kind": "非节拍鸟啁啾"})
    fade_in = np.minimum(t / .3, 1)
    fade_out = np.clip((seconds - t) / .8, 0, 1)**3
    signal *= (fade_in * fade_out)[:, None]
    pcm = np.rint(np.clip(signal, -.95, .95) * 32767).astype("<i2")
    return pcm, events


def video_hash(path: Path) -> str:
    return subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:v:0", "-c", "copy", "-f", "hash", "-hash", "sha256", "-"], capture_output=True, text=True, check=True).stdout.strip()


def replace(source: Path, output: Path, seed: int = 106):
    seconds = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(source)], capture_output=True, text=True, check=True).stdout)
    pcm, events = synthesize(seconds, seed)
    wav = output.with_suffix(".ambience.wav")
    with wave.open(str(wav), "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(48000)
        f.writeframes(pcm.tobytes())
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(source), "-i", str(wav), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", str(seconds), "-movflags", "+faststart", str(output)], check=True)
    assert video_hash(source) == video_hash(output), "画面码流改变，不能沿用画面证据"
    decoded = subprocess.run(["ffmpeg", "-v", "error", "-i", str(output), "-map", "0:a:0", "-ac", "2", "-ar", "48000", "-f", "s16le", "-"], capture_output=True, check=True).stdout
    actual = np.frombuffer(decoded, dtype="<i2").reshape(-1, 2).astype(float)
    count = min(len(actual), len(pcm))
    expected = pcm[:count].astype(float)
    error = actual[:count] - expected
    snr = float(10 * np.log10(np.mean(expected**2) / max(np.mean(error**2), 1e-9)))
    assert snr >= 15, "合成源与实际音轨不一致"
    report = {"method": "procedural_nature_ambience", "source_video": str(source.resolve()), "source_sha256": sha(source),
              "output_sha256": sha(output), "wav_sha256": sha(wav), "script_sha256": sha(Path(__file__)), "seed": seed,
              "rate": 48000, "seconds": seconds, "events": events, "external_samples": [], "speech_sources": [], "music_sources": [],
              "layers": ["80–1400Hz低电平风叶滤波噪声", "250–6500Hz远水滤波噪声", "不构成拍子/旋律的短鸟啁啾"],
              "fade_out_s": .8, "video_bitstream_unchanged": True, "decoded_audio_snr_db": snr,
              "limitation": "代码和回读证明内容来源、无语音/BGM输入及淡出；环境不支持听音，不能据此声称主观音效品质已听审。"}
    output.with_suffix(".audio_provenance.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("source", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--seed", type=int, default=106)
    args = p.parse_args()
    print(json.dumps(replace(args.source, args.output, args.seed), ensure_ascii=False))
